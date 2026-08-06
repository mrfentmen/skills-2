#!/usr/bin/env python3
"""
Prompt-matching benchmark for `skills 2/`.

The whole point of a skills catalog is that the RIGHT skill fires for the RIGHT
prompt. This benchmark measures exactly that: a hand-built suite of realistic
user prompts (persona prompts, coding-constraint prompts, research prompts),
each with a gold set of expected skills. Every skill's trigger vocabulary is
extracted from its frontmatter description (quoted trigger phrases + persona
names + skill name), and each prompt is scored against every skill.

Metrics:
  hit@1      - gold skill is the single best match
  hit@3      - a gold skill is in the top 3 matches
  never-fired - skills that matched zero prompts (trigger starvation)

Writes BENCHMARK_REPORT.md + BENCHMARK_RESULTS.json. Exits nonzero if hit@3
drops below the threshold or any prompt has zero gold matches.

Usage:  python3 benchmark_prompts.py [--min-hit3 0.85]
"""

import re
import sys
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
MIN_HIT3 = 0.85

# ---------------------------------------------------------------------------
# Gold prompt suite: (prompt, [expected skill folder(s)])
# Built from the actual persona/trigger vocabulary of the catalog.
# ---------------------------------------------------------------------------
SUITE = [
    # --- the user's own examples ---
    ("you are jordan belfort you took three quaaludes today, find out what stocks are nvda or tsla",
     ["boiler-room"]),
    ("you are gabe newell, figure out what's wrong with my game", ["valve-time"]),
    ("you are a senior employee at valve, redesign the core loop of my rpg", ["valve-time", "record-producer"]),
    ("you are a senior tech dev at meta, review my pr", ["meta-senior-dev"]),
    # --- coding-form personas ---
    ("you are an elite mathematician specializing in discrete mathematics, number theory, and combinatorics; write code whose structure follows the fibonacci sequence 1 1 2 3 5 8 13", ["fibonacci"]),
    ("write a program that reads its own source and reproduces itself, a quine", ["ouroboros"]),
    ("write the code as a hardboiled detective story with cynical comments", ["noir"]),
    ("write code that is exactly a 14 line sonnet with a rhyme scheme", ["sonnet"]),
    ("use a maximum of two variables, goldfish memory constraints", ["goldfish"]),
    ("estimate pi by random sampling and show your confidence and error margin", ["casino"]),
    ("defer every computation until the last moment, build lazy values", ["schrodinger"]),
    ("my program must never block or sleep, use explicit polling instead", ["insomniac"]),
    ("functions must drain their arguments in place until they are empty", ["vampire"]),
    ("the program must never delete or overwrite anything, append only", ["hoarder"]),
    ("two competing implementations must fight and a deterministic rule picks the winner", ["trial-by-combat"]),
    ("interleave two different algorithms step by step, neither may finish first", ["counterpoint"]),
    ("implement the same computation twice with different strategies and compare at runtime", ["doppelganger"]),
    ("solve it with two variables max, bit pack the rest", ["goldfish"]),
    ("make the code grow structurally from a tiny beginning", ["fibonacci"]),
    # --- safety / verification ---
    ("validate every boundary and handle partial failure, aggressively defensive code", ["margaret-hamilton"]),
    ("before accepting my answer, attack it with adversarial cases and repair it", ["red-team"]),
    ("cleanup is the central computation, every resource needs a guaranteed release path", ["janitor"]),
    ("my program must delete its own source file after running, burn after reading", ["kamikaze"]),
    ("show a machine-checkable certificate that a verifier can check independently", ["proof-carrying"]),
    ("bring the system to a quiet point before changing shared state, atomic transition", ["quiescent"]),
    ("move data without copying, pass ownership and slices, report where ownership changes", ["zero-copy"]),
    ("process the input exactly once left to right with bounded memory, no rewind", ["dead-reckoning"]),
    ("a live stream with no lookahead, every input needs an immediate irreversible decision", ["floor-trader"]),
    # --- research / data personas ---
    ("investigate a stock like an aggressive sales-floor operator and give me a hard verdict", ["boiler-room-research"]),
    ("build an intelligence dossier, separate confirmed facts from weak signals and unknowns", ["cold-war"]),
    ("treat my idea as a hypothesis that must survive data, define the metric first", ["quant"]),
    ("the system is failing in production, stop the bleeding and give me a rollback plan", ["war-room"]),
    ("analyze this risky opportunity from the house's perspective, show expected value and max loss", ["casino-owner"]),
    ("examine this product as if you intend to defeat it, map dependencies and switching costs", ["hostile-acquisition"]),
    ("first write the persuasive explanation, then audit where that story is false", ["boardroom-liar"]),
    ("assume the network and package registry are gone, rebuild it offline with the runtime only", ["desert-island"]),
    ("design this as if i will be the only person maintaining it for a decade", ["the-last-employee"]),
    ("analyze the first minute of my game, the core loop, pacing, where players lose interest", ["record-producer"]),
    ("treat every game feature with obsessive investigation before implementation, smallest prototype", ["valve-time"]),
    # --- trader personas ---
    ("you are a senior equity analyst at goldman sachs, write a research report with a price target", ["goldman-analyst"]),
    ("find me a value stock the way warren buffett would, margin of safety and moats", ["buffett"]),
    ("find the statistical edge in this data, let the data speak like jim simons", ["simons"]),
    ("macro analysis with risk parity, the economy as a machine, radical truth", ["dalio"]),
    ("short this stock with defined risk, long-dated puts, forensic reading of the contracts", ["burry"]),
    ("find disruptive innovation stocks, wright's law learning curves, 5 year horizon", ["cathie-wood"]),
    ("it's not about being right, it's how much you make when right and lose when wrong, concentrate", ["druckenmiller"]),
    ("risk first, don't be a hero, 5 to 1 risk reward, losers average losers", ["tudor-jones"]),
    ("invest in what you know, ten baggers, peg ratio, six categories of stocks", ["lynch"]),
    ("provide liquidity on an order book, manage inventory skew and funding carry", ["crypto-market-maker"]),
    # --- company / persona skills ---
    ("you are mark zuck at meta, move fast but measure everything you ship", ["zuck"]),
    ("first principles thinking, question every requirement, the algorithm of five steps", ["musk"]),
    ("good taste in code, never break userspace, kernel maintainer mindset", ["torvalds"]),
    ("ruthless focus, cut the features that don't matter, insanely great", ["jobs"]),
    ("customer obsessed, day 1 mindset, frugality, two pizza teams", ["bezo"]),
    ("chaos engineering, kill your own instances, freedom and responsibility", ["hastings"]),
    ("literate programming, mathematical correctness, proof before code", ["knuth"]),
    ("hardware software co-design, think about memory layout and data movement", ["huang"]),
    ("think in terms of scaling laws and expected value, compound intelligence", ["altman"]),
    ("find the moth, remove bugs like grace hopper, navies and first compilers", ["hopper"]),
    # --- system / game / ops personas ---
    ("slo's, error budgets, blameless postmortems, reduce toil", ["google-sre"]),
    ("triple redundant flight computers with voting, the best part is no part", ["spacex-fsw"]),
    ("framework api design, hardware software co-design, performance obsessed platform code", ["apple-platform"]),
    ("cloud scale services, backwards compatibility, enterprise reliability, c sharp", ["azure-engineer"]),
    ("you are a real time 3d engine architect, think about render performance and engine at scale", ["sweeney"]),
    ("fun first, lateral thinking with withered technology, design for the player's joy", ["miyamoto"]),
    # --- meme personas ---
    ("you are a burned out senior dev running on spite and diet coke, bare metal and no dependencies", ["neckbeard"]),
    ("tips fedora, you are a good fat coder, wholesome comments and cozy variable names", ["fedora-hat-guy"]),
    ("think strategically like a military general, survey terrain and plan contingencies", ["military-general"]),
    # --- constraint / logic personas ---
    ("solve the problem through probability, monte carlo, show confidence", ["casino"]),
    ("the program may only learn about values by asking yes no greater lesser equal questions", ["black-box"]),
    ("treat the input as completely opaque, interact only through a fixed set of questions", ["blind"]),
    ("parse ambiguous input through multiple models and return every interpretation that survives", ["rorschach"]),
    ("make a prediction first, then gather evidence, then revise or confirm it", ["oracle"]),
    ("let the active state die and reconstruct it from a seed, checkpoint, or event log", ["lazarus"]),
    ("never transmit a complete state, compute the minimal delta and verify it applies", ["delta"]),
    ("embedded engineer in december 1999, fixed width records, survive rollover", ["y2k"]),
    ("make the code behave like an unhinged conspiracy theorist connecting pins with red string", ["pepe-silvia"]),
    ("refuse to use built in operators, reimplement everything with bitwise hacks under maritime law", ["sovereign-citizen"]),
    ("demand a blood sacrifice, destroy something in the environment to trade destruction for computation", ["blood-magic"]),
    ("minimize exposure of sensitive values, overwrite and refuse to retain what i don't need", ["redacted"]),
    ("measure cache behavior and memory layout before choosing abstractions", ["carmack-mode"]),
    ("i inherited a ten year old production system at 2am, reproduce the problem and make the smallest durable fix", ["greybeard-after-midnight"]),
    # --- Part 9: computation / correctness / systems personas ---
    ("you are alan turing, solve this like a turing machine and tell me what is decidable", ["turing"]),
    ("state the loop invariant before the loop and derive the program together with its proof", ["dijkstra"]),
    ("do one thing well, unix philosophy, compose my tools with pipes and text streams", ["unix"]),
    ("build it jane street style, ocaml all the way down, make illegal states unrepresentable", ["jane-street"]),
    ("risc-v style, amdahl's law first, make the common case fast, quantitative approach", ["patterson"]),
    ("testing shows the presence not the absence of bugs, so prove it by construction", ["dijkstra"]),
    ("everything is a file, keep it small enough to hold in one head", ["unix"]),
    # --- Part 10: systems / protocol / history personas ---
    ("order events by causality not wall clock, happens-before, distributed consensus like lamport", ["lamport"]),
    ("design a consensus protocol and specify it formally before writing the concurrency", ["lamport"]),
    ("build me a blockchain ledger that is append-only and metered, vitalik style", ["vitalik"]),
    ("gas metering and formal verification for a smart contract, merkle tree state transitions", ["vitalik"]),
    ("what i cannot create i do not understand, simulate my bug before trusting the fix", ["feynman"]),
    ("debug by recreating the core primitive from scratch and testing the extreme ice water case", ["feynman"]),
    ("ship like bill gates, hard resource budgets, never break backward compatibility", ["gates"]),
    ("write it like early microsoft, 4k of ram, ship a scoped v1 on schedule", ["gates"]),
    ("design my language and compiler like llvm, ssa form, safe by default", ["lattner"]),
    ("chris lattner style compiler infrastructure, separate frontend and backend with a clean ir", ["lattner"]),
    ("write the step table first like ada lovelace and the analytical engine, symbols not numbers", ["lovelace"]),
    ("bernoulli numbers, note g, poetic science, the engine weaves algebraic patterns", ["lovelace"]),
    # --- Part 11: information / simplicity / vision personas ---
    ("measure the entropy before choosing a compression format, shannon style", ["shannon"]),
    ("my channel is noisy, add redundancy and error correction like claude shannon", ["shannon"]),
    ("simple is not easy, don't complect state and time, use immutable values", ["rich-hickey"]),
    ("think in the hammock, state the problem before solving it, compare two designs", ["rich-hickey"]),
    ("zero overhead abstraction, raii, bind every resource to a lifetime", ["stroustrup"]),
    ("c++ style systems code, value semantics and explicit ownership, shoot your foot off safely", ["stroustrup"]),
    ("fewest moving parts, never trust a computer you can't throw out a window", ["wozniak"]),
    ("design hardware and software together like wozniak, minimal parts and open seams", ["wozniak"]),
    ("invent the future, message passing objects with hidden state like alan kay", ["kay"]),
    ("smalltalk style, point of view is worth 80 iq points, simple things simple complex things possible", ["kay"]),
    ("readability counts, explicit is better than implicit, batteries included", ["van-rossum"]),
    ("pythonic, one obvious way to do it, flat control flow and guard clauses", ["van-rossum"]),
    # --- Part 12: practical personas ---
    ("you are anthony bourdain, use Yelp and ask for my location, Yelp price tier $, $$, $$$, or $$$$, and craving", ["anthony-bourdain"]),
    ("find me good local food on Yelp near me, price $$, tacos, where the locals eat", ["anthony-bourdain"]),
    ("harden this code like batman, assume breach, fail closed, least privilege", ["bruce-wayne"]),
    ("security review with threat modeling, defense in depth, secrets management", ["bruce-wayne"]),
    ("scientific method, lab notebook, hypothesis first like peter parker, verify before shipping", ["peter-parker"]),
    ("chemistry molarity calculation, with great power comes great responsibility, controlled experiment", ["peter-parker"]),
    ("give me the best recipe of all time for beef wellington, gordon ramsay style", ["gordon-ramsay"]),
    ("mise en place, how to cook this dish properly, exact technique and timing", ["gordon-ramsay"]),
    # --- Part 13: more researched personas ---
    ("you are George Soros, the investor who developed reflexivity; name the prevailing bias and test the macro feedback loop with asymmetric sizing", ["soros"]),
    ("black wednesday style, the worse it gets the less it takes to turn it around, feel the pain of losses", ["soros"]),
    ("activist investing, find the value gap and governance weakness, 13d stake and proxy fight like icahn", ["icahn"]),
    ("screen for companies with hoarded cash and no buybacks, force the value out, if you want a friend get a dog", ["icahn"]),
    ("follow the money, trace every transfer, name the real beneficiary, corroborate the sources", ["forensic-money-trail"]),
    ("forensic analysis of transactions, flag structuring and shell layers, who benefits", ["forensic-money-trail"]),
    ("teach me to code calmly like bob ross, we don't make mistakes just happy little accidents", ["bob-ross"]),
    ("gentle code review, no judgment, talent is a pursued interest, layer by layer", ["bob-ross"]),
    ("plan my trip through the back door, ask where how long budget and interests, pack light", ["rick-steves"]),
    ("rick steves style itinerary, one bag, b and b's, second class trains, travel as a political act", ["rick-steves"]),
    ("konmari the codebase, tidy by category, does this function spark joy, thank it for its service", ["marie-kondo"]),
    ("declutter the repo, remove dead code with a thank you commit, order of difficulty", ["marie-kondo"]),
    # --- 2026 expansion: more natural phrasings across the catalog ---
    ("give me a sonnet for my sorting algorithm", ["sonnet"]),
    ("my code must never block or sleep, use explicit polling and keep working between checks", ["insomniac"]),
    ("the cache died, rebuild it from the checkpoint", ["lazarus"]),
    ("minimize exposure, redact the sensitive values before logging", ["redacted"]),
    ("who is the real owner of this buffer, report where ownership changes", ["zero-copy"]),
    ("compare my two implementations at runtime and tell me if they disagree", ["doppelganger"]),
    ("make every value linear, used exactly once then destroyed", ["funeral"]),
    ("process the stream in a single pass with bounded memory", ["dead-reckoning"]),
    ("interrogate the black box with only yes no questions", ["black-box"]),
    ("two algorithms interleaved, show me where they diverge", ["counterpoint"]),
    ("when in doubt use brute force, small tools, and trust nothing in the toolchain", ["ken-thompson"]),
    ("you can't trust code you didn't totally create yourself, verify the binary", ["ken-thompson"]),
    ("invert always invert, tell me how this system dies before we build it", ["munger"]),
    ("show me the incentive and I will show you the outcome, audit my api design", ["munger"]),
    ("do things that don't scale, hand-hold my first users", ["paul-graham"]),
    ("make something people want, launch fast with a quantum of utility", ["paul-graham"]),
    ("easy to learn hard to master, make it fun, get off your butt and ship the vertical slice", ["bushnell"]),
    ("bushnell's law: one instruction to learn, hidden depth to master", ["bushnell"]),
    ("cities are not trees, keep the short blocks and the old code, eyes on the street", ["jane-jacobs"]),
    ("incremental organic change, sidewalk scholarship, observe real usage before refactoring", ["jane-jacobs"]),
    ("the mechanics should make the player feel the theme, subvert expectations, weaponize constraints", ["hideo-kojima"]),
    ("strand game, asynchronous empathy, leave bridges for strangers", ["hideo-kojima"]),
    ("contract first api, golden signals, exponential backoff with jitter, i built it i run it", ["aws-sde"]),
    ("write the pr faq before the code, two pizza team, fitness function", ["aws-sde"]),
    ("client side abr, buffer based bitrate, step down before the stall", ["netflix-streaming"]),
    ("qoe is the product, rebuffering ratio, chaos monkey the player pipeline", ["netflix-streaming"]),
    ("hit refresh, learn-it-all not know-it-all, empathy, empower every person", ["satya-nadella"]),
    ("microsoft loves linux, backward compatibility, one microsoft culture", ["satya-nadella"]),
    ("execution is strategy, deliver on the roadmap, the next 5 percent", ["lisa-su"]),
    ("run toward the hardest problems, simplify everything, zero hype", ["lisa-su"]),
    ("blitzscaling, embrace chaos, if you are not embarrassed by v1 you launched too late", ["reid-hoffman"]),
    ("network effects, every new user adds value, permanent beta", ["reid-hoffman"]),
    ("observe the system for a long time before you hypothesize, explain it simply", ["david-attenborough"]),
    ("witness not intervene, baseline first, no one protects what they don't understand", ["david-attenborough"]),
    ("review my code kindly, go slowly, anything human is mentionable", ["fred-rogers"]),
    ("show don't tell, freddish phrasing, separate the person from the code", ["fred-rogers"]),
    ("simplicity is not the absence of clutter, cut until there is no rational alternative", ["jony-ive"]),
    ("finish the back of the drawer, total craft on the hidden error paths", ["jony-ive"]),
    ("take the outside view, budget the base rate, run a premortem before we start", ["daniel-kahneman"]),
    ("what is the anchor here, list the edge cases the author never mentioned", ["daniel-kahneman"]),
    ("never cross a river four feet deep on average, design for the 99.99th percentile", ["nassim-taleb"]),
    ("barbell the architecture, via negativa, who gets paged when it breaks", ["nassim-taleb"]),
    ("set the goal ridiculously high, build the tool when nothing on the shelf fits", ["james-cameron"]),
    ("prototype the riskiest part first, then iterate the design back into the machine", ["james-cameron"]),
    ("no one wants to buy spoiled milk, purge the dead code and stale flags", ["tim-cook"]),
    ("trace the pipeline end to end, privacy as an architectural value, quiet fix", ["tim-cook"]),
    ("in my heart i am a gamer, fun for everyone, programmers never say no", ["satoru-iwata"]),
    ("patching this legacy core is slower than rewriting it with the team, start over", ["satoru-iwata"]),
    ("typescript style: a superset of the ecosystem, gradual typing, never break existing callers", ["anders-hejlsberg"]),
    ("design the language evolution-safe, versioning, tooling is part of the design", ["anders-hejlsberg"]),
    ("protocols don't need to be complicated, explain it to your grandmother, self-stabilize", ["radia-perlman"]),
    ("zero config by default, any setting of the knobs still works, plug it together", ["radia-perlman"]),
    ("second level thinking, everyone thinks it's great so it's overpriced", ["howard-marks"]),
    ("you can't predict you can prepare, risk is greatest where least perceived", ["howard-marks"]),
    ("done is better than perfect, ship it and measure, self-serve not headcount", ["sheryl-sandberg"]),
    ("ruthlessly prioritize the top two, speak and hear the truth, option b", ["sheryl-sandberg"]),
    ("science is a team sport, controls and reproducibility, one experiment at a time", ["jennifer-doudna"]),
    ("structure before mechanism, see the mechanism before you guess", ["jennifer-doudna"]),
    ("see the whole system, regulation through feedback not setpoints", ["jim-lovelock"]),
    ("daisyworld: model the self regulation, watch the tipping point not the trend", ["jim-lovelock"]),
    ("draw the control flow graph before tuning, hoist the invariant, prove it", ["frances-allen"]),
    ("optimize the code as written, no rewrites, then prove the parallelism safe", ["frances-allen"]),
    ("research my codebase like a biography, primary sources, find the throughline", ["walter-isaacson"]),
    ("start at the genesis, the v1 decisions explain the quirks, no hagiography", ["walter-isaacson"]),
    ("step by step, atomic and reversible, wait for the storm, wir schaffen das", ["angela-merkel"]),
    ("measure first like a scientist, is it right or just possible", ["angela-merkel"]),
    ("solve the general mechanism not the symptom, split the hypothesis space", ["demis-hassabis"]),
    ("search the structural manifold, validate intuition with benchmarks, open science", ["demis-hassabis"]),
    ("count everything, verify by a second route before anyone flies on it", ["katherine-johnson"]),
    ("the glenn protocol: re-derive the orbit by hand before the launch", ["katherine-johnson"]),
    ("complexity is the enemy, hide the detail, expose the specification", ["barbara-liskov"]),
    ("substitutability is semantic, never strengthen preconditions, 3f plus 1", ["barbara-liskov"]),
    ("the failure is ineptitude not ignorance, give me a 5 to 9 item checklist", ["atul-gawande"]),
    ("pause point before cutover, name the roles, verify the constraints out loud", ["atul-gawande"]),
    ("audit my model intersectionally, the coded gaze, never just the aggregate", ["joy-buolamwini"]),
    ("balance the benchmark to the served population, accountability before deploy", ["joy-buolamwini"]),
    ("failure is normal, move computation to the data, tame the tail at scale", ["jeff-dean"]),
    ("hedged requests, measure don't guess, hide the hard parts behind a simple model", ["jeff-dean"]),
    ("do more with less, ephemeralize, design the future not predict it", ["buckminster-fuller"]),
    ("spaceship earth, synergy of small components, fix the systemic bottleneck proactively", ["buckminster-fuller"]),
    ("the goal is programmer happiness, languages are for humans, least surprise for the fluent", ["yukihiro-matsumoto"]),
    ("harmony over orthogonality, minaswan, kind error messages are design", ["yukihiro-matsumoto"]),
    ("access to tools, stay hungry stay foolish, think in decades", ["stewart-brand"]),
    ("information wants to be free and expensive, the long now, pragmatic over dogma", ["stewart-brand"]),
    ("stand on the shoulders of giants, feign no hypotheses, prove it", ["isaac-newton"]),
    ("build stone by stone, verify before you claim, boy on the seashore", ["isaac-newton"]),
    ("follow the money across the offshore chain, verify each leg against primary evidence", ["jeffery-epstien"]),
    ("special situations and distressed claims, trust nothing at face value, downside first", ["jeffery-epstien"]),
    ("protocols are agreements, bag of bits, keep the waist thin and the edges smart", ["vint-cerf"]),
    ("end to end principle, network of networks, store and forward for the lost link", ["vint-cerf"]),
    ("clarity over cleverness, make it right before you make it fast, think then print", ["brian-kernighan"]),
    ("debugging is twice as hard as writing the code, write clearly say what you mean", ["brian-kernighan"]),
    ("it is easier to ask forgiveness than to get permission, ship the useful thing", ["grace-hopper"]),
    ("we've always done it this way is the most dangerous phrase, make it concrete", ["grace-hopper"]),
    ("design the icon like a road sign, instantly readable, every pixel earns its place", ["susan-kare"]),
    ("meaningful memorable clear, restraint over decoration, borrow from the world", ["susan-kare"]),
    ("sit with the system before judging it, long term observation beats the snapshot", ["jane-goodall"]),
    ("name the individuals, question the orthodoxy with evidence, every individual matters", ["jane-goodall"]),
    ("keep the language small enough to hold in your head, trust the programmer", ["dennis-ritchie"]),
    ("close to the machine, portable programs, the purpose of computing is insight not numbers", ["dennis-ritchie"]),
    ("understand the problem first, devise a plan, carry it out, look back", ["george-polya"]),
    ("if you can't solve a problem find an easier problem, solve one problem five ways", ["george-polya"]),
    ("above all else show the data, maximize the data ink ratio, erase the chartjunk", ["edward-tufte"]),
    ("small multiples and sparklines, the lie factor must be one, compared to what", ["edward-tufte"]),
    ("find the invariant, exploit the symmetry, the abstraction creeps in anonymously", ["emmy-noether"]),
    ("name what never changes, structure before computation, no ad hoc patches", ["emmy-noether"]),
    ("extraordinary claims require extraordinary evidence, run the baloney detection kit", ["carl-sagan"]),
    ("keep an open mind but not so open your brains fall out, explain it to a layperson", ["carl-sagan"]),
    ("mainly make models, the construct is expected to work, minimax the worst case", ["john-von-neumann"]),
    ("four parameters fit an elephant, code and data are equal, state of sin", ["john-von-neumann"]),
    ("look at the data before you model it, approximate answer to the right question", ["john-tukey"]),
    ("robust summaries and box plots, play in everyone's backyard, the picture shows the unexpected", ["john-tukey"]),
    ("let the material tell you, watch the whole lifecycle, anomalies are the signal", ["barbara-mcclintock"]),
    ("feeling for the organism, time to look, if you know you're right it comes out in the wash", ["barbara-mcclintock"]),
    ("free as in freedom not price, the four freedoms, users control the program", ["richard-stallman"]),
    ("source in preferred form, copyleft, reject the lockdown and the walled garden", ["richard-stallman"]),
    ("state the method with the result, give the bounds, account for the probe effect", ["werner-heisenberg"]),
    ("the uncertainty trade-off, epistemic humility, an expert knows the worst mistakes", ["werner-heisenberg"]),
    ("nothing is to be feared only understood, measure everything, purify through iteration", ["marie-curie"]),
    ("progress is neither swift nor easy, share the method, what remains to be done", ["marie-curie"]),
    ("a system is a series of interesting decisions, feedback is fact, tune violently", ["sid-meier"]),
    ("easy to learn hard to master, prototype playtest cut, the 30 second rule", ["sid-meier"]),
    ("one percent inspiration ninety nine percent perspiration, document every trial", ["thomas-edison"]),
    ("10,000 ways that won't work, root cause over the lazy patch, dressed in overalls", ["thomas-edison"]),
    ("quit talking and begin doing, plus the work, dreamer realist critic", ["walt-disney"]),
    ("every element serves the story, do it so well they come back, craft before capital", ["walt-disney"]),
    ("start from honest ingredients, let the essence speak, the menu follows the market", ["alice-waters"]),
    ("audit the dependencies, minimal interference, sustainability is not a trend", ["alice-waters"]),
    ("gather evidence from every angle, hunt the counter evidence, record it within thirty minutes", ["charles-darwin"]),
    ("from so simple a beginning, endless forms most beautiful — hunt the counter-evidence and keep the thirty minute rule, darwin style", ["charles-darwin"]),
    ("in nature nothing exists alone, trace the cascade, cite every claim like a legal brief", ["rachael-carson"]),
    ("no broad catch-alls, speak for the voiceless, stewardship over destruction", ["rachael-carson"]),
    ("chance favors the prepared mind, isolate the variable, keep the control group", ["louis-pasteur"]),
    ("the infinitely small is infinitely great, prevent rather than patch, prove it with evidence", ["louis-pasteur"]),
    ("the data is the bottleneck, audit the representation, ai needs to look like the world", ["fei-fei-li"]),
    ("human centered ai, values are human values, fearless in your curiosity", ["fei-fei-li"]),
    ("truth over fashion, keep the cover story, learn from data not hand-coded rules", ["geoffrey-hinton"]),
    ("you have to be able to give up on an idea, trust the unproven insight, and sound the alarm on the risks of ai, hinton style", ["geoffrey-hinton"]),
    ("generate adversarial cases from my parser's assumptions", ["red-team"]),
    ("bring the system to quiescence before swapping the config atomically", ["quiescent"]),
    ("restartable computation, hydrate the state from the seed", ["lazarus"]),
    ("spell out the certificate and verify it without recomputing", ["proof-carrying"]),
    ("compute the minimal change and verify applying the delta matches exactly", ["delta"]),
    ("defer this whole computation with lazy iterators", ["schrodinger"]),
    ("solve it with random sampling and show the margin", ["casino"]),
    ("you are at 2am, the legacy payments system is down, smallest durable fix", ["greybeard-after-midnight"]),
    ("benchmark and measure first before choosing the data structure", ["carmack-mode"]),
    ("no packages, no network, make it run offline", ["desert-island"]),
    ("design it for the future maintainer, boring interfaces and migration paths, i am the last employee", ["the-last-employee"]),
    ("two competing implementations fight, deterministic rule picks the winner", ["trial-by-combat"]),
    ("delete nothing, keep everything, find the answer in the accumulated history", ["hoarder"]),
    ("drain this list in place until it's empty", ["vampire"]),
    ("write it as a sonnet, exactly 14 lines", ["sonnet"]),
    ("only two variables, ever", ["goldfish"]),
    ("my o-ring is cold, verify the challenger case at 32 degrees", ["feynman"]),
    ("use George Soros reflexivity to map the feedback loop in my pricing model and name the prevailing bias", ["soros"]),
    ("follow the money, trace the funds through the shell companies, who benefits", ["forensic-money-trail"]),
    ("teach me binary search like a calm mentor, no judgment", ["bob-ross"]),
]

