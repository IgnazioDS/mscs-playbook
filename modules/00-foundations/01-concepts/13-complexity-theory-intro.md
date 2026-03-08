# Complexity Theory Intro

## Key Ideas

- Complexity theory studies which problems are efficiently solvable, not just how fast a particular implementation runs on one machine.
- A problem, an algorithm, and a complexity class are different objects, so claims about `P`, `NP`, or NP-hardness must keep those levels separate.
- Polynomial time is used as the main tractability benchmark because it grows much more slowly than exponential or factorial time as input size increases.
- Reductions transfer difficulty between problems by showing how solving one efficiently would solve another efficiently.
- Complexity classes guide engineering judgment: they tell us when exact algorithms are realistic and when approximation, randomization, or heuristics become necessary.

## 1. What It Is

Complexity theory studies the resource requirements of computational problems as input size grows. Unlike implementation-level analysis, which asks whether one program runs faster than another, complexity theory asks broader questions such as:

- Is there any polynomial-time algorithm for this problem?
- Is the problem at least as hard as other known hard problems?
- What changes if we allow randomness or approximation?

This matters because some problems remain difficult even after careful coding and constant-factor optimization. In those settings, the bottleneck is not engineering style but the problem’s computational structure.

### 1.1 Core definitions

- A **decision problem** asks for a yes-or-no answer.
- A **language** is the set of strings for which a decision problem answers yes.
- A problem is in **P** if some deterministic algorithm solves it in polynomial worst-case time.
- A problem is in **NP** if a proposed yes-instance certificate can be verified in polynomial worst-case time.
- A problem is **NP-hard** if every problem in NP reduces to it in polynomial time.
- A problem is **NP-complete** if it is both in NP and NP-hard.

## 2. Why Polynomial Time Matters

A polynomial-time bound does not guarantee practical speed, but it is the standard notion of efficient solvability because it scales qualitatively better than exponential growth.

For example:

- `n^3` is usually manageable for moderate `n`.
- `2^n` becomes infeasible quickly.
- `n!` becomes infeasible even faster.

This does not mean all polynomial-time algorithms are good or all exponential-time algorithms are useless. It means the distinction is structurally important.

For the algorithm-design use of reductions after this page, see [Reductions and Hardness Basics](../../01-algorithms/01-concepts/15-reductions-and-hardness-basics.md).

## 3. The Main Classes and Their Meaning

### 3.1 Class `P`

`P` contains decision problems solvable in polynomial worst-case time on a deterministic model of computation. Many standard graph and numeric problems fall here.

Examples include:

- graph reachability,
- shortest path with nonnegative weights,
- and primality testing.

### 3.2 Class `NP`

`NP` contains decision problems for which yes-instances have polynomial-size certificates verifiable in polynomial worst-case time.

A key point is that `NP` is not “non-polynomial.” It is a verification-based class.

### 3.3 NP-hard and NP-complete

If a problem is NP-hard, it is at least as hard as every problem in NP under polynomial-time reductions. If it is also in NP, it is NP-complete.

This matters because if any NP-complete problem were shown to be in `P`, then every problem in NP would also be in `P`.

## 4. Worked Example

Consider the decision version of subset sum:

```text
Input: positive integers a_1, ..., a_n and target T
Question: is there a subset whose sum is exactly T?
```

Take the concrete instance:

```text
numbers = {3, 5, 6, 10}
T = 11
```

### 4.1 Check candidate subsets

Possible relevant subset sums include:

```text
3
5
6
10
3 + 5 = 8
3 + 6 = 9
3 + 10 = 13
5 + 6 = 11
5 + 10 = 15
6 + 10 = 16
3 + 5 + 6 = 14
...
```

We find:

```text
5 + 6 = 11
```

So this instance is a yes-instance.

### 4.2 Why it is in NP

A certificate can simply be the claimed subset, here `{5, 6}`. Verification consists of summing those numbers and checking equality with `11`.

For input length `n`, verification is polynomial worst-case time because it only requires summing the listed elements and comparing with `T`.

Verification: `{5, 6}` sums to `11`, so the certificate is valid and the example illustrates the definition of membership in `NP`.

## 5. Pseudocode Pattern

```text
procedure verify_subset_sum(numbers, target, certificate_indices):
    total = 0
    for index in certificate_indices:
        total = total + numbers[index]
    return total == target
```

Time: `Theta(k)` worst case where `k` is the number of indices in the certificate and `k <= n`. Space: `Theta(1)` auxiliary space beyond the input and certificate.

This is a verifier, not a solver. Complexity theory distinguishes these tasks carefully.

## 6. Common Mistakes

1. **NP means non-polynomial.** Reading `NP` as “not polynomial” is wrong and causes basic class confusion; `NP` is defined through polynomial-time verification.
2. **Algorithm-problem collapse.** Saying an algorithm is NP-complete mixes the complexity of a problem with one implementation; complexity classes classify problems, not source files.
3. **Optimization-decision blur.** Using NP-complete terminology on an optimization version without stating the associated decision problem makes the claim imprecise; define the decision form first.
4. **Practical-theoretical collapse.** Concluding that a problem is “impossible in practice” because it is NP-hard ignores approximation, parameterization, special cases, and moderate input sizes; complexity informs design but does not end it.
5. **Reduction direction error.** Reversing a reduction proves the wrong hardness statement; keep track of which problem is transformed into which.

## 7. Practical Checklist

- [ ] State the problem in decision form before using `P`, `NP`, NP-hard, or NP-complete language.
- [ ] Name the case for every time-complexity claim.
- [ ] Separate a verifier from a solver when discussing `NP`.
- [ ] Check the direction of every reduction carefully.
- [ ] Use hardness results to motivate algorithm choice, not as a substitute for problem-specific analysis.
- [ ] Distinguish asymptotic intractability from real-world instance size limits.

## 8. References

- Sipser, Michael. 2012. *Introduction to the Theory of Computation* (3rd ed.). Cengage. <https://www.cengage.com/c/introduction-to-the-theory-of-computation-3e-sipser/9781133187790/>
- Arora, Sanjeev, and Boaz Barak. 2009. *Computational Complexity: A Modern Approach*. Cambridge University Press. <https://theory.cs.princeton.edu/complexity/>
- Garey, Michael R., and David S. Johnson. 1979. *Computers and Intractability*. W. H. Freeman. <https://archive.org/details/computersintract0000gare>
- Papadimitriou, Christos H. 1994. *Computational Complexity*. Addison-Wesley. <https://www.pearson.com/en-us/subject-catalog/p/computational-complexity/P200000003594>
- Lehman, Eric, F. Thomson Leighton, and Albert R. Meyer. 2018. *Mathematics for Computer Science*. MIT. <https://courses.csail.mit.edu/6.042/spring18/mcs.pdf>
- MIT OpenCourseWare. 2005. *Mathematics for Computer Science*. <https://ocw.mit.edu/courses/6-042j-mathematics-for-computer-science-fall-2010/>
