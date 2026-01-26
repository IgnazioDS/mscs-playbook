# RSA Intro

## What it is
RSA is a public-key cryptosystem based on modular exponentiation and the
assumed hardness of factoring large integers.

## Why it matters
It enables secure key exchange and digital signatures, forming a foundation of
modern security infrastructure.

## Core idea (intuition)
Encryption uses a public exponent and modulus, while decryption uses a private
exponent that is hard to derive without factoring the modulus.

## Formal definition
Choose large primes p and q, set n = pq and phi = (p-1)(q-1). Pick e coprime to
phi, compute d = e^{-1} mod phi. Encrypt c = m^e mod n, decrypt m = c^d mod n.

## Patterns / common techniques
- Modular exponentiation by repeated squaring
- Euler's theorem for correctness intuition
- Padding schemes in practical deployments

## Complexity notes
- Modular exponentiation: O(log n) multiplications
- Security depends on key size and implementation hardness

## Pitfalls
- Using RSA without padding or with small exponents
- Reusing keys across contexts without proper protocols

## References
- Katz and Lindell, Introduction to Modern Cryptography
- Ferguson, Schneier, Kohno, Cryptography Engineering