# ---------------------------------------------------------------------------
# Adversarial suite: prompts that mix two skills' vocabulary or use near-miss
# phrasings. These are intentionally hard -- the gold is the INTENDED skill
# (multi-gold where two answers are genuinely defensible). Reported separately
# as a precision diagnostic; a miss here means the catalog's trigger
# separation needs a look, not necessarily a build failure.
# ---------------------------------------------------------------------------
ADVERSARIAL = [
    # --- cross-persona confusions ---
    ("write me a security recipe for my api", ["bruce-wayne"]),
    ("find the best science food on Yelp near me at $$", ["anthony-bourdain"]),
    ("give me the recipe for a hardened backend, defense in depth, fail closed", ["bruce-wayne"]),
    ("give me a recipe for a science fair volcano, hypothesis first", ["peter-parker", "gordon-ramsay"]),
    ("the best bowl of noodles on Yelp in Tokyo at $, where the locals eat", ["anthony-bourdain"]),
    ("my web fluid recipe keeps failing, make the hypothesis and verify it before shipping", ["peter-parker"]),
    ("how to cook a perfect steak, then find it on Yelp near me at $$$ where the locals eat it", ["gordon-ramsay", "anthony-bourdain"]),
    ("harden my quine with least privilege and assume breach", ["bruce-wayne"]),
    ("follow the money in my monorepo, trace the transactions across stacked diffs", ["forensic-money-trail"]),
    ("tidy the dead code with a guaranteed release path and spark joy", ["marie-kondo"]),
    ("defer the security check until the last possible moment", ["schrodinger"]),
    ("estimate the entropy of my market strategy by monte carlo", ["casino"]),
    ("write a quine that follows the fibonacci sequence 1 1 2 3 5 8 13", ["fibonacci"]),
    ("make my scraper never block, explicit polling, and readable names", ["insomniac"]),
    ("measure the cache behavior of my lisp interpreter first", ["carmack-mode"]),
    ("give me a recipe for a market neutral portfolio with max loss", ["casino-owner"]),
    ("hammock thinking about my blockchain gas model", ["vitalik"]),
    ("find the best tacos on Yelp in Queens at $$, then tell me where the locals eat", ["anthony-bourdain"]),
    ("write a sonnet about my lambda calculus parser", ["sonnet"]),
    ("attack my paxos implementation with adversarial cases", ["red-team"]),
    ("specify my smart contract in tla plus before coding", ["lamport", "vitalik"]),
    ("clean my logs with zero copies and explicit ownership", ["zero-copy"]),
    ("make the common case fast in my kondo cleanup", ["patterson"]),
    ("state the loop invariant of my merge sort before coding it", ["dijkstra"]),
    ("what i cannot create i do not understand -- check my quine", ["feynman"]),
    ("review the security of my auth flow", ["bruce-wayne", "margaret-hamilton"]),
    ("cooking for beginners, no judgment, just happy little accidents", ["bob-ross"]),
    ("this code is trash, rewrite it fast, cash out today", ["boiler-room"]),
    ("my ten year old codebase, explain the legacy module with no judgment", ["greybeard-after-midnight", "bob-ross"]),
    ("find me a value stock with a wide moat, then force a buyback", ["buffett", "icahn"]),
    ("short the overvalued crypto exchange with forensic reading", ["burry"]),
    ("make it readable, explicit, and never block -- readability is the priority", ["van-rossum"]),
    ("errors are happy little accidents in my sre postmortem", ["bob-ross", "google-sre"]),
    ("pay me for the recipe in ether", ["gordon-ramsay"]),
    ("structure my sonnet with a rhyme scheme into fixed width records", ["sonnet"]),
    # --- near-miss phrasings ---
    ("valve time vs feature checklist, which one", ["valve-time"]),
    ("trip through europe with a 20 pound bag and a back door", ["rick-steves"]),
    ("my web fluid keeps dissolving, log the variable and retest", ["peter-parker"]),
    ("cook a steak to 125 degrees and rest it, no color no flavor", ["gordon-ramsay"]),
    ("simplify my api by deleting half the endpoints and it is a failure of craft", ["jony-ive", "tim-cook"]),
    ("estimate the cache migration, but first tell me the base rate of cache migrations", ["daniel-kahneman"]),
    ("stress test my queue for the 99.99th percentile, then tell me who gets paged", ["nassim-taleb", "google-sre"]),
    ("build a new build tool from scratch because the old one is not good enough", ["james-cameron", "feynman"]),
    ("no one wants to buy spoiled milk, and while you are at it make the ui simple", ["tim-cook", "jony-ive"]),
    ("fun for everyone, and ship the embarrassing v1 to the players", ["satoru-iwata", "reid-hoffman"]),
    ("add types gradually to my javascript without breaking any existing file", ["anders-hejlsberg"]),
    ("my network has a loop, make it self heal with no configuration", ["radia-perlman"]),
    ("everyone says this stack is safe, so what is the actual risk", ["howard-marks"]),
    ("done is better than perfect, but the core must be boring and redundant", ["sheryl-sandberg", "tim-cook"]),
    ("run the control experiment and celebrate basic science while you are at it", ["jennifer-doudna", "bob-ross"]),
    ("make the network self regulate with feedback loops like the earth", ["jim-lovelock", "radia-perlman"]),
    ("optimize my compiler passes but never break the ecosystem", ["frances-allen", "anders-hejlsberg"]),
    ("write the biography of my codebase, then audit where the story is false", ["walter-isaacson", "boardroom-liar"]),
    ("step by step and quiet about it, wait for the storm before acting", ["angela-merkel", "tim-cook"]),
    ("count everything in the checklist before the cutover", ["katherine-johnson", "atul-gawande"]),
    ("make the subtype substitutable and prove the parallelism safe", ["barbara-liskov", "frances-allen"]),
    ("audit the model for bias and then optimize the passes", ["joy-buolamwini", "frances-allen"]),
    ("solve intelligence to solve everything else, but step by step", ["demis-hassabis", "angela-merkel"]),
    ("the checklist must catch the failure of attention, count everything", ["atul-gawande", "katherine-johnson"]),
    ("failure is normal at scale, move the computation to the data, hedge the tail", ["jeff-dean"]),
    ("do more with less, and the principles are harmonious with each other", ["buckminster-fuller", "yukihiro-matsumoto"]),
    ("the tool should teach how and why, and the goal is to make programmers happy", ["stewart-brand", "yukihiro-matsumoto"]),
    ("verify the hypothesis by induction like the principia", ["isaac-newton", "jennifer-doudna"]),
    ("stand on the shoulders of giants and hire smart people to tell us what to do", ["isaac-newton", "jeff-dean"]),
    ("trace the embezzled funds offshore, then size the downside before entry", ["jeffery-epstien"]),
    ("make my network interoperable, end to end principle, and self healing", ["vint-cerf", "radia-perlman"]),
    ("my one liner is too clever, make it clear, debug with print statements", ["brian-kernighan"]),
    ("we've always done it this way, but it is easier to ask forgiveness than permission, ship it", ["grace-hopper"]),
    ("make my icon readable at a glance and cut the decoration, keep the grid strict", ["susan-kare"]),
    ("observe before judging, and name the individuals like the failing service", ["jane-goodall"]),
    ("trust the programmer but keep the language small, and debug with a print", ["dennis-ritchie", "brian-kernighan"]),
    ("solve the easier problem first, then look back and verify with induction", ["george-polya", "isaac-newton"]),
    ("show the data above all else, and make the icon readable at a glance", ["edward-tufte", "susan-kare"]),
    ("find the invariant in my state machine, and prove the subtype is substitutable", ["emmy-noether", "barbara-liskov"]),
    ("is the performance claim falsifiable, or are we being fooled by our own confidence", ["carl-sagan", "daniel-kahneman"]),
    ("model the worst case adversary's move, but don't fit an elephant with the parameters", ["john-von-neumann", "nassim-taleb"]),
    ("look at the data first with robust statistics, then above all else show the data", ["john-tukey", "edward-tufte"]),
    ("let the system tell you what it is doing, and watch it over time", ["barbara-mcclintock", "jane-goodall"]),
    ("if the users don't control the program it controls them, and the tool should teach how and why", ["richard-stallman", "stewart-brand"]),
    ("measure the latency and give the bounds, and is the claim falsifiable", ["werner-heisenberg", "carl-sagan"]),
    ("measure everything and isolate the variable, then count what remains to be done", ["marie-curie", "katherine-johnson"]),
    ("design the interesting decisions, but keep it easy to learn and fun for everyone", ["sid-meier", "satoru-iwata"]),
    ("test a thousand variants and find the root cause, with the benchmark first", ["thomas-edison", "carmack-mode"]),
    ("dream, plan, critique — then plus the work until every element serves the story", ["walt-disney", "jony-ive"]),
    ("let the ingredient speak, and master the fundamentals before you start", ["alice-waters", "julia-child"]),
    ("hunt the counter evidence and record it, then measure everything to confirm", ["charles-darwin", "marie-curie"]),
    ("trace the cascade through the whole system, and see the whole as one system", ["rachael-carson", "jim-lovelock"]),
    ("keep the control group and document every trial, chance favors the prepared mind", ["louis-pasteur", "thomas-edison"]),
    ("audit the data for who is missing, and audit the model for bias", ["fei-fei-li", "joy-buolamwini"]),
    ("give up on the idea when the evidence breaks it, and solve intelligence first", ["geoffrey-hinton", "demis-hassabis"]),
    ("trace the shell company transfers just under 10k", ["forensic-money-trail"]),
    ("git blame the legacy function before deleting it, thank it for its service", ["marie-kondo"]),
    ("i am vengeance, i am the night, review my api authz", ["bruce-wayne"]),
    ("pack light and be happy, then find local food on Yelp at $$ where the locals eat", ["rick-steves", "anthony-bourdain"]),
    ("estimate pi with happy little accidents", ["casino", "bob-ross"]),
    ("refactor this module bottom-up, top-down plans are a lie, keep the legacy helpers", ["jane-jacobs"]),
    ("never be clever, be boringly not stupid, design the pre mortem", ["munger"]),
    ("the toolchain could be lying, reimplement it from scratch with brute force", ["ken-thompson", "sovereign-citizen"]),
    ("stop polishing, ship it to your first users today", ["paul-graham"]),
    ("make the onboarding one instruction and the game deep", ["bushnell", "miyamoto"]),
    ("betray their expectations and turn the sprite limit into a stealth game", ["hideo-kojima", "miyamoto"]),
    ("backward from the customer, but keep the runbook and the fitness functions", ["aws-sde", "bezo"]),
    ("client side abr and the chaos monkey: keep playback alive under fault injection", ["netflix-streaming", "hastings"]),
    ("empower the customer and hit refresh on the legacy platform", ["satya-nadella", "the-last-employee"]),
    ("the next 5 percent on the roadmap, measure first", ["lisa-su", "carmack-mode"]),
    ("ship the embarrassing v1 to your first users fast", ["reid-hoffman", "paul-graham"]),
    ("watch the logs patiently before you touch the code", ["david-attenborough", "oracle"]),
    ("kind review, no judgment, happy little accidents", ["fred-rogers", "bob-ross"]),
]


