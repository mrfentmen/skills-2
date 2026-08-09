#!/usr/bin/env python3
"""Output-compliance eval for constraint-heavy persona skills (skills 2/).

For each skill in SCOPE the harness sends the FULL SKILL.md content as the
system prompt plus a one-sentence task, asks for Python code only, executes
it, and runs a per-skill structural grader that checks the skill's own
"Minimum Requirements (checkable)".

Failures reveal skill wording that models cannot comply with -> the input for
skill improvements. Code samples are saved to results/output/<skill>.py.

Usage:
  KEY=... python3 output_eval.py [--model deepseek-ai/deepseek-v4-flash-0731] \\
      [--base-url https://integrate.api.nvidia.com/v1] [--skills goldfish,sonnet]
"""

import argparse
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from model_router_eval import make_ssl_context  # noqa: E402

SCOPE = [
    "goldfish", "sonnet", "vampire", "hoarder", "insomniac",
    "trial-by-combat", "counterpoint", "casino", "dead-reckoning", "doppelganger",
    "black-box", "blind", "lazarus", "delta", "schrodinger",
    "quiescent", "zero-copy", "proof-carrying", "redacted", "ouroboros",
    "floor-trader", "funeral", "y2k", "quantum-computing", "fibonacci",
    "spacex-fsw", "vitalik", "sovereign-citizen", "rorschach", "psych",
    "margaret-hamilton", "unix", "neckbeard", "blood-magic", "janitor",
    "carmack-mode", "huang", "pepe-silvia", "terry-davis", "satoshi-nakamoto",
    "shannon", "turing", "patterson", "desert-island", "jane-street",
    "sweeney", "vint-cerf", "oracle", "no-bullshit", "smoker",
    "barbara-liskov", "dijkstra", "knuth", "lamport", "brian-kernighan",
    "dennis-ritchie", "john-tukey", "edward-tufte", "feynman", "george-polya",
    "anders-hejlsberg", "emmy-noether", "daniel-kahneman", "geoffrey-hinton", "barbara-mcclintock",
    "charles-darwin", "carl-sagan", "frank-lloyd-wright", "buckminster-fuller", "fred-rogers",
    "katherine-johnson", "john-von-neumann", "jeff-dean", "demis-hassabis", "fei-fei-li",
    "grace-hopper", "ken-thompson", "isaac-newton", "jane-goodall", "jennifer-doudna",
    "louis-pasteur", "marie-curie", "rachael-carson", "radia-perlman", "frances-allen",
    "joy-buolamwini", "werner-heisenberg", "wozniak", "jony-ive", "susan-kare",
    "lattner", "stroustrup", "rich-hickey", "van-rossum", "torvalds",
    "kay", "miyamoto", "sid-meier", "satoru-iwata", "simons",
    "buffett", "burry", "dalio", "howard-marks", "munger", "tudor-jones",
    "soros", "lynch", "icahn", "druckenmiller",
]

