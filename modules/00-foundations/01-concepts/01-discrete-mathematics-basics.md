# Discrete Mathematics Basics

## Key Ideas

- Discrete mathematics studies finite or countable structures, which makes it the natural language for algorithms, data structures, logic, and state machines.
- Sets, functions, and relations let us model data and constraints precisely before we design an implementation.
- Logical statements become useful in computer science only when quantifiers, implication, and equivalence are interpreted operationally.
- Equivalence relations and partial orders are not abstract decoration; they explain partitioning, dependency structure, and canonical representations.
- A correct discrete model exposes what must be proved, counted, or computed, while a weak model hides essential assumptions.

## 1. What It Is

Discrete mathematics is the study of mathematical objects built from separated, countable pieces rather than continuously varying quantities. In computer science, the most common discrete objects are finite sets, strings, graphs, trees, relations, and logical statements.

This matters because software is executed as discrete state transitions. Memory addresses are finite bit strings. Program traces are finite or countable sequences. Dependency graphs, schedules, type systems, and databases are all modeled more naturally with discrete structures than with calculus.

### 1.1 Core definitions

- A **set** is an unordered collection of distinct elements.
- A **function** is a rule that maps each element of a domain to exactly one element of a codomain.
- A **relation** on a set `A` is a subset of `A x A`.
- A **predicate** is a statement that becomes true or false after its variables are assigned values.
- A **quantifier** specifies how a predicate ranges over a domain: `forall` means “for every element,” and `exists` means “for at least one element.”

## 2. Logic, Sets, and Functions

A discrete model starts by naming the objects under discussion and the statements that can be made about them. If the objects are ambiguous, later proofs and algorithms are ambiguous too.

### 2.1 Sets and operations

For sets `A` and `B`:

- `A union B` contains elements in either set.
- `A intersection B` contains elements in both sets.
- `A \ B` contains elements in `A` but not in `B`.
- `A x B` is the Cartesian product of ordered pairs.

These operations appear directly in implementations. A permission system can be modeled as a set of enabled capabilities. A graph is often represented as a set of vertices together with a set of edges. A database join is a structured form of Cartesian product followed by filtering.

### 2.2 Logical connectives and quantifiers

A statement such as

```text
forall user in users, exists session in sessions such that owns(user, session)
```

means every user has at least one associated session. Reversing the quantifiers changes the meaning completely:

```text
exists session in sessions such that forall user in users, owns(user, session)
```

The first statement allows a different session per user. The second says a single session is owned by every user. Quantifier order is a correctness issue, not a notation issue.

### 2.3 Functions as program contracts

A function `f: A -> B` must produce exactly one output in `B` for every input in `A`. In software terms, a deterministic total function is a strong contract. If the mapping is partial or many-to-one, the distinction must be explicit.

Common properties:

- **Injective**: different inputs map to different outputs.
- **Surjective**: every element of the codomain is hit by some input.
- **Bijective**: both injective and surjective, so the function has an inverse.

## 3. Relations, Equivalence, and Order

Relations explain how elements are connected beyond simple membership.

### 3.1 Equivalence relations

A relation `R` on `A` is an **equivalence relation** if it is:

- **Reflexive**: `a R a` for every `a in A`.
- **Symmetric**: if `a R b`, then `b R a`.
- **Transitive**: if `a R b` and `b R c`, then `a R c`.

Equivalence relations partition a set into **equivalence classes**. This is the mathematical basis of grouping identical outputs, canonicalization, and quotient structures.

### 3.2 Partial orders

A relation `<=` is a **partial order** if it is reflexive, antisymmetric, and transitive. Partial orders model dependencies where not every pair is comparable. Build systems, prerequisite graphs, and version constraints all behave this way.

### 3.3 Why this matters in implementations

If an engineer confuses an equivalence relation with an arbitrary similarity rule, deduplication can become inconsistent. If a dependency relation is not transitive, topological reasoning breaks. Discrete mathematics supplies the exact properties an implementation relies on.

## 4. Worked Example

Let `A = {1, 2, 3}` and define relation `R` by:

```text
R = {(1, 1), (2, 2), (3, 3), (1, 2), (2, 1)}
```

We want to decide whether `R` is an equivalence relation.

### 4.1 Check reflexivity

A relation on `A` is reflexive if `(1, 1)`, `(2, 2)`, and `(3, 3)` are all present.

They are all in `R`, so `R` is reflexive.

### 4.2 Check symmetry

If `(1, 2)` is present, then `(2, 1)` must also be present. Both are in `R`.

