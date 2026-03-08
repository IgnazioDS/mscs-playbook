# Linear Algebra: Vectors and Matrices

## Key Ideas

- A vector represents magnitude and direction, while a matrix represents either a rectangular table of numbers or a linear transformation.
- Dot products, norms, and matrix multiplication are the core operations behind similarity, projection, and linear model computation.
- Matrix dimensions are part of the meaning of an expression, so shape checks are a mathematical requirement, not just an implementation detail.
- Systems of linear equations can often be written compactly as `Ax = b`, which connects algebraic solving to geometric interpretation.
- Conditioning matters: even when formulas are correct, poorly conditioned matrices can produce unstable numerical results.

## 1. What It Is

Linear algebra studies vectors, matrices, and linear transformations. In engineering, statistics, machine learning, graphics, and scientific computing, it provides a compact language for representing data and computation.

A **vector** is an ordered list of numbers, often interpreted as a point or direction in space. A **matrix** is a rectangular array of numbers that can represent data, a system of equations, or a transformation that maps one vector to another.

This page covers the minimal toolkit needed for later work:

- vectors and their basic operations,
- matrices and matrix multiplication,
- systems of equations in matrix form,
- and the numerical pitfalls that appear in real implementations.

### 1.1 Core Definitions

- A **scalar** is a single number.
- A **vector** in `R^n` is an ordered list of `n` scalars.
- A **matrix** in `R^(m x n)` has `m` rows and `n` columns.
- The **transpose** of a matrix `A`, written `A^T`, swaps rows and columns.
- A **linear transformation** is a mapping `T` such that `T(u + v) = T(u) + T(v)` and `T(cu) = cT(u)`.
- A **square matrix** has the same number of rows and columns.
- A matrix is **invertible** if there exists `A^(-1)` such that `A A^(-1) = I` and `A^(-1) A = I`.

### 1.2 Why This Matters

Linear algebra is the execution layer of many modern algorithms. A linear regression model computes `Xw`. A neural network layer applies matrix multiplication plus a nonlinearity. Embedding similarity uses dot products or cosine similarity. Principal component analysis, least squares, and many optimization methods rely on matrix structure.

This means that weak linear algebra intuition causes both conceptual and implementation errors. Many bugs that look like model issues are actually shape mistakes, bad numerical conditioning, or misuse of vector geometry.

## 2. Vectors

### 2.1 Vector Notation and Geometry

A vector in `R^n` is typically written as:

```text
x = [x_1, x_2, ..., x_n]
```

Geometrically, a vector can be interpreted as:

- a point in `n`-dimensional space,
- a displacement from the origin,
- or a direction with magnitude.

For example, in `R^2`, the vector `[3, 4]` points from `(0, 0)` to `(3, 4)`.

### 2.2 Dot Product

For vectors `x, y` in `R^n`, the dot product is:

```text
x · y = sum_{i=1 to n} x_i y_i
```

The dot product measures alignment.

- Positive dot product: vectors point in broadly similar directions.
- Zero dot product: vectors are orthogonal.
- Negative dot product: vectors point in opposing directions.

It also appears in the geometric identity:

```text
x · y = ||x|| ||y|| cos(theta)
```

where `theta` is the angle between the vectors.

### 2.3 Norms and Cosine Similarity

The Euclidean norm of `x` is:

```text
||x||_2 = sqrt(sum_{i=1 to n} x_i^2)
```

This is the usual vector length.

Cosine similarity is:

```text
cos_sim(x, y) = (x · y) / (||x|| ||y||)
```

Cosine similarity removes the effect of overall scale and keeps only directional similarity. This is why it is common for comparing embeddings and normalized feature vectors.

## 3. Matrices

### 3.1 Matrix Structure

A matrix `A` in `R^(m x n)` has the form:

```text
A =
[a_11 a_12 ... a_1n]
[a_21 a_22 ... a_2n]
[ ...            ...]
[a_m1 a_m2 ... a_mn]
```

You can interpret a matrix in two useful ways:

- as a table of coefficients or data,
- or as a transformation applied to a vector.

Each row and column has semantic meaning. In data settings, rows often represent observations and columns represent features. In transformations, columns often describe how basis vectors are mapped.

### 3.2 Matrix-Vector and Matrix-Matrix Multiplication

If `A` is an `(m x n)` matrix and `x` is a vector in `R^n`, then `Ax` is a vector in `R^m`.

The product is defined only when the inner dimensions match.

- `(m x n) * (n x 1)` is valid and produces `(m x 1)`.
- `(m x n) * (p x 1)` is invalid if `n != p`.

For matrix multiplication, if `A` is `(m x n)` and `B` is `(n x p)`, then `AB` is `(m x p)`.

The `(i, j)` entry of `AB` is:

```text
(AB)_ij = sum_{k=1 to n} A_ik B_kj
```

**Why this matters:** Matrix multiplication is not just combining numbers. It composes linear transformations. It is also not commutative in general, so `AB != BA` in most cases.

### 3.3 Transpose, Identity, and Determinant

The transpose `A^T` swaps rows and columns. It is used in least squares, covariance computation, and many optimization derivations.

The identity matrix `I` acts like a multiplicative neutral element:

```text
AI = IA = A
```

For a square matrix, the determinant gives information about scaling and invertibility.

- If `det(A) = 0`, then `A` is singular and not invertible.
- If `det(A) != 0`, then `A` is invertible.

For larger numerical systems, however, determinant is rarely the best practical test of stability. Conditioning is usually more informative.

## 4. Systems of Equations and Linear Transformations

### 4.1 Matrix Form of a Linear System

A system of linear equations can be written as:

```text
Ax = b
```

where:

- `A` is the coefficient matrix,
- `x` is the vector of unknowns,
- `b` is the right-hand-side vector.

