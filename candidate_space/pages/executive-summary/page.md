# Executive summary


---
<!-- trackio-cell
{"type": "markdown", "id": "cell_940fd9780f56", "created_at": "2026-07-19T18:56:29+00:00", "title": "Executive summary", "pinned": true, "pinned_at": "2026-07-19T19:02:00+00:00"}
-->
This campaign audits the five challenge-anchored claims against arXiv:2602.05549 and the pinned author release at 94ef35bafd4b4239e9832d8295128c09e8fc1472.

| Claim | Verdict | Direct evidence |
| --- | --- | --- |
| C1 exact logical-score calculus | VERIFIED | 6,350 exhaustive compiled formulas, 100 primitive checks, finite-difference and real trained-UNet algebra checks |
| C2 recursive CMNIST and Shapes3D range statement | FALSIFIED AS WRITTEN | Only 2 of 8 LOGDIFF cells are within 94-98 percent; only 5 of 8 constant-baseline cells are within 63-77 percent |
| C3 CelebA negation FID and conformity | TABLE TRANSCRIPTION MATCHES; EMPIRICAL RUN BLOCKED BY RELEASE | All nine declared checkpoints are absent; the released config is broken; released FID code differs from the paper protocol |
| C4 GRM5-RRM1 molecular result | FULL-SCALE RECOVERY IN PROGRESS | Exact pair, released TargetDiff and property weights, real sampler, and AutoDock Vina are independently recovered and executable |
| C5 Proposition C.2 completeness | VERIFIED | 20,650 independent-product events plus 6,350 taxonomy events; errors at floating-point roundoff; invalid overlap rejected |

A falsified claim is not converted into a success: the logbook records what the paper tables and executable evidence actually show.


