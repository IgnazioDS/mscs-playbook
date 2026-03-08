# Linear Algebra: Rank, Independence, Eigenvalues, and Least Squares

## Key Ideas

- Rank measures how many independent directions a matrix contains, which determines solvability, compression, and whether parameters are identifiable.
- Linear independence is the statement that no vector in a set can be written as a combination of the others, and it is the structural reason bases and coordinates work.
- Eigenvalues and eigenvectors describe directions that a linear transformation scales without rotating away, which makes them central in dynamics, stability, and dimensionality reduction.
- Least squares solves inconsistent linear systems by finding the vector whose prediction minimizes squared residual error.
- Implementation quality depends on numerical method choice: QR factorization is usually safer than forming normal equations directly.

## 1. What It Is

The earlier foundations page on vectors and matrices introduces the language of linear algebra. This page extends that foundation to the matrix properties that most often determine whether an algorithm works, is identifiable, or is numerically stable.

A matrix `A` can be viewed as:

- a table of numbers,
- a linear map from one vector space to another,
- or a collection of column vectors.

Rank, independence, eigenstructure, and least squares answer four different questions about that map:

- How many genuinely different directions does it contain?
- Are some columns redundant?
- What directions are preserved by the transformation?
- If `Ax = b` has no exact solution, what approximate solution is best?

## 2. Rank and Linear Independence

### 2.1 Definitions

A set of vectors is **linearly independent** if the only coefficients that make their linear combination equal zero are all zero. Otherwise the vectors are **linearly dependent**.

The **rank** of a matrix is the dimension of its column space, which is also equal to the dimension of its row space.

If `A` is an `m x n` matrix:

- `rank(A) <= min(m, n)`
- full column rank means `rank(A) = n`
- full row rank means `rank(A) = m`

### 2.2 Why rank matters

Rank tells you whether information was lost.

- If `A` has full column rank, different parameter vectors produce different outputs.
- If columns are dependent, some parameters are redundant.
- In least squares, full column rank gives a unique minimizer.

For implementation work, rank is the difference between a model being identifiable and a model having infinitely many equivalent parameter settings.

## 3. Eigenvalues and Eigenvectors

For a square matrix `A`, a nonzero vector `v` is an **eigenvector** with **eigenvalue** `lambda` if:

```text
Av = lambda v
```

The equation says `A` acts on direction `v` by scaling it, not by sending it to a different direction.

### 3.1 Why they matter

Eigenvalues describe repeated action.

- In linear dynamical systems, eigenvalues tell us whether repeated updates grow, decay, or oscillate.
- In spectral methods and PCA, dominant eigenvectors capture high-variance directions.
- In graph algorithms, matrix spectra reveal connectivity and diffusion behavior.

### 3.2 Characteristic equation

Eigenvalues satisfy:

```text
det(A - lambda I) = 0
```

Solving this polynomial yields the candidate eigenvalues. Each eigenvector then lies in the null space of `A - lambda I`.

## 4. Least Squares and Projection

When `Ax = b` is inconsistent, we cannot make the residual `r = b - Ax` equal zero. Least squares instead solves:

```text
minimize_x ||Ax - b||_2^2
```

The geometric meaning is projection: `Ax_hat` is the point in the column space of `A` closest to `b` in Euclidean distance.

### 4.1 Normal equations

If `A` has full column rank, the least-squares solution satisfies:

```text
A^T A x = A^T b
```

This is useful conceptually, but numerically it can square the condition number. In production code, QR factorization is usually preferred.

### 4.2 Why this matters

Least squares appears in regression, calibration, sensor fusion, system identification, and curve fitting. The mathematical question “what is the closest point in a subspace?” becomes the engineering question “what parameters best fit noisy measurements?”

## 5. Worked Example

Fit a line `y = beta_0 + beta_1 x` to the three points:

```text
(0, 1), (1, 2), (2, 2)
```

Write this as `A beta ≈ b` with:

```text
A = [1 0]
    [1 1]
    [1 2]

beta = [beta_0]
       [beta_1]

b = [1]
    [2]
    [2]
```

### 5.1 Check rank

The two columns of `A` are:

```text
c_1 = [1, 1, 1]^T
c_2 = [0, 1, 2]^T
```

