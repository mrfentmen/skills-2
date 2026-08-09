def launch_plan():
    # (1) user statement: first users are the 3 solo indie hackers who asked for
    # "a CLI that turns my messy meeting notes into a single TODO list, nothing more"
    first_users = [
        {"name": "ana", "ask": "merge my daily notes into one TODO list"},
        {"name": "ben", "ask": "same, but keep the source file names"},
        {"name": "cat", "ask": "just the TODOs, no fluff"},
    ]

    # (2) non-scalable move: manually edit their first output by hand today
    #     — send each user a personalized diff showing their exact TODOs merged
    def manual_delight(user):
        return f"hand-edited {user['name']}'s first merged TODO list and emailed the diff"

    # (3) launch gate: ships when it correctly merges 2+ note files into one
    #     TODO list for a single real user — that's the quantum of utility
    def launch_gate(notes):
        return len(notes) >= 2 and all("TODO" in n for n in notes)

    # (4) narrow focus: only plain-text .md files in one folder, no subdirs,
    #     no config, no install — just `merge-todos *.md`
    narrow_focus = "single folder of .md files, zero config, one command"

    # (5) redesign pass: v1 parsed JSON config and supported nested folders —
    #     users ignored it. After talking to them, we threw it away and rebuilt
    #     as a zero-config glob. Worth it: the real ask was "just work on my notes"
    redesign_note = (
        "v1 had config + recursion; users never used it. "
        "Rebuilt as zero-config glob after 2 user calls — worth the throwaway"
    )

    # demo
    notes = ["meeting1.md: TODO fix login bug", "meeting2.md: TODO ship v0.1"]
    shipped = launch_gate(notes)
    plan = {
        "first_users": [u["name"] for u in first_users],
        "non_scalable_move": [manual_delight(u) for u in first_users],
        "launch_gate_met": shipped,
        "narrow_focus": narrow_focus,
        "redesign_pass": redesign_note,
    }
    return plan

plan = launch_plan()
for key, value in plan.items():
    print(f"{key}: {value}")

# demo: show the actual merge working
def merge_todos(files):
    todos = []
    for f in files:
        for line in f.splitlines():
            if "TODO" in line:
                todos.append(line.split("TODO ", 1)[1])
    return todos

print("\ndemo merge:", merge_todos([
    "meeting1.md: TODO fix login bug",
    "meeting2.md: TODO ship v0.1",
]))