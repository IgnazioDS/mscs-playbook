# Quantum Algorithms Intro

## Key Ideas

- Quantum algorithms do not speed up arbitrary computation; they exploit specific algebraic or probabilistic structure using superposition, interference, and entanglement.
- The computational state of a quantum algorithm is not directly readable: measurement samples from a probability distribution, so algorithm design must amplify the probability of useful outcomes before measurement.
- Query-complexity speedups such as Grover’s `O(sqrt(N))` search improvement are real but narrower than the exponential speedups promised by special algorithms such as Shor’s factoring method.
- Quantum circuit cost is measured not just by asymptotic gate count, but also by qubit count, circuit depth, noise tolerance, and fault-tolerance overhead.
- A correct mental model treats quantum algorithms as structured linear-algebraic transformations on amplitudes, not as “trying all answers at once.”

## 1. What It Is

Quantum algorithms are algorithms designed for quantum computers. They manipulate **qubits** using reversible linear operations and then extract information through measurement.

Unlike classical bits, which are either `0` or `1`, a qubit can exist in a superposition of basis states. A system of multiple qubits is described by a complex-valued state vector whose amplitudes evolve under unitary transformations. Because amplitudes can interfere constructively or destructively, the algorithm can increase the probability of desirable outcomes and suppress undesirable ones.

This does not mean that every problem becomes easy on a quantum computer. Quantum advantage depends on whether the problem admits a structure that a quantum circuit can exploit.

### 1.1 Core Definitions

- A **qubit** is a two-level quantum system whose state is a unit vector in a two-dimensional complex vector space.
- A **basis state** for one qubit is usually written as `|0>` or `|1>`.
- A **superposition** is a linear combination of basis states with complex amplitudes.
- A **unitary operation** is a reversible linear transformation that preserves total probability.
- **Measurement** maps a quantum state to a classical outcome according to squared amplitude magnitudes.
- **Interference** is the reinforcement or cancellation of amplitudes caused by phase-sensitive combination of computational paths.
- An **oracle** is a black-box subroutine used in many query-complexity models.
- **Circuit depth** is the number of sequential gate layers required to run the computation.

### 1.2 Why This Matters

Quantum algorithms matter because they change the known complexity of certain problems. Shor’s algorithm shows that integer factoring and discrete logarithms are solvable in polynomial time on an ideal quantum computer, which directly affects classical public-key cryptography. Grover’s algorithm gives a quadratic speedup for unstructured search, which changes brute-force security estimates for symmetric cryptography.

They also matter because they force a more precise view of computation. Many claims about “massive parallelism” or “checking all solutions at once” are misleading. The real source of speedup is a carefully engineered transformation of amplitudes, followed by measurement. Understanding that distinction is essential for reading quantum algorithms correctly.

## 2. The Computational Model

### 2.1 State and Measurement

A one-qubit state has the form:

```text
|psi> = alpha|0> + beta|1>
```

where `alpha` and `beta` are complex numbers satisfying:

```text
|alpha|^2 + |beta|^2 = 1
```

Measurement in the computational basis returns:

- `0` with probability `|alpha|^2`
- `1` with probability `|beta|^2`

For multiple qubits, the state is a superposition over all basis strings. The number of amplitudes grows exponentially with the number of qubits, which is why classical simulation becomes difficult.

### 2.2 Reversible Evolution

Quantum computation evolves by unitary gates. Common examples include:

- **Hadamard** gates to create balanced superpositions,
- **phase** gates to change relative phases,
- **controlled** gates such as CNOT to create entanglement,
- and structured transforms such as the quantum Fourier transform.

Because the evolution is reversible until measurement, algorithm design often looks unlike classical branching logic.

### 2.3 Complexity Measures

Quantum algorithms are usually analyzed by:

- gate complexity,
- query complexity,
- qubit count,
- and depth.

In practice, asymptotic speedup alone is not enough. A theoretically fast algorithm may still be impractical if it needs too many logical qubits, too much fault tolerance, or too much coherent runtime.

## 3. Core Quantum Algorithm Patterns

### 3.1 Amplitude Amplification

Amplitude amplification increases the probability of measuring a marked or good state.

Grover’s search is the canonical example. Given an oracle that recognizes a target item among `N` possibilities, Grover’s algorithm finds it using `O(sqrt(N))` oracle queries, compared with `Theta(N)` classical queries in the unstructured setting.

The speedup is quadratic, not exponential. This is still important, especially for exhaustive search and cryptographic key search, but it does not make NP-hard problems generically easy.

### 3.2 Period Finding and Fourier Structure

Some quantum algorithms gain speed by exploiting hidden periodicity.

Shor’s factoring algorithm reduces factoring to order finding, then solves the order-finding subproblem using quantum phase estimation and the quantum Fourier transform. This yields polynomial-time factoring on an ideal quantum computer.

The key point is that the advantage comes from algebraic structure, not from a generic search over divisors.

### 3.3 Oracle and Query Models

Many quantum algorithms are described in the oracle model, where the cost of the black-box query is emphasized and other operations may be treated separately.

This model is useful because it isolates where the speedup comes from. But it can also mislead readers into ignoring the cost of implementing the oracle itself in a concrete system.

## 4. Grover and Shor at a Glance

### 4.1 Grover’s Algorithm

Grover’s algorithm solves unstructured search.

Problem form:

- there is a search space of size `N`,
- a black-box oracle identifies marked items,
- we want to find one marked item.

Classical query complexity:

```text
Theta(N)
```

Quantum query complexity:

```text
O(sqrt(N))
```