No scalar multiple of `c_1` equals `c_2`, so the columns are linearly independent and `rank(A) = 2`.

### 5.2 Form the normal equations

```text
A^T A = [3 3]
        [3 5]

A^T b = [5]
        [6]
```

So we solve:

```text
[3 3] [beta_0] = [5]
[3 5] [beta_1]   [6]
```

Subtract the first equation from the second:

```text
2 beta_1 = 1
beta_1 = 1 / 2
```

Then:

```text
beta_0 + beta_1 = 5 / 3
beta_0 = 5 / 3 - 1 / 2 = 7 / 6
```

Thus the least-squares line is:

```text
y = 7 / 6 + (1 / 2)x
```

### 5.3 Verify the residual geometry

Predictions:

```text
x = 0 -> 7 / 6
x = 1 -> 5 / 3
x = 2 -> 13 / 6
```

Residual vector:

```text
r = b - A beta
  = [1, 2, 2]^T - [7 / 6, 5 / 3, 13 / 6]^T
  = [-1 / 6, 1 / 3, -1 / 6]^T
```

Check orthogonality to the columns of `A`:

```text
c_1^T r = (-1 / 6) + (1 / 3) + (-1 / 6) = 0
c_2^T r = 0 * (-1 / 6) + 1 * (1 / 3) + 2 * (-1 / 6) = 0
```

Verification: the residual is orthogonal to the column space of `A`, so the computed line is the correct least-squares solution.

## 6. Pseudocode Pattern

```text
procedure least_squares_qr(A, b):
    Q, R = householder_qr(A)
    y = transpose(Q) * b
    return back_substitute(R, y[0:number_of_columns(A)])
```

Time: `Theta(mn^2)` worst case for a dense `m x n` matrix with `m >= n`. Space: `Theta(mn)` to store the dense factors in a straightforward implementation.

This pattern is preferable to directly forming `A^T A` when numerical stability matters.

## 7. Common Mistakes

1. **Rank-nullity blindness.** Treating a rank-deficient matrix as if it had unique parameters leads to unstable or non-identifiable models; check rank before claiming uniqueness.
2. **Eigenvalue overgeneralization.** Assuming every square matrix has a full basis of eigenvectors is false and can break diagonalization-based reasoning; verify diagonalizability before relying on it.
3. **Normal-equation overuse.** Forming `A^T A` by default can amplify conditioning problems and lose precision; prefer QR or SVD when numerical quality matters.
4. **Residual-magnitude confusion.** A small residual does not prove the parameters are unique or well-conditioned; inspect rank and conditioning separately from fit error.
5. **Geometric-language omission.** Writing least squares only as algebra hides the key projection interpretation and makes orthogonality checks harder; interpret the solution in the column space.

## 8. Practical Checklist

- [ ] State the matrix dimensions before discussing rank or solvability.
- [ ] Check whether columns are independent before claiming a unique parameter vector.
- [ ] Distinguish exact solves `Ax = b` from approximate least-squares solves.
- [ ] Use eigenvalues to reason about repeated linear action, not arbitrary nonlinear updates.
- [ ] Prefer QR or SVD over normal equations for numerically sensitive implementations.
- [ ] Verify least-squares solutions by checking residual orthogonality when possible.

## 9. References

- Strang, Gilbert. 2016. *Introduction to Linear Algebra* (5th ed.). Wellesley-Cambridge Press. <https://math.mit.edu/~gs/linearalgebra/>
- Hefferon, Jim. 2020. *Linear Algebra*. Orthogonal Publishing. <https://hefferon.net/linearalgebra/>
- Trefethen, Lloyd N., and David Bau III. 1997. *Numerical Linear Algebra*. SIAM. <https://epubs.siam.org/doi/book/10.1137/1.9780898719574>
- Golub, Gene H., and Charles F. Van Loan. 2013. *Matrix Computations* (4th ed.). Johns Hopkins University Press. <https://jhupbooks.press.jhu.edu/title/matrix-computations>
- Boyd, Stephen, and Lieven Vandenberghe. 2004. *Convex Optimization*. Cambridge University Press. <https://web.stanford.edu/~boyd/cvxbook/>
- MIT OpenCourseWare. 2025. *18.06 Linear Algebra*. <https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/>
