import random
import math

class Qubit:
    """A single qubit in superposition: |ψ⟩ = α|0⟩ + β|1⟩"""
    def __init__(self, alpha=complex(1, 0), beta=complex(0, 0)):
        self.alpha = alpha  # amplitude for |0⟩
        self.beta = beta    # amplitude for |1⟩
        self.measured = False

    def normalize(self):
        """Ensure |α|² + |β|² = 1"""
        norm = math.sqrt(abs(self.alpha)**2 + abs(self.beta)**2)
        if norm > 0:
            self.alpha /= norm
            self.beta /= norm

    def hadamard(self):
        """Apply Hadamard gate: H = (1/√2)[[1,1],[1,-1]]"""
        new_alpha = (self.alpha + self.beta) / math.sqrt(2)
        new_beta = (self.alpha - self.beta) / math.sqrt(2)
        self.alpha, self.beta = new_alpha, new_beta
        self.normalize()

    def pauli_x(self):
        """Apply Pauli-X gate (quantum NOT): swaps |0⟩ and |1⟩"""
        self.alpha, self.beta = self.beta, self.alpha

    def pauli_z(self):
        """Apply Pauli-Z gate: flips phase of |1⟩"""
        self.beta = -self.beta

    def phase(self, theta):
        """Apply phase gate: |1⟩ → e^{iθ}|1⟩"""
        self.beta *= complex(math.cos(theta), math.sin(theta))

    def measure(self):
        """Collapse the wave function: returns 0 or 1 with probability |α|², |β|²"""
        prob_0 = abs(self.alpha)**2
        result = 0 if random.random() < prob_0 else 1
        self.measured = True
        if result == 0:
            self.alpha, self.beta = complex(1, 0), complex(0, 0)
        else:
            self.alpha, self.beta = complex(0, 0), complex(1, 0)
        return result

    def __str__(self):
        return f"|ψ⟩ = {self.alpha:.3f}|0⟩ + {self.beta:.3f}|1⟩"

# Demonstrate superposition
q = Qubit()
print("Initial state:", q)
q.hadamard()  # Create superposition
print("After Hadamard:", q)
print("Probability of |0⟩:", abs(q.alpha)**2)
print("Probability of |1⟩:", abs(q.beta)**2)

# Apply another gate to show interference
q.pauli_z()
print("After Pauli-Z:", q)

# Measure and show collapse
result = q.measure()
print(f"Measurement result: {result}")
print("Post-measurement state:", q)