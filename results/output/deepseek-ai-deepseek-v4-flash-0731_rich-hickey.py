# problem: We need to model a bank account balance that changes over time via deposits and withdrawals.
# The naive approach braids identity (the account), state (the current balance), and time (the sequence of changes)
# into one mutable object, making it impossible to reason about past values or share snapshots safely.

# de-complection pass: identity is the account (stable logical entity), state is the immutable balance value at a
# given moment, time is the sequence of states produced by operations. These are separated: the account never mutates,
# each operation produces a new state value, and the timeline is the ordered collection of those values.

# immutability choice: Account is a frozen dataclass — its balance is a value, shared freely without mutation.
# The single mutation point is the `accounts` dictionary in the Bank class, which atomically rebinds an identity
# to a new state value. No other mutation exists.

# tradeoff table:
# | Alternative                    | Cost                                                                 |
# |--------------------------------|----------------------------------------------------------------------|
# | Mutable account object         | History lost, concurrent access needs locks, reasoning about time impossible |
# | Immutable value + identity map | Slight allocation overhead, but full history, thread-safe sharing, explicit time |

# reasoning artifact: The hammock design survived because it treats the account as an identity bound to a timeline
# of immutable values. The first instinct (a mutable class with deposit/withdraw methods) was rejected because it
# complects time and state — the final design keeps the bank as the only place where time advances.

from dataclasses import dataclass
from typing import Dict

@dataclass(frozen=True)
class Account:
    owner: str
    balance: int

    def deposit(self, amount: int) -> "Account":
        return Account(self.owner, self.balance + amount)

    def withdraw(self, amount: int) -> "Account":
        if amount > self.balance:
            raise ValueError("Insufficient funds")
        return Account(self.owner, self.balance - amount)

class Bank:
    def __init__(self) -> None:
        # The one mutation point: identity -> current state
        self._accounts: Dict[str, Account] = {}

    def open(self, owner: str, initial: int) -> None:
        self._accounts[owner] = Account(owner, initial)

    def deposit(self, owner: str, amount: int) -> None:
        current = self._accounts[owner]
        self._accounts[owner] = current.deposit(amount)

    def withdraw(self, owner: str, amount: int) -> None:
        current = self._accounts[owner]
        self._accounts[owner] = current.withdraw(amount)

    def balance(self, owner: str) -> int:
        return self._accounts[owner].balance

bank = Bank()
bank.open("ada", 100)
bank.deposit("ada", 25)
bank.withdraw("ada", 10)
print(bank.balance("ada"))  # 115