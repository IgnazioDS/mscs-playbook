# Primes, Totients, and Fast Exponentiation

## Key Ideas
- Prime numbers matter in cryptography because many hard problems and algebraic structures depend on factorization or arithmetic over prime-related moduli.
- Euler's totient function counts the integers coprime to a modulus and is central to RSA correctness.
- Fermat's little theorem and Euler's theorem explain why modular exponentiation can reverse itself under the right conditions.
- Fast exponentiation makes cryptographic arithmetic practical because it avoids constructing enormous intermediate integers.
- Mathematical correctness and computational feasibility are different concerns, and cryptographic systems need both.

## 1. Why primes matter

A **prime number** is an integer greater than `1` with no positive divisors other than `1` and itself. Primes are the basic building blocks of integers because every positive integer factors into primes.

Cryptography uses primes for two main reasons:

- prime-based arithmetic often produces clean algebraic behavior
- some computational problems related to primes, such as factoring large composites, appear hard enough to support security assumptions

In RSA, the modulus `n = pq` is built from two large primes. In Diffie-Hellman, arithmetic is often performed modulo a large prime or inside a prime-order subgroup.

## 2. Totients, Fermat, and Euler

Euler's totient function `phi(n)` counts how many integers in `{1, 2, ..., n}` are coprime to `n`.

For distinct primes `p` and `q`:

`phi(pq) = (p - 1)(q - 1)`

Two key theorems:

- **Fermat's little theorem**: if `p` is prime and `gcd(a, p) = 1`, then `a^(p-1) ≡ 1 (mod p)`
- **Euler's theorem**: if `gcd(a, n) = 1`, then `a^(phi(n)) ≡ 1 (mod n)`

These results explain why exponents can "wrap around" modulo a group size and why RSA decryption recovers the original message under the right conditions.

## 3. Fast modular exponentiation

Naively computing `a^k` first and reducing afterward is impractical because the intermediate number becomes enormous. **Repeated squaring** avoids that by reducing modulo `n` after each multiplication.

```text
procedure modexp(base, exponent, modulus):
    result = 1
    base = base % modulus

    while exponent > 0:
        if exponent % 2 == 1:
            result = (result * base) % modulus
        base = (base * base) % modulus
        exponent = exponent // 2

    return result
```

Time: worst-case `O(log exponent)` modular multiplications. Space: `O(1)` auxiliary space.

This is one of the core routines in public-key cryptography. The mathematics may define security, but repeated squaring makes the formulas executable.

## 4. Worked example: totient and modular exponentiation

Let:

- `p = 11`
- `q = 13`

Then:

`n = pq = 143`

Compute the totient:

`phi(143) = (11 - 1)(13 - 1) = 10 * 12 = 120`

Now compute `7^13 mod 143` by repeated squaring.

Start:

- `7^1 ≡ 7 (mod 143)`
- `7^2 = 49`
- `7^4 = 49^2 = 2401 ≡ 113 (mod 143)` because `2401 - 16 * 143 = 2401 - 2288 = 113`
- `7^8 = 113^2 = 12769 ≡ 42 (mod 143)` because `12769 - 89 * 143 = 12769 - 12727 = 42`

Since `13 = 8 + 4 + 1`:

`7^13 ≡ 7^8 * 7^4 * 7^1 ≡ 42 * 113 * 7 (mod 143)`

First multiply:

`42 * 113 = 4746 ≡ 27 (mod 143)` because `4746 - 33 * 143 = 4746 - 4719 = 27`

Then:

`27 * 7 = 189 ≡ 46 (mod 143)`

So:

`7^13 mod 143 = 46`

Verification: repeated squaring and reduction give the final remainder `46`.

## 5. Why these tools appear everywhere

Totients and modular exponentiation are not specific to RSA. They show up in:

- primality-related reasoning
- key-generation logic
- discrete-log-based cryptography
- digital signature verification

This page belongs before full cryptosystems because later algorithms reuse these exact operations while adding security notions, padding, and protocol constraints.

## 6. Common Mistakes

1. **Prime-assumption slippage**: applying Fermat's little theorem to a composite modulus without the right conditions produces false conclusions; check whether the theorem's premises hold.
2. **Totient miscalculation**: using `phi(pq) = (p - 1)(q - 1)` without confirming `p` and `q` are distinct primes breaks RSA-style arithmetic; state the factorization assumptions explicitly.
3. **Exponentiation naivety**: computing giant powers directly is computationally wasteful and error-prone; use repeated squaring with modular reduction at each step.
4. **Coprimality neglect**: Euler's theorem requires `gcd(a, n) = 1`; verify that condition before using it in a proof or simplification.
5. **Correctness-security confusion**: a theorem proving arithmetic correctness does not prove cryptographic security; keep algebraic validity separate from hardness assumptions.

## 7. Practical Checklist

- [ ] Be able to compute `phi(pq)` for distinct primes `p` and `q`.
- [ ] Use repeated squaring for every nontrivial modular exponentiation task.
- [ ] State when Fermat's theorem or Euler's theorem is applicable before using it.
- [ ] Reduce intermediate products modulo `n` during hand calculations to keep numbers manageable.
- [ ] Distinguish between arithmetic proofs and security arguments.
- [ ] Treat fast modular exponentiation as a core primitive, not as an implementation detail.

## References

1. Victor Shoup, *A Computational Introduction to Number Theory and Algebra*. [https://shoup.net/ntb/](https://shoup.net/ntb/)
2. Dan Boneh and Victor Shoup, *A Graduate Course in Applied Cryptography*. [https://toc.cryptobook.us/](https://toc.cryptobook.us/)
3. Alfred J. Menezes, Paul C. van Oorschot, and Scott A. Vanstone, *Handbook of Applied Cryptography*. [https://cacr.uwaterloo.ca/hac/](https://cacr.uwaterloo.ca/hac/)
4. Jonathan Katz and Yehuda Lindell, *Introduction to Modern Cryptography*. [https://www.routledge.com/Introduction-to-Modern-Cryptography/Katz-Lindell/p/book/9780815354369](https://www.routledge.com/Introduction-to-Modern-Cryptography/Katz-Lindell/p/book/9780815354369)
5. Richard Crandall and Carl Pomerance, *Prime Numbers: A Computational Perspective*. [https://link.springer.com/book/10.1007/978-0-387-28979-6](https://link.springer.com/book/10.1007/978-0-387-28979-6)
6. NIST, *Computer Security Resource Center*. [https://csrc.nist.gov/](https://csrc.nist.gov/)
7. Stanford Encyclopedia of Philosophy, *Number Theory in Cryptography*. [https://plato.stanford.edu/](https://plato.stanford.edu/)
