# problem: We need a system that tracks a bank account's balance over time while
# maintaining a clear history of all transactions. The account has an owner and
# a balance that changes with deposits and withdrawals. We must avoid accidental
# complexity from mixing identity, state, and time in a mutable object.

# complected: A traditional mutable Account class where identity (the account
# object), state (balance), and time (transaction history) are braided together.
# This makes reasoning about past states difficult and introduces race conditions
# in concurrent scenarios.

# immutability choice: Use immutable Account values where each transaction
# produces a new Account instance. The one mutation point is the creation of
# new Account instances via deposit/withdraw methods. Old values remain
# accessible and unchanged, enabling clear reasoning about history.

# tradeoff table:
# 1. Mutable Account with history list
#    - Costs: Complex thread-safety, accidental state changes, hard to reason
#      about past states, requires defensive copying
#    - Benefits: Familiar OOP pattern, in-place updates feel "natural"
#
# 2. Immutable Account with persistent history
#    - Costs: New objects created on each change, potential memory overhead
#    - Benefits: Thread-safe by design, clear transaction history, easy to
#      debug, reasoning about state at any point in time

# reasoning artifact: The immutable design survived the hammock because:
# - It separates identity (the logical account) from state (balance at time T)
# - Time is explicit through the chain of Account values
# - No hidden mutations mean reasoning is always possible
# - The design scales better to concurrent scenarios
# - The tradeoff of memory for correctness is acceptable for this domain

from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class Account:
    owner: str
    balance: int
    previous: Optional['Account'] = None

    def deposit(self, amount: int) -> 'Account':
        """Return a new Account with updated balance, preserving history."""
        return Account(self.owner, self.balance + amount, self)

    def withdraw(self, amount: int) -> 'Account':
        """Return a new Account with updated balance if sufficient funds."""
        if amount > self.balance:
            raise ValueError("Insufficient funds")
        return Account(self.owner, self.balance - amount, self)

# Create initial account
initial = Account("Ada Lovelace", 100)

# Perform transactions
after_deposit = initial.deposit(50)
after_withdrawal = after_deposit.withdraw(30)

# Print results showing the chain of values
print(f"Initial balance: {initial.balance}")  # 100
print(f"After deposit: {after_deposit.balance}")  # 150
print(f"After withdrawal: {after_withdrawal.balance}")  # 120

# Demonstrate history access
current = after_withdrawal
while current is not None:
    print(f"Account at {current.balance} owned by {current.owner}")
    current = current.previous