This is achieved by repeated Grover iterations, each of which rotates amplitude toward the marked subspace.

### 4.2 Shor’s Algorithm

Shor’s algorithm solves factoring and discrete logarithms in polynomial time on an ideal fault-tolerant quantum computer.

Its structure includes:

1. reduction from factoring to order finding,
2. coherent modular arithmetic,
3. quantum Fourier transform,
4. classical post-processing.

This is one of the most important examples of exponential quantum speedup over the best known classical algorithms for a practically relevant problem.

### 4.3 Practical Reality Check

Shor’s and Grover’s asymptotic statements describe idealized algorithmic performance. Practical deployment depends on error correction, logical qubit counts, gate fidelity, and hardware architecture.

**Why this matters:** a correct introduction to quantum algorithms must separate theoretical complexity results from current implementation feasibility.

## 5. Worked Example

We will trace the first step of Grover-style amplitude amplification for the smallest nontrivial case: searching among `N = 4` basis states with one marked item.

Suppose the marked state is:

```text
|10>
```

### 5.1 Start in Uniform Superposition

Apply Hadamard gates to both qubits, producing equal amplitude on all four basis states:

```text
|psi_0> = (1/2)(|00> + |01> + |10> + |11>)
```

So each basis state has amplitude:

```text
1/2
```

and measurement probabilities:

```text
(1/2)^2 = 1/4
```

for each state.

### 5.2 Oracle Phase Flip

The oracle flips the sign of the marked state amplitude and leaves the others unchanged:

```text
|psi_1> = (1/2)(|00> + |01> - |10> + |11>)
```

Now the amplitudes are:

- `|00>`: `1/2`
- `|01>`: `1/2`
- `|10>`: `-1/2`
- `|11>`: `1/2`

The probabilities are still all `1/4` at this stage, because measurement depends on squared magnitude, not sign.

### 5.3 Diffusion Step Intuition

The Grover diffusion operator reflects amplitudes about their average. After the phase flip, this reflection increases the marked-state amplitude and decreases the others.

For `N = 4` with one marked state, one Grover iteration is enough to rotate all amplitude onto the marked item. After the diffusion step, the marked state is measured with probability `1` in the idealized setting.

Verification: the oracle step alone changes phase but not probability. The full Grover iteration then uses interference to move amplitude toward the marked basis state. This illustrates the central mechanism: speedup comes from amplitude engineering, not direct parallel readout. Correct.

## 6. Pseudocode Pattern

```text
procedure grover_search(oracle, num_iterations):
    initialize register to uniform superposition
    for t = 1 to num_iterations:
        apply oracle phase flip to marked states
        apply diffusion operator
    measure the register
    return observed basis state
```

Query complexity: `O(sqrt(N))` for search over `N` items with a constant number of marked states. Circuit cost depends additionally on oracle implementation, qubit count, and gate decomposition.

## 7. Common Mistakes

1. **All-solutions-at-once myth.** Saying that a quantum computer simply evaluates every answer simultaneously ignores the fact that measurement returns only one outcome and that interference must be engineered to make that outcome useful.
2. **Universal-speedup assumption.** Assuming quantum algorithms provide large speedups for all hard problems is false; advantages are known only for specific problem structures.
3. **Query-time conflation.** Reporting Grover’s `O(sqrt(N))` query bound as total runtime without discussing oracle cost can make an algorithm look cheaper than it really is.
4. **Asymptotic-practical collapse.** Treating Shor’s polynomial-time result as immediate practical breakage of all deployed cryptography ignores hardware limits and fault-tolerance overhead.
5. **Measurement-state confusion.** Confusing amplitudes with probabilities leads to incorrect reasoning about phase flips, since a sign change can matter algorithmically even when the immediate measurement probability is unchanged.

## 8. Practical Checklist

- [ ] State clearly whether the algorithmic claim is about query complexity, gate complexity, qubit count, or full fault-tolerant runtime.
- [ ] Describe the precondition or structure the algorithm exploits, such as periodicity, oracle access, or nonnegative amplitudes under a transform.
- [ ] Explain what measurement returns and why pre-measurement interference is necessary.
- [ ] Distinguish theoretical asymptotic advantage from current hardware feasibility.
- [ ] Check whether the oracle cost is included or excluded in the complexity claim.
- [ ] Use linear-algebra language precisely when describing states, amplitudes, and unitary operations.
- [ ] Avoid claiming exponential speedup unless the algorithm and comparison model actually justify it.

## 9. References

- Nielsen, Michael A., and Isaac L. Chuang. 2010. *Quantum Computation and Quantum Information* (10th anniversary ed.). Cambridge University Press. <https://doi.org/10.1017/CBO9780511976667>
- Aaronson, Scott. 2013. *Quantum Computing Since Democritus*. Cambridge University Press. <https://doi.org/10.1017/CBO9780511979309>
- Shor, Peter W. 1997. Polynomial-Time Algorithms for Prime Factorization and Discrete Logarithms on a Quantum Computer. *SIAM Journal on Computing* 26(5): 1484–1509. <https://doi.org/10.1137/S0097539795293172>
- Grover, Lov K. 1996. A Fast Quantum Mechanical Algorithm for Database Search. *Proceedings of STOC 1996*, 212–219. <https://doi.org/10.1145/237814.237866>
- Montanaro, Ashley. 2016. Quantum algorithms: an overview. *npj Quantum Information* 2, 15023. <https://doi.org/10.1038/npjqi.2015.23>
- Watrous, John. 2018. *The Theory of Quantum Information*. Cambridge University Press. <https://doi.org/10.1017/9781316848142>
