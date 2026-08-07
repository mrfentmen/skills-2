---
name: quantum-computing
description: >-
  Write code that embodies quantum mechanics: superposition, entanglement, quantum gates,
  and probabilistic measurement. Use this skill when the user wants quantum-inspired or
  quantum-simulating code. Triggers on requests for: "quantum", "qubit", "superposition",
  "entanglement", "quantum gate", "Hadamard", "Bell state", "wave function",
  "Schrodinger". Also triggers when the user wants probability amplitudes, complex
  coefficients, or measurement collapse. Make sure to use this skill whenever the user
  mentions quantum computing or quantum-inspired patterns. This skill is NOT for
  psychedelic or emergent aesthetics (use psych) and NOT for pure-classical probability
  problems.
---

# Quantum Computing Skill

Embrace the strange and beautiful world of quantum mechanics in code! This skill creates programs that embody quantum principles: superposition, entanglement, interference, and measurement.

## Philosophy

"Quantum computing is not about making computers faster, it's about making them think differently."

The quantum mindset:
1. **Superposition**: Things can be in multiple states at once
2. **Entanglement**: Distant particles can be mysteriously connected
3. **Interference**: Waves can amplify or cancel each other
4. **Measurement**: Observation collapses possibilities into reality
5. **Uncertainty**: Some properties cannot be known simultaneously

## Core Patterns

### Qubit Representation
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
        "Measurement is the moment of truth."
        """
        import random
        prob_0 = abs(self.alpha) ** 2
        result = 0 if random.random() < prob_0 else 1
        self.measured = True
        self.alpha = complex(1, 0) if result == 0 else complex(0, 0)
        self.beta = complex(0, 0) if result == 0 else complex(1, 0)
        return result
```

### Quantum Gates
```python
def pauli_x(qubit):
    """Pauli-X gate (quantum NOT)"""
    qubit.alpha, qubit.beta = qubit.beta, qubit.alpha

def pauli_z(qubit):
    """Pauli-Z gate (phase flip)"""
    qubit.beta = -qubit.beta

def cnot(control, target):
    """CNOT gate - entanglement creator"""
    if abs(control.alpha) ** 2 < 0.5:  # If control is |1⟩
        target.alpha, target.beta = target.beta, target.alpha
```

### Entanglement
```python
def create_bell_state():
    """
    Create a Bell state - maximally entangled qubits.
    "Entanglement is the universe's way of being non-local."
    """
    q1, q2 = Qubit(), Qubit()
    q1.hadamard()
    cnot(q1, q2)
    return q1, q2
```

## Boundaries, when NOT to use this skill (use a different skill instead)

This skill is **not for** every request in its neighborhood. When the user
asks for one of the following, **instead use** the listed skill, the goal is
that two skills never coin-flip on the same prompt:

- - psychedelic / emergent aesthetics -> psych
- elegant pure-math code -> mathematical-elegance
- classical probability only -> no theme skill needed

The point of these lines is not to be restrictive, it is so that two skills
never coin-flip on the same prompt. If two skills could both claim a request,
pick the one whose name matches the dominant theme and say so in your reply.


## Minimum Requirements (checkable)

Every deliverable produced with this skill should be gradeable. You must
include ALL of the following so a reviewer can check them without judgment
calls:

- a qubit representation with amplitudes (complex numbers or alpha/beta pairs)
- at least 1 quantum gate (Hadamard, Pauli, CNOT, phase)
- superposition and/or entanglement demonstrated
- Dirac notation or wave-function vocabulary in comments (|0>, |1>, |psi>)
- no mock, fake, or pseudo code: every line is real, runs, and does the actual work

These requirements exist because a theme without a spec produces vibes, not
output. They also keep the skill's own evaluations meaningful.


## When to Use Quantum Patterns

Use quantum-inspired code when:
- Modeling uncertainty and probability
- Simulating parallel possibilities
- Creating algorithms that explore multiple paths simultaneously
- Building systems that embrace observation-dependent reality
- Writing code that thinks in waves, not bits

## Examples of Quantum Thinking

1. **Quantum Random Walk**: A random walk where the walker exists in superposition of all positions
2. **Quantum Search**: Grover's algorithm that searches by amplifying correct answers
3. **Quantum Simulation**: Simulating quantum systems with classical code
4. **Quantum-Inspired Optimization**: Using quantum principles for classical optimization

## The Quantum Aesthetic

Write code that:
- Uses complex numbers for amplitudes
- Includes probability calculations
- References quantum mechanics concepts
- Embraces uncertainty and measurement
- Uses wave function metaphors
- Includes Dirac notation in comments: |0⟩, |1⟩, ⟨ψ|

Remember: "In quantum computing, the journey is the destination, the superposition of paths is more beautiful than any single solution."

## Cross-Language Examples

The patterns above are Python-first, but the theme is language-agnostic. Here
is the same spirit in JavaScript and Rust:

```javascript
// |psi> = a|0> + b|1>
class Qubit {
  constructor() { this.a = [1, 0]; } // amplitudes in |0>, |1>
  hadamard() {
    const [a, b] = this.a;
    this.a = [(a + b) / Math.SQRT2, (a - b) / Math.SQRT2];
  }
}
```

```rust
// Superposition until measured
struct Qubit { alpha: f64, beta: f64 }
impl Qubit {
    fn hadamard(&mut self) {
        let (a, b) = (self.alpha, self.beta);
        let s = std::f64::consts::SQRT_2;
        self.alpha = (a + b) / s; self.beta = (a - b) / s;
    }
}
```

If the user is working in another language (Go, C, Bash, TypeScript...),
translate the same patterns, the theme lives in structure and vocabulary, not
in one language.

## Bundled Helpers

This skill shares a small toolkit with the other themed skills. When your
output needs ASCII rendering, line drawing, decorative headers, or randomness,
reuse these instead of rewriting them from scratch:

- `shared/ascii_canvas.py`, ASCII canvas with Bresenham lines, circles,
  rectangles, and ink-density characters (█ ▓ ▒ ░)
- `shared/box_drawing.py`, box-drawing headers and sections (╔══╗ ║ ╚══╝)
- `shared/rng.py`, seeded RNG, gaussian/choice helpers, and value noise

Reference them from the code you produce (copy the relevant function into the
answer, or point to the file) so every themed skill outputs consistent,
non-reinvented helpers.

