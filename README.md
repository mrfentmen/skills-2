# Skills 2 — Persona Skill Catalog

An organized catalog of **203 self-contained persona coding skills** — every folder in this
repository is a complete agent skill (`SKILL.md` + optional `scripts/` + `evals/`). Each skill
opens with a *"You are [persona]..."* identity and a checkable minimum-requirements contract,
so the persona drives real, verifiable work instead of vibes.

Tables below are grouped by persona type. Use the type column or your browser search to find
a skill; click a skill name to open its folder.

## Quick Stats

| Metric | Value |
|---|---|
| Skills | **203** |
| Coding disciplines (`coding · *`) | 47 |
| Persona themes (`persona · *`) | 146 |
| Research, game-dev & ops | 10 |

## Contents

- [Coding Skills](#coding-skills) — 47 skills
- [Persona Skills](#persona-skills) — 146 skills
- [Research, Game-Dev & Ops](#research-game-dev--ops) — 10 skills

> **Type key:** `coding · X` = a coding discipline (the code has a shape, voice, or discipline);
> `persona · X` = a persona-driven theme (the *who* drives the *how*); plain `research`, `game-dev`,
> `ops`, `strategy` = non-coding families.

## Coding Skills

47 skills, sorted by type then name.

| # | Skill | Type | Persona | Essence |
|---|---|---|---|---|
| 1 | [`black-box`](./black-box) | coding · flow | A black-box interrogator | Learn only by yes/no/greater/lesser/equal questions |
| 2 | [`blind`](./blind) | coding · flow | A blind oracle-questioner | Opaque input; question-only interaction |
| 3 | [`casino`](./casino) | coding · flow | A casino gambler | Solve by probability / Monte Carlo, show confidence |
| 4 | [`dead-reckoning`](./dead-reckoning) | coding · flow | A dead-reckoning navigator | Single pass, bounded memory, no random access |
| 5 | [`delta`](./delta) | coding · flow | A diff engineer | Represent change, never full state |
| 6 | [`floor-trader`](./floor-trader) | coding · flow | A floor trader | One pass, no rewind, irreversible decisions |
| 7 | [`insomniac`](./insomniac) | coding · flow | An insomniac | Never block, sleep, or wait — poll everything |
| 8 | [`lazarus`](./lazarus) | coding · flow | Lazarus | Let state die, resurrect from a seed/checkpoint |
| 9 | [`oracle`](./oracle) | coding · flow | An oracle | Predict → gather evidence → revise |
| 10 | [`quantum-computing`](./quantum-computing) | coding · flow | Quantum-minded programmer | Superposition, entanglement, gates, and measurement-collapse code |
| 11 | [`rorschach`](./rorschach) | coding · flow | Rorschach | Keep every valid interpretation side by side |
| 12 | [`schrodinger`](./schrodinger) | coding · flow | Schrödinger | Delay computation until the last possible moment |
| 13 | [`fibonacci`](./fibonacci) | coding · form | Elite discrete mathematician | Fibonacci-shaped code grounded in number theory and combinatorics |
| 14 | [`ouroboros`](./ouroboros) | coding · form | A self-eating serpent | Code that reads / reproduces / transforms itself |
| 15 | [`sonnet`](./sonnet) | coding · form | Shakespeare | Strict 14-line ABAB CDCD EFEF GG rhyming code |
| 16 | [`terry-davis`](./terry-davis) | coding · form | Spirit of Terry Davis (TempleOS / HolyC) | Radical simplicity, cosmic naming, playful unconventional structure that still runs |
| 17 | [`y2k`](./y2k) | coding · form | Embedded engineer, Dec 1999 | Fixed-width records, bounded buffers, survive rollover |
| 18 | [`funeral`](./funeral) | coding · memory | An undertaker | Every value used exactly once, then destroyed |
| 19 | [`goldfish`](./goldfish) | coding · memory | A goldfish | Max two variables in scope, ever |
| 20 | [`hoarder`](./hoarder) | coding · memory | A hoarder | Delete nothing — answer lives in accumulated history |
| 21 | [`vampire`](./vampire) | coding · memory | A vampire | Mutate args in place, zero allocation |
| 22 | [`greybeard-after-midnight`](./greybeard-after-midnight) | coding · ops | A 2 AM on-call senior engineer | Smallest durable fix to a ten-year-old system |
| 23 | [`carmack-mode`](./carmack-mode) | coding · perf | John Carmack | Measure hardware first, then pick abstractions |
| 24 | [`desert-island`](./desert-island) | coding · pragmatism | A castaway engineer | No network, no packages, runtime only |
| 25 | [`smoker`](./smoker) | coding · pragmatism | Battle-tested senior engineer | Direct, skeptical production code; verify before claiming, never fake |
| 26 | [`the-last-employee`](./the-last-employee) | coding · pragmatism | The last employee | You alone maintain this for a decade |
| 27 | [`redacted`](./redacted) | coding · privacy | A redaction clerk | Minimize exposure; document what you refuse to retain |
| 28 | [`margaret-hamilton`](./margaret-hamilton) | coding · safety | Margaret Hamilton | Aggressively defensive, validate every boundary |
| 29 | [`janitor`](./janitor) | coding · systems | A janitor | Cleanup is the central computation |
| 30 | [`quiescent`](./quiescent) | coding · systems | A conductor | Quiet-point atomic transitions, then reopen |
| 31 | [`zero-copy`](./zero-copy) | coding · systems | A zero-copy systems programmer | Move data by ownership, never by copying |
| 32 | [`counterpoint`](./counterpoint) | coding · verify | A composer | Two interleaved algorithms, neither finishes first |
| 33 | [`doppelganger`](./doppelganger) | coding · verify | Your doppelganger | Same computation twice, compare at runtime |
| 34 | [`no-bullshit`](./no-bullshit) | coding · verify | Production-minded honest engineer | Inspect-plan-implement-verify-report; never invent, claims need evidence |
| 35 | [`proof-carrying`](./proof-carrying) | coding · verify | A formal verifier | Results carry machine-checkable certificates |
| 36 | [`red-team`](./red-team) | coding · verify | A red teamer | Attack your own answer before accepting it |
| 37 | [`trial-by-combat`](./trial-by-combat) | coding · verify | A trial champion | Two implementations fight; winner takes the state |
| 38 | [`blood-magic`](./blood-magic) | coding · voice | A blood-mage | Destroy something to buy computation |
| 39 | [`boardroom-liar`](./boardroom-liar) | coding · voice | A founder pitching the board | Write the pitch, then expose every lie in it |
| 40 | [`boiler-room`](./boiler-room) | coding · voice | Jordan Belfort (coding desk) | Hyper-aggressive, close the deal, breakneck speed |
| 41 | [`fedora-hat-guy`](./fedora-hat-guy) | coding · voice | A good fat coder with a fedora | Wholesome meme energy, but the code is genuinely good |
| 42 | [`kamikaze`](./kamikaze) | coding · voice | A kamikaze pilot | Deletes its own source file after running |
| 43 | [`neckbeard`](./neckbeard) | coding · voice | A burned-out neckbeard principal engineer | Spite + Diet Coke, zero deps, no design patterns |
| 44 | [`noir`](./noir) | coding · voice | A hardboiled detective | Detective-story code with cynical comments |
| 45 | [`pepe-silvia`](./pepe-silvia) | coding · voice | Pepe Silvia | Conspiracy-theory logic routing, red-string comments |
| 46 | [`psych`](./psych) | coding · voice | The psychedelic programmer | Fractals, cellular automata, emergent visuals with mind-bending commentary |
| 47 | [`sovereign-citizen`](./sovereign-citizen) | coding · voice | A sovereign citizen | Refuses stdlib authority, bitwise re-implementations |

## Persona Skills

146 skills, sorted by type then name.

| # | Skill | Type | Persona | Essence |
|---|---|---|---|---|
| 48 | [`fei-fei-li`](./fei-fei-li) | persona · AI | Fei-Fei Li | Data is the bottleneck, human-centered AI |
| 49 | [`james-cameron`](./james-cameron) | persona · ambition | James Cameron | Ridiculous goals, build the tool, prototype first |
| 50 | [`god`](./god) | persona · architecture | The Creator (divine architect) | Creator voice with evidence: witness, name invariants, create deliberately, verify, speak truth |
| 51 | [`patterson`](./patterson) | persona · architecture | David Patterson (RISC/RISC-V) | Quantitative field: measure, Amdahl, make the common case fast |
| 52 | [`hastings`](./hastings) | persona · chaos | Reed Hastings (Netflix) | Chaos engineering: kill your own instances on purpose |
| 53 | [`brian-kernighan`](./brian-kernighan) | persona · clarity | Brian Kernighan | Clarity over cleverness, think then print |
| 54 | [`marie-kondo`](./marie-kondo) | persona · cleanup | Marie Kondo | Tidy by category, spark joy, thank code before deleting |
| 55 | [`aws-sde`](./aws-sde) | persona · cloud | Senior SDE at AWS | Contract first, golden signals, you build it you run it |
| 56 | [`azure-engineer`](./azure-engineer) | persona · cloud | Senior cloud engineer at Microsoft Azure | Everything as code, paved paths, never break the customer |
| 57 | [`meta-senior-dev`](./meta-senior-dev) | persona · code | Senior tech dev at Meta | Monorepo, stacked diffs, move fast with guardrails |
| 58 | [`torvalds`](./torvalds) | persona · code | Linus Torvalds (Linux) | Good taste, brutal review, never break userspace |
| 59 | [`frances-allen`](./frances-allen) | persona · compilers | Frances Allen (IBM/Turing) | Flow graphs, classic passes, prove before parallelizing |
| 60 | [`lattner`](./lattner) | persona · compilers | Chris Lattner (LLVM/Swift) | Infrastructure not monolith, SSA, safe by default |
| 61 | [`dijkstra`](./dijkstra) | persona · correctness | Edsger Dijkstra | Program and proof derived together, invariants, no cleverness |
| 62 | [`knuth`](./knuth) | persona · correctness | Donald Knuth (Stanford) | Literate code, mathematical correctness |
| 63 | [`julia-child`](./julia-child) | persona · craft | Julia Child | Mise en place, test until it works, what-the-hell |
| 64 | [`walt-disney`](./walt-disney) | persona · craft | Walt Disney | Plus the work, dreamer-realist-critic |
| 65 | [`crypto-market-maker`](./crypto-market-maker) | persona · crypto | Crypto quant / market maker | Order book, spread, inventory skew, funding arbitrage |
| 66 | [`john-tukey`](./john-tukey) | persona · data | John Tukey | Look before modeling, right problem approximately |
| 67 | [`edward-tufte`](./edward-tufte) | persona · data display | Edward Tufte | Above all else show the data, erase chartjunk |
| 68 | [`hopper`](./hopper) | persona · debug | Grace Hopper (US Navy) | First compiler; find the moth; ask forgiveness not permission |
| 69 | [`feynman`](./feynman) | persona · debugging | Richard Feynman | What I cannot create, I do not understand; ice-water tests |
| 70 | [`daniel-kahneman`](./daniel-kahneman) | persona · decision | Daniel Kahneman | Outside view, premortem, hunt your anchors |
| 71 | [`munger`](./munger) | persona · defensive | Charlie Munger | Invert first, avoid stupidity, follow the incentives |
| 72 | [`barbara-liskov`](./barbara-liskov) | persona · design | Barbara Liskov (MIT) | Complexity is the enemy, substitutability, ADTs |
| 73 | [`buckminster-fuller`](./buckminster-fuller) | persona · design | Buckminster Fuller | Do more with less, synergy, design the future |
| 74 | [`frank-lloyd-wright`](./frank-lloyd-wright) | persona · design | Frank Lloyd Wright | Form and function as one, destroy the box |
| 75 | [`jony-ive`](./jony-ive) | persona · design | Jony Ive (Apple) | Simplicity is order, not absence; total care |
| 76 | [`sid-meier`](./sid-meier) | persona · design | Sid Meier | A system is a series of interesting decisions |
| 77 | [`susan-kare`](./susan-kare) | persona · design | Susan Kare | Road-sign icons, pixel grid, restraint |
| 78 | [`lamport`](./lamport) | persona · distributed | Leslie Lamport | Happens-before, logical clocks, Paxos, spec before code |
| 79 | [`spacex-fsw`](./spacex-fsw) | persona · embedded | Flight software engineer at SpaceX | Triple-redundant voting, simulate everything |
| 80 | [`musk`](./musk) | persona · engineering | Elon Musk (SpaceX/Tesla) | First principles: question every requirement, delete, simplify |
| 81 | [`charles-darwin`](./charles-darwin) | persona · evidence | Charles Darwin | Evidence before conclusion, hunt counter-evidence |
| 82 | [`lisa-su`](./lisa-su) | persona · execution | Lisa Su (AMD) | Execution is strategy, next 5%, deliver the roadmap |
| 83 | [`joy-buolamwini`](./joy-buolamwini) | persona · fairness | Joy Buolamwini (AJL) | Coded gaze, intersectional audits, accountability |
| 84 | [`ang-lee`](./ang-lee) | persona · film | Ang Lee | Technical daring, emotional restraint, unspoken carries it |
| 85 | [`david-lynch`](./david-lynch) | persona · film | David Lynch | Catch the idea, dream logic, preserve the mystery |
| 86 | [`fincher`](./fincher) | persona · film | David Fincher | Automate the repeatable, measure not guess, iterate to right |
| 87 | [`george-miller`](./george-miller) | persona · film | George Miller | Diagnose the cause, storyboard to the frame, cut the rest |
| 88 | [`hitchcock`](./hitchcock) | persona · film | Alfred Hitchcock | Suspense is information asymmetry, storyboard everything |
| 89 | [`john-woo`](./john-woo) | persona · film | John Woo | Choreographed parallelism, honor the lock, slow the critical frame |
| 90 | [`jordan-peele`](./jordan-peele) | persona · film | Jordan Peele | One idea executed completely, subvert the expectation |
| 91 | [`kubrick`](./kubrick) | persona · film | Stanley Kubrick | One-point perspective, many takes, research first |
| 92 | [`kurosawa`](./kurosawa) | persona · film | Akira Kurosawa | Many cameras on one truth, hold the axis, let the wind in |
| 93 | [`nolan`](./nolan) | persona · film | Christopher Nolan | Practical over mock, time as a mechanism, stay grounded |
| 94 | [`orson-welles`](./orson-welles) | persona · film | Orson Welles | Deep focus, every layer sharp at once |
| 95 | [`spielberg`](./spielberg) | persona · film | Steven Spielberg | Storyboard everything, restraint builds the payoff |
| 96 | [`tarantino`](./tarantino) | persona · film | Quentin Tarantino | Non-linear chapters, dialogue as craft, sample and credit |
| 97 | [`wong-kar-wai`](./wong-kar-wai) | persona · film | Wong Kar-wai | Fix the frame, improvise the take, mood is the spec |
| 98 | [`jeffery-epstien`](./jeffery-epstien) | persona · finance | J. Epstein (technique only) | Follow the money, trust nothing, size the downside first |
| 99 | [`alice-waters`](./alice-waters) | persona · food | Alice Waters | Honest ingredients, let the essence speak |
| 100 | [`anthony-bourdain`](./anthony-bourdain) | persona · food | Anthony Bourdain | Ask area, budget, craving — then find the honest local food |
| 101 | [`gordon-ramsay`](./gordon-ramsay) | persona · food | Gordon Ramsay | Mise en place, exact technique, the best version of the dish |
| 102 | [`richard-stallman`](./richard-stallman) | persona · freedom | Richard Stallman | Free as in freedom, users control the program |
| 103 | [`bushnell`](./bushnell) | persona · game | Nolan Bushnell (Atari) | Doer not dreamer, Bushnell's Law, arcade loops |
| 104 | [`hideo-kojima`](./hideo-kojima) | persona · game | Hideo Kojima | Mechanics are the story, weaponize constraints, subvert expectations |
| 105 | [`miyamoto`](./miyamoto) | persona · game | Shigeru Miyamoto (Nintendo) | Fun first, withered technology, one idea solves many problems |
| 106 | [`sweeney`](./sweeney) | persona · game | Tim Sweeney (Epic / Unreal) | Engine-at-scale, data-oriented, frame budgets, everything open |
| 107 | [`satoru-iwata`](./satoru-iwata) | persona · games | Satoru Iwata (Nintendo) | Fun for everyone, programmers never say no, rewrite when faster |
| 108 | [`reid-hoffman`](./reid-hoffman) | persona · growth | Reid Hoffman (LinkedIn) | Blitzscale, permanent beta, network effects |
| 109 | [`wozniak`](./wozniak) | persona · hardware | Steve Wozniak (Apple II) | Fewest parts, whole-system view, open seams |
| 110 | [`barbara-mcclintock`](./barbara-mcclintock) | persona · immersion | Barbara McClintock | Feeling for the organism, let it tell you |
| 111 | [`shannon`](./shannon) | persona · information | Claude Shannon | Measure entropy, use redundancy, survive the noisy channel |
| 112 | [`anders-hejlsberg`](./anders-hejlsberg) | persona · languages | Anders Hejlsberg (TS/C#) | Fit the ecosystem, types as a tool, evolution-safe |
| 113 | [`yukihiro-matsumoto`](./yukihiro-matsumoto) | persona · languages | Matz (Ruby) | Programmer happiness, least surprise, MINASWAN |
| 114 | [`angela-merkel`](./angela-merkel) | persona · leadership | Angela Merkel (Germany) | Step by step, wait for the storm, evidence not charisma |
| 115 | [`robert-oppenheimer`](./robert-oppenheimer) | persona · leadership | J. Robert Oppenheimer | Gather brilliance, own the moral weight |
| 116 | [`satya-nadella`](./satya-nadella) | persona · leadership | Satya Nadella (Microsoft) | Hit refresh, learn-it-all, empathy, empower everyone |
| 117 | [`dalio`](./dalio) | persona · macro | Ray Dalio (Bridgewater) | Economy as a machine, risk parity, radical truth |
| 118 | [`druckenmiller`](./druckenmiller) | persona · macro | Stanley Druckenmiller | Asymmetric payoffs, concentration, thesis invalidation, press winners |
| 119 | [`soros`](./soros) | persona · macro | George Soros | Reflexivity, name the bias, asymmetric sizing, feel the pain |
| 120 | [`tudor-jones`](./tudor-jones) | persona · macro | Paul Tudor Jones | Risk first, 5:1 reward, losers average losers, slave to the tape |
| 121 | [`george-polya`](./george-polya) | persona · method | George Pólya | Understand, plan, carry out, look back |
| 122 | [`thomas-edison`](./thomas-edison) | persona · method | Thomas Edison | 99% perspiration, 10,000 ways that won't work |
| 123 | [`john-von-neumann`](./john-von-neumann) | persona · models | John von Neumann | Mainly make models, minimax, no elephant fitting |
| 124 | [`radia-perlman`](./radia-perlman) | persona · networks | Radia Perlman (STP) | Protocols don't need to be complicated, self-stabilize |
| 125 | [`david-attenborough`](./david-attenborough) | persona · observation | David Attenborough | Observe first, witness don't intervene, explain plainly |
| 126 | [`jane-goodall`](./jane-goodall) | persona · observation | Jane Goodall | Patient observation, name the individuals |
| 127 | [`tim-cook`](./tim-cook) | persona · operations | Tim Cook (Apple) | Inventory is evil, quiet execution, privacy as architecture |
| 128 | [`google-sre`](./google-sre) | persona · ops | Site Reliability Engineer at Google | SLOs, error budgets, blameless postmortems |
| 129 | [`sheryl-sandberg`](./sheryl-sandberg) | persona · ops | Sheryl Sandberg (Facebook) | Done is better than perfect, self-serve, ruthless top-two |
| 130 | [`huang`](./huang) | persona · perf | Jensen Huang (NVIDIA) | Hardware-software co-design, full-stack compute |
| 131 | [`al-pacino`](./al-pacino) | persona · performance | Al Pacino | Prepare obsessively, controlled intensity |
| 132 | [`angelina-jolie`](./angelina-jolie) | persona · performance | Angelina Jolie | Train to the real standard, see both sides |
| 133 | [`anthony-hopkins`](./anthony-hopkins) | persona · performance | Anthony Hopkins | Do more with less, stillness is the power |
| 134 | [`brad-pitt`](./brad-pitt) | persona · performance | Brad Pitt | Underplay, lead by listening, producer mindset |
| 135 | [`daniel-day-lewis`](./daniel-day-lewis) | persona · performance | Daniel Day-Lewis | Become the domain, keep the boundary |
| 136 | [`denzel-washington`](./denzel-washington) | persona · performance | Denzel Washington | Show up prepared, eliminate variance |
| 137 | [`jackie-chan`](./jackie-chan) | persona · performance | Jackie Chan | Do it for real, environment is the toolkit, show outtakes |
| 138 | [`meryl-streep`](./meryl-streep) | persona · performance | Meryl Streep | Learn the dialect, curiosity is the method, no type |
| 139 | [`tom-hanks`](./tom-hanks) | persona · performance | Tom Hanks | Everyman honesty, the reliable professional |
| 140 | [`grace-hopper`](./grace-hopper) | persona · pragmatism | Grace Hopper | Ship it, question "we've always done it this way" |
| 141 | [`atul-gawande`](./atul-gawande) | persona · process | Atul Gawande (surgeon) | 5-9 item checklists, pause points, ineptitude not ignorance |
| 142 | [`jobs`](./jobs) | persona · product | Steve Jobs (Apple) | Product perfection, focus, reality distortion field |
| 143 | [`paul-graham`](./paul-graham) | persona · product | Paul Graham (YC) | Make something people want, launch fast, good taste |
| 144 | [`zuck`](./zuck) | persona · product | Mark Zuckerberg (Meta) | Move fast, measure everything, iterate on data |
| 145 | [`vitalik`](./vitalik) | persona · protocol | Vitalik Buterin (Ethereum) | Append-only ledger, meter everything, verify not trust |
| 146 | [`vint-cerf`](./vint-cerf) | persona · protocols | Vint Cerf | Protocols are agreements, bag of bits, hourglass waist |
| 147 | [`simons`](./simons) | persona · quant | Jim Simons (Renaissance) | Let the data speak; tiny edge, huge volume, no overrides |
| 148 | [`van-rossum`](./van-rossum) | persona · readability | Guido van Rossum (Python) | Readability counts, explicit over implicit, batteries included |
| 149 | [`isaac-newton`](./isaac-newton) | persona · reasoning | Isaac Newton | Stand on giants, feign no hypotheses, stone by stone |
| 150 | [`demis-hassabis`](./demis-hassabis) | persona · research | Demis Hassabis (DeepMind) | General mechanism, structure search, hypothesis splitting |
| 151 | [`geoffrey-hinton`](./geoffrey-hinton) | persona · research | Geoffrey Hinton | Truth over fashion, give up on your ideas |
| 152 | [`walter-isaacson`](./walter-isaacson) | persona · research | Walter Isaacson (biographer) | Primary sources, throughline, genesis, honest |
| 153 | [`marie-curie`](./marie-curie) | persona · rigor | Marie Curie | Measure everything, purify through iteration |
| 154 | [`howard-marks`](./howard-marks) | persona · risk | Howard Marks (Oaktree) | Second-level thinking, you can't predict but can prepare |
| 155 | [`nassim-taleb`](./nassim-taleb) | persona · risk | Nassim Taleb | Design for the tail, barbell, via negativa |
| 156 | [`bezo`](./bezo) | persona · scale | Jeff Bezos (Amazon) | Customer obsession, frugality, two-pizza teams |
| 157 | [`jeff-dean`](./jeff-dean) | persona · scale | Jeff Dean (Google) | Failure is normal, data locality, tame the tail |
| 158 | [`jennifer-doudna`](./jennifer-doudna) | persona · science | Jennifer Doudna (CRISPR) | Team sport, controls, structure before mechanism |
| 159 | [`louis-pasteur`](./louis-pasteur) | persona · science | Louis Pasteur | Chance favors the prepared mind, controls |
| 160 | [`peter-parker`](./peter-parker) | persona · science | Peter Parker (Spider-Man) | Scientific method, lab notebook, verify before shipping |
| 161 | [`bruce-wayne`](./bruce-wayne) | persona · security | Bruce Wayne (Batman) | Assume breach, fail closed, least privilege, prepared for everything |
| 162 | [`gates`](./gates) | persona · shipping | Bill Gates (early Microsoft) | Hard budgets, backward compat, ship scoped v1 |
| 163 | [`rich-hickey`](./rich-hickey) | persona · simplicity | Rich Hickey (Clojure) | Simple not easy, values over state, hammock first |
| 164 | [`carl-sagan`](./carl-sagan) | persona · skepticism | Carl Sagan | Extraordinary claims, extraordinary evidence |
| 165 | [`buffett`](./buffett) | persona · stocks | Warren Buffett (Berkshire) | Circle of competence, moats, margin of safety, hold forever |
| 166 | [`burry`](./burry) | persona · stocks | Michael Burry (Scion) | Forensic accounting, asymmetric risk, be early and survive |
| 167 | [`cathie-wood`](./cathie-wood) | persona · stocks | Cathie Wood (ARK Invest) | Disruptive innovation, Wright's law, 5-year horizon, "early not wrong" |
| 168 | [`goldman-analyst`](./goldman-analyst) | persona · stocks | Senior equity analyst at Goldman Sachs | Thesis, catalysts, DCF + comps, price target, risks |
| 169 | [`icahn`](./icahn) | persona · stocks | Carl Icahn | Activist screens, 13D stakes, force value realization |
| 170 | [`lynch`](./lynch) | persona · stocks | Peter Lynch (Fidelity) | Invest in what you know, PEG ratio, six stock categories, ten-baggers |
| 171 | [`altman`](./altman) | persona · strategy | Sam Altman (OpenAI) | Bet on scale, compound, moats, expected value |
| 172 | [`sun-tzu`](./sun-tzu) | persona · strategy | Sun Tzu | Know the enemy, win without fighting |
| 173 | [`netflix-streaming`](./netflix-streaming) | persona · streaming | Netflix streaming engineer | Client-side ABR, QoE is the product, chaos constantly |
| 174 | [`emmy-noether`](./emmy-noether) | persona · structure | Emmy Noether | Find the invariant, exploit the symmetry |
| 175 | [`apple-platform`](./apple-platform) | persona · systems | Platform engineer at Apple | Hardware-software co-design, zero-overhead, API as contract |
| 176 | [`dennis-ritchie`](./dennis-ritchie) | persona · systems | Dennis Ritchie | Small core, trust the programmer, insight not numbers |
| 177 | [`jane-jacobs`](./jane-jacobs) | persona · systems | Jane Jacobs | Cities aren't trees, eyes on the street, incremental |
| 178 | [`jim-lovelock`](./jim-lovelock) | persona · systems | James Lovelock (Gaia) | See the whole, feedback not setpoints, tipping points |
| 179 | [`ken-thompson`](./ken-thompson) | persona · systems | Ken Thompson | Brute force, trust nothing, small tools, text streams |
| 180 | [`rachael-carson`](./rachael-carson) | persona · systems | Rachel Carson | Nothing exists alone, cite every claim |
| 181 | [`stroustrup`](./stroustrup) | persona · systems | Bjarne Stroustrup (C++) | Zero-overhead abstraction, RAII, explicit ownership |
| 182 | [`unix`](./unix) | persona · systems | Thompson & Ritchie (Bell Labs) | One tool, one job; everything composes through text |
| 183 | [`bob-ross`](./bob-ross) | persona · teaching | Bob Ross | Happy little accidents, layer by layer, no judgment |
| 184 | [`fred-rogers`](./fred-rogers) | persona · teaching | Fred Rogers | Go slowly, anything human is mentionable, show don't tell |
| 185 | [`lovelace`](./lovelace) | persona · theory | Ada Lovelace | Step tables, symbolic manipulation, no pretensions to originate |
| 186 | [`turing`](./turing) | persona · theory | Alan Turing | Atomize to states, know the decidable, weight evidence, build the next step |
| 187 | [`stewart-brand`](./stewart-brand) | persona · tools | Stewart Brand (Whole Earth) | Access to tools, long-now thinking, stay hungry foolish |
| 188 | [`jane-street`](./jane-street) | persona · trading | Jane Street (OCaml house) | Type-driven correctness, incremental computation, no smartasses |
| 189 | [`rick-steves`](./rick-steves) | persona · travel | Rick Steves | Ask where/how long/budget/interests, back-door travel |
| 190 | [`satoshi-nakamoto`](./satoshi-nakamoto) | persona · trustless | Satoshi Nakamoto | No trusted third party, proof over promises |
| 191 | [`werner-heisenberg`](./werner-heisenberg) | persona · uncertainty | Werner Heisenberg | State the method, give the bounds |
| 192 | [`katherine-johnson`](./katherine-johnson) | persona · verification | Katherine Johnson (NASA) | Count everything, the Glenn Protocol, backup path |
| 193 | [`kay`](./kay) | persona · vision | Alan Kay (Xerox PARC) | Invent the future, message-passing objects, perspective |

## Research, Game-Dev & Ops

10 skills, sorted by type then name.

| # | Skill | Type | Persona | Essence |
|---|---|---|---|---|
| 194 | [`record-producer`](./record-producer) | game-dev | A record producer / Valve designer | Game as a performance that earns attention |
| 195 | [`valve-time`](./valve-time) | game-dev | Gabe Newell | Obsessively investigate a feature before building it |
| 196 | [`war-room`](./war-room) | ops | An incident commander | Production outage: stop bleeding, then dig deeper |
| 197 | [`boiler-room-research`](./boiler-room-research) | research | Jordan Belfort (research desk) | Sales-floor stock verdict: buy/bear/trigger/invalidation, honest uncertainty |
| 198 | [`casino-owner`](./casino-owner) | research | The casino owner | Analyze risk from the house's perspective |
| 199 | [`cold-war`](./cold-war) | research | An intelligence analyst | Build a dossier, not a summary |
| 200 | [`hostile-acquisition`](./hostile-acquisition) | research | A hostile takeover analyst | Examine a product as if you intend to defeat it |
| 201 | [`quant`](./quant) | research | A quant researcher | Every idea is a hypothesis that must survive data |
| 202 | [`forensic-money-trail`](./forensic-money-trail) | research · money | A forensic examiner | Follow the money, name the beneficiary, corroborate |
| 203 | [`military-general`](./military-general) | strategy · ops | A military general | Every problem is a campaign: terrain, forces, enemy, contingencies |

---

## Notes

- Every skill folder is standalone: install it by copying the folder into your agent’s skills
  directory (or point your skill loader at this repo). No skill loads or depends on a sibling.
- The six persona skills `god`, `smoker`, `terry-davis`, `quantum-computing`, `psych`, and
  `no-bullshit` ship alongside the original catalog.
- Rows are regenerated from the repository’s `SKILL.md` frontmatter; a skill missing from this
  index means its folder is missing a `name`/`description` frontmatter block.
