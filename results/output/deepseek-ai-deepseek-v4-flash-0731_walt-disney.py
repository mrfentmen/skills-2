# the ideal: a tiny interactive story that feels alive — choices ripple, the world remembers, and the user forgets they're reading text
# the plan: 3 modules — a story graph, a state engine, a renderer; the graph is data, the engine mutates state, the renderer prints; no deps, no I/O
# the critique: infinite loops if graph cycles, dead ends if no next node, state bleed between runs, user confusion if choices are ambiguous — each guarded by a max-step cap, a terminal check, fresh state per run, and explicit choice labels
# plussing: beyond a bare choose-your-own-adventure, the story now tracks a "mood" that changes the flavor of later text, and the ending reflects the user's cumulative choices — not just the last one
# story test: every node exists to push the user's emotional arc — the mood system exists so the user feels their choices matter; if a node didn't serve that, it would be cut

class StoryNode:
    def __init__(self, text, choices=None, mood_delta=0, terminal=False):
        self.text = text
        self.choices = choices or {}  # {label: (next_node_id, mood_delta)}
        self.mood_delta = mood_delta
        self.terminal = terminal

class StoryEngine:
    def __init__(self, graph, start):
        self.graph = graph
        self.current = start
        self.mood = 0  # -2..2: gloomy to radiant
        self.steps = 0
        self.max_steps = 10

    def run(self, scripted_choices):
        # scripted choices: a list of labels to pick, embedded as variables — no input()
        for choice_label in scripted_choices:
            if self.steps >= self.max_steps:
                print("...the tale fades into mist (step cap reached)")
                return
            node = self.graph[self.current]
            if node.terminal:
                break
            print(f"\n{node.text}")
            print("Choices: " + ", ".join(node.choices.keys()))
            if choice_label not in node.choices:
                print(f"  (scripted choice '{choice_label}' not found — defaulting to first)")
                choice_label = next(iter(node.choices))
            next_id, mood_delta = node.choices[choice_label]
            self.mood = max(-2, min(2, self.mood + mood_delta))
            self.current = next_id
            self.steps += 1
        # render the ending with mood-aware flavor
        node = self.graph[self.current]
        print(f"\n{node.text}")
        if self.mood >= 1:
            print("The warmth of your choices lingers like a golden sunset.")
        elif self.mood <= -1:
            print("A chill follows your path — the forest remembers your shadows.")
        else:
            print("The balance holds, neither bright nor dark, but yours.")

def build_story():
    # the real: a small graph — 5 nodes, 4 choices, 1 terminal, mood deltas on each edge
    return {
        "start": StoryNode(
            "You stand at the edge of the Whispering Woods.",
            {"enter": ("clearing", 1), "turn back": ("home", -1)}
        ),
        "clearing": StoryNode(
            "A fox offers a glowing berry.",
            {"take": ("cave", 1), "decline": ("river", 0)}
        ),
        "river": StoryNode(
            "The river whispers a riddle.",
            {"answer": ("cave", 1), "ignore": ("home", -1)}
        ),
        "cave": StoryNode(
            "Inside, a mirror shows your reflection — but it smiles back.",
            {"touch": ("end", 1), "leave": ("home", -1)}
        ),
        "home": StoryNode(
            "You return home, the woods behind you.",
            terminal=True
        ),
        "end": StoryNode(
            "The mirror dissolves into light, and you carry the forest's secret.",
            terminal=True
        ),
    }

def main():
    # the demo: scripted choices as variables — zero interactive input, terminates on its own
    graph = build_story()
    engine = StoryEngine(graph, "start")
    engine.run(["enter", "take", "touch"])  # a bright path
    print("\n--- second run: a darker path ---")
    engine2 = StoryEngine(graph, "start")
    engine2.run(["turn back"])  # early exit, mood negative

main()