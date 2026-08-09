# what this changes: the user authors conversations, not just programs
# medium statement: people stop thinking in terms of data flow and start thinking in terms of living conversations between autonomous actors

# message-passing design: every interaction is a message sent to an object; no object ever exposes its state, only behavior
class Actor:
    def __init__(self, name):
        self._name = name
        self._mailbox = []

    def receive(self, msg):
        self._mailbox.append(msg)

    def ask(self, target, verb, *args):
        target.receive((self._name, verb, args))
        return self

    def step(self):
        if not self._mailbox:
            return None
        sender, verb, args = self._mailbox.pop(0)
        if verb == "greet":
            return f"{self._name} greets {sender}"
        if verb == "compute":
            return f"{self._name} computes {args[0]}"
        raise ValueError(f"unknown verb: {verb}")

# perspective note: the metaphor is a lively coffeehouse where ideas travel as spoken messages; it replaces the factory assembly line of data processing

# range proof:
# simple path shown simple: two actors exchange greetings in one line
# complex path shown possible: actors can chain computations and forward results

# future claim: twenty years from now every user will routinely author distributed conversations as naturally as they now author documents

alice = Actor("Alice")
bob = Actor("Bob")

alice.ask(bob, "greet")
bob.ask(alice, "compute", 42)

print(alice.step())
print(bob.step())