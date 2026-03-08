# Randomized Algorithms

## Key Ideas

- A randomized algorithm makes some decisions using random bits, so its analysis must distinguish worst-case inputs from expected or probability-of-failure guarantees.
- Las Vegas algorithms always return a correct answer and randomize running time, while Monte Carlo algorithms bound running time and randomize the chance of error.
- Expected-time guarantees are mathematical guarantees over the algorithm's internal randomness, not vague claims about typical benchmark behavior.
- Randomization often avoids adversarial worst-case structure, which is why it is useful in sorting, selection, hashing, graph algorithms, and approximate counting.
- Probability amplification can reduce failure probability substantially, but only when repeated runs are independent and the error model is understood.

## 1. What It Is

A randomized algorithm is an algorithm whose behavior depends on random choices made during execution. Those random choices might select a pivot, sample an item, choose a hash function, or pick an edge to contract.

### 1.1 Core Definitions

- A **Las Vegas algorithm** always outputs a correct answer, but its running time is random.
- A **Monte Carlo algorithm** has bounded running time but may output an incorrect answer with some bounded probability.
- An **expected running time** is the average running time over the algorithm's internal randomness for a fixed input.
- A **failure probability** is the probability that the randomized algorithm returns an incorrect answer or misses a target property.
- **Probability amplification** repeats an experiment to reduce the failure probability.

### 1.2 Why This Matters

Randomization is often a practical response to worst-case structure. Deterministic quicksort can be driven into quadratic worst-case time by adversarial pivot choices. A randomized pivot choice yields `Theta(n log n)` expected time on every fixed input. Similar gains appear in hashing, skip lists, primality testing, and graph algorithms.

## 2. Two Main Guarantee Styles

### 2.1 Las Vegas Algorithms

Las Vegas algorithms never sacrifice correctness. The randomness only affects how much work is done.

Examples include:

- randomized quicksort,
- randomized quickselect,
- and many randomized balanced-search-tree schemes.

When discussing Las Vegas algorithms, say:

- expected time,
- worst-case time,
- and what randomness is assumed.

### 2.2 Monte Carlo Algorithms

Monte Carlo algorithms trade a bounded error probability for speed or simplicity.

Examples include:

- polynomial identity testing,
- Bloom filters,
- and many sketching or approximate-counting methods.

For Monte Carlo algorithms, two questions matter separately:

1. how likely is an incorrect answer,
2. how expensive is it to reduce that probability.

## 3. Why Randomization Helps

### 3.1 Escaping Adversarial Inputs

If the algorithm chooses a pivot or hash function randomly, an adversary who controls the input cannot force the same deterministic bad case unless it also controls the random bits. This often turns structurally bad instances into rare events in the analysis.

### 3.2 Indicator and Linearity-of-Expectation Analysis

Many expected-time proofs use indicator random variables and linearity of expectation. This is important because expected bounds often remain simple even when the random events are not independent.

### 3.3 Amplification

If one Monte Carlo run fails with probability at most `1/3`, repeating it independently `k` times and taking a suitable aggregate can shrink failure probability exponentially in `k`. The design of the aggregate rule depends on the error model.

## 4. Worked Example

Use randomized quickselect to find the `4`th smallest element in:

```text
[7, 2, 9, 4, 1, 5]
```

Assume this specific run chooses pivot `4` first, then pivot `7`.

### 4.1 First Partition

Pivot:

```text
4
```

Partition the array:

```text
less = [2, 1]
equal = [4]
greater = [7, 9, 5]
```

There are `2` elements less than `4`, so `4` is the `3`rd smallest element. We want the `4`th smallest, so recurse into `greater` looking for its `1`st smallest element.

### 4.2 Second Partition

Now solve:

```text
select([7, 9, 5], 1)
```

Pivot:

```text
7
```

Partition:

```text
less = [5]
equal = [7]
greater = [9]
```

We want the `1`st smallest element, and there is exactly one element in `less`, so the answer is:

```text
5
```

### 4.3 Interpret the Guarantee

This trace shows one valid run, not the full proof. For randomized quickselect:

- Time: `Theta(n)` expected case.
- Time: `O(n^2)` worst case.
- Space: `O(1)` auxiliary space for an in-place partition implementation, or `O(n)` auxiliary space for a list-copying teaching implementation like the trace above.

Verification: sorting the original array gives `[1, 2, 4, 5, 7, 9]`, so the `4`th smallest element is indeed `5`.

## 5. Pseudocode Pattern

```text
procedure randomized_quickselect(values, k):
    if length(values) == 1:
        return values[0]

    pivot = uniformly_random_element(values)
    less, equal, greater = three_way_partition(values, pivot)

    if k <= length(less):
        return randomized_quickselect(less, k)
    if k <= length(less) + length(equal):
        return pivot
    return randomized_quickselect(greater, k - length(less) - length(equal))
```

Time: `Theta(n)` expected case and `O(n^2)` worst case. Space: `O(n)` auxiliary space for the recursive partition-copying form above.

## 6. Common Mistakes

1. **Expected-equals-usual confusion.** Saying an expected-time bound means the algorithm is fast on every run hides tail risk; expected analysis averages over randomness and still allows rare slow executions.
2. **Guarantee-type mixing.** Treating a Monte Carlo algorithm like a Las Vegas algorithm, or the reverse, misstates the correctness guarantee; say explicitly whether errors are possible.
3. **Amplification without independence.** Repeating correlated trials and assuming exponential failure reduction is unjustified; the amplification argument requires independent or appropriately controlled repeats.
4. **Worst-case omission.** Reporting only the expected time of randomized quicksort or quickselect hides the existence of quadratic worst-case runs; state both case labels when they matter.
5. **Bad randomness assumptions.** Using a weak or biased random source without analysis can invalidate the intended guarantee; document what randomness model the proof relies on.

## 7. Practical Checklist

- [ ] State whether the algorithm is Las Vegas or Monte Carlo before discussing performance.
- [ ] Label every complexity claim as expected, worst case, or failure-probability dependent.
- [ ] Identify which part of the algorithm is randomized and why that helps.
- [ ] Check whether amplification arguments require independent reruns.
- [ ] Use deterministic fallbacks when correctness or reproducibility constraints forbid probabilistic failure.
- [ ] Trace at least one concrete run to separate the mechanics from the probabilistic proof.

## 8. References

- Motwani, Rajeev, and Prabhakar Raghavan. 1995. *Randomized Algorithms*. Cambridge University Press.
- Mitzenmacher, Michael, and Eli Upfal. 2017. *Probability and Computing* (2nd ed.). Cambridge University Press.
- Cormen, Thomas H., Charles E. Leiserson, Ronald L. Rivest, and Clifford Stein. 2022. *Introduction to Algorithms* (4th ed.). MIT Press. <https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/>
- Karger, David. 2013. *6.856J/18.416J Randomized Algorithms*. Massachusetts Institute of Technology. <https://courses.csail.mit.edu/6.856/13/>
- MIT OpenCourseWare. 2002. *6.856J Randomized Algorithms: Lecture Notes*. <https://ocw.mit.edu/courses/6-856j-randomized-algorithms-fall-2002/pages/lecture-notes/>
- Roughgarden, Tim. 2026. *Lecture Notes*. Stanford University. <https://theory.stanford.edu/~tim/notes.html>
