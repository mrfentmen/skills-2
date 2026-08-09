# Skill Improvements — Live Multi-Model Evaluation

## Executive summary

This is a **read-only live evaluation report** for the 180 skills in `skills 2/`. No skill definitions, scripts, benchmark files, or existing reports were changed. Only this report was created.

### Important result

- The experiment attempted **1,080 requests**: 180 skills × 3 models × 2 standardized tasks.
- Only **122 responses were usable**; **958 attempts failed**, overwhelmingly because the free provider returned HTTP 429 rate limits.
- Therefore, **140 skills are marked `NOT JUDGED`**, not failed. A missing response is an infrastructure result, not evidence that the skill is bad.
- NIM connectivity did not complete within the allotted probe window, so no NIM result is treated as a model score.
- A slower follow-up batch attempted 20 previously unjudged skills; all 20 returned HTTP 429, so it added no new live grades.
- One-key loop: 58 OpenRouter keys were each assigned once to a distinct skill; all 58 returned HTTP 429. Six NIM keys were each assigned once before the runner ceiling; all six timed out. A separate NIM probe using `google/gemma-4-31b-it` also timed out after 30 seconds. These are provider/endpoint failures, not skill grades.

### Model availability

| Model | Usable responses | Average heuristic score | Interpretation |
|---|---:|---:|---|
| `google/gemma-4-31b-it:free` | 0 | — | No usable responses; unavailable/rate-limited in this run. |
| `nvidia/nemotron-3-super-120b-a12b:free` | 76 | 44.1 | Usable comparison sample. |
| `openai/gpt-oss-20b:free` | 46 | 37.3 | Usable comparison sample. |

### Experiment matrix

Each skill was composed through the repository’s existing `skill_cli.py` prompt composer and sent with two common tasks: (A) a newline-delimited record-processing design, and (B) an ambiguous reliability/failure-handling request. This tests whether the skill changes behavior rather than merely repeating its persona.

### Rubric

The heuristic score is out of 100 and is intentionally transparent—not a claim of human-quality judgment:

- **10 points — nonempty response:** response was present and parseable.
- **20 points — task evidence:** addressed the concrete task rather than only naming the persona.
- **35 points — skill requirements:** showed evidence of the active skill’s checkable requirements.
- **20 points — boundaries/failure handling:** surfaced limits, invalid inputs, uncertainty, or safety boundaries.
- **15 points — concrete/verifiable output:** included assumptions, examples, checks, or reviewable steps.

HTTP errors, timeouts, and empty responses are excluded from skill scores. Because the surviving sample is uneven, scores should be used for triage, not as final rankings.

## Findings: skill versus model/provider

### Provider/model problems observed

- OpenRouter returned HTTP 429 on **925 of 1,080** attempts. The parallel full matrix exceeded free-tier limits.
- `google/gemma-4-31b-it:free` produced **0 usable responses** in this run; that is an availability result, not a quality score.
- The NIM probe returned HTTP 404 for the tested route, and Kilo returned HTTP 200 with no usable text; neither provider was scored.
- The two models with usable output differed substantially: Nemotron averaged **44.1**, GPT-OSS averaged **37.3** under this heuristic. This shows model variance is material.

### What can reasonably be improved in the skills

- Make each skill’s most important behavior observable in the first few lines of the response.
- Add one compact worked example and one adversarial/failure example to skills that repeatedly scored weakly on requirements, boundaries, or concrete output.
- Keep persona voice subordinate to the contract: the task should be completed before stylistic flourishes.
- For a trustworthy next run, use sequential requests with per-model cooldowns and a retry budget; do not turn rate limits into skill grades.

### One-key loop results

The requested one-key-to-one-skill loop was attempted with immediate checkpointing. It assigned 64 distinct skills: 58 OpenRouter keys and 6 NIM keys. No usable response was returned, so no new PROMISING/MIXED/WEAK quality grade was created from this loop. The report records the provider failure for each assignment rather than pretending the skill was tested successfully.

### Manual response inspection

I manually inspected eight actual response excerpts from the usable archive. This is separate from the lexical heuristic and is **not** a claim that all 122 response bodies were manually read. The visible samples were:

- **Promising:** `dead-reckoning`, `carmack-mode`, `bob-ross`, `david-attenborough` — these visibly applied the task and showed recognizable skill behavior.
- **Mixed:** `blood-magic`, `black-box` — some contract signals appeared, but theatrical framing or truncation made the result incomplete.
- **Weak:** `anthony-bourdain`, `dalio` — one mostly asked for unrelated persona context; the other was fragmentary and did not execute the task.

The prior 122 usable responses were machine-screened for task, boundary, verification, and concreteness signals. Those signals are useful for triage, but they are not equivalent to a human reading every answer.
- Only these eight response excerpts were manually inspected in this follow-up; the other 114 usable responses remain machine-screened rather than human-reviewed.

## Per-skill results

Each entry is labeled with the skill name. `STATIC` signals are structural checks from the skill file; they are not live model scores. `NOT JUDGED` means no usable live response survived.

## Skill: `alice-waters`

