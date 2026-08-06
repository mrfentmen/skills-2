# quantum-computing

[![Audit & Package](https://github.com/mrfentmen/quantum-computing/actions/workflows/audit-and-package.yml/badge.svg)](https://github.com/mrfentmen/quantum-computing/actions)

A coding skill: Write code that embodies quantum mechanics: superposition, entanglement, quantum gates, and probabilistic measurement. Use this skill when the user wants quantum-inspired or quantum-simulating code. Triggers on requests for: "quantum", "qubit", "superposition", "entanglement", "quantum gate", "Hadamard", "Bell state", "wave function", "Schrodinger". Also triggers when the user wants probability amplitudes, complex coefficients, or measurement collapse. Make sure to use this skill whenever the user mentions quantum computing or quantum-inspired patterns. This skill is NOT for psychedelic or emergent aesthetics (use psych) and NOT for pure-classical probability problems.

## Usage

Ask your AI to write code in this style. For example:

> Write a quantum computing simulator with qubits and gates

A taste of what it produces (from the skill's own examples):

```python
class Qubit:
    """
    A qubit exists in superposition until measured.
    "The qubit is the atom of quantum information."
    """
    def __init__(self):
        self.alpha = complex(1, 0)  # |0⟩ amplitude
        self.beta = complex(0, 0)   # |1⟩ amplitude
        self.measured = False
        
    def hadamard(self):
        """Apply Hadamard gate - create superposition"""
        # H = (1/√2) [[1, 1], [1, -1]]
        new_alpha = (self.alpha + self.beta) / (2 ** 0.5)
        new_beta = (self.alpha - self.beta) / (2 ** 0.5)
        self.alpha, self.beta = new_alpha, new_beta
        
    def measure(self):
        """
        Measure the qubit - collapse the wave function.
…
```

## What's inside

- `SKILL.md`: the skill definition (philosophy, patterns, boundaries, checkable requirements)
- `evals/`: eval cases
- `quantum-computing.skill`: packaged single-file skill
- `shared/`: helper modules (ASCII canvas, box drawing, RNG)
- `.github/workflows/audit-and-package.yml`: CI: static audit + repackage on every push (bad quality fails the run; refreshed artifacts are committed back). Status is shown by the badge at the top of this README.

## Install

Place this folder in your skills directory, or load the packaged `quantum-computing.skill`:

- **Codex**: `.codex/skills/`
- **Freebuff**: `.agents/skills/`