---
<!-- trackio-cell
{"type": "figure", "id": "cell_7107877f27f0", "created_at": "2026-07-19T19:02:59+00:00", "title": "Reproduction poster", "pinned": true, "pinned_at": "2026-07-19T19:03:00+00:00"}
-->
[Poster source: poster_embed.html](https://huggingface.co/spaces/DineshAI/OAM1jJsMGp/blob/main/poster_embed.html)

````html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>LOGDIFF independent reproduction evidence</title>
<style>
  @page { size: A2 portrait; margin: 0; }
  :root {
    /* ===== DESIGN TOKENS ===== */
    --navy: #173653;
    --blue: #2D5F8B;
    --pale: #E8F1F8;
    --gold: #C9A24A;
    --ink: #1A1A1A;
    --muted: #5E6570;
    --paper: #F6F3F0;
    --white: #FFFFFF;
    --line: #CDD5DD;
    --green: #176B4D;
    --red: #9B2F35;
    --orange: #8A5417;
    --u: 1.6px;
    --font-sans: "Inter", "Helvetica Neue", sans-serif;
    --font-serif: "Charter", "Source Serif Pro", Georgia, serif;
    --fs-1: calc(4.7 * var(--u));
    --fs-2: calc(5.4 * var(--u));
    --fs-3: calc(6 * var(--u));
    --fs-4: calc(7 * var(--u));
    --fs-5: calc(8 * var(--u));
    --fs-6: calc(9 * var(--u));
    --fs-7: calc(10 * var(--u));
    --fs-8: calc(13 * var(--u));
    --fs-9: calc(18 * var(--u));
    --shadow-screen: 0 0 40px rgba(0, 0, 0, 0.4);
    /* ===== END DESIGN TOKENS ===== */
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  p, li, dd, figcaption, .body-text, .section-title { text-wrap: pretty; }
  .title { text-wrap: balance; }
  html, body { background: var(--ink); color: var(--ink); font-family: var(--font-serif); }
  .poster {
    width: calc(420 * var(--u));
    height: calc(594 * var(--u));
    margin: 20px auto;
    padding: calc(8 * var(--u)) calc(10 * var(--u));
    background: var(--paper);
    display: grid;
    grid-template-rows: auto auto minmax(0, 1fr) auto auto;
    gap: calc(8 * var(--u));
    overflow: hidden;
    box-shadow: var(--shadow-screen);
  }
  .header {
    border-top: calc(4 * var(--u)) solid var(--blue);
    border-bottom: calc(1 * var(--u)) solid var(--blue);
    padding: calc(4 * var(--u)) calc(2 * var(--u));
  }
  .eyebrow { color: var(--blue); font: 800 var(--fs-3)/1.1 var(--font-sans); letter-spacing: 1.1px; text-transform: uppercase; }
  .title { color: var(--navy); font: 800 var(--fs-9)/1.05 var(--font-sans); margin-top: calc(2 * var(--u)); }
  .title .accent { color: var(--orange); }
  .subtitle { color: var(--muted); font: 500 var(--fs-4)/1.25 var(--font-sans); margin-top: calc(2 * var(--u)); }
  .meta { color: var(--blue); font: 650 var(--fs-3)/1.25 var(--font-sans); margin-top: calc(2 * var(--u)); }
  .banner {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: calc(3 * var(--u));
  }
  .banner-item { background: var(--navy); color: var(--white); border-radius: calc(1.5 * var(--u)); padding: calc(3 * var(--u)); text-align: center; }
  .banner-num { color: var(--gold); font: 800 var(--fs-7)/1 var(--font-sans); }
  .banner-label { color: var(--pale); font: 600 var(--fs-2)/1.2 var(--font-sans); margin-top: calc(1 * var(--u)); }
  .body-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: calc(5 * var(--u)); min-height: 0; }
  .column { display: grid; grid-template-rows: repeat(3, minmax(0, 1fr)); gap: calc(4 * var(--u)); min-height: 0; }
  .card { background: var(--white); border: calc(0.4 * var(--u)) solid var(--line); border-left: calc(2.5 * var(--u)) solid var(--blue); border-radius: calc(1.5 * var(--u)); padding: calc(4 * var(--u)); overflow: hidden; }
  .card.caution { border-left-color: var(--orange); }
  .card.verified { border-left-color: var(--green); }
  .card.falsified { border-left-color: var(--red); }
  .section-title { color: var(--navy); font: 800 var(--fs-5)/1.12 var(--font-sans); margin-bottom: calc(2 * var(--u)); }
  .status { display: inline-block; color: var(--white); border-radius: calc(0.8 * var(--u)); padding: calc(0.6 * var(--u)) calc(1.5 * var(--u)); font: 800 var(--fs-1)/1 var(--font-sans); margin-bottom: calc(2 * var(--u)); }
  .status.ok { background: var(--green); }
  .status.no { background: var(--red); }
  .status.partial { background: var(--orange); }
  .body-text, .card li { font-size: var(--fs-2); line-height: 1.34; }
  .body-text + .body-text { margin-top: calc(1.5 * var(--u)); }
  .card ul { padding-left: calc(8 * var(--u)); }
  .card li + li { margin-top: calc(1 * var(--u)); }
  .metric { color: var(--blue); font-weight: 800; white-space: nowrap; }
  table { width: 100%; border-collapse: collapse; font: 600 var(--fs-1)/1.15 var(--font-sans); margin-top: calc(2 * var(--u)); }
  th, td { padding: calc(1.2 * var(--u)); border-bottom: calc(0.3 * var(--u)) solid var(--line); text-align: right; }
  th:first-child, td:first-child { text-align: left; }
  th { color: var(--white); background: var(--blue); }
  .range-note { color: var(--red); font: 750 var(--fs-2)/1.2 var(--font-sans); margin-top: calc(2 * var(--u)); }
  .takeaway { background: var(--pale); border: calc(0.5 * var(--u)) solid var(--blue); border-radius: calc(1.5 * var(--u)); padding: calc(3 * var(--u)) calc(5 * var(--u)); color: var(--navy); font: 750 var(--fs-3)/1.25 var(--font-sans); }
  .footer { display: grid; grid-template-columns: 1fr auto; gap: calc(5 * var(--u)); color: var(--muted); font: 600 var(--fs-2)/1.2 var(--font-sans); padding: 0 calc(2 * var(--u)); }
  .footer .right { color: var(--blue); }
  @media print {
    :root { --u: 1mm; }
    html, body { background: var(--white); margin: 0; width: 100%; height: 100%; overflow: hidden; }
    .poster { margin: 0; box-shadow: none; page-break-after: avoid; }
  }
</style>
</head>
<body>
<main class="poster" data-measure-role="poster">
  <header class="header" data-measure-role="header">
    <div class="eyebrow">ICML 2026 Agent Reproduction Challenge · OpenReview OAM1jJsMGp</div>
    <h1 class="title">LOGDIFF: <span class="accent">claim-specific evidence</span>, not one blanket verdict</h1>
    <p class="subtitle">Independent reconstruction of exact Boolean guidance, source-scale CMNIST classifiers, release boundaries, and the GRM5-RRM1 molecular pipeline.</p>
    <p class="meta">Pinned LOGDIFF source 94ef35b · pinned FKC source aa6f5ed · zero-cost local execution</p>
  </header>

  <section class="banner" data-measure-role="banner">
    <div class="banner-item"><div class="banner-num">27,000</div><div class="banner-label">C5 semantic events exhausted</div></div>
    <div class="banner-item"><div class="banner-num">70,000</div><div class="banner-label">fixed-timestep test predictions per attribute pair</div></div>
    <div class="banner-item"><div class="banner-num">3 / 3</div><div class="banner-label">molecular artifacts hash-verified</div></div>
  </section>

  <section class="body-grid" data-measure-role="body">
    <div class="column" data-measure-role="column">
      <article class="card verified" data-measure-role="card">
        <div class="status ok">C1 VERIFIED</div>
        <h2 class="section-title">Exact Boolean guidance</h2>
        <p class="body-text">An independent full-joint oracle agrees with recursive LOGDIFF evaluation across <span class="metric">6,350 formulas</span> and <span class="metric">100 primitive checks</span>.</p>
        <ul>
          <li>Max probability error: <span class="metric">2.22e-16</span></li>
          <li>Max score error: <span class="metric">3.33e-16</span></li>
          <li>Finite-difference error: <span class="metric">5.21e-10</span></li>
          <li>Real trained-UNet OR-ME and NOT algebra also matches direct mixtures.</li>
        </ul>
      </article>

      <article class="card falsified" data-measure-role="card">
        <div class="status no">C2 FALSIFIED AS WRITTEN</div>
        <h2 class="section-title">Table 2 contradicts the anchored ranges</h2>
        <table>
          <thead><tr><th>Method / data</th><th>N2</th><th>N3</th><th>N4</th><th>N5</th></tr></thead>
          <tbody>
            <tr><td>LOGDIFF CMNIST</td><td>93.8</td><td>93.3</td><td>94.2</td><td>94.4</td></tr>
            <tr><td>LOGDIFF Shapes3D</td><td>88.8</td><td>88.6</td><td>85.1</td><td>87.6</td></tr>
            <tr><td>Constant CMNIST</td><td>76.1</td><td>66.7</td><td>68.3</td><td>75.2</td></tr>
            <tr><td>Constant Shapes3D</td><td>67.2</td><td>59.4</td><td>58.4</td><td>57.9</td></tr>
          </tbody>
        </table>
        <p class="range-note">Only 2/8 LOGDIFF cells fall in 94-98%; only 5/8 constant cells fall in 63-77%.</p>
      </article>

      <article class="card caution" data-measure-role="card">
        <div class="status partial">C3 RELEASE-BOUND</div>
        <h2 class="section-title">CelebA numbers transcribe; protocol does not execute</h2>
        <ul>
          <li>Paper table: negation FID <span class="metric">23.61 vs 32.87</span>.</li>
          <li>All nine declared model/classifier checkpoints are absent.</li>
          <li>Requested CelebA dataset YAML is missing; only a copy-suffixed file exists.</li>
          <li>Paper specifies clean-fid on 5,000 samples; source imports TorchMetrics FID and records 500,000 by default.</li>
        </ul>
      </article>
    </div>

    <div class="column" data-measure-role="column">
      <article class="card caution" data-measure-role="card">
        <div class="status partial">C4 FULL-SCALE RECOVERY</div>
        <h2 class="section-title">GRM5-RRM1 pipeline now executes</h2>
        <ul>
          <li>Exact pair: <span class="metric">29 / 371</span>, UniProt P41594 / P23921.</li>
          <li>Released TargetDiff: <span class="metric">2.84M</span> parameters.</li>
          <li>Property model: <span class="metric">2.55M</span> parameters.</li>
          <li>Real SO(3)-equivariant sampler passes on the GRM5 pocket.</li>
          <li>Real Vina reference docking: <span class="metric">-5.050</span> and <span class="metric">-7.587 kcal/mol</span>.</li>
        </ul>
        <p class="body-text">The 32-ligand, size-23, 1,000-step, beta-2.0 campaign remains active; no paper metric is claimed from a smoke test.</p>
      </article>

      <article class="card verified" data-measure-role="card">
        <div class="status ok">C5 VERIFIED</div>
        <h2 class="section-title">Proposition C.2 completeness certificate</h2>
        <table>
          <thead><tr><th>Constructive case</th><th>Events</th><th>Score error</th></tr></thead>
          <tbody>
            <tr><td>Independent groups</td><td>20,650</td><td>3.33e-16</td></tr>
            <tr><td>Nested / ME taxonomy</td><td>6,350</td><td>2.22e-16</td></tr>
          </tbody>
        </table>
        <p class="body-text">Twenty-five posterior settings are used. An overlapping pair that is neither nested nor mutually exclusive is rejected by the fail-closed control.</p>
      </article>

      <article class="card verified" data-measure-role="card">
        <div class="status ok">SOURCE-SCALE TRAINING</div>
        <h2 class="section-title">Missing CMNIST classifier rebuilt exactly</h2>
        <p class="body-text">The pinned author trainer completed <span class="metric">50 epochs</span> over all <span class="metric">60,000</span> source training examples and produced the expected epoch=49-step=2950 checkpoint.</p>
        <table>
          <thead><tr><th>Noise time</th><th>Digit</th><th>Colour</th></tr></thead>
          <tbody>
            <tr><td>t = 0</td><td>97.56%</td><td>100.00%</td></tr>
            <tr><td>t = 100</td><td>96.38%</td><td>99.98%</td></tr>
            <tr><td>t = 500</td><td>33.89%</td><td>48.82%</td></tr>
            <tr><td>t = 999</td><td>10.64%</td><td>10.79%</td></tr>
          </tbody>
        </table>
      </article>
    </div>
  </section>

  <section class="takeaway" data-measure-role="footer-strip">Bottom line: exactness and completeness survive exhaustive tests; the recursive range statement does not; empirical image and molecule claims stay explicitly bounded by what their released artifacts can support.</section>
  <footer class="footer" data-measure-role="footer"><div>Reproduction evidence · DineshAI/OAM1jJsMGp · arXiv:2602.05549</div><div class="right">Audited 20 July 2026</div></footer>
</main>
</body>
</html>

````


---
<!-- trackio-cell
{"type": "dashboard", "id": "cell_d1d0bf10fcd2", "created_at": "2026-07-19T19:05:46+00:00", "title": "Dashboard: reproduction-logdiff", "dashboard_project": "reproduction-logdiff"}
-->
**🎯 Trackio dashboard** `reproduction-logdiff`

trackio-local-dashboard://reproduction-logdiff