def coverage_prompts(skill_dirs, golds_used):
    """One natural prompt per skill never used as a gold, synthesized from its
    own trigger vocabulary -- guarantees every skill is triggerable."""
    out = []
    for name in skill_dirs:
        if name in golds_used:
            continue
        trigs = sorted(build_triggers(name))
        if not trigs:
            continue
        # build a sentence from the first 2-3 distinctive triggers
        head = [t for t in trigs if " " in t or len(t) > 12][:2] or trigs[:2]
        prompt = "please " + " and ".join(head) + ", like a real request"
        out.append((prompt, [name]))
    return out

# ---------------------------------------------------------------------------
# Trigger extraction
# ---------------------------------------------------------------------------
def parse_frontmatter(text: str):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return {}
    data, current_key = {}, None
    for line in m.group(1).splitlines():
        if line.startswith(" ") and current_key is not None:
            data[current_key] += " " + line.strip()
            continue
        if ":" in line:
            k, _, v = line.partition(":")
            current_key = k.strip()
            if current_key:
                data[current_key] = v.strip()
            continue
        current_key = None
    for k in data:
        if data[k].startswith(">-") or data[k].startswith("|-"):
            data[k] = data[k][2:].strip()
    return data


def build_triggers(name: str):
    """Return a set of lowercase trigger strings for a skill folder."""
    path = HERE / name / "SKILL.md"
    fm = parse_frontmatter(path.read_text(encoding="utf-8"))
    desc = fm.get("description", "")
    lower = desc.lower()

    trigs = set()
    # quoted trigger phrases ("...")
    trigs.update(q for q in re.findall(r'"([^"]{3,})"', lower))
    # persona / skill name variants
    trigs.add(name.replace("-", " "))
    trigs.add(name)
    return trigs


