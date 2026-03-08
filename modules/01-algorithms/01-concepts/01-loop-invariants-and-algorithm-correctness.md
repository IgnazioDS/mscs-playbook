# Loop Invariants and Algorithm Correctness

## Key Ideas

- A loop invariant is a property that is true before every iteration of a loop, and it is the central tool for proving iterative algorithm correctness.
- Correctness proofs usually have three parts: initialization, maintenance, and termination.
- A loop invariant should describe meaningful partial progress, not just a fact that remains true trivially.
- Termination needs its own argument, often through a decreasing measure or bounded index movement.
- In practice, strong invariants improve implementation quality because they guide assertions, tests, and edge-case reasoning.

## 1. What It Is

An algorithm is **correct** if it always returns a result satisfying its specification for every allowed input. For loops, the standard proof technique is a loop invariant.

A **loop invariant** is a statement that holds:

- before the first iteration,
- before every later iteration,
- and together with loop termination implies the postcondition.

The reason invariants matter is simple: a loop can execute many times, but the invariant compresses the reasoning into one reusable claim.

## 2. The Proof Structure

### 2.1 Initialization

Show the invariant holds before the loop starts. If it fails here, the rest of the proof is irrelevant.

### 2.2 Maintenance

Assume the invariant holds at the start of an iteration. Prove it still holds at the start of the next iteration after the loop body executes.

### 2.3 Termination

When the loop exits, combine the negation of the loop condition with the invariant to derive the postcondition.

This structure is closely related to induction: each iteration is the next inductive step.

## 3. Termination and Measures

A loop can preserve a beautiful invariant and still fail to terminate. Correctness therefore includes both:

- **partial correctness**: if the algorithm terminates, the result is correct;
- **total correctness**: the algorithm terminates and the result is correct.

A common termination tool is a **variant** or **ranking function**, a quantity that decreases each iteration and cannot decrease forever.

Examples include:

- the number of unprocessed elements,
- the width of a search interval,
- or the remaining capacity in a bounded process.

## 4. Worked Example

Consider insertion sort:

```text
procedure insertion_sort(A):
    for i = 1 to length(A) - 1:
        key = A[i]
        j = i - 1
        while j >= 0 and A[j] > key:
            A[j + 1] = A[j]
            j = j - 1
        A[j + 1] = key
```

Time: `Theta(n^2)` worst and average case, `Theta(n)` best case when the array is already sorted. Space: `Theta(1)` auxiliary space.

We prove the outer-loop invariant:

```text
Before iteration i, the prefix A[0:i] is sorted and contains exactly the elements originally in positions 0 through i - 1.
```

### 4.1 Trace on a concrete input

Start with:

```text
A = [5, 2, 4, 6, 1, 3]
```

Iteration `i = 1`, `key = 2`:

```text
sorted prefix before iteration: [5]
shift 5 right
insert 2
A = [2, 5, 4, 6, 1, 3]
```

Iteration `i = 2`, `key = 4`:

```text
sorted prefix before iteration: [2, 5]
shift 5 right
insert 4
A = [2, 4, 5, 6, 1, 3]
```

Iteration `i = 3`, `key = 6`:

```text
sorted prefix before iteration: [2, 4, 5]
no shifts needed
A = [2, 4, 5, 6, 1, 3]
```

Iteration `i = 4`, `key = 1`:

```text
sorted prefix before iteration: [2, 4, 5, 6]
shift 6, 5, 4, 2 right
insert 1
A = [1, 2, 4, 5, 6, 3]
```

Iteration `i = 5`, `key = 3`:

```text
sorted prefix before iteration: [1, 2, 4, 5, 6]
shift 6, 5, 4 right
insert 3
A = [1, 2, 3, 4, 5, 6]
```

### 4.2 Proof outline

- **Initialization:** before `i = 1`, the prefix `A[0:1]` has one element, so it is sorted and contains the original first element.
- **Maintenance:** assume before iteration `i` that `A[0:i]` is sorted. The inner loop shifts every element greater than `key` one position to the right, preserving order among shifted elements. Inserting `key` at `A[j + 1]` restores sorted order on `A[0:i + 1]` without changing the multiset of elements in the prefix.
- **Termination:** when the loop ends, `i = length(A)`. The invariant says `A[0:length(A)]`, which is the whole array, is sorted and contains exactly the original elements.

Verification: the trace ends with `[1, 2, 3, 4, 5, 6]`, and the invariant-based argument explains why this happens for every valid input.

## 5. Pseudocode Pattern

```text
procedure binary_search(A, target):
    left = 0
    right = length(A) - 1

    while left <= right:
        mid = floor((left + right) / 2)
        if A[mid] == target:
            return mid
        if A[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return not_found
```

Time: `Theta(log n)` worst and best case when measured by iterations over a sorted array of length `n`. Space: `Theta(1)` auxiliary space.

A useful invariant is: if `target` appears in `A`, then it must lie within the current interval `A[left:right + 1]`. The interval shrinks every iteration, which also gives the termination argument.

## 6. Common Mistakes

1. **Trivial invariant choice.** Picking a statement that is always true but says nothing about progress cannot prove the desired postcondition; choose an invariant that tracks the algorithm’s partial goal.
2. **Initialization gap.** Stating a plausible invariant without proving it before the first iteration leaves the proof incomplete; check the pre-loop state explicitly.
3. **Termination omission.** Showing maintenance without proving the loop ends gives only partial correctness; identify a decreasing bounded measure.
4. **Index-bound slippage.** Off-by-one mistakes often come from invariants that do not name interval endpoints precisely; write array ranges explicitly.
5. **Postcondition leap.** Claiming the final answer “is obvious” from the invariant usually hides the crucial use of the negated loop condition; combine both facts explicitly at termination.

## 7. Practical Checklist

- [ ] Write the algorithm’s precondition and postcondition before proposing an invariant.
- [ ] State the invariant in terms of concrete variables and array ranges.
- [ ] Prove initialization, maintenance, and termination separately.
- [ ] Identify a variant that decreases and is bounded below.
- [ ] Test the invariant against empty, singleton, and boundary-case inputs.
- [ ] Turn strong invariants into runtime assertions when debugging.

## 8. References

- Hoare, C. A. R. 1969. *An Axiomatic Basis for Computer Programming*. *Communications of the ACM* 12 (10). <https://cacm.acm.org/research/an-axiomatic-basis-for-computer-programming/>
- Cormen, Thomas H., Charles E. Leiserson, Ronald L. Rivest, and Clifford Stein. 2022. *Introduction to Algorithms* (4th ed.). MIT Press. <https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/>
- Gries, David. 1981. *The Science of Programming*. Springer. <https://doi.org/10.1007/978-1-4612-5983-1>
- Dijkstra, Edsger W. 1976. *A Discipline of Programming*. Prentice Hall. <https://www.cs.utexas.edu/~EWD/transcriptions/EWD04xx/EWD418.html>
- Apt, Krzysztof R., Frank S. de Boer, and Ernst-Rudiger Olderog. 2009. *Verification of Sequential and Concurrent Programs* (3rd ed.). Springer. <https://link.springer.com/book/10.1007/978-1-84882-745-5>
- Lehman, Eric, F. Thomson Leighton, and Albert R. Meyer. 2018. *Mathematics for Computer Science*. MIT. <https://courses.csail.mit.edu/6.042/spring18/mcs.pdf>