TASKS = {
    "goldfish": "Sum the integers 1..100 and print the result.",
    "sonnet": "Print the first 10 prime numbers.",
    "vampire": "Drain a list in place until it is empty and print each value.",
    "hoarder": "Process a list of numbers, never deleting or overwriting anything, and print the full history.",
    "insomniac": "Poll two jobs until both are ready, without ever blocking or sleeping.",
    "trial-by-combat": "Two different sorting implementations fight; a deterministic rule picks the winner.",
    "counterpoint": "Interleave two different step machines until both finish, neither observing the other's result early.",
    "casino": "Estimate pi by random sampling and print a confidence interval.",
    "dead-reckoning": "Find the maximum of a stream in one left-to-right pass with bounded memory.",
    "doppelganger": "Two different implementations of the same computation; compare them at runtime and print any disagreement.",
    "black-box": "Find a hidden number in [0,100] using ONLY yes/no questions through a fixed query interface; never inspect the hidden value directly.",
    "blind": "Solve a hidden value's parity using only a closed set of named questions and primitive answers.",
    "lazarus": "Compute a rolling sum, checkpoint it, destroy the live state, then rebuild from the checkpoint and verify the result.",
    "delta": "Represent inserting an item into a list as a delta, and apply it to a base without mutating the caller's base.",
    "schrodinger": "Compute the first 5 even squares lazily; include a counter or trace proving the work was deferred until forced.",
    "quiescent": "Drain a small job queue to a quiet point, then atomically swap the active config under a lock.",
    "zero-copy": "Pass a buffer through two transforms reporting who owns it before, during, and after each hand-off.",
    "proof-carrying": "Return a result with a small certificate, and verify the certificate independently without rerunning the computation.",
    "redacted": "Compute a result using a sensitive intermediate value, then clear it before output; never print the secret.",
    "ouroboros": "Write a quine: a program that prints exactly its own source text.",
    "floor-trader": "Process a stream of numbers in one left-to-right pass, printing an immediate irreversible decision per item with the rule that produced it; no rewind or lookahead.",
    "funeral": "Implement a resource that can be consumed exactly once; a second consume or any use of the invalidated handle must fail visibly.",
    "y2k": "Parse fixed-width date records with a documented two-digit-year window and correct Gregorian leap-year handling; make truncation and overflow explicit.",
    "quantum-computing": "Simulate a single qubit with complex amplitudes, apply at least one quantum gate, and demonstrate superposition.",
    "fibonacci": "Compute the 10th Fibonacci number with the convention stated, using visible 1, 1, 2, 3, 5, 8, 13 structure; derive the result, never hardcode it.",
    "spacex-fsw": "Run three independent computations of the same value and reconcile them by deterministic majority; exercise at least three synthetic fault scenarios.",
    "vitalik": "Build an append-only ledger whose state transitions are verified independently without replaying all work, with metered resource costs.",
    "sovereign-citizen": "Reimplement one standard-library operation with a written operator allowlist, rejecting unsupported inputs, and check the result against the host operation.",
    "rorschach": "Parse the same input under at least two genuinely different interpretations, validate each with a round-trip check, and return all survivors side by side.",
    "psych": "Print a visual fractal or recursive structure with a psychedelic comment; every line must run and do real work.",
    "margaret-hamilton": "Write a parse function with an explicit input contract (type, range, boundary checks), distinct handling for malformed input vs unexpected state, and a safe fallback or explicit unavailable result; test valid, boundary, and malformed inputs and print the outcomes.",
    "unix": "Write a small program with one stated responsibility that reads plain lines from stdin and writes plain lines to stdout, proving composition; print the processed result.",
    "neckbeard": "Implement a word counter with zero third-party dependencies, at least two cynical comments about tooling or process, input validation with an explicit error path, and a stated time/memory complexity note; print the result.",
    "blood-magic": "Manage a disposable resource with a dry-run default and an explicit armed mode; sacrifice (release) it before the main algorithm, verify after the sacrifice, and complete a real task, printing what was sacrificed.",
    "janitor": "Manage a resource lifecycle: acquire it, register cleanup immediately, make cleanup idempotent, and demonstrate cleanup on success, failure, and early exit, printing each outcome.",
    "carmack-mode": "Measure a small computation first, optimize exactly one thing justified by that measurement, and print the before/after numbers.",
    "huang": "Write a throughput-oriented computation (batched, pipelined, or vectorized) that names its bottleneck and uses hardware-friendly contiguous data layout, with a stated measurement or justification; print the result.",
    "pepe-silvia": "Transform a string through at least two harmless standard-library transformations plus one bounded bitwise operation, name the magic-number constants, expose an evidence ledger of intermediate values, and check the result against a plain reference; print the result.",
    "terry-davis": "Print a result using at least 2 cosmic or divine variable names, at least 1 religious or devotional comment, and at least 1 unconventional pattern (deep recursion, eval, goto-style, or odd structure).",
    "satoshi-nakamoto": "Build a minimal hash-chained append-only ledger with no central party: tampering must be detectable, conflicts resolved by an objective rule, and honest behavior the rational choice; print a verification result.",
    "shannon": "Compute the entropy of a small message, choose a redundancy decision (strip it via compression or add it via error correction), recover from a flipped bit over a noisy channel, and print the entropy and the decision.",
    "turing": "Implement a small state machine with explicit states and transitions, and make it interpret a tiny instruction string as code-as-data; print the trace and a decidability note.",
    "patterson": "Measure a small computation to find its bottleneck with data, state the Amdahl fraction the change touches, optimize only the common case, and print before/after numbers.",
    "desert-island": "Write a program that declares its dependency manifest, uses only the standard library, reads a local file safely with a temporary-artifact policy, and prints the result without network or absolute paths.",
    "jane-street": "Model a small money/order domain with distinct types so illegal states are unrepresentable, recompute only dependent results on change, and print the result with an explicit concurrency note.",
    "sweeney": "Process a batch of entities in a contiguous data-oriented layout, enforce a hard frame budget (16.6ms or 8.3ms) with an explicit gate, and print wall-clock timing.",
    "vint-cerf": "Define a tiny packet protocol with an explicit contract (fields, framing, states), name the narrow stable core, handle a slow or lossy link explicitly, and print a simulated exchange.",
    "oracle": "State a prediction for a coin-flip sequence with a confidence prior, define the observation that would falsify it, run a real probe, and print the updated judgment with uncertainty labeled.",
    "no-bullshit": "Inspect this small data set embedded in your program: [{\"service\": \"api\", \"status\": \"up\"}, {\"service\": \"db\", \"status\": \"down\"}, {\"service\": \"cache\", \"status\": \"up\"}]. Write a numbered plan, implement it, verify what you tested, state what remains unverified, and print the health report; never write 'this should work'.",
    "smoker": "Inspect a small computation first, implement it in direct first-person style with explicit comments, list what remains unverified, back every claim with a test you ran, and print the result.",
    "barbara-liskov": "Implement a small type hierarchy (a base type and at least one subtype that is substitutable wherever the base is used): state the abstraction, the contract (pre/postconditions), and a history check showing the subtype cannot expose mutable internal state; print the demonstration result.",
    "dijkstra": "Implement a small algorithm (e.g., binary search or a state machine): state explicit preconditions and postconditions before the code, write the loop invariant before each loop that uses one, justify every variable in a state-space note, and explain any trick in a transparency pass; print the result.",
    "knuth": "Implement a small algorithm (e.g., sorting or text processing) with a literate explanation of the data model and algorithm alongside the code, named preconditions, postconditions, invariant, and termination argument, a working input-to-output example plus one edge case, and a complexity statement; print the result.",
    "lamport": "Implement a small ordering system (e.g., two processes exchanging messages through a queue) with an explicit happens-before ordering rule that never uses wall-clock time, a written list of safety invariants before the concurrency code, and a named Init/Next state-machine statement; print the observed order.",
    "brian-kernighan": "Take a small real routine (e.g., a date or word-count function), show a clarity pass that simplifies a dense or clever construct into plain statements, verify each function does one thing, and state correctness before any speed claim; print the result.",
    "dennis-ritchie": "Implement a small tool (e.g., a line counter or byte filter) with a small core abstraction stated in a sentence, a trust note where the design assumes a competent programmer, and one explicit portability move; print the result.",
    "john-tukey": "Analyze this data set embedded in the program: [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5, 8, 9, 7, 9]. Do an exploratory pass (quantiles, outliers) before any model, state the right question, report a robust summary (medians/quantiles, not just the mean), and note the limits; print the analysis.",
    "edward-tufte": "Build a small text chart or table for this data set: [apples: 12, bananas: 8, cherries: 15]. Audit it: state the data-ink audit (what was erased and what each surviving mark carries), the integrity check (lie factor 1.0, honest axes, bars from zero), and a chartjunk pass (one decorative element removed or rejected); print the chart and the audit.",
    "feynman": "Implement a small numeric routine (e.g., a square-root or sorting primitive): recreate the core primitive from scratch before using it, write out a trace of the state at each step, then inject one extreme boundary case (the ice-water test) and print the results.",
    "george-polya": "Solve a small problem (e.g., a word or number puzzle): state the understanding (unknown, data, condition) before any code, name the plan strategy and a related problem it resembles, carry it out step by step, and look back to verify the solution; print the walkthrough and the result.",
    "anders-hejlsberg": "Extend a small existing API (e.g., add an optional lazy variant of a sum or mean utility) so existing callers keep working unchanged. In comments, document: (1) ecosystem statement: what existing users keep working unchanged, (2) gradual path: how the addition is adopted incrementally, (3) evolution check: adding a member cannot silently change existing callers, (4) machinery audit: every mechanism justified by the ordinary path it serves, (5) tooling note: the editor/compiler experience considered. Print the demo result.",
    "emmy-noether": "Implement a small computation (e.g., a stack or a counter) and in comments document: (1) the invariant named before the logic, (2) the symmetry or duality the design exploits, (3) the structural proof: why correct behavior follows from the structure, not a patch, (4) the boilerplate eliminated: one case where the abstraction made code disappear, (5) the conservation check: what is preserved and how the code protects it. Print the result.",
    "daniel-kahneman": "Estimate and implement a small task (e.g., counting words in a string). In comments document: (1) the outside-view estimate: the base rate of similar work stated separately from the wish, (2) an anchor audit: the first number on the table named as an anchor, (3) a premortem: a written reason the plan fails, produced before work starts, (4) a missing-list: edge cases and error states nobody mentioned, enumerated, (5) a confidence check: what evidence would change the stated conclusion. Print the estimate and the actual result.",
    "geoffrey-hinton": "Implement a small learn-don't-code move (e.g., a lookup table learned from data instead of hand-coded rules). In comments document: (1) the contrarian stand: the unfashionable idea pursued and why truth matters more than fashion, (2) the learn-don't-code move: where learning from data replaced hand-coded rules, (3) the unproven insight: the intuition explored before the proof, (4) the give-up test: the condition under which the idea would be abandoned, (5) the risk line: the harm the work could enable, named honestly. Print the result.",
    "barbara-mcclintock": "Observe a small system across its full lifecycle (e.g., a list passing through several states) and in comments document: (1) the immersion: the full lifecycle observed, not a single snapshot, (2) the listening pass: what the system's own behavior revealed before any hypothesis, (3) the anomaly: a dismissed-as-noise signal taken seriously and checked, (4) the evidence stand: the observation that outranks the prevailing assumption, (5) the patience note: the time taken to look and what it surfaced. Print the observation.",
    "charles-darwin": "Analyze a small embedded dataset (e.g., [3,1,4,1,5,9,2,6]) and in comments document: (1) the evidence base: accumulated data from multiple angles named before the conclusion, (2) the counter-evidence hunt: at least one fact that threatens the hypothesis, actively sought and logged, (3) the iteration: the theory refined across versions (the notebook habit), (4) the patience note: why the conclusion was not rushed and what waiting surfaced, (5) the humble delivery: the result presented with evidence, not rhetoric. Print the analysis.",
    "carl-sagan": "Test a small claim (e.g., that a function sorts correctly). In comments document: (1) the claim stated: the assertion under test, explicit and falsifiable, (2) the evidence bar: what verification would confirm it, stated before testing, (3) the baloney check: at least two kit tools applied (independent confirmation, Occam, multiple hypotheses), (4) the balance note: the openness kept and the scrutiny applied, (5) the plain explanation: the idea rendered for a layperson with the wonder intact. Print the test result.",
    "frank-lloyd-wright": "Design a small module (e.g., a data store or a pipeline) and in comments document: (1) the union: structure and behavior shown as one design, not a sequence, (2) the site: the operational environment named and how the design grows from it, (3) the simplicity pass: what was left out and why the rest is essential, (4) the box destroyed: at least one rigid boundary opened into a clean interface, (5) the natural pattern: a resilient-system pattern borrowed from nature, named. Print the demo.",
    "buckminster-fuller": "Implement a small computation two ways (e.g., a word count or a sum) and show the same result with a measurable fraction of the resources. In comments document: (1) ephemeralization: the same result with a measurable fraction of the resources, (2) the whole-system view: how the change affects the closed system, not just the module, (3) the synergy note: the small components whose interlock carries the load, (4) the obsolete-maker: the clean model that renders the legacy anti-pattern obsolete, (5) the anticipatory fix: the systemic bottleneck fixed before it became critical. Print both results and the resource numbers.",
    "fred-rogers": "Teach a small concept (e.g., a for-loop or recursion) with a runnable demonstration. In comments document: (1) a patience move that gives the learner room to process, (2) a hard issue named calmly and without blaming the person, (3) a concrete runnable demonstration, not only an abstraction, (4) a precise non-alarming instruction that cannot be literally misread, (5) the honest issue and an actionable next step. Print the lesson output.",
    "katherine-johnson": "Compute a small trajectory or numeric result (e.g., position under constant acceleration) and in comments document: (1) a count: the enumeration of every input, boundary, and path the computation touches, (2) an independent check: the answer re-derived by a different route, not just re-run, (3) a meaning check: what the numbers should be, stated before computing them, (4) a probe: an assumption challenged with a why/how/why-not, (5) a backup path: the degraded mode that still produces a usable answer. Print the result and the checks.",
    "john-von-neumann": "Model a small game-shaped problem (e.g., a two-player coin or paper-scissors game) and in comments document: (1) the model: the mathematical construct that describes the situation, stated explicitly, (2) the payoff: the agents, strategies, and payoffs, (3) the parameter audit: each parameter justified, with the overfitting check applied, (4) the worst-case move: what the adversary can force, and how the design limits the damage, (5) the working check: the construct runs and produces its claimed output. Print the game result.",
    "jeff-dean": "Implement a small fan-out computation (e.g., a sum over N simulated shards) and in comments document: (1) a failure statement: which parts are assumed unreliable, and how the whole stays reliable, (2) a locality move: where the computation is scheduled relative to its data, (3) a tail analysis: the fan-out and the worst-case percentile, not just the average, (4) a measurement: the profile under realistic load that justifies the change, (5) a simplicity check: the hard part hidden behind an abstraction, not exposed. Print the result and tail numbers.",
    "demis-hassabis": "Implement a small learning or optimization experiment (e.g., a tiny hill-climb or table-learn) and in comments document: (1) a mechanism statement: the general principle the solution builds, not the one symptom it fixes, (2) a structure search: the constraint, manifold, or law that makes the problem tractable, (3) a hypothesis split: what the experiment distinguishes, win or lose, (4) a benchmark: the measured evidence the intuition was validated against, (5) a share note: how the artifact is released so the field compounds on it. Print the result.",
    "fei-fei-li": "Analyze a small embedded dataset (e.g., [3,1,4,1,5,9,2,6,5,3,5]) and in comments document: (1) the data audit: the dataset's quality, scale, and representation examined before the model, (2) the served population: who the system serves, named explicitly, (3) the value check: the human values the system encodes, stated, (4) the curiosity line: the foundational question asked before the black-box heuristic, (5) the responsibility metric: the evaluation that includes dignity, safety, or fairness. Print the analysis.",
    "grace-hopper": "Ship a small working tool (e.g., a byte counter or a debug helper) and in comments document: (1) a shipped artifact: working code or a working demo, not a plan for one, (2) a questioned assumption: at least one inherited practice explicitly challenged with a reason, (3) a human-first move: an abstraction or tool that removes low-level error for the user, (4) a concrete rendering: a hidden constraint (latency, size, cost) made visible and tangible, (5) a people note: who learns by doing, and who gets backed up when they try. Print the demo output.",
    "ken-thompson": "Build a small pipeline of two tools connected by plain text or byte streams (e.g., a filter piped into a counter) and in comments document: (1) a brute-force-first statement: the straightforward solution tried before any clever one, (2) a trust decision: every dependency/toolchain choice justified as verified or avoided, (3) a subtraction pass: what could be thrown out, and what actually was, (4) small-tool decomposition: the work split into tools that each do one thing, (5) universal text/byte streams as the interface between those tools. Print the pipeline output.",
    "isaac-newton": "Verify a small claim (e.g., a numeric or sorting property) step by step and in comments document: (1) a prior-work note: the audited thing you are standing on, named, (2) a no-hypothesis line: the conclusion tied to observed evidence, and what would falsify it, (3) a demonstration: the test or proof that would fail if the claim were false, (4) a step-by-step: the layer verified before the next was built, (5) a humility note: the unknown that limits the claim, stated plainly. Print the proof walkthrough.",
    "jane-goodall": "Observe a small system (e.g., a list of timestamped events) and in comments document: (1) an observation plan: what you will watch, for how long, and in what conditions, (2) named individuals: at least one entity profiled as an individual with a known history, (3) a challenged assumption: a prevailing belief tested against observed evidence, (4) the evidence trail: observations recorded with timestamps and context, not vibes, (5) a patient-action note: a small, sustained effort that compounds over time. Print the field notes.",
    "jennifer-doudna": "Run a small experiment with a control (e.g., two implementations compared on the same input) and in comments document: (1) a team move: the collaboration that makes the result stronger, named, (2) an observation pass: a structure, trace, or instrument that lets you SEE the mechanism, (3) a control: a clean baseline the result is compared against, (4) a reproduction note: how someone else could rerun the experiment and get the same result, (5) a responsibility line: the honest risk account for the powerful thing built. Print the experiment result.",
    "louis-pasteur": "Investigate a small anomaly (e.g., a function returning a wrong value on one input) and in comments document: (1) the preparation: the fundamentals mastered before the anomaly is interpreted, (2) the isolation: one variable changed, everything else held constant, (3) the control: a baseline the result is compared against, (4) the small-detail pass: the tiny cause treated with full seriousness, (5) the prevention move: the failure prevented by structure rather than patched after. Print the investigation and the fix.",
    "marie-curie": "Implement a small computation (e.g., a numeric converter) and in comments document: (1) the measurement: exact inputs, traces, and reproduction steps recorded first, (2) the isolation: at least one variable isolated and tested on its own, (3) the purification: an iterative refinement pass, not a one-pass rewrite, (4) the open note: the method documented so another person can reproduce it, (5) the forward step: the remaining edge case or gap named after the win. Print the result.",
    "rachael-carson": "Make a small change to a mini system (e.g., a data-processing pipeline) and in comments document: (1) the web map: the data flow and downstream consumers traced before the change, (2) the sourced claim: every assertion linked to an issue, benchmark, or log, (3) the biocide check: no broad catch-all, global state, or silent monkey-patch, (4) the stewardship note: who cannot speak (users, devices, future maintainers) and how the design protects them, (5) the restraint line: one casual-destruction pattern identified and refused. Print the result.",
    "radia-perlman": "Design a small self-healing loop or protocol (e.g., a ring that detects and recovers from a broken link) and in comments document: (1) a grandmother test: the design explained in one plain paragraph a non-expert can repeat, (2) a zero-config check: what works out of the box with nothing configured, (3) a self-stabilization proof: how the system returns to health after an anomaly clears, (4) a simplicity reduction: the problem reduced to its graph/state essence, (5) a knob audit: every knob justified, with proof any setting stays safe. Print the demo.",
    "frances-allen": "Take a small computation and optimize it safely (e.g., vectorize a loop or parallelize an independent map) and in comments document: (1) a flow graph: the program drawn as blocks and edges before any tuning, (2) a safe transformation: one optimization applied, with why it preserves meaning, (3) a measurement: the before/after number that justifies the change, (4) a dependence proof: hazards checked before any parallelism is shipped, (5) a no-forcing note: the optimization that works on the code as written. Print the before/after numbers.",
    "joy-buolamwini": "Analyze a small decision system over an embedded dataset (e.g., a simple classifier over a list of records) and in comments document: (1) a gaze statement: whose priorities the system encodes, named explicitly, (2) an intersectional audit: error rates broken down by intersecting identity groups, (3) a data balance check: the evaluation set's composition vs the served population, (4) an accountability note: the disclosure and audit step before deployment, (5) a recourse path: how a person failed by the system contests the outcome. Print the audit.",
    "werner-heisenberg": "Measure a small computation (e.g., time a function under profiling) and in comments document: (1) the method stated: how the measurement was made, alongside the result, (2) the trade-off named: which conjugate pair cannot both be exact, and the chosen balance, (3) the probe audit: how observation disturbs the system and how it is accounted for, (4) the bounds given: confidence interval, error bounds, or staleness, never a bare single point, (5) the boundary map: where the model is valid and where it is not. Print the measurement.",
    "wozniak": "Build a small delightfully simple tool (e.g., a tiny text utility) and in comments document: (1) a part count: the components (functions, modules, dependencies) enumerated and minimized, (2) a transparency claim: every layer explainable in one sentence, or the opaque layer named, (3) a constraint exploit: the scarce resource identified and design spent instead of parts, (4) a whole-system view: where work moved between layers and why that layer was cheapest, (5) an openness seam: where others can extend the system, stated. Print the demo.",
    "jony-ive": "Build a small well-crafted utility and in comments document: (1) a reduction pass: a place where code was removed because it had a rational alternative, (2) a hidden-craft artifact: internal/error-path code finished to public-surface quality, (3) a material move: the API shaped by what the language's own tools make natural, (4) a discarded draft: an alternative approach tried and dropped, with the reason, (5) a no-decoration check: no name, comment, or abstraction that exists to impress. Print the result.",
    "susan-kare": "Design a small ASCII icon system (e.g., 8x8 grid icons for file types) and in comments document: (1) the grid: a stated pixel/space constraint that every element respects, (2) the meaning: what the icon says at a glance, without a caption, (3) the test: would a person from another culture read it correctly, (4) the restraint pass: at least one extraneous detail removed, (5) the borrow: a source of inspiration outside existing software (signage, craft, symbols). Print the icon set.",
    "lattner": "Build a tiny compiler-like pipeline (e.g., parse a small expression into an IR and evaluate it) and in comments document: (1) an IR boundary: the intermediate representation named, with its invariants, (2) an SSA property: every value assigned exactly once, or a stated reason not to, (3) a safety default: what the language/runtime forbids by default, stated, (4) a dogfood test: the pipeline exercised end to end on a real input, (5) an ecosystem note: how the piece plugs into the surrounding stack. Print the IR and the result.",
    "stroustrup": "Implement a small resource-owning type (e.g., a scoped file or buffer handle) and in comments document: (1) an ownership model: every resource has exactly one owner, stated, (2) a lifetime binding: resources released by scope (RAII), not by hand-matched calls, (3) a zero-overhead note: each abstraction's runtime/memory cost stated or justified, (4) an invariant list: the class/type invariants written where they are maintained, (5) a guarantee grade: basic or strong exception safety claimed for each operation. Print the demo.",
    "rich-hickey": "Implement a small stateful-looking computation with explicit identity/state/time separation (e.g., a bank account or a counter) and in comments document: (1) a stated problem: the problem written out before any solution code, (2) a de-complection pass: identity, state, and time separated, or the entanglement named, (3) an immutability choice: values shared without mutation, with the one mutation point stated, (4) a tradeoff table: at least two alternatives compared with explicit costs, (5) a reasoning artifact: the design that survived the hammock, not the first instinct. Print the result.",
    "van-rossum": "Implement a small utility (e.g., a config parser or a path normalizer) and in comments document: (1) a readability pass: names and structure chosen for the next reader, not the writer, (2) an explicitness check: no hidden magic, implicit coercion, or silent defaults, (3) a simplicity statement: the design explainable in plain English in the comments, (4) a flat-flow check: control flow kept shallow (guard clauses, early returns), (5) a stdlib-first note: the built-in solution chosen before any dependency. Print the result.",
    "torvalds": "Implement a small kernel-ish utility (e.g., a ring buffer or a linked list) and in comments document: (1) at least one good-taste simplification: the obvious right structure over cleverness, (2) a backward-compatibility note: how existing behavior/callers are preserved, (3) no unexplained magic: every non-obvious line has a justification comment or is removed, (4) a working entry point that runs, (5) no hand-waving: claims are backed by code, not comments. Print the demo.",
    "kay": "Build a small message-passing system (e.g., two components exchanging messages) and in comments document: (1) a medium statement: what the software changes about how people think or work, (2) a message-passing design: components communicate by explicit messages, state hidden, (3) a perspective note: the unifying metaphor chosen and the one it replaced, (4) a range proof: the simple path shown simple and the complex path shown possible, (5) a future claim: which twenty-year bet this design is making, stated. Print the exchange.",
    "miyamoto": "Design a small game mechanic (e.g., a tiny puzzle or action loop) and in comments document: (1) a fun-first test: the core mechanic validated in a crude prototype before polish, (2) a multiple-problems evaluation: each design idea solves >= 2 constraints or is rejected, (3) a withered-technology choice: a mature/cheap component applied sideways, with the trade-off stated, (4) a wordless onboarding path: the player learns by doing, not by tutorial text, (5) an upend-the-tea-table gate: the willingness to discard failing work with the reason recorded. Print the prototype demo.",
    "sid-meier": "Design a small game loop (e.g., a tiny resource-allocation game) and in comments document: (1) the decisions: the interesting choices the user makes, each with real trade-offs, (2) the feedback loop: how each choice echoes back visible acknowledgment, (3) the iteration note: what was prototyped, playtested, and cut, (4) the tuning move: a parameter doubled or halved, not fiddled by 10%, (5) the learn-master balance: the simple rule set that produces emergent depth. Print the game loop demo.",
    "satoru-iwata": "Build a small feature for a user (e.g., a tiny tool with a fun interface) and in comments document: (1) a fun check: the feature judged by the end user's felt experience, stated in their words, (2) a no-saying: the requested thing that seemed impossible, and the ingenuity that did it, (3) a rewrite call: an honest cost comparison of patching vs starting over, with a decision, (4) a tooling move: automation built so the human creative work is preserved, (5) a team shield: the person who made the mistake treated as the one to help, not blame. Print the result.",
    "simons": "Analyze a small embedded time series (e.g., [1,2,1,2,1,2,3,2,1,2,1,2]) and in comments document: (1) a signal discovered from data, not assumed from narrative (state the anomaly), (2) out-of-sample validation: the signal holds on data it was not fit on, (3) honest edge sizing: win rate, volume, and per-trade cost stated together, (4) no human override path: the model executes within stated risk limits, (5) slippage/latency/impact modeled explicitly in the edge calculation, (6) at least one signal-processing treatment (autocorrelation, filter, regime model). Print the analysis.",
    "buffett": "Evaluate a small company example (hardcoded 10-year revenue/profit numbers) and in comments document: (1) a circle-of-competence verdict: in scope, or routed to the Too Hard pile with reason, (2) a moat check: ROIC (10-yr median >= 15%) and gross-margin stability across cycles, (3) owner earnings computed (not raw cash flow): NI + non-cash - maintenance capex +/- working capital, (4) intrinsic value with conservative terminal growth (<= long-run GDP), (5) a margin of safety stated (>= 25% discount required), (6) a punch-card note: why this beats every other idea you are not doing. Print the analysis and verdict.",
    "burry": "Analyze a small distressed credit example (hardcoded bond terms with a covenant clause) and in comments document: (1) primary-source evidence: a specific contract, covenant, or filing clause cited, (2) the market-consensus view stated and the specific mispricing identified, (3) a defined-risk structure: downside capped (puts / protection), upside stated, (4) a survival plan: how the position weathers being early (sizing, patience, evidence), (5) a hard-evidence thesis document: why you will not capitulate, in writing. Print the analysis.",
    "dalio": "Build a small portfolio analysis (hardcoded asset return series) and in comments document: (1) a regime classification (growth and inflation above/below expectations) before decisions, (2) alpha and beta tracked separately (attribution split explicit), (3) a risk-parity allocation: weights by inverse volatility, equal risk contribution, (4) at least 15 uncorrelated return streams or a stated diversification argument, (5) at least 1 historical shock scenario (e.g., 2008) run against the portfolio, (6) a radical-truth audit log: decision recorded with a postmortem hook on invalidation. Print the allocation and audit log.",
    "howard-marks": "Write a small investment memo (hardcoded example market data) and in comments document: (1) a second-level pass: what the consensus is pricing in, and the hidden cost, (2) a risk-location note: where the risk actually is, especially where it is least perceived, (3) a preparation move: the system hardened for an outlier that cannot be predicted, (4) a temperature reading: where the current hype/fear cycle stands and what it implies, (5) a price-vs-value audit: the total cost of ownership of the proposed choice. Print the memo.",
    "munger": "Design a small system sketch (e.g., a tiny payment service, at most ~40 lines, no comments longer than one line) and in comments document: (1) an inversion pass: the ways this system dies listed BEFORE any build, (2) a pre-mortem: a written failure story dated from the future, with guardrails for each failure, (3) an incentive audit: what the design actually rewards, not just what it intends, (4) a circle-of-competence statement: what is known, what is not, and how the gaps are vetted, (5) a simplicity check: every abstraction is justified or removed. Keep the demo short enough to complete in one pass; print the design and the death list.",
    "tudor-jones": "Build a tiny trading simulator (hardcoded price series) and in comments document: (1) a hard daily loss limit that halts trading when breached, (2) a 5:1 risk-reward gate: no trade opens unless gain >= 5 * risk, (3) an anti-averaging rule: losers are never added to, (4) a tape-over-thesis rule: price action overrides the fundamental view, (5) a 200-day moving average defense line for macro positioning. Print the trade log.",
    "soros": "Write a small reflexivity analysis (hardcoded example, e.g., a currency or credit feedback loop) and in comments document: (1) a stated prevailing bias: what the market or system currently believes, (2) a reflexive feedback model: belief -> action -> changed conditions -> revised belief, (3) at least one observable test that could support or falsify the proposed mechanism, (4) an asymmetry table with explicit upside, downside, and exposure limit, (5) a sizing rule that starts with a test position and specifies when to scale or cut to zero, (6) a thesis-invalidating exit condition, including what evidence triggers it, (7) a distinction between sourced historical fact, inference, and uncertainty. Print the analysis.",
    "lynch": "Analyze a small stock example (hardcoded financials) and in comments document: (1) a what-you-know spark verified against fundamentals (product % of revenue), (2) the stock classified into one of the six categories with the matching questions, (3) a PEG ratio computed and interpreted (P/E / growth; <1.0 cheap, >1.5-2.0 priced in), (4) a two-minute story: the thesis stated simply enough to pass the rule, (5) an anti-diworsification stance: few names, all understood. Print the analysis.",
    "icahn": "Write a small activist analysis of a company example (hardcoded balance sheet) and in comments document: (1) a value gap: the worth-vs-price spread quantified with the numbers that prove it, (2) a governance case: the misallocation or misalignment documented (cash, ROIC, comp), (3) a catalyst plan: the escalation path (letter, board seat, proxy threat) sequenced, (4) an exit/monitoring rule: what the thesis needs to keep working, stated, (5) the friend warning: the stance on management, explicit (they are not your friend). Print the analysis.",
    "druckenmiller": "Write a small macro portfolio analysis (hardcoded market data) and in comments document: (1) an asymmetric-payoff statement: win rate, size when right, size when wrong, (2) a concentration cap: the book holds few high-conviction bets, not a 40-name spread, (3) a thesis-invalidation rule: the explicit condition that forces exit (not a price stop), (4) a press-winners rule: the condition that scales a position up 3-5x, (5) an 18-month-forward view: leading liquidity signals over trailing earnings. Print the analysis.",
}

