# Quantum Algorithms Intro

## What it is

Quantum algorithms exploit superposition and interference to solve specific
problems faster than known classical algorithms.

## Why it matters

They reshape complexity assumptions for tasks like unstructured search and
integer factoring, with practical impacts on security and optimization.

## Core idea (intuition)

Quantum states encode many possibilities at once; operations amplify the
probability of correct outcomes through interference.

## Formal definition

A quantum algorithm applies unitary operations to qubits, followed by
measurement that samples a probability distribution over outcomes.

## Patterns / common techniques

- Amplitude amplification (Grover)
- Period finding and Fourier transforms (Shor)
- Oracle-based models and query complexity

## Complexity notes

- Grover: O(sqrt(N)) queries for search
- Shor: polynomial time for factoring (theoretical)

## Pitfalls

- Assuming quantum speedups apply to all problems
- Ignoring overheads and error correction costs

## References

- Nielsen and Chuang, Quantum Computation and Quantum Information
- Aaronson, Quantum Computing Since Democritus