For example, the system

```text
2x + y = 5
x - y = 1
```

can be written as:

```text
[2  1] [x] = [5]
[1 -1] [y]   [1]
```

This compact form lets us reason about the system structurally rather than equation by equation.

### 4.2 Linear Transformations

A matrix can also be viewed as a function that transforms vectors.

Examples:

- scaling,
- rotation,
- reflection,
- projection,
- and coordinate change.

For instance, the diagonal matrix

```text
[2 0]
[0 3]
```

scales the x-axis by 2 and the y-axis by 3. Applying it to `[1, 1]^T` produces `[2, 3]^T`.

**Why this matters:** This interpretation makes matrix multiplication intuitive. If `B` transforms a vector first and `A` transforms the result, then the combined transformation is `AB`.

## 5. Worked Example

Consider two vectors:

```text
x = [1, 2, 2]
y = [2, 0, 1]
```

We compute the dot product, norms, cosine similarity, and a matrix-vector product.

### 5.1 Dot Product and Norms

First compute the dot product:

```text
x · y = (1)(2) + (2)(0) + (2)(1)
      = 2 + 0 + 2
      = 4
```

Now compute the norms:

```text
||x|| = sqrt(1^2 + 2^2 + 2^2)
      = sqrt(1 + 4 + 4)
      = sqrt(9)
      = 3
```

```text
||y|| = sqrt(2^2 + 0^2 + 1^2)
      = sqrt(4 + 0 + 1)
      = sqrt(5)
```

### 5.2 Cosine Similarity

```text
cos_sim(x, y) = (x · y) / (||x|| ||y||)
              = 4 / (3 * sqrt(5))
              ≈ 0.596
```

So the vectors are positively aligned, but not extremely close in direction.

### 5.3 Matrix-Vector Product

Now let

```text
A =
[1 0 2]
[0 1 1]
```

and compute `Ax`.

Check dimensions first:

- `A` is `(2 x 3)`
- `x` is `(3 x 1)`
- result will be `(2 x 1)`

Now compute row by row:

```text
Ax =
[1 0 2] [1]
[0 1 1] [2]
        [2]
```

First component:

```text
(1)(1) + (0)(2) + (2)(2) = 1 + 0 + 4 = 5
```

Second component:

```text
(0)(1) + (1)(2) + (1)(2) = 0 + 2 + 2 = 4
```

Therefore:

```text
Ax = [5, 4]^T
```

Verification: `x · y = 4`, `||x|| = 3`, `||y|| = sqrt(5)`, `cos_sim(x, y) ≈ 0.596`, and `Ax = [5, 4]^T`. Each quantity is dimensionally valid and numerically consistent. Correct.

## 6. Common Mistakes

1. **Row-column convention mismatch.** Writing vectors inconsistently as rows in one place and columns in another leads to invalid products or silent transpose errors; choose one convention and keep it consistent.
2. **Unchecked shape compatibility.** Performing matrix multiplication without checking dimensions causes incorrect algebra and implementation bugs; always verify inner dimensions before multiplying.
3. **Assumed commutativity.** Assuming `AB = BA` is generally false and breaks both proofs and code; multiplication order encodes transformation order.
4. **Determinant-as-stability test.** A nonzero determinant guarantees invertibility, but it does not guarantee numerical stability; check conditioning when solving systems numerically.
5. **Zero-vector cosine similarity.** Cosine similarity divides by vector norms, so zero vectors make the expression undefined; guard against zero-norm inputs before computing it.

## 7. Practical Checklist

- [ ] Write vector and matrix dimensions explicitly before doing algebra.
- [ ] Check inner dimensions for every matrix multiplication.
- [ ] Use dot products only for vectors in the same space and with matching dimensions.
- [ ] Normalize vectors before using cosine similarity when scale should not affect comparison.
- [ ] Represent systems of equations as `Ax = b` before reasoning about solving strategy.
- [ ] Distinguish conceptual invertibility from numerical stability when working with real data.
- [ ] Verify whether row-major or column-vector conventions are assumed in the surrounding code or notes.

## 8. Pseudocode Pattern

```text
procedure matvec_multiply(A, x):
    -- A has shape (m x n), x has shape (n x 1)
    m = number_of_rows(A)
    n = number_of_columns(A)
    y = zero_vector(m)
    for i = 0 to m - 1:
        total = 0
        for j = 0 to n - 1:
            total = total + A[i][j] * x[j]
        y[i] = total
    return y
```

Time: `Theta(mn)` in all cases. Space: `Theta(m)` auxiliary space for the output vector `y`, excluding storage for the inputs.

## 9. References

- Boyd, Stephen, and Lieven Vandenberghe. 2004. *Convex Optimization*. Cambridge University Press. <https://web.stanford.edu/~boyd/cvxbook/>
- Hefferon, Jim. 2020. *Linear Algebra*. Orthogonal Publishing. <https://hefferon.net/linearalgebra/>
- Lay, David C., Steven R. Lay, and Judi J. McDonald. 2021. *Linear Algebra and Its Applications* (6th ed.). Pearson. <https://www.pearson.com/en-us/subject-catalog/p/linear-algebra-and-its-applications/P200000003044>
- Morin, Pat. 2013. *Open Data Structures*. AU Press. <https://opendatastructures.org/>
- Strang, Gilbert. 2016. *Introduction to Linear Algebra* (5th ed.). Wellesley-Cambridge Press. <https://math.mit.edu/~gs/linearalgebra/>
- Strang, Gilbert. 2023. *18.06 Linear Algebra*. MIT OpenCourseWare. <https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/>
- Trefethen, Lloyd N., and David Bau III. 1997. *Numerical Linear Algebra*. SIAM. <https://epubs.siam.org/doi/book/10.1137/1.9781611971484>
