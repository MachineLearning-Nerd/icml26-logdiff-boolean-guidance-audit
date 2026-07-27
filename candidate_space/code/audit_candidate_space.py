#!/usr/bin/env python3
"""Evaluator-blind structural audit for the additive Hugging Face candidate."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote


TEXT_SUFFIXES = {
    ".css",
    ".html",
    ".js",
    ".json",
    ".lock",
    ".md",
    ".py",
    ".svg",
    ".toml",
    ".txt",
}
MUTABLE_ENTRYPOINTS = {"README.md", "logbook.json", "pages/index.md"}
LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
SECRET_PATTERNS = {
    "hugging_face_token": re.compile(r"\bhf_[A-Za-z0-9]{20,}\b"),
    "github_token": re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}\b"),
    "bearer_token": re.compile(r"\bBearer\s+[A-Za-z0-9._~-]{16,}\b", re.IGNORECASE),
    "aws_access_key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def flatten_pages(node: dict) -> dict[str, str]:
    pages: dict[str, str] = {}
    for child in node.get("children", []):
        pages[child["slug"]] = child["file"]
        pages.update(flatten_pages(child))
    return pages


def parse_judged_manifest(path: Path) -> dict[str, str]:
    result = {}
    for line in path.read_text().splitlines():
        digest, relative = line.split("  ", 1)
        result[relative] = digest
    return result


def resolve_link(space: Path, source: Path, raw_target: str, routes: dict[str, str]) -> Path | None:
    target = raw_target.strip().split(" ", 1)[0].strip("<>")
    if target.startswith(("http://", "https://", "mailto:")) or target == "":
        return None
    if target.startswith("#/"):
        slug = target[2:].split("#", 1)[0]
        if slug not in routes:
            raise ValueError(f"unknown route {target} from {source.relative_to(space)}")
        return space / routes[slug]
    if target.startswith("#"):
        return None
    target = unquote(target.split("#", 1)[0].split("?", 1)[0])
    return (source.parent / target).resolve()


def main() -> None:
    if len(sys.argv) != 4:
        raise SystemExit(
            "usage: audit_candidate_space.py CANDIDATE_DIR JUDGED_MANIFEST OUTPUT_DIR"
        )
    space = Path(sys.argv[1]).resolve()
    judged_manifest_path = Path(sys.argv[2]).resolve()
    output = Path(sys.argv[3]).resolve() / "release"
    output.mkdir(parents=True, exist_ok=True)
    failures: list[str] = []

    try:
        logbook = json.loads((space / "logbook.json").read_text())
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"invalid candidate logbook: {exc}")
    routes = flatten_pages(logbook["root"])
    routes[logbook["root"]["slug"]] = logbook["root"]["file"]
    children = logbook["root"].get("children", [])
    if not children or children[0].get("slug") != "current-cumulative-verification":
        failures.append("current_cumulative_not_first")

    judged = parse_judged_manifest(judged_manifest_path)
    candidate_paths = {
        path.relative_to(space).as_posix(): path
        for path in space.rglob("*")
        if path.is_file()
    }
    missing_old_paths = sorted(set(judged) - set(candidate_paths))
    if missing_old_paths:
        failures.append("judged_file_set_not_subset")
    changed_historical_pages = []
    for relative, expected in judged.items():
        if relative.startswith("pages/") and relative != "pages/index.md":
            path = candidate_paths.get(relative)
            if path is not None and sha256(path) != expected:
                changed_historical_pages.append(relative)
    if changed_historical_pages:
        failures.append("historical_page_changed")

    json_failures = []
    for relative, path in candidate_paths.items():
        if path.suffix == ".json":
            try:
                json.loads(path.read_text())
            except (UnicodeDecodeError, json.JSONDecodeError):
                json_failures.append(relative)
    if json_failures:
        failures.append("invalid_json")

    opened: list[str] = []
    broken_links: list[dict[str, str]] = []
    queue = [space / "README.md", space / "pages/index.md"]
    seen: set[Path] = set()
    while queue:
        source = queue.pop(0).resolve()
        if source in seen:
            continue
        seen.add(source)
        if not source.is_file() or space not in source.parents:
            broken_links.append({"source": "entrypoint", "target": str(source)})
            continue
        opened.append(source.relative_to(space).as_posix())
        if source.suffix not in {".md", ".html"}:
            continue
        text = source.read_text(errors="strict")
        for raw_target in LINK_RE.findall(text):
            try:
                resolved = resolve_link(space, source, raw_target, routes)
            except ValueError:
                broken_links.append(
                    {"source": source.relative_to(space).as_posix(), "target": raw_target}
                )
                continue
            if resolved is None:
                continue
            if not resolved.is_file() or (resolved != space and space not in resolved.parents):
                broken_links.append(
                    {"source": source.relative_to(space).as_posix(), "target": raw_target}
                )
                continue
            if resolved.suffix in {".md", ".html"}:
                queue.append(resolved)
            elif resolved.relative_to(space).as_posix() not in opened:
                opened.append(resolved.relative_to(space).as_posix())
    if broken_links:
        failures.append("broken_reachable_links")

    cumulative = (space / "pages/current-cumulative-verification/page.md").read_text()
    visibility_rows = {}
    for line in cumulative.splitlines():
        match = re.match(r"\|\s*([1-5])\s*\|(.+)\|", line)
        if match and "Canonical page" not in line:
            cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
            if len(cells) == 9:
                visibility_rows[match.group(1)] = cells
    if set(visibility_rows) != set("12345"):
        failures.append("visibility_matrix_claim_rows")
    elif any(
        any(value in {"", "No", "Missing", "INCONCLUSIVE"} for value in row[1:])
        for row in visibility_rows.values()
    ):
        failures.append("visibility_matrix_missing_cell")

    required_opened = {
        "README.md",
        "pages/index.md",
        "pages/current-cumulative-verification/page.md",
        "pages/current-claim-3-celeba-verification/page.md",
        "pages/current-claim-4-molecular-verification/page.md",
        "code/run_logdiff.py",
        "code/check_baseline_artifacts.py",
        "code/check_claim3_release.py",
        "code/check_claim4_evidence.py",
        "code/audit_candidate_space.py",
        "environment/pyproject.toml",
        "environment/uv.lock",
        "evidence/run-07daf77f-summary.json",
    }
    missing_from_traversal = sorted(required_opened - set(opened))
    if missing_from_traversal:
        failures.append("required_evidence_not_reachable")

    changed_or_new = []
    for relative, path in sorted(candidate_paths.items()):
        if relative not in judged or sha256(path) != judged[relative]:
            changed_or_new.append(relative)
    non_text_uploads = [
        relative for relative in changed_or_new if Path(relative).suffix not in TEXT_SUFFIXES
    ]
    if non_text_uploads:
        failures.append("non_text_candidate_change")

    secret_hits = []
    for relative in changed_or_new:
        path = candidate_paths[relative]
        if path.suffix not in TEXT_SUFFIXES:
            continue
        text = path.read_text(errors="strict")
        for name, pattern in SECRET_PATTERNS.items():
            if pattern.search(text):
                secret_hits.append({"path": relative, "pattern": name})
    if secret_hits:
        failures.append("secret_pattern")

    candidate_manifest = [
        f"{sha256(path)}  {relative}" for relative, path in sorted(candidate_paths.items())
    ]
    upload_allowlist = [
        relative
        for relative in changed_or_new
        if Path(relative).suffix in TEXT_SUFFIXES
        and relative not in {"release/candidate_manifest.sha256", "release/upload_allowlist.txt"}
    ]
    (output / "candidate_manifest.sha256").write_text("\n".join(candidate_manifest) + "\n")
    (output / "upload_allowlist.txt").write_text("\n".join(upload_allowlist) + "\n")

    result = {
        "checker": "evaluator-blind candidate traversal and release audit",
        "status": "PASS" if not failures else "FAIL",
        "failures": failures,
        "canonical_entrypoint": "README.md -> pages/index.md -> current cumulative verification",
        "files_opened": opened,
        "conclusions_not_verified": [],
        "broken_links": broken_links,
        "missing_from_traversal": missing_from_traversal,
        "judged_manifest_entries": len(judged),
        "candidate_file_entries": len(candidate_paths),
        "old_file_set_subset": not missing_old_paths,
        "missing_old_paths": missing_old_paths,
        "historical_pages_unchanged": not changed_historical_pages,
        "changed_historical_pages": changed_historical_pages,
        "json_files_checked": sum(path.suffix == ".json" for path in candidate_paths.values()),
        "invalid_json_files": json_failures,
        "visibility_claim_rows": len(visibility_rows),
        "non_text_uploads": non_text_uploads,
        "secret_hits": secret_hits,
        "upload_allowlist_entries": len(upload_allowlist),
    }
    (output / "candidate_audit.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
