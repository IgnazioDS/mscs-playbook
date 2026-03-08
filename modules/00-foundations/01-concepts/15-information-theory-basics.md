# Information Theory Basics

## Key Ideas

- Information theory quantifies uncertainty and information in probabilistic terms, so probability models must be defined before entropy or mutual information can be computed.
- Entropy measures average uncertainty in a random variable, not semantic meaning or usefulness of a message.
- Conditional entropy and mutual information describe how uncertainty changes when another variable is observed, which is why they matter in communication, compression, and machine learning.
- Relative entropy, also called Kullback-Leibler divergence, measures mismatch between probability models, and it is not symmetric or a true metric.
- Information-theoretic quantities give limits on coding and inference, but those limits only apply under the assumptions built into the source and channel model.

## 1. What It Is

Information theory studies how uncertainty, coding, and communication can be described mathematically. It asks questions such as:

- How many bits are needed, on average, to encode a source?
- How much information does one variable reveal about another?
- How much performance is lost when a model assumes the wrong distribution?

### 1.1 Core Definitions

- A **random variable** is a variable whose value depends on the outcome of a probabilistic process.
- **Self-information** of an outcome `x` with probability `p(x)` is `-log_2 p(x)` bits.
- **Entropy** `H(X)` is the expected self-information of a random variable `X`.
- **Conditional entropy** `H(X | Y)` is the remaining uncertainty in `X` after observing `Y`.
- **Mutual information** `I(X; Y)` is the reduction in uncertainty about `X` obtained by observing `Y`.
- **Kullback-Leibler divergence** `D(P || Q)` measures how different model `Q` is from data or beliefs represented by `P`.

### 1.2 Why This Matters

Compression algorithms, error-correcting codes, probabilistic models, feature selection, decision trees, and generative modeling all rely on information-theoretic ideas. Entropy explains why some sources can be compressed more than others. Mutual information explains why one variable is predictive of another. Relative entropy explains why training on the wrong model can be costly.

## 2. Entropy and Coding

### 2.1 Entropy

For a discrete random variable `X` with possible outcomes `x`, entropy is:

```text
H(X) = -sum_x p(x) log_2 p(x)
```

Entropy is measured in bits when the logarithm base is `2`.

Low entropy means the source is predictable. High entropy means the source is uncertain. A deterministic source has entropy `0`, while a fair coin has entropy `1` bit.

### 2.2 Source-Coding Interpretation

Entropy gives a lower bound on the average number of bits needed to encode symbols from a source without loss, under idealized assumptions. It does not say that every symbol can be encoded with exactly `H(X)` bits. It says that over long sequences, no prefix-free code can beat the entropy rate on average.

## 3. Conditional Entropy and Mutual Information

### 3.1 Conditional Entropy

Conditional entropy measures what uncertainty remains in `X` after `Y` is known:

```text
H(X | Y) = -sum_{x, y} p(x, y) log_2 p(x | y)
```

If `Y` determines `X` perfectly, then `H(X | Y) = 0`. If `Y` tells us nothing about `X`, conditional entropy stays large.

### 3.2 Mutual Information

Mutual information can be written as:

```text
I(X; Y) = H(X) - H(X | Y)
```

and also as:

```text
I(X; Y) = H(Y) - H(Y | X)
```

It is always nonnegative. Mutual information is `0` exactly when `X` and `Y` are independent.

## 4. Relative Entropy and Model Mismatch

For discrete distributions `P` and `Q` on the same support:

```text
D(P || Q) = sum_x P(x) log_2 (P(x) / Q(x))
```

Relative entropy is `0` only when `P = Q`, but it is not symmetric:

```text
D(P || Q) != D(Q || P)
```

This matters in machine learning and statistics because optimizing cross-entropy or likelihood often amounts to reducing divergence between the empirical data distribution and the model distribution.

## 5. Worked Example

Consider a binary source `X` that is equally likely to produce `0` or `1`:

```text
P(X = 0) = 0.5
P(X = 1) = 0.5
```

The bit is sent through a binary symmetric channel with crossover probability `0.1`, meaning the output `Y` flips the input with probability `0.1`.

### 5.1 Compute the Source Entropy

```text
H(X) = -(0.5 log_2 0.5 + 0.5 log_2 0.5)
     = -(0.5 * -1 + 0.5 * -1)
     = 1 bit
```

