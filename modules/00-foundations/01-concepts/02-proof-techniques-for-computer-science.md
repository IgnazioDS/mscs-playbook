# Proof Techniques for Computer Science

## Key Ideas

- A proof is a structured argument that shows a claim follows from definitions, assumptions, and previously established results.
- In computer science, proof techniques justify algorithm correctness, data-structure invariants, protocol properties, and asymptotic claims.
- The right proof technique depends on the claim’s structure: implications often invite direct proof or contrapositive, recursive objects invite induction, and impossibility claims often invite contradiction.
- A proof becomes implementation-aware when every mathematical claim is tied to a program state, an invariant, or an execution step.
- Good proofs remove ambiguity by naming the inductive parameter, the invariant, or the exact statement being established.

## 1. What It Is

A proof is not a collection of plausible examples. It is an argument that covers all cases allowed by the statement. In computer science, this distinction matters because a single missing case can become a bug, a security flaw, or a failed guarantee.

Typical proof targets include:

- correctness of a loop or recursive algorithm,
- uniqueness or existence of a data representation,
- asymptotic upper or lower bounds,
- and impossibility results about what an algorithm cannot do.

### 1.1 Core definitions

- A **theorem** is a statement proved from accepted premises.
- A **lemma** is an intermediate result used to prove a larger theorem.
- A **corollary** is an immediate consequence of a previous result.
- An **invariant** is a property that remains true throughout a process.
- **Induction** proves a family of statements indexed by size or structure.

## 2. Main Proof Techniques

### 2.1 Direct proof

A direct proof starts from the assumptions and derives the conclusion step by step. It is appropriate when the definitions naturally compose.

If the statement is “if `P`, then `Q`,” direct proof assumes `P` and derives `Q`.

### 2.2 Contrapositive

The contrapositive of “if `P`, then `Q`” is “if not `Q`, then not `P`.” These statements are logically equivalent.

Contrapositive proof is useful when `not Q` has a clearer operational meaning than `Q`. For example, proving “if a graph has a topological order, then it is acyclic” can be easier through the contrapositive: “if a graph has a cycle, then it has no topological order.”

### 2.3 Contradiction

A proof by contradiction assumes the claim is false and derives an impossibility. It is useful for impossibility theorems, uniqueness results, and statements about nonexistence.

The method is powerful, but it can hide the real mechanism if used lazily. When a direct or invariant-based proof exists, it is usually more informative.

### 2.4 Induction and structural induction

**Mathematical induction** proves a statement `P(n)` for all integers `n >= n_0` by showing:

1. the base case `P(n_0)` is true, and
2. `P(k)` implies `P(k + 1)` for every `k >= n_0`.

**Strong induction** assumes all smaller cases up to `k`, not just `P(k)`.

**Structural induction** is the analogous method for recursively defined objects such as trees, expressions, and syntax trees.

The conceptual reason induction works is that it follows the same construction rule as the object being proved about.

## 3. Choosing the Right Technique

A proof method should match the shape of the claim.

- Use direct proof when the definitions compose cleanly.
- Use contrapositive when the negated conclusion has a cleaner structure.
- Use contradiction when the statement is inherently impossibility-based.
- Use induction when the object or algorithm is defined recursively or by size.
- Use invariants when the statement concerns an iterative process.

This page focuses on foundational techniques; for iterative correctness arguments, see [Loop Invariants and Algorithm Correctness](../../01-algorithms/01-concepts/01-loop-invariants-and-algorithm-correctness.md).

## 4. Worked Example

Consider exponentiation by squaring for computing `a^n` with integer `n >= 0`.

```text
procedure fast_power(a, n):
    if n == 0:
        return 1
    if n mod 2 == 0:
        half = fast_power(a, n / 2)
        return half * half
    return a * fast_power(a, n - 1)
```

Time: `Theta(log n)` worst case multiplication depth if even cases dominate and multiplication cost is treated as constant. Space: `Theta(log n)` worst case recursion depth.

We want to prove that `fast_power(a, n)` returns `a^n` for every integer `n >= 0`.

### 4.1 Trace on a concrete input

Take `a = 3` and `n = 13`.

