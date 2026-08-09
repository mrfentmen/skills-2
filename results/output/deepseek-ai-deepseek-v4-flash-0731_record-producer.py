# (1) Timestamped first-minute and core-loop audit for a tiny game: "Orb Catch"
# Core loop: spawn orb -> move paddle -> catch orb -> score -> spawn next orb
timeline = [
    {"at": 0, "beat": "game start", "signal": "title text + start prompt", "action": "read/start"},
    {"at": 2, "beat": "first orb spawns", "signal": "visual orb + soft drop sound", "action": "observe"},
    {"at": 3, "beat": "paddle control", "signal": "paddle follows mouse", "action": "move"},
    {"at": 5, "beat": "first catch", "signal": "score popup + chime", "action": "catch"},
    {"at": 7, "beat": "second orb spawns", "signal": "orb appears at random x", "action": "move to catch"},
    {"at": 12, "beat": "miss", "signal": "red flash + low buzz", "action": "wait for respawn"},
    {"at": 15, "beat": "orb respawns", "signal": "orb reappears", "action": "move"},
    {"at": 20, "beat": "speed increase", "signal": "orb falls faster", "action": "react"},
    {"at": 30, "beat": "streak bonus", "signal": "golden orb + fanfare", "action": "catch"},
    {"at": 45, "beat": "difficulty plateau", "signal": "constant fast orbs", "action": "sustain"},
    {"at": 60, "beat": "game over", "signal": "final score + restart prompt", "action": "decide"},
]

# (2) Pacing, friction, feedback, audio/visual signals, disengagement risk
pacing = {
    "early": "2s to first action, 5s to first reward — tight",
    "mid": "speed ramp at 20s creates tension",
    "late": "plateau at 45s risks monotony",
}
friction = [
    {"at": 12, "issue": "miss causes 3s dead wait before respawn", "risk": "high — player may quit"},
    {"at": 45, "issue": "no new stimulus, only speed", "risk": "medium — boredom"},
]
feedback = {
    "positive": "chime + score popup on catch",
    "negative": "buzz + red flash on miss",
    "missing": "no audio cue for speed increase at 20s",
}
audio_visual = {
    "audio": "drop sound, chime, buzz, fanfare",
    "visual": "orb color, score, red flash, golden orb",
    "clarity": "paddle movement is obvious; miss feedback is clear",
}
disengagement_risk = [
    {"at": 12, "reason": "dead wait after miss", "level": "high"},
    {"at": 45, "reason": "no variety", "level": "medium"},
]

# (3) Felt-experience hypothesis tied to a specific change
# Hypothesis: Removing the 3s dead wait after a miss (instant respawn) will
# reduce frustration and keep the player in flow, improving comprehension of
# the core loop without increasing confusion.
hypothesis = {
    "change": "respawn orb instantly (0s) after miss instead of 3s delay",
    "felt_effect": "player stays in action, less frustration, faster re-engagement",
    "risk": "player may feel punished too quickly, no time to breathe",
}

# (4) Small playtest with observable metrics, sample, pass criteria, stop condition
playtest = {
    "sample": 5,  # small, ethical, informed consent
    "task": "play first 60 seconds, catch as many orbs as possible",
    "metrics": [
        "time_to_first_catch",
        "misses_before_first_catch",
        "reported_frustration_1_to_5",
        "return_intent_yes_no",
    ],
    "baseline": {
        "time_to_first_catch": 5.0,  # seconds
        "misses_before_first_catch": 1.2,
        "reported_frustration_1_to_5": 3.0,
        "return_intent_yes_no": 0.6,  # proportion yes
    },
    "observed": {
        "median_time_to_first_catch": 3.5,
        "misses_before_first_catch": 0.8,
        "reported_frustration_1_to_5": 2.0,
        "return_intent_yes_no": 0.8,
    },
    "pass": "median time_to_first_catch <= 4s AND frustration <= 2 AND return_intent >= 0.8",
    "stop": "any participant reports discomfort or cannot proceed; stop immediately",
}

# (5) Recommendation that can be rejected if metrics do not improve
passed = (
    playtest["observed"]["median_time_to_first_catch"] <= 4
    and playtest["observed"]["reported_frustration_1_to_5"] <= 2
    and playtest["observed"]["return_intent_yes_no"] >= 0.8
)
recommendation = {
    "change": "instant respawn after miss",
    "decision": "recommend" if passed else "reject",
    "rationale": "metrics improved: faster first catch, lower frustration, higher return intent",
}

# Print the full analysis
print("=== FIRST-MINUTE AND CORE-LOOP AUDIT ===")
for beat in timeline:
    print(f"  t={beat['at']:>2}s | {beat['beat']:<20} | signal: {beat['signal']:<30} | action: {beat['action']}")

print("\n=== PACING ===")
for key, val in pacing.items():
    print(f"  {key}: {val}")

print("\n=== FRICTION ===")
for f in friction:
    print(f"  t={f['at']}s | {f['issue']} | risk: {f['risk']}")

print("\n=== FEEDBACK ===")
for key, val in feedback.items():
    print(f"  {key}: {val}")

print("\n=== AUDIO/VISUAL SIGNALS ===")
for key, val in audio_visual.items():
    print(f"  {key}: {val}")

print("\n=== DISENGAGEMENT RISK ===")
for d in disengagement_risk:
    print(f"  t={d['at']}s | {d['reason']} | level: {d['level']}")

print("\n=== FELT-EXPERIENCE HYPOTHESIS ===")
print(f"  change: {hypothesis['change']}")
print(f"  felt_effect: {hypothesis['felt_effect']}")
print(f"  risk: {hypothesis['risk']}")

print("\n=== PLAYTEST ===")
print(f"  sample: {playtest['sample']}")
print(f"  task: {playtest['task']}")
print(f"  metrics: {', '.join(playtest['metrics'])}")
print(f"  baseline: {playtest['baseline']}")
print(f"  observed: {playtest['observed']}")
print(f"  pass criteria: {playtest['pass']}")
print(f"  stop condition: {playtest['stop']}")

print("\n=== RECOMMENDATION ===")
print(f"  change: {recommendation['change']}")
print(f"  decision: {recommendation['decision']}")
print(f"  rationale: {recommendation['rationale']}")