### 5.2 Compute the Conditional Entropy of the Channel

Given the input, the output is correct with probability `0.9` and flipped with probability `0.1`, so:

```text
H(Y | X) = -(0.9 log_2 0.9 + 0.1 log_2 0.1)
```

Using:

```text
log_2 0.9 ≈ -0.1520
log_2 0.1 ≈ -3.3219
```

we get:

```text
H(Y | X) ≈ -(0.9 * -0.1520 + 0.1 * -3.3219)
         ≈ 0.1368 + 0.3322
         ≈ 0.4690 bits
```

### 5.3 Compute the Output Entropy

Because the input is uniform and the channel is symmetric:

```text
P(Y = 0) = 0.5
P(Y = 1) = 0.5
```

So:

```text
H(Y) = 1 bit
```

### 5.4 Compute Mutual Information

```text
I(X; Y) = H(Y) - H(Y | X)
        = 1 - 0.4690
        = 0.5310 bits
```

This means each received bit carries about `0.531` bits of information about the transmitted bit on average under this noise model.

Verification: `H(X) = 1`, `H(Y | X) ≈ 0.4690`, `H(Y) = 1`, and therefore `I(X; Y) = 1 - 0.4690 ≈ 0.5310` bits, which is consistent with a noisy but informative channel.

## 6. Pseudocode Pattern

```text
procedure entropy(probabilities):
    total = 0
    for p in probabilities:
        if p > 0:
            total = total - p * log2(p)
    return total
```

Time: `Theta(k)` worst case where `k` is the number of probability masses. Space: `Theta(1)` auxiliary space beyond the input list.

## 7. Common Mistakes

1. **Meaning-versus-entropy confusion.** Equating semantic importance with entropy is wrong because entropy measures probabilistic uncertainty, not whether the message is useful or interesting.
2. **Zero-probability mishandling.** Plugging `log(0)` directly into a calculation causes undefined expressions; use the standard convention that `0 log 0 = 0` in entropy sums.
3. **Mutual-information symmetry errors.** Claiming `I(X; Y)` can be negative or changes when the variable order is swapped is incorrect; mutual information is nonnegative and symmetric.
4. **Divergence-as-distance language.** Treating `D(P || Q)` like a metric hides the fact that it is asymmetric and does not satisfy the triangle inequality; use it as a divergence, not a geometric distance.
5. **Coding-limit overreach.** Saying entropy alone determines a real codec's exact performance ignores block length, modeling error, latency constraints, and implementation overhead; entropy provides a limit, not an automatic construction.

## 8. Practical Checklist

- [ ] Define the random variables and their probability distributions before computing any information measure.
- [ ] Keep logarithm bases consistent and state the unit, such as bits for base `2`.
- [ ] Check whether the model is discrete or continuous before applying discrete entropy formulas.
- [ ] Use conditional entropy or mutual information when the question is about information gain after observing another variable.
- [ ] Treat KL divergence as a model-mismatch measure, not as a symmetric distance.
- [ ] Connect entropy claims to an explicit source or channel model before drawing compression or communication conclusions.

## 9. References

- Shannon, Claude E. 1948. *A Mathematical Theory of Communication*. *Bell System Technical Journal* 27(3-4). <https://reach.ieee.org/primary-sources/a-mathematical-theory-of-communication/>
- Cover, Thomas M., and Joy A. Thomas. 2006. *Elements of Information Theory* (2nd ed.). Wiley.
- MacKay, David J. C. 2003. *Information Theory, Inference, and Learning Algorithms*. Cambridge University Press. <https://www.inference.org.uk/itprnn/book.html>
- Polyanskiy, Yury, and Yihong Wu. 2016. *Information Theory* lecture notes. MIT OpenCourseWare. <https://ocw.mit.edu/courses/6-441-information-theory-spring-2016/pages/lecture-notes/>
- Stanford University. 2025. *EE 376A: Information Theory*. <https://web.stanford.edu/class/ee376a/>
- Csiszar, Imre, and Janos Korner. 2011. *Information Theory: Coding Theorems for Discrete Memoryless Systems* (2nd ed.). Cambridge University Press.
- Ba, Anasse, Justin Solomon, and George Ver Steeg. 2017. *Divergence, Entropy, Information: An Opinionated Introduction to Information Theory*. arXiv. <https://arxiv.org/abs/1708.07459>
