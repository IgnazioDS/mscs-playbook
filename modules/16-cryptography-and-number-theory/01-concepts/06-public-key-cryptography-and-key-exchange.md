# Public-Key Cryptography and Key Exchange

## Key Ideas
- Public-key cryptography separates public operations from private operations so parties can communicate securely without sharing a secret in advance.
- Key exchange solves the problem of establishing a shared secret over an insecure channel.
- Public-key encryption, digital signatures, and key agreement are distinct tools with different security goals.
- The discrete logarithm problem and related hardness assumptions support many key-exchange and signature systems.
- Real deployments use public-key methods mainly to authenticate parties and establish symmetric session keys, not to encrypt all traffic directly.

## 1. Why public-key cryptography was a breakthrough

Symmetric cryptography works well only if both parties already share a secret key. This creates a scaling problem. A network with many participants cannot realistically pre-distribute a unique shared secret between every pair.

Public-key cryptography changes that model. A participant publishes a public key and keeps a private key secret. Others can use the public key for encryption or verification, while only the private-key holder can decrypt or sign.

This does not eliminate the need for symmetric cryptography. It makes secure key establishment and identity binding possible at scale.

## 2. Encryption, signatures, and key exchange

Three different goals often get grouped together:

- **public-key encryption**: keep content secret from outsiders
- **digital signatures**: prove origin and integrity
- **key exchange / key agreement**: derive a shared secret between parties

These goals are related but not interchangeable. A signature does not provide secrecy, and encryption does not prove who created the ciphertext. Key exchange is often preferred to raw public-key encryption for session establishment because it composes better with forward secrecy.

## 3. Diffie-Hellman intuition

The classic Diffie-Hellman idea uses exponentiation in a group where the **discrete logarithm problem** is believed hard.

Public parameters:

- a group generator `g`
- a modulus or group context

Alice chooses secret `a` and sends `g^a`.
Bob chooses secret `b` and sends `g^b`.

Both compute:

`g^(ab)`

because:

- Alice computes `(g^b)^a`
- Bob computes `(g^a)^b`

An eavesdropper sees `g`, `g^a`, and `g^b`, but is assumed unable to compute `g^(ab)` efficiently without solving a hard problem.

## 4. Worked example: toy Diffie-Hellman exchange

Use a small toy setting with prime modulus `23` and generator `5`. These values are not secure; they are for arithmetic illustration only.

Alice chooses secret:

`a = 6`

Bob chooses secret:

`b = 15`

Alice sends:

`A = 5^6 mod 23`

Compute:

- `5^2 = 25 ≡ 2 (mod 23)`
- `5^4 ≡ 2^2 = 4 (mod 23)`
- `5^6 ≡ 5^4 * 5^2 ≡ 4 * 2 = 8 (mod 23)`

So `A = 8`.

Bob sends:

`B = 5^15 mod 23`

Use repeated squaring:

- `5^1 ≡ 5`
- `5^2 ≡ 2`
- `5^4 ≡ 4`
- `5^8 ≡ 16`

Since `15 = 8 + 4 + 2 + 1`:

`5^15 ≡ 16 * 4 * 2 * 5 = 640 ≡ 19 (mod 23)`

So `B = 19`.

Shared secret from Alice's side:

`B^a = 19^6 mod 23`

Compute:

- `19^2 = 361 ≡ 16 (mod 23)`
- `19^4 ≡ 16^2 = 256 ≡ 3 (mod 23)`
- `19^6 ≡ 19^4 * 19^2 ≡ 3 * 16 = 48 ≡ 2 (mod 23)`

Shared secret from Bob's side:

`A^b = 8^15 mod 23`

Compute:

- `8^2 = 64 ≡ 18`
- `8^4 ≡ 18^2 = 324 ≡ 2`
- `8^8 ≡ 2^2 = 4`

Then:

`8^15 ≡ 8^8 * 8^4 * 8^2 * 8 ≡ 4 * 2 * 18 * 8 = 1152 ≡ 2 (mod 23)`

Both sides derive the same value `2`.

Verification: both computations reduce to the same shared secret `2 mod 23`.

## 5. Why public-key methods rarely handle bulk data alone

Public-key operations are computationally expensive relative to symmetric operations. They are also more exposed to subtle misuse. Modern protocols therefore use public-key cryptography to:

- authenticate identities
- establish or protect session keys
- verify software, certificates, or messages

Then they use symmetric cryptography for bulk traffic.

## 6. Common Mistakes

1. **Goal mixing**: assuming key exchange, encryption, and signatures are interchangeable because they all use public keys leads to protocol confusion; map each task to the correct primitive.
2. **Toy-parameter extrapolation**: learning Diffie-Hellman from small arithmetic examples is fine, but treating those parameters as representative of real security is not; separate pedagogy from deployment.
3. **Bulk-encryption misuse**: trying to encrypt large data directly with public-key systems is inefficient and often architecturally wrong; use hybrid encryption.
4. **Authentication omission**: a key exchange without identity authentication can permit man-in-the-middle attacks; bind the exchange to authenticated identities when the setting requires it.
5. **Hardness-handwave**: saying "discrete log is hard" without naming the group ignores that some groups are weak or poorly parameterized; the algebraic setting is part of the security claim.

## 7. Practical Checklist

- [ ] State whether the system needs encryption, signatures, key exchange, or some combination.
- [ ] Treat public-key cryptography as the setup layer for symmetric session protection in ordinary network protocols.
- [ ] Use authenticated key exchange when active attackers are part of the threat model.
- [ ] Remember that hardness claims depend on the group or modulus used.
- [ ] Keep toy examples separate from real parameter choices and standards.
- [ ] Evaluate how public keys are distributed, validated, and revoked in the larger system.

## References

1. Whitfield Diffie and Martin Hellman, *New Directions in Cryptography*. [https://ee.stanford.edu/~hellman/publications/24.pdf](https://ee.stanford.edu/~hellman/publications/24.pdf)
2. Dan Boneh and Victor Shoup, *A Graduate Course in Applied Cryptography*. [https://toc.cryptobook.us/](https://toc.cryptobook.us/)
3. Jonathan Katz and Yehuda Lindell, *Introduction to Modern Cryptography*. [https://www.routledge.com/Introduction-to-Modern-Cryptography/Katz-Lindell/p/book/9780815354369](https://www.routledge.com/Introduction-to-Modern-Cryptography/Katz-Lindell/p/book/9780815354369)
4. NIST SP 800-56A, *Pair-Wise Key-Establishment Schemes Using Discrete Logarithm Cryptography*. [https://csrc.nist.gov/pubs/sp/800/56/a/r3/final](https://csrc.nist.gov/pubs/sp/800/56/a/r3/final)
5. Christof Paar and Jan Pelzl, *Understanding Cryptography*. [https://www.crypto-textbook.com/](https://www.crypto-textbook.com/)
6. RFC 8446, *The Transport Layer Security (TLS) Protocol Version 1.3*. [https://www.rfc-editor.org/rfc/rfc8446](https://www.rfc-editor.org/rfc/rfc8446)
7. Ferguson, Schneier, and Kohno, *Cryptography Engineering*. [https://www.schneier.com/books/cryptography_engineering/](https://www.schneier.com/books/cryptography_engineering/)
