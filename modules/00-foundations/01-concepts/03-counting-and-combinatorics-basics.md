# Counting and Combinatorics Basics

## Key Ideas

- Counting is the mathematical discipline of determining how many configurations satisfy a rule without enumerating every case one by one.
- The addition principle and multiplication principle explain why a problem decomposes into mutually exclusive cases or sequential choices.
- Permutations, combinations, and binomial coefficients are distinct objects, so the correct formula depends on whether order matters and whether repetition is allowed.
- Counting arguments are implementation-relevant because they bound search spaces, estimate memory growth, and justify probabilistic models.
- A clean counting model starts by defining the objects being counted before any formula is chosen.

## 1. What It Is

Combinatorics studies finite arrangements, selections, and discrete structures. In computer science, it appears whenever we ask how many states, inputs, schedules, subsets, strings, or execution paths are possible.

This matters because algorithm design depends on state-space size. If a brute-force solver must inspect `2^n` subsets, the counting argument already explains why the approach will fail at moderate `n`. Likewise, if a randomized algorithm samples from a family of size `n!`, counting tells us what the sample space actually is.

### 1.1 Core definitions

- A **permutation** is an ordered arrangement of distinct items.
- A **combination** is an unordered selection of items.
- A **binomial coefficient** `C(n, k)` counts the number of `k`-element subsets of an `n`-element set.
- The **addition principle** says counts add across disjoint cases.
- The **multiplication principle** says counts multiply across sequential independent choices.

## 2. Core Counting Principles

### 2.1 Addition principle

If a set of valid outcomes can be partitioned into disjoint cases `A` and `B`, then:

```text
count(A union B) = count(A) + count(B)
```

The disjointness condition matters. If the cases overlap, simple addition double-counts some outcomes.

### 2.2 Multiplication principle

If a process consists of `m` choices for the first step and `n` choices for the second step for each first-step outcome, then the total number of outcomes is:

```text
m * n
```

This generalizes to longer sequences. Password counts, state counts, and nested-loop iteration spaces are all direct applications.

### 2.3 Permutations and combinations

For `n` distinct items:

- Number of full permutations: `n!`
- Number of ordered selections of `k` distinct items: `n! / (n-k)!`
- Number of unordered selections of `k` distinct items:

```text
C(n, k) = n! / (k!(n-k)!)
```

The reason combinations divide by `k!` is that each unordered `k`-subset corresponds to `k!` internal orderings that should not be counted separately.

## 3. Binomial Coefficients and Counting Models

### 3.1 Why binomial coefficients matter

`C(n, k)` appears whenever we choose `k` positions, features, or elements from `n` candidates without caring about order. This includes subsets, committee selection, and many dynamic-programming state counts.

### 3.2 Pascal recurrence

Binomial coefficients satisfy:

```text
C(n, k) = C(n - 1, k - 1) + C(n - 1, k)
```

The reason is structural: when counting `k`-subsets of an `n`-element set, either a chosen distinguished element is included or it is not. These are disjoint cases.

### 3.3 Why this matters in CS

Combinatorial counts are often the first asymptotic warning sign in algorithms. If a problem requires checking every subset, the search space has size `2^n`. If it requires checking every ordering, the search space has size `n!`. These are not implementation details; they determine whether an exact algorithm is feasible.

## 4. Worked Example

How many 4-bit strings contain exactly two `1` bits?

### 4.1 Model the object correctly

A 4-bit string is a length-4 sequence over `{0, 1}`. To contain exactly two `1` bits, we need to choose which two of the four positions contain `1`.

Order among the chosen positions does not matter, because the bit value is the same in both chosen positions.

### 4.2 Count by combinations

So the count is:

```text
C(4, 2) = 4! / (2!2!) = 6
```

### 4.3 Enumerate to verify

The six strings are:

```text
1100
1010
1001
0110
0101
0011
```

Verification: there are exactly `6` valid strings, matching `C(4, 2) = 6`.

## 5. Pseudocode Pattern

```text
procedure binomial_coefficient(n, k):
    if k < 0 or k > n:
        return 0
    if k == 0 or k == n:
        return 1

    k = min(k, n - k)
    result = 1
    for i = 1 to k:
        result = result * (n - k + i)
        result = result / i
    return result
```

Time: `Theta(k)` worst case. Space: `Theta(1)` auxiliary space.

This pattern avoids computing large factorials directly, which is better numerically and algorithmically for moderate `n`.

## 6. Common Mistakes

1. **Order-blind counting.** Using combinations when order matters undercounts the outcome space; decide first whether rearrangements represent different objects.
2. **Overlap double-counting.** Adding counts from cases that are not disjoint inflates the answer; partition the space into mutually exclusive cases before using the addition principle.
3. **Formula-first reasoning.** Picking `n!`, `C(n, k)`, or `n^k` before defining the object usually leads to the wrong model; write down what one valid outcome looks like first.
4. **Repetition confusion.** Treating “choose `k` items” as if repetition were impossible when reuse is allowed changes the problem entirely; state whether elements may repeat.
5. **Asymptotic neglect.** Counting a search space exactly but ignoring how quickly it grows can lead to infeasible brute-force designs; translate the count into a scalability claim.

## 7. Practical Checklist

- [ ] Define the object being counted before choosing a formula.
- [ ] Check whether cases are disjoint before adding counts.
- [ ] Check whether choices are sequential before multiplying counts.
- [ ] Decide explicitly whether order matters.
- [ ] Decide explicitly whether repetition is allowed.
- [ ] Convert the final count into an algorithmic implication when the problem is computational.

## 8. References

- Graham, Ronald L., Donald E. Knuth, and Oren Patashnik. 1994. *Concrete Mathematics* (2nd ed.). Addison-Wesley. <https://www-cs-faculty.stanford.edu/~knuth/gkp.html>
- Lehman, Eric, F. Thomson Leighton, and Albert R. Meyer. 2018. *Mathematics for Computer Science*. MIT. <https://courses.csail.mit.edu/6.042/spring18/mcs.pdf>
- Rosen, Kenneth H. 2019. *Discrete Mathematics and Its Applications* (8th ed.). McGraw Hill. <https://www.mheducation.com/highered/product/discrete-mathematics-applications-rosen/M9781259676512.html>
- Epp, Susanna S. 2019. *Discrete Mathematics with Applications* (5th ed.). Cengage. <https://www.cengage.com/c/discrete-mathematics-with-applications-5e-epp/9781337694193/>
- Bona, Miklos. 2023. *A Walk Through Combinatorics* (5th ed.). World Scientific. <https://www.worldscientific.com/worldscibooks/10.1142/13443>
- OpenDSA Project. 2024. *Combinatorics and Counting*. <https://opendsa-server.cs.vt.edu/ODSA/Books/Everything/html/>