**Live score:** **53.2/100** (range 47–64; 4 usable responses)
**Models observed:** `nvidia/nemotron-3-super-120b-a12b:free`, `openai/gpt-oss-20b:free`
**Dimension averages:** total 53.2, task 9.8, requirements 18, boundaries 6.2, concrete 9.2
**Attempts:** 6 total; **usable:** 4
**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**How to improve:** Improve boundaries evidence: add one explicit, testable requirement/example for this dimension and a failure-boundary example.
**Second-pass grade:** **40/100 — MIXED** (3315 response characters).
**Second-pass evidence:** Second-pass response evidence: task=10/20, assumptions=0/20, boundaries=10/20, verification=0/20, contract=10/10; weakest=assumptions; field=reasoning.
**Second-pass improvement:** always state assumptions explicitly, including what information is missing.
**Third-pass grade:** **38/100 — WEAK** (3526 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 0/20, assumption 0/15, boundary/failure 8/15, verification 0/10, revision 0/10, nonempty 10/10; weakest=requirements; field=reasoning.
**Third-pass improvement:** name which active-skill requirements were satisfied and which were missed, with evidence for each.
**Fourth-pass grade:** **43/100 — MIXED** (3558 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 20/20, addressed requirements 0/20, unmet requirements 0/10, complete/pending 0/10, verification 8/15, limitation/failure 5/10, ledger structure 0/5, nonempty 10/10; weakest=addressed; field=reasoning.
**Fourth-pass improvement:** name the active minimum requirements and map each to evidence in the result.
## Skill: `altman`

**Live score:** **50/100** (range 37–75; 3 usable responses)
**Models observed:** `nvidia/nemotron-3-super-120b-a12b:free`, `openai/gpt-oss-20b:free`
**Dimension averages:** total 50, task 10, requirements 18, boundaries 5, concrete 7
**Attempts:** 6 total; **usable:** 3
**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=missing, cross_language=pass.
**How to improve:** Improve boundaries evidence: add one explicit, testable requirement/example for this dimension and a failure-boundary example.
**Second-pass grade:** **80/100 — PROMISING** (2570 response characters).
**Second-pass evidence:** Second-pass response evidence: task=10/20, assumptions=10/20, boundaries=20/20, verification=20/20, contract=10/10; weakest=task; field=reasoning.
**Second-pass improvement:** put the useful domain answer before persona framing and show a concrete output.
**Third-pass grade:** **50/100 — MIXED** (3355 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 0/20, assumption 0/15, boundary/failure 0/15, verification 10/10, revision 10/10, nonempty 10/10; weakest=requirements; field=reasoning.
**Third-pass improvement:** name which active-skill requirements were satisfied and which were missed, with evidence for each.
**Fourth-pass grade:** **63/100 — MIXED** (2934 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 20/20, addressed requirements 20/20, unmet requirements 0/10, complete/pending 0/10, verification 8/15, limitation/failure 0/10, ledger structure 5/5, nonempty 10/10; weakest=unmet; field=reasoning.
**Fourth-pass improvement:** explicitly list every unmet requirement instead of implying full completion.
## Skill: `anders-hejlsberg`

**Live score:** **36.5/100** (range 36–37; 2 usable responses)
**Models observed:** `nvidia/nemotron-3-super-120b-a12b:free`
**Dimension averages:** total 36.5, task 6.5, requirements 11, boundaries 3.5, concrete 5.5
**Attempts:** 6 total; **usable:** 2
**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**How to improve:** Improve boundaries evidence: add one explicit, testable requirement/example for this dimension and a failure-boundary example.
**Second-pass grade:** **40/100 — MIXED** (3279 response characters).
**Second-pass evidence:** Second-pass response evidence: task=10/20, assumptions=0/20, boundaries=0/20, verification=10/20, contract=10/10; weakest=assumptions; field=reasoning.
**Second-pass improvement:** always state assumptions explicitly, including what information is missing.
**Third-pass grade:** **46/100 — MIXED** (3781 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 6/20, assumption 0/15, boundary/failure 0/15, verification 5/10, revision 5/10, nonempty 10/10; weakest=assumption; field=reasoning.
**Third-pass improvement:** state one specific unsafe or weak assumption and explain how the answer changes if it is false.
**Fourth-pass grade:** **58/100 — MIXED** (3553 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 20/20, addressed requirements 0/20, unmet requirements 0/10, complete/pending 10/10, verification 8/15, limitation/failure 5/10, ledger structure 5/5, nonempty 10/10; weakest=addressed; field=reasoning.
**Fourth-pass improvement:** name the active minimum requirements and map each to evidence in the result.
## Skill: `angela-merkel`

**Live score:** **56/100** (range 52–62; 4 usable responses)
**Models observed:** `nvidia/nemotron-3-super-120b-a12b:free`, `openai/gpt-oss-20b:free`
**Dimension averages:** total 56, task 12, requirements 13, boundaries 10, concrete 11
**Attempts:** 6 total; **usable:** 4
**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**How to improve:** Improve boundaries evidence: add one explicit, testable requirement/example for this dimension and a failure-boundary example.
**Second-pass grade:** **50/100 — MIXED** (3192 response characters).
**Second-pass evidence:** Second-pass response evidence: task=20/20, assumptions=0/20, boundaries=0/20, verification=10/20, contract=10/10; weakest=assumptions; field=reasoning.
**Second-pass improvement:** always state assumptions explicitly, including what information is missing.
**Third-pass grade:** **64/100 — MIXED** (3399 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 14/20, assumption 0/15, boundary/failure 0/15, verification 10/10, revision 10/10, nonempty 10/10; weakest=assumption; field=reasoning.
**Third-pass improvement:** state one specific unsafe or weak assumption and explain how the answer changes if it is false.
**Fourth-pass grade:** **100/100 — PROMISING** (3488 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 20/20, addressed requirements 20/20, unmet requirements 10/10, complete/pending 10/10, verification 15/15, limitation/failure 10/10, ledger structure 5/5, nonempty 10/10; weakest=ledger; field=reasoning.
**Fourth-pass improvement:** use a clearly labeled contract ledger with all requested fields.
## Skill: `anthony-bourdain`

**Live score:** **23/100** (range 10–38; 4 usable responses)
**Models observed:** `nvidia/nemotron-3-super-120b-a12b:free`, `openai/gpt-oss-20b:free`
**Dimension averages:** total 23, task 0.5, requirements 11.5, boundaries 0, concrete 1
**Attempts:** 6 total; **usable:** 4
**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**Manual sample grade:** **WEAK** — the sampled response asked for persona-specific context and did not perform the engineering task.
**How to improve:** Make the skill complete the requested task before asking persona-specific questions; add an engineering example showing when its food/research workflow should refuse or redirect unrelated tasks.
**Second-pass grade:** **40/100 — MIXED** (2972 response characters).
**Second-pass evidence:** Second-pass response evidence: task=10/20, assumptions=0/20, boundaries=0/20, verification=10/20, contract=10/10; weakest=assumptions; field=reasoning.
**Second-pass improvement:** always state assumptions explicitly, including what information is missing.
**Third-pass grade:** **100/100 — PROMISING** (3355 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 20/20, assumption 15/15, boundary/failure 15/15, verification 10/10, revision 10/10, nonempty 10/10; weakest=verification; field=reasoning.
**Third-pass improvement:** add a concrete verification step with an expected result, metric, or assertion.
**Fourth-pass grade:** **59/100 — MIXED** (3620 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 20/20, addressed requirements 6/20, unmet requirements 0/10, complete/pending 10/10, verification 8/15, limitation/failure 0/10, ledger structure 5/5, nonempty 10/10; weakest=unmet; field=reasoning.
**Fourth-pass improvement:** explicitly list every unmet requirement instead of implying full completion.
## Skill: `apple-platform`

**Live score:** **47.7/100** (range 38–61; 3 usable responses)
**Models observed:** `nvidia/nemotron-3-super-120b-a12b:free`, `openai/gpt-oss-20b:free`
**Dimension averages:** total 47.7, task 7.7, requirements 10.7, boundaries 10.3, concrete 9
**Attempts:** 6 total; **usable:** 3
**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**How to improve:** Improve task evidence: add one explicit, testable requirement/example for this dimension and a failure-boundary example.
**Second-pass grade:** **60/100 — MIXED** (3071 response characters).
**Second-pass evidence:** Second-pass response evidence: task=20/20, assumptions=0/20, boundaries=10/20, verification=10/20, contract=10/10; weakest=assumptions; field=reasoning.
**Second-pass improvement:** always state assumptions explicitly, including what information is missing.
**Third-pass grade:** **43/100 — MIXED** (3466 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 0/20, assumption 0/15, boundary/failure 8/15, verification 5/10, revision 0/10, nonempty 10/10; weakest=requirements; field=reasoning.
**Third-pass improvement:** name which active-skill requirements were satisfied and which were missed, with evidence for each.
**Fourth-pass grade:** **41/100 — MIXED** (3567 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 20/20, addressed requirements 6/20, unmet requirements 0/10, complete/pending 0/10, verification 0/15, limitation/failure 5/10, ledger structure 0/5, nonempty 10/10; weakest=unmet; field=reasoning.
**Fourth-pass improvement:** explicitly list every unmet requirement instead of implying full completion.
## Skill: `atul-gawande`

**Live score:** **38.7/100** (range 33–47; 3 usable responses)
**Models observed:** `nvidia/nemotron-3-super-120b-a12b:free`, `openai/gpt-oss-20b:free`
**Dimension averages:** total 38.7, task 7.3, requirements 9.3, boundaries 4, concrete 8
**Attempts:** 6 total; **usable:** 3
**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=missing, cross_language=pass.
**How to improve:** Improve boundaries evidence: add one explicit, testable requirement/example for this dimension and a failure-boundary example.
**Second-pass grade:** **40/100 — MIXED** (3078 response characters).
**Second-pass evidence:** Second-pass response evidence: task=0/20, assumptions=0/20, boundaries=0/20, verification=20/20, contract=10/10; weakest=task; field=reasoning.
**Second-pass improvement:** put the useful domain answer before persona framing and show a concrete output.
**Third-pass grade:** **54/100 — MIXED** (3590 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 14/20, assumption 0/15, boundary/failure 0/15, verification 10/10, revision 0/10, nonempty 10/10; weakest=assumption; field=reasoning.
**Third-pass improvement:** state one specific unsafe or weak assumption and explain how the answer changes if it is false.
**Fourth-pass grade:** **74/100 — PROMISING** (3664 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 20/20, addressed requirements 6/20, unmet requirements 5/10, complete/pending 10/10, verification 8/15, limitation/failure 10/10, ledger structure 5/5, nonempty 10/10; weakest=unmet; field=reasoning.
**Fourth-pass improvement:** explicitly list every unmet requirement instead of implying full completion.
## Skill: `aws-sde`

**Live score:** **43.2/100** (range 31–53; 4 usable responses)
**Models observed:** `nvidia/nemotron-3-super-120b-a12b:free`, `openai/gpt-oss-20b:free`
**Dimension averages:** total 43.2, task 11.5, requirements 9, boundaries 8.2, concrete 4.5
**Attempts:** 6 total; **usable:** 4
**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**How to improve:** Improve concrete evidence: add one explicit, testable requirement/example for this dimension and a failure-boundary example.
**Second-pass grade:** **40/100 — MIXED** (3234 response characters).
**Second-pass evidence:** Second-pass response evidence: task=10/20, assumptions=0/20, boundaries=0/20, verification=10/20, contract=10/10; weakest=assumptions; field=reasoning.
**Second-pass improvement:** always state assumptions explicitly, including what information is missing.
**Third-pass grade:** **61/100 — MIXED** (3272 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 6/20, assumption 0/15, boundary/failure 15/15, verification 10/10, revision 0/10, nonempty 10/10; weakest=assumption; field=reasoning.
**Third-pass improvement:** state one specific unsafe or weak assumption and explain how the answer changes if it is false.
**Fourth-pass grade:** **64/100 — MIXED** (3327 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 20/20, addressed requirements 6/20, unmet requirements 0/10, complete/pending 10/10, verification 8/15, limitation/failure 10/10, ledger structure 0/5, nonempty 10/10; weakest=unmet; field=reasoning.
**Fourth-pass improvement:** explicitly list every unmet requirement instead of implying full completion.
## Skill: `azure-engineer`

**Live score:** **36.2/100** (range 27–49; 4 usable responses)
**Models observed:** `nvidia/nemotron-3-super-120b-a12b:free`, `openai/gpt-oss-20b:free`
**Dimension averages:** total 36.2, task 5.8, requirements 12, boundaries 5, concrete 3.5
**Attempts:** 6 total; **usable:** 4
**Static signals:** frontmatter=pass, triggers=missing, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=missing, cross_language=pass.
**How to improve:** Improve concrete evidence: add one explicit, testable requirement/example for this dimension and a failure-boundary example.
**Second-pass grade:** **40/100 — MIXED** (3168 response characters).
**Second-pass evidence:** Second-pass response evidence: task=10/20, assumptions=0/20, boundaries=10/20, verification=0/20, contract=10/10; weakest=assumptions; field=reasoning.
**Second-pass improvement:** always state assumptions explicitly, including what information is missing.
**Third-pass grade:** **93/100 — PROMISING** (3622 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 20/20, assumption 8/15, boundary/failure 15/15, verification 10/10, revision 10/10, nonempty 10/10; weakest=assumption; field=reasoning.
**Third-pass improvement:** state one specific unsafe or weak assumption and explain how the answer changes if it is false.
**Fourth-pass grade:** **64/100 — MIXED** (3662 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 20/20, addressed requirements 6/20, unmet requirements 0/10, complete/pending 10/10, verification 8/15, limitation/failure 5/10, ledger structure 5/5, nonempty 10/10; weakest=unmet; field=reasoning.
**Fourth-pass improvement:** explicitly list every unmet requirement instead of implying full completion.
## Skill: `barbara-liskov`

**Live score:** **43.7/100** (range 42–46; 3 usable responses)
**Models observed:** `nvidia/nemotron-3-super-120b-a12b:free`, `openai/gpt-oss-20b:free`
**Dimension averages:** total 43.7, task 7.7, requirements 11, boundaries 6, concrete 9
**Attempts:** 6 total; **usable:** 3
**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**How to improve:** Improve boundaries evidence: add one explicit, testable requirement/example for this dimension and a failure-boundary example.
**Second-pass grade:** **60/100 — MIXED** (3079 response characters).
**Second-pass evidence:** Second-pass response evidence: task=20/20, assumptions=0/20, boundaries=10/20, verification=10/20, contract=10/10; weakest=assumptions; field=reasoning.
**Second-pass improvement:** always state assumptions explicitly, including what information is missing.
**Third-pass grade:** **56/100 — MIXED** (3802 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 6/20, assumption 0/15, boundary/failure 15/15, verification 5/10, revision 0/10, nonempty 10/10; weakest=assumption; field=reasoning.
**Third-pass improvement:** state one specific unsafe or weak assumption and explain how the answer changes if it is false.
**Fourth-pass grade:** **94/100 — PROMISING** (3928 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 20/20, addressed requirements 14/20, unmet requirements 10/10, complete/pending 10/10, verification 15/15, limitation/failure 10/10, ledger structure 5/5, nonempty 10/10; weakest=ledger; field=reasoning.
**Fourth-pass improvement:** use a clearly labeled contract ledger with all requested fields.
## Skill: `barbara-mcclintock`

**Live score:** **26.2/100** (range 17–43; 4 usable responses)
**Models observed:** `nvidia/nemotron-3-super-120b-a12b:free`, `openai/gpt-oss-20b:free`
**Dimension averages:** total 26.2, task 4, requirements 9.5, boundaries 1.8, concrete 1
**Attempts:** 6 total; **usable:** 4
**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**How to improve:** Improve concrete evidence: add one explicit, testable requirement/example for this dimension and a failure-boundary example.
**Second-pass grade:** **60/100 — MIXED** (3102 response characters).
**Second-pass evidence:** Second-pass response evidence: task=0/20, assumptions=20/20, boundaries=10/20, verification=10/20, contract=10/10; weakest=task; field=reasoning.
**Second-pass improvement:** put the useful domain answer before persona framing and show a concrete output.
**Third-pass grade:** **94/100 — PROMISING** (3453 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 14/20, assumption 15/15, boundary/failure 15/15, verification 10/10, revision 10/10, nonempty 10/10; weakest=verification; field=reasoning.
**Third-pass improvement:** add a concrete verification step with an expected result, metric, or assertion.
**Fourth-pass grade:** **80/100 — PROMISING** (3513 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 10/20, addressed requirements 20/20, unmet requirements 5/10, complete/pending 10/10, verification 15/15, limitation/failure 5/10, ledger structure 5/5, nonempty 10/10; weakest=unmet; field=reasoning.
**Fourth-pass improvement:** explicitly list every unmet requirement instead of implying full completion.
## Skill: `bezo`

**Live score:** **43/100** (range 41–45; 2 usable responses)
**Models observed:** `nvidia/nemotron-3-super-120b-a12b:free`
**Dimension averages:** total 43, task 8, requirements 11, boundaries 10, concrete 4
**Attempts:** 6 total; **usable:** 2
**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**How to improve:** Improve concrete evidence: add one explicit, testable requirement/example for this dimension and a failure-boundary example.
**Second-pass grade:** **40/100 — MIXED** (3125 response characters).
**Second-pass evidence:** Second-pass response evidence: task=10/20, assumptions=0/20, boundaries=10/20, verification=0/20, contract=10/10; weakest=assumptions; field=reasoning.
**Second-pass improvement:** always state assumptions explicitly, including what information is missing.
**Third-pass grade:** **87/100 — PROMISING** (3423 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 14/20, assumption 8/15, boundary/failure 15/15, verification 10/10, revision 10/10, nonempty 10/10; weakest=assumption; field=reasoning.
**Third-pass improvement:** state one specific unsafe or weak assumption and explain how the answer changes if it is false.
**Fourth-pass grade:** **50/100 — MIXED** (3348 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 15/20, addressed requirements 0/20, unmet requirements 0/10, complete/pending 0/10, verification 15/15, limitation/failure 10/10, ledger structure 0/5, nonempty 10/10; weakest=addressed; field=reasoning.
**Fourth-pass improvement:** name the active minimum requirements and map each to evidence in the result.
## Skill: `black-box`

**Live score:** **33.5/100** (range 13–54; 2 usable responses)
**Models observed:** `nvidia/nemotron-3-super-120b-a12b:free`
**Dimension averages:** total 33.5, task 5.5, requirements 8.5, boundaries 5, concrete 4.5
**Attempts:** 6 total; **usable:** 2
**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=missing, cross_language=pass.
**Manual sample grade:** **MIXED** — the sampled response started a black-box design, but the available excerpt was truncated before the query protocol and stopping proof could be verified.
**How to improve:** Improve concrete evidence: add one explicit, testable requirement/example for this dimension and a failure-boundary example.
**Second-pass grade:** **40/100 — MIXED** (2622 response characters).
**Second-pass evidence:** Second-pass response evidence: task=10/20, assumptions=0/20, boundaries=0/20, verification=10/20, contract=10/10; weakest=assumptions; field=reasoning.
**Second-pass improvement:** always state assumptions explicitly, including what information is missing.
**Third-pass grade:** **44/100 — MIXED** (3313 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 14/20, assumption 0/15, boundary/failure 0/15, verification 0/10, revision 0/10, nonempty 10/10; weakest=assumption; field=reasoning.
**Third-pass improvement:** state one specific unsafe or weak assumption and explain how the answer changes if it is false.
**Fourth-pass grade:** **41/100 — MIXED** (2968 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 15/20, addressed requirements 6/20, unmet requirements 0/10, complete/pending 0/10, verification 0/15, limitation/failure 5/10, ledger structure 5/5, nonempty 10/10; weakest=unmet; field=reasoning.
**Fourth-pass improvement:** explicitly list every unmet requirement instead of implying full completion.
## Skill: `blind`

**Live score:** **31.5/100** (range 26–37; 2 usable responses)
**Models observed:** `nvidia/nemotron-3-super-120b-a12b:free`
**Dimension averages:** total 31.5, task 6.5, requirements 10, boundaries 1, concrete 4
**Attempts:** 6 total; **usable:** 2
**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=missing, cross_language=pass.
**How to improve:** Improve boundaries evidence: add one explicit, testable requirement/example for this dimension and a failure-boundary example.
**Second-pass grade:** **80/100 — PROMISING** (3138 response characters).
**Second-pass evidence:** Second-pass response evidence: task=10/20, assumptions=10/20, boundaries=20/20, verification=20/20, contract=10/10; weakest=task; field=reasoning.
**Second-pass improvement:** put the useful domain answer before persona framing and show a concrete output.
**Third-pass grade:** **75/100 — PROMISING** (3785 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 20/20, assumption 0/15, boundary/failure 15/15, verification 10/10, revision 0/10, nonempty 10/10; weakest=assumption; field=reasoning.
**Third-pass improvement:** state one specific unsafe or weak assumption and explain how the answer changes if it is false.
**Fourth-pass grade:** **95/100 — PROMISING** (3660 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 20/20, addressed requirements 20/20, unmet requirements 10/10, complete/pending 10/10, verification 15/15, limitation/failure 5/10, ledger structure 5/5, nonempty 10/10; weakest=limitation; field=reasoning.
**Fourth-pass improvement:** state a concrete failure, boundary, invalid-input, or uncertainty condition and the safe response.
## Skill: `blood-magic`

**Live score:** **29.5/100** (range 20–39; 2 usable responses)
**Models observed:** `nvidia/nemotron-3-super-120b-a12b:free`
**Dimension averages:** total 29.5, task 5.5, requirements 10.5, boundaries 2.5, concrete 1
**Attempts:** 6 total; **usable:** 2
**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=missing, cross_language=pass.
**Manual sample grade:** **MIXED** — the sampled response showed disposable-resource and ownership framing, but the theatrical trade-off could overshadow the actual engineering contract.
**How to improve:** Improve concrete evidence: add one explicit, testable requirement/example for this dimension and a failure-boundary example.
**Second-pass grade:** **50/100 — MIXED** (3062 response characters).
**Second-pass evidence:** Second-pass response evidence: task=10/20, assumptions=0/20, boundaries=0/20, verification=20/20, contract=10/10; weakest=assumptions; field=reasoning.
**Second-pass improvement:** always state assumptions explicitly, including what information is missing.
**Third-pass grade:** **46/100 — MIXED** (3510 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 6/20, assumption 0/15, boundary/failure 0/15, verification 10/10, revision 0/10, nonempty 10/10; weakest=assumption; field=reasoning.
**Third-pass improvement:** state one specific unsafe or weak assumption and explain how the answer changes if it is false.
**Fourth-pass grade:** **85/100 — PROMISING** (3520 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 20/20, addressed requirements 20/20, unmet requirements 5/10, complete/pending 10/10, verification 15/15, limitation/failure 0/10, ledger structure 5/5, nonempty 10/10; weakest=limitation; field=reasoning.
**Fourth-pass improvement:** state a concrete failure, boundary, invalid-input, or uncertainty condition and the safe response.
## Skill: `boardroom-liar`

**Live score:** **44.5/100** (range 42–49; 4 usable responses)
**Models observed:** `nvidia/nemotron-3-super-120b-a12b:free`, `openai/gpt-oss-20b:free`
**Dimension averages:** total 44.5, task 9.2, requirements 15.8, boundaries 6.5, concrete 3
**Attempts:** 6 total; **usable:** 4
**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=missing, cross_language=pass.
**How to improve:** Improve concrete evidence: add one explicit, testable requirement/example for this dimension and a failure-boundary example.
**Second-pass grade:** **70/100 — PROMISING** (3152 response characters).
**Second-pass evidence:** Second-pass response evidence: task=10/20, assumptions=10/20, boundaries=10/20, verification=20/20, contract=10/10; weakest=task; field=reasoning.
**Second-pass improvement:** put the useful domain answer before persona framing and show a concrete output.
**Third-pass grade:** **31/100 — WEAK** (3261 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 15/20, requirement audit 6/20, assumption 0/15, boundary/failure 0/15, verification 0/10, revision 0/10, nonempty 10/10; weakest=assumption; field=reasoning.
**Third-pass improvement:** state one specific unsafe or weak assumption and explain how the answer changes if it is false.
**Fourth-pass grade:** **95/100 — PROMISING** (3517 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 15/20, addressed requirements 20/20, unmet requirements 10/10, complete/pending 10/10, verification 15/15, limitation/failure 10/10, ledger structure 5/5, nonempty 10/10; weakest=ledger; field=reasoning.
**Fourth-pass improvement:** use a clearly labeled contract ledger with all requested fields.
## Skill: `bob-ross`

**Live score:** **52.8/100** (range 39–82; 4 usable responses)
**Models observed:** `nvidia/nemotron-3-super-120b-a12b:free`, `openai/gpt-oss-20b:free`
**Dimension averages:** total 52.8, task 13, requirements 14.5, boundaries 7, concrete 8.2
**Attempts:** 6 total; **usable:** 4
**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**Manual sample grade:** **PROMISING** — the sampled response gave a concrete Python-oriented design with validation and test framing.
**How to improve:** Improve boundaries evidence: add one explicit, testable requirement/example for this dimension and a failure-boundary example.
**Second-pass grade:** **80/100 — PROMISING** (2852 response characters).
**Second-pass evidence:** Second-pass response evidence: task=10/20, assumptions=10/20, boundaries=20/20, verification=20/20, contract=10/10; weakest=task; field=reasoning.
**Second-pass improvement:** put the useful domain answer before persona framing and show a concrete output.
**Third-pass grade:** **58/100 — MIXED** (3288 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 0/20, assumption 0/15, boundary/failure 8/15, verification 10/10, revision 10/10, nonempty 10/10; weakest=requirements; field=reasoning.
**Third-pass improvement:** name which active-skill requirements were satisfied and which were missed, with evidence for each.
**Fourth-pass grade:** **64/100 — MIXED** (3416 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 20/20, addressed requirements 6/20, unmet requirements 0/10, complete/pending 5/10, verification 8/15, limitation/failure 10/10, ledger structure 5/5, nonempty 10/10; weakest=unmet; field=reasoning.
**Fourth-pass improvement:** explicitly list every unmet requirement instead of implying full completion.
## Skill: `boiler-room`

**Live score:** **42/100** (range 19–57; 4 usable responses)
**Models observed:** `nvidia/nemotron-3-super-120b-a12b:free`, `openai/gpt-oss-20b:free`
**Dimension averages:** total 42, task 9.5, requirements 10, boundaries 6.2, concrete 6.2
**Attempts:** 6 total; **usable:** 4
**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=missing, cross_language=pass.
**How to improve:** Improve boundaries evidence: add one explicit, testable requirement/example for this dimension and a failure-boundary example.
**Second-pass grade:** **100/100 — PROMISING** (2893 response characters).
**Second-pass evidence:** Second-pass response evidence: task=20/20, assumptions=20/20, boundaries=20/20, verification=20/20, contract=10/10; weakest=contract; field=reasoning.
**Second-pass improvement:** tie the response to at least one named minimum requirement instead of generic advice.
**Third-pass grade:** **61/100 — MIXED** (3013 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 6/20, assumption 0/15, boundary/failure 15/15, verification 10/10, revision 0/10, nonempty 10/10; weakest=assumption; field=reasoning.
**Third-pass improvement:** state one specific unsafe or weak assumption and explain how the answer changes if it is false.
**Fourth-pass grade:** **61/100 — MIXED** (3185 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 15/20, addressed requirements 6/20, unmet requirements 0/10, complete/pending 0/10, verification 15/15, limitation/failure 10/10, ledger structure 5/5, nonempty 10/10; weakest=unmet; field=reasoning.
**Fourth-pass improvement:** explicitly list every unmet requirement instead of implying full completion.
## Skill: `boiler-room-research`

**Live score:** **27.3/100** (range 10–38; 3 usable responses)
**Models observed:** `nvidia/nemotron-3-super-120b-a12b:free`, `openai/gpt-oss-20b:free`
**Dimension averages:** total 27.3, task 5.3, requirements 6, boundaries 3.3, concrete 2.7
**Attempts:** 6 total; **usable:** 3
**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**How to improve:** Improve concrete evidence: add one explicit, testable requirement/example for this dimension and a failure-boundary example.
**Second-pass grade:** **50/100 — MIXED** (2683 response characters).
**Second-pass evidence:** Second-pass response evidence: task=10/20, assumptions=0/20, boundaries=10/20, verification=10/20, contract=10/10; weakest=assumptions; field=reasoning.
**Second-pass improvement:** always state assumptions explicitly, including what information is missing.
**Third-pass grade:** **43/100 — MIXED** (2866 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 0/20, assumption 0/15, boundary/failure 8/15, verification 5/10, revision 0/10, nonempty 10/10; weakest=requirements; field=reasoning.
**Third-pass improvement:** name which active-skill requirements were satisfied and which were missed, with evidence for each.
**Fourth-pass grade:** **41/100 — MIXED** (3032 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 15/20, addressed requirements 6/20, unmet requirements 0/10, complete/pending 0/10, verification 0/15, limitation/failure 5/10, ledger structure 5/5, nonempty 10/10; weakest=unmet; field=reasoning.
**Fourth-pass improvement:** explicitly list every unmet requirement instead of implying full completion.
## Skill: `brian-kernighan`

**Live score:** **39.5/100** (range 30–47; 4 usable responses)
**Models observed:** `nvidia/nemotron-3-super-120b-a12b:free`, `openai/gpt-oss-20b:free`
**Dimension averages:** total 39.5, task 9.5, requirements 8.8, boundaries 5.5, concrete 5.8
**Attempts:** 6 total; **usable:** 4
**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=missing, cross_language=pass.
**How to improve:** Improve boundaries evidence: add one explicit, testable requirement/example for this dimension and a failure-boundary example.
**Second-pass grade:** **40/100 — MIXED** (3014 response characters).
**Second-pass evidence:** Second-pass response evidence: task=10/20, assumptions=0/20, boundaries=0/20, verification=10/20, contract=10/10; weakest=assumptions; field=reasoning.
**Second-pass improvement:** always state assumptions explicitly, including what information is missing.
**Third-pass grade:** **68/100 — MIXED** (3409 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 20/20, assumption 0/15, boundary/failure 8/15, verification 10/10, revision 0/10, nonempty 10/10; weakest=assumption; field=reasoning.
**Third-pass improvement:** state one specific unsafe or weak assumption and explain how the answer changes if it is false.
**Fourth-pass grade:** **38/100 — WEAK** (3163 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 20/20, addressed requirements 0/20, unmet requirements 0/10, complete/pending 0/10, verification 8/15, limitation/failure 0/10, ledger structure 0/5, nonempty 10/10; weakest=addressed; field=reasoning.
**Fourth-pass improvement:** name the active minimum requirements and map each to evidence in the result.
## Skill: `bruce-wayne`

**Live score:** **41.8/100** (range 32–51; 4 usable responses)
**Models observed:** `nvidia/nemotron-3-super-120b-a12b:free`, `openai/gpt-oss-20b:free`
**Dimension averages:** total 41.8, task 10, requirements 7, boundaries 8.5, concrete 6.2
**Attempts:** 6 total; **usable:** 4
**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**How to improve:** Improve concrete evidence: add one explicit, testable requirement/example for this dimension and a failure-boundary example.
**Second-pass grade:** **80/100 — PROMISING** (3250 response characters).
**Second-pass evidence:** Second-pass response evidence: task=10/20, assumptions=10/20, boundaries=20/20, verification=20/20, contract=10/10; weakest=task; field=reasoning.
**Second-pass improvement:** put the useful domain answer before persona framing and show a concrete output.
**Third-pass grade:** **61/100 — MIXED** (3261 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 6/20, assumption 0/15, boundary/failure 15/15, verification 10/10, revision 0/10, nonempty 10/10; weakest=assumption; field=reasoning.
**Third-pass improvement:** state one specific unsafe or weak assumption and explain how the answer changes if it is false.
**Fourth-pass grade:** **58/100 — MIXED** (3426 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 15/20, addressed requirements 0/20, unmet requirements 0/10, complete/pending 10/10, verification 8/15, limitation/failure 10/10, ledger structure 5/5, nonempty 10/10; weakest=addressed; field=reasoning.
**Fourth-pass improvement:** name the active minimum requirements and map each to evidence in the result.
## Skill: `buckminster-fuller`

**Live score:** **41/100** (range 17–52; 4 usable responses)
**Models observed:** `nvidia/nemotron-3-super-120b-a12b:free`, `openai/gpt-oss-20b:free`
**Dimension averages:** total 41, task 9.5, requirements 9.5, boundaries 5.8, concrete 6.2
**Attempts:** 6 total; **usable:** 4
**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**How to improve:** Improve boundaries evidence: add one explicit, testable requirement/example for this dimension and a failure-boundary example.
**Second-pass grade:** **50/100 — MIXED** (3167 response characters).
**Second-pass evidence:** Second-pass response evidence: task=10/20, assumptions=0/20, boundaries=0/20, verification=20/20, contract=10/10; weakest=assumptions; field=reasoning.
**Second-pass improvement:** always state assumptions explicitly, including what information is missing.
**Third-pass grade:** **60/100 — MIXED** (3619 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 0/20, assumption 0/15, boundary/failure 15/15, verification 5/10, revision 10/10, nonempty 10/10; weakest=requirements; field=reasoning.
**Third-pass improvement:** name which active-skill requirements were satisfied and which were missed, with evidence for each.
**Fourth-pass grade:** **43/100 — MIXED** (3518 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 20/20, addressed requirements 0/20, unmet requirements 0/10, complete/pending 0/10, verification 8/15, limitation/failure 5/10, ledger structure 0/5, nonempty 10/10; weakest=addressed; field=reasoning.
**Fourth-pass improvement:** name the active minimum requirements and map each to evidence in the result.
## Skill: `buffett`

**Live score:** **42.8/100** (range 19–78; 4 usable responses)
**Models observed:** `nvidia/nemotron-3-super-120b-a12b:free`, `openai/gpt-oss-20b:free`
**Dimension averages:** total 42.8, task 8.8, requirements 12.8, boundaries 4.8, concrete 6.5
**Attempts:** 6 total; **usable:** 4
**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**How to improve:** Improve boundaries evidence: add one explicit, testable requirement/example for this dimension and a failure-boundary example.
**Second-pass grade:** **50/100 — MIXED** (2863 response characters).
**Second-pass evidence:** Second-pass response evidence: task=0/20, assumptions=0/20, boundaries=10/20, verification=20/20, contract=10/10; weakest=task; field=reasoning.
**Second-pass improvement:** put the useful domain answer before persona framing and show a concrete output.
**Third-pass grade:** **56/100 — MIXED** (2790 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 0/20, assumption 8/15, boundary/failure 8/15, verification 10/10, revision 0/10, nonempty 10/10; weakest=requirements; field=reasoning.
**Third-pass improvement:** name which active-skill requirements were satisfied and which were missed, with evidence for each.
**Fourth-pass grade:** **43/100 — MIXED** (2568 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 10/20, addressed requirements 0/20, unmet requirements 0/10, complete/pending 0/10, verification 8/15, limitation/failure 10/10, ledger structure 5/5, nonempty 10/10; weakest=addressed; field=reasoning.
**Fourth-pass improvement:** name the active minimum requirements and map each to evidence in the result.
## Skill: `burry`

**Live score:** **31.5/100** (range 26–37; 2 usable responses)
**Models observed:** `nvidia/nemotron-3-super-120b-a12b:free`
**Dimension averages:** total 31.5, task 7, requirements 7, boundaries 3.5, concrete 4
**Attempts:** 6 total; **usable:** 2
**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=missing, cross_language=pass.
**How to improve:** Improve boundaries evidence: add one explicit, testable requirement/example for this dimension and a failure-boundary example.
**Second-pass grade:** **40/100 — MIXED** (2604 response characters).
**Second-pass evidence:** Second-pass response evidence: task=0/20, assumptions=0/20, boundaries=10/20, verification=10/20, contract=10/10; weakest=task; field=reasoning.
**Second-pass improvement:** put the useful domain answer before persona framing and show a concrete output.
**Third-pass grade:** **54/100 — MIXED** (3022 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 6/20, assumption 0/15, boundary/failure 8/15, verification 10/10, revision 0/10, nonempty 10/10; weakest=assumption; field=reasoning.
**Third-pass improvement:** state one specific unsafe or weak assumption and explain how the answer changes if it is false.
**Fourth-pass grade:** **41/100 — MIXED** (3320 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 10/20, addressed requirements 6/20, unmet requirements 0/10, complete/pending 0/10, verification 0/15, limitation/failure 10/10, ledger structure 5/5, nonempty 10/10; weakest=unmet; field=reasoning.
**Fourth-pass improvement:** explicitly list every unmet requirement instead of implying full completion.
## Skill: `bushnell`

**Live score:** **43/100** (range 25–59; 4 usable responses)
**Models observed:** `nvidia/nemotron-3-super-120b-a12b:free`, `openai/gpt-oss-20b:free`
**Dimension averages:** total 43, task 10, requirements 10.8, boundaries 9.2, concrete 3
**Attempts:** 6 total; **usable:** 4
**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**How to improve:** Improve concrete evidence: add one explicit, testable requirement/example for this dimension and a failure-boundary example.
**Second-pass grade:** **30/100 — WEAK** (2962 response characters).
**Second-pass evidence:** Second-pass response evidence: task=0/20, assumptions=0/20, boundaries=0/20, verification=10/20, contract=10/10; weakest=task; field=reasoning.
**Second-pass improvement:** put the useful domain answer before persona framing and show a concrete output.
**Third-pass grade:** **65/100 — MIXED** (3403 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 20/20, assumption 0/15, boundary/failure 0/15, verification 10/10, revision 5/10, nonempty 10/10; weakest=assumption; field=reasoning.
**Third-pass improvement:** state one specific unsafe or weak assumption and explain how the answer changes if it is false.
**Fourth-pass grade:** **49/100 — MIXED** (3302 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 20/20, addressed requirements 6/20, unmet requirements 0/10, complete/pending 0/10, verification 8/15, limitation/failure 0/10, ledger structure 5/5, nonempty 10/10; weakest=unmet; field=reasoning.
**Fourth-pass improvement:** explicitly list every unmet requirement instead of implying full completion.
## Skill: `carl-sagan`

**Live score:** **47.8/100** (range 37–69; 4 usable responses)
**Models observed:** `nvidia/nemotron-3-super-120b-a12b:free`, `openai/gpt-oss-20b:free`
**Dimension averages:** total 47.8, task 10.8, requirements 10.8, boundaries 9, concrete 7.2
**Attempts:** 6 total; **usable:** 4
**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**How to improve:** Improve concrete evidence: add one explicit, testable requirement/example for this dimension and a failure-boundary example.
**Second-pass grade:** **40/100 — MIXED** (3421 response characters).
**Second-pass evidence:** Second-pass response evidence: task=10/20, assumptions=0/20, boundaries=0/20, verification=10/20, contract=10/10; weakest=assumptions; field=reasoning.
**Second-pass improvement:** always state assumptions explicitly, including what information is missing.
**Third-pass grade:** **54/100 — MIXED** (3615 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 14/20, assumption 0/15, boundary/failure 0/15, verification 10/10, revision 0/10, nonempty 10/10; weakest=assumption; field=reasoning.
**Third-pass improvement:** state one specific unsafe or weak assumption and explain how the answer changes if it is false.
**Fourth-pass grade:** **54/100 — MIXED** (3788 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 15/20, addressed requirements 6/20, unmet requirements 0/10, complete/pending 10/10, verification 8/15, limitation/failure 0/10, ledger structure 5/5, nonempty 10/10; weakest=unmet; field=reasoning.
**Fourth-pass improvement:** explicitly list every unmet requirement instead of implying full completion.
## Skill: `carmack-mode`

**Live score:** **47.7/100** (range 43–57; 3 usable responses)
**Models observed:** `nvidia/nemotron-3-super-120b-a12b:free`, `openai/gpt-oss-20b:free`
**Dimension averages:** total 47.7, task 11.3, requirements 10.3, boundaries 9, concrete 7
**Attempts:** 6 total; **usable:** 3
**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**Manual sample grade:** **PROMISING** — the sampled response named a measurement-first baseline and performance constraints; verify benchmark claims in a fuller review.
**How to improve:** Improve concrete evidence: add one explicit, testable requirement/example for this dimension and a failure-boundary example.
**Second-pass grade:** **30/100 — WEAK** (2665 response characters).
**Second-pass evidence:** Second-pass response evidence: task=0/20, assumptions=0/20, boundaries=0/20, verification=10/20, contract=10/10; weakest=task; field=reasoning.
**Second-pass improvement:** put the useful domain answer before persona framing and show a concrete output.
**Third-pass grade:** **35/100 — WEAK** (3207 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 0/20, assumption 0/15, boundary/failure 0/15, verification 5/10, revision 0/10, nonempty 10/10; weakest=requirements; field=reasoning.
**Third-pass improvement:** name which active-skill requirements were satisfied and which were missed, with evidence for each.
**Fourth-pass grade:** **30/100 — WEAK** (2859 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 20/20, addressed requirements 0/20, unmet requirements 0/10, complete/pending 0/10, verification 0/15, limitation/failure 0/10, ledger structure 0/5, nonempty 10/10; weakest=addressed; field=reasoning.
**Fourth-pass improvement:** name the active minimum requirements and map each to evidence in the result.
## Skill: `casino`

**Live score:** **28/100** (range 10–46; 2 usable responses)
**Models observed:** `nvidia/nemotron-3-super-120b-a12b:free`
**Dimension averages:** total 28, task 7.5, requirements 4.5, boundaries 4, concrete 2
**Attempts:** 6 total; **usable:** 2
**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=missing, cross_language=pass.
**How to improve:** Improve concrete evidence: add one explicit, testable requirement/example for this dimension and a failure-boundary example.
**Second-pass grade:** **40/100 — MIXED** (3023 response characters).
**Second-pass evidence:** Second-pass response evidence: task=0/20, assumptions=0/20, boundaries=10/20, verification=10/20, contract=10/10; weakest=task; field=reasoning.
**Second-pass improvement:** put the useful domain answer before persona framing and show a concrete output.
**Third-pass grade:** **56/100 — MIXED** (3234 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 6/20, assumption 15/15, boundary/failure 0/15, verification 5/10, revision 0/10, nonempty 10/10; weakest=boundary; field=reasoning.
**Third-pass improvement:** give one concrete failure, refusal, uncertainty, or edge-case condition and the safe response.
**Fourth-pass grade:** **45/100 — MIXED** (2884 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 10/20, addressed requirements 20/20, unmet requirements 0/10, complete/pending 0/10, verification 0/15, limitation/failure 0/10, ledger structure 5/5, nonempty 10/10; weakest=unmet; field=reasoning.
**Fourth-pass improvement:** explicitly list every unmet requirement instead of implying full completion.
## Skill: `casino-owner`

**Live score:** **47/100** (range 37–57; 3 usable responses)
**Models observed:** `nvidia/nemotron-3-super-120b-a12b:free`, `openai/gpt-oss-20b:free`
**Dimension averages:** total 47, task 6, requirements 21.3, boundaries 4, concrete 5.7
**Attempts:** 6 total; **usable:** 3
**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=missing, cross_language=pass.
**How to improve:** Improve boundaries evidence: add one explicit, testable requirement/example for this dimension and a failure-boundary example.
**Second-pass grade:** **40/100 — MIXED** (2841 response characters).
**Second-pass evidence:** Second-pass response evidence: task=0/20, assumptions=0/20, boundaries=10/20, verification=10/20, contract=10/10; weakest=task; field=reasoning.
**Second-pass improvement:** put the useful domain answer before persona framing and show a concrete output.
**Third-pass grade:** **30/100 — WEAK** (2719 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 0/20, assumption 0/15, boundary/failure 0/15, verification 0/10, revision 0/10, nonempty 10/10; weakest=requirements; field=reasoning.
**Third-pass improvement:** name which active-skill requirements were satisfied and which were missed, with evidence for each.
**Fourth-pass grade:** **30/100 — WEAK** (2910 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 15/20, addressed requirements 0/20, unmet requirements 0/10, complete/pending 0/10, verification 0/15, limitation/failure 0/10, ledger structure 5/5, nonempty 10/10; weakest=addressed; field=reasoning.
**Fourth-pass improvement:** name the active minimum requirements and map each to evidence in the result.
## Skill: `cathie-wood`

**Live score:** **32.5/100** (range 31–34; 2 usable responses)
**Models observed:** `nvidia/nemotron-3-super-120b-a12b:free`
**Dimension averages:** total 32.5, task 9, requirements 4, boundaries 6.5, concrete 3
**Attempts:** 6 total; **usable:** 2
**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**How to improve:** Improve concrete evidence: add one explicit, testable requirement/example for this dimension and a failure-boundary example.
**Second-pass grade:** **40/100 — MIXED** (2397 response characters).
**Second-pass evidence:** Second-pass response evidence: task=10/20, assumptions=0/20, boundaries=0/20, verification=10/20, contract=10/10; weakest=assumptions; field=reasoning.
**Second-pass improvement:** always state assumptions explicitly, including what information is missing.
**Third-pass grade:** **30/100 — WEAK** (2682 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 0/20, assumption 0/15, boundary/failure 0/15, verification 0/10, revision 0/10, nonempty 10/10; weakest=requirements; field=reasoning.
**Third-pass improvement:** name which active-skill requirements were satisfied and which were missed, with evidence for each.
**Fourth-pass grade:** **36/100 — WEAK** (2790 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 15/20, addressed requirements 6/20, unmet requirements 0/10, complete/pending 0/10, verification 0/15, limitation/failure 0/10, ledger structure 5/5, nonempty 10/10; weakest=unmet; field=reasoning.
**Fourth-pass improvement:** explicitly list every unmet requirement instead of implying full completion.
## Skill: `charles-darwin`

**Live score:** **47/100** (range 27–60; 3 usable responses)
**Models observed:** `nvidia/nemotron-3-super-120b-a12b:free`, `openai/gpt-oss-20b:free`
**Dimension averages:** total 47, task 10, requirements 11, boundaries 8, concrete 8
**Attempts:** 6 total; **usable:** 3
**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**How to improve:** Improve boundaries evidence: add one explicit, testable requirement/example for this dimension and a failure-boundary example.
**Second-pass grade:** **40/100 — MIXED** (3170 response characters).
**Second-pass evidence:** Second-pass response evidence: task=10/20, assumptions=0/20, boundaries=0/20, verification=10/20, contract=10/10; weakest=assumptions; field=reasoning.
**Second-pass improvement:** always state assumptions explicitly, including what information is missing.
**Third-pass grade:** **40/100 — MIXED** (4067 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 0/20, assumption 0/15, boundary/failure 0/15, verification 10/10, revision 0/10, nonempty 10/10; weakest=requirements; field=reasoning.
**Third-pass improvement:** name which active-skill requirements were satisfied and which were missed, with evidence for each.
**Fourth-pass grade:** **100/100 — PROMISING** (3742 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 20/20, addressed requirements 20/20, unmet requirements 10/10, complete/pending 10/10, verification 15/15, limitation/failure 10/10, ledger structure 5/5, nonempty 10/10; weakest=ledger; field=reasoning.
**Fourth-pass improvement:** use a clearly labeled contract ledger with all requested fields.
## Skill: `cold-war`

**Live score:** **47.7/100** (range 41–57; 3 usable responses)
**Models observed:** `nvidia/nemotron-3-super-120b-a12b:free`, `openai/gpt-oss-20b:free`
**Dimension averages:** total 47.7, task 17.3, requirements 6.3, boundaries 9.3, concrete 4.7
**Attempts:** 6 total; **usable:** 3
**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=missing, cross_language=pass.
**How to improve:** Improve concrete evidence: add one explicit, testable requirement/example for this dimension and a failure-boundary example.
**Second-pass grade:** **40/100 — MIXED** (3390 response characters).
**Second-pass evidence:** Second-pass response evidence: task=0/20, assumptions=0/20, boundaries=10/20, verification=10/20, contract=10/10; weakest=task; field=reasoning.
**Second-pass improvement:** put the useful domain answer before persona framing and show a concrete output.
**Third-pass grade:** **45/100 — MIXED** (3713 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 15/20, requirement audit 0/20, assumption 0/15, boundary/failure 15/15, verification 5/10, revision 0/10, nonempty 10/10; weakest=requirements; field=reasoning.
**Third-pass improvement:** name which active-skill requirements were satisfied and which were missed, with evidence for each.
**Fourth-pass grade:** **61/100 — MIXED** (3654 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 20/20, addressed requirements 6/20, unmet requirements 0/10, complete/pending 10/10, verification 0/15, limitation/failure 10/10, ledger structure 5/5, nonempty 10/10; weakest=unmet; field=reasoning.
**Fourth-pass improvement:** explicitly list every unmet requirement instead of implying full completion.
## Skill: `counterpoint`

**Live score:** **51.5/100** (range 42–61; 2 usable responses)
**Models observed:** `nvidia/nemotron-3-super-120b-a12b:free`
**Dimension averages:** total 51.5, task 8.5, requirements 15.5, boundaries 7.5, concrete 10
**Attempts:** 6 total; **usable:** 2
**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**How to improve:** Improve boundaries evidence: add one explicit, testable requirement/example for this dimension and a failure-boundary example.
**Second-pass grade:** **40/100 — MIXED** (2067 response characters).
**Second-pass evidence:** Second-pass response evidence: task=10/20, assumptions=0/20, boundaries=0/20, verification=10/20, contract=10/10; weakest=assumptions; field=reasoning.
**Second-pass improvement:** always state assumptions explicitly, including what information is missing.
**Third-pass grade:** **50/100 — MIXED** (3210 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 0/20, assumption 0/15, boundary/failure 0/15, verification 10/10, revision 10/10, nonempty 10/10; weakest=requirements; field=reasoning.
**Third-pass improvement:** name which active-skill requirements were satisfied and which were missed, with evidence for each.
**Fourth-pass grade:** **38/100 — WEAK** (2918 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 15/20, addressed requirements 0/20, unmet requirements 0/10, complete/pending 5/10, verification 8/15, limitation/failure 0/10, ledger structure 0/5, nonempty 10/10; weakest=addressed; field=reasoning.
**Fourth-pass improvement:** name the active minimum requirements and map each to evidence in the result.
## Skill: `crypto-market-maker`

**Live score:** **46.5/100** (range 21–72; 2 usable responses)
**Models observed:** `nvidia/nemotron-3-super-120b-a12b:free`
**Dimension averages:** total 46.5, task 11, requirements 14.5, boundaries 6, concrete 5
**Attempts:** 6 total; **usable:** 2
**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**How to improve:** Improve concrete evidence: add one explicit, testable requirement/example for this dimension and a failure-boundary example.
**Second-pass grade:** **30/100 — WEAK** (2227 response characters).
**Second-pass evidence:** Second-pass response evidence: task=0/20, assumptions=0/20, boundaries=0/20, verification=10/20, contract=10/10; weakest=task; field=reasoning.
**Second-pass improvement:** put the useful domain answer before persona framing and show a concrete output.
**Third-pass grade:** **51/100 — MIXED** (2789 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 6/20, assumption 0/15, boundary/failure 15/15, verification 0/10, revision 0/10, nonempty 10/10; weakest=assumption; field=reasoning.
**Third-pass improvement:** state one specific unsafe or weak assumption and explain how the answer changes if it is false.
**Fourth-pass grade:** **31/100 — WEAK** (2564 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 5/20, addressed requirements 6/20, unmet requirements 0/10, complete/pending 5/10, verification 0/15, limitation/failure 0/10, ledger structure 5/5, nonempty 10/10; weakest=unmet; field=reasoning.
**Fourth-pass improvement:** explicitly list every unmet requirement instead of implying full completion.
## Skill: `dalio`

**Live score:** **16/100** (range 16–16; 1 usable responses)
**Models observed:** `openai/gpt-oss-20b:free`
**Dimension averages:** total 16, task 2, requirements 2, boundaries 0, concrete 2
**Attempts:** 6 total; **usable:** 1
**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=missing, cross_language=pass.
**Manual sample grade:** **WEAK** — the sampled response was fragmentary and did not visibly execute the requested task.
**How to improve:** Improve boundaries evidence: add one explicit, testable requirement/example for this dimension and a failure-boundary example.
**Second-pass grade:** **50/100 — MIXED** (2183 response characters).
**Second-pass evidence:** Second-pass response evidence: task=10/20, assumptions=0/20, boundaries=10/20, verification=10/20, contract=10/10; weakest=assumptions; field=reasoning.
**Second-pass improvement:** always state assumptions explicitly, including what information is missing.
**Third-pass grade:** **46/100 — MIXED** (3332 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 18/20, requirement audit 0/20, assumption 0/15, boundary/failure 8/15, verification 0/10, revision 10/10, nonempty 10/10; weakest=requirements; field=reasoning.
**Third-pass improvement:** name which active-skill requirements were satisfied and which were missed, with evidence for each.
**Fourth-pass grade:** **61/100 — MIXED** (3062 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 10/20, addressed requirements 6/20, unmet requirements 0/10, complete/pending 5/10, verification 15/15, limitation/failure 10/10, ledger structure 5/5, nonempty 10/10; weakest=unmet; field=reasoning.
**Fourth-pass improvement:** explicitly list every unmet requirement instead of implying full completion.
## Skill: `daniel-kahneman`

**Live score:** **43/100** (range 26–62; 4 usable responses)
**Models observed:** `nvidia/nemotron-3-super-120b-a12b:free`, `openai/gpt-oss-20b:free`
**Dimension averages:** total 43, task 9.8, requirements 10, boundaries 5.2, concrete 8
**Attempts:** 6 total; **usable:** 4
**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**How to improve:** Improve boundaries evidence: add one explicit, testable requirement/example for this dimension and a failure-boundary example.
**Second-pass grade:** **40/100 — MIXED** (3002 response characters).
**Second-pass evidence:** Second-pass response evidence: task=10/20, assumptions=0/20, boundaries=0/20, verification=10/20, contract=10/10; weakest=assumptions; field=reasoning.
**Second-pass improvement:** always state assumptions explicitly, including what information is missing.
**Third-pass grade:** **55/100 — MIXED** (3456 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 0/20, assumption 0/15, boundary/failure 15/15, verification 10/10, revision 0/10, nonempty 10/10; weakest=requirements; field=reasoning.
**Third-pass improvement:** name which active-skill requirements were satisfied and which were missed, with evidence for each.
**Fourth-pass grade:** **64/100 — MIXED** (3447 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 20/20, addressed requirements 6/20, unmet requirements 0/10, complete/pending 5/10, verification 8/15, limitation/failure 10/10, ledger structure 5/5, nonempty 10/10; weakest=unmet; field=reasoning.
**Fourth-pass improvement:** explicitly list every unmet requirement instead of implying full completion.
## Skill: `david-attenborough`

**Live score:** **54.5/100** (range 41–60; 4 usable responses)
**Models observed:** `nvidia/nemotron-3-super-120b-a12b:free`, `openai/gpt-oss-20b:free`
**Dimension averages:** total 54.5, task 11, requirements 16.2, boundaries 8.2, concrete 9
**Attempts:** 6 total; **usable:** 4
**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**Manual sample grade:** **PROMISING** — the sampled response used an observation log, named the input format, and identified concrete anomalies.
**How to improve:** Improve boundaries evidence: add one explicit, testable requirement/example for this dimension and a failure-boundary example.
**Second-pass grade:** **50/100 — MIXED** (3166 response characters).
**Second-pass evidence:** Second-pass response evidence: task=10/20, assumptions=0/20, boundaries=10/20, verification=10/20, contract=10/10; weakest=assumptions; field=reasoning.
**Second-pass improvement:** always state assumptions explicitly, including what information is missing.
**Third-pass grade:** **61/100 — MIXED** (3645 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 6/20, assumption 0/15, boundary/failure 15/15, verification 10/10, revision 0/10, nonempty 10/10; weakest=assumption; field=reasoning.
**Third-pass improvement:** state one specific unsafe or weak assumption and explain how the answer changes if it is false.
**Fourth-pass grade:** **100/100 — PROMISING** (3495 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 20/20, addressed requirements 20/20, unmet requirements 10/10, complete/pending 10/10, verification 15/15, limitation/failure 10/10, ledger structure 5/5, nonempty 10/10; weakest=ledger; field=reasoning.
**Fourth-pass improvement:** use a clearly labeled contract ledger with all requested fields.
## Skill: `dead-reckoning`

**Live score:** **32/100** (range 13–51; 2 usable responses)
**Models observed:** `nvidia/nemotron-3-super-120b-a12b:free`
**Dimension averages:** total 32, task 9, requirements 7, boundaries 4, concrete 2
**Attempts:** 6 total; **usable:** 2
**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**Manual sample grade:** **PROMISING** — the sampled response explicitly used a single-pass stream, bounded state, and accepted/rejected goals.
**How to improve:** Improve concrete evidence: add a small executable example and precise malformed-input/error-bound handling.
**Second-pass grade:** **40/100 — MIXED** (2661 response characters).
**Second-pass evidence:** Second-pass response evidence: task=10/20, assumptions=0/20, boundaries=0/20, verification=10/20, contract=10/10; weakest=assumptions; field=reasoning.
**Second-pass improvement:** always state assumptions explicitly, including what information is missing.
**Third-pass grade:** **25/100 — WEAK** (3091 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 15/20, requirement audit 0/20, assumption 0/15, boundary/failure 0/15, verification 0/10, revision 0/10, nonempty 10/10; weakest=requirements; field=reasoning.
**Third-pass improvement:** name which active-skill requirements were satisfied and which were missed, with evidence for each.
**Fourth-pass grade:** **20/100 — WEAK** (1852 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 10/20, addressed requirements 0/20, unmet requirements 0/10, complete/pending 0/10, verification 0/15, limitation/failure 0/10, ledger structure 0/5, nonempty 10/10; weakest=addressed; field=reasoning.
**Fourth-pass improvement:** name the active minimum requirements and map each to evidence in the result.
## Skill: `delta`

**Live score:** **38.7/100** (range 29–45; 3 usable responses)
**Models observed:** `nvidia/nemotron-3-super-120b-a12b:free`, `openai/gpt-oss-20b:free`
**Dimension averages:** total 38.7, task 8, requirements 14, boundaries 3.3, concrete 3.3
**Attempts:** 6 total; **usable:** 3
**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**How to improve:** Improve boundaries evidence: add one explicit, testable requirement/example for this dimension and a failure-boundary example.
**Second-pass grade:** **30/100 — WEAK** (2205 response characters).
**Second-pass evidence:** Second-pass response evidence: task=0/20, assumptions=0/20, boundaries=0/20, verification=10/20, contract=10/10; weakest=task; field=reasoning.
**Second-pass improvement:** put the useful domain answer before persona framing and show a concrete output.
**Third-pass grade:** **50/100 — MIXED** (2930 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 0/20, assumption 0/15, boundary/failure 0/15, verification 10/10, revision 10/10, nonempty 10/10; weakest=requirements; field=reasoning.
**Third-pass improvement:** name which active-skill requirements were satisfied and which were missed, with evidence for each.
**Fourth-pass grade:** **43/100 — MIXED** (2595 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 10/20, addressed requirements 0/20, unmet requirements 5/10, complete/pending 10/10, verification 8/15, limitation/failure 0/10, ledger structure 0/5, nonempty 10/10; weakest=addressed; field=reasoning.
**Fourth-pass improvement:** name the active minimum requirements and map each to evidence in the result.
## Skill: `demis-hassabis`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**Live Kilo grade:** **49/100 — MIXED** (3432 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 13/20, requirements 18/35, boundaries 2/20, verification 4/15, concrete 2/15; weakest=boundaries; response field=reasoning.
**How to improve:** state concrete invalid-input, refusal, uncertainty, edge-case, and failure behavior.
**Second-pass grade:** **50/100 — MIXED** (3364 response characters).
**Second-pass evidence:** Second-pass response evidence: task=10/20, assumptions=0/20, boundaries=10/20, verification=10/20, contract=10/10; weakest=assumptions; field=reasoning.
**Second-pass improvement:** always state assumptions explicitly, including what information is missing.
**Third-pass grade:** **56/100 — MIXED** (4105 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 6/20, assumption 0/15, boundary/failure 0/15, verification 10/10, revision 10/10, nonempty 10/10; weakest=assumption; field=reasoning.
**Third-pass improvement:** state one specific unsafe or weak assumption and explain how the answer changes if it is false.
**Fourth-pass grade:** **83/100 — PROMISING** (3233 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 20/20, addressed requirements 20/20, unmet requirements 10/10, complete/pending 10/10, verification 8/15, limitation/failure 0/10, ledger structure 5/5, nonempty 10/10; weakest=limitation; field=reasoning.
**Fourth-pass improvement:** state a concrete failure, boundary, invalid-input, or uncertainty condition and the safe response.
## Skill: `dennis-ritchie`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**Live Kilo grade:** **56/100 — MIXED** (3054 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 15/20, requirements 19/35, boundaries 2/20, verification 2/15, concrete 8/15; weakest=boundaries; response field=reasoning.
**How to improve:** state concrete invalid-input, refusal, uncertainty, edge-case, and failure behavior.
**Second-pass grade:** **40/100 — MIXED** (3183 response characters).
**Second-pass evidence:** Second-pass response evidence: task=10/20, assumptions=0/20, boundaries=0/20, verification=10/20, contract=10/10; weakest=assumptions; field=reasoning.
**Second-pass improvement:** always state assumptions explicitly, including what information is missing.
**Third-pass grade:** **35/100 — WEAK** (3035 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 0/20, assumption 0/15, boundary/failure 0/15, verification 5/10, revision 0/10, nonempty 10/10; weakest=requirements; field=reasoning.
**Third-pass improvement:** name which active-skill requirements were satisfied and which were missed, with evidence for each.
**Fourth-pass grade:** **100/100 — PROMISING** (3368 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 20/20, addressed requirements 20/20, unmet requirements 10/10, complete/pending 10/10, verification 15/15, limitation/failure 10/10, ledger structure 5/5, nonempty 10/10; weakest=ledger; field=reasoning.
**Fourth-pass improvement:** use a clearly labeled contract ledger with all requested fields.
## Skill: `desert-island`

**Live score:** **30/100** (range 30–30; 1 usable responses)
**Models observed:** `openai/gpt-oss-20b:free`
**Dimension averages:** total 30, task 11, requirements 2, boundaries 5, concrete 2
**Attempts:** 6 total; **usable:** 1
**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=missing, cross_language=pass.
**How to improve:** Improve requirements evidence: add one explicit, testable requirement/example for this dimension and a failure-boundary example.
**Second-pass grade:** **60/100 — MIXED** (3071 response characters).
**Second-pass evidence:** Second-pass response evidence: task=20/20, assumptions=10/20, boundaries=0/20, verification=10/20, contract=10/10; weakest=boundaries; field=reasoning.
**Second-pass improvement:** name a likely failure and a concrete refusal, uncertainty, or limit condition.
**Third-pass grade:** **75/100 — PROMISING** (3420 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 20/20, assumption 0/15, boundary/failure 15/15, verification 10/10, revision 0/10, nonempty 10/10; weakest=assumption; field=reasoning.
**Third-pass improvement:** state one specific unsafe or weak assumption and explain how the answer changes if it is false.
**Fourth-pass grade:** **59/100 — MIXED** (3349 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 20/20, addressed requirements 6/20, unmet requirements 0/10, complete/pending 10/10, verification 8/15, limitation/failure 0/10, ledger structure 5/5, nonempty 10/10; weakest=unmet; field=reasoning.
**Fourth-pass improvement:** explicitly list every unmet requirement instead of implying full completion.
## Skill: `dijkstra`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**Live Kilo grade:** **45/100 — MIXED** (2760 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 11/20, requirements 14/35, boundaries 2/20, verification 6/15, concrete 2/15; weakest=boundaries; response field=reasoning.
**How to improve:** state concrete invalid-input, refusal, uncertainty, edge-case, and failure behavior.
**Second-pass grade:** **40/100 — MIXED** (2585 response characters).
**Second-pass evidence:** Second-pass response evidence: task=10/20, assumptions=10/20, boundaries=0/20, verification=0/20, contract=10/10; weakest=boundaries; field=reasoning.
**Second-pass improvement:** name a likely failure and a concrete refusal, uncertainty, or limit condition.
**Third-pass grade:** **46/100 — MIXED** (3226 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 6/20, assumption 0/15, boundary/failure 0/15, verification 10/10, revision 0/10, nonempty 10/10; weakest=assumption; field=reasoning.
**Third-pass improvement:** state one specific unsafe or weak assumption and explain how the answer changes if it is false.
**Fourth-pass grade:** **49/100 — MIXED** (2958 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 15/20, addressed requirements 6/20, unmet requirements 0/10, complete/pending 5/10, verification 8/15, limitation/failure 0/10, ledger structure 5/5, nonempty 10/10; weakest=unmet; field=reasoning.
**Fourth-pass improvement:** explicitly list every unmet requirement instead of implying full completion.
## Skill: `doppelganger`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**Live Kilo grade:** **60/100 — PROMISING** (3105 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 11/20, requirements 16/35, boundaries 8/20, verification 4/15, concrete 11/15; weakest=verification; response field=reasoning.
**How to improve:** add an explicit check, expected result, metric, or reviewable verification step.
**Second-pass grade:** **60/100 — MIXED** (3277 response characters).
**Second-pass evidence:** Second-pass response evidence: task=20/20, assumptions=0/20, boundaries=10/20, verification=10/20, contract=10/10; weakest=assumptions; field=reasoning.
**Second-pass improvement:** always state assumptions explicitly, including what information is missing.
**Third-pass grade:** **54/100 — MIXED** (3368 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 6/20, assumption 0/15, boundary/failure 8/15, verification 10/10, revision 0/10, nonempty 10/10; weakest=assumption; field=reasoning.
**Third-pass improvement:** state one specific unsafe or weak assumption and explain how the answer changes if it is false.
**Fourth-pass grade:** **59/100 — MIXED** (2549 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 20/20, addressed requirements 6/20, unmet requirements 0/10, complete/pending 5/10, verification 8/15, limitation/failure 10/10, ledger structure 0/5, nonempty 10/10; weakest=unmet; field=reasoning.
**Fourth-pass improvement:** explicitly list every unmet requirement instead of implying full completion.
## Skill: `druckenmiller`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**Live Kilo grade:** **57/100 — MIXED** (2863 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 9/20, requirements 20/35, boundaries 8/20, verification 8/15, concrete 2/15; weakest=concrete; response field=reasoning.
**How to improve:** replace general advice with a concrete input/output example, procedure, or implementation sketch.
**Second-pass grade:** **80/100 — PROMISING** (2835 response characters).
**Second-pass evidence:** Second-pass response evidence: task=10/20, assumptions=10/20, boundaries=20/20, verification=20/20, contract=10/10; weakest=task; field=reasoning.
**Second-pass improvement:** put the useful domain answer before persona framing and show a concrete output.
**Third-pass grade:** **77/100 — PROMISING** (3216 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 15/20, requirement audit 14/20, assumption 8/15, boundary/failure 15/15, verification 5/10, revision 10/10, nonempty 10/10; weakest=verification; field=reasoning.
**Third-pass improvement:** add a concrete verification step with an expected result, metric, or assertion.
**Fourth-pass grade:** **78/100 — PROMISING** (3016 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 10/20, addressed requirements 20/20, unmet requirements 10/10, complete/pending 10/10, verification 8/15, limitation/failure 5/10, ledger structure 5/5, nonempty 10/10; weakest=limitation; field=reasoning.
**Fourth-pass improvement:** state a concrete failure, boundary, invalid-input, or uncertainty condition and the safe response.
## Skill: `edward-tufte`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**Live Kilo grade:** **50/100 — MIXED** (3074 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 13/20, requirements 15/35, boundaries 2/20, verification 6/15, concrete 4/15; weakest=boundaries; response field=reasoning.
**How to improve:** state concrete invalid-input, refusal, uncertainty, edge-case, and failure behavior.
**Second-pass grade:** **80/100 — PROMISING** (3039 response characters).
**Second-pass evidence:** Second-pass response evidence: task=10/20, assumptions=20/20, boundaries=10/20, verification=20/20, contract=10/10; weakest=task; field=reasoning.
**Second-pass improvement:** put the useful domain answer before persona framing and show a concrete output.
**Third-pass grade:** **54/100 — MIXED** (3460 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 14/20, assumption 0/15, boundary/failure 0/15, verification 10/10, revision 0/10, nonempty 10/10; weakest=assumption; field=reasoning.
**Third-pass improvement:** state one specific unsafe or weak assumption and explain how the answer changes if it is false.
**Fourth-pass grade:** **41/100 — MIXED** (2984 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 20/20, addressed requirements 6/20, unmet requirements 0/10, complete/pending 0/10, verification 0/15, limitation/failure 0/10, ledger structure 5/5, nonempty 10/10; weakest=unmet; field=reasoning.
**Fourth-pass improvement:** explicitly list every unmet requirement instead of implying full completion.
## Skill: `emmy-noether`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**Live Kilo grade:** **49/100 — MIXED** (3264 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 13/20, requirements 16/35, boundaries 6/20, verification 2/15, concrete 2/15; weakest=verification; response field=reasoning.
**How to improve:** add an explicit check, expected result, metric, or reviewable verification step.
**Second-pass grade:** **50/100 — MIXED** (3269 response characters).
**Second-pass evidence:** Second-pass response evidence: task=10/20, assumptions=0/20, boundaries=10/20, verification=10/20, contract=10/10; weakest=assumptions; field=reasoning.
**Second-pass improvement:** always state assumptions explicitly, including what information is missing.
**Third-pass grade:** **41/100 — MIXED** (3678 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 6/20, assumption 0/15, boundary/failure 0/15, verification 5/10, revision 0/10, nonempty 10/10; weakest=assumption; field=reasoning.
**Third-pass improvement:** state one specific unsafe or weak assumption and explain how the answer changes if it is false.
**Fourth-pass grade:** **48/100 — MIXED** (3532 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 20/20, addressed requirements 0/20, unmet requirements 0/10, complete/pending 0/10, verification 8/15, limitation/failure 5/10, ledger structure 5/5, nonempty 10/10; weakest=addressed; field=reasoning.
**Fourth-pass improvement:** name the active minimum requirements and map each to evidence in the result.
## Skill: `fedora-hat-guy`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=missing, cross_language=pass.
**Live Kilo grade:** **75/100 — PROMISING** (2790 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 15/20, requirements 27/35, boundaries 4/20, verification 6/15, concrete 13/15; weakest=boundaries; response field=reasoning.
**How to improve:** state concrete invalid-input, refusal, uncertainty, edge-case, and failure behavior.
**Second-pass grade:** **60/100 — MIXED** (2763 response characters).
**Second-pass evidence:** Second-pass response evidence: task=20/20, assumptions=0/20, boundaries=10/20, verification=10/20, contract=10/10; weakest=assumptions; field=reasoning.
**Second-pass improvement:** always state assumptions explicitly, including what information is missing.
**Third-pass grade:** **56/100 — MIXED** (3142 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 6/20, assumption 0/15, boundary/failure 0/15, verification 10/10, revision 10/10, nonempty 10/10; weakest=assumption; field=reasoning.
**Third-pass improvement:** state one specific unsafe or weak assumption and explain how the answer changes if it is false.
**Fourth-pass grade:** **75/100 — PROMISING** (3188 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 20/20, addressed requirements 20/20, unmet requirements 0/10, complete/pending 0/10, verification 15/15, limitation/failure 5/10, ledger structure 5/5, nonempty 10/10; weakest=unmet; field=reasoning.
**Fourth-pass improvement:** explicitly list every unmet requirement instead of implying full completion.
## Skill: `fei-fei-li`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**Live Kilo grade:** **63/100 — PROMISING** (3390 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 13/20, requirements 24/35, boundaries 4/20, verification 6/15, concrete 6/15; weakest=boundaries; response field=reasoning.
**How to improve:** state concrete invalid-input, refusal, uncertainty, edge-case, and failure behavior.
**Second-pass grade:** **40/100 — MIXED** (3306 response characters).
**Second-pass evidence:** Second-pass response evidence: task=10/20, assumptions=0/20, boundaries=0/20, verification=10/20, contract=10/10; weakest=assumptions; field=reasoning.
**Second-pass improvement:** always state assumptions explicitly, including what information is missing.
**Third-pass grade:** **40/100 — MIXED** (3654 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 0/20, assumption 0/15, boundary/failure 0/15, verification 10/10, revision 0/10, nonempty 10/10; weakest=requirements; field=reasoning.
**Third-pass improvement:** name which active-skill requirements were satisfied and which were missed, with evidence for each.
**Fourth-pass grade:** **73/100 — PROMISING** (3709 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 20/20, addressed requirements 20/20, unmet requirements 10/10, complete/pending 0/10, verification 8/15, limitation/failure 0/10, ledger structure 5/5, nonempty 10/10; weakest=pending; field=reasoning.
**Fourth-pass improvement:** separate completed work from pending work and state what remains to finish.
## Skill: `feynman`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**Live Kilo grade:** **54/100 — MIXED** (3003 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 15/20, requirements 21/35, boundaries 2/20, verification 4/15, concrete 2/15; weakest=boundaries; response field=reasoning.
**How to improve:** state concrete invalid-input, refusal, uncertainty, edge-case, and failure behavior.
**Second-pass grade:** **80/100 — PROMISING** (2962 response characters).
**Second-pass evidence:** Second-pass response evidence: task=20/20, assumptions=10/20, boundaries=10/20, verification=20/20, contract=10/10; weakest=assumptions; field=reasoning.
**Second-pass improvement:** always state assumptions explicitly, including what information is missing.
**Third-pass grade:** **50/100 — MIXED** (3336 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 0/20, assumption 0/15, boundary/failure 0/15, verification 10/10, revision 10/10, nonempty 10/10; weakest=requirements; field=reasoning.
**Third-pass improvement:** name which active-skill requirements were satisfied and which were missed, with evidence for each.
**Fourth-pass grade:** **53/100 — MIXED** (2306 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 20/20, addressed requirements 0/20, unmet requirements 0/10, complete/pending 0/10, verification 8/15, limitation/failure 10/10, ledger structure 5/5, nonempty 10/10; weakest=addressed; field=reasoning.
**Fourth-pass improvement:** name the active minimum requirements and map each to evidence in the result.
## Skill: `fibonacci`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**Live Kilo grade:** **50/100 — MIXED** (2290 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 11/20, requirements 17/35, boundaries 6/20, verification 2/15, concrete 4/15; weakest=verification; response field=reasoning.
**How to improve:** add an explicit check, expected result, metric, or reviewable verification step.
**Second-pass grade:** **60/100 — MIXED** (1878 response characters).
**Second-pass evidence:** Second-pass response evidence: task=0/20, assumptions=10/20, boundaries=10/20, verification=20/20, contract=10/10; weakest=task; field=reasoning.
**Second-pass improvement:** put the useful domain answer before persona framing and show a concrete output.
**Third-pass grade:** **40/100 — MIXED** (2224 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 0/20, assumption 0/15, boundary/failure 0/15, verification 10/10, revision 0/10, nonempty 10/10; weakest=requirements; field=reasoning.
**Third-pass improvement:** name which active-skill requirements were satisfied and which were missed, with evidence for each.
**Fourth-pass grade:** **54/100 — MIXED** (2845 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 20/20, addressed requirements 6/20, unmet requirements 0/10, complete/pending 0/10, verification 8/15, limitation/failure 5/10, ledger structure 5/5, nonempty 10/10; weakest=unmet; field=reasoning.
**Fourth-pass improvement:** explicitly list every unmet requirement instead of implying full completion.
## Skill: `floor-trader`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**Live Kilo grade:** **56/100 — MIXED** (2563 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 13/20, requirements 23/35, boundaries 4/20, verification 2/15, concrete 4/15; weakest=verification; response field=reasoning.
**How to improve:** add an explicit check, expected result, metric, or reviewable verification step.
**Second-pass grade:** **30/100 — WEAK** (2461 response characters).
**Second-pass evidence:** Second-pass response evidence: task=0/20, assumptions=0/20, boundaries=10/20, verification=0/20, contract=10/10; weakest=task; field=reasoning.
**Second-pass improvement:** put the useful domain answer before persona framing and show a concrete output.
**Third-pass grade:** **55/100 — MIXED** (2679 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 0/20, assumption 0/15, boundary/failure 15/15, verification 0/10, revision 10/10, nonempty 10/10; weakest=requirements; field=reasoning.
**Third-pass improvement:** name which active-skill requirements were satisfied and which were missed, with evidence for each.
**Fourth-pass grade:** **25/100 — WEAK** (2674 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 10/20, addressed requirements 0/20, unmet requirements 0/10, complete/pending 0/10, verification 0/15, limitation/failure 0/10, ledger structure 5/5, nonempty 10/10; weakest=addressed; field=reasoning.
**Fourth-pass improvement:** name the active minimum requirements and map each to evidence in the result.
## Skill: `forensic-money-trail`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**Live Kilo grade:** **34/100 — WEAK** (2700 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 13/20, requirements 9/35, boundaries 0/20, verification 2/15, concrete 0/15; weakest=boundaries; response field=reasoning.
**How to improve:** state concrete invalid-input, refusal, uncertainty, edge-case, and failure behavior.
**Second-pass grade:** **30/100 — WEAK** (2644 response characters).
**Second-pass evidence:** Second-pass response evidence: task=0/20, assumptions=0/20, boundaries=0/20, verification=10/20, contract=10/10; weakest=task; field=reasoning.
**Second-pass improvement:** put the useful domain answer before persona framing and show a concrete output.
**Third-pass grade:** **40/100 — MIXED** (2824 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 0/20, assumption 0/15, boundary/failure 0/15, verification 10/10, revision 0/10, nonempty 10/10; weakest=requirements; field=reasoning.
**Third-pass improvement:** name which active-skill requirements were satisfied and which were missed, with evidence for each.
**Fourth-pass grade:** **44/100 — MIXED** (2231 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 10/20, addressed requirements 6/20, unmet requirements 0/10, complete/pending 5/10, verification 8/15, limitation/failure 0/10, ledger structure 5/5, nonempty 10/10; weakest=unmet; field=reasoning.
**Fourth-pass improvement:** explicitly list every unmet requirement instead of implying full completion.
## Skill: `frances-allen`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**Live Kilo grade:** **46/100 — MIXED** (2682 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 11/20, requirements 12/35, boundaries 0/20, verification 2/15, concrete 11/15; weakest=boundaries; response field=reasoning.
**How to improve:** state concrete invalid-input, refusal, uncertainty, edge-case, and failure behavior.
**Second-pass grade:** **40/100 — MIXED** (2684 response characters).
**Second-pass evidence:** Second-pass response evidence: task=10/20, assumptions=0/20, boundaries=0/20, verification=10/20, contract=10/10; weakest=assumptions; field=reasoning.
**Second-pass improvement:** always state assumptions explicitly, including what information is missing.
**Third-pass grade:** **46/100 — MIXED** (2532 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 6/20, assumption 0/15, boundary/failure 0/15, verification 5/10, revision 5/10, nonempty 10/10; weakest=assumption; field=reasoning.
**Third-pass improvement:** state one specific unsafe or weak assumption and explain how the answer changes if it is false.
**Fourth-pass grade:** **44/100 — MIXED** (2896 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 20/20, addressed requirements 6/20, unmet requirements 0/10, complete/pending 0/10, verification 8/15, limitation/failure 0/10, ledger structure 0/5, nonempty 10/10; weakest=unmet; field=reasoning.
**Fourth-pass improvement:** explicitly list every unmet requirement instead of implying full completion.
## Skill: `frank-lloyd-wright`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**Live Kilo grade:** **53/100 — MIXED** (3058 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 13/20, requirements 22/35, boundaries 0/20, verification 0/15, concrete 8/15; weakest=boundaries; response field=reasoning.
**How to improve:** state concrete invalid-input, refusal, uncertainty, edge-case, and failure behavior.
**Second-pass grade:** **50/100 — MIXED** (3396 response characters).
**Second-pass evidence:** Second-pass response evidence: task=10/20, assumptions=0/20, boundaries=10/20, verification=10/20, contract=10/10; weakest=assumptions; field=reasoning.
**Second-pass improvement:** always state assumptions explicitly, including what information is missing.
**Third-pass grade:** **71/100 — PROMISING** (3846 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 6/20, assumption 0/15, boundary/failure 15/15, verification 10/10, revision 10/10, nonempty 10/10; weakest=assumption; field=reasoning.
**Third-pass improvement:** state one specific unsafe or weak assumption and explain how the answer changes if it is false.
**Fourth-pass grade:** **45/100 — MIXED** (3792 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 20/20, addressed requirements 0/20, unmet requirements 0/10, complete/pending 0/10, verification 0/15, limitation/failure 10/10, ledger structure 5/5, nonempty 10/10; weakest=addressed; field=reasoning.
**Fourth-pass improvement:** name the active minimum requirements and map each to evidence in the result.
## Skill: `fred-rogers`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=missing, cross_language=pass.
**Live Kilo grade:** **81/100 — PROMISING** (2868 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 19/20, requirements 29/35, boundaries 4/20, verification 6/15, concrete 13/15; weakest=boundaries; response field=reasoning.
**How to improve:** state concrete invalid-input, refusal, uncertainty, edge-case, and failure behavior.
**Second-pass grade:** **70/100 — PROMISING** (2851 response characters).
**Second-pass evidence:** Second-pass response evidence: task=20/20, assumptions=20/20, boundaries=0/20, verification=10/20, contract=10/10; weakest=boundaries; field=reasoning.
**Second-pass improvement:** name a likely failure and a concrete refusal, uncertainty, or limit condition.
**Third-pass grade:** **50/100 — MIXED** (3317 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 0/20, assumption 0/15, boundary/failure 0/15, verification 10/10, revision 10/10, nonempty 10/10; weakest=requirements; field=reasoning.
**Third-pass improvement:** name which active-skill requirements were satisfied and which were missed, with evidence for each.
**Fourth-pass grade:** **88/100 — PROMISING** (3347 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 20/20, addressed requirements 20/20, unmet requirements 10/10, complete/pending 10/10, verification 8/15, limitation/failure 5/10, ledger structure 5/5, nonempty 10/10; weakest=limitation; field=reasoning.
**Fourth-pass improvement:** state a concrete failure, boundary, invalid-input, or uncertainty condition and the safe response.
## Skill: `funeral`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**Live Kilo grade:** **69/100 — PROMISING** (3278 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 15/20, requirements 28/35, boundaries 6/20, verification 6/15, concrete 4/15; weakest=concrete; response field=reasoning.
**How to improve:** replace general advice with a concrete input/output example, procedure, or implementation sketch.
**Second-pass grade:** **60/100 — MIXED** (3087 response characters).
**Second-pass evidence:** Second-pass response evidence: task=20/20, assumptions=0/20, boundaries=10/20, verification=10/20, contract=10/10; weakest=assumptions; field=reasoning.
**Second-pass improvement:** always state assumptions explicitly, including what information is missing.
**Third-pass grade:** **56/100 — MIXED** (3688 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 6/20, assumption 0/15, boundary/failure 15/15, verification 5/10, revision 0/10, nonempty 10/10; weakest=assumption; field=reasoning.
**Third-pass improvement:** state one specific unsafe or weak assumption and explain how the answer changes if it is false.
**Fourth-pass grade:** **59/100 — MIXED** (3590 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 20/20, addressed requirements 6/20, unmet requirements 0/10, complete/pending 0/10, verification 8/15, limitation/failure 10/10, ledger structure 5/5, nonempty 10/10; weakest=unmet; field=reasoning.
**Fourth-pass improvement:** explicitly list every unmet requirement instead of implying full completion.
## Skill: `gates`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**Live Kilo grade:** **54/100 — MIXED** (2778 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 9/20, requirements 23/35, boundaries 6/20, verification 4/15, concrete 2/15; weakest=concrete; response field=reasoning.
**How to improve:** replace general advice with a concrete input/output example, procedure, or implementation sketch.
**Second-pass grade:** **50/100 — MIXED** (3037 response characters).
**Second-pass evidence:** Second-pass response evidence: task=0/20, assumptions=0/20, boundaries=20/20, verification=10/20, contract=10/10; weakest=task; field=reasoning.
**Second-pass improvement:** put the useful domain answer before persona framing and show a concrete output.
**Third-pass grade:** **61/100 — MIXED** (3102 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 6/20, assumption 0/15, boundary/failure 15/15, verification 0/10, revision 10/10, nonempty 10/10; weakest=assumption; field=reasoning.
**Third-pass improvement:** state one specific unsafe or weak assumption and explain how the answer changes if it is false.
**Fourth-pass grade:** **54/100 — MIXED** (3194 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 15/20, addressed requirements 6/20, unmet requirements 0/10, complete/pending 10/10, verification 8/15, limitation/failure 0/10, ledger structure 5/5, nonempty 10/10; weakest=unmet; field=reasoning.
**Fourth-pass improvement:** explicitly list every unmet requirement instead of implying full completion.
## Skill: `geoffrey-hinton`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**Live Kilo grade:** **65/100 — PROMISING** (3278 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 15/20, requirements 21/35, boundaries 4/20, verification 9/15, concrete 6/15; weakest=boundaries; response field=reasoning.
**How to improve:** state concrete invalid-input, refusal, uncertainty, edge-case, and failure behavior.
**Second-pass grade:** **60/100 — MIXED** (3218 response characters).
**Second-pass evidence:** Second-pass response evidence: task=10/20, assumptions=0/20, boundaries=20/20, verification=10/20, contract=10/10; weakest=assumptions; field=reasoning.
**Second-pass improvement:** always state assumptions explicitly, including what information is missing.
**Third-pass grade:** **85/100 — PROMISING** (3706 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 20/20, assumption 0/15, boundary/failure 15/15, verification 10/10, revision 10/10, nonempty 10/10; weakest=assumption; field=reasoning.
**Third-pass improvement:** state one specific unsafe or weak assumption and explain how the answer changes if it is false.
**Fourth-pass grade:** **59/100 — MIXED** (3091 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 20/20, addressed requirements 6/20, unmet requirements 0/10, complete/pending 10/10, verification 8/15, limitation/failure 0/10, ledger structure 5/5, nonempty 10/10; weakest=unmet; field=reasoning.
**Fourth-pass improvement:** explicitly list every unmet requirement instead of implying full completion.
## Skill: `george-polya`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**Live Kilo grade:** **47/100 — MIXED** (2618 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 9/20, requirements 16/35, boundaries 4/20, verification 4/15, concrete 4/15; weakest=boundaries; response field=reasoning.
**How to improve:** state concrete invalid-input, refusal, uncertainty, edge-case, and failure behavior.
**Second-pass grade:** **40/100 — MIXED** (3033 response characters).
**Second-pass evidence:** Second-pass response evidence: task=10/20, assumptions=0/20, boundaries=0/20, verification=10/20, contract=10/10; weakest=assumptions; field=reasoning.
**Second-pass improvement:** always state assumptions explicitly, including what information is missing.
**Third-pass grade:** **30/100 — WEAK** (3259 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 0/20, assumption 0/15, boundary/failure 0/15, verification 0/10, revision 0/10, nonempty 10/10; weakest=requirements; field=reasoning.
**Third-pass improvement:** name which active-skill requirements were satisfied and which were missed, with evidence for each.
**Fourth-pass grade:** **38/100 — WEAK** (2835 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 20/20, addressed requirements 0/20, unmet requirements 0/10, complete/pending 0/10, verification 8/15, limitation/failure 0/10, ledger structure 0/5, nonempty 10/10; weakest=addressed; field=reasoning.
**Fourth-pass improvement:** name the active minimum requirements and map each to evidence in the result.
## Skill: `god`

**Static signals:** frontmatter=pass, triggers=missing, boundaries=pass, requirements=pass, activation=pass, principles=missing, style=missing, cross_language=pass.
**Live Kilo grade:** **66/100 — PROMISING** (2822 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 13/20, requirements 17/35, boundaries 6/20, verification 9/15, concrete 11/15; weakest=boundaries; response field=reasoning.
**How to improve:** state concrete invalid-input, refusal, uncertainty, edge-case, and failure behavior.
**Second-pass grade:** **80/100 — PROMISING** (2981 response characters).
**Second-pass evidence:** Second-pass response evidence: task=10/20, assumptions=10/20, boundaries=20/20, verification=20/20, contract=10/10; weakest=task; field=reasoning.
**Second-pass improvement:** put the useful domain answer before persona framing and show a concrete output.
**Third-pass grade:** **65/100 — MIXED** (3205 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 0/20, assumption 0/15, boundary/failure 15/15, verification 10/10, revision 10/10, nonempty 10/10; weakest=requirements; field=reasoning.
**Third-pass improvement:** name which active-skill requirements were satisfied and which were missed, with evidence for each.
**Fourth-pass grade:** **61/100 — MIXED** (3371 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 20/20, addressed requirements 6/20, unmet requirements 0/10, complete/pending 0/10, verification 15/15, limitation/failure 5/10, ledger structure 5/5, nonempty 10/10; weakest=unmet; field=reasoning.
**Fourth-pass improvement:** explicitly list every unmet requirement instead of implying full completion.
## Skill: `goldfish`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=missing, cross_language=pass.
**Live Kilo grade:** **66/100 — PROMISING** (2817 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 15/20, requirements 21/35, boundaries 6/20, verification 6/15, concrete 8/15; weakest=boundaries; response field=reasoning.
**How to improve:** state concrete invalid-input, refusal, uncertainty, edge-case, and failure behavior.
**Second-pass grade:** **70/100 — PROMISING** (2755 response characters).
**Second-pass evidence:** Second-pass response evidence: task=10/20, assumptions=10/20, boundaries=10/20, verification=20/20, contract=10/10; weakest=task; field=reasoning.
**Second-pass improvement:** put the useful domain answer before persona framing and show a concrete output.
**Third-pass grade:** **49/100 — MIXED** (3188 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 6/20, assumption 0/15, boundary/failure 8/15, verification 5/10, revision 0/10, nonempty 10/10; weakest=assumption; field=reasoning.
**Third-pass improvement:** state one specific unsafe or weak assumption and explain how the answer changes if it is false.
**Fourth-pass grade:** **49/100 — MIXED** (2844 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 15/20, addressed requirements 6/20, unmet requirements 0/10, complete/pending 0/10, verification 8/15, limitation/failure 5/10, ledger structure 5/5, nonempty 10/10; weakest=unmet; field=reasoning.
**Fourth-pass improvement:** explicitly list every unmet requirement instead of implying full completion.
## Skill: `goldman-analyst`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**Live Kilo grade:** **46/100 — MIXED** (2632 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 9/20, requirements 23/35, boundaries 2/20, verification 0/15, concrete 2/15; weakest=verification; response field=reasoning.
**How to improve:** add an explicit check, expected result, metric, or reviewable verification step.
**Second-pass grade:** **30/100 — WEAK** (2457 response characters).
**Second-pass evidence:** Second-pass response evidence: task=0/20, assumptions=0/20, boundaries=10/20, verification=0/20, contract=10/10; weakest=task; field=reasoning.
**Second-pass improvement:** put the useful domain answer before persona framing and show a concrete output.
**Third-pass grade:** **48/100 — MIXED** (2786 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 15/20, requirement audit 0/20, assumption 15/15, boundary/failure 8/15, verification 0/10, revision 0/10, nonempty 10/10; weakest=requirements; field=reasoning.
**Third-pass improvement:** name which active-skill requirements were satisfied and which were missed, with evidence for each.
**Fourth-pass grade:** **41/100 — MIXED** (2689 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 10/20, addressed requirements 6/20, unmet requirements 0/10, complete/pending 0/10, verification 0/15, limitation/failure 10/10, ledger structure 5/5, nonempty 10/10; weakest=unmet; field=reasoning.
**Fourth-pass improvement:** explicitly list every unmet requirement instead of implying full completion.
## Skill: `google-sre`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=missing, cross_language=pass.
**Live Kilo grade:** **57/100 — MIXED** (2774 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 11/20, requirements 16/35, boundaries 6/20, verification 6/15, concrete 8/15; weakest=boundaries; response field=reasoning.
**How to improve:** state concrete invalid-input, refusal, uncertainty, edge-case, and failure behavior.
**Second-pass grade:** **80/100 — PROMISING** (2972 response characters).
**Second-pass evidence:** Second-pass response evidence: task=10/20, assumptions=10/20, boundaries=20/20, verification=20/20, contract=10/10; weakest=task; field=reasoning.
**Second-pass improvement:** put the useful domain answer before persona framing and show a concrete output.
**Third-pass grade:** **54/100 — MIXED** (3062 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 14/20, assumption 0/15, boundary/failure 0/15, verification 10/10, revision 0/10, nonempty 10/10; weakest=assumption; field=reasoning.
**Third-pass improvement:** state one specific unsafe or weak assumption and explain how the answer changes if it is false.
**Fourth-pass grade:** **100/100 — PROMISING** (3243 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 20/20, addressed requirements 20/20, unmet requirements 10/10, complete/pending 10/10, verification 15/15, limitation/failure 10/10, ledger structure 5/5, nonempty 10/10; weakest=ledger; field=reasoning.
**Fourth-pass improvement:** use a clearly labeled contract ledger with all requested fields.
## Skill: `gordon-ramsay`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**Live Kilo grade:** **44/100 — MIXED** (2666 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 11/20, requirements 21/35, boundaries 0/20, verification 0/15, concrete 2/15; weakest=boundaries; response field=reasoning.
**How to improve:** state concrete invalid-input, refusal, uncertainty, edge-case, and failure behavior.
**Second-pass grade:** **60/100 — MIXED** (2770 response characters).
**Second-pass evidence:** Second-pass response evidence: task=0/20, assumptions=10/20, boundaries=10/20, verification=20/20, contract=10/10; weakest=task; field=reasoning.
**Second-pass improvement:** put the useful domain answer before persona framing and show a concrete output.
**Third-pass grade:** **46/100 — MIXED** (2975 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 6/20, assumption 0/15, boundary/failure 0/15, verification 10/10, revision 0/10, nonempty 10/10; weakest=assumption; field=reasoning.
**Third-pass improvement:** state one specific unsafe or weak assumption and explain how the answer changes if it is false.
**Fourth-pass grade:** **49/100 — MIXED** (3165 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 10/20, addressed requirements 6/20, unmet requirements 0/10, complete/pending 10/10, verification 8/15, limitation/failure 0/10, ledger structure 5/5, nonempty 10/10; weakest=unmet; field=reasoning.
**Fourth-pass improvement:** explicitly list every unmet requirement instead of implying full completion.
## Skill: `grace-hopper`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**Live Kilo grade:** **63/100 — PROMISING** (3083 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 13/20, requirements 24/35, boundaries 8/20, verification 4/15, concrete 4/15; weakest=verification; response field=reasoning.
**How to improve:** add an explicit check, expected result, metric, or reviewable verification step.
**Second-pass grade:** **40/100 — MIXED** (2823 response characters).
**Second-pass evidence:** Second-pass response evidence: task=10/20, assumptions=0/20, boundaries=0/20, verification=10/20, contract=10/10; weakest=assumptions; field=reasoning.
**Second-pass improvement:** always state assumptions explicitly, including what information is missing.
**Third-pass grade:** **100/100 — PROMISING** (3758 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 20/20, assumption 15/15, boundary/failure 15/15, verification 10/10, revision 10/10, nonempty 10/10; weakest=verification; field=reasoning.
**Third-pass improvement:** add a concrete verification step with an expected result, metric, or assertion.
**Fourth-pass grade:** **50/100 — MIXED** (3201 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 20/20, addressed requirements 0/20, unmet requirements 0/10, complete/pending 0/10, verification 15/15, limitation/failure 5/10, ledger structure 0/5, nonempty 10/10; weakest=addressed; field=reasoning.
**Fourth-pass improvement:** name the active minimum requirements and map each to evidence in the result.
## Skill: `greybeard-after-midnight`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=missing, cross_language=pass.
**Live Kilo grade:** **64/100 — PROMISING** (2656 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 15/20, requirements 20/35, boundaries 2/20, verification 6/15, concrete 11/15; weakest=boundaries; response field=reasoning.
**How to improve:** state concrete invalid-input, refusal, uncertainty, edge-case, and failure behavior.
**Second-pass grade:** **50/100 — MIXED** (2872 response characters).
**Second-pass evidence:** Second-pass response evidence: task=10/20, assumptions=0/20, boundaries=10/20, verification=10/20, contract=10/10; weakest=assumptions; field=reasoning.
**Second-pass improvement:** always state assumptions explicitly, including what information is missing.
**Third-pass grade:** **38/100 — WEAK** (3110 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 0/20, assumption 0/15, boundary/failure 8/15, verification 0/10, revision 0/10, nonempty 10/10; weakest=requirements; field=reasoning.
**Third-pass improvement:** name which active-skill requirements were satisfied and which were missed, with evidence for each.
**Fourth-pass grade:** **38/100 — WEAK** (2998 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 15/20, addressed requirements 0/20, unmet requirements 0/10, complete/pending 0/10, verification 8/15, limitation/failure 5/10, ledger structure 0/5, nonempty 10/10; weakest=addressed; field=reasoning.
**Fourth-pass improvement:** name the active minimum requirements and map each to evidence in the result.
## Skill: `hastings`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=missing, cross_language=pass.
**Live Kilo grade:** **63/100 — PROMISING** (2925 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 9/20, requirements 26/35, boundaries 8/20, verification 6/15, concrete 4/15; weakest=concrete; response field=reasoning.
**How to improve:** replace general advice with a concrete input/output example, procedure, or implementation sketch.
**Second-pass grade:** **80/100 — PROMISING** (3048 response characters).
**Second-pass evidence:** Second-pass response evidence: task=10/20, assumptions=10/20, boundaries=20/20, verification=20/20, contract=10/10; weakest=task; field=reasoning.
**Second-pass improvement:** put the useful domain answer before persona framing and show a concrete output.
**Third-pass grade:** **69/100 — MIXED** (3618 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 14/20, assumption 0/15, boundary/failure 15/15, verification 10/10, revision 0/10, nonempty 10/10; weakest=assumption; field=reasoning.
**Third-pass improvement:** state one specific unsafe or weak assumption and explain how the answer changes if it is false.
**Fourth-pass grade:** **100/100 — PROMISING** (3544 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 20/20, addressed requirements 20/20, unmet requirements 10/10, complete/pending 10/10, verification 15/15, limitation/failure 10/10, ledger structure 5/5, nonempty 10/10; weakest=ledger; field=reasoning.
**Fourth-pass improvement:** use a clearly labeled contract ledger with all requested fields.
## Skill: `hideo-kojima`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**Live Kilo grade:** **52/100 — MIXED** (3134 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 17/20, requirements 19/35, boundaries 2/20, verification 2/15, concrete 2/15; weakest=boundaries; response field=reasoning.
**How to improve:** state concrete invalid-input, refusal, uncertainty, edge-case, and failure behavior.
**Second-pass grade:** **50/100 — MIXED** (3158 response characters).
**Second-pass evidence:** Second-pass response evidence: task=10/20, assumptions=0/20, boundaries=10/20, verification=10/20, contract=10/10; weakest=assumptions; field=reasoning.
**Second-pass improvement:** always state assumptions explicitly, including what information is missing.
**Third-pass grade:** **61/100 — MIXED** (3745 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 6/20, assumption 0/15, boundary/failure 15/15, verification 0/10, revision 10/10, nonempty 10/10; weakest=assumption; field=reasoning.
**Third-pass improvement:** state one specific unsafe or weak assumption and explain how the answer changes if it is false.
**Fourth-pass grade:** **65/100 — MIXED** (3659 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 20/20, addressed requirements 20/20, unmet requirements 0/10, complete/pending 0/10, verification 0/15, limitation/failure 10/10, ledger structure 5/5, nonempty 10/10; weakest=unmet; field=reasoning.
**Fourth-pass improvement:** explicitly list every unmet requirement instead of implying full completion.
## Skill: `hoarder`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**Live Kilo grade:** **73/100 — PROMISING** (3058 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 20/20, requirements 26/35, boundaries 0/20, verification 6/15, concrete 11/15; weakest=boundaries; response field=reasoning.
**How to improve:** state concrete invalid-input, refusal, uncertainty, edge-case, and failure behavior.
**Second-pass grade:** **30/100 — WEAK** (2321 response characters).
**Second-pass evidence:** Second-pass response evidence: task=0/20, assumptions=0/20, boundaries=0/20, verification=10/20, contract=10/10; weakest=task; field=reasoning.
**Second-pass improvement:** put the useful domain answer before persona framing and show a concrete output.
**Third-pass grade:** **61/100 — MIXED** (2659 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 6/20, assumption 0/15, boundary/failure 15/15, verification 10/10, revision 0/10, nonempty 10/10; weakest=assumption; field=reasoning.
**Third-pass improvement:** state one specific unsafe or weak assumption and explain how the answer changes if it is false.
**Fourth-pass grade:** **35/100 — WEAK** (2895 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 20/20, addressed requirements 0/20, unmet requirements 0/10, complete/pending 0/10, verification 0/15, limitation/failure 0/10, ledger structure 5/5, nonempty 10/10; weakest=addressed; field=reasoning.
**Fourth-pass improvement:** name the active minimum requirements and map each to evidence in the result.
## Skill: `hopper`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**Live Kilo grade:** **73/100 — PROMISING** (2906 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 20/20, requirements 22/35, boundaries 4/20, verification 8/15, concrete 9/15; weakest=boundaries; response field=reasoning.
**How to improve:** state concrete invalid-input, refusal, uncertainty, edge-case, and failure behavior.
**Second-pass grade:** **100/100 — PROMISING** (3326 response characters).
**Second-pass evidence:** Second-pass response evidence: task=20/20, assumptions=20/20, boundaries=20/20, verification=20/20, contract=10/10; weakest=contract; field=reasoning.
**Second-pass improvement:** tie the response to at least one named minimum requirement instead of generic advice.
**Third-pass grade:** **50/100 — MIXED** (3176 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 0/20, assumption 0/15, boundary/failure 0/15, verification 10/10, revision 10/10, nonempty 10/10; weakest=requirements; field=reasoning.
**Third-pass improvement:** name which active-skill requirements were satisfied and which were missed, with evidence for each.
**Fourth-pass grade:** **100/100 — PROMISING** (3252 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 20/20, addressed requirements 20/20, unmet requirements 10/10, complete/pending 10/10, verification 15/15, limitation/failure 10/10, ledger structure 5/5, nonempty 10/10; weakest=ledger; field=reasoning.
**Fourth-pass improvement:** use a clearly labeled contract ledger with all requested fields.
## Skill: `hostile-acquisition`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=missing, cross_language=pass.
**Live Kilo grade:** **55/100 — MIXED** (3283 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 9/20, requirements 22/35, boundaries 4/20, verification 8/15, concrete 2/15; weakest=concrete; response field=reasoning.
**How to improve:** replace general advice with a concrete input/output example, procedure, or implementation sketch.
**Second-pass grade:** **90/100 — PROMISING** (3129 response characters).
**Second-pass evidence:** Second-pass response evidence: task=10/20, assumptions=20/20, boundaries=20/20, verification=20/20, contract=10/10; weakest=task; field=reasoning.
**Second-pass improvement:** put the useful domain answer before persona framing and show a concrete output.
**Third-pass grade:** **63/100 — MIXED** (3651 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 0/20, assumption 15/15, boundary/failure 8/15, verification 10/10, revision 0/10, nonempty 10/10; weakest=requirements; field=reasoning.
**Third-pass improvement:** name which active-skill requirements were satisfied and which were missed, with evidence for each.
**Fourth-pass grade:** **46/100 — MIXED** (3617 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 15/20, addressed requirements 6/20, unmet requirements 0/10, complete/pending 0/10, verification 0/15, limitation/failure 10/10, ledger structure 5/5, nonempty 10/10; weakest=unmet; field=reasoning.
**Fourth-pass improvement:** explicitly list every unmet requirement instead of implying full completion.
## Skill: `howard-marks`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**Live Kilo grade:** **46/100 — MIXED** (3050 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 9/20, requirements 17/35, boundaries 4/20, verification 2/15, concrete 4/15; weakest=verification; response field=reasoning.
**How to improve:** add an explicit check, expected result, metric, or reviewable verification step.
**Second-pass grade:** **40/100 — MIXED** (3141 response characters).
**Second-pass evidence:** Second-pass response evidence: task=0/20, assumptions=0/20, boundaries=10/20, verification=10/20, contract=10/10; weakest=task; field=reasoning.
**Second-pass improvement:** put the useful domain answer before persona framing and show a concrete output.
**Third-pass grade:** **53/100 — MIXED** (3631 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 0/20, assumption 0/15, boundary/failure 8/15, verification 10/10, revision 5/10, nonempty 10/10; weakest=requirements; field=reasoning.
**Third-pass improvement:** name which active-skill requirements were satisfied and which were missed, with evidence for each.
**Fourth-pass grade:** **51/100 — MIXED** (3378 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 10/20, addressed requirements 6/20, unmet requirements 0/10, complete/pending 10/10, verification 0/15, limitation/failure 10/10, ledger structure 5/5, nonempty 10/10; weakest=unmet; field=reasoning.
**Fourth-pass improvement:** explicitly list every unmet requirement instead of implying full completion.
## Skill: `huang`

**Static signals:** frontmatter=pass, triggers=missing, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**Live Kilo grade:** **48/100 — MIXED** (2940 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 13/20, requirements 15/35, boundaries 2/20, verification 4/15, concrete 4/15; weakest=boundaries; response field=reasoning.
**How to improve:** state concrete invalid-input, refusal, uncertainty, edge-case, and failure behavior.
**Second-pass grade:** **40/100 — MIXED** (2717 response characters).
**Second-pass evidence:** Second-pass response evidence: task=20/20, assumptions=0/20, boundaries=0/20, verification=0/20, contract=10/10; weakest=assumptions; field=reasoning.
**Second-pass improvement:** always state assumptions explicitly, including what information is missing.
**Third-pass grade:** **30/100 — WEAK** (3238 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 0/20, assumption 0/15, boundary/failure 0/15, verification 0/10, revision 0/10, nonempty 10/10; weakest=requirements; field=reasoning.
**Third-pass improvement:** name which active-skill requirements were satisfied and which were missed, with evidence for each.
**Fourth-pass grade:** **59/100 — MIXED** (3341 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 20/20, addressed requirements 6/20, unmet requirements 0/10, complete/pending 0/10, verification 8/15, limitation/failure 10/10, ledger structure 5/5, nonempty 10/10; weakest=unmet; field=reasoning.
**Fourth-pass improvement:** explicitly list every unmet requirement instead of implying full completion.
## Skill: `icahn`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**Live Kilo grade:** **42/100 — MIXED** (2368 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 9/20, requirements 17/35, boundaries 0/20, verification 6/15, concrete 0/15; weakest=boundaries; response field=reasoning.
**How to improve:** state concrete invalid-input, refusal, uncertainty, edge-case, and failure behavior.
**Second-pass grade:** **40/100 — MIXED** (2335 response characters).
**Second-pass evidence:** Second-pass response evidence: task=10/20, assumptions=0/20, boundaries=0/20, verification=10/20, contract=10/10; weakest=assumptions; field=reasoning.
**Second-pass improvement:** always state assumptions explicitly, including what information is missing.
**Third-pass grade:** **44/100 — MIXED** (2469 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 10/20, requirement audit 14/20, assumption 0/15, boundary/failure 0/15, verification 10/10, revision 0/10, nonempty 10/10; weakest=assumption; field=reasoning.
**Third-pass improvement:** state one specific unsafe or weak assumption and explain how the answer changes if it is false.
**Fourth-pass grade:** **49/100 — MIXED** (3175 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 10/20, addressed requirements 14/20, unmet requirements 5/10, complete/pending 0/10, verification 0/15, limitation/failure 5/10, ledger structure 5/5, nonempty 10/10; weakest=pending; field=reasoning.
**Fourth-pass improvement:** separate completed work from pending work and state what remains to finish.
## Skill: `insomniac`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=missing, cross_language=pass.
**Live Kilo grade:** **58/100 — MIXED** (3129 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 15/20, requirements 25/35, boundaries 2/20, verification 4/15, concrete 2/15; weakest=boundaries; response field=reasoning.
**How to improve:** state concrete invalid-input, refusal, uncertainty, edge-case, and failure behavior.
**Second-pass grade:** **70/100 — PROMISING** (3118 response characters).
**Second-pass evidence:** Second-pass response evidence: task=20/20, assumptions=10/20, boundaries=10/20, verification=10/20, contract=10/10; weakest=assumptions; field=reasoning.
**Second-pass improvement:** always state assumptions explicitly, including what information is missing.
**Third-pass grade:** **55/100 — MIXED** (3343 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 20/20, assumption 0/15, boundary/failure 0/15, verification 5/10, revision 0/10, nonempty 10/10; weakest=assumption; field=reasoning.
**Third-pass improvement:** state one specific unsafe or weak assumption and explain how the answer changes if it is false.
**Fourth-pass grade:** **70/100 — PROMISING** (3215 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 20/20, addressed requirements 0/20, unmet requirements 5/10, complete/pending 10/10, verification 15/15, limitation/failure 10/10, ledger structure 0/5, nonempty 10/10; weakest=addressed; field=reasoning.
**Fourth-pass improvement:** name the active minimum requirements and map each to evidence in the result.
## Skill: `isaac-newton`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**Live Kilo grade:** **61/100 — PROMISING** (2952 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 15/20, requirements 23/35, boundaries 4/20, verification 9/15, concrete 0/15; weakest=concrete; response field=reasoning.
**How to improve:** replace general advice with a concrete input/output example, procedure, or implementation sketch.
**Second-pass grade:** **40/100 — MIXED** (2932 response characters).
**Second-pass evidence:** Second-pass response evidence: task=10/20, assumptions=0/20, boundaries=0/20, verification=10/20, contract=10/10; weakest=assumptions; field=reasoning.
**Second-pass improvement:** always state assumptions explicitly, including what information is missing.
**Third-pass grade:** **62/100 — MIXED** (3167 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 14/20, assumption 8/15, boundary/failure 0/15, verification 10/10, revision 0/10, nonempty 10/10; weakest=boundary; field=reasoning.
**Third-pass improvement:** give one concrete failure, refusal, uncertainty, or edge-case condition and the safe response.
**Fourth-pass grade:** **88/100 — PROMISING** (3260 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 15/20, addressed requirements 20/20, unmet requirements 10/10, complete/pending 10/10, verification 8/15, limitation/failure 10/10, ledger structure 5/5, nonempty 10/10; weakest=ledger; field=reasoning.
**Fourth-pass improvement:** use a clearly labeled contract ledger with all requested fields.
## Skill: `james-cameron`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**Live Kilo grade:** **42/100 — MIXED** (3270 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 13/20, requirements 15/35, boundaries 2/20, verification 0/15, concrete 2/15; weakest=verification; response field=reasoning.
**How to improve:** add an explicit check, expected result, metric, or reviewable verification step.
**Second-pass grade:** **50/100 — MIXED** (3384 response characters).
**Second-pass evidence:** Second-pass response evidence: task=10/20, assumptions=0/20, boundaries=10/20, verification=10/20, contract=10/10; weakest=assumptions; field=reasoning.
**Second-pass improvement:** always state assumptions explicitly, including what information is missing.
**Third-pass grade:** **69/100 — MIXED** (3632 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 14/20, assumption 0/15, boundary/failure 15/15, verification 10/10, revision 0/10, nonempty 10/10; weakest=assumption; field=reasoning.
**Third-pass improvement:** state one specific unsafe or weak assumption and explain how the answer changes if it is false.
**Fourth-pass grade:** **88/100 — PROMISING** (3748 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 20/20, addressed requirements 20/20, unmet requirements 10/10, complete/pending 10/10, verification 8/15, limitation/failure 5/10, ledger structure 5/5, nonempty 10/10; weakest=limitation; field=reasoning.
**Fourth-pass improvement:** state a concrete failure, boundary, invalid-input, or uncertainty condition and the safe response.
## Skill: `jane-goodall`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**Live Kilo grade:** **56/100 — MIXED** (3021 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 11/20, requirements 27/35, boundaries 0/20, verification 8/15, concrete 0/15; weakest=boundaries; response field=reasoning.
**How to improve:** state concrete invalid-input, refusal, uncertainty, edge-case, and failure behavior.
**Second-pass grade:** **60/100 — MIXED** (2985 response characters).
**Second-pass evidence:** Second-pass response evidence: task=10/20, assumptions=20/20, boundaries=0/20, verification=10/20, contract=10/10; weakest=boundaries; field=reasoning.
**Second-pass improvement:** name a likely failure and a concrete refusal, uncertainty, or limit condition.
**Third-pass grade:** **55/100 — MIXED** (3367 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 0/20, assumption 15/15, boundary/failure 0/15, verification 10/10, revision 0/10, nonempty 10/10; weakest=requirements; field=reasoning.
**Third-pass improvement:** name which active-skill requirements were satisfied and which were missed, with evidence for each.
**Fourth-pass grade:** **43/100 — MIXED** (3264 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 15/20, addressed requirements 0/20, unmet requirements 0/10, complete/pending 10/10, verification 8/15, limitation/failure 0/10, ledger structure 0/5, nonempty 10/10; weakest=addressed; field=reasoning.
**Fourth-pass improvement:** name the active minimum requirements and map each to evidence in the result.
## Skill: `jane-jacobs`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**Live Kilo grade:** **62/100 — PROMISING** (3346 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 17/20, requirements 19/35, boundaries 4/20, verification 6/15, concrete 6/15; weakest=boundaries; response field=reasoning.
**How to improve:** state concrete invalid-input, refusal, uncertainty, edge-case, and failure behavior.
**Second-pass grade:** **60/100 — MIXED** (3131 response characters).
**Second-pass evidence:** Second-pass response evidence: task=20/20, assumptions=0/20, boundaries=10/20, verification=10/20, contract=10/10; weakest=assumptions; field=reasoning.
**Second-pass improvement:** always state assumptions explicitly, including what information is missing.
**Third-pass grade:** **67/100 — MIXED** (3774 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 14/20, assumption 0/15, boundary/failure 8/15, verification 5/10, revision 10/10, nonempty 10/10; weakest=assumption; field=reasoning.
**Third-pass improvement:** state one specific unsafe or weak assumption and explain how the answer changes if it is false.
**Fourth-pass grade:** **59/100 — MIXED** (3656 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 20/20, addressed requirements 6/20, unmet requirements 0/10, complete/pending 10/10, verification 8/15, limitation/failure 5/10, ledger structure 0/5, nonempty 10/10; weakest=unmet; field=reasoning.
**Fourth-pass improvement:** explicitly list every unmet requirement instead of implying full completion.
## Skill: `jane-street`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**Live Kilo grade:** **70/100 — PROMISING** (3098 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 20/20, requirements 23/35, boundaries 0/20, verification 6/15, concrete 11/15; weakest=boundaries; response field=reasoning.
**How to improve:** state concrete invalid-input, refusal, uncertainty, edge-case, and failure behavior.
**Second-pass grade:** **100/100 — PROMISING** (3226 response characters).
**Second-pass evidence:** Second-pass response evidence: task=20/20, assumptions=20/20, boundaries=20/20, verification=20/20, contract=10/10; weakest=contract; field=reasoning.
**Second-pass improvement:** tie the response to at least one named minimum requirement instead of generic advice.
**Third-pass grade:** **100/100 — PROMISING** (3331 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 20/20, assumption 15/15, boundary/failure 15/15, verification 10/10, revision 10/10, nonempty 10/10; weakest=verification; field=reasoning.
**Third-pass improvement:** add a concrete verification step with an expected result, metric, or assertion.
**Fourth-pass grade:** **76/100 — PROMISING** (3283 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 20/20, addressed requirements 6/20, unmet requirements 0/10, complete/pending 10/10, verification 15/15, limitation/failure 10/10, ledger structure 5/5, nonempty 10/10; weakest=unmet; field=reasoning.
**Fourth-pass improvement:** explicitly list every unmet requirement instead of implying full completion.
## Skill: `janitor`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=missing, cross_language=pass.
**Live Kilo grade:** **66/100 — PROMISING** (3219 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 17/20, requirements 25/35, boundaries 4/20, verification 2/15, concrete 8/15; weakest=verification; response field=reasoning.
**How to improve:** add an explicit check, expected result, metric, or reviewable verification step.
**Second-pass grade:** **90/100 — PROMISING** (3282 response characters).
**Second-pass evidence:** Second-pass response evidence: task=20/20, assumptions=10/20, boundaries=20/20, verification=20/20, contract=10/10; weakest=assumptions; field=reasoning.
**Second-pass improvement:** always state assumptions explicitly, including what information is missing.
**Third-pass grade:** **54/100 — MIXED** (3800 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 6/20, assumption 0/15, boundary/failure 8/15, verification 10/10, revision 0/10, nonempty 10/10; weakest=assumption; field=reasoning.
**Third-pass improvement:** state one specific unsafe or weak assumption and explain how the answer changes if it is false.
**Fourth-pass grade:** **48/100 — MIXED** (3350 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 20/20, addressed requirements 0/20, unmet requirements 0/10, complete/pending 0/10, verification 8/15, limitation/failure 5/10, ledger structure 5/5, nonempty 10/10; weakest=addressed; field=reasoning.
**Fourth-pass improvement:** name the active minimum requirements and map each to evidence in the result.
## Skill: `jeff-dean`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**Live Kilo grade:** **54/100 — MIXED** (2991 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 13/20, requirements 25/35, boundaries 2/20, verification 2/15, concrete 2/15; weakest=boundaries; response field=reasoning.
**How to improve:** state concrete invalid-input, refusal, uncertainty, edge-case, and failure behavior.
**Second-pass grade:** **70/100 — PROMISING** (3073 response characters).
**Second-pass evidence:** Second-pass response evidence: task=20/20, assumptions=10/20, boundaries=10/20, verification=10/20, contract=10/10; weakest=assumptions; field=reasoning.
**Second-pass improvement:** always state assumptions explicitly, including what information is missing.
**Third-pass grade:** **52/100 — MIXED** (3409 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 14/20, assumption 0/15, boundary/failure 8/15, verification 0/10, revision 0/10, nonempty 10/10; weakest=assumption; field=reasoning.
**Third-pass improvement:** state one specific unsafe or weak assumption and explain how the answer changes if it is false.
**Fourth-pass grade:** **54/100 — MIXED** (3455 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 20/20, addressed requirements 6/20, unmet requirements 0/10, complete/pending 0/10, verification 8/15, limitation/failure 5/10, ledger structure 5/5, nonempty 10/10; weakest=unmet; field=reasoning.
**Fourth-pass improvement:** explicitly list every unmet requirement instead of implying full completion.
## Skill: `jeffery-epstien`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=missing, cross_language=pass.
**Live Kilo grade:** **49/100 — MIXED** (2968 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 13/20, requirements 14/35, boundaries 2/20, verification 6/15, concrete 4/15; weakest=boundaries; response field=reasoning.
**How to improve:** state concrete invalid-input, refusal, uncertainty, edge-case, and failure behavior.
**Second-pass grade:** **30/100 — WEAK** (3064 response characters).
**Second-pass evidence:** Second-pass response evidence: task=0/20, assumptions=0/20, boundaries=0/20, verification=10/20, contract=10/10; weakest=task; field=reasoning.
**Second-pass improvement:** put the useful domain answer before persona framing and show a concrete output.
**Third-pass grade:** **69/100 — MIXED** (3363 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 6/20, assumption 8/15, boundary/failure 15/15, verification 10/10, revision 0/10, nonempty 10/10; weakest=revision; field=reasoning.
**Third-pass improvement:** end with a clearly labeled revised answer that incorporates the critique.
**Fourth-pass grade:** **43/100 — MIXED** (3268 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 10/20, addressed requirements 0/20, unmet requirements 0/10, complete/pending 10/10, verification 8/15, limitation/failure 0/10, ledger structure 5/5, nonempty 10/10; weakest=addressed; field=reasoning.
**Fourth-pass improvement:** name the active minimum requirements and map each to evidence in the result.
## Skill: `jennifer-doudna`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**Live Kilo grade:** **55/100 — MIXED** (3125 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 15/20, requirements 22/35, boundaries 0/20, verification 6/15, concrete 2/15; weakest=boundaries; response field=reasoning.
**How to improve:** state concrete invalid-input, refusal, uncertainty, edge-case, and failure behavior.
**Second-pass grade:** **50/100 — MIXED** (3308 response characters).
**Second-pass evidence:** Second-pass response evidence: task=10/20, assumptions=0/20, boundaries=10/20, verification=10/20, contract=10/10; weakest=assumptions; field=reasoning.
**Second-pass improvement:** always state assumptions explicitly, including what information is missing.
**Third-pass grade:** **55/100 — MIXED** (3510 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 0/20, assumption 15/15, boundary/failure 0/15, verification 5/10, revision 5/10, nonempty 10/10; weakest=requirements; field=reasoning.
**Third-pass improvement:** name which active-skill requirements were satisfied and which were missed, with evidence for each.
**Fourth-pass grade:** **45/100 — MIXED** (3018 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 20/20, addressed requirements 0/20, unmet requirements 0/10, complete/pending 0/10, verification 15/15, limitation/failure 0/10, ledger structure 0/5, nonempty 10/10; weakest=addressed; field=reasoning.
**Fourth-pass improvement:** name the active minimum requirements and map each to evidence in the result.
## Skill: `jim-lovelock`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**Live Kilo grade:** **59/100 — MIXED** (3172 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 19/20, requirements 20/35, boundaries 2/20, verification 0/15, concrete 8/15; weakest=verification; response field=reasoning.
**How to improve:** add an explicit check, expected result, metric, or reviewable verification step.
**Second-pass grade:** **40/100 — MIXED** (3115 response characters).
**Second-pass evidence:** Second-pass response evidence: task=10/20, assumptions=0/20, boundaries=0/20, verification=10/20, contract=10/10; weakest=assumptions; field=reasoning.
**Second-pass improvement:** always state assumptions explicitly, including what information is missing.
**Third-pass grade:** **48/100 — MIXED** (3644 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 0/20, assumption 0/15, boundary/failure 8/15, verification 0/10, revision 10/10, nonempty 10/10; weakest=requirements; field=reasoning.
**Third-pass improvement:** name which active-skill requirements were satisfied and which were missed, with evidence for each.
**Fourth-pass grade:** **35/100 — WEAK** (3602 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 20/20, addressed requirements 0/20, unmet requirements 0/10, complete/pending 0/10, verification 0/15, limitation/failure 0/10, ledger structure 5/5, nonempty 10/10; weakest=addressed; field=reasoning.
**Fourth-pass improvement:** name the active minimum requirements and map each to evidence in the result.
## Skill: `jobs`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**Live Kilo grade:** **32/100 — WEAK** (3012 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 9/20, requirements 11/35, boundaries 0/20, verification 2/15, concrete 0/15; weakest=boundaries; response field=reasoning.
**How to improve:** state concrete invalid-input, refusal, uncertainty, edge-case, and failure behavior.
**Second-pass grade:** **40/100 — MIXED** (2967 response characters).
**Second-pass evidence:** Second-pass response evidence: task=10/20, assumptions=0/20, boundaries=0/20, verification=10/20, contract=10/10; weakest=assumptions; field=reasoning.
**Second-pass improvement:** always state assumptions explicitly, including what information is missing.
**Third-pass grade:** **54/100 — MIXED** (3327 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 6/20, assumption 0/15, boundary/failure 8/15, verification 0/10, revision 10/10, nonempty 10/10; weakest=assumption; field=reasoning.
**Third-pass improvement:** state one specific unsafe or weak assumption and explain how the answer changes if it is false.
**Fourth-pass grade:** **46/100 — MIXED** (3358 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 15/20, addressed requirements 6/20, unmet requirements 0/10, complete/pending 5/10, verification 0/15, limitation/failure 10/10, ledger structure 0/5, nonempty 10/10; weakest=unmet; field=reasoning.
**Fourth-pass improvement:** explicitly list every unmet requirement instead of implying full completion.
## Skill: `john-tukey`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**Live Kilo grade:** **35/100 — MIXED** (1978 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 9/20, requirements 14/35, boundaries 0/20, verification 0/15, concrete 2/15; weakest=boundaries; response field=reasoning.
**How to improve:** state concrete invalid-input, refusal, uncertainty, edge-case, and failure behavior.
**Second-pass grade:** **40/100 — MIXED** (2767 response characters).
**Second-pass evidence:** Second-pass response evidence: task=10/20, assumptions=0/20, boundaries=0/20, verification=10/20, contract=10/10; weakest=assumptions; field=reasoning.
**Second-pass improvement:** always state assumptions explicitly, including what information is missing.
**Third-pass grade:** **30/100 — WEAK** (2863 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 0/20, assumption 0/15, boundary/failure 0/15, verification 0/10, revision 0/10, nonempty 10/10; weakest=requirements; field=reasoning.
**Third-pass improvement:** name which active-skill requirements were satisfied and which were missed, with evidence for each.
**Fourth-pass grade:** **35/100 — WEAK** (2303 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 15/20, addressed requirements 0/20, unmet requirements 0/10, complete/pending 0/10, verification 0/15, limitation/failure 10/10, ledger structure 0/5, nonempty 10/10; weakest=addressed; field=reasoning.
**Fourth-pass improvement:** name the active minimum requirements and map each to evidence in the result.
## Skill: `john-von-neumann`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**Live Kilo grade:** **50/100 — MIXED** (2410 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 13/20, requirements 19/35, boundaries 0/20, verification 2/15, concrete 6/15; weakest=boundaries; response field=reasoning.
**How to improve:** state concrete invalid-input, refusal, uncertainty, edge-case, and failure behavior.
**Second-pass grade:** **40/100 — MIXED** (2774 response characters).
**Second-pass evidence:** Second-pass response evidence: task=0/20, assumptions=10/20, boundaries=0/20, verification=10/20, contract=10/10; weakest=task; field=reasoning.
**Second-pass improvement:** put the useful domain answer before persona framing and show a concrete output.
**Third-pass grade:** **41/100 — MIXED** (3599 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 6/20, assumption 0/15, boundary/failure 0/15, verification 5/10, revision 0/10, nonempty 10/10; weakest=assumption; field=reasoning.
**Third-pass improvement:** state one specific unsafe or weak assumption and explain how the answer changes if it is false.
**Fourth-pass grade:** **100/100 — PROMISING** (3397 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 20/20, addressed requirements 20/20, unmet requirements 10/10, complete/pending 10/10, verification 15/15, limitation/failure 10/10, ledger structure 5/5, nonempty 10/10; weakest=ledger; field=reasoning.
**Fourth-pass improvement:** use a clearly labeled contract ledger with all requested fields.
## Skill: `jony-ive`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**Live Kilo grade:** **57/100 — MIXED** (3065 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 13/20, requirements 18/35, boundaries 4/20, verification 4/15, concrete 8/15; weakest=boundaries; response field=reasoning.
**How to improve:** state concrete invalid-input, refusal, uncertainty, edge-case, and failure behavior.
**Second-pass grade:** **60/100 — MIXED** (2931 response characters).
**Second-pass evidence:** Second-pass response evidence: task=20/20, assumptions=0/20, boundaries=10/20, verification=10/20, contract=10/10; weakest=assumptions; field=reasoning.
**Second-pass improvement:** always state assumptions explicitly, including what information is missing.
**Third-pass grade:** **100/100 — PROMISING** (3497 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 20/20, assumption 15/15, boundary/failure 15/15, verification 10/10, revision 10/10, nonempty 10/10; weakest=verification; field=reasoning.
**Third-pass improvement:** add a concrete verification step with an expected result, metric, or assertion.
**Fourth-pass grade:** **59/100 — MIXED** (3493 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 20/20, addressed requirements 6/20, unmet requirements 0/10, complete/pending 0/10, verification 8/15, limitation/failure 10/10, ledger structure 5/5, nonempty 10/10; weakest=unmet; field=reasoning.
**Fourth-pass improvement:** explicitly list every unmet requirement instead of implying full completion.
## Skill: `joy-buolamwini`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**Live Kilo grade:** **56/100 — MIXED** (2996 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 13/20, requirements 25/35, boundaries 2/20, verification 4/15, concrete 2/15; weakest=boundaries; response field=reasoning.
**How to improve:** state concrete invalid-input, refusal, uncertainty, edge-case, and failure behavior.
**Second-pass grade:** **30/100 — WEAK** (3178 response characters).
**Second-pass evidence:** Second-pass response evidence: task=0/20, assumptions=0/20, boundaries=0/20, verification=10/20, contract=10/10; weakest=task; field=reasoning.
**Second-pass improvement:** put the useful domain answer before persona framing and show a concrete output.
**Third-pass grade:** **35/100 — WEAK** (3462 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 0/20, assumption 0/15, boundary/failure 0/15, verification 5/10, revision 0/10, nonempty 10/10; weakest=requirements; field=reasoning.
**Third-pass improvement:** name which active-skill requirements were satisfied and which were missed, with evidence for each.
**Fourth-pass grade:** **69/100 — MIXED** (3485 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 20/20, addressed requirements 6/20, unmet requirements 0/10, complete/pending 10/10, verification 8/15, limitation/failure 10/10, ledger structure 5/5, nonempty 10/10; weakest=unmet; field=reasoning.
**Fourth-pass improvement:** explicitly list every unmet requirement instead of implying full completion.
## Skill: `julia-child`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**Live Kilo grade:** **68/100 — PROMISING** (2958 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 15/20, requirements 19/35, boundaries 10/20, verification 6/15, concrete 8/15; weakest=verification; response field=reasoning.
**How to improve:** add an explicit check, expected result, metric, or reviewable verification step.
**Second-pass grade:** **70/100 — PROMISING** (2977 response characters).
**Second-pass evidence:** Second-pass response evidence: task=0/20, assumptions=10/20, boundaries=20/20, verification=20/20, contract=10/10; weakest=task; field=reasoning.
**Second-pass improvement:** put the useful domain answer before persona framing and show a concrete output.
**Third-pass grade:** **65/100 — MIXED** (3290 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 0/20, assumption 0/15, boundary/failure 15/15, verification 10/10, revision 10/10, nonempty 10/10; weakest=requirements; field=reasoning.
**Third-pass improvement:** name which active-skill requirements were satisfied and which were missed, with evidence for each.
**Fourth-pass grade:** **60/100 — MIXED** (3548 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 20/20, addressed requirements 0/20, unmet requirements 0/10, complete/pending 0/10, verification 15/15, limitation/failure 10/10, ledger structure 5/5, nonempty 10/10; weakest=addressed; field=reasoning.
**Fourth-pass improvement:** name the active minimum requirements and map each to evidence in the result.
## Skill: `kamikaze`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=missing, cross_language=pass.
**Live Kilo grade:** **64/100 — PROMISING** (3113 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 15/20, requirements 25/35, boundaries 2/20, verification 6/15, concrete 6/15; weakest=boundaries; response field=reasoning.
**How to improve:** state concrete invalid-input, refusal, uncertainty, edge-case, and failure behavior.
**Second-pass grade:** **60/100 — MIXED** (2828 response characters).
**Second-pass evidence:** Second-pass response evidence: task=10/20, assumptions=0/20, boundaries=10/20, verification=20/20, contract=10/10; weakest=assumptions; field=reasoning.
**Second-pass improvement:** always state assumptions explicitly, including what information is missing.
**Third-pass grade:** **46/100 — MIXED** (3395 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 6/20, assumption 0/15, boundary/failure 0/15, verification 10/10, revision 0/10, nonempty 10/10; weakest=assumption; field=reasoning.
**Third-pass improvement:** state one specific unsafe or weak assumption and explain how the answer changes if it is false.
**Fourth-pass grade:** **60/100 — MIXED** (3376 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 20/20, addressed requirements 0/20, unmet requirements 0/10, complete/pending 5/10, verification 15/15, limitation/failure 5/10, ledger structure 5/5, nonempty 10/10; weakest=addressed; field=reasoning.
**Fourth-pass improvement:** name the active minimum requirements and map each to evidence in the result.
## Skill: `katherine-johnson`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**Live Kilo grade:** **51/100 — MIXED** (2701 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 15/20, requirements 16/35, boundaries 2/20, verification 6/15, concrete 2/15; weakest=boundaries; response field=reasoning.
**How to improve:** state concrete invalid-input, refusal, uncertainty, edge-case, and failure behavior.
**Second-pass grade:** **60/100 — MIXED** (2647 response characters).
**Second-pass evidence:** Second-pass response evidence: task=10/20, assumptions=0/20, boundaries=10/20, verification=20/20, contract=10/10; weakest=assumptions; field=reasoning.
**Second-pass improvement:** always state assumptions explicitly, including what information is missing.
**Third-pass grade:** **62/100 — MIXED** (3374 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 6/20, assumption 8/15, boundary/failure 8/15, verification 10/10, revision 0/10, nonempty 10/10; weakest=revision; field=reasoning.
**Third-pass improvement:** end with a clearly labeled revised answer that incorporates the critique.
**Fourth-pass grade:** **35/100 — WEAK** (2731 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 5/20, addressed requirements 0/20, unmet requirements 0/10, complete/pending 0/10, verification 15/15, limitation/failure 0/10, ledger structure 5/5, nonempty 10/10; weakest=addressed; field=reasoning.
**Fourth-pass improvement:** name the active minimum requirements and map each to evidence in the result.
## Skill: `kay`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**Live Kilo grade:** **46/100 — MIXED** (3113 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 13/20, requirements 19/35, boundaries 0/20, verification 0/15, concrete 4/15; weakest=boundaries; response field=reasoning.
**How to improve:** state concrete invalid-input, refusal, uncertainty, edge-case, and failure behavior.
**Second-pass grade:** **30/100 — WEAK** (3237 response characters).
**Second-pass evidence:** Second-pass response evidence: task=10/20, assumptions=0/20, boundaries=0/20, verification=0/20, contract=10/10; weakest=assumptions; field=reasoning.
**Second-pass improvement:** always state assumptions explicitly, including what information is missing.
**Third-pass grade:** **30/100 — WEAK** (3505 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 0/20, assumption 0/15, boundary/failure 0/15, verification 0/10, revision 0/10, nonempty 10/10; weakest=requirements; field=reasoning.
**Third-pass improvement:** name which active-skill requirements were satisfied and which were missed, with evidence for each.
**Fourth-pass grade:** **53/100 — MIXED** (3718 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 20/20, addressed requirements 0/20, unmet requirements 0/10, complete/pending 10/10, verification 8/15, limitation/failure 0/10, ledger structure 5/5, nonempty 10/10; weakest=addressed; field=reasoning.
**Fourth-pass improvement:** name the active minimum requirements and map each to evidence in the result.
## Skill: `ken-thompson`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**Live Kilo grade:** **66/100 — PROMISING** (3058 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 19/20, requirements 15/35, boundaries 8/20, verification 8/15, concrete 6/15; weakest=concrete; response field=reasoning.
**How to improve:** replace general advice with a concrete input/output example, procedure, or implementation sketch.
**Second-pass grade:** **60/100 — MIXED** (2902 response characters).
**Second-pass evidence:** Second-pass response evidence: task=10/20, assumptions=10/20, boundaries=20/20, verification=0/20, contract=10/10; weakest=verification; field=reasoning.
**Second-pass improvement:** include a check with an expected result or measurable pass criterion.
**Third-pass grade:** **55/100 — MIXED** (3265 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 0/20, assumption 0/15, boundary/failure 15/15, verification 10/10, revision 0/10, nonempty 10/10; weakest=requirements; field=reasoning.
**Third-pass improvement:** name which active-skill requirements were satisfied and which were missed, with evidence for each.
**Fourth-pass grade:** **54/100 — MIXED** (3334 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 20/20, addressed requirements 6/20, unmet requirements 0/10, complete/pending 5/10, verification 8/15, limitation/failure 0/10, ledger structure 5/5, nonempty 10/10; weakest=unmet; field=reasoning.
**Fourth-pass improvement:** explicitly list every unmet requirement instead of implying full completion.
## Skill: `knuth`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=missing, cross_language=pass.
**Live Kilo grade:** **49/100 — MIXED** (2701 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 13/20, requirements 14/35, boundaries 2/20, verification 2/15, concrete 8/15; weakest=boundaries; response field=reasoning.
**How to improve:** state concrete invalid-input, refusal, uncertainty, edge-case, and failure behavior.
**Second-pass grade:** **90/100 — PROMISING** (2788 response characters).
**Second-pass evidence:** Second-pass response evidence: task=20/20, assumptions=20/20, boundaries=10/20, verification=20/20, contract=10/10; weakest=boundaries; field=reasoning.
**Second-pass improvement:** name a likely failure and a concrete refusal, uncertainty, or limit condition.
**Third-pass grade:** **95/100 — PROMISING** (3455 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 20/20, assumption 15/15, boundary/failure 15/15, verification 10/10, revision 5/10, nonempty 10/10; weakest=revision; field=reasoning.
**Third-pass improvement:** end with a clearly labeled revised answer that incorporates the critique.
**Fourth-pass grade:** **100/100 — PROMISING** (3299 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 20/20, addressed requirements 20/20, unmet requirements 10/10, complete/pending 10/10, verification 15/15, limitation/failure 10/10, ledger structure 5/5, nonempty 10/10; weakest=ledger; field=reasoning.
**Fourth-pass improvement:** use a clearly labeled contract ledger with all requested fields.
## Skill: `lamport`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**Live Kilo grade:** **54/100 — MIXED** (3179 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 11/20, requirements 21/35, boundaries 6/20, verification 2/15, concrete 4/15; weakest=verification; response field=reasoning.
**How to improve:** add an explicit check, expected result, metric, or reviewable verification step.
**Second-pass grade:** **60/100 — MIXED** (2935 response characters).
**Second-pass evidence:** Second-pass response evidence: task=10/20, assumptions=20/20, boundaries=10/20, verification=0/20, contract=10/10; weakest=verification; field=reasoning.
**Second-pass improvement:** include a check with an expected result or measurable pass criterion.
**Third-pass grade:** **66/100 — MIXED** (3245 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 0/20, assumption 8/15, boundary/failure 8/15, verification 10/10, revision 10/10, nonempty 10/10; weakest=requirements; field=reasoning.
**Third-pass improvement:** name which active-skill requirements were satisfied and which were missed, with evidence for each.
**Fourth-pass grade:** **61/100 — MIXED** (3297 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 15/20, addressed requirements 6/20, unmet requirements 5/10, complete/pending 10/10, verification 0/15, limitation/failure 10/10, ledger structure 5/5, nonempty 10/10; weakest=verification; field=reasoning.
**Fourth-pass improvement:** give one runnable or checkable verification step with a precise expected result.
## Skill: `lattner`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**Live Kilo grade:** **62/100 — PROMISING** (2999 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 15/20, requirements 21/35, boundaries 4/20, verification 4/15, concrete 8/15; weakest=boundaries; response field=reasoning.
**How to improve:** state concrete invalid-input, refusal, uncertainty, edge-case, and failure behavior.
**Second-pass grade:** **60/100 — MIXED** (3082 response characters).
**Second-pass evidence:** Second-pass response evidence: task=20/20, assumptions=0/20, boundaries=10/20, verification=10/20, contract=10/10; weakest=assumptions; field=reasoning.
**Second-pass improvement:** always state assumptions explicitly, including what information is missing.
**Third-pass grade:** **79/100 — PROMISING** (3676 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 6/20, assumption 8/15, boundary/failure 15/15, verification 10/10, revision 10/10, nonempty 10/10; weakest=requirements; field=reasoning.
**Third-pass improvement:** name which active-skill requirements were satisfied and which were missed, with evidence for each.
**Fourth-pass grade:** **69/100 — MIXED** (3395 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 20/20, addressed requirements 6/20, unmet requirements 0/10, complete/pending 10/10, verification 8/15, limitation/failure 10/10, ledger structure 5/5, nonempty 10/10; weakest=unmet; field=reasoning.
**Fourth-pass improvement:** explicitly list every unmet requirement instead of implying full completion.
## Skill: `lazarus`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**Live Kilo grade:** **72/100 — PROMISING** (2955 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 13/20, requirements 22/35, boundaries 10/20, verification 6/15, concrete 11/15; weakest=verification; response field=reasoning.
**How to improve:** add an explicit check, expected result, metric, or reviewable verification step.
**Second-pass grade:** **60/100 — MIXED** (3031 response characters).
**Second-pass evidence:** Second-pass response evidence: task=20/20, assumptions=0/20, boundaries=0/20, verification=20/20, contract=10/10; weakest=assumptions; field=reasoning.
**Second-pass improvement:** always state assumptions explicitly, including what information is missing.
**Third-pass grade:** **49/100 — MIXED** (3272 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 14/20, assumption 0/15, boundary/failure 0/15, verification 5/10, revision 0/10, nonempty 10/10; weakest=assumption; field=reasoning.
**Third-pass improvement:** state one specific unsafe or weak assumption and explain how the answer changes if it is false.
**Fourth-pass grade:** **54/100 — MIXED** (3417 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 10/20, addressed requirements 6/20, unmet requirements 5/10, complete/pending 0/10, verification 8/15, limitation/failure 10/10, ledger structure 5/5, nonempty 10/10; weakest=pending; field=reasoning.
**Fourth-pass improvement:** separate completed work from pending work and state what remains to finish.
## Skill: `lisa-su`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**Live Kilo grade:** **65/100 — PROMISING** (3190 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 13/20, requirements 28/35, boundaries 6/20, verification 6/15, concrete 2/15; weakest=concrete; response field=reasoning.
**How to improve:** replace general advice with a concrete input/output example, procedure, or implementation sketch.
**Second-pass grade:** **40/100 — MIXED** (3221 response characters).
**Second-pass evidence:** Second-pass response evidence: task=0/20, assumptions=0/20, boundaries=10/20, verification=10/20, contract=10/10; weakest=task; field=reasoning.
**Second-pass improvement:** put the useful domain answer before persona framing and show a concrete output.
**Third-pass grade:** **80/100 — PROMISING** (3711 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 20/20, assumption 0/15, boundary/failure 15/15, verification 5/10, revision 10/10, nonempty 10/10; weakest=assumption; field=reasoning.
**Third-pass improvement:** state one specific unsafe or weak assumption and explain how the answer changes if it is false.
**Fourth-pass grade:** **100/100 — PROMISING** (3461 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 20/20, addressed requirements 20/20, unmet requirements 10/10, complete/pending 10/10, verification 15/15, limitation/failure 10/10, ledger structure 5/5, nonempty 10/10; weakest=ledger; field=reasoning.
**Fourth-pass improvement:** use a clearly labeled contract ledger with all requested fields.
## Skill: `louis-pasteur`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**Live Kilo grade:** **51/100 — MIXED** (3173 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 15/20, requirements 20/35, boundaries 0/20, verification 2/15, concrete 4/15; weakest=boundaries; response field=reasoning.
**How to improve:** state concrete invalid-input, refusal, uncertainty, edge-case, and failure behavior.
**Second-pass grade:** **50/100 — MIXED** (3283 response characters).
**Second-pass evidence:** Second-pass response evidence: task=0/20, assumptions=0/20, boundaries=10/20, verification=20/20, contract=10/10; weakest=task; field=reasoning.
**Second-pass improvement:** put the useful domain answer before persona framing and show a concrete output.
**Third-pass grade:** **45/100 — MIXED** (3472 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 0/20, assumption 0/15, boundary/failure 0/15, verification 10/10, revision 5/10, nonempty 10/10; weakest=requirements; field=reasoning.
**Third-pass improvement:** name which active-skill requirements were satisfied and which were missed, with evidence for each.
**Fourth-pass grade:** **46/100 — MIXED** (3359 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 10/20, addressed requirements 6/20, unmet requirements 0/10, complete/pending 0/10, verification 15/15, limitation/failure 0/10, ledger structure 5/5, nonempty 10/10; weakest=unmet; field=reasoning.
**Fourth-pass improvement:** explicitly list every unmet requirement instead of implying full completion.
## Skill: `lovelace`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**Live Kilo grade:** **64/100 — PROMISING** (2999 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 13/20, requirements 24/35, boundaries 0/20, verification 4/15, concrete 13/15; weakest=boundaries; response field=reasoning.
**How to improve:** state concrete invalid-input, refusal, uncertainty, edge-case, and failure behavior.
**Second-pass grade:** **50/100 — MIXED** (2744 response characters).
**Second-pass evidence:** Second-pass response evidence: task=20/20, assumptions=0/20, boundaries=0/20, verification=10/20, contract=10/10; weakest=assumptions; field=reasoning.
**Second-pass improvement:** always state assumptions explicitly, including what information is missing.
**Third-pass grade:** **35/100 — WEAK** (2759 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 0/20, assumption 0/15, boundary/failure 0/15, verification 5/10, revision 0/10, nonempty 10/10; weakest=requirements; field=reasoning.
**Third-pass improvement:** name which active-skill requirements were satisfied and which were missed, with evidence for each.
**Fourth-pass grade:** **93/100 — PROMISING** (3441 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 20/20, addressed requirements 20/20, unmet requirements 10/10, complete/pending 10/10, verification 8/15, limitation/failure 10/10, ledger structure 5/5, nonempty 10/10; weakest=ledger; field=reasoning.
**Fourth-pass improvement:** use a clearly labeled contract ledger with all requested fields.
## Skill: `lynch`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**Live Kilo grade:** **45/100 — MIXED** (2710 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 7/20, requirements 14/35, boundaries 2/20, verification 8/15, concrete 4/15; weakest=boundaries; response field=reasoning.
**How to improve:** state concrete invalid-input, refusal, uncertainty, edge-case, and failure behavior.
**Second-pass grade:** **60/100 — MIXED** (2602 response characters).
**Second-pass evidence:** Second-pass response evidence: task=0/20, assumptions=10/20, boundaries=10/20, verification=20/20, contract=10/10; weakest=task; field=reasoning.
**Second-pass improvement:** put the useful domain answer before persona framing and show a concrete output.
**Third-pass grade:** **58/100 — MIXED** (3087 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 0/20, assumption 0/15, boundary/failure 8/15, verification 10/10, revision 10/10, nonempty 10/10; weakest=requirements; field=reasoning.
**Third-pass improvement:** name which active-skill requirements were satisfied and which were missed, with evidence for each.
**Fourth-pass grade:** **75/100 — PROMISING** (3259 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 10/20, addressed requirements 20/20, unmet requirements 0/10, complete/pending 5/10, verification 15/15, limitation/failure 10/10, ledger structure 5/5, nonempty 10/10; weakest=unmet; field=reasoning.
**Fourth-pass improvement:** explicitly list every unmet requirement instead of implying full completion.
## Skill: `margaret-hamilton`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=missing, cross_language=pass.
**Live Kilo grade:** **61/100 — PROMISING** (2581 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 17/20, requirements 14/35, boundaries 6/20, verification 6/15, concrete 8/15; weakest=boundaries; response field=reasoning.
**How to improve:** state concrete invalid-input, refusal, uncertainty, edge-case, and failure behavior.
**Second-pass grade:** **60/100 — MIXED** (3193 response characters).
**Second-pass evidence:** Second-pass response evidence: task=20/20, assumptions=0/20, boundaries=10/20, verification=10/20, contract=10/10; weakest=assumptions; field=reasoning.
**Second-pass improvement:** always state assumptions explicitly, including what information is missing.
**Third-pass grade:** **93/100 — PROMISING** (3386 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 20/20, assumption 8/15, boundary/failure 15/15, verification 10/10, revision 10/10, nonempty 10/10; weakest=assumption; field=reasoning.
**Third-pass improvement:** state one specific unsafe or weak assumption and explain how the answer changes if it is false.
**Fourth-pass grade:** **69/100 — MIXED** (3338 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 20/20, addressed requirements 6/20, unmet requirements 0/10, complete/pending 10/10, verification 8/15, limitation/failure 10/10, ledger structure 5/5, nonempty 10/10; weakest=unmet; field=reasoning.
**Fourth-pass improvement:** explicitly list every unmet requirement instead of implying full completion.
## Skill: `marie-curie`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**Live Kilo grade:** **69/100 — PROMISING** (2711 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 15/20, requirements 24/35, boundaries 4/20, verification 8/15, concrete 8/15; weakest=boundaries; response field=reasoning.
**How to improve:** state concrete invalid-input, refusal, uncertainty, edge-case, and failure behavior.
**Second-pass grade:** **50/100 — MIXED** (3214 response characters).
**Second-pass evidence:** Second-pass response evidence: task=10/20, assumptions=0/20, boundaries=10/20, verification=10/20, contract=10/10; weakest=assumptions; field=reasoning.
**Second-pass improvement:** always state assumptions explicitly, including what information is missing.
**Third-pass grade:** **53/100 — MIXED** (3173 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 0/20, assumption 8/15, boundary/failure 0/15, verification 10/10, revision 5/10, nonempty 10/10; weakest=requirements; field=reasoning.
**Third-pass improvement:** name which active-skill requirements were satisfied and which were missed, with evidence for each.
**Fourth-pass grade:** **55/100 — MIXED** (2989 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 20/20, addressed requirements 0/20, unmet requirements 0/10, complete/pending 5/10, verification 15/15, limitation/failure 0/10, ledger structure 5/5, nonempty 10/10; weakest=addressed; field=reasoning.
**Fourth-pass improvement:** name the active minimum requirements and map each to evidence in the result.
## Skill: `marie-kondo`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=missing, cross_language=pass.
**Live Kilo grade:** **48/100 — MIXED** (2844 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 9/20, requirements 14/35, boundaries 0/20, verification 4/15, concrete 11/15; weakest=boundaries; response field=reasoning.
**How to improve:** state concrete invalid-input, refusal, uncertainty, edge-case, and failure behavior.
**Second-pass grade:** **40/100 — MIXED** (2977 response characters).
**Second-pass evidence:** Second-pass response evidence: task=10/20, assumptions=0/20, boundaries=0/20, verification=10/20, contract=10/10; weakest=assumptions; field=reasoning.
**Second-pass improvement:** always state assumptions explicitly, including what information is missing.
**Third-pass grade:** **49/100 — MIXED** (3493 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 14/20, assumption 0/15, boundary/failure 0/15, verification 5/10, revision 0/10, nonempty 10/10; weakest=assumption; field=reasoning.
**Third-pass improvement:** state one specific unsafe or weak assumption and explain how the answer changes if it is false.
**Fourth-pass grade:** **66/100 — MIXED** (3344 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 20/20, addressed requirements 6/20, unmet requirements 0/10, complete/pending 10/10, verification 15/15, limitation/failure 0/10, ledger structure 5/5, nonempty 10/10; weakest=unmet; field=reasoning.
**Fourth-pass improvement:** explicitly list every unmet requirement instead of implying full completion.
## Skill: `meta-senior-dev`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**Live Kilo grade:** **58/100 — MIXED** (2984 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 11/20, requirements 24/35, boundaries 0/20, verification 11/15, concrete 2/15; weakest=boundaries; response field=reasoning.
**How to improve:** state concrete invalid-input, refusal, uncertainty, edge-case, and failure behavior.
**Second-pass grade:** **40/100 — MIXED** (2861 response characters).
**Second-pass evidence:** Second-pass response evidence: task=10/20, assumptions=0/20, boundaries=0/20, verification=10/20, contract=10/10; weakest=assumptions; field=reasoning.
**Second-pass improvement:** always state assumptions explicitly, including what information is missing.
**Third-pass grade:** **54/100 — MIXED** (3267 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 6/20, assumption 8/15, boundary/failure 0/15, verification 10/10, revision 0/10, nonempty 10/10; weakest=boundary; field=reasoning.
**Third-pass improvement:** give one concrete failure, refusal, uncertainty, or edge-case condition and the safe response.
**Fourth-pass grade:** **59/100 — MIXED** (3257 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 20/20, addressed requirements 6/20, unmet requirements 0/10, complete/pending 0/10, verification 8/15, limitation/failure 10/10, ledger structure 5/5, nonempty 10/10; weakest=unmet; field=reasoning.
**Fourth-pass improvement:** explicitly list every unmet requirement instead of implying full completion.
## Skill: `military-general`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**Live Kilo grade:** **67/100 — PROMISING** (2940 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 13/20, requirements 30/35, boundaries 8/20, verification 2/15, concrete 4/15; weakest=verification; response field=reasoning.
**How to improve:** add an explicit check, expected result, metric, or reviewable verification step.
**Second-pass grade:** **60/100 — MIXED** (3139 response characters).
**Second-pass evidence:** Second-pass response evidence: task=10/20, assumptions=0/20, boundaries=20/20, verification=10/20, contract=10/10; weakest=assumptions; field=reasoning.
**Second-pass improvement:** always state assumptions explicitly, including what information is missing.
**Third-pass grade:** **74/100 — PROMISING** (2946 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 14/20, assumption 0/15, boundary/failure 15/15, verification 5/10, revision 10/10, nonempty 10/10; weakest=assumption; field=reasoning.
**Third-pass improvement:** state one specific unsafe or weak assumption and explain how the answer changes if it is false.
**Fourth-pass grade:** **100/100 — PROMISING** (3783 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 20/20, addressed requirements 20/20, unmet requirements 10/10, complete/pending 10/10, verification 15/15, limitation/failure 10/10, ledger structure 5/5, nonempty 10/10; weakest=ledger; field=reasoning.
**Fourth-pass improvement:** use a clearly labeled contract ledger with all requested fields.
## Skill: `miyamoto`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**Live Kilo grade:** **49/100 — MIXED** (2827 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 15/20, requirements 18/35, boundaries 2/20, verification 2/15, concrete 2/15; weakest=boundaries; response field=reasoning.
**How to improve:** state concrete invalid-input, refusal, uncertainty, edge-case, and failure behavior.
**Second-pass grade:** **50/100 — MIXED** (3031 response characters).
**Second-pass evidence:** Second-pass response evidence: task=10/20, assumptions=0/20, boundaries=10/20, verification=10/20, contract=10/10; weakest=assumptions; field=reasoning.
**Second-pass improvement:** always state assumptions explicitly, including what information is missing.
**Third-pass grade:** **65/100 — MIXED** (3270 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 0/20, assumption 0/15, boundary/failure 15/15, verification 10/10, revision 10/10, nonempty 10/10; weakest=requirements; field=reasoning.
**Third-pass improvement:** name which active-skill requirements were satisfied and which were missed, with evidence for each.
**Fourth-pass grade:** **68/100 — MIXED** (3455 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 20/20, addressed requirements 20/20, unmet requirements 5/10, complete/pending 0/10, verification 8/15, limitation/failure 0/10, ledger structure 5/5, nonempty 10/10; weakest=pending; field=reasoning.
**Fourth-pass improvement:** separate completed work from pending work and state what remains to finish.
## Skill: `munger`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**Live Kilo grade:** **61/100 — PROMISING** (3129 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 15/20, requirements 22/35, boundaries 8/20, verification 4/15, concrete 2/15; weakest=concrete; response field=reasoning.
**How to improve:** replace general advice with a concrete input/output example, procedure, or implementation sketch.
**Second-pass grade:** **40/100 — MIXED** (3188 response characters).
**Second-pass evidence:** Second-pass response evidence: task=0/20, assumptions=0/20, boundaries=10/20, verification=10/20, contract=10/10; weakest=task; field=reasoning.
**Second-pass improvement:** put the useful domain answer before persona framing and show a concrete output.
**Third-pass grade:** **60/100 — MIXED** (3451 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 0/20, assumption 0/15, boundary/failure 15/15, verification 5/10, revision 10/10, nonempty 10/10; weakest=requirements; field=reasoning.
**Third-pass improvement:** name which active-skill requirements were satisfied and which were missed, with evidence for each.
**Fourth-pass grade:** **69/100 — MIXED** (3466 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 20/20, addressed requirements 6/20, unmet requirements 5/10, complete/pending 5/10, verification 8/15, limitation/failure 10/10, ledger structure 5/5, nonempty 10/10; weakest=unmet; field=reasoning.
**Fourth-pass improvement:** explicitly list every unmet requirement instead of implying full completion.
## Skill: `musk`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**Live Kilo grade:** **42/100 — MIXED** (3035 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 13/20, requirements 13/35, boundaries 4/20, verification 0/15, concrete 2/15; weakest=verification; response field=reasoning.
**How to improve:** add an explicit check, expected result, metric, or reviewable verification step.
**Second-pass grade:** **80/100 — PROMISING** (3023 response characters).
**Second-pass evidence:** Second-pass response evidence: task=20/20, assumptions=10/20, boundaries=10/20, verification=20/20, contract=10/10; weakest=assumptions; field=reasoning.
**Second-pass improvement:** always state assumptions explicitly, including what information is missing.
**Third-pass grade:** **54/100 — MIXED** (3341 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 6/20, assumption 0/15, boundary/failure 8/15, verification 10/10, revision 0/10, nonempty 10/10; weakest=assumption; field=reasoning.
**Third-pass improvement:** state one specific unsafe or weak assumption and explain how the answer changes if it is false.
**Fourth-pass grade:** **49/100 — MIXED** (3309 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 20/20, addressed requirements 6/20, unmet requirements 0/10, complete/pending 0/10, verification 8/15, limitation/failure 5/10, ledger structure 0/5, nonempty 10/10; weakest=unmet; field=reasoning.
**Fourth-pass improvement:** explicitly list every unmet requirement instead of implying full completion.
## Skill: `nassim-taleb`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**Live Kilo grade:** **48/100 — MIXED** (2908 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 13/20, requirements 15/35, boundaries 4/20, verification 6/15, concrete 0/15; weakest=concrete; response field=reasoning.
**How to improve:** replace general advice with a concrete input/output example, procedure, or implementation sketch.
**Second-pass grade:** **50/100 — MIXED** (3067 response characters).
**Second-pass evidence:** Second-pass response evidence: task=10/20, assumptions=0/20, boundaries=10/20, verification=10/20, contract=10/10; weakest=assumptions; field=reasoning.
**Second-pass improvement:** always state assumptions explicitly, including what information is missing.
**Third-pass grade:** **62/100 — MIXED** (3624 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 14/20, assumption 0/15, boundary/failure 8/15, verification 10/10, revision 0/10, nonempty 10/10; weakest=assumption; field=reasoning.
**Third-pass improvement:** state one specific unsafe or weak assumption and explain how the answer changes if it is false.
**Fourth-pass grade:** **69/100 — MIXED** (3563 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 20/20, addressed requirements 6/20, unmet requirements 0/10, complete/pending 10/10, verification 8/15, limitation/failure 10/10, ledger structure 5/5, nonempty 10/10; weakest=unmet; field=reasoning.
**Fourth-pass improvement:** explicitly list every unmet requirement instead of implying full completion.
## Skill: `neckbeard`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=missing, cross_language=pass.
**Live Kilo grade:** **75/100 — PROMISING** (2761 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 17/20, requirements 28/35, boundaries 4/20, verification 8/15, concrete 8/15; weakest=boundaries; response field=reasoning.
**How to improve:** state concrete invalid-input, refusal, uncertainty, edge-case, and failure behavior.
**Second-pass grade:** **60/100 — MIXED** (2982 response characters).
**Second-pass evidence:** Second-pass response evidence: task=20/20, assumptions=0/20, boundaries=10/20, verification=10/20, contract=10/10; weakest=assumptions; field=reasoning.
**Second-pass improvement:** always state assumptions explicitly, including what information is missing.
**Third-pass grade:** **48/100 — MIXED** (3508 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 0/20, assumption 0/15, boundary/failure 8/15, verification 10/10, revision 0/10, nonempty 10/10; weakest=requirements; field=reasoning.
**Third-pass improvement:** name which active-skill requirements were satisfied and which were missed, with evidence for each.
**Fourth-pass grade:** **93/100 — PROMISING** (3536 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 20/20, addressed requirements 20/20, unmet requirements 10/10, complete/pending 10/10, verification 8/15, limitation/failure 10/10, ledger structure 5/5, nonempty 10/10; weakest=ledger; field=reasoning.
**Fourth-pass improvement:** use a clearly labeled contract ledger with all requested fields.
## Skill: `netflix-streaming`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=missing, cross_language=pass.
**Live Kilo grade:** **44/100 — MIXED** (2638 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 11/20, requirements 15/35, boundaries 2/20, verification 2/15, concrete 4/15; weakest=boundaries; response field=reasoning.
**How to improve:** state concrete invalid-input, refusal, uncertainty, edge-case, and failure behavior.
**Second-pass grade:** **70/100 — PROMISING** (2316 response characters).
**Second-pass evidence:** Second-pass response evidence: task=0/20, assumptions=10/20, boundaries=20/20, verification=20/20, contract=10/10; weakest=task; field=reasoning.
**Second-pass improvement:** put the useful domain answer before persona framing and show a concrete output.
**Third-pass grade:** **45/100 — MIXED** (3183 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 0/20, assumption 0/15, boundary/failure 0/15, verification 5/10, revision 10/10, nonempty 10/10; weakest=requirements; field=reasoning.
**Third-pass improvement:** name which active-skill requirements were satisfied and which were missed, with evidence for each.
**Fourth-pass grade:** **49/100 — MIXED** (3146 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 20/20, addressed requirements 6/20, unmet requirements 0/10, complete/pending 0/10, verification 8/15, limitation/failure 0/10, ledger structure 5/5, nonempty 10/10; weakest=unmet; field=reasoning.
**Fourth-pass improvement:** explicitly list every unmet requirement instead of implying full completion.
## Skill: `no-bullshit`

**Static signals:** frontmatter=pass, triggers=missing, boundaries=pass, requirements=pass, activation=pass, principles=missing, style=missing, cross_language=pass.
**Live Kilo grade:** **79/100 — PROMISING** (3204 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 19/20, requirements 18/35, boundaries 8/20, verification 13/15, concrete 11/15; weakest=boundaries; response field=reasoning.
**How to improve:** state concrete invalid-input, refusal, uncertainty, edge-case, and failure behavior.
**Second-pass grade:** **60/100 — MIXED** (2600 response characters).
**Second-pass evidence:** Second-pass response evidence: task=10/20, assumptions=0/20, boundaries=10/20, verification=20/20, contract=10/10; weakest=assumptions; field=reasoning.
**Second-pass improvement:** always state assumptions explicitly, including what information is missing.
**Third-pass grade:** **46/100 — MIXED** (3483 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 6/20, assumption 0/15, boundary/failure 0/15, verification 10/10, revision 0/10, nonempty 10/10; weakest=assumption; field=reasoning.
**Third-pass improvement:** state one specific unsafe or weak assumption and explain how the answer changes if it is false.
**Fourth-pass grade:** **85/100 — PROMISING** (3275 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 20/20, addressed requirements 20/20, unmet requirements 10/10, complete/pending 0/10, verification 15/15, limitation/failure 5/10, ledger structure 5/5, nonempty 10/10; weakest=pending; field=reasoning.
**Fourth-pass improvement:** separate completed work from pending work and state what remains to finish.
## Skill: `noir`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=missing, cross_language=pass.
**Live Kilo grade:** **58/100 — MIXED** (2750 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 9/20, requirements 18/35, boundaries 4/20, verification 9/15, concrete 8/15; weakest=boundaries; response field=reasoning.
**How to improve:** state concrete invalid-input, refusal, uncertainty, edge-case, and failure behavior.
**Second-pass grade:** **40/100 — MIXED** (2626 response characters).
**Second-pass evidence:** Second-pass response evidence: task=10/20, assumptions=0/20, boundaries=0/20, verification=10/20, contract=10/10; weakest=assumptions; field=reasoning.
**Second-pass improvement:** always state assumptions explicitly, including what information is missing.
**Third-pass grade:** **48/100 — MIXED** (3075 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 0/20, assumption 0/15, boundary/failure 8/15, verification 10/10, revision 0/10, nonempty 10/10; weakest=requirements; field=reasoning.
**Third-pass improvement:** name which active-skill requirements were satisfied and which were missed, with evidence for each.
**Fourth-pass grade:** **40/100 — MIXED** (2680 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 10/20, addressed requirements 0/20, unmet requirements 0/10, complete/pending 0/10, verification 15/15, limitation/failure 0/10, ledger structure 5/5, nonempty 10/10; weakest=addressed; field=reasoning.
**Fourth-pass improvement:** name the active minimum requirements and map each to evidence in the result.
## Skill: `oracle`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**Live Kilo grade:** **59/100 — MIXED** (2911 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 13/20, requirements 19/35, boundaries 4/20, verification 9/15, concrete 4/15; weakest=boundaries; response field=reasoning.
**How to improve:** state concrete invalid-input, refusal, uncertainty, edge-case, and failure behavior.
**Second-pass grade:** **70/100 — PROMISING** (2685 response characters).
**Second-pass evidence:** Second-pass response evidence: task=0/20, assumptions=10/20, boundaries=20/20, verification=20/20, contract=10/10; weakest=task; field=reasoning.
**Second-pass improvement:** put the useful domain answer before persona framing and show a concrete output.
**Third-pass grade:** **79/100 — PROMISING** (3114 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 14/20, assumption 0/15, boundary/failure 15/15, verification 10/10, revision 10/10, nonempty 10/10; weakest=assumption; field=reasoning.
**Third-pass improvement:** state one specific unsafe or weak assumption and explain how the answer changes if it is false.
**Fourth-pass grade:** **41/100 — MIXED** (2745 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 15/20, addressed requirements 6/20, unmet requirements 0/10, complete/pending 5/10, verification 0/15, limitation/failure 0/10, ledger structure 5/5, nonempty 10/10; weakest=unmet; field=reasoning.
**Fourth-pass improvement:** explicitly list every unmet requirement instead of implying full completion.
## Skill: `ouroboros`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**Live Kilo grade:** **60/100 — PROMISING** (3217 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 11/20, requirements 19/35, boundaries 4/20, verification 8/15, concrete 8/15; weakest=boundaries; response field=reasoning.
**How to improve:** state concrete invalid-input, refusal, uncertainty, edge-case, and failure behavior.
**Second-pass grade:** **50/100 — MIXED** (2831 response characters).
**Second-pass evidence:** Second-pass response evidence: task=10/20, assumptions=0/20, boundaries=10/20, verification=10/20, contract=10/10; weakest=assumptions; field=reasoning.
**Second-pass improvement:** always state assumptions explicitly, including what information is missing.
**Third-pass grade:** **55/100 — MIXED** (3673 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 0/20, assumption 0/15, boundary/failure 15/15, verification 10/10, revision 0/10, nonempty 10/10; weakest=requirements; field=reasoning.
**Third-pass improvement:** name which active-skill requirements were satisfied and which were missed, with evidence for each.
**Fourth-pass grade:** **60/100 — MIXED** (3553 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 20/20, addressed requirements 0/20, unmet requirements 0/10, complete/pending 0/10, verification 15/15, limitation/failure 10/10, ledger structure 5/5, nonempty 10/10; weakest=addressed; field=reasoning.
**Fourth-pass improvement:** name the active minimum requirements and map each to evidence in the result.
## Skill: `patterson`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**Live Kilo grade:** **39/100 — MIXED** (2756 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 11/20, requirements 10/35, boundaries 2/20, verification 2/15, concrete 4/15; weakest=boundaries; response field=reasoning.
**How to improve:** state concrete invalid-input, refusal, uncertainty, edge-case, and failure behavior.
**Second-pass grade:** **50/100 — MIXED** (2716 response characters).
**Second-pass evidence:** Second-pass response evidence: task=20/20, assumptions=0/20, boundaries=0/20, verification=10/20, contract=10/10; weakest=assumptions; field=reasoning.
**Second-pass improvement:** always state assumptions explicitly, including what information is missing.
**Third-pass grade:** **45/100 — MIXED** (2860 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 0/20, assumption 0/15, boundary/failure 0/15, verification 5/10, revision 10/10, nonempty 10/10; weakest=requirements; field=reasoning.
**Third-pass improvement:** name which active-skill requirements were satisfied and which were missed, with evidence for each.
**Fourth-pass grade:** **50/100 — MIXED** (2898 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 20/20, addressed requirements 0/20, unmet requirements 5/10, complete/pending 5/10, verification 0/15, limitation/failure 10/10, ledger structure 0/5, nonempty 10/10; weakest=addressed; field=reasoning.
**Fourth-pass improvement:** name the active minimum requirements and map each to evidence in the result.
## Skill: `paul-graham`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**Live Kilo grade:** **62/100 — PROMISING** (3125 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 17/20, requirements 23/35, boundaries 0/20, verification 6/15, concrete 6/15; weakest=boundaries; response field=reasoning.
**How to improve:** state concrete invalid-input, refusal, uncertainty, edge-case, and failure behavior.
**Second-pass grade:** **40/100 — MIXED** (3099 response characters).
**Second-pass evidence:** Second-pass response evidence: task=10/20, assumptions=0/20, boundaries=0/20, verification=10/20, contract=10/10; weakest=assumptions; field=reasoning.
**Second-pass improvement:** always state assumptions explicitly, including what information is missing.
**Third-pass grade:** **46/100 — MIXED** (3536 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 6/20, assumption 0/15, boundary/failure 0/15, verification 0/10, revision 10/10, nonempty 10/10; weakest=assumption; field=reasoning.
**Third-pass improvement:** state one specific unsafe or weak assumption and explain how the answer changes if it is false.
**Fourth-pass grade:** **78/100 — PROMISING** (3564 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 20/20, addressed requirements 20/20, unmet requirements 0/10, complete/pending 10/10, verification 8/15, limitation/failure 5/10, ledger structure 5/5, nonempty 10/10; weakest=unmet; field=reasoning.
**Fourth-pass improvement:** explicitly list every unmet requirement instead of implying full completion.
## Skill: `pepe-silvia`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=missing, cross_language=pass.
**Live Kilo grade:** **46/100 — MIXED** (2700 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 9/20, requirements 17/35, boundaries 0/20, verification 2/15, concrete 8/15; weakest=boundaries; response field=reasoning.
**How to improve:** state concrete invalid-input, refusal, uncertainty, edge-case, and failure behavior.
**Second-pass grade:** **50/100 — MIXED** (2623 response characters).
**Second-pass evidence:** Second-pass response evidence: task=20/20, assumptions=0/20, boundaries=0/20, verification=10/20, contract=10/10; weakest=assumptions; field=reasoning.
**Second-pass improvement:** always state assumptions explicitly, including what information is missing.
**Third-pass grade:** **40/100 — MIXED** (2699 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 0/20, assumption 0/15, boundary/failure 0/15, verification 10/10, revision 0/10, nonempty 10/10; weakest=requirements; field=reasoning.
**Third-pass improvement:** name which active-skill requirements were satisfied and which were missed, with evidence for each.
**Fourth-pass grade:** **38/100 — WEAK** (2932 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 20/20, addressed requirements 0/20, unmet requirements 0/10, complete/pending 0/10, verification 8/15, limitation/failure 0/10, ledger structure 0/5, nonempty 10/10; weakest=addressed; field=reasoning.
**Fourth-pass improvement:** name the active minimum requirements and map each to evidence in the result.
## Skill: `peter-parker`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**Live Kilo grade:** **66/100 — PROMISING** (2863 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 13/20, requirements 20/35, boundaries 6/20, verification 11/15, concrete 6/15; weakest=boundaries; response field=reasoning.
**How to improve:** state concrete invalid-input, refusal, uncertainty, edge-case, and failure behavior.
**Second-pass grade:** **70/100 — PROMISING** (3113 response characters).
**Second-pass evidence:** Second-pass response evidence: task=10/20, assumptions=0/20, boundaries=20/20, verification=20/20, contract=10/10; weakest=assumptions; field=reasoning.
**Second-pass improvement:** always state assumptions explicitly, including what information is missing.
**Third-pass grade:** **50/100 — MIXED** (3352 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 0/20, assumption 0/15, boundary/failure 0/15, verification 10/10, revision 10/10, nonempty 10/10; weakest=requirements; field=reasoning.
**Third-pass improvement:** name which active-skill requirements were satisfied and which were missed, with evidence for each.
**Fourth-pass grade:** **64/100 — MIXED** (2909 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 20/20, addressed requirements 6/20, unmet requirements 0/10, complete/pending 5/10, verification 8/15, limitation/failure 10/10, ledger structure 5/5, nonempty 10/10; weakest=unmet; field=reasoning.
**Fourth-pass improvement:** explicitly list every unmet requirement instead of implying full completion.
## Skill: `proof-carrying`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=missing, cross_language=pass.
**Live Kilo grade:** **64/100 — PROMISING** (2943 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 19/20, requirements 17/35, boundaries 2/20, verification 8/15, concrete 8/15; weakest=boundaries; response field=reasoning.
**How to improve:** state concrete invalid-input, refusal, uncertainty, edge-case, and failure behavior.
**Second-pass grade:** **90/100 — PROMISING** (3122 response characters).
**Second-pass evidence:** Second-pass response evidence: task=20/20, assumptions=20/20, boundaries=10/20, verification=20/20, contract=10/10; weakest=boundaries; field=reasoning.
**Second-pass improvement:** name a likely failure and a concrete refusal, uncertainty, or limit condition.
**Third-pass grade:** **48/100 — MIXED** (3386 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 0/20, assumption 8/15, boundary/failure 0/15, verification 10/10, revision 0/10, nonempty 10/10; weakest=requirements; field=reasoning.
**Third-pass improvement:** name which active-skill requirements were satisfied and which were missed, with evidence for each.
**Fourth-pass grade:** **35/100 — WEAK** (2832 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 10/20, addressed requirements 0/20, unmet requirements 0/10, complete/pending 0/10, verification 15/15, limitation/failure 0/10, ledger structure 0/5, nonempty 10/10; weakest=addressed; field=reasoning.
**Fourth-pass improvement:** name the active minimum requirements and map each to evidence in the result.
## Skill: `psych`

**Static signals:** frontmatter=pass, triggers=missing, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=missing, cross_language=pass.
**Live Kilo grade:** **54/100 — MIXED** (2912 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 11/20, requirements 23/35, boundaries 0/20, verification 6/15, concrete 4/15; weakest=boundaries; response field=reasoning.
**How to improve:** state concrete invalid-input, refusal, uncertainty, edge-case, and failure behavior.
**Second-pass grade:** **80/100 — PROMISING** (2967 response characters).
**Second-pass evidence:** Second-pass response evidence: task=10/20, assumptions=10/20, boundaries=20/20, verification=20/20, contract=10/10; weakest=task; field=reasoning.
**Second-pass improvement:** put the useful domain answer before persona framing and show a concrete output.
**Third-pass grade:** **60/100 — MIXED** (3505 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 20/20, assumption 0/15, boundary/failure 0/15, verification 10/10, revision 0/10, nonempty 10/10; weakest=assumption; field=reasoning.
**Third-pass improvement:** state one specific unsafe or weak assumption and explain how the answer changes if it is false.
**Fourth-pass grade:** **100/100 — PROMISING** (3358 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 20/20, addressed requirements 20/20, unmet requirements 10/10, complete/pending 10/10, verification 15/15, limitation/failure 10/10, ledger structure 5/5, nonempty 10/10; weakest=ledger; field=reasoning.
**Fourth-pass improvement:** use a clearly labeled contract ledger with all requested fields.
## Skill: `quant`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**Live Kilo grade:** **63/100 — PROMISING** (2943 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 13/20, requirements 22/35, boundaries 8/20, verification 6/15, concrete 4/15; weakest=concrete; response field=reasoning.
**How to improve:** replace general advice with a concrete input/output example, procedure, or implementation sketch.
**Second-pass grade:** **60/100 — MIXED** (2856 response characters).
**Second-pass evidence:** Second-pass response evidence: task=10/20, assumptions=10/20, boundaries=10/20, verification=10/20, contract=10/10; weakest=task; field=reasoning.
**Second-pass improvement:** put the useful domain answer before persona framing and show a concrete output.
**Third-pass grade:** **80/100 — PROMISING** (3144 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 14/20, assumption 8/15, boundary/failure 8/15, verification 10/10, revision 10/10, nonempty 10/10; weakest=assumption; field=reasoning.
**Third-pass improvement:** state one specific unsafe or weak assumption and explain how the answer changes if it is false.
**Fourth-pass grade:** **49/100 — MIXED** (3257 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 5/20, addressed requirements 6/20, unmet requirements 0/10, complete/pending 10/10, verification 8/15, limitation/failure 5/10, ledger structure 5/5, nonempty 10/10; weakest=unmet; field=reasoning.
**Fourth-pass improvement:** explicitly list every unmet requirement instead of implying full completion.
## Skill: `quantum-computing`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=missing, principles=missing, style=missing, cross_language=pass.
**Live Kilo grade:** **58/100 — MIXED** (2752 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 11/20, requirements 21/35, boundaries 2/20, verification 6/15, concrete 8/15; weakest=boundaries; response field=reasoning.
**How to improve:** state concrete invalid-input, refusal, uncertainty, edge-case, and failure behavior.
**Second-pass grade:** **80/100 — PROMISING** (2677 response characters).
**Second-pass evidence:** Second-pass response evidence: task=10/20, assumptions=10/20, boundaries=20/20, verification=20/20, contract=10/10; weakest=task; field=reasoning.
**Second-pass improvement:** put the useful domain answer before persona framing and show a concrete output.
**Third-pass grade:** **64/100 — MIXED** (3227 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 14/20, assumption 0/15, boundary/failure 0/15, verification 10/10, revision 10/10, nonempty 10/10; weakest=assumption; field=reasoning.
**Third-pass improvement:** state one specific unsafe or weak assumption and explain how the answer changes if it is false.
**Fourth-pass grade:** **73/100 — PROMISING** (3111 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 20/20, addressed requirements 20/20, unmet requirements 10/10, complete/pending 0/10, verification 8/15, limitation/failure 0/10, ledger structure 5/5, nonempty 10/10; weakest=pending; field=reasoning.
**Fourth-pass improvement:** separate completed work from pending work and state what remains to finish.
## Skill: `quiescent`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=missing, cross_language=pass.
**Live Kilo grade:** **63/100 — PROMISING** (3135 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 17/20, requirements 26/35, boundaries 4/20, verification 2/15, concrete 4/15; weakest=verification; response field=reasoning.
**How to improve:** add an explicit check, expected result, metric, or reviewable verification step.
**Second-pass grade:** **50/100 — MIXED** (2938 response characters).
**Second-pass evidence:** Second-pass response evidence: task=10/20, assumptions=0/20, boundaries=10/20, verification=10/20, contract=10/10; weakest=assumptions; field=reasoning.
**Second-pass improvement:** always state assumptions explicitly, including what information is missing.
**Third-pass grade:** **54/100 — MIXED** (3370 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 6/20, assumption 0/15, boundary/failure 8/15, verification 10/10, revision 0/10, nonempty 10/10; weakest=assumption; field=reasoning.
**Third-pass improvement:** state one specific unsafe or weak assumption and explain how the answer changes if it is false.
**Fourth-pass grade:** **76/100 — PROMISING** (3273 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 20/20, addressed requirements 6/20, unmet requirements 5/10, complete/pending 10/10, verification 15/15, limitation/failure 5/10, ledger structure 5/5, nonempty 10/10; weakest=unmet; field=reasoning.
**Fourth-pass improvement:** explicitly list every unmet requirement instead of implying full completion.
## Skill: `rachael-carson`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**Live Kilo grade:** **54/100 — MIXED** (3047 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 15/20, requirements 15/35, boundaries 4/20, verification 4/15, concrete 6/15; weakest=boundaries; response field=reasoning.
**How to improve:** state concrete invalid-input, refusal, uncertainty, edge-case, and failure behavior.
**Second-pass grade:** **50/100 — MIXED** (3387 response characters).
**Second-pass evidence:** Second-pass response evidence: task=10/20, assumptions=0/20, boundaries=10/20, verification=10/20, contract=10/10; weakest=assumptions; field=reasoning.
**Second-pass improvement:** always state assumptions explicitly, including what information is missing.
**Third-pass grade:** **78/100 — PROMISING** (3578 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 20/20, assumption 0/15, boundary/failure 8/15, verification 10/10, revision 10/10, nonempty 10/10; weakest=assumption; field=reasoning.
**Third-pass improvement:** state one specific unsafe or weak assumption and explain how the answer changes if it is false.
**Fourth-pass grade:** **58/100 — MIXED** (3412 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 15/20, addressed requirements 0/20, unmet requirements 0/10, complete/pending 10/10, verification 8/15, limitation/failure 10/10, ledger structure 5/5, nonempty 10/10; weakest=addressed; field=reasoning.
**Fourth-pass improvement:** name the active minimum requirements and map each to evidence in the result.
## Skill: `radia-perlman`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**Live Kilo grade:** **47/100 — MIXED** (2921 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 11/20, requirements 20/35, boundaries 0/20, verification 4/15, concrete 2/15; weakest=boundaries; response field=reasoning.
**How to improve:** state concrete invalid-input, refusal, uncertainty, edge-case, and failure behavior.
**Second-pass grade:** **40/100 — MIXED** (2901 response characters).
**Second-pass evidence:** Second-pass response evidence: task=10/20, assumptions=0/20, boundaries=0/20, verification=10/20, contract=10/10; weakest=assumptions; field=reasoning.
**Second-pass improvement:** always state assumptions explicitly, including what information is missing.
**Third-pass grade:** **40/100 — MIXED** (3368 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 0/20, assumption 0/15, boundary/failure 0/15, verification 10/10, revision 0/10, nonempty 10/10; weakest=requirements; field=reasoning.
**Third-pass improvement:** name which active-skill requirements were satisfied and which were missed, with evidence for each.
**Fourth-pass grade:** **48/100 — MIXED** (3285 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 20/20, addressed requirements 0/20, unmet requirements 0/10, complete/pending 0/10, verification 8/15, limitation/failure 5/10, ledger structure 5/5, nonempty 10/10; weakest=addressed; field=reasoning.
**Fourth-pass improvement:** name the active minimum requirements and map each to evidence in the result.
## Skill: `record-producer`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=missing, cross_language=pass.
**Live Kilo grade:** **45/100 — MIXED** (2830 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 13/20, requirements 18/35, boundaries 2/20, verification 2/15, concrete 0/15; weakest=concrete; response field=reasoning.
**How to improve:** replace general advice with a concrete input/output example, procedure, or implementation sketch.
**Second-pass grade:** **70/100 — PROMISING** (2792 response characters).
**Second-pass evidence:** Second-pass response evidence: task=0/20, assumptions=10/20, boundaries=20/20, verification=20/20, contract=10/10; weakest=task; field=reasoning.
**Second-pass improvement:** put the useful domain answer before persona framing and show a concrete output.
**Third-pass grade:** **28/100 — WEAK** (2893 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 10/20, requirement audit 0/20, assumption 0/15, boundary/failure 8/15, verification 0/10, revision 0/10, nonempty 10/10; weakest=requirements; field=reasoning.
**Third-pass improvement:** name which active-skill requirements were satisfied and which were missed, with evidence for each.
**Fourth-pass grade:** **64/100 — MIXED** (3268 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 20/20, addressed requirements 6/20, unmet requirements 0/10, complete/pending 5/10, verification 8/15, limitation/failure 10/10, ledger structure 5/5, nonempty 10/10; weakest=unmet; field=reasoning.
**Fourth-pass improvement:** explicitly list every unmet requirement instead of implying full completion.
## Skill: `red-team`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**Live Kilo grade:** **63/100 — PROMISING** (3107 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 17/20, requirements 15/35, boundaries 8/20, verification 4/15, concrete 9/15; weakest=verification; response field=reasoning.
**How to improve:** add an explicit check, expected result, metric, or reviewable verification step.
**Second-pass grade:** **100/100 — PROMISING** (3002 response characters).
**Second-pass evidence:** Second-pass response evidence: task=20/20, assumptions=20/20, boundaries=20/20, verification=20/20, contract=10/10; weakest=contract; field=reasoning.
**Second-pass improvement:** tie the response to at least one named minimum requirement instead of generic advice.
**Third-pass grade:** **100/100 — PROMISING** (3347 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 20/20, assumption 15/15, boundary/failure 15/15, verification 10/10, revision 10/10, nonempty 10/10; weakest=verification; field=reasoning.
**Third-pass improvement:** add a concrete verification step with an expected result, metric, or assertion.
**Fourth-pass grade:** **64/100 — MIXED** (3656 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 20/20, addressed requirements 6/20, unmet requirements 0/10, complete/pending 10/10, verification 8/15, limitation/failure 5/10, ledger structure 5/5, nonempty 10/10; weakest=unmet; field=reasoning.
**Fourth-pass improvement:** explicitly list every unmet requirement instead of implying full completion.
## Skill: `redacted`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=missing, cross_language=pass.
**Live Kilo grade:** **62/100 — PROMISING** (3143 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 17/20, requirements 20/35, boundaries 2/20, verification 2/15, concrete 11/15; weakest=boundaries; response field=reasoning.
**How to improve:** state concrete invalid-input, refusal, uncertainty, edge-case, and failure behavior.
**Second-pass grade:** **100/100 — PROMISING** (2971 response characters).
**Second-pass evidence:** Second-pass response evidence: task=20/20, assumptions=20/20, boundaries=20/20, verification=20/20, contract=10/10; weakest=contract; field=reasoning.
**Second-pass improvement:** tie the response to at least one named minimum requirement instead of generic advice.
**Third-pass grade:** **40/100 — MIXED** (3502 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 0/20, assumption 0/15, boundary/failure 0/15, verification 10/10, revision 0/10, nonempty 10/10; weakest=requirements; field=reasoning.
**Third-pass improvement:** name which active-skill requirements were satisfied and which were missed, with evidence for each.
**Fourth-pass grade:** **63/100 — MIXED** (3409 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 20/20, addressed requirements 20/20, unmet requirements 0/10, complete/pending 0/10, verification 8/15, limitation/failure 0/10, ledger structure 5/5, nonempty 10/10; weakest=unmet; field=reasoning.
**Fourth-pass improvement:** explicitly list every unmet requirement instead of implying full completion.
## Skill: `reid-hoffman`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**Live Kilo grade:** **54/100 — MIXED** (2898 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 13/20, requirements 21/35, boundaries 0/20, verification 6/15, concrete 4/15; weakest=boundaries; response field=reasoning.
**How to improve:** state concrete invalid-input, refusal, uncertainty, edge-case, and failure behavior.
**Second-pass grade:** **40/100 — MIXED** (3003 response characters).
**Second-pass evidence:** Second-pass response evidence: task=10/20, assumptions=0/20, boundaries=0/20, verification=10/20, contract=10/10; weakest=assumptions; field=reasoning.
**Second-pass improvement:** always state assumptions explicitly, including what information is missing.
**Third-pass grade:** **59/100 — MIXED** (3573 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 14/20, assumption 0/15, boundary/failure 0/15, verification 5/10, revision 10/10, nonempty 10/10; weakest=assumption; field=reasoning.
**Third-pass improvement:** state one specific unsafe or weak assumption and explain how the answer changes if it is false.
**Fourth-pass grade:** **54/100 — MIXED** (3447 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 20/20, addressed requirements 6/20, unmet requirements 0/10, complete/pending 10/10, verification 8/15, limitation/failure 0/10, ledger structure 0/5, nonempty 10/10; weakest=unmet; field=reasoning.
**Fourth-pass improvement:** explicitly list every unmet requirement instead of implying full completion.
## Skill: `rich-hickey`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**Live Kilo grade:** **53/100 — MIXED** (3341 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 11/20, requirements 22/35, boundaries 2/20, verification 0/15, concrete 8/15; weakest=verification; response field=reasoning.
**How to improve:** add an explicit check, expected result, metric, or reviewable verification step.
**Second-pass grade:** **90/100 — PROMISING** (3164 response characters).
**Second-pass evidence:** Second-pass response evidence: task=10/20, assumptions=20/20, boundaries=20/20, verification=20/20, contract=10/10; weakest=task; field=reasoning.
**Second-pass improvement:** put the useful domain answer before persona framing and show a concrete output.
**Third-pass grade:** **54/100 — MIXED** (3691 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 14/20, assumption 0/15, boundary/failure 0/15, verification 10/10, revision 0/10, nonempty 10/10; weakest=assumption; field=reasoning.
**Third-pass improvement:** state one specific unsafe or weak assumption and explain how the answer changes if it is false.
**Fourth-pass grade:** **50/100 — MIXED** (3724 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 20/20, addressed requirements 0/20, unmet requirements 0/10, complete/pending 10/10, verification 0/15, limitation/failure 10/10, ledger structure 0/5, nonempty 10/10; weakest=addressed; field=reasoning.
**Fourth-pass improvement:** name the active minimum requirements and map each to evidence in the result.
## Skill: `richard-stallman`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**Live Kilo grade:** **56/100 — MIXED** (3096 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 11/20, requirements 27/35, boundaries 2/20, verification 2/15, concrete 4/15; weakest=boundaries; response field=reasoning.
**How to improve:** state concrete invalid-input, refusal, uncertainty, edge-case, and failure behavior.
**Second-pass grade:** **80/100 — PROMISING** (3177 response characters).
**Second-pass evidence:** Second-pass response evidence: task=10/20, assumptions=10/20, boundaries=20/20, verification=20/20, contract=10/10; weakest=task; field=reasoning.
**Second-pass improvement:** put the useful domain answer before persona framing and show a concrete output.
**Third-pass grade:** **41/100 — MIXED** (3763 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 6/20, assumption 0/15, boundary/failure 0/15, verification 5/10, revision 0/10, nonempty 10/10; weakest=assumption; field=reasoning.
**Third-pass improvement:** state one specific unsafe or weak assumption and explain how the answer changes if it is false.
**Fourth-pass grade:** **94/100 — PROMISING** (3167 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 20/20, addressed requirements 14/20, unmet requirements 10/10, complete/pending 10/10, verification 15/15, limitation/failure 10/10, ledger structure 5/5, nonempty 10/10; weakest=ledger; field=reasoning.
**Fourth-pass improvement:** use a clearly labeled contract ledger with all requested fields.
## Skill: `rick-steves`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**Live Kilo grade:** **55/100 — MIXED** (3078 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 20/20, requirements 13/35, boundaries 0/20, verification 4/15, concrete 8/15; weakest=boundaries; response field=reasoning.
**How to improve:** state concrete invalid-input, refusal, uncertainty, edge-case, and failure behavior.
**Second-pass grade:** **80/100 — PROMISING** (2957 response characters).
**Second-pass evidence:** Second-pass response evidence: task=10/20, assumptions=10/20, boundaries=20/20, verification=20/20, contract=10/10; weakest=task; field=reasoning.
**Second-pass improvement:** put the useful domain answer before persona framing and show a concrete output.
**Third-pass grade:** **59/100 — MIXED** (3417 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 6/20, assumption 8/15, boundary/failure 0/15, verification 5/10, revision 10/10, nonempty 10/10; weakest=boundary; field=reasoning.
**Third-pass improvement:** give one concrete failure, refusal, uncertainty, or edge-case condition and the safe response.
**Fourth-pass grade:** **53/100 — MIXED** (3310 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 20/20, addressed requirements 0/20, unmet requirements 0/10, complete/pending 10/10, verification 8/15, limitation/failure 0/10, ledger structure 5/5, nonempty 10/10; weakest=addressed; field=reasoning.
**Fourth-pass improvement:** name the active minimum requirements and map each to evidence in the result.
## Skill: `robert-oppenheimer`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**Live Kilo grade:** **64/100 — PROMISING** (3334 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 19/20, requirements 21/35, boundaries 2/20, verification 8/15, concrete 4/15; weakest=boundaries; response field=reasoning.
**How to improve:** state concrete invalid-input, refusal, uncertainty, edge-case, and failure behavior.
**Second-pass grade:** **40/100 — MIXED** (3198 response characters).
**Second-pass evidence:** Second-pass response evidence: task=0/20, assumptions=0/20, boundaries=10/20, verification=10/20, contract=10/10; weakest=task; field=reasoning.
**Second-pass improvement:** put the useful domain answer before persona framing and show a concrete output.
**Third-pass grade:** **58/100 — MIXED** (3787 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 0/20, assumption 0/15, boundary/failure 8/15, verification 10/10, revision 10/10, nonempty 10/10; weakest=requirements; field=reasoning.
**Third-pass improvement:** name which active-skill requirements were satisfied and which were missed, with evidence for each.
**Fourth-pass grade:** **68/100 — MIXED** (3798 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 20/20, addressed requirements 20/20, unmet requirements 0/10, complete/pending 0/10, verification 8/15, limitation/failure 5/10, ledger structure 5/5, nonempty 10/10; weakest=unmet; field=reasoning.
**Fourth-pass improvement:** explicitly list every unmet requirement instead of implying full completion.
## Skill: `rorschach`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**Live Kilo grade:** **39/100 — MIXED** (2859 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 13/20, requirements 8/35, boundaries 2/20, verification 0/15, concrete 6/15; weakest=verification; response field=reasoning.
**How to improve:** add an explicit check, expected result, metric, or reviewable verification step.
**Second-pass grade:** **40/100 — MIXED** (2842 response characters).
**Second-pass evidence:** Second-pass response evidence: task=10/20, assumptions=0/20, boundaries=0/20, verification=10/20, contract=10/10; weakest=assumptions; field=reasoning.
**Second-pass improvement:** always state assumptions explicitly, including what information is missing.
**Third-pass grade:** **63/100 — MIXED** (3051 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 0/20, assumption 8/15, boundary/failure 15/15, verification 10/10, revision 0/10, nonempty 10/10; weakest=requirements; field=reasoning.
**Third-pass improvement:** name which active-skill requirements were satisfied and which were missed, with evidence for each.
**Fourth-pass grade:** **60/100 — MIXED** (3132 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 10/20, addressed requirements 0/20, unmet requirements 5/10, complete/pending 10/10, verification 15/15, limitation/failure 5/10, ledger structure 5/5, nonempty 10/10; weakest=addressed; field=reasoning.
**Fourth-pass improvement:** name the active minimum requirements and map each to evidence in the result.
## Skill: `satoru-iwata`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**Live Kilo grade:** **47/100 — MIXED** (3138 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 13/20, requirements 16/35, boundaries 2/20, verification 2/15, concrete 4/15; weakest=boundaries; response field=reasoning.
**How to improve:** state concrete invalid-input, refusal, uncertainty, edge-case, and failure behavior.
**Second-pass grade:** **50/100 — MIXED** (3260 response characters).
**Second-pass evidence:** Second-pass response evidence: task=10/20, assumptions=0/20, boundaries=10/20, verification=10/20, contract=10/10; weakest=assumptions; field=reasoning.
**Second-pass improvement:** always state assumptions explicitly, including what information is missing.
**Third-pass grade:** **60/100 — MIXED** (3622 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 0/20, assumption 0/15, boundary/failure 15/15, verification 10/10, revision 5/10, nonempty 10/10; weakest=requirements; field=reasoning.
**Third-pass improvement:** name which active-skill requirements were satisfied and which were missed, with evidence for each.
**Fourth-pass grade:** **35/100 — WEAK** (3554 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 20/20, addressed requirements 0/20, unmet requirements 0/10, complete/pending 0/10, verification 0/15, limitation/failure 0/10, ledger structure 5/5, nonempty 10/10; weakest=addressed; field=reasoning.
**Fourth-pass improvement:** name the active minimum requirements and map each to evidence in the result.
## Skill: `satoshi-nakamoto`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**Live Kilo grade:** **50/100 — MIXED** (3140 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 13/20, requirements 19/35, boundaries 0/20, verification 6/15, concrete 2/15; weakest=boundaries; response field=reasoning.
**How to improve:** state concrete invalid-input, refusal, uncertainty, edge-case, and failure behavior.
**Second-pass grade:** **50/100 — MIXED** (3233 response characters).
**Second-pass evidence:** Second-pass response evidence: task=10/20, assumptions=0/20, boundaries=0/20, verification=20/20, contract=10/10; weakest=assumptions; field=reasoning.
**Second-pass improvement:** always state assumptions explicitly, including what information is missing.
**Third-pass grade:** **59/100 — MIXED** (3775 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 6/20, assumption 0/15, boundary/failure 8/15, verification 10/10, revision 5/10, nonempty 10/10; weakest=assumption; field=reasoning.
**Third-pass improvement:** state one specific unsafe or weak assumption and explain how the answer changes if it is false.
**Fourth-pass grade:** **49/100 — MIXED** (3678 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 20/20, addressed requirements 6/20, unmet requirements 0/10, complete/pending 0/10, verification 8/15, limitation/failure 0/10, ledger structure 5/5, nonempty 10/10; weakest=unmet; field=reasoning.
**Fourth-pass improvement:** explicitly list every unmet requirement instead of implying full completion.
## Skill: `satya-nadella`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**Live Kilo grade:** **51/100 — MIXED** (3425 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 13/20, requirements 20/35, boundaries 4/20, verification 2/15, concrete 2/15; weakest=verification; response field=reasoning.
**How to improve:** add an explicit check, expected result, metric, or reviewable verification step.
**Second-pass grade:** **30/100 — WEAK** (3460 response characters).
**Second-pass evidence:** Second-pass response evidence: task=0/20, assumptions=0/20, boundaries=0/20, verification=10/20, contract=10/10; weakest=task; field=reasoning.
**Second-pass improvement:** put the useful domain answer before persona framing and show a concrete output.
**Third-pass grade:** **75/100 — PROMISING** (3674 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 20/20, assumption 0/15, boundary/failure 15/15, verification 10/10, revision 0/10, nonempty 10/10; weakest=assumption; field=reasoning.
**Third-pass improvement:** state one specific unsafe or weak assumption and explain how the answer changes if it is false.
**Fourth-pass grade:** **72/100 — PROMISING** (3590 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 20/20, addressed requirements 14/20, unmet requirements 10/10, complete/pending 0/10, verification 8/15, limitation/failure 5/10, ledger structure 5/5, nonempty 10/10; weakest=pending; field=reasoning.
**Fourth-pass improvement:** separate completed work from pending work and state what remains to finish.
## Skill: `schrodinger`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**Live Kilo grade:** **65/100 — PROMISING** (3041 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 19/20, requirements 22/35, boundaries 0/20, verification 6/15, concrete 8/15; weakest=boundaries; response field=reasoning.
**How to improve:** state concrete invalid-input, refusal, uncertainty, edge-case, and failure behavior.
**Second-pass grade:** **50/100 — MIXED** (2887 response characters).
**Second-pass evidence:** Second-pass response evidence: task=20/20, assumptions=0/20, boundaries=0/20, verification=10/20, contract=10/10; weakest=assumptions; field=reasoning.
**Second-pass improvement:** always state assumptions explicitly, including what information is missing.
**Third-pass grade:** **51/100 — MIXED** (3407 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 6/20, assumption 0/15, boundary/failure 15/15, verification 0/10, revision 0/10, nonempty 10/10; weakest=assumption; field=reasoning.
**Third-pass improvement:** state one specific unsafe or weak assumption and explain how the answer changes if it is false.
**Fourth-pass grade:** **50/100 — MIXED** (3012 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 20/20, addressed requirements 0/20, unmet requirements 0/10, complete/pending 5/10, verification 15/15, limitation/failure 0/10, ledger structure 0/5, nonempty 10/10; weakest=addressed; field=reasoning.
**Fourth-pass improvement:** name the active minimum requirements and map each to evidence in the result.
## Skill: `shannon`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**Live Kilo grade:** **68/100 — PROMISING** (3100 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 17/20, requirements 20/35, boundaries 6/20, verification 4/15, concrete 11/15; weakest=verification; response field=reasoning.
**How to improve:** add an explicit check, expected result, metric, or reviewable verification step.
**Second-pass grade:** **40/100 — MIXED** (2881 response characters).
**Second-pass evidence:** Second-pass response evidence: task=10/20, assumptions=0/20, boundaries=0/20, verification=10/20, contract=10/10; weakest=assumptions; field=reasoning.
**Second-pass improvement:** always state assumptions explicitly, including what information is missing.
**Third-pass grade:** **44/100 — MIXED** (2929 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 14/20, assumption 0/15, boundary/failure 0/15, verification 0/10, revision 0/10, nonempty 10/10; weakest=assumption; field=reasoning.
**Third-pass improvement:** state one specific unsafe or weak assumption and explain how the answer changes if it is false.
**Fourth-pass grade:** **54/100 — MIXED** (2361 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 20/20, addressed requirements 6/20, unmet requirements 0/10, complete/pending 0/10, verification 8/15, limitation/failure 5/10, ledger structure 5/5, nonempty 10/10; weakest=unmet; field=reasoning.
**Fourth-pass improvement:** explicitly list every unmet requirement instead of implying full completion.
## Skill: `sheryl-sandberg`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**Live Kilo grade:** **46/100 — MIXED** (2895 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 13/20, requirements 19/35, boundaries 2/20, verification 2/15, concrete 0/15; weakest=concrete; response field=reasoning.
**How to improve:** replace general advice with a concrete input/output example, procedure, or implementation sketch.
**Second-pass grade:** **40/100 — MIXED** (2945 response characters).
**Second-pass evidence:** Second-pass response evidence: task=10/20, assumptions=0/20, boundaries=0/20, verification=10/20, contract=10/10; weakest=assumptions; field=reasoning.
**Second-pass improvement:** always state assumptions explicitly, including what information is missing.
**Third-pass grade:** **56/100 — MIXED** (3324 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 6/20, assumption 0/15, boundary/failure 0/15, verification 10/10, revision 10/10, nonempty 10/10; weakest=assumption; field=reasoning.
**Third-pass improvement:** state one specific unsafe or weak assumption and explain how the answer changes if it is false.
**Fourth-pass grade:** **83/100 — PROMISING** (3601 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 20/20, addressed requirements 20/20, unmet requirements 0/10, complete/pending 10/10, verification 8/15, limitation/failure 10/10, ledger structure 5/5, nonempty 10/10; weakest=unmet; field=reasoning.
**Fourth-pass improvement:** explicitly list every unmet requirement instead of implying full completion.
## Skill: `sid-meier`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=missing, cross_language=pass.
**Live Kilo grade:** **52/100 — MIXED** (2891 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 17/20, requirements 17/35, boundaries 4/20, verification 4/15, concrete 0/15; weakest=concrete; response field=reasoning.
**How to improve:** replace general advice with a concrete input/output example, procedure, or implementation sketch.
**Second-pass grade:** **40/100 — MIXED** (3017 response characters).
**Second-pass evidence:** Second-pass response evidence: task=10/20, assumptions=0/20, boundaries=0/20, verification=10/20, contract=10/10; weakest=assumptions; field=reasoning.
**Second-pass improvement:** always state assumptions explicitly, including what information is missing.
**Third-pass grade:** **64/100 — MIXED** (3506 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 14/20, assumption 0/15, boundary/failure 0/15, verification 10/10, revision 10/10, nonempty 10/10; weakest=assumption; field=reasoning.
**Third-pass improvement:** state one specific unsafe or weak assumption and explain how the answer changes if it is false.
**Fourth-pass grade:** **49/100 — MIXED** (3298 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 20/20, addressed requirements 6/20, unmet requirements 0/10, complete/pending 0/10, verification 8/15, limitation/failure 0/10, ledger structure 5/5, nonempty 10/10; weakest=unmet; field=reasoning.
**Fourth-pass improvement:** explicitly list every unmet requirement instead of implying full completion.
## Skill: `simons`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=missing, cross_language=pass.
**Live Kilo grade:** **54/100 — MIXED** (2764 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 9/20, requirements 21/35, boundaries 2/20, verification 6/15, concrete 6/15; weakest=boundaries; response field=reasoning.
**How to improve:** state concrete invalid-input, refusal, uncertainty, edge-case, and failure behavior.
**Second-pass grade:** **50/100 — MIXED** (2534 response characters).
**Second-pass evidence:** Second-pass response evidence: task=10/20, assumptions=10/20, boundaries=0/20, verification=10/20, contract=10/10; weakest=boundaries; field=reasoning.
**Second-pass improvement:** name a likely failure and a concrete refusal, uncertainty, or limit condition.
**Third-pass grade:** **47/100 — MIXED** (3253 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 18/20, requirement audit 14/20, assumption 0/15, boundary/failure 0/15, verification 5/10, revision 0/10, nonempty 10/10; weakest=assumption; field=reasoning.
**Third-pass improvement:** state one specific unsafe or weak assumption and explain how the answer changes if it is false.
**Fourth-pass grade:** **39/100 — WEAK** (2946 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 10/20, addressed requirements 6/20, unmet requirements 0/10, complete/pending 0/10, verification 8/15, limitation/failure 0/10, ledger structure 5/5, nonempty 10/10; weakest=unmet; field=reasoning.
**Fourth-pass improvement:** explicitly list every unmet requirement instead of implying full completion.
## Skill: `smoker`

**Static signals:** frontmatter=pass, triggers=missing, boundaries=pass, requirements=pass, activation=pass, principles=missing, style=missing, cross_language=pass.
**Live Kilo grade:** **52/100 — MIXED** (2997 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 11/20, requirements 19/35, boundaries 2/20, verification 6/15, concrete 4/15; weakest=boundaries; response field=reasoning.
**How to improve:** state concrete invalid-input, refusal, uncertainty, edge-case, and failure behavior.
**Second-pass grade:** **50/100 — MIXED** (2900 response characters).
**Second-pass evidence:** Second-pass response evidence: task=10/20, assumptions=0/20, boundaries=10/20, verification=10/20, contract=10/10; weakest=assumptions; field=reasoning.
**Second-pass improvement:** always state assumptions explicitly, including what information is missing.
**Third-pass grade:** **61/100 — MIXED** (3308 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 6/20, assumption 0/15, boundary/failure 15/15, verification 10/10, revision 0/10, nonempty 10/10; weakest=assumption; field=reasoning.
**Third-pass improvement:** state one specific unsafe or weak assumption and explain how the answer changes if it is false.
**Fourth-pass grade:** **100/100 — PROMISING** (3386 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 20/20, addressed requirements 20/20, unmet requirements 10/10, complete/pending 10/10, verification 15/15, limitation/failure 10/10, ledger structure 5/5, nonempty 10/10; weakest=ledger; field=reasoning.
**Fourth-pass improvement:** use a clearly labeled contract ledger with all requested fields.
## Skill: `sonnet`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=missing, cross_language=pass.
**Live Kilo grade:** **55/100 — MIXED** (2530 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 15/20, requirements 17/35, boundaries 0/20, verification 2/15, concrete 11/15; weakest=boundaries; response field=reasoning.
**How to improve:** state concrete invalid-input, refusal, uncertainty, edge-case, and failure behavior.
**Second-pass grade:** **30/100 — WEAK** (2318 response characters).
**Second-pass evidence:** Second-pass response evidence: task=10/20, assumptions=0/20, boundaries=0/20, verification=0/20, contract=10/10; weakest=assumptions; field=reasoning.
**Second-pass improvement:** always state assumptions explicitly, including what information is missing.
**Third-pass grade:** **66/100 — MIXED** (2647 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 6/20, assumption 0/15, boundary/failure 15/15, verification 5/10, revision 10/10, nonempty 10/10; weakest=assumption; field=reasoning.
**Third-pass improvement:** state one specific unsafe or weak assumption and explain how the answer changes if it is false.
**Fourth-pass grade:** **38/100 — WEAK** (2181 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 15/20, addressed requirements 0/20, unmet requirements 5/10, complete/pending 0/10, verification 8/15, limitation/failure 0/10, ledger structure 0/5, nonempty 10/10; weakest=addressed; field=reasoning.
**Fourth-pass improvement:** name the active minimum requirements and map each to evidence in the result.
## Skill: `soros`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**Live Kilo grade:** **45/100 — MIXED** (3243 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 9/20, requirements 18/35, boundaries 0/20, verification 4/15, concrete 4/15; weakest=boundaries; response field=reasoning.
**How to improve:** state concrete invalid-input, refusal, uncertainty, edge-case, and failure behavior.
**Second-pass grade:** **40/100 — MIXED** (3107 response characters).
**Second-pass evidence:** Second-pass response evidence: task=0/20, assumptions=0/20, boundaries=10/20, verification=10/20, contract=10/10; weakest=task; field=reasoning.
**Second-pass improvement:** put the useful domain answer before persona framing and show a concrete output.
**Third-pass grade:** **66/100 — MIXED** (3351 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 15/20, requirement audit 6/20, assumption 0/15, boundary/failure 15/15, verification 10/10, revision 10/10, nonempty 10/10; weakest=assumption; field=reasoning.
**Third-pass improvement:** state one specific unsafe or weak assumption and explain how the answer changes if it is false.
**Fourth-pass grade:** **64/100 — MIXED** (3085 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 10/20, addressed requirements 6/20, unmet requirements 5/10, complete/pending 10/10, verification 8/15, limitation/failure 10/10, ledger structure 5/5, nonempty 10/10; weakest=unmet; field=reasoning.
**Fourth-pass improvement:** explicitly list every unmet requirement instead of implying full completion.
## Skill: `sovereign-citizen`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=missing, cross_language=pass.
**Live Kilo grade:** **56/100 — MIXED** (3055 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 13/20, requirements 21/35, boundaries 4/20, verification 4/15, concrete 4/15; weakest=boundaries; response field=reasoning.
**How to improve:** state concrete invalid-input, refusal, uncertainty, edge-case, and failure behavior.
**Second-pass grade:** **80/100 — PROMISING** (2800 response characters).
**Second-pass evidence:** Second-pass response evidence: task=20/20, assumptions=10/20, boundaries=10/20, verification=20/20, contract=10/10; weakest=assumptions; field=reasoning.
**Second-pass improvement:** always state assumptions explicitly, including what information is missing.
**Third-pass grade:** **83/100 — PROMISING** (3217 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 20/20, assumption 8/15, boundary/failure 15/15, verification 10/10, revision 0/10, nonempty 10/10; weakest=revision; field=reasoning.
**Third-pass improvement:** end with a clearly labeled revised answer that incorporates the critique.
**Fourth-pass grade:** **48/100 — MIXED** (3180 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 20/20, addressed requirements 0/20, unmet requirements 0/10, complete/pending 0/10, verification 8/15, limitation/failure 5/10, ledger structure 5/5, nonempty 10/10; weakest=addressed; field=reasoning.
**Fourth-pass improvement:** name the active minimum requirements and map each to evidence in the result.
## Skill: `spacex-fsw`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=missing, cross_language=pass.
**Live Kilo grade:** **79/100 — PROMISING** (3129 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 13/20, requirements 26/35, boundaries 6/20, verification 13/15, concrete 11/15; weakest=boundaries; response field=reasoning.
**How to improve:** state concrete invalid-input, refusal, uncertainty, edge-case, and failure behavior.
**Second-pass grade:** **60/100 — MIXED** (3159 response characters).
**Second-pass evidence:** Second-pass response evidence: task=20/20, assumptions=0/20, boundaries=10/20, verification=10/20, contract=10/10; weakest=assumptions; field=reasoning.
**Second-pass improvement:** always state assumptions explicitly, including what information is missing.
**Third-pass grade:** **51/100 — MIXED** (3593 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 6/20, assumption 0/15, boundary/failure 15/15, verification 0/10, revision 0/10, nonempty 10/10; weakest=assumption; field=reasoning.
**Third-pass improvement:** state one specific unsafe or weak assumption and explain how the answer changes if it is false.
**Fourth-pass grade:** **100/100 — PROMISING** (3322 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 20/20, addressed requirements 20/20, unmet requirements 10/10, complete/pending 10/10, verification 15/15, limitation/failure 10/10, ledger structure 5/5, nonempty 10/10; weakest=ledger; field=reasoning.
**Fourth-pass improvement:** use a clearly labeled contract ledger with all requested fields.
## Skill: `stewart-brand`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**Live Kilo grade:** **49/100 — MIXED** (3135 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 13/20, requirements 20/35, boundaries 0/20, verification 2/15, concrete 4/15; weakest=boundaries; response field=reasoning.
**How to improve:** state concrete invalid-input, refusal, uncertainty, edge-case, and failure behavior.
**Second-pass grade:** **50/100 — MIXED** (3251 response characters).
**Second-pass evidence:** Second-pass response evidence: task=10/20, assumptions=0/20, boundaries=10/20, verification=10/20, contract=10/10; weakest=assumptions; field=reasoning.
**Second-pass improvement:** always state assumptions explicitly, including what information is missing.
**Third-pass grade:** **40/100 — MIXED** (3825 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 0/20, assumption 0/15, boundary/failure 0/15, verification 0/10, revision 10/10, nonempty 10/10; weakest=requirements; field=reasoning.
**Third-pass improvement:** name which active-skill requirements were satisfied and which were missed, with evidence for each.
**Fourth-pass grade:** **43/100 — MIXED** (3260 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 20/20, addressed requirements 0/20, unmet requirements 0/10, complete/pending 0/10, verification 8/15, limitation/failure 0/10, ledger structure 5/5, nonempty 10/10; weakest=addressed; field=reasoning.
**Fourth-pass improvement:** name the active minimum requirements and map each to evidence in the result.
## Skill: `stroustrup`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**Live Kilo grade:** **55/100 — MIXED** (3164 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 11/20, requirements 20/35, boundaries 4/20, verification 4/15, concrete 6/15; weakest=boundaries; response field=reasoning.
**How to improve:** state concrete invalid-input, refusal, uncertainty, edge-case, and failure behavior.
**Second-pass grade:** **80/100 — PROMISING** (2958 response characters).
**Second-pass evidence:** Second-pass response evidence: task=10/20, assumptions=20/20, boundaries=10/20, verification=20/20, contract=10/10; weakest=task; field=reasoning.
**Second-pass improvement:** put the useful domain answer before persona framing and show a concrete output.
**Third-pass grade:** **51/100 — MIXED** (3628 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 6/20, assumption 0/15, boundary/failure 0/15, verification 5/10, revision 10/10, nonempty 10/10; weakest=assumption; field=reasoning.
**Third-pass improvement:** state one specific unsafe or weak assumption and explain how the answer changes if it is false.
**Fourth-pass grade:** **30/100 — WEAK** (3213 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 20/20, addressed requirements 0/20, unmet requirements 0/10, complete/pending 0/10, verification 0/15, limitation/failure 0/10, ledger structure 0/5, nonempty 10/10; weakest=addressed; field=reasoning.
**Fourth-pass improvement:** name the active minimum requirements and map each to evidence in the result.
## Skill: `sun-tzu`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**Live Kilo grade:** **57/100 — MIXED** (2978 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 15/20, requirements 16/35, boundaries 10/20, verification 4/15, concrete 2/15; weakest=concrete; response field=reasoning.
**How to improve:** replace general advice with a concrete input/output example, procedure, or implementation sketch.
**Second-pass grade:** **50/100 — MIXED** (3201 response characters).
**Second-pass evidence:** Second-pass response evidence: task=10/20, assumptions=0/20, boundaries=10/20, verification=10/20, contract=10/10; weakest=assumptions; field=reasoning.
**Second-pass improvement:** always state assumptions explicitly, including what information is missing.
**Third-pass grade:** **56/100 — MIXED** (3780 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 6/20, assumption 0/15, boundary/failure 15/15, verification 5/10, revision 0/10, nonempty 10/10; weakest=assumption; field=reasoning.
**Third-pass improvement:** state one specific unsafe or weak assumption and explain how the answer changes if it is false.
**Fourth-pass grade:** **58/100 — MIXED** (3841 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 20/20, addressed requirements 0/20, unmet requirements 0/10, complete/pending 10/10, verification 8/15, limitation/failure 10/10, ledger structure 0/5, nonempty 10/10; weakest=addressed; field=reasoning.
**Fourth-pass improvement:** name the active minimum requirements and map each to evidence in the result.
## Skill: `susan-kare`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**Live Kilo grade:** **43/100 — MIXED** (2722 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 11/20, requirements 16/35, boundaries 2/20, verification 2/15, concrete 2/15; weakest=boundaries; response field=reasoning.
**How to improve:** state concrete invalid-input, refusal, uncertainty, edge-case, and failure behavior.
**Second-pass grade:** **40/100 — MIXED** (2549 response characters).
**Second-pass evidence:** Second-pass response evidence: task=10/20, assumptions=0/20, boundaries=0/20, verification=10/20, contract=10/10; weakest=assumptions; field=reasoning.
**Second-pass improvement:** always state assumptions explicitly, including what information is missing.
**Third-pass grade:** **41/100 — MIXED** (3079 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 6/20, assumption 0/15, boundary/failure 0/15, verification 5/10, revision 0/10, nonempty 10/10; weakest=assumption; field=reasoning.
**Third-pass improvement:** state one specific unsafe or weak assumption and explain how the answer changes if it is false.
**Fourth-pass grade:** **49/100 — MIXED** (2639 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 15/20, addressed requirements 6/20, unmet requirements 0/10, complete/pending 5/10, verification 8/15, limitation/failure 0/10, ledger structure 5/5, nonempty 10/10; weakest=unmet; field=reasoning.
**Fourth-pass improvement:** explicitly list every unmet requirement instead of implying full completion.
## Skill: `sweeney`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=missing, cross_language=pass.
**Live Kilo grade:** **62/100 — PROMISING** (3021 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 13/20, requirements 31/35, boundaries 2/20, verification 2/15, concrete 4/15; weakest=boundaries; response field=reasoning.
**How to improve:** state concrete invalid-input, refusal, uncertainty, edge-case, and failure behavior.
**Second-pass grade:** **30/100 — WEAK** (3050 response characters).
**Second-pass evidence:** Second-pass response evidence: task=0/20, assumptions=0/20, boundaries=0/20, verification=10/20, contract=10/10; weakest=task; field=reasoning.
**Second-pass improvement:** put the useful domain answer before persona framing and show a concrete output.
**Third-pass grade:** **51/100 — MIXED** (3553 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 6/20, assumption 0/15, boundary/failure 0/15, verification 5/10, revision 10/10, nonempty 10/10; weakest=assumption; field=reasoning.
**Third-pass improvement:** state one specific unsafe or weak assumption and explain how the answer changes if it is false.
**Fourth-pass grade:** **49/100 — MIXED** (3218 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 20/20, addressed requirements 6/20, unmet requirements 0/10, complete/pending 0/10, verification 8/15, limitation/failure 0/10, ledger structure 5/5, nonempty 10/10; weakest=unmet; field=reasoning.
**Fourth-pass improvement:** explicitly list every unmet requirement instead of implying full completion.
## Skill: `terry-davis`

**Static signals:** frontmatter=pass, triggers=missing, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=missing, cross_language=pass.
**Live Kilo grade:** **53/100 — MIXED** (2854 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 11/20, requirements 22/35, boundaries 2/20, verification 0/15, concrete 8/15; weakest=verification; response field=reasoning.
**How to improve:** add an explicit check, expected result, metric, or reviewable verification step.
**Second-pass grade:** **40/100 — MIXED** (2815 response characters).
**Second-pass evidence:** Second-pass response evidence: task=10/20, assumptions=0/20, boundaries=0/20, verification=10/20, contract=10/10; weakest=assumptions; field=reasoning.
**Second-pass improvement:** always state assumptions explicitly, including what information is missing.
**Third-pass grade:** **46/100 — MIXED** (3330 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 6/20, assumption 0/15, boundary/failure 0/15, verification 10/10, revision 0/10, nonempty 10/10; weakest=assumption; field=reasoning.
**Third-pass improvement:** state one specific unsafe or weak assumption and explain how the answer changes if it is false.
**Fourth-pass grade:** **49/100 — MIXED** (2784 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 20/20, addressed requirements 6/20, unmet requirements 0/10, complete/pending 5/10, verification 8/15, limitation/failure 0/10, ledger structure 0/5, nonempty 10/10; weakest=unmet; field=reasoning.
**Fourth-pass improvement:** explicitly list every unmet requirement instead of implying full completion.
## Skill: `the-last-employee`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=missing, cross_language=pass.
**Live Kilo grade:** **57/100 — MIXED** (3258 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 11/20, requirements 28/35, boundaries 4/20, verification 2/15, concrete 2/15; weakest=verification; response field=reasoning.
**How to improve:** add an explicit check, expected result, metric, or reviewable verification step.
**Second-pass grade:** **30/100 — WEAK** (3000 response characters).
**Second-pass evidence:** Second-pass response evidence: task=10/20, assumptions=0/20, boundaries=0/20, verification=0/20, contract=10/10; weakest=assumptions; field=reasoning.
**Second-pass improvement:** always state assumptions explicitly, including what information is missing.
**Third-pass grade:** **54/100 — MIXED** (3708 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 6/20, assumption 0/15, boundary/failure 8/15, verification 10/10, revision 0/10, nonempty 10/10; weakest=assumption; field=reasoning.
**Third-pass improvement:** state one specific unsafe or weak assumption and explain how the answer changes if it is false.
**Fourth-pass grade:** **64/100 — MIXED** (3707 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 20/20, addressed requirements 6/20, unmet requirements 5/10, complete/pending 10/10, verification 8/15, limitation/failure 0/10, ledger structure 5/5, nonempty 10/10; weakest=limitation; field=reasoning.
**Fourth-pass improvement:** state a concrete failure, boundary, invalid-input, or uncertainty condition and the safe response.
## Skill: `thomas-edison`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**Live Kilo grade:** **48/100 — MIXED** (2928 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 11/20, requirements 15/35, boundaries 4/20, verification 4/15, concrete 4/15; weakest=boundaries; response field=reasoning.
**How to improve:** state concrete invalid-input, refusal, uncertainty, edge-case, and failure behavior.
**Second-pass grade:** **40/100 — MIXED** (2885 response characters).
**Second-pass evidence:** Second-pass response evidence: task=10/20, assumptions=0/20, boundaries=0/20, verification=10/20, contract=10/10; weakest=assumptions; field=reasoning.
**Second-pass improvement:** always state assumptions explicitly, including what information is missing.
**Third-pass grade:** **40/100 — MIXED** (3043 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 0/20, assumption 0/15, boundary/failure 0/15, verification 10/10, revision 0/10, nonempty 10/10; weakest=requirements; field=reasoning.
**Third-pass improvement:** name which active-skill requirements were satisfied and which were missed, with evidence for each.
**Fourth-pass grade:** **49/100 — MIXED** (3024 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 20/20, addressed requirements 6/20, unmet requirements 0/10, complete/pending 0/10, verification 8/15, limitation/failure 5/10, ledger structure 0/5, nonempty 10/10; weakest=unmet; field=reasoning.
**Fourth-pass improvement:** explicitly list every unmet requirement instead of implying full completion.
## Skill: `tim-cook`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**Live Kilo grade:** **49/100 — MIXED** (3009 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 15/20, requirements 18/35, boundaries 0/20, verification 2/15, concrete 4/15; weakest=boundaries; response field=reasoning.
**How to improve:** state concrete invalid-input, refusal, uncertainty, edge-case, and failure behavior.
**Second-pass grade:** **50/100 — MIXED** (3123 response characters).
**Second-pass evidence:** Second-pass response evidence: task=10/20, assumptions=0/20, boundaries=10/20, verification=10/20, contract=10/10; weakest=assumptions; field=reasoning.
**Second-pass improvement:** always state assumptions explicitly, including what information is missing.
**Third-pass grade:** **64/100 — MIXED** (3301 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 14/20, assumption 0/15, boundary/failure 15/15, verification 5/10, revision 0/10, nonempty 10/10; weakest=assumption; field=reasoning.
**Third-pass improvement:** state one specific unsafe or weak assumption and explain how the answer changes if it is false.
**Fourth-pass grade:** **59/100 — MIXED** (3505 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 20/20, addressed requirements 6/20, unmet requirements 0/10, complete/pending 0/10, verification 8/15, limitation/failure 10/10, ledger structure 5/5, nonempty 10/10; weakest=unmet; field=reasoning.
**Fourth-pass improvement:** explicitly list every unmet requirement instead of implying full completion.
## Skill: `torvalds`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**Live Kilo grade:** **45/100 — MIXED** (2875 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 11/20, requirements 14/35, boundaries 0/20, verification 2/15, concrete 8/15; weakest=boundaries; response field=reasoning.
**How to improve:** state concrete invalid-input, refusal, uncertainty, edge-case, and failure behavior.
**Second-pass grade:** **30/100 — WEAK** (2775 response characters).
**Second-pass evidence:** Second-pass response evidence: task=10/20, assumptions=0/20, boundaries=0/20, verification=0/20, contract=10/10; weakest=assumptions; field=reasoning.
**Second-pass improvement:** always state assumptions explicitly, including what information is missing.
**Third-pass grade:** **36/100 — WEAK** (3505 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 6/20, assumption 0/15, boundary/failure 0/15, verification 0/10, revision 0/10, nonempty 10/10; weakest=assumption; field=reasoning.
**Third-pass improvement:** state one specific unsafe or weak assumption and explain how the answer changes if it is false.
**Fourth-pass grade:** **38/100 — WEAK** (3348 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 20/20, addressed requirements 0/20, unmet requirements 0/10, complete/pending 0/10, verification 8/15, limitation/failure 0/10, ledger structure 0/5, nonempty 10/10; weakest=addressed; field=reasoning.
**Fourth-pass improvement:** name the active minimum requirements and map each to evidence in the result.
## Skill: `trial-by-combat`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=missing, cross_language=pass.
**Live Kilo grade:** **56/100 — MIXED** (2631 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 11/20, requirements 17/35, boundaries 8/20, verification 4/15, concrete 6/15; weakest=verification; response field=reasoning.
**How to improve:** add an explicit check, expected result, metric, or reviewable verification step.
**Second-pass grade:** **50/100 — MIXED** (2177 response characters).
**Second-pass evidence:** Second-pass response evidence: task=20/20, assumptions=0/20, boundaries=0/20, verification=10/20, contract=10/10; weakest=assumptions; field=reasoning.
**Second-pass improvement:** always state assumptions explicitly, including what information is missing.
**Third-pass grade:** **54/100 — MIXED** (2923 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 6/20, assumption 0/15, boundary/failure 8/15, verification 0/10, revision 10/10, nonempty 10/10; weakest=assumption; field=reasoning.
**Third-pass improvement:** state one specific unsafe or weak assumption and explain how the answer changes if it is false.
**Fourth-pass grade:** **61/100 — MIXED** (2911 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 20/20, addressed requirements 6/20, unmet requirements 0/10, complete/pending 0/10, verification 15/15, limitation/failure 10/10, ledger structure 0/5, nonempty 10/10; weakest=unmet; field=reasoning.
**Fourth-pass improvement:** explicitly list every unmet requirement instead of implying full completion.
## Skill: `tudor-jones`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**Live Kilo grade:** **47/100 — MIXED** (2600 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 11/20, requirements 20/35, boundaries 4/20, verification 0/15, concrete 2/15; weakest=verification; response field=reasoning.
**How to improve:** add an explicit check, expected result, metric, or reviewable verification step.
**Second-pass grade:** **40/100 — MIXED** (2373 response characters).
**Second-pass evidence:** Second-pass response evidence: task=0/20, assumptions=0/20, boundaries=10/20, verification=10/20, contract=10/10; weakest=task; field=reasoning.
**Second-pass improvement:** put the useful domain answer before persona framing and show a concrete output.
**Third-pass grade:** **71/100 — PROMISING** (2925 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 6/20, assumption 0/15, boundary/failure 15/15, verification 10/10, revision 10/10, nonempty 10/10; weakest=assumption; field=reasoning.
**Third-pass improvement:** state one specific unsafe or weak assumption and explain how the answer changes if it is false.
**Fourth-pass grade:** **63/100 — MIXED** (2997 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 10/20, addressed requirements 20/20, unmet requirements 0/10, complete/pending 0/10, verification 8/15, limitation/failure 10/10, ledger structure 5/5, nonempty 10/10; weakest=unmet; field=reasoning.
**Fourth-pass improvement:** explicitly list every unmet requirement instead of implying full completion.
## Skill: `turing`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**Live Kilo grade:** **42/100 — MIXED** (2573 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 11/20, requirements 13/35, boundaries 2/20, verification 0/15, concrete 6/15; weakest=verification; response field=reasoning.
**How to improve:** add an explicit check, expected result, metric, or reviewable verification step.
**Second-pass grade:** **50/100 — MIXED** (2977 response characters).
**Second-pass evidence:** Second-pass response evidence: task=10/20, assumptions=0/20, boundaries=0/20, verification=20/20, contract=10/10; weakest=assumptions; field=reasoning.
**Second-pass improvement:** always state assumptions explicitly, including what information is missing.
**Third-pass grade:** **55/100 — MIXED** (2995 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 0/20, assumption 0/15, boundary/failure 15/15, verification 10/10, revision 0/10, nonempty 10/10; weakest=requirements; field=reasoning.
**Third-pass improvement:** name which active-skill requirements were satisfied and which were missed, with evidence for each.
**Fourth-pass grade:** **41/100 — MIXED** (2803 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 20/20, addressed requirements 6/20, unmet requirements 0/10, complete/pending 0/10, verification 0/15, limitation/failure 0/10, ledger structure 5/5, nonempty 10/10; weakest=unmet; field=reasoning.
**Fourth-pass improvement:** explicitly list every unmet requirement instead of implying full completion.
## Skill: `unix`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**Live Kilo grade:** **59/100 — MIXED** (2871 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 13/20, requirements 22/35, boundaries 2/20, verification 6/15, concrete 6/15; weakest=boundaries; response field=reasoning.
**How to improve:** state concrete invalid-input, refusal, uncertainty, edge-case, and failure behavior.
**Second-pass grade:** **70/100 — PROMISING** (2736 response characters).
**Second-pass evidence:** Second-pass response evidence: task=20/20, assumptions=10/20, boundaries=10/20, verification=10/20, contract=10/10; weakest=assumptions; field=reasoning.
**Second-pass improvement:** always state assumptions explicitly, including what information is missing.
**Third-pass grade:** **30/100 — WEAK** (3021 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 0/20, assumption 0/15, boundary/failure 0/15, verification 0/10, revision 0/10, nonempty 10/10; weakest=requirements; field=reasoning.
**Third-pass improvement:** name which active-skill requirements were satisfied and which were missed, with evidence for each.
**Fourth-pass grade:** **59/100 — MIXED** (3085 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 20/20, addressed requirements 6/20, unmet requirements 0/10, complete/pending 0/10, verification 8/15, limitation/failure 10/10, ledger structure 5/5, nonempty 10/10; weakest=unmet; field=reasoning.
**Fourth-pass improvement:** explicitly list every unmet requirement instead of implying full completion.
## Skill: `valve-time`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**Live Kilo grade:** **52/100 — MIXED** (2901 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 17/20, requirements 15/35, boundaries 2/20, verification 4/15, concrete 4/15; weakest=boundaries; response field=reasoning.
**How to improve:** state concrete invalid-input, refusal, uncertainty, edge-case, and failure behavior.
**Second-pass grade:** **60/100 — MIXED** (3311 response characters).
**Second-pass evidence:** Second-pass response evidence: task=20/20, assumptions=0/20, boundaries=10/20, verification=10/20, contract=10/10; weakest=assumptions; field=reasoning.
**Second-pass improvement:** always state assumptions explicitly, including what information is missing.
**Third-pass grade:** **78/100 — PROMISING** (3584 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 20/20, assumption 0/15, boundary/failure 8/15, verification 10/10, revision 10/10, nonempty 10/10; weakest=assumption; field=reasoning.
**Third-pass improvement:** state one specific unsafe or weak assumption and explain how the answer changes if it is false.
**Fourth-pass grade:** **69/100 — MIXED** (3594 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 20/20, addressed requirements 6/20, unmet requirements 0/10, complete/pending 10/10, verification 8/15, limitation/failure 10/10, ledger structure 5/5, nonempty 10/10; weakest=unmet; field=reasoning.
**Fourth-pass improvement:** explicitly list every unmet requirement instead of implying full completion.
## Skill: `vampire`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=missing, cross_language=pass.
**Live Kilo grade:** **55/100 — MIXED** (3155 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 19/20, requirements 20/35, boundaries 0/20, verification 0/15, concrete 6/15; weakest=boundaries; response field=reasoning.
**How to improve:** state concrete invalid-input, refusal, uncertainty, edge-case, and failure behavior.
**Second-pass grade:** **40/100 — MIXED** (2996 response characters).
**Second-pass evidence:** Second-pass response evidence: task=20/20, assumptions=0/20, boundaries=0/20, verification=0/20, contract=10/10; weakest=assumptions; field=reasoning.
**Second-pass improvement:** always state assumptions explicitly, including what information is missing.
**Third-pass grade:** **30/100 — WEAK** (3570 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 0/20, assumption 0/15, boundary/failure 0/15, verification 0/10, revision 0/10, nonempty 10/10; weakest=requirements; field=reasoning.
**Third-pass improvement:** name which active-skill requirements were satisfied and which were missed, with evidence for each.
**Fourth-pass grade:** **46/100 — MIXED** (3637 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 20/20, addressed requirements 6/20, unmet requirements 0/10, complete/pending 5/10, verification 0/15, limitation/failure 5/10, ledger structure 0/5, nonempty 10/10; weakest=unmet; field=reasoning.
**Fourth-pass improvement:** explicitly list every unmet requirement instead of implying full completion.
## Skill: `van-rossum`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**Live Kilo grade:** **78/100 — PROMISING** (3003 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 20/20, requirements 19/35, boundaries 6/20, verification 8/15, concrete 15/15; weakest=boundaries; response field=reasoning.
**How to improve:** state concrete invalid-input, refusal, uncertainty, edge-case, and failure behavior.
**Second-pass grade:** **60/100 — MIXED** (3021 response characters).
**Second-pass evidence:** Second-pass response evidence: task=20/20, assumptions=0/20, boundaries=10/20, verification=10/20, contract=10/10; weakest=assumptions; field=reasoning.
**Second-pass improvement:** always state assumptions explicitly, including what information is missing.
**Third-pass grade:** **46/100 — MIXED** (3342 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 6/20, assumption 0/15, boundary/failure 0/15, verification 10/10, revision 0/10, nonempty 10/10; weakest=assumption; field=reasoning.
**Third-pass improvement:** state one specific unsafe or weak assumption and explain how the answer changes if it is false.
**Fourth-pass grade:** **54/100 — MIXED** (3288 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 20/20, addressed requirements 6/20, unmet requirements 0/10, complete/pending 0/10, verification 8/15, limitation/failure 10/10, ledger structure 0/5, nonempty 10/10; weakest=unmet; field=reasoning.
**Fourth-pass improvement:** explicitly list every unmet requirement instead of implying full completion.
## Skill: `vint-cerf`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**Live Kilo grade:** **44/100 — MIXED** (2693 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 9/20, requirements 13/35, boundaries 2/20, verification 4/15, concrete 6/15; weakest=boundaries; response field=reasoning.
**How to improve:** state concrete invalid-input, refusal, uncertainty, edge-case, and failure behavior.
**Second-pass grade:** **50/100 — MIXED** (3037 response characters).
**Second-pass evidence:** Second-pass response evidence: task=10/20, assumptions=10/20, boundaries=10/20, verification=0/20, contract=10/10; weakest=verification; field=reasoning.
**Second-pass improvement:** include a check with an expected result or measurable pass criterion.
**Third-pass grade:** **59/100 — MIXED** (3542 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 6/20, assumption 8/15, boundary/failure 0/15, verification 5/10, revision 10/10, nonempty 10/10; weakest=boundary; field=reasoning.
**Third-pass improvement:** give one concrete failure, refusal, uncertainty, or edge-case condition and the safe response.
**Fourth-pass grade:** **50/100 — MIXED** (3506 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 15/20, addressed requirements 0/20, unmet requirements 0/10, complete/pending 0/10, verification 15/15, limitation/failure 5/10, ledger structure 5/5, nonempty 10/10; weakest=addressed; field=reasoning.
**Fourth-pass improvement:** name the active minimum requirements and map each to evidence in the result.
## Skill: `vitalik`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**Live Kilo grade:** **60/100 — PROMISING** (3047 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 15/20, requirements 20/35, boundaries 6/20, verification 9/15, concrete 0/15; weakest=concrete; response field=reasoning.
**How to improve:** replace general advice with a concrete input/output example, procedure, or implementation sketch.
**Second-pass grade:** **60/100 — MIXED** (3018 response characters).
**Second-pass evidence:** Second-pass response evidence: task=10/20, assumptions=0/20, boundaries=10/20, verification=20/20, contract=10/10; weakest=assumptions; field=reasoning.
**Second-pass improvement:** always state assumptions explicitly, including what information is missing.
**Third-pass grade:** **65/100 — MIXED** (3788 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 0/20, assumption 0/15, boundary/failure 15/15, verification 10/10, revision 10/10, nonempty 10/10; weakest=requirements; field=reasoning.
**Third-pass improvement:** name which active-skill requirements were satisfied and which were missed, with evidence for each.
**Fourth-pass grade:** **59/100 — MIXED** (3463 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 20/20, addressed requirements 6/20, unmet requirements 0/10, complete/pending 0/10, verification 8/15, limitation/failure 10/10, ledger structure 5/5, nonempty 10/10; weakest=unmet; field=reasoning.
**Fourth-pass improvement:** explicitly list every unmet requirement instead of implying full completion.
## Skill: `walt-disney`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**Live Kilo grade:** **40/100 — MIXED** (3101 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 11/20, requirements 15/35, boundaries 2/20, verification 2/15, concrete 0/15; weakest=concrete; response field=reasoning.
**How to improve:** replace general advice with a concrete input/output example, procedure, or implementation sketch.
**Second-pass grade:** **40/100 — MIXED** (2999 response characters).
**Second-pass evidence:** Second-pass response evidence: task=10/20, assumptions=0/20, boundaries=10/20, verification=0/20, contract=10/10; weakest=assumptions; field=reasoning.
**Second-pass improvement:** always state assumptions explicitly, including what information is missing.
**Third-pass grade:** **45/100 — MIXED** (3469 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 0/20, assumption 0/15, boundary/failure 15/15, verification 0/10, revision 0/10, nonempty 10/10; weakest=requirements; field=reasoning.
**Third-pass improvement:** name which active-skill requirements were satisfied and which were missed, with evidence for each.
**Fourth-pass grade:** **93/100 — PROMISING** (3496 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 20/20, addressed requirements 20/20, unmet requirements 10/10, complete/pending 10/10, verification 8/15, limitation/failure 10/10, ledger structure 5/5, nonempty 10/10; weakest=ledger; field=reasoning.
**Fourth-pass improvement:** use a clearly labeled contract ledger with all requested fields.
## Skill: `walter-isaacson`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**Live Kilo grade:** **44/100 — MIXED** (2853 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 13/20, requirements 13/35, boundaries 2/20, verification 4/15, concrete 2/15; weakest=boundaries; response field=reasoning.
**How to improve:** state concrete invalid-input, refusal, uncertainty, edge-case, and failure behavior.
**Second-pass grade:** **80/100 — PROMISING** (3153 response characters).
**Second-pass evidence:** Second-pass response evidence: task=10/20, assumptions=20/20, boundaries=10/20, verification=20/20, contract=10/10; weakest=task; field=reasoning.
**Second-pass improvement:** put the useful domain answer before persona framing and show a concrete output.
**Third-pass grade:** **30/100 — WEAK** (3473 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 0/20, assumption 0/15, boundary/failure 0/15, verification 0/10, revision 0/10, nonempty 10/10; weakest=requirements; field=reasoning.
**Third-pass improvement:** name which active-skill requirements were satisfied and which were missed, with evidence for each.
**Fourth-pass grade:** **100/100 — PROMISING** (3734 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 20/20, addressed requirements 20/20, unmet requirements 10/10, complete/pending 10/10, verification 15/15, limitation/failure 10/10, ledger structure 5/5, nonempty 10/10; weakest=ledger; field=reasoning.
**Fourth-pass improvement:** use a clearly labeled contract ledger with all requested fields.
## Skill: `war-room`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**Live Kilo grade:** **32/100 — WEAK** (966 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`content`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 9/20, requirements 5/35, boundaries 2/20, verification 2/15, concrete 4/15; weakest=boundaries; response field=content.
**How to improve:** state concrete invalid-input, refusal, uncertainty, edge-case, and failure behavior.
**Second-pass grade:** **70/100 — PROMISING** (2977 response characters).
**Second-pass evidence:** Second-pass response evidence: task=0/20, assumptions=10/20, boundaries=20/20, verification=20/20, contract=10/10; weakest=task; field=reasoning.
**Second-pass improvement:** put the useful domain answer before persona framing and show a concrete output.
**Third-pass grade:** **39/100 — WEAK** (3228 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 10/20, requirement audit 6/20, assumption 0/15, boundary/failure 8/15, verification 5/10, revision 0/10, nonempty 10/10; weakest=assumption; field=reasoning.
**Third-pass improvement:** state one specific unsafe or weak assumption and explain how the answer changes if it is false.
**Fourth-pass grade:** **28/100 — WEAK** (624 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 5/20, addressed requirements 0/20, unmet requirements 0/10, complete/pending 0/10, verification 8/15, limitation/failure 5/10, ledger structure 0/5, nonempty 10/10; weakest=addressed; field=content.
**Fourth-pass improvement:** name the active minimum requirements and map each to evidence in the result.
## Skill: `werner-heisenberg`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**Live Kilo grade:** **61/100 — PROMISING** (3093 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 13/20, requirements 22/35, boundaries 6/20, verification 6/15, concrete 4/15; weakest=concrete; response field=reasoning.
**How to improve:** replace general advice with a concrete input/output example, procedure, or implementation sketch.
**Second-pass grade:** **60/100 — MIXED** (3387 response characters).
**Second-pass evidence:** Second-pass response evidence: task=10/20, assumptions=0/20, boundaries=20/20, verification=10/20, contract=10/10; weakest=assumptions; field=reasoning.
**Second-pass improvement:** always state assumptions explicitly, including what information is missing.
**Third-pass grade:** **51/100 — MIXED** (3686 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 6/20, assumption 0/15, boundary/failure 15/15, verification 0/10, revision 0/10, nonempty 10/10; weakest=assumption; field=reasoning.
**Third-pass improvement:** state one specific unsafe or weak assumption and explain how the answer changes if it is false.
**Fourth-pass grade:** **51/100 — MIXED** (2952 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 20/20, addressed requirements 6/20, unmet requirements 5/10, complete/pending 0/10, verification 0/15, limitation/failure 10/10, ledger structure 0/5, nonempty 10/10; weakest=pending; field=reasoning.
**Fourth-pass improvement:** separate completed work from pending work and state what remains to finish.
## Skill: `wozniak`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**Live Kilo grade:** **43/100 — MIXED** (2730 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 15/20, requirements 10/35, boundaries 0/20, verification 0/15, concrete 8/15; weakest=boundaries; response field=reasoning.
**How to improve:** state concrete invalid-input, refusal, uncertainty, edge-case, and failure behavior.
**Second-pass grade:** **30/100 — WEAK** (2579 response characters).
**Second-pass evidence:** Second-pass response evidence: task=10/20, assumptions=0/20, boundaries=0/20, verification=0/20, contract=10/10; weakest=assumptions; field=reasoning.
**Second-pass improvement:** always state assumptions explicitly, including what information is missing.
**Third-pass grade:** **40/100 — MIXED** (2846 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 0/20, assumption 0/15, boundary/failure 0/15, verification 0/10, revision 10/10, nonempty 10/10; weakest=requirements; field=reasoning.
**Third-pass improvement:** name which active-skill requirements were satisfied and which were missed, with evidence for each.
**Fourth-pass grade:** **45/100 — MIXED** (2962 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 20/20, addressed requirements 0/20, unmet requirements 0/10, complete/pending 0/10, verification 15/15, limitation/failure 0/10, ledger structure 0/5, nonempty 10/10; weakest=addressed; field=reasoning.
**Fourth-pass improvement:** name the active minimum requirements and map each to evidence in the result.
## Skill: `y2k`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=missing, cross_language=pass.
**Live Kilo grade:** **66/100 — PROMISING** (2736 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 13/20, requirements 27/35, boundaries 6/20, verification 6/15, concrete 4/15; weakest=concrete; response field=reasoning.
**How to improve:** replace general advice with a concrete input/output example, procedure, or implementation sketch.
**Second-pass grade:** **60/100 — MIXED** (2409 response characters).
**Second-pass evidence:** Second-pass response evidence: task=10/20, assumptions=0/20, boundaries=10/20, verification=20/20, contract=10/10; weakest=assumptions; field=reasoning.
**Second-pass improvement:** always state assumptions explicitly, including what information is missing.
**Third-pass grade:** **35/100 — WEAK** (2631 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 15/20, requirement audit 0/20, assumption 0/15, boundary/failure 0/15, verification 10/10, revision 0/10, nonempty 10/10; weakest=requirements; field=reasoning.
**Third-pass improvement:** name which active-skill requirements were satisfied and which were missed, with evidence for each.
**Fourth-pass grade:** **53/100 — MIXED** (2597 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 20/20, addressed requirements 0/20, unmet requirements 0/10, complete/pending 0/10, verification 8/15, limitation/failure 10/10, ledger structure 5/5, nonempty 10/10; weakest=addressed; field=reasoning.
**Fourth-pass improvement:** name the active minimum requirements and map each to evidence in the result.
## Skill: `yukihiro-matsumoto`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**Live Kilo grade:** **52/100 — MIXED** (2970 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 13/20, requirements 17/35, boundaries 4/20, verification 2/15, concrete 6/15; weakest=verification; response field=reasoning.
**How to improve:** add an explicit check, expected result, metric, or reviewable verification step.
**Second-pass grade:** **80/100 — PROMISING** (2906 response characters).
**Second-pass evidence:** Second-pass response evidence: task=10/20, assumptions=10/20, boundaries=20/20, verification=20/20, contract=10/10; weakest=task; field=reasoning.
**Second-pass improvement:** put the useful domain answer before persona framing and show a concrete output.
**Third-pass grade:** **35/100 — WEAK** (3213 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 0/20, assumption 0/15, boundary/failure 0/15, verification 5/10, revision 0/10, nonempty 10/10; weakest=requirements; field=reasoning.
**Third-pass improvement:** name which active-skill requirements were satisfied and which were missed, with evidence for each.
**Fourth-pass grade:** **48/100 — MIXED** (3336 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 20/20, addressed requirements 0/20, unmet requirements 0/10, complete/pending 0/10, verification 8/15, limitation/failure 5/10, ledger structure 5/5, nonempty 10/10; weakest=addressed; field=reasoning.
**Fourth-pass improvement:** name the active minimum requirements and map each to evidence in the result.
## Skill: `zero-copy`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**Live Kilo grade:** **57/100 — MIXED** (3175 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 15/20, requirements 21/35, boundaries 2/20, verification 0/15, concrete 9/15; weakest=verification; response field=reasoning.
**How to improve:** add an explicit check, expected result, metric, or reviewable verification step.
**Second-pass grade:** **80/100 — PROMISING** (2914 response characters).
**Second-pass evidence:** Second-pass response evidence: task=20/20, assumptions=10/20, boundaries=10/20, verification=20/20, contract=10/10; weakest=assumptions; field=reasoning.
**Second-pass improvement:** always state assumptions explicitly, including what information is missing.
**Third-pass grade:** **36/100 — WEAK** (3463 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 6/20, assumption 0/15, boundary/failure 0/15, verification 0/10, revision 0/10, nonempty 10/10; weakest=assumption; field=reasoning.
**Third-pass improvement:** state one specific unsafe or weak assumption and explain how the answer changes if it is false.
**Fourth-pass grade:** **55/100 — MIXED** (3067 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 20/20, addressed requirements 0/20, unmet requirements 0/10, complete/pending 5/10, verification 15/15, limitation/failure 0/10, ledger structure 5/5, nonempty 10/10; weakest=addressed; field=reasoning.
**Fourth-pass improvement:** name the active minimum requirements and map each to evidence in the result.
## Skill: `zuck`

**Static signals:** frontmatter=pass, triggers=pass, boundaries=pass, requirements=pass, activation=pass, principles=pass, style=pass, cross_language=pass.
**Second-pass grade:** **40/100 — MIXED** (2816 response characters).
**Second-pass evidence:** Second-pass response evidence: task=10/20, assumptions=0/20, boundaries=0/20, verification=10/20, contract=10/10; weakest=assumptions; field=reasoning.
**Second-pass improvement:** always state assumptions explicitly, including what information is missing.
**Third-pass grade:** **56/100 — MIXED** (3317 response characters).
**Third-pass evidence:** Self-critique response evidence: answer 20/20, requirement audit 6/20, assumption 0/15, boundary/failure 0/15, verification 10/10, revision 10/10, nonempty 10/10; weakest=assumption; field=reasoning.
**Third-pass improvement:** state one specific unsafe or weak assumption and explain how the answer changes if it is false.
**Fourth-pass grade:** **48/100 — MIXED** (3226 response characters).
**Fourth-pass evidence:** Contract-first response evidence: answer 15/20, addressed requirements 0/20, unmet requirements 0/10, complete/pending 10/10, verification 8/15, limitation/failure 0/10, ledger structure 5/5, nonempty 10/10; weakest=addressed; field=reasoning.
**Fourth-pass improvement:** name the active minimum requirements and map each to evidence in the result.
## Recommended next experiment

1. Revoke and rotate the credentials that were pasted into chat; keep replacement keys outside the repository.
2. Choose 3–5 models that are confirmed available and run at one request every 2–5 seconds per model.
3. Use skill-specific gold tasks derived from each skill’s own minimum requirements instead of one generic task for all personas.
4. Have a separate judge model or deterministic evaluator score the full response against those gold requirements.
5. Require at least 3 successful responses per skill before publishing a live quality score.

## Limitations

- This report uses a lexical heuristic and does not claim human semantic evaluation.
- The matrix had uneven coverage because free endpoints rate-limited heavily.
- No response bodies are included in this report; temporary raw outputs were kept outside the repository for grading only.
- Existing repository changes were preserved and were not created by this evaluation.
**Live Kilo grade:** **54/100 — MIXED** (3048 response characters)
**Models observed:** `kilo-auto/free` via Kilo; response field=`reasoning`.
**Kilo evidence:** Kilo response inspected by deterministic rubric: task 13/20, requirements 21/35, boundaries 0/20, verification 6/15, concrete 4/15; weakest=boundaries; response field=reasoning.
**How to improve:** state concrete invalid-input, refusal, uncertainty, edge-case, and failure behavior.
## Kilo grading summary

Graded **140** previously unjudged skills from actual Kilo response text using the transparent deterministic rubric above.

| Label | Count |
|---|---:|
| PROMISING | 47 |
| MIXED | 90 |
| WEAK | 3 |

Mean score: **55.4/100** · median: **55.0/100**.
These are machine-assisted rubric grades based on returned text, not human semantic judgments. The earlier eight manual sample grades remain separately labeled.

**Second-pass grade:** **40/100 — MIXED** (2816 response characters).
**Second-pass evidence:** Second-pass response evidence: task=10/20, assumptions=0/20, boundaries=0/20, verification=10/20, contract=10/10; weakest=assumptions; field=reasoning.
**Second-pass improvement:** always state assumptions explicitly, including what information is missing.
## Second-pass robustness summary

Completed a second robustness experiment for **180/180** skills using actual Kilo response text. Each task demanded useful output, assumptions, a failure/boundary condition, and a verification check.

| Label | Count |
|---|---:|
| PROMISING | 42 |
| MIXED | 121 |
| WEAK | 17 |

Mean score: **54.0/100** · median: **50.0/100**.
Marker presence rates: task 80.0%, assumptions 30.0%, boundaries 61.1%, verification 90.6%, contract 100.0%.
Scores are deterministic text-based triage, not human semantic judgments.

## Third-pass self-critique summary

This pass asked every skill to produce a useful domain answer, audit satisfied and missed requirements, identify an unsafe or weak assumption, name a failure/boundary condition, give a verification step, and end with a revised answer. Responses were sent sequentially through Kilo `kilo-auto/free`; five timed-out/empty assignments were retried once and all five then returned usable text.

- **Coverage:** 180/180 skills with usable response text; duplicate retry rows were deduplicated by skill.
- **Grades:** 25 PROMISING, 132 MIXED, 23 WEAK.
- **Mean / median:** 55.0 / 54.0.
- **Marker rates:** concrete answer 100.0%; requirement audit 60.0%; assumptions 16.7%; boundary/failure 52.2%; verification 80.6%; revised answer 41.1%.

### Interpretation

The strongest recurring signal is that the model can often produce a long answer and name a verification step when explicitly asked. The weakest recurring signals are explicit requirement auditing, specific assumptions, and clearly separated revised answers. Improve skills by making those artifacts part of their minimum response contract rather than relying on the model to infer them. Scores are deterministic lexical triage, not human-quality judgments; a high score means the requested artifacts were visibly present, not that the domain advice is correct.

## Fourth-pass contract-first summary

This pass required each skill to complete a concrete domain task before producing a contract ledger covering addressed requirements, unmet requirements, complete versus pending status, verification with an expected result, and a limitation or failure case. Responses were run sequentially through Kilo `kilo-auto/free`; checkpoint files covered all 180 skills.

- **Coverage:** 180/180 skills with usable response text.
- **Grades:** 41 PROMISING, 117 MIXED, 22 WEAK.
- **Mean / median:** 59.4 / 55.0.
- **Marker rates:** concrete answer 100.0%; addressed requirements 68.3%; unmet requirements 26.7%; complete/pending 51.7%; verification/expected result 82.2%; limitation/failure 64.4%; ledger structure 77.8%.

### Interpretation

This pass measures whether requested contract artifacts were visibly present, not whether the domain advice was correct. Lexical markers can be incidental, so these are triage grades rather than human semantic judgments. The most useful improvement targets are the dimensions with the lowest marker rates: explicitly name unmet requirements, distinguish completed from pending work, and attach an expected result to every verification check.
