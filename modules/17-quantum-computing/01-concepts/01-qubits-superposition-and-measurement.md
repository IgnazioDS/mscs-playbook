# Qubits, Superposition, and Measurement

## Key Ideas
- A qubit is a two-level quantum system whose state is described by complex amplitudes rather than a single classical bit value.
- Superposition means a qubit can be in a linear combination of basis states, but measurement produces only one classical outcome sampled from the amplitude magnitudes.
- Quantum state evolution is linear and reversible until measurement, which is why amplitudes and phases matter.
- The probability of a measurement outcome is the squared magnitude of its amplitude, not the amplitude itself.
- A correct quantum-computing mental model begins with state representation and measurement rules, not with vague claims about parallelism.

## 1. Why quantum information is different

Classical computation represents information with bits that are either `0` or `1`. Quantum computation represents information with **qubits**, which are physical systems described by quantum mechanics. The important difference is not that a qubit is "both `0` and `1`" in a casual sense. The real difference is that a qubit is a vector in a complex state space, and operations transform that vector linearly.

This matters because later quantum algorithms rely on engineering amplitudes and phases so that measurement is likely to reveal useful information.

## 2. Basis states and superposition

The standard computational basis for one qubit is:

- `|0>`
- `|1>`

A general one-qubit state is:

`|psi> = alpha|0> + beta|1>`

where `alpha` and `beta` are complex numbers satisfying:

`|alpha|^2 + |beta|^2 = 1`

This normalization condition ensures total measurement probability is `1`.

A **superposition** is any state where both amplitudes are present. The amplitudes are not probabilities directly. They are complex coefficients whose squared magnitudes determine probabilities.

## 3. Measurement and probabilistic outcomes

Measuring `|psi> = alpha|0> + beta|1>` in the computational basis gives:

- outcome `0` with probability `|alpha|^2`
- outcome `1` with probability `|beta|^2`

After measurement, the state collapses to the observed basis state in the idealized model.

This is why quantum computation cannot simply "read out every branch." The algorithm can manipulate many amplitudes coherently, but only a sampled classical outcome is observed at the end.

## 4. Worked example: one-qubit measurement probabilities

Suppose:

`|psi> = (sqrt(3)/2)|0> + (1/2)|1>`

Check normalization:

`|sqrt(3)/2|^2 + |1/2|^2 = 3/4 + 1/4 = 1`

So the state is valid.

Measurement probabilities:

- outcome `0`: `3/4`
- outcome `1`: `1/4`

Now suppose we measure the qubit and observe `1`. In the idealized projective model, the state after that measurement becomes:

`|1>`

If we immediately measure again in the same basis, the outcome `1` now occurs with probability `1`.

Verification: the probabilities sum to `1`, and repeated measurement after collapse returns the observed basis state deterministically in the same basis.

## 5. Why this page comes before gates and algorithms

Without a correct model of superposition and measurement, later claims about Hadamard gates, interference, Grover's search, or phase estimation become misleading. This page therefore belongs first: the rest of the module depends on understanding that amplitudes are manipulated before probabilities are observed.

## 6. Common Mistakes

1. **Parallel-world metaphor misuse**: saying a qubit "stores both answers at once" hides the role of amplitudes and measurement; use vector and probability language instead.
2. **Amplitude-probability confusion**: treating amplitudes as probabilities leads to wrong calculations; square magnitudes to get measurement probabilities.
3. **Measurement-overread**: assuming all superposed information is directly readable ignores collapse; only one classical outcome is obtained per measurement.
4. **Normalization neglect**: forgetting the amplitudes must satisfy total probability `1` breaks the state model; verify normalization before interpreting a state.
5. **Classical-bit substitution**: reasoning about qubits as if they were uncertain classical bits misses phase and interference effects; keep the linear-algebra model explicit.

## 7. Practical Checklist

- [ ] Write one-qubit states explicitly in the computational basis before reasoning about them.
- [ ] Check normalization whenever amplitudes are introduced or transformed.
- [ ] Convert amplitudes to probabilities by squaring magnitudes, not by reading coefficients directly.
- [ ] Distinguish the pre-measurement state from the post-measurement collapsed state.
- [ ] Avoid informal metaphors when a short amplitude calculation is clearer.
- [ ] Treat measurement as the bridge from quantum state to classical output.

## References

1. Michael A. Nielsen and Isaac L. Chuang, *Quantum Computation and Quantum Information*. [https://doi.org/10.1017/CBO9780511976667](https://doi.org/10.1017/CBO9780511976667)
2. John Watrous, *The Theory of Quantum Information*. [https://doi.org/10.1017/9781316848142](https://doi.org/10.1017/9781316848142)
3. MIT OpenCourseWare, *Quantum Computation Lecture Notes*. [https://ocw.mit.edu/](https://ocw.mit.edu/)
4. Scott Aaronson, *Quantum Computing Since Democritus*. [https://doi.org/10.1017/CBO9780511979309](https://doi.org/10.1017/CBO9780511979309)
5. IBM Quantum Learning, *Qubits and Measurement*. [https://learning.quantum.ibm.com/](https://learning.quantum.ibm.com/)
6. John Preskill, *Lecture Notes for Physics 219/Computer Science 219*. [https://theory.caltech.edu/~preskill/ph219/](https://theory.caltech.edu/~preskill/ph219/)
7. Umesh Vazirani, *Quantum Computation Notes*. [https://people.eecs.berkeley.edu/~vazirani/quantum.html](https://people.eecs.berkeley.edu/~vazirani/quantum.html)
