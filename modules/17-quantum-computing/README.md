# Quantum Computing

This module introduces quantum computing from first principles through algorithmic consequences and deployment reality. It is organized to prevent the common mistake of starting with headline speedups before the reader understands qubits, circuits, measurement, and hardware constraints.

## Why This Module Matters

Quantum computing changes how computation is modeled by representing information with amplitudes, phases, and entangled states. It matters not because it speeds up everything, but because it changes the known complexity of specific important problems and forces more careful thinking about information, measurement, and physical limits.

## Recommended Reading Path

1. [Qubits, Superposition, and Measurement](01-concepts/01-qubits-superposition-and-measurement.md)
2. [Quantum Gates and the Circuit Model](01-concepts/02-quantum-gates-and-circuit-model.md)
3. [Entanglement, Interference, and the No-Cloning Principle](01-concepts/03-entanglement-interference-and-no-cloning.md)
4. [Quantum Complexity and Circuit Costs](01-concepts/04-quantum-complexity-and-circuit-costs.md)
5. [Noise, Error Correction, and Fault Tolerance](01-concepts/05-noise-error-correction-and-fault-tolerance.md)
6. [Quantum Algorithms Intro](01-concepts/06-quantum-algorithms-intro.md)
7. [Quantum Fourier Transform and Phase Estimation](01-concepts/07-quantum-fourier-transform-and-phase-estimation.md)
8. [Quantum Information, Communication, and Cryptography](01-concepts/08-quantum-information-communication-and-cryptography.md)

## Module Map

- [Concepts](01-concepts/README.md): the main conceptual path through quantum information and computation
- [Cheatsheets](02-cheatsheets/README.md): compact reminders for notation, gates, and complexity language
- [Python Implementations](03-implementations/python/README.md): a future home for simulation and teaching utilities
- [TypeScript Implementations](03-implementations/typescript/README.md): a future home for browser-based visualizations
- [Case Studies](04-case-studies/README.md): scenario-driven applications and tradeoff discussions
- [Exercises](05-exercises/README.md): derivations, small simulations, and algorithm reasoning prompts
- [Notes](06-notes/README.md): supporting observations and follow-up material

## Suggested Workflow

1. Learn the first three pages as the physical and mathematical language of the module.
2. Use the complexity and noise pages as a reality check before reading algorithmic speedup claims.
3. Read the algorithms page and QFT page together if the goal is to understand the structure behind Shor-like results.
4. End with communication and cryptography to connect quantum ideas back to systems impact.

## Prerequisites

- comfort with basic linear algebra and complex-number notation
- willingness to reason carefully about probability and state transformation
- interest in the boundary between theoretical models and hardware constraints
