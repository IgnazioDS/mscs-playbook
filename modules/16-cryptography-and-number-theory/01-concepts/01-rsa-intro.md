
# RSA Intro

## Key Ideas

- RSA is a public-key cryptosystem whose security depends on arithmetic over modular integers and the practical difficulty of deriving the private key from the public modulus.
- Correctness comes from number theory: modular exponentiation with a public exponent `e` and private exponent `d` reverses itself on valid messages because `ed ≡ 1 (mod phi(n))`.
- RSA encryption and RSA signatures are different operations with different security goals, even though both use modular exponentiation.
- Textbook RSA is not secure in practice; real deployments require randomized padding for encryption and structured hash-based encoding for signatures.
- The hardest part of RSA in practice is not the formula but the protocol discipline: padding, key generation, parameter validation, and implementation details determine real security.

## 1. What It Is

RSA is a public-key cryptosystem based on modular arithmetic. It uses one key for public operations and a different key for private operations. In the most common use cases, the public key is used to verify signatures or encrypt a small secret, while the private key is used to sign or decrypt.

The core mathematical object is a modulus:

```text
n = pq
```

where `p` and `q` are large primes. The public and private exponents are chosen so that exponentiation with one can be reversed by exponentiation with the other.

RSA is historically important because it was one of the first practical public-key cryptosystems and remains a foundational example in modern cryptography. It is also a good introduction to modular arithmetic, Euler-style correctness arguments, and the distinction between mathematical correctness and practical security.

### 1.1 Core Definitions

- A **public-key cryptosystem** uses a public key for one operation and a private key for the inverse or complementary operation.
- A **modulus** is the integer `n` that defines arithmetic modulo `n`.
- `phi(n)` is Euler’s totient function, equal to `(p - 1)(q - 1)` when `n = pq` for distinct primes `p` and `q`.
- A **public exponent** `e` is chosen so that `gcd(e, phi(n)) = 1`.
- A **private exponent** `d` satisfies `ed ≡ 1 (mod phi(n))`.
- **Modular exponentiation** computes `a^k mod n` efficiently without forming the full integer `a^k`.
- **Padding** is structured preprocessing applied to a message before RSA is used; secure RSA requires padding in real systems.

### 1.2 Why This Matters

RSA matters for two reasons. First, it is one of the canonical examples of public-key cryptography and appears throughout security engineering, certificate infrastructure, and signature systems. Second, it teaches an important lesson: a mathematically correct scheme can still be insecure if used without the right encoding and protocol protections.

For example, textbook RSA encryption is deterministic, which makes it unsuitable for secure encryption. Likewise, raw RSA signing without a proper signature scheme is vulnerable to forgery-style attacks. So RSA is useful not only as an algorithm, but also as a case study in how cryptography moves from mathematics to secure engineering.

## 2. Key Generation and Core Operations

### 2.1 Key Generation

The standard RSA setup is:

1. Choose large distinct primes `p` and `q`.
2. Compute:

```text
n = pq
phi(n) = (p - 1)(q - 1)
```

3. Choose a public exponent `e` such that:

```text
gcd(e, phi(n)) = 1
```

4. Compute the private exponent `d` such that:

```text
ed ≡ 1 (mod phi(n))
```

The public key is typically:

```text
(n, e)
```

and the private key includes:

```text
d
```

along with the factors or CRT parameters in practical implementations.

### 2.2 Encryption and Decryption

In textbook RSA encryption, a message integer `m` with `0 <= m < n` is encrypted as:

```text
c = m^e mod n
```

and decrypted as:

```text
m = c^d mod n
```

This is mathematically simple, but textbook RSA encryption is not secure in practice because it is deterministic and malleable.

### 2.3 Signing and Verification

RSA can also be used for signatures. In the simplified textbook view:

```text
s = m^d mod n
```

and verification checks whether:

```text
m ≡ s^e mod n
```

In real deployments, signatures are not applied directly to raw messages. Instead, the message is hashed and encoded using a signature scheme such as RSA-PSS before the RSA operation is performed.

**Why this matters:** encryption and signing are not interchangeable “because RSA is reversible.” The surrounding encoding and security goals are different.

## 3. Why RSA Works

### 3.1 Modular Inverse Relationship

The exponents `e` and `d` are chosen so that:

```text
ed = 1 + k phi(n)
```

for some integer `k`.

That means exponentiating by `e` and then by `d` is equivalent to raising to the power:

```text
ed
```

which behaves like `1` modulo the relevant multiplicative structure.

### 3.2 Euler-Style Correctness Intuition

For values relatively prime to `n`, Euler’s theorem says:

```text
m^phi(n) ≡ 1 (mod n)
```

So if:

```text
ed = 1 + k phi(n)
```

then:

```text
m^(ed) = m^(1 + k phi(n)) = m * (m^phi(n))^k ≡ m * 1^k ≡ m (mod n)
```

This gives the correctness intuition for why decryption reverses encryption in the modular setting.

### 3.3 Security Intuition

The public key reveals `n` and `e`, but not `d`. To compute `d`, an attacker would typically need information equivalent to knowing `phi(n)`, which in turn is easy to compute if `n` can be factored into `p` and `q`.

So the practical security intuition is that recovering the private key is hard because factoring a large RSA modulus is believed to be hard for classical computers at appropriate key sizes.

This is a practical hardness assumption, not a proof of impossibility.

## 4. Worked Example

Use a small toy example for arithmetic clarity. These numbers are far too small for real security.

Choose:

