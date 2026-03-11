# Quantum Gates and the Circuit Model

## Key Ideas
- Quantum computation is commonly described with circuits made of qubits, gates, and measurements.
- Quantum gates are unitary transformations, which means they are reversible linear operations on the quantum state.
- Single-qubit gates change amplitudes and phases, while multi-qubit gates create correlations needed for nonclassical behavior.
- Circuit depth and qubit count both matter because physical quantum devices have limited coherence and noisy operations.
- The circuit model is useful because it gives a concrete way to reason about algorithms as sequences of state transformations.

## 1. Why the circuit model matters

After defining qubits, the next question is how they are manipulated. The standard answer is the **quantum circuit model**, which describes a computation as:

- qubits prepared in an initial state
- unitary gates applied in sequence
- measurements at the end or at controlled intermediate points

This model is not the only one in quantum computing, but it is the dominant language for algorithms and hardware-independent reasoning.

## 2. Gates as unitary operations

A quantum gate is represented mathematically by a **unitary matrix**, meaning a complex matrix `U` satisfying:

`U* U = I`

where `U*` is the conjugate transpose.

Unitary operations preserve normalization and are reversible. Common one-qubit gates include:

- `X`, analogous to a bit flip
- `Z`, a phase flip
- `H` (Hadamard), which creates balanced superpositions from basis states

A key consequence is that purely quantum evolution is reversible even when the algorithm later produces a probabilistic classical result after measurement.

## 3. Circuits, depth, and resource thinking

A **quantum circuit** arranges gates into time-ordered layers. Two central resource measures are:

- **qubit count**, the number of quantum registers needed
- **circuit depth**, the number of sequential layers of gates

Theoretical asymptotic analyses often focus on gate count, but practical execution is also constrained by noise, error rates, and coherence time. A shallow circuit may be much more realistic than a deep one with the same asymptotic complexity.

## 4. Worked example: applying a Hadamard then an X gate

Start with the basis state:

`|0>`

Apply the Hadamard gate:

`H|0> = (1/sqrt(2))(|0> + |1>)`

Now apply the `X` gate, which swaps `|0>` and `|1>`:

`X[(1/sqrt(2))(|0> + |1>)] = (1/sqrt(2))(|1> + |0>)`

Reordering terms:

`(1/sqrt(2))(|0> + |1>)`

So the state is unchanged by `X` in this specific case because the superposition is symmetric between `|0>` and `|1>`.

Measurement probabilities remain:

- `1/2` for `0`
- `1/2` for `1`

Verification: the final state is the same balanced superposition as after the Hadamard, so both measurement outcomes still occur with probability `1/2`.

## 5. Why this page comes before entanglement and algorithms

Quantum algorithms are built from gates. Entanglement, interference, oracle design, and algorithmic speedups all rely on understanding how circuit steps transform the state. This page therefore defines the operational language that later pages use.

## 6. Common Mistakes

1. **Irreversibility assumption**: treating quantum gates like arbitrary classical instructions misses the unitary constraint; remember that gates must preserve normalization and reversibility.
2. **Gate-count tunnel vision**: focusing only on asymptotic gate count ignores depth and hardware limits; include qubit count and circuit depth in practical reasoning.
3. **Matrix-avoidance confusion**: avoiding the linear-algebra meaning of gates makes phase and interference harder to understand; connect gate symbols to transformations explicitly.
4. **Classical-logic analogy overuse**: thinking of quantum circuits as ordinary Boolean circuits with strange bits leads to errors; measurement and superposition change the model fundamentally.
5. **Resource-claim inflation**: calling a circuit practical based only on small gate counts ignores noise and coherence constraints; separate theoretical resource counts from hardware feasibility.

## 7. Practical Checklist

- [ ] Interpret each gate as a state transformation, not just a circuit icon.
- [ ] Track both qubit count and depth when discussing circuit cost.
- [ ] Use simple state-vector calculations on one or two qubits to build intuition.
- [ ] Distinguish reversible quantum evolution from irreversible measurement.
- [ ] Avoid translating every gate into a classical analogy if the analogy hides phase behavior.
- [ ] Treat the circuit diagram as a precise computational model, not just a teaching illustration.

## References

1. Michael A. Nielsen and Isaac L. Chuang, *Quantum Computation and Quantum Information*. [https://doi.org/10.1017/CBO9780511976667](https://doi.org/10.1017/CBO9780511976667)
2. John Preskill, *Lecture Notes for Physics 219/Computer Science 219*. [https://theory.caltech.edu/~preskill/ph219/](https://theory.caltech.edu/~preskill/ph219/)
3. John Watrous, *The Theory of Quantum Information*. [https://doi.org/10.1017/9781316848142](https://doi.org/10.1017/9781316848142)
4. IBM Quantum Learning, *Quantum Circuits and Gates*. [https://learning.quantum.ibm.com/](https://learning.quantum.ibm.com/)
5. Scott Aaronson, *Quantum Computing Since Democritus*. [https://doi.org/10.1017/CBO9780511979309](https://doi.org/10.1017/CBO9780511979309)
6. MIT OpenCourseWare, *Quantum Computation Materials*. [https://ocw.mit.edu/](https://ocw.mit.edu/)
7. Umesh Vazirani, *Quantum Computation Notes*. [https://people.eecs.berkeley.edu/~vazirani/quantum.html](https://people.eecs.berkeley.edu/~vazirani/quantum.html)