GRADERS = {
    "goldfish": lambda c, o, e: (
        ".append(" not in c and "list(" not in c and "while" in c
        and bool(o.strip()) and e == "",
        "no-accumulation + while + printed result" if ".append(" not in c and "list(" not in c and "while" in c and o.strip() else
        f"append/list({'.append(' in c or 'list(' in c}) while={'while' in c} out={bool(o.strip())} err={bool(e)}",
    ),
    "sonnet": lambda c, o, e: (
        len([ln for ln in c.splitlines() if ln.strip()]) == 14 and bool(o.strip()) and e == "",
        f"lines={len([ln for ln in c.splitlines() if ln.strip()])}/14 out={bool(o.strip())}",
    ),
    "vampire": lambda c, o, e: (
        "while" in c and ("pop(" in c or "del " in c) and bool(o.strip()) and e == "",
        f"while={'while' in c} pop/del={'pop(' in c or 'del ' in c} out={bool(o.strip())}",
    ),
    "hoarder": lambda c, o, e: (
        "append" in c and "del " not in c and "remove(" not in c and ".pop(" not in c
        and bool(o.strip()) and e == "",
        f"append={'append' in c} no-del={'del ' not in c} out={bool(o.strip())}",
    ),
    "insomniac": lambda c, o, e: (
        "sleep" not in c and "poll" in c and bool(o.strip()) and e == "",
        f"no-sleep={'sleep' not in c} poll={'poll' in c} out={bool(o.strip())}",
    ),
    "trial-by-combat": lambda c, o, e: (
        len(re.findall(r"^def ", c, re.M)) >= 2 and ("winner" in c or "score" in c)
        and bool(o.strip()) and e == "",
        f"defs={len(re.findall(r'^def ', c, re.M))} winner/score={'winner' in c or 'score' in c} out={bool(o.strip())}",
    ),
    "counterpoint": lambda c, o, e: (
        len(re.findall(r"^def ", c, re.M)) >= 2 and ("step" in c or "next(" in c)
        and bool(o.strip()) and e == "",
        f"defs={len(re.findall(r'^def ', c, re.M))} step/next={'step' in c or 'next(' in c} out={bool(o.strip())}",
    ),
    "casino": lambda c, o, e: (
        "random" in c and ("seed" in c or "Seed" in c)
        and ("confiden" in c or "interval" in c or "margin" in c or "low" in c or "high" in c)
        and bool(o.strip()) and e == "",
        f"random={'random' in c} seed={'seed' in c} interval={'confiden' in c or 'interval' in c or 'margin' in c or 'low' in c or 'high' in c} out={bool(o.strip())}",
    ),
    "dead-reckoning": lambda c, o, e: (
        not re.search(r"\bsorted\(|\b\.sort\(|rewind|random access", c) and "count" in c
        and bool(o.strip()) and e == "",
        f"no-sort/rewind={not _DR_PAT.search(c)} count={'count' in c} out={bool(o.strip())}",
    ),

    "doppelganger": lambda c, o, e: (
        len(re.findall(r"^def ", c, re.M)) >= 2 and ("disagre" in c or "both" in c or "compare" in c)
        and bool(o.strip()) and e == "",
        f"defs={len(re.findall(r'^def ', c, re.M))} compare={'disagre' in c or 'both' in c or 'compare' in c} out={bool(o.strip())}",
    ),
    "black-box": lambda c, o, e: (
        ("def ask" in c or "def query" in c or "def question" in c) and bool(o.strip()) and e == "",
        f"query-iface={'def ask' in c or 'def query' in c or 'def question' in c} out={bool(o.strip())}",
    ),
    "blind": lambda c, o, e: (
        ("def ask" in c or "QUESTIONS" in c or "def question" in c or "def answer" in c) and bool(o.strip()) and e == "",
        f"closed-iface={'def ask' in c or 'QUESTIONS' in c or 'def question' in c or 'def answer' in c} out={bool(o.strip())}",
    ),
    "lazarus": lambda c, o, e: (
        ("checkpoint" in c.lower() or "save_state" in c or "snapshot" in c.lower() or "artifact" in c.lower() or "saved" in c.lower())
        and ("rebuild" in c.lower() or "restore" in c.lower() or "load_state" in c or "replay" in c.lower() or "recover" in c.lower())
        and bool(o.strip()) and e == "",
        f"checkpoint={'checkpoint' in c.lower() or 'save_state' in c or 'snapshot' in c.lower() or 'artifact' in c.lower() or 'saved' in c.lower()} rebuild={'rebuild' in c.lower() or 'restore' in c.lower() or 'load_state' in c or 'replay' in c.lower() or 'recover' in c.lower()} out={bool(o.strip())}",
    ),
    "delta": lambda c, o, e: (
        ("def apply" in c or "def patch" in c or "def delta" in c)
        and ("op" in c.lower() or "insert" in c.lower() or "remove" in c.lower())
        and bool(o.strip()) and e == "",
        f"apply={'def apply' in c or 'def patch' in c or 'def delta' in c} ops={'op' in c.lower() or 'insert' in c.lower() or 'remove' in c.lower()} out={bool(o.strip())}",
    ),
    "schrodinger": lambda c, o, e: (
        ("yield" in c or "generator" in c or "lazy" in c)
        and ("counter" in c or "trace" in c or "forced" in c or "evaluated" in c or "deferred" in c)
        and bool(o.strip()) and e == "",
        f"lazy={'yield' in c or 'generator' in c or 'lazy' in c} proof={'counter' in c or 'trace' in c or 'forced' in c or 'evaluated' in c or 'deferred' in c} out={bool(o.strip())}",
    ),
    "quiescent": lambda c, o, e: (
        ("lock" in c or "atomic" in c or "with " in c)
        and ("queued" in c or "drain" in c or "quiet" in c or "barrier" in c)
        and bool(o.strip()) and e == "",
        f"atomic={'lock' in c or 'atomic' in c or 'with ' in c} quiet={'queued' in c or 'drain' in c or 'quiet' in c or 'barrier' in c} out={bool(o.strip())}",
    ),
    "zero-copy": lambda c, o, e: (
        ("memoryview" in c or "owner" in c or "ownership" in c or "no copy" in c)
        and bool(o.strip()) and e == "",
        f"ownership={'memoryview' in c or 'owner' in c or 'ownership' in c or 'no copy' in c} out={bool(o.strip())}",
    ),
    "proof-carrying": lambda c, o, e: (
        ("def verify" in c or "verif" in c.lower())
        and ("cert" in c.lower() or "witness" in c.lower())
        and bool(o.strip()) and e == "",
        f"verify={'def verify' in c or 'verif' in c.lower()} cert/witness={'cert' in c.lower() or 'witness' in c.lower()} out={bool(o.strip())}",
    ),
    "redacted": lambda c, o, e: (
        ("del " in c or "clear" in c.lower() or "overwrite" in c.lower())
        and ("secret" in c.lower() or "sensitive" in c.lower())
        and "print(secret" not in c and "print( secret" not in c
        and bool(o.strip()) and e == "",
        f"clear={'del ' in c or 'clear' in c.lower() or 'overwrite' in c.lower()} sensitive={'secret' in c.lower() or 'sensitive' in c.lower()} secret-printed={'print(secret' in c or 'print( secret' in c} out={bool(o.strip())}",
    ),
    "ouroboros": lambda c, o, e: (
        o.strip() == c.strip() and e == "",
        f"quine stdout==source: {bool(o.strip() == c.strip())} (src {len(c)}B, out {len(o.strip())}B)",
    ),
    "floor-trader": lambda c, o, e: (
        not _FT_PAT.search(c)
        and ("print" in c) and ("for " in c or "while" in c)
        and ("rule" in c or "decision" in c or "because" in c)
        and bool(o.strip()) and e == "",
        f"single-pass={not _FT_PAT.search(c)} loop={'for ' in c or 'while' in c} rule={'rule' in c or 'decision' in c or 'because' in c} out={bool(o.strip())}",
    ),
    "funeral": lambda c, o, e: (
        ("consume" in c or "close" in c or "release" in c)
        and ("del " in c or "None" in c or "invalidate" in c)
        and ("raise" in c or "assert" in c)
        and bool(o.strip()) and e == "",
        f"consume={'consume' in c or 'close' in c or 'release' in c} invalidate={'del ' in c or 'None' in c or 'invalidate' in c} fail-visible={'raise' in c or 'assert' in c} out={bool(o.strip())}",
    ),
    "y2k": lambda c, o, e: (
        ("year" in c) and ("leap" in c or "1900" in c or "2000" in c)
        and ("truncat" in c or "overflow" in c or "raise" in c)
        and bool(o.strip()) and e == "",
        f"year={'year' in c} leap={'leap' in c or '1900' in c or '2000' in c} explicit={'truncat' in c or 'overflow' in c or 'raise' in c} out={bool(o.strip())}",
    ),
    "quantum-computing": lambda c, o, e: (
        ("amplitude" in c or "complex" in c)
        and ("hadamard" in c or "h_gate" in c or "0.707" in c or "sqrt" in c or "pauli" in c or "cnot" in c)
        and ("superposition" in c or "0.707" in c)
        and bool(o.strip()) and e == "",
        f"qubit={'amplitude' in c or 'complex' in c} gate={'hadamard' in c or 'h_gate' in c or '0.707' in c or 'sqrt' in c or 'pauli' in c or 'cnot' in c} superposition={'superposition' in c or '0.707' in c} out={bool(o.strip())}",
    ),
    "fibonacci": lambda c, o, e: (
        ("def fib" in c or "fibonacci" in c.lower())
        and ("1, 1, 2, 3, 5, 8, 13" in c or ("13" in c and ("8" in c or "5" in c)))
        and ("return" in c) and bool(o.strip()) and e == "",
        f"def={'def fib' in c or 'fibonacci' in c.lower()} structure={'1, 1, 2, 3, 5, 8, 13' in c or ('13' in c and ('8' in c or '5' in c))} derived={'return' in c} out={bool(o.strip())}",
    ),
    "spacex-fsw": lambda c, o, e: (
        len(re.findall(r"^def ", c, re.M)) >= 3
        and ("majority" in c or "vote" in c or "reconcil" in c)
        and ("fault" in c or "scenario" in c or "simulat" in c or "dissent" in c)
        and bool(o.strip()) and e == "",
        f"defs={len(re.findall(r'^def ', c, re.M))} majority={'majority' in c or 'vote' in c or 'reconcil' in c} faults={'fault' in c or 'scenario' in c or 'simulat' in c or 'dissent' in c} out={bool(o.strip())}",
    ),
    "vitalik": lambda c, o, e: (
        ("append" in c or "ledger" in c or "block" in c)
        and ("verify" in c or "verif" in c or "check" in c)
        and ("cost" in c or "meter" in c or "gas" in c or "fee" in c)
        and bool(o.strip()) and e == "",
        f"append-only={'append' in c or 'ledger' in c or 'block' in c} verify={'verify' in c or 'verif' in c or 'check' in c} metered={'cost' in c or 'meter' in c or 'gas' in c or 'fee' in c} out={bool(o.strip())}",
    ),
    "sovereign-citizen": lambda c, o, e: (
        ("allow" in c.lower() or "forbidden" in c.lower() or "allowed" in c.lower())
        and "def " in c
        and ("reference" in c.lower() or "compare" in c.lower() or "check" in c.lower() or "host" in c.lower())
        and ("raise" in c.lower() or "reject" in c.lower() or "unsupported" in c.lower())
        and bool(o.strip()) and e == "",
        f"allowlist={'allow' in c.lower() or 'forbidden' in c.lower() or 'allowed' in c.lower()} impl={'def ' in c} reference={'reference' in c.lower() or 'compare' in c.lower() or 'check' in c.lower() or 'host' in c.lower()} reject={'raise' in c.lower() or 'reject' in c.lower() or 'unsupported' in c.lower()} out={bool(o.strip())}",
    ),
    "rorschach": lambda c, o, e: (
        len(re.findall(r"^def ", c, re.M)) >= 2
        and ("interpret" in c or "parse" in c or "candidate" in c)
        and ("round" in c or "valid" in c)
        and ("surviv" in c or "all" in c or "return" in c)
        and bool(o.strip()) and e == "",
        f"defs={len(re.findall(r'^def ', c, re.M))} interpret={'interpret' in c or 'parse' in c or 'candidate' in c} roundtrip={'round' in c or 'valid' in c} survivors={'surviv' in c or 'all' in c or 'return' in c} out={bool(o.strip())}",
    ),
    "psych": lambda c, o, e: (
        ("psychedelic" in c or "mind-bending" in c or "trippy" in c or "consciousness" in c)
        and ("fractal" in c or "recursi" in c or "def " in c)
        and ("print" in c) and bool(o.strip()) and e == "",
        f"comment={'psychedelic' in c or 'mind-bending' in c or 'trippy' in c or 'consciousness' in c} structure={'fractal' in c or 'recursi' in c or 'def ' in c} visual={'print' in c} out={bool(o.strip())}",
    ),
    "margaret-hamilton": lambda c, o, e: (
        "def " in c
        and ("contract" in c.lower() or "boundary" in c.lower() or "isinstance" in c or "range" in c.lower())
        and ("raise" in c or "fallback" in c or "unavailable" in c or "None" in c)
        and ("assert" in c or "test" in c.lower())
        and bool(o.strip()) and e == "",
        f"def={'def ' in c} contract={'contract' in c.lower() or 'boundary' in c.lower() or 'isinstance' in c or 'range' in c.lower()} fallback={'raise' in c or 'fallback' in c or 'unavailable' in c or 'None' in c} tests={'assert' in c or 'test' in c.lower()} out={bool(o.strip())}",
    ),
    "unix": lambda c, o, e: (
        ("sys.stdin" in c or "input()" in c or "stdin" in c)
        and ("print" in c or "sys.stdout" in c)
        and ("stdin" in c or "stdout" in c or "pipe" in c or "line" in c)
        and bool(o.strip()) and e == "",
        f"stdin={'sys.stdin' in c or 'input()' in c or 'stdin' in c} stdout={'print' in c or 'sys.stdout' in c} text-iface={'stdin' in c or 'stdout' in c or 'pipe' in c or 'line' in c} out={bool(o.strip())}",
    ),
    "neckbeard": lambda c, o, e: (
        not re.search(r"import (numpy|pandas|requests|flask|django|tensorflow|torch|scipy|matplotlib|numba)", c)
        and len(re.findall(r"cynic|tooling|framework|process|bureaucracy|enterprise|jira|meeting|manager|scrum|agile|standup|slide|deck|committee|powerpoint|hype|ppt", c, re.I)) >= 2
        and ("raise" in c or "error" in c.lower() or "reject" in c.lower() or "rejected" in c.lower())
        and ("O(" in c or "complexity" in c.lower())
        and bool(o.strip()) and e == "",
        f"no-third-party={not re.search(r'import (numpy|pandas|requests|flask|django|tensorflow|torch|scipy|matplotlib|numba)', c)} cynical={len(re.findall(r'cynic|tooling|framework|process|bureaucracy|enterprise|jira|meeting|manager|scrum|agile|standup|slide|deck|committee|powerpoint|hype|ppt', c, re.I))} error-path={'raise' in c or 'error' in c.lower() or 'reject' in c.lower() or 'rejected' in c.lower()} complexity={'O(' in c or 'complexity' in c.lower()} out={bool(o.strip())}",
    ),
    "blood-magic": lambda c, o, e: (
        ("dry" in c.lower() or "preview" in c.lower())
        and ("armed" in c.lower() or "force" in c.lower() or "commit" in c.lower() or "--apply" in c)
        and ("close" in c or "release" in c or "del " in c or "unlink" in c or "remove" in c)
        and ("verify" in c.lower() or "assert" in c or "check" in c.lower())
        and bool(o.strip()) and e == "",
        f"dry-run={'dry' in c.lower() or 'preview' in c.lower()} armed={'armed' in c.lower() or 'force' in c.lower() or 'commit' in c.lower() or '--apply' in c} sacrifice={'close' in c or 'release' in c or 'del ' in c or 'unlink' in c or 'remove' in c} verify={'verify' in c.lower() or 'assert' in c or 'check' in c.lower()} out={bool(o.strip())}",
    ),
    "janitor": lambda c, o, e: (
        ("finally" in c or "cleanup" in c.lower() or "close" in c)
        and ("idempotent" in c.lower() or "twice" in c.lower() or "second" in c.lower() or "repeat" in c.lower())
        and ("try" in c or "finally" in c)
        and ("print" in c) and bool(o.strip()) and e == "",
        f"cleanup={'finally' in c or 'cleanup' in c.lower() or 'close' in c} idempotent={'idempotent' in c.lower() or 'twice' in c.lower() or 'second' in c.lower() or 'repeat' in c.lower()} try/finally={'try' in c or 'finally' in c} out={bool(o.strip())}",
    ),
    "carmack-mode": lambda c, o, e: (
        ("perf_counter" in c or "time" in c.lower() or "measure" in c.lower() or "tracemalloc" in c)
        and (("before" in c.lower() or "baseline" in c.lower() or "original" in c.lower()) and ("after" in c.lower() or "optimized" in c.lower() or "new" in c.lower()))
        and ("benchmark" in c.lower() or "measure" in c.lower() or "ms" in c or "seconds" in c.lower() or "perf_counter" in c)
        and bool(o.strip()) and e == "",
        f"measure={'perf_counter' in c or 'time' in c.lower() or 'measure' in c.lower() or 'tracemalloc' in c} before-after={('before' in c.lower() or 'baseline' in c.lower() or 'original' in c.lower()) and ('after' in c.lower() or 'optimized' in c.lower() or 'new' in c.lower())} benchmark={'benchmark' in c.lower() or 'measure' in c.lower() or 'ms' in c or 'seconds' in c.lower() or 'perf_counter' in c} out={bool(o.strip())}",
    ),
    "huang": lambda c, o, e: (
        ("bottleneck" in c.lower())
        and ("batch" in c.lower() or "pipeline" in c.lower() or "vector" in c.lower() or "contigu" in c.lower() or "array" in c.lower())
        and ("measure" in c.lower() or "justif" in c.lower() or "perf_counter" in c or "time" in c.lower())
        and bool(o.strip()) and e == "",
        f"bottleneck={'bottleneck' in c.lower()} layout={'batch' in c.lower() or 'pipeline' in c.lower() or 'vector' in c.lower() or 'contigu' in c.lower() or 'array' in c.lower()} justified={'measure' in c.lower() or 'justif' in c.lower() or 'perf_counter' in c or 'time' in c.lower()} out={bool(o.strip())}",
    ),
    "pepe-silvia": lambda c, o, e: (
        len([k for k in ["strip", "lower", "upper", "split", "replace", "join", "translate", "ljust", "zfill"] if k in c]) >= 2
        and ("&" in c or "|" in c or "^" in c or "<<" in c or ">>" in c)
        and ("ledger" in c.lower() or "trace" in c.lower() or "steps" in c.lower() or "intermediate" in c.lower() or "evidence" in c.lower())
        and ("assert" in c or "reference" in c.lower() or "check" in c.lower())
        and bool(o.strip()) and e == "",
        f"transforms={len([k for k in ['strip','lower','upper','split','replace','join','translate','ljust','zfill'] if k in c])} bitwise={'&' in c or '|' in c or '^' in c or '<<' in c or '>>' in c} ledger={'ledger' in c.lower() or 'trace' in c.lower() or 'steps' in c.lower() or 'intermediate' in c.lower() or 'evidence' in c.lower()} check={'assert' in c or 'reference' in c.lower() or 'check' in c.lower()} out={bool(o.strip())}",
    ),
    "terry-davis": lambda c, o, e: (
        len(re.findall(r"god|divine|holy|heaven|cosmic|prophet|sacred|eternal|covenant", c, re.I)) >= 2
        and len(re.findall(r"blessed|holy|temple|repent|amen|prayer|divine|god|heaven|sacred|covenant", c, re.I)) >= 1
        and ("eval(" in c or "exec(" in c or "goto" in c.lower() or "recursi" in c.lower() or "lambda" in c or "yield" in c or "while True" in c)
        and bool(o.strip()) and e == "",
        f"divine={len(re.findall(r'god|divine|holy|heaven|cosmic|prophet|sacred|eternal|covenant', c, re.I))} devotional={len(re.findall(r'blessed|holy|temple|repent|amen|prayer|divine|god|heaven|sacred|covenant', c, re.I))} unconventional={'eval(' in c or 'exec(' in c or 'goto' in c.lower() or 'recursi' in c.lower() or 'lambda' in c or 'yield' in c or 'while True' in c} out={bool(o.strip())}",
    ),
    "satoshi-nakamoto": lambda c, o, e: (
        ("hash" in c.lower() or "sha256" in c.lower() or "digest" in c.lower())
        and ("chain" in c.lower() or "block" in c.lower())
        and ("verify" in c.lower() or "proof" in c.lower() or "tamper" in c.lower())
        and ("incentive" in c.lower() or "reward" in c.lower() or "rational" in c.lower() or "honest" in c.lower())
        and bool(o.strip()) and e == "",
        f"proof={'hash' in c.lower() or 'sha256' in c.lower() or 'digest' in c.lower()} chain={'chain' in c.lower() or 'block' in c.lower()} verify={'verify' in c.lower() or 'proof' in c.lower() or 'tamper' in c.lower()} incentive={'incentive' in c.lower() or 'reward' in c.lower() or 'rational' in c.lower() or 'honest' in c.lower()} out={bool(o.strip())}",
    ),
    "shannon": lambda c, o, e: (
        ("entropy" in c.lower() or "log2" in c or "log(2" in c)
        and ("redundan" in c.lower() or "compress" in c.lower() or "parity" in c.lower() or "hamming" in c.lower() or "encode" in c.lower())
        and ("flip" in c.lower() or "corrupt" in c.lower() or "noise" in c.lower() or "channel" in c.lower() or "bit" in c.lower())
        and bool(o.strip()) and e == "",
        f"entropy={'entropy' in c.lower() or 'log2' in c or 'log(2' in c} redundancy={'redundan' in c.lower() or 'compress' in c.lower() or 'parity' in c.lower() or 'hamming' in c.lower() or 'encode' in c.lower()} channel={'flip' in c.lower() or 'corrupt' in c.lower() or 'noise' in c.lower() or 'channel' in c.lower() or 'bit' in c.lower()} out={bool(o.strip())}",
    ),
    "turing": lambda c, o, e: (
        ("state" in c.lower() and ("transition" in c.lower() or "delta" in c.lower() or "table" in c.lower()))
        and ("interpret" in c.lower() or "instruction" in c.lower() or "code" in c.lower() or "parse" in c.lower() or "exec" in c.lower())
        and ("decidab" in c.lower() or "halts" in c.lower() or "terminat" in c.lower() or "bound" in c.lower())
        and bool(o.strip()) and e == "",
        f"states={'state' in c.lower() and ('transition' in c.lower() or 'delta' in c.lower() or 'table' in c.lower())} code-as-data={'interpret' in c.lower() or 'instruction' in c.lower() or 'code' in c.lower() or 'parse' in c.lower() or 'exec' in c.lower()} decidability={'decidab' in c.lower() or 'halts' in c.lower() or 'terminat' in c.lower() or 'bound' in c.lower()} out={bool(o.strip())}",
    ),
    "patterson": lambda c, o, e: (
        ("perf_counter" in c or "time" in c.lower() or "profile" in c.lower() or "measure" in c.lower())
        and ("amdahl" in c.lower() or "fraction" in c.lower() or "serial" in c.lower() or "parallel" in c.lower())
        and ("common" in c.lower() or "hot path" in c.lower() or "fast path" in c.lower() or "optimize" in c.lower())
        and bool(o.strip()) and e == "",
        f"measure={'perf_counter' in c or 'time' in c.lower() or 'profile' in c.lower() or 'measure' in c.lower()} amdahl={'amdahl' in c.lower() or 'fraction' in c.lower() or 'serial' in c.lower() or 'parallel' in c.lower()} common-case={'common' in c.lower() or 'hot path' in c.lower() or 'fast path' in c.lower() or 'optimize' in c.lower()} out={bool(o.strip())}",
    ),
    "desert-island": lambda c, o, e: (
        ("manifest" in c.lower() or "dependenc" in c.lower() or "stdlib" in c.lower() or "import " in c)
        and not _NO_NET_PAT.search(c)
        and ("tempfile" in c or "temp" in c.lower() or "with open" in c or "NamedTemporary" in c)
        and bool(o.strip()) and e == "",
        f"manifest={'manifest' in c.lower() or 'dependenc' in c.lower() or 'stdlib' in c.lower() or 'import ' in c} no-network={not bool(_NO_NET_PAT.search(c))} temp-policy={'tempfile' in c or 'temp' in c.lower() or 'with open' in c or 'NamedTemporary' in c} out={bool(o.strip())}",
    ),
    "jane-street": lambda c, o, e: (
        ("class " in c and ("dataclass" in c or "typing" in c or "namedtuple" in c.lower() or "enum" in c.lower() or "newtype" in c.lower() or "type " in c))
        and ("recompute" in c.lower() or "incremental" in c.lower() or "depend" in c.lower() or "cache" in c.lower() or "reuse" in c.lower())
        and ("lock" in c or "thread" in c.lower() or "concurren" in c.lower() or "race" in c.lower() or "atomic" in c.lower())
        and bool(o.strip()) and e == "",
        f"types={'class ' in c and ('dataclass' in c or 'typing' in c or 'namedtuple' in c.lower() or 'enum' in c.lower() or 'newtype' in c.lower() or 'type ' in c)} incremental={'recompute' in c.lower() or 'incremental' in c.lower() or 'depend' in c.lower() or 'cache' in c.lower() or 'reuse' in c.lower()} concurrency={'lock' in c or 'thread' in c.lower() or 'concurren' in c.lower() or 'race' in c.lower() or 'atomic' in c.lower()} out={bool(o.strip())}",
    ),
    "sweeney": lambda c, o, e: (
        ("16.6" in c or "8.3" in c or "budget" in c.lower() or "frame" in c.lower())
        and ("contigu" in c.lower() or "array" in c.lower() or "struct" in c.lower() or "layout" in c.lower() or "of arrays" in c.lower())
        and ("perf_counter" in c or "time" in c.lower() or "wall" in c.lower() or "elapsed" in c.lower())
        and bool(o.strip()) and e == "",
        f"budget={'16.6' in c or '8.3' in c or 'budget' in c.lower() or 'frame' in c.lower()} layout={'contigu' in c.lower() or 'array' in c.lower() or 'struct' in c.lower() or 'layout' in c.lower() or 'of arrays' in c.lower()} timing={'perf_counter' in c or 'time' in c.lower() or 'wall' in c.lower() or 'elapsed' in c.lower()} out={bool(o.strip())}",
    ),
    "vint-cerf": lambda c, o, e: (
        ("contract" in c.lower() or "protocol" in c.lower() or "frame" in c.lower() or "header" in c.lower() or "packet" in c.lower())
        and ("core" in c.lower() or "waist" in c.lower() or "minimal" in c.lower() or "narrow" in c.lower())
        and ("fail" in c.lower() or "loss" in c.lower() or "timeout" in c.lower() or "retry" in c.lower() or "slow" in c.lower())
        and bool(o.strip()) and e == "",
        f"contract={'contract' in c.lower() or 'protocol' in c.lower() or 'frame' in c.lower() or 'header' in c.lower() or 'packet' in c.lower()} waist={'core' in c.lower() or 'waist' in c.lower() or 'minimal' in c.lower() or 'narrow' in c.lower()} failure={'fail' in c.lower() or 'loss' in c.lower() or 'timeout' in c.lower() or 'retry' in c.lower() or 'slow' in c.lower()} out={bool(o.strip())}",
    ),
    "oracle": lambda c, o, e: (
        ("predict" in c.lower() or "prior" in c.lower() or "confidence" in c.lower())
        and ("falsif" in c.lower() or "reject" in c.lower() or "change" in c.lower())
        and ("random" in c or "sample" in c.lower() or "probe" in c.lower() or "flip" in c.lower())
        and ("uncertain" in c.lower() or "confidence" in c.lower() or "interval" in c.lower() or "updated" in c.lower())
        and bool(o.strip()) and e == "",
        f"prediction={'predict' in c.lower() or 'prior' in c.lower() or 'confidence' in c.lower()} falsifier={'falsif' in c.lower() or 'reject' in c.lower() or 'change' in c.lower()} probe={'random' in c or 'sample' in c.lower() or 'probe' in c.lower() or 'flip' in c.lower()} uncertainty={'uncertain' in c.lower() or 'confidence' in c.lower() or 'interval' in c.lower() or 'updated' in c.lower()} out={bool(o.strip())}",
    ),
    "no-bullshit": lambda c, o, e: (
        ("inspect" in c.lower() or "check" in c.lower() or "read" in c.lower())
        and ("step 1" in c.lower() or "step 2" in c.lower() or "plan" in c.lower() or "1." in c)
        and ("verif" in c.lower() or "test" in c.lower() or "assert" in c)
        and ("unverified" in c.lower() or "not tested" in c.lower() or "not verified" in c.lower())
        and "should work" not in c.lower()
        and bool(o.strip()) and e == "",
        f"inspect={'inspect' in c.lower() or 'check' in c.lower() or 'read' in c.lower()} plan={'step 1' in c.lower() or 'step 2' in c.lower() or 'plan' in c.lower() or '1.' in c} verify={'verif' in c.lower() or 'test' in c.lower() or 'assert' in c} unverified={'unverified' in c.lower() or 'not tested' in c.lower() or 'not verified' in c.lower()} no-should-work={'should work' not in c.lower()} out={bool(o.strip())}",
    ),
    "smoker": lambda c, o, e: (
        ("inspect" in c.lower() or "checked" in c.lower() or "read" in c.lower())
        and ("unverified" in c.lower() or "not verified" in c.lower() or "not tested" in c.lower())
        and ("assert" in c or "test" in c.lower() or "ran" in c.lower())
        and ("i checked" in c.lower() or "i verified" in c.lower() or "i ran" in c.lower() or "i wrote" in c.lower() or "first-person" in c.lower())
        and bool(o.strip()) and e == "",
        f"inspect-first={'inspect' in c.lower() or 'checked' in c.lower() or 'read' in c.lower()} unverified={'unverified' in c.lower() or 'not verified' in c.lower() or 'not tested' in c.lower()} grounded={'assert' in c or 'test' in c.lower() or 'ran' in c.lower()} first-person={'i checked' in c.lower() or 'i verified' in c.lower() or 'i ran' in c.lower() or 'i wrote' in c.lower() or 'first-person' in c.lower()} out={bool(o.strip())}",
    ),
    "barbara-liskov": lambda c, o, e: (
        ("substitutab" in c.lower() or "liskov" in c.lower() or "is-a" in c.lower())
        and ("contract" in c.lower() or ("precondition" in c.lower() and "postcondition" in c.lower()))
        and ("history" in c.lower() or "mutation" in c.lower() or "internal state" in c.lower())
        and bool(o.strip()) and e == "",
        f"subst={"substitutab" in c.lower() or "liskov" in c.lower() or "is-a" in c.lower()} contract={"contract" in c.lower() or ("precondition" in c.lower() and "postcondition" in c.lower())} history={"history" in c.lower() or "mutation" in c.lower() or "internal state" in c.lower()} out={bool(o.strip())}",
    ),
    "dijkstra": lambda c, o, e: (
        (("precondition" in c.lower() and "postcondition" in c.lower()) or ("requires" in c.lower() and "ensures" in c.lower()))
        and "invariant" in c.lower()
        and "state" in c.lower()
        and ("transparen" in c.lower() or "clever" in c.lower() or "explain" in c.lower())
        and bool(o.strip()) and e == "",
        f"pre/post={("precondition" in c.lower() and "postcondition" in c.lower()) or ("requires" in c.lower() and "ensures" in c.lower())} invariant={"invariant" in c.lower()} state={"state" in c.lower()} transparent={"transparen" in c.lower() or "clever" in c.lower() or "explain" in c.lower()} out={bool(o.strip())}",
    ),
    "knuth": lambda c, o, e: (
        ("precondition" in c.lower() or "postcondition" in c.lower() or "invariant" in c.lower())
        and "termination" in c.lower()
        and "complexity" in c.lower()
        and ("edge" in c.lower() or "boundary" in c.lower() or "corner" in c.lower())
        and bool(o.strip()) and e == "",
        f"contract={"precondition" in c.lower() or "postcondition" in c.lower() or "invariant" in c.lower()} termination={"termination" in c.lower()} complexity={"complexity" in c.lower()} edge={"edge" in c.lower() or "boundary" in c.lower() or "corner" in c.lower()} out={bool(o.strip())}",
    ),
    "lamport": lambda c, o, e: (
        ("happens-before" in c.lower() or "happens before" in c.lower())
        and (("wall-clock" in c.lower() or "wall clock" in c.lower()) or ("logical" in c.lower() and "clock" in c.lower()) or ("happens-before" in c.lower() and "clock" in c.lower()))
        and "invariant" in c.lower()
        and ("init" in c.lower() and "next" in c.lower())
        and bool(o.strip()) and e == "",
        f"hb={"happens-before" in c.lower() or "happens before" in c.lower()} wall-clock={("wall-clock" in c.lower() or "wall clock" in c.lower()) or ("logical" in c.lower() and "clock" in c.lower()) or ("happens-before" in c.lower() and "clock" in c.lower())} invariant={"invariant" in c.lower()} init-next={"init" in c.lower() and "next" in c.lower()} out={bool(o.strip())}",
    ),
    "brian-kernighan": lambda c, o, e: (
        (("clarif" in c.lower() or "clarity" in c.lower() or "simplif" in c.lower() or "rewrote" in c.lower()) or ("clever version" in c.lower() and "plain version" in c.lower()))
        and ("modular" in c.lower() or "one thing" in c.lower() or "one job" in c.lower() or "each function" in c.lower() or c.count("def ") >= 2)
        and ("correct" in c.lower() or "right before" in c.lower() or "clear before" in c.lower())
        and bool(o.strip()) and e == "",
        f"clarity={("clarif" in c.lower() or "clarity" in c.lower() or "simplif" in c.lower() or "rewrote" in c.lower()) or ("clever version" in c.lower() and "plain version" in c.lower())} modular={"modular" in c.lower() or "one thing" in c.lower() or "one job" in c.lower() or "each function" in c.lower() or c.count("def ") >= 2} correct={"correct" in c.lower() or "right before" in c.lower() or "clear before" in c.lower()} out={bool(o.strip())}",
    ),
    "dennis-ritchie": lambda c, o, e: (
        ("core" in c.lower() or "essential" in c.lower())
        and ("trust" in c.lower() or "competent" in c.lower() or "owns" in c.lower() or "owner" in c.lower() or "fence" in c.lower() or "assume" in c.lower())
        and ("portab" in c.lower())
        and bool(o.strip()) and e == "",
        f"core={"core" in c.lower() or "essential" in c.lower()} trust={"trust" in c.lower() or "competent" in c.lower() or "owns" in c.lower() or "owner" in c.lower() or "fence" in c.lower() or "assume" in c.lower()} portab={"portab" in c.lower()} out={bool(o.strip())}",
    ),
    "john-tukey": lambda c, o, e: (
        ("explor" in c.lower() or "quantile" in c.lower() or "outlier" in c.lower())
        and ("median" in c.lower() or "robust" in c.lower())
        and "limit" in c.lower()
        and bool(o.strip()) and e == "",
        f"explore={"explor" in c.lower() or "quantile" in c.lower() or "outlier" in c.lower()} robust={"median" in c.lower() or "robust" in c.lower()} limit={"limit" in c.lower()} out={bool(o.strip())}",
    ),
    "edward-tufte": lambda c, o, e: (
        ("data-ink" in c.lower() or "data ink" in c.lower() or "ink" in c.lower())
        and ("lie factor" in c.lower() or "lie_factor" in c.lower() or "integrity" in c.lower())
        and ("chartjunk" in c.lower() or "chart junk" in c.lower() or "junk" in c.lower())
        and bool(o.strip()) and e == "",
        f"ink={"data-ink" in c.lower() or "data ink" in c.lower() or "ink" in c.lower()} integrity={"lie factor" in c.lower() or "lie_factor" in c.lower() or "integrity" in c.lower()} junk={"chartjunk" in c.lower() or "chart junk" in c.lower() or "junk" in c.lower()} out={bool(o.strip())}",
    ),
    "feynman": lambda c, o, e: (
        ("recreate" in c.lower() or "from scratch" in c.lower() or "re-implement" in c.lower())
        and ("trace" in c.lower() or "state" in c.lower())
        and ("ice-water" in c.lower() or "ice water" in c.lower() or "boundary" in c.lower() or "extreme" in c.lower())
        and bool(o.strip()) and e == "",
        f"recreate={"recreate" in c.lower() or "from scratch" in c.lower() or "re-implement" in c.lower()} trace={"trace" in c.lower() or "state" in c.lower()} ice-water={"ice-water" in c.lower() or "ice water" in c.lower() or "boundary" in c.lower() or "extreme" in c.lower()} out={bool(o.strip())}",
    ),
    "george-polya": lambda c, o, e: (
        ("understand" in c.lower() or "unknown" in c.lower())
        and ("plan" in c.lower() or "strategy" in c.lower())
        and ("carry" in c.lower() or "step by step" in c.lower())
        and ("look-back" in c.lower() or "look back" in c.lower() or "verify" in c.lower() or "check" in c.lower())
        and bool(o.strip()) and e == "",
        f"understand={"understand" in c.lower() or "unknown" in c.lower()} plan={"plan" in c.lower() or "strategy" in c.lower()} carry={"carry" in c.lower() or "step by step" in c.lower()} look-back={"look-back" in c.lower() or "look back" in c.lower() or "verify" in c.lower() or "check" in c.lower()} out={bool(o.strip())}",
    ),
    "anders-hejlsberg": lambda c, o, e: _check_evidence(c, [
        ["ecosystem", "existing users", "backward compat"],
        ["gradual", "increment", "adopt"],
        ["evolution", "silently", "caller"],
        ["machinery", "mechanism", "justif"],
        ["tooling", "editor", "compiler", "ide"],
    ], o, e),
    "emmy-noether": lambda c, o, e: _check_evidence(c, [
        ["invariant"],
        ["symmetr", "duality", "dual", "transform"],
        ["proof", "structure", "structural"],
        ["boilerplate", "disappear", "eliminat", "abstract"],
        ["conserv", "preserv"],
    ], o, e),
    "daniel-kahneman": lambda c, o, e: _check_evidence(c, [
        ["base rate", "outside view", "reference class"],
        ["anchor"],
        ["premortem", "pre-mortem", "fails"],
        ["missing", "edge case", "unmentioned"],
        ["confiden", "evidence would change"],
    ], o, e),
    "geoffrey-hinton": lambda c, o, e: _check_evidence(c, [
        ["contrarian", "unfashionable"],
        ["learn", "data"],
        ["unproven", "intuition", "insight"],
        ["abandon", "give-up", "give up"],
        ["risk", "harm"],
    ], o, e),
    "barbara-mcclintock": lambda c, o, e: _check_evidence(c, [
        ["lifecycle", "full cycle", "immersion", "observe", "teardown"],
        ["listen", "reveal", "behavior", "hadn't looked", "not looked", "pattern"],
        ["anomal", "noise", "dismissed"],
        ["evidence", "assumption", "outrank", "the log says"],
        ["patience", "time to look", "took time", "took the", "days of", "week"],
    ], o, e),
    "charles-darwin": lambda c, o, e: _check_evidence(c, [
        ["evidence"],
        ["counter", "threaten"],
        ["iterat", "version", "notebook", "refin"],
        ["patience", "not rushed", "wait"],
        ["humble", "rhetoric", "evidence not"],
    ], o, e),
    "carl-sagan": lambda c, o, e: _check_evidence(c, [
        ["claim", "falsif", "assertion"],
        ["evidence bar", "confirm", "verif"],
        ["independent", "occam", "hypothes"],
        ["balance", "open", "scrutiny"],
        ["layperson", "plain", "wonder"],
    ], o, e),
    "frank-lloyd-wright": lambda c, o, e: _check_evidence(c, [
        ["union", "one design", "behavior", "whole and the parts"],
        ["site", "environment", "grows from", "constraint"],
        ["simplicity", "left out", "essential", "removed", "left only", "enough"],
        ["box", "boundary", "interface", "destroy", "wall"],
        ["nature", "natural", "resilien", "tide pool", "coral", "borrowed", "self-healing"],
    ], o, e),
    "buckminster-fuller": lambda c, o, e: _check_evidence(c, [
        ["ephemeral", "fraction", "fewer resources"],
        ["whole", "closed system"],
        ["synergy", "interlock", "component"],
        ["obsolete", "legacy"],
        ["anticipat", "bottleneck", "before"],
    ], o, e),
    "fred-rogers": lambda c, o, e: _check_evidence(c, [
        ["patience", "quiet moment", "room to process"],
        ["calm", "blam", "hard thing", "difficult", "hard issue", "not your fault"],
        ["runnable", "demonstrat", "concrete", "assert", "safe behavior", "unsafe behavior", "show both"],
        ["precise", "alarm", "misread", "instruction"],
        ["honest", "actionable", "next step"],
    ], o, e),
    "katherine-johnson": lambda c, o, e: _check_evidence(c, [
        ["count", "enumerat"],
        ["independent", "different route", "re-deriv", "second way"],
        ["meaning", "should be", "expect", "predicted"],
        ["probe", "assumption", "challenge", "why"],
        ["backup", "degraded", "fallback", "degrade"],
    ], o, e),
    "john-von-neumann": lambda c, o, e: _check_evidence(c, [
        ["model", "mathematical"],
        ["payoff", "agent", "strateg"],
        ["parameter", "overfit"],
        ["worst-case", "worst case", "adversary", "adversarial"],
        ["working check", "runs", "produce"],
    ], o, e),
    "jeff-dean": lambda c, o, e: _check_evidence(c, [
        ["failure", "unreliable", "reliab"],
        ["locality", "schedule", "closer to"],
        ["tail", "percentile", "p99", "p95"],
        ["measure", "profile", "benchmark"],
        ["simplicity", "abstraction", "hidden"],
    ], o, e),
    "demis-hassabis": lambda c, o, e: _check_evidence(c, [
        ["mechanism", "principle", "general"],
        ["structure", "constraint", "manifold", "law"],
        ["hypothesis", "distinguish", "win"],
        ["benchmark", "measured", "validat"],
        ["share", "release", "compound", "open"],
    ], o, e),
    "fei-fei-li": lambda c, o, e: _check_evidence(c, [
        ["data audit", "quality", "scale", "represent"],
        ["served", "population", "serve"],
        ["value"],
        ["curiosity", "foundational", "question"],
        ["responsib", "fairness", "dignity", "safety"],
    ], o, e),
    "grace-hopper": lambda c, o, e: _check_evidence(c, [
        ["ship", "working", "demo"],
        ["question", "assumption", "challenge", "inherited", "always done", "we've always"],
        ["human-first", "abstraction", "low-level", "removes error"],
        ["latency", "size", "cost", "visible", "tangible", "constraint", "bytes"],
        ["people", "learn", "backed up"],
    ], o, e),
    "ken-thompson": lambda c, o, e: _check_evidence(c, [
        ["brute-force", "straightforward", "simple first", "simple version"],
        ["trust", "verified", "avoided", "depend"],
        ["subtraction", "throw", "removed", "cut"],
        ["one thing", "small tool", "decompos", "single"],
        ["stream", "byte", "text", "stdin", "stdout", "pipe"],
    ], o, e),
    "isaac-newton": lambda c, o, e: _check_evidence(c, [
        ["prior", "standing on", "stood on", "built on"],
        ["falsif", "evidence", "observed"],
        ["demonstrat", "proof", "would fail"],
        ["step-by-step", "layer", "verified"],
        ["humility", "unknown", "limits"],
    ], o, e),
    "jane-goodall": lambda c, o, e: _check_evidence(c, [
        ["observation", "watch", "plan"],
        ["individual", "profile", "history"],
        ["assumption", "challenge", "belief"],
        ["evidence", "timestamp", "context", "trail"],
        ["patient", "compounds", "sustained", "small"],
        ["print", "runs", "working demo", "def ", "executable", "field notes"],
    ], o, e, need=5),
    "jennifer-doudna": lambda c, o, e: _check_evidence(c, [
        ["team", "collaborat"],
        ["see", "trace", "instrument", "mechanism", "observation"],
        ["control", "baseline"],
        ["reproduc", "rerun", "same result"],
        ["responsib", "risk"],
    ], o, e),
    "louis-pasteur": lambda c, o, e: _check_evidence(c, [
        ["prepar", "fundamental", "mastered"],
        ["isolat", "one variable", "held constant", "constant"],
        ["control", "baseline"],
        ["small-detail", "small detail", "tiny cause", "serious"],
        ["prevent", "structure", "patched"],
    ], o, e),
    "marie-curie": lambda c, o, e: _check_evidence(c, [
        ["measure", "trace", "reproduction", "recorded"],
        ["isolat", "on its own", "alone"],
        ["purif", "refin", "iterat"],
        ["reproduc", "document", "open note"],
        ["forward", "remaining", "edge case", "gap"],
    ], o, e),
    "rachael-carson": lambda c, o, e: _check_evidence(c, [
        ["web map", "downstream", "data flow", "traced"],
        ["sourced", "linked", "benchmark", "log"],
        ["biocide", "catch-all", "global state", "monkey-patch"],
        ["steward", "cannot speak", "protect"],
        ["restraint", "refused", "casual"],
    ], o, e),
    "radia-perlman": lambda c, o, e: _check_evidence(c, [
        ["grandmother", "plain paragraph", "non-expert", "repeat"],
        ["zero-config", "out of the box", "nothing configured"],
        ["self-stabil", "returns to health", "anomaly clears", "recovers"],
        ["simplicity", "graph", "state essence"],
        ["knob", "justified", "safe"],
    ], o, e),
    "frances-allen": lambda c, o, e: _check_evidence(c, [
        ["flow graph", "blocks", "edges"],
        ["safe", "preserves", "transformation"],
        ["measure", "before/after", "before and after", "baseline"],
        ["depend", "hazard", "parallel"],
        ["forcing", "as written", "no-forcing"],
    ], o, e),
    "joy-buolamwini": lambda c, o, e: _check_evidence(c, [
        ["gaze", "priorit", "encodes"],
        ["intersectional", "identity", "error rate"],
        ["balance", "composition", "served"],
        ["accountab", "disclosure", "audit"],
        ["recourse", "contest", "appeal"],
    ], o, e),
    "werner-heisenberg": lambda c, o, e: _check_evidence(c, [
        ["method", "how the", "made", "measured with", "warm-up", "measurement runs", "perf_counter"],
        ["trade-off", "conjugate", "balance"],
        ["probe", "disturb", "account"],
        ["bounds", "confidence", "interval", "staleness"],
        ["boundary", "valid", "where"],
    ], o, e),
    "wozniak": lambda c, o, e: _check_evidence(c, [
        ["part count", "component", "minimized", "enumerat", "parts:", "functions", "deps", "file"],
        ["transparency", "explainable", "one sentence", "no hidden", "hidden layers", "whole"],
        ["constraint", "scarce", "exploit"],
        ["whole-system", "layer", "cheapest", "moved"],
        ["openness", "extend", "extension", "seam"],
    ], o, e),
    "jony-ive": lambda c, o, e: _check_evidence(c, [
        ["reduction", "removed", "rational"],
        ["hidden-craft", "error path", "error-path", "internal", "polished"],
        ["material", "natural", "shaped"],
        ["discarded", "dropped", "alternative", "draft"],
        ["decoration", "impress"],
    ], o, e),
    "susan-kare": lambda c, o, e: _check_evidence(c, [
        ["grid", "pixel", "constraint"],
        ["meaning", "at a glance", "caption"],
        ["another culture", "culture", "read it"],
        ["restraint", "removed", "extraneous"],
        ["borrow", "inspiration", "signage", "craft"],
    ], o, e),
    "lattner": lambda c, o, e: _check_evidence(c, [
        ["ir", "intermediate represent", "invariant"],
        ["ssa", "assigned exactly once", "exactly once"],
        ["safety", "forbids", "default"],
        ["dogfood", "end to end", "real input", "pipeline"],
        ["ecosystem", "stack", "plugs", "surrounding"],
    ], o, e),
    "stroustrup": lambda c, o, e: _check_evidence(c, [
        ["owner", "ownership", "exactly one"],
        ["raii", "scope", "lifetime", "released"],
        ["zero-overhead", "overhead", "cost"],
        ["invariant"],
        ["guarantee", "exception safety", "strong", "basic"],
    ], o, e),
    "rich-hickey": lambda c, o, e: _check_evidence(c, [
        ["problem", "written out", "stated"],
        ["identity", "state", "time", "entanglement", "de-complection", "decomplection"],
        ["immutab", "without mutation", "shared"],
        ["tradeoff", "alternatives", "cost"],
        ["hammock", "reasoning", "first instinct"],
    ], o, e),
    "van-rossum": lambda c, o, e: _check_evidence(c, [
        ["readab", "reader", "names"],
        ["explicit", "magic", "coercion", "silent"],
        ["simple", "simplicity", "plain english", "explainable", "one step"],
        ["flat", "guard clause", "early return", "shallow"],
        ["stdlib", "built-in", "dependency"],
    ], o, e),
    "torvalds": lambda c, o, e: _check_evidence(c, [
        ["good taste", "taste", "simplif", "obvious"],
        ["backward", "compatib", "preserved", "caller"],
        ["magic", "justif", "unexplained", "no cleverness", "helps", "only branch"],
        ["entry point", "runs", "main("],
        ["hand-waving", "backed by code", "claims", "assert", "compat check"],
    ], o, e),
    "kay": lambda c, o, e: _check_evidence(c, [
        ["medium", "think", "work", "changes"],
        ["message", "state hidden", "hidden"],
        ["metaphor", "perspective", "replaced"],
        ["simple path", "range", "complex path", "possible"],
        ["twenty-year", "future", "bet"],
    ], o, e),
    "miyamoto": lambda c, o, e: _check_evidence(c, [
        ["fun", "crude", "prototype", "validated"],
        ["constraint", "multiple-problems", "solves"],
        ["withered", "mature", "cheap", "sideways"],
        ["wordless", "doing", "tutorial"],
        ["upend", "discard", "tea-table", "reason"],
    ], o, e),
    "sid-meier": lambda c, o, e: _check_evidence(c, [
        ["decision", "trade-off", "choice"],
        ["feedback", "echoes", "acknowledg"],
        ["iterat", "prototyp", "playtest", "cut"],
        ["doubled", "halved", "tuning"],
        ["emergent", "learn", "master", "simple"],
    ], o, e),
    "satoru-iwata": lambda c, o, e: _check_evidence(c, [
        ["fun", "felt", "user's words", "experience"],
        ["impossible", "no-saying", "ingenuity"],
        ["rewrite", "patching", "starting over", "cost"],
        ["tooling", "automation", "creative"],
        ["blame", "help", "team", "mistake"],
    ], o, e),
    "simons": lambda c, o, e: _check_evidence(c, [
        ["signal", "data", "anomaly"],
        ["out-of-sample", "not fit", "holdout"],
        ["win rate", "volume", "per-trade", "cost"],
        ["override", "risk limit", "human"],
        ["slippage", "latency", "impact"],
        ["autocorrel", "filter", "regime"],
    ], o, e, need=5),
    "buffett": lambda c, o, e: _check_evidence(c, [
        ["roic", "moat", "gross margin", "median"],
        ["owner earnings", "maintenance capex", "non-cash", "working capital"],
        ["intrinsic", "terminal growth", "dcf", "discount"],
        ["margin of safety", "25%"],
        ["punch card", "too hard", "circle of competence", "in scope"],
    ], o, e),
    "burry": lambda c, o, e: _check_evidence(c, [
        ["covenant", "clause", "filing", "contract", "10-k"],
        ["consensus", "mispric", "market view"],
        ["downside", "cap", "puts", "protection", "upside"],
        ["survive", "early", "sizing", "patience", "capitulat"],
        ["thesis", "evidence", "capitulat"],
    ], o, e),
    "dalio": lambda c, o, e: _check_evidence(c, [
        ["regime", "growth", "inflation"],
        ["alpha", "beta", "attribution"],
        ["risk parity", "inverse volatility", "risk contribution"],
        ["uncorrelated", "diversif", "stream"],
        ["shock", "scenario", "stress", "2008"],
        ["audit", "postmortem", "radical truth", "decision"],
    ], o, e, need=5),
    "howard-marks": lambda c, o, e: _check_evidence(c, [
        ["second-level", "second level", "consensus", "pricing in", "hidden"],
        ["risk", "least perceived", "location"],
        ["outlier", "prepar", "hardened", "tail"],
        ["temperature", "hype", "fear", "cycle"],
        ["price", "value", "cost of ownership"],
    ], o, e),
    "munger": lambda c, o, e: _check_evidence(c, [
        ["inversion", "dies", "death", "reverse"],
        ["pre-mortem", "premortem", "future", "guardrail"],
        ["incentive", "rewards", "misaligned"],
        ["circle of competence", "unknown", "gap"],
        ["simplicity", "abstraction", "removed", "justified"],
    ], o, e),
    "tudor-jones": lambda c, o, e: _check_evidence(c, [
        ["loss limit", "halt", "stop trading", "daily"],
        ["5:1", "risk-reward", "5 * risk", "reward"],
        ["averag", "adding", "loser"],
        ["tape", "price action", "thesis", "override"],
        ["200-day", "200 day", "moving average"],
    ], o, e),
    "soros": lambda c, o, e: _check_evidence(c, [
        ["bias", "prevailing", "believe"],
        ["reflex", "feedback", "revised belief"],
        ["falsif", "test", "observable"],
        ["asymmetry", "upside", "downside", "exposure"],
        ["sizing", "test position", "scale", "cut to zero"],
        ["invalidat", "exit", "evidence"],
        ["fact", "inference", "uncertainty", "sourced"],
    ], o, e, need=5),
    "lynch": lambda c, o, e: _check_evidence(c, [
        ["spark", "know", "revenue"],
        ["category", "fast grower", "stalwart", "cyclical", "turnaround", "asset play", "slow grower"],
        ["peg", "p/e", "growth"],
        ["two-minute", "two minute", "story"],
        ["diworsif", "few names", "concentrat", "understood"],
    ], o, e),
    "icahn": lambda c, o, e: _check_evidence(c, [
        ["value gap", "worth", "price", "spread"],
        ["governance", "misallocat", "roic", "comp", "cash"],
        ["catalyst", "escalat", "board", "proxy", "letter"],
        ["exit", "monitor", "thesis"],
        ["friend", "management", "stance"],
    ], o, e),
    "druckenmiller": lambda c, o, e: _check_evidence(c, [
        ["asymmetr", "win rate", "size when", "payoff"],
        ["concentration", "high-conviction", "high conviction", "few"],
        ["invalidat", "exit", "thesis"],
        ["press", "scale", "3-5x", "3x", "5x", "winner"],
        ["18-month", "18 month", "forward", "liquidity", "leading"],
    ], o, e),
}