```text
p = 5
q = 11
```

Then:

```text
n = pq = 55
phi(n) = (5 - 1)(11 - 1) = 4 * 10 = 40
```

Choose:

```text
e = 3
```

Check:

```text
gcd(3, 40) = 1
```

Now find `d` such that:

```text
3d ≡ 1 (mod 40)
```

A valid choice is:

```text
d = 27
```

because:

```text
3 * 27 = 81 ≡ 1 (mod 40)
```

### 4.1 Encrypt a Message

Let the message be:

```text
m = 12
```

Encrypt:

```text
c = 12^3 mod 55
```

Compute:

```text
12^2 = 144 ≡ 34 (mod 55)
12^3 = 12 * 34 = 408 ≡ 23 (mod 55)
```

So the ciphertext is:

```text
c = 23
```

### 4.2 Decrypt the Ciphertext

Now compute:

```text
m = 23^27 mod 55
```

Using repeated squaring:

```text
23^2 ≡ 34 (mod 55)
23^4 ≡ 34^2 = 1156 ≡ 1 (mod 55)
23^8 ≡ 1
23^16 ≡ 1
```

Since:

```text
27 = 16 + 8 + 2 + 1
```

we get:

```text
23^27 ≡ 23^16 * 23^8 * 23^2 * 23
      ≡ 1 * 1 * 34 * 23
      ≡ 782
      ≡ 12 (mod 55)
```

So decryption recovers:

```text
m = 12
```

Verification: encryption maps `12` to `23`, and decryption maps `23` back to `12`. The toy RSA instance is arithmetically correct. Correct.

## 5. Practical Security Notes

### 5.1 Textbook RSA Is Not Enough

Raw RSA formulas are useful for explanation, but not for secure deployment.

For encryption, modern practice uses schemes such as RSA-OAEP rather than textbook RSA. For signatures, modern practice uses a scheme such as RSA-PSS rather than raising raw messages directly to the private exponent.

### 5.2 Padding and Randomization

Padding adds structure and, for encryption, randomness. This prevents deterministic leakage and protects against a range of chosen-ciphertext and structural attacks.

A secure RSA implementation is therefore really a secure RSA-based construction, not just modular exponentiation.

### 5.3 Performance and Implementation

RSA operations are dominated by modular exponentiation. Practical implementations use optimizations such as repeated squaring and Chinese Remainder Theorem acceleration for private-key operations.

Even then, RSA is relatively expensive compared with symmetric cryptography, which is why RSA is usually used to exchange or protect small secrets rather than to encrypt large data directly.

## 6. Pseudocode Pattern

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

Time: `O(log exponent)` modular multiplications in all cases. Space: `O(1)` auxiliary space.

This repeated-squaring routine is the core arithmetic primitive behind RSA encryption, decryption, signing, and verification.

## 7. Common Mistakes

1. **Textbook-RSA deployment.** Using raw RSA without OAEP or PSS turns a mathematically correct construction into an insecure real-world system.
2. **Encryption-signature conflation.** Treating signing as “just decrypting” or encryption as “just verifying in reverse” ignores the fact that secure constructions for confidentiality and authenticity use different encodings and threat models.
3. **Small-parameter intuition.** Believing that toy examples with tiny primes reflect real security hides the enormous gap between arithmetic demonstration and cryptographic strength.
4. **Unchecked message range.** Applying RSA directly to values outside the valid encoded range, or to malformed padded blocks, breaks correctness or security assumptions.
5. **Hardness-overstatement.** Saying RSA is secure because factoring is impossible is too strong; the security claim is based on a practical hardness assumption at suitable key sizes and implementations.

## 8. Practical Checklist

- [ ] State clearly whether the context is encryption, signatures, or key transport.
- [ ] Use a real padding scheme such as OAEP for encryption and PSS for signatures.
- [ ] Validate that keys and encoded messages satisfy the required range and format constraints.
- [ ] Treat textbook RSA as a teaching model, not a deployment design.
- [ ] Use modular exponentiation by repeated squaring or a vetted library primitive.
- [ ] Keep private-key operations and CRT optimizations inside constant-time, reviewed implementations.
- [ ] Separate mathematical correctness claims from practical security claims.

## 9. References

- Katz, Jonathan, and Yehuda Lindell. 2020. *Introduction to Modern Cryptography* (3rd ed.). CRC Press. <https://www.routledge.com/Introduction-to-Modern-Cryptography/Katz-Lindell/p/book/9780815354369>
- Boneh, Dan, and Victor Shoup. 2020. *A Graduate Course in Applied Cryptography*. <https://toc.cryptobook.us/>
- Menezes, Alfred J., Paul C. van Oorschot, and Scott A. Vanstone. 1996. *Handbook of Applied Cryptography*. CRC Press. <https://cacr.uwaterloo.ca/hac/>
- Ferguson, Niels, Bruce Schneier, and Tadayoshi Kohno. 2010. *Cryptography Engineering*. Wiley. <https://www.schneier.com/books/cryptography_engineering/>
- Rivest, Ronald L., Adi Shamir, and Leonard Adleman. 1978. A Method for Obtaining Digital Signatures and Public-Key Cryptosystems. *Communications of the ACM* 21(2): 120–126. <https://doi.org/10.1145/359340.359342>
- NIST. 2023. *Recommendation for Pair-Wise Key-Establishment Schemes Using Integer Factorization Cryptography (SP 800-56B Rev. 3)*. <https://csrc.nist.gov/pubs/sp/800/56/b/r3/final>
