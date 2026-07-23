# Claim 2 — sufficient conditions


---
<!-- trackio-cell
{"type": "markdown", "id": "cell_1406b9b8f184", "created_at": "2026-07-17T03:43:11+00:00", "title": "Every Boolean-calculus rule"}
-->
We test every rule in Table 1 separately: negation, conditionally-independent conjunction, conditionally-independent disjunction, and mutually-exclusive disjunction. Atom probabilities are smooth softmax functions, so direct enumeration and differentiation provide an implementation-independent oracle. This targets the exact conditions of Proposition 3.1 and its discrete equivalent Proposition C.3.


---
<!-- trackio-cell
{"type": "markdown", "id": "cell_1afb1d9b2ad5", "created_at": "2026-07-17T03:43:12+00:00", "title": "Result"}
-->
**VERIFIED:** all 100 primitive rule/seed combinations match direct posterior and score computation. Maximum probability error is 2.22e-16 and maximum score error is 3.33e-16.


---
<!-- trackio-cell
{"type": "code", "id": "cell_276088d934f2", "created_at": "2026-07-17T03:43:14+00:00", "title": "Run independent verification tests", "command": ["python", "-m", "pytest", "repro/tests", "-q"], "exit_code": 0, "duration_s": 0.577}
-->
````bash
$ python -m pytest repro/tests -q
````

exit 0 · 0.6s


````output
............                                                             [100%]
12 passed in 0.29s

````
