# RSA and Padding

## Key Ideas
- RSA is a public-key cryptosystem built from modular arithmetic over a composite modulus `n = pq`.
- RSA correctness depends on choosing exponents that are inverses modulo a totient-related quantity.
- Encryption, key transport, and signatures are distinct RSA uses and require different secure encodings.
- Textbook RSA is not secure in practice because it is deterministic for encryption and structurally unsafe for raw signatures.
- Real RSA security depends on padding, key generation discipline, parameter validation, and constant-time implementation details.

## 1. Why RSA still matters

RSA is historically central because it made public-key cryptography practical and remains widely used in certificates, signatures, and legacy systems. It is also pedagogically valuable because it connects earlier number theory directly to a deployable cryptographic construction.

That said, RSA should not be learned as "raise to the `e` or `d` power and you are done." Real security comes from the surrounding construction, not from textbook exponentiation alone.

## 2. Key generation and core arithmetic

RSA starts with two large primes `p` and `q`.

Compute:

- `n = pq`
- `phi(n) = (p - 1)(q - 1)` for distinct primes

Choose a public exponent `e` such that:

`gcd(e, phi(n)) = 1`

Then compute the private exponent `d` satisfying:

`ed ≡ 1 (mod phi(n))`

The public key is `(n, e)`. The private key includes `d` and usually CRT-related values for faster private-key operations.

## 3. Encryption, signatures, and padding

Textbook RSA encryption uses:

`c = m^e mod n`

and decryption uses:

`m = c^d mod n`

Textbook RSA signatures reverse the exponent roles conceptually, but secure signature systems never sign raw messages directly. Instead:

- RSA-OAEP is used for encryption or key transport style constructions
- RSA-PSS is used for signatures

These encodings matter because they add structure, randomness, and security properties that raw exponentiation lacks.

## 4. Worked example: toy RSA arithmetic

Choose:

- `p = 5`
- `q = 11`

Then:

- `n = 55`
- `phi(n) = (5 - 1)(11 - 1) = 40`

Choose:

`e = 3`

Check:

`gcd(3, 40) = 1`

Find `d` such that:

`3d ≡ 1 (mod 40)`

A valid choice is:

`d = 27`

because:

`3 * 27 = 81 ≡ 1 (mod 40)`

Now encrypt message `m = 12`:

`c = 12^3 mod 55`

Compute:

- `12^2 = 144 ≡ 34 (mod 55)`
- `12^3 ≡ 34 * 12 = 408 ≡ 23 (mod 55)`

So:

`c = 23`

Decrypt:

`m = 23^27 mod 55`

Use repeated squaring:

- `23^2 ≡ 34 (mod 55)`
- `23^4 ≡ 34^2 = 1156 ≡ 1 (mod 55)`
- `23^8 ≡ 1`
- `23^16 ≡ 1`

Since `27 = 16 + 8 + 2 + 1`:

`23^27 ≡ 23^16 * 23^8 * 23^2 * 23 ≡ 1 * 1 * 34 * 23 = 782 ≡ 12 (mod 55)`

So the message is recovered.

Verification: encrypting `12` yields `23`, and decrypting `23` recovers `12`.

## 5. Practical security lessons

The example above proves arithmetic correctness, not practical security. Textbook RSA encryption is deterministic, which leaks structure. Raw RSA signatures are vulnerable to forgery-style reasoning because they lack secure hashing and formatting.

Modern practice therefore treats RSA as one component inside a secure scheme:

- OAEP for encryption-style use
- PSS for signatures
- validated key sizes and parameters
- constant-time implementations

This is why RSA is best understood as a case study in how mathematics and engineering meet.

## 6. Common Mistakes

1. **Textbook-deployment mistake**: using raw RSA formulas directly in applications ignores known attacks; use vetted constructions like OAEP and PSS.
2. **Role confusion**: treating encryption and signing as the same operation with swapped exponents misses different security goals and encodings; keep the use cases distinct.
3. **Small-key intuition**: extrapolating from toy primes to real deployments hides the enormous security gap between arithmetic examples and actual parameter sizes; use small numbers only for explanation.
4. **Range-validation omission**: failing to validate encoded message structure and key parameters can break both correctness and security; treat parsing and validation as part of the design.
5. **Math-only security thinking**: believing the theorem alone secures the system ignores side channels, padding oracles, and protocol misuse; evaluate the whole implementation context.

## 7. Practical Checklist

- [ ] State clearly whether RSA is being used for encryption-style key transport or for signatures.
- [ ] Use OAEP for encryption-related use and PSS for signatures in modern systems.
- [ ] Treat the toy arithmetic example as a correctness demonstration only.
- [ ] Validate key sizes, exponents, and encoded message formats before use.
- [ ] Prefer vetted libraries for modular arithmetic and side-channel-resistant operations.
- [ ] Check whether a newer elliptic-curve or hybrid construction is more appropriate for the deployment.

## References

1. Ronald L. Rivest, Adi Shamir, and Leonard Adleman, *A Method for Obtaining Digital Signatures and Public-Key Cryptosystems*. [https://doi.org/10.1145/359340.359342](https://doi.org/10.1145/359340.359342)
2. Jonathan Katz and Yehuda Lindell, *Introduction to Modern Cryptography*. [https://www.routledge.com/Introduction-to-Modern-Cryptography/Katz-Lindell/p/book/9780815354369](https://www.routledge.com/Introduction-to-Modern-Cryptography/Katz-Lindell/p/book/9780815354369)
3. Dan Boneh and Victor Shoup, *A Graduate Course in Applied Cryptography*. [https://toc.cryptobook.us/](https://toc.cryptobook.us/)
4. NIST SP 800-56B Rev. 3, *Integer Factorization Cryptography*. [https://csrc.nist.gov/pubs/sp/800/56/b/r3/final](https://csrc.nist.gov/pubs/sp/800/56/b/r3/final)
5. Alfred J. Menezes, Paul C. van Oorschot, and Scott A. Vanstone, *Handbook of Applied Cryptography*. [https://cacr.uwaterloo.ca/hac/](https://cacr.uwaterloo.ca/hac/)
6. Ferguson, Schneier, and Kohno, *Cryptography Engineering*. [https://www.schneier.com/books/cryptography_engineering/](https://www.schneier.com/books/cryptography_engineering/)
7. RFC 8017, *PKCS #1: RSA Cryptography Specifications*. [https://www.rfc-editor.org/rfc/rfc8017](https://www.rfc-editor.org/rfc/rfc8017)