All other non-diagonal pairs in `R` already satisfy symmetry, so `R` is symmetric.

### 4.3 Check transitivity

The only nontrivial chains are:

- `(1, 2)` and `(2, 1)`, which require `(1, 1)`.
- `(2, 1)` and `(1, 2)`, which require `(2, 2)`.
- `(1, 2)` and `(2, 2)`, which require `(1, 2)`.
- `(2, 1)` and `(1, 1)`, which require `(2, 1)`.

All required pairs are already in `R`, so `R` is transitive.

### 4.4 Equivalence classes

Because `1` and `2` are related to each other, they belong to the same class. Element `3` is related only to itself.

The equivalence classes are:

```text
[1] = [2] = {1, 2}
[3] = {3}
```

Verification: `R` is reflexive, symmetric, and transitive, so it is an equivalence relation, and the classes `{1, 2}` and `{3}` form a partition of `A`.

## 5. Pseudocode Pattern

```text
procedure is_equivalence_relation(elements, relation_matrix):
    n = length(elements)

    for i = 0 to n - 1:
        if relation_matrix[i][i] == false:
            return false

    for i = 0 to n - 1:
        for j = 0 to n - 1:
            if relation_matrix[i][j] and not relation_matrix[j][i]:
                return false

    for i = 0 to n - 1:
        for j = 0 to n - 1:
            if relation_matrix[i][j]:
                for k = 0 to n - 1:
                    if relation_matrix[j][k] and not relation_matrix[i][k]:
                        return false

    return true
```

Time: `Theta(n^3)` worst case because transitivity checks all triples. Space: `Theta(1)` auxiliary beyond the input matrix.

This pattern is implementation-aware: once a relation is represented as a Boolean adjacency matrix, mathematical properties become testable program properties. For bit-packed relations, the same logic can often be vectorized with word-level operations, which connects directly to [Boolean Algebra and Bit Operations](12-boolean-algebra-and-bit-operations.md).

## 6. Common Mistakes

1. **Quantifier reversal.** Swapping `forall` and `exists` changes the meaning of a specification and can make a proof or API contract false; rewrite the statement in plain language before relying on it.
2. **Set-sequence confusion.** Treating sets as ordered containers leads to invalid arguments about “first” or “next” elements; if order matters, model a sequence or tuple explicitly.
3. **Relation-property drift.** Assuming a relation is an equivalence relation or partial order without checking the defining properties causes invalid deduplication or dependency reasoning; test reflexivity, symmetry or antisymmetry, and transitivity directly.
4. **Codomain omission.** Describing a function only by its formula hides whether outputs are actually guaranteed to lie in the intended target set; state the domain and codomain together.
5. **Model under-specification.** Jumping to an algorithm before identifying the underlying sets, predicates, and relations produces brittle code because the invariants were never formalized; write the discrete model first.

## 7. Practical Checklist

- [ ] Name the underlying set or domain before stating any property.
- [ ] Rewrite quantified statements in plain English to confirm the quantifier order.
- [ ] Distinguish clearly between sets, sequences, tuples, and multisets.
- [ ] Check relation properties explicitly instead of assuming them from intuition.
- [ ] State whether a function is total, partial, injective, surjective, or bijective when that distinction matters.
- [ ] Use equivalence classes when you need canonical grouping, not ad hoc similarity scores.

## 8. References

- Lehman, Eric, F. Thomson Leighton, and Albert R. Meyer. 2018. *Mathematics for Computer Science*. MIT. <https://courses.csail.mit.edu/6.042/spring18/mcs.pdf>
- MIT OpenCourseWare. 2015. *Mathematics for Computer Science*. <https://ocw.mit.edu/courses/6-042j-mathematics-for-computer-science-fall-2010/>
- Rosen, Kenneth H. 2019. *Discrete Mathematics and Its Applications* (8th ed.). McGraw Hill. <https://www.mheducation.com/highered/product/discrete-mathematics-applications-rosen/M9781259676512.html>
- Epp, Susanna S. 2019. *Discrete Mathematics with Applications* (5th ed.). Cengage. <https://www.cengage.com/c/discrete-mathematics-with-applications-5e-epp/9781337694193/>
- Graham, Ronald L., Donald E. Knuth, and Oren Patashnik. 1994. *Concrete Mathematics* (2nd ed.). Addison-Wesley. <https://www-cs-faculty.stanford.edu/~knuth/gkp.html>
- OpenDSA Project. 2024. *OpenDSA: Open Computer Science Textbook*. <https://opendsa-server.cs.vt.edu/ODSA/Books/Everything/html/>
