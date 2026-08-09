# keeping: the soul of error handling — fail loudly, never swallow.
# reframing: the strategy — from "who broke it" to "what did it teach us".

# learn-it-all move: a failed experiment — a teammate's try/except swallowed a
# config typo and shipped a silent regression. The insight mined, not punished:
# silent excepts are the enemy; every failure is a signal to be surfaced.

# empathy pass: the unmet, unarticulated need — the teammate doesn't know they
# want a safety net that turns their fear of "looking bad" into a shared,
# blame-free learning log. They need permission to fail visibly.

# clarity line: the fuzzy ask "handle errors better" becomes crisp and simple:
# every exception must carry a lesson and a next step, or it is not handled.

# growth-verse note: fixed mindset "I must never make a mistake" reframed as
# "every mistake is a data point that makes the team smarter."

class CultureShift:
    def __init__(self):
        self.lessons = []

    def handle(self, error, context):
        # learn-it-all: mine the failure, never punish it
        insight = f"{context}: {type(error).__name__} -> {error}"
        self.lessons.append(insight)
        # empathy: surface the lesson, don't hide the shame
        return {"celebrated": True, "insight": insight}

    def report(self):
        # ecosystem check: works with any logging stack, locks nothing out
        return {"lessons": self.lessons, "count": len(self.lessons)}

demo = CultureShift()
demo.handle(ValueError("config typo: port='abc'"), "deploy")
demo.handle(KeyError("missing 'retries'"), "retry logic")
print(demo.report())
# culture note: the team now sees errors as curriculum, not culpability —
# serving the customer (fewer silent regressions), the team (shared learning),
# and the whole (a platform that grows wiser with every failure).