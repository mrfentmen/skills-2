import cmath
import random

class Qubit:
    """
    A qubit in superposition: |ψ⟩ = α|0⟩ + β|1⟩
    where α and β are complex probability amplitudes.
    """
    def __init__(self):
        self.alpha = complex(1, 0)  # |0⟩ amplitude
        self.beta = complex(0, 0)   # |1⟩ amplitude
        self.measured = False

    def hadamard(self):
        """
        Apply Hadamard gate H to create superposition.
        H|0⟩ = (|0⟩ + |1⟩)/√2
        H|1⟩ = (|0⟩ - |1⟩)/√2
        """
        new_alpha = (self.alpha + self.beta) / (2 ** 0.5)
        new_beta = (self.alpha - self.beta) / (2 ** 0.5)
        self.alpha, self.beta = new_alpha, new_beta

    def measure(self):
        """
        Measure the qubit: collapses |ψ⟩ to |0⟩ or |1⟩ with probabilities |α|² and |β|².
        Returns 0 or 1.
        """
        prob_0 = abs(self.alpha) ** 2
        result = 0 if random.random() < prob_0 else 1
        self.measured = True
        self.alpha = complex(1, 0) if result == 0 else complex(0, 0)
        self.beta = complex(0, 0) if result == 0 else complex(1, 0)
        return result

    def __str__(self):
        return f"|ψ⟩ = {self.alpha:.3f}|0⟩ + {self.beta:.3f}|1⟩"

# Demonstration
if __name__ == "__main__":
    q = Qubit()
    print("Initial state:", q)

    q.hadamard()
    print("After Hadamard (superposition):", q)

    print("Measuring...")
    outcome = q.measure()
    print(f"Measurement result: {outcome}")
    print("Post-measurement state:", q)