# Real-Model Routing Eval — skills 2 (180 persona skills)

Date: 2026-08-08
Harness: `model_router_eval.py` (+ `run_arm.sh`)
Prompt suite: 56 curated prompts drawn from `benchmark_prompts.SUITE`
(8 finance personas, 8 tech personas, 8 coding-forms, 7 safety/verification,
8 CS greats, 8 odd/creative, 9 shorthand repeats)

## Methodology

For each prompt the model receives ONLY the catalog (skill folder name +
frontmatter description, exactly what an agent skill-loader sees at trigger
time) and must answer `{"id": "<skill>"}` or `{"id": "NONE"}`. hit@1 = gold
skill chosen. Keys are passed via env at runtime and never committed.

## Results

| Model | Provider | n | hit@1 (raw) | Format-compliant accuracy | Notes |
|---|---|---|---|---|---|
| deepseek-ai/deepseek-v4-flash-0731 | NVIDIA | 56 | **100%** | 100% | only model with 0 format misses |
| nvidia/nemotron-3-super-120b-a12b | NVIDIA | 56 | 71% | ~97% | 16 format misses (prose / literal `<skill-folder-name>`); 1 real routing error (huang) now fixed |
| mistral-small-latest | Mistral | 56 | 30% | **94%** | 38 format misses; 1 real error (boiler-room -> boiler-room-research) now fixed |
| stepfun-ai/step-3.7-flash | NVIDIA | 8 | — | 100% on completed | API too slow/timeouts on free tier; abandoned mid-run |
| deepseek/deepseek-chat-v3-0324 | OpenRouter | 56 | 5% | — | mostly unparseable reasoning output; parsed samples show overlap confusion (fixed) |
| meta-llama/llama-3.3-70b-instruct | OpenRouter | 56 | 11% | — | prose writer; not format-compliant |
| llama-3.3-70b-versatile | Groq | 6 | 0% | — | prose writer; not format-compliant |

## Key findings

1. **The catalog routes correctly for format-compliant models.** deepseek-v4
   scores 100% with zero misses; nemotron and mistral score ~94-97% once their
   prose responses are excluded. The low raw scores are instruction-following
   quirks of individual models, NOT description quality.

2. **Two genuine description overlaps were found and fixed:**
   - `huang` vs `apple-platform` — both described "hardware/software
     co-design" with cache/memory vocabulary; nemotron routed the huang prompt
     to apple-platform. Fixed: huang now states it is the Jensen Huang/NVIDIA
     compute persona (GPUs, CUDA kernels, memory bandwidth, accelerators) and
     gained "CUDA kernel"/"memory bandwidth"/"accelerator"/"throughput"
     triggers. **Verified: huang prompt now routes to huang on nemotron.**
   - `boiler-room` vs `boiler-room-research` — both triggered on "boiler
     room"; two models routed the Jordan Belfort prompt to boiler-room-research.
     Fixed: boiler-room description now covers fast Belfort-style stock pitches
     ("find out what stocks", "pitch me stocks") and gained those triggers.

3. **Buzzword experiment (research -> analyst):** the audit found no prompt
   where a persona skill was missed because a user buzzword ("analyst",
   "investigate", "research") differed from description vocabulary. The
   descriptions already contain the working vocabulary; the two overlap fixes
   above were the only real routing failures.

## Regression checks after edits

- `python3 benchmark_prompts.py` -> hit@1 100%, hit@3 100%, adversarial 100%,
  never-fired none (unchanged, no regressions).
- Targeted 6-prompt re-run: deepseek-v4 6/6; nemotron huang prompt now HIT.
- `run_ci.sh` -> all 9 gates green.

## Reproduce

    KEY=... python3 model_router_eval.py \
        --model nvidia/nemotron-3-super-120b-a12b \
        --base-url https://integrate.api.nvidia.com/v1 \
        --out results/nemotron.json

Raw per-prompt decisions: `results/*.json`.