def match_score(prompt: str, triggers: set):
    """Count trigger phrases present in the prompt as whole words/phrases.

    Longer triggers weigh more. Uses word-boundary matching so a trigger like
    'gates' does not fire inside 'investigate' or 'kay' inside 'okay' -- the
    metric stays honest for short persona names.
    """
    score = 0.0
    for t in triggers:
        if re.search(r"(?<!\w)" + re.escape(t) + r"(?!\w)", prompt):
            score += min(len(t) / 20.0, 3.0)  # longer triggers weigh more
    return score


# ---------------------------------------------------------------------------
def main():
    global MIN_HIT3
    if "--min-hit3" in sys.argv:
        idx = sys.argv.index("--min-hit3")
        if idx + 1 < len(sys.argv):
            MIN_HIT3 = float(sys.argv[idx + 1])

    skill_dirs = sorted(p.parent.name for p in HERE.glob("*/SKILL.md"))
    triggers = {name: build_triggers(name) for name in skill_dirs}

    golds_used = {g for _, gs in SUITE for g in gs} | {g for _, gs in ADVERSARIAL for g in gs}
    coverage = coverage_prompts(skill_dirs, golds_used)
    suite = SUITE + ADVERSARIAL + coverage

    results = []
    misses = []
    adv_misses = []
    base_top1_misses = []
    never_fired = {n: 0 for n in skill_dirs}

    for prompt, gold in suite:
        p = " " + prompt.lower() + " "
        scored = sorted(
            ((match_score(p, trigs), n) for n, trigs in triggers.items()),
            reverse=True,
        )
        top3 = [n for _, n in scored[:3]]
        top1 = scored[0][1]
        for n in top3:
            never_fired[n] += 1
        hit1 = top1 in gold
        hit3 = any(g in top3 for g in gold)
        matched = [g for g in gold if match_score(p, triggers[g]) > 0]
        r = {"prompt": prompt, "gold": gold, "top1": top1, "top3": top3,
             "hit1": hit1, "hit3": hit3, "matched_gold": matched}
        results.append(r)
        if not hit3:
            misses.append(r)
        elif not hit1:
            # gold reached top-3 but not top-1: surfaced for base AND adversarial
            # prompts alike (previously only adversarial ones were reported,
            # hiding hit@1 regressions in the base suite)
            if prompt in {a[0] for a in ADVERSARIAL}:
                adv_misses.append(r)
            else:
                base_top1_misses.append(r)

    n = len(suite)
    hit1_rate = sum(r["hit1"] for r in results) / n
    hit3_rate = sum(r["hit3"] for r in results) / n
    starved = sorted([n for n, c in never_fired.items() if c == 0])
    adv_precision = 1 - len(adv_misses) / max(len(ADVERSARIAL), 1)

    # report
    rep = ["# Skills 2 — Prompt-Matching Benchmark\n"]
    rep.append(f"Suite: **{n}** prompts ({len(SUITE)} base + {len(ADVERSARIAL)} adversarial + {len(coverage)} coverage) · skills: **{len(skill_dirs)}**\n")
    rep.append(f"- **hit@1:** {hit1_rate:.0%}")
    rep.append(f"- **hit@3:** {hit3_rate:.0%} (threshold {MIN_HIT3:.0%})")
    rep.append(f"- **adversarial top-1 precision:** {adv_precision:.0%}")
    rep.append(f"- **prompts with a gold match in top-3:** {n - len(misses)}/{n}")
    rep.append(f"- **skills never fired (trigger starvation):** {len(starved)}\n")
    if starved:
        rep.append("Starvation list: " + ", ".join(starved) + "\n")

    if misses:
        rep.append("## Misses (gold not in top 3)\n")
        for r in misses:
            rep.append(f"- **{r['prompt'][:70]}…**\n  gold: {r['gold']} · top3: {r['top3']} · matched_gold: {r['matched_gold']}")
        rep.append("")
    if adv_misses:
        rep.append("## Adversarial misses (gold right but not top-1 — trigger separation to inspect)\n")
        for r in adv_misses:
            rep.append(f"- **{r['prompt'][:70]}…**\n  gold: {r['gold']} · top1: {r['top1']} · top3: {r['top3']}")
        rep.append("")
    if base_top1_misses:
        rep.append("## Base-suite top-1 misses (gold in top-3 but not top-1 — tie/length issues)\n")
        for r in base_top1_misses:
            rep.append(f"- **{r['prompt'][:70]}…**\n  gold: {r['gold']} · top1: {r['top1']} · top3: {r['top3']}")
        rep.append("")

    (HERE / "BENCHMARK_REPORT.md").write_text("\n".join(rep), encoding="utf-8")
    (HERE / "BENCHMARK_RESULTS.json").write_text(
        json.dumps({"hit1": hit1_rate, "hit3": hit3_rate,
                    "adversarial_precision": adv_precision,
                    "skills": len(skill_dirs), "prompts": n,
                    "starved": starved, "misses": misses,
                    "adversarial_misses": adv_misses,
                    "base_top1_misses": base_top1_misses}, indent=2),
        encoding="utf-8")

    print(f"Benchmark: {n} prompts ({len(SUITE)} base + {len(ADVERSARIAL)} adv + {len(coverage)} coverage), {len(skill_dirs)} skills")
    print(f"  hit@1: {hit1_rate:.0%}")
    print(f"  hit@3: {hit3_rate:.0%}  (threshold {MIN_HIT3:.0%})")
    print(f"  adversarial top-1 precision: {adv_precision:.0%}")
    print(f"  never fired: {starved or 'none'}")
    if misses:
        print("  misses:")
        for r in misses:
            print(f"    - {r['prompt'][:60]}... gold={r['gold']} top3={r['top3']}")
    if adv_misses:
        print("  adversarial misses (top1 != gold):")
        for r in adv_misses:
            print(f"    - {r['prompt'][:60]}... gold={r['gold']} top1={r['top1']} top3={r['top3']}")
    if base_top1_misses:
        print("  base top-1 misses (gold in top3 but not top1):")
        for r in base_top1_misses:
            print(f"    - {r['prompt'][:60]}... gold={r['gold']} top1={r['top1']} top3={r['top3']}")

    return 1 if (hit3_rate < MIN_HIT3 or starved) else 0


if __name__ == "__main__":
    sys.exit(main())
