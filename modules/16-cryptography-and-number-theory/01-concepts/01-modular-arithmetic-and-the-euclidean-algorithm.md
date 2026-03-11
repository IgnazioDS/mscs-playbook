# Modular Arithmetic and the Euclidean Algorithm

## Key Ideas
- Modular arithmetic studies integers by their remainders after division by a modulus, which is the basic language of much of cryptography.
- Congruence lets large arithmetic expressions be simplified safely because equal remainders behave the same way under addition and multiplication.
- The greatest common divisor of two integers determines whether division-like operations such as modular inversion are possible.
- The Euclidean algorithm computes greatest common divisors efficiently and is one of the foundational algorithms behind key generation.
- The extended Euclidean algorithm is important because it not only finds a gcd but also coefficients that explain how the gcd is formed.

## 1. Why modular arithmetic matters

Cryptography often works with integers inside a bounded arithmetic system. Instead of asking for the full value of an expression, it asks only for the remainder after division by some modulus `n`. This is called arithmetic **modulo** `n`.

We write:

`a ≡ b (mod n)`

to mean that `a` and `b` leave the same remainder when divided by `n`, or equivalently that `n` divides `a - b`.

This matters because many cryptographic operations are built from repeated modular multiplication and exponentiation. If modular arithmetic is not comfortable, RSA, Diffie-Hellman, and elliptic-curve arithmetic all look more mysterious than they are.

## 2. Congruence, gcd, and invertibility

Two ideas appear constantly in number theory for cryptography:

- the **greatest common divisor** `gcd(a, b)`, the largest positive integer dividing both `a` and `b`
- a **modular inverse**, an integer `x` such that `ax ≡ 1 (mod n)`

A modular inverse exists exactly when `gcd(a, n) = 1`. This condition is called **coprimality**.

The Euclidean algorithm computes gcd values by repeatedly replacing a pair `(a, b)` with `(b, a mod b)` until the remainder is zero. The worst-case time is `O(log min(a, b))` arithmetic steps, and the space is `O(1)` auxiliary space when implemented iteratively.

## 3. The Euclidean and extended Euclidean algorithms

The Euclidean algorithm uses:

`gcd(a, b) = gcd(b, a mod b)`

The **extended Euclidean algorithm** goes further and finds integers `x` and `y` such that:

`ax + by = gcd(a, b)`

This identity is called a **Bézout identity**. It matters because when the gcd is `1`, the coefficient `x` is a modular inverse of `a` modulo `b`, up to reduction.

```text
procedure extended_gcd(a, b):
    old_r = a
    r = b
    old_s = 1
    s = 0
    old_t = 0
    t = 1

    while r != 0:
        q = old_r // r
        old_r, r = r, old_r - q * r
        old_s, s = s, old_s - q * s
        old_t, t = t, old_t - q * t

    return old_r, old_s, old_t
```

Time: worst-case `O(log min(a, b))` arithmetic steps. Space: `O(1)` auxiliary space.

## 4. Worked example: gcd and modular inverse

Compute `gcd(252, 105)`:

1. `252 = 2 * 105 + 42`
2. `105 = 2 * 42 + 21`
3. `42 = 2 * 21 + 0`

So:

`gcd(252, 105) = 21`

Now find the inverse of `17 mod 43`.

Apply the Euclidean algorithm:

1. `43 = 2 * 17 + 9`
2. `17 = 1 * 9 + 8`
3. `9 = 1 * 8 + 1`
4. `8 = 8 * 1 + 0`

So `gcd(17, 43) = 1`, meaning an inverse exists.

Back-substitute:

`1 = 9 - 1 * 8`

`8 = 17 - 1 * 9`

So:

`1 = 9 - (17 - 9) = 2 * 9 - 17`

And `9 = 43 - 2 * 17`, so:

`1 = 2 * (43 - 2 * 17) - 17 = 2 * 43 - 5 * 17`

Therefore:

`-5 * 17 ≡ 1 (mod 43)`

Reduce `-5 mod 43`:

`-5 ≡ 38 (mod 43)`

So the inverse of `17 mod 43` is `38`.

Verification: `17 * 38 = 646`, and `646 mod 43 = 1`.

## 5. Why this page comes before cryptography

The Euclidean algorithm and modular inverses are not optional mathematical decoration. They appear directly in:

- RSA key generation
- finite-field arithmetic
- elliptic-curve formulas
- many protocol checks and parameter validations

If the reader can compute a gcd and inverse by hand, later cryptographic formulas become much easier to trust and debug.

## 6. Common Mistakes

1. **Remainder-sign confusion**: forgetting to reduce negative numbers correctly produces wrong modular results; always reduce into a stated residue range.
2. **Inverse-assumption error**: assuming every nonzero number has a modular inverse ignores the gcd condition; check coprimality before solving `ax ≡ 1 (mod n)`.
3. **Division shortcut**: canceling factors modulo `n` without confirming invertibility can break algebra; only divide by values that have inverses modulo `n`.
4. **Back-substitution slips**: arithmetic mistakes in the extended Euclidean algorithm lead to wrong coefficients; verify the final Bézout identity explicitly.
5. **Algorithm-black-box thinking**: using gcd routines without knowing what they return makes key-generation logic harder to reason about; connect each output to its number-theoretic meaning.

## 7. Practical Checklist

- [ ] Be able to interpret `a ≡ b (mod n)` as a divisibility statement.
- [ ] Use the Euclidean algorithm to compute gcd values instead of factoring by hand.
- [ ] Check `gcd(a, n) = 1` before searching for a modular inverse.
- [ ] Verify any computed inverse by multiplying and reducing modulo `n`.
- [ ] Keep track of the residue range you are using, especially when negative numbers appear.
- [ ] Treat the extended Euclidean algorithm as a core tool for later cryptographic key calculations.

## References

1. Victor Shoup, *A Computational Introduction to Number Theory and Algebra*. [https://shoup.net/ntb/](https://shoup.net/ntb/)
2. Alfred J. Menezes, Paul C. van Oorschot, and Scott A. Vanstone, *Handbook of Applied Cryptography*. [https://cacr.uwaterloo.ca/hac/](https://cacr.uwaterloo.ca/hac/)
3. Dan Boneh and Victor Shoup, *A Graduate Course in Applied Cryptography*. [https://toc.cryptobook.us/](https://toc.cryptobook.us/)
4. MIT OpenCourseWare, *Elementary Number Theory Notes*. [https://ocw.mit.edu/](https://ocw.mit.edu/)
5. NIST, *Glossary of Cryptographic Terms*. [https://csrc.nist.gov/glossary](https://csrc.nist.gov/glossary)
6. Richard Crandall and Carl Pomerance, *Prime Numbers: A Computational Perspective*. [https://link.springer.com/book/10.1007/978-0-387-28979-6](https://link.springer.com/book/10.1007/978-0-387-28979-6)
7. Terence Tao, *An Introduction to Measure and Number Theory Notes*. [https://terrytao.wordpress.com/books/](https://terrytao.wordpress.com/books/)
