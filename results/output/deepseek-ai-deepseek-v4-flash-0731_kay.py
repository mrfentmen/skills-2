# medium statement: this changes how people think about programs -- from a list of
# instructions to a conversation between living cells; the user authors dialogues, not flows.
# message-passing design: every component is a Cell with hidden state; the only way in is
# an explicit message (ask/tell). No getters, no reach-in, no shared mutable place.
# perspective note: the unifying metaphor is a biological cell / network node -- each unit
# is a sealed membrane that reacts to signals. This replaces the metaphor of a program as
# a recipe of steps operating on a global blackboard.
# range proof: the simple path is two cells exchanging one message (below, one line each);
# the complex path is a broker that routes messages between many cells, still with no
# internals exposed -- shown by the Router that composes cells without touching their state.
# future claim: the twenty-year bet is that late-bound, self-describing message systems
# will outlive today's framework pyramids -- that a medium where every object can be
# asked "what do you do?" and "who do you know?" will make software as malleable as
# human language, not as brittle as a stack of bricks.

class Cell:
    def __init__(self, name, value=0):
        self._name = name
        self._v = value
        self._peers = {}

    def ask(self, msg, *args):
        if msg == "name":
            return self._name
        if msg == "value":
            return self._v
        if msg == "add":
            self._v += args[0]
            return self._v
        if msg == "connect":
            self._peers[args[0]] = args[1]
            return f"{self._name} now knows {args[0]}"
        if msg == "send":
            peer_name, payload = args
            if peer_name not in self._peers:
                return f"{self._name} does not know {peer_name}"
            return self._peers[peer_name].ask("receive", self._name, payload)
        if msg == "receive":
            sender, payload = args
            self._v += payload
            return f"{self._name} got {payload} from {sender}; value now {self._v}"
        raise ValueError(f"no such message: {msg}")

# simple path: two cells, one message -- the whole system in three lines
alice = Cell("alice", 5)
bob = Cell("bob", 0)
print(alice.ask("connect", "bob", bob))
print(alice.ask("send", "bob", 3))

# complex path: a router that composes many cells, still message-only
class Router:
    def __init__(self):
        self._cells = {}

    def tell(self, name, msg, *args):
        if msg == "register":
            self._cells[name] = args[0]
            return f"registered {name}"
        if msg == "route":
            sender, target, payload = args
            if target not in self._cells:
                return f"no cell named {target}"
            return self._cells[target].ask("receive", sender, payload)
        raise ValueError(f"no such message: {msg}")

r = Router()
print(r.tell("a", "register", Cell("a", 10)))
print(r.tell("b", "register", Cell("b", 0)))
print(r.tell("a", "route", "a", "b", 7))
print("final values:", r.tell("a", "route", "a", "a", 0) if False else "hidden -- ask the cells")