```text
fast_power(3, 13)
= 3 * fast_power(3, 12)
= 3 * (fast_power(3, 6))^2
= 3 * ((fast_power(3, 3))^2)^2
= 3 * ((3 * fast_power(3, 2))^2)^2
= 3 * ((3 * (fast_power(3, 1))^2)^2)^2
= 3 * ((3 * (3 * fast_power(3, 0))^2)^2)^2
= 3 * ((3 * 3^2)^2)^2
= 3 * (27^2)^2
= 3 * 729^2
= 3 * 531441
= 1594323
```

### 4.2 Induction proof

We prove by strong induction on `n` that `fast_power(a, n) = a^n` for all `n >= 0`.

**Base case:** `n = 0`.
The procedure returns `1`, and by definition `a^0 = 1`. So the claim holds.

**Inductive hypothesis:** assume for all integers `m` with `0 <= m < n`, the procedure returns `a^m`.

**Inductive step:** prove the claim for `n`.

- If `n` is even, write `n = 2t`. The algorithm computes `half = fast_power(a, t)` and returns `half * half`. Since `t < n`, the inductive hypothesis gives `half = a^t`. Therefore the returned value is `a^t * a^t = a^(2t) = a^n`.
- If `n` is odd and positive, the algorithm returns `a * fast_power(a, n - 1)`. Since `n - 1 < n`, the inductive hypothesis gives `fast_power(a, n - 1) = a^(n - 1)`. Therefore the returned value is `a * a^(n - 1) = a^n`.

In both cases the procedure returns `a^n`, so the statement holds for all `n >= 0`.

Verification: the trace gives `fast_power(3, 13) = 1594323`, and `3^13 = 1594323`, matching the theorem.

## 5. Common Mistakes

1. **Example-based certainty.** Testing a few inputs and calling that a proof leaves uncovered cases that can still fail; convert examples into a universal argument.
2. **Induction-parameter drift.** Changing the variable being measured midway through an induction proof breaks the logical chain; state the inductive parameter once and keep it fixed.
3. **Unstated base case.** Omitting the base case makes the inductive proof incomplete and can hide failures at the smallest input size; prove the smallest valid case explicitly.
4. **Technique mismatch.** Using contradiction for a claim that has a simple direct proof often obscures the core idea and invites hidden assumptions; choose the technique that mirrors the structure of the statement.
5. **Definition skipping.** Invoking words such as “sorted,” “correct,” or “balanced” without definitions makes the proof non-checkable; restate the exact property being proved before reasoning about it.

## 6. Practical Checklist

- [ ] Write the claim in symbolic and plain-language form before proving it.
- [ ] Name every assumption and every definition the proof depends on.
- [ ] Choose the proof technique that matches the claim’s structure.
- [ ] For induction, state the base case, inductive hypothesis, and inductive step separately.
- [ ] For algorithm proofs, tie each statement to a program state or recursive call.
- [ ] End by restating exactly what has been established, not just that the algebra worked.

## 7. References

- Velleman, Daniel J. 2019. *How to Prove It* (3rd ed.). Cambridge University Press. <https://www.cambridge.org/highereducation/books/how-to-prove-it/6D2965D625C6836CD4A785A2C843B3DA>
- Hammack, Richard. 2022. *Book of Proof* (3rd ed.). Virginia Commonwealth University. <https://richardhammack.github.io/BookOfProof/>
- Lehman, Eric, F. Thomson Leighton, and Albert R. Meyer. 2018. *Mathematics for Computer Science*. MIT. <https://courses.csail.mit.edu/6.042/spring18/mcs.pdf>
- Epp, Susanna S. 2019. *Discrete Mathematics with Applications* (5th ed.). Cengage. <https://www.cengage.com/c/discrete-mathematics-with-applications-5e-epp/9781337694193/>
- Cormen, Thomas H., Charles E. Leiserson, Ronald L. Rivest, and Clifford Stein. 2022. *Introduction to Algorithms* (4th ed.). MIT Press. <https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/>
- Gries, David. 1981. *The Science of Programming*. Springer. <https://doi.org/10.1007/978-1-4612-5983-1>