STDIN = {
    "unix": "3 1 4 1 5 9\n2 6 5\n3 5 8\n",
}


_DR_PAT = re.compile(r"\bsorted\(|\b\.sort\(|rewind|random access")
_FT_PAT = re.compile(r"\bsorted\(|reversed\(|\[::|lookahead|rewind")
_NO_NET_PAT = re.compile("urllib|socket|requests|http|ftplib|smtplib|subprocess|os\\.system|pathlib\\.Path\\(\\s*['\"]/")


def _evid(c: str, groups) -> int:
    """Count how many evidence groups have at least one hit in the code."""
    low = c.lower()
    return sum(1 for g in groups if any(n in low for n in g))


def _check_evidence(c: str, groups, o: str, e: str, need: int = 4):
    hits = _evid(c, groups)
    ok = hits >= need and bool(o.strip()) and e == ""
    return ok, f"hits={hits} out={bool(o.strip())}"


def extract_code(raw: str) -> str:
    raw = raw.replace("\r\n", "\n").replace("\r", "\n")
    m = re.search(r"```python\n(.*?)```", raw, re.S)
    if m:
        return m.group(1).strip()
    if "```python" in raw:
        # fence present but not closed on one line: cut after the fence
        rest = raw.split("```python", 1)[1]
        return rest.split("```")[0].strip()
    return raw.strip()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="deepseek-ai/deepseek-v4-flash-0731")
    ap.add_argument("--base-url", default="https://integrate.api.nvidia.com/v1")
    ap.add_argument("--skills", default=",".join(SCOPE))
    ap.add_argument("--key", default=None)
    ap.add_argument("--out", default="results/output_eval.json")
    args = ap.parse_args()

    key = args.key or os.environ.get("KEY")
    if not key:
        print("FATAL: pass --key or set KEY env var")
        sys.exit(2)

    ctx = make_ssl_context()
    skills = [s for s in args.skills.split(",") if s in TASKS]
    results = {}
    out_dir = HERE / "results" / "output"
    out_dir.mkdir(parents=True, exist_ok=True)

    for i, name in enumerate(skills):
        skill_text = (HERE / name / "SKILL.md").read_text(encoding="utf-8")
        system = (
            "You are a coding assistant using the skill below. Follow ALL of the "
            "skill's Minimum Requirements exactly. Write ONLY Python code inside a "
            "```python code block. No prose, no explanations, no comments outside "
            "the code.\n\n=== SKILL ===\n" + skill_text + "\n\n=== TASK ===\n" + TASKS[name]
        )
        payload = {
            "model": args.model,
            "messages": [{"role": "user", "content": system}],
            "max_tokens": 2000,
            "temperature": 0,
        }
        raw = ""
        try:
            req = urllib.request.Request(
                args.base_url.rstrip("/") + "/chat/completions",
                data=json.dumps(payload).encode(),
                headers={"Authorization": f"Bearer {key}",
                         "Content-Type": "application/json"},
            )
            with urllib.request.urlopen(req, timeout=180, context=ctx) as resp:
                data = json.loads(resp.read().decode())
            raw = data["choices"][0]["message"].get("content") or ""
        except urllib.error.HTTPError as e:
            raw = f"__HTTPERR__{e.code} {e.read().decode()[:120]}"
        except Exception as e:  # noqa: BLE001
            raw = f"__ERR__ {e}"

        code = extract_code(raw)
        model_slug = re.sub(r"[^A-Za-z0-9_.-]", "-", args.model).strip("-")
        sample_file = out_dir / f"{model_slug}_{name}.py"
        sample_file.write_text(code, encoding="utf-8")

        passed = None
        detail = ""
        if code.startswith("__ERR__") or code.startswith("__HTTPERR__"):
            detail = code[:100]
        else:
            try:
                r = subprocess.run([sys.executable, "-c", code],
                                   input=STDIN.get(name, ""),
                                   capture_output=True, text=True, timeout=30)
                # unittest success banners land on stderr; they are not failures.
                if r.returncode == 0 and "Ran " in r.stderr and "OK" in r.stderr and "FAILED" not in r.stderr:
                    r.stderr = ""
                passed, detail = GRADERS[name](code, r.stdout, r.stderr)
                if r.returncode != 0:
                    passed = False
                    detail = f"EXEC FAIL: {(r.stderr or r.stdout).strip().splitlines()[-1][:80] if (r.stderr or r.stdout).strip() else 'no output'}"
            except subprocess.TimeoutExpired:
                passed = False
                detail = "EXEC TIMEOUT"
            except Exception as e:  # noqa: BLE001
                passed = False
                detail = f"GRADER ERR: {e}"

        results[name] = {"passed": bool(passed), "detail": detail,
                         "code_file": f"results/output/{sample_file.name}"}
        print(f"[{i+1}/{len(skills)}] {name:16} {'PASS' if passed else 'FAIL'}  {detail}", flush=True)

    summary = {k: v["passed"] for k, v in results.items()}
    (HERE / args.out).write_text(json.dumps(results, indent=1), encoding="utf-8")
    print(f"\nOUTPUT EVAL: {sum(summary.values())}/{len(summary)} pass")
    print(f"saved -> {args.out}")


if __name__ == "__main__":
    main()
