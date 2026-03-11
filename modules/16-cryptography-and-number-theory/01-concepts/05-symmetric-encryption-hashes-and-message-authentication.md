# Symmetric Encryption, Hashes, and Message Authentication

## Key Ideas
- Symmetric cryptography uses the same shared secret for both protection and recovery operations, making it efficient and foundational in real systems.
- Encryption, hashing, and message authentication codes solve different problems and should not be confused with one another.
- Block ciphers and stream ciphers need modes of operation and nonce discipline to be secure in practice.
- Cryptographic hash functions compress arbitrary-length input into fixed-length digests while aiming to resist collision and preimage attacks.
- Message authentication codes provide integrity and authenticity for parties that share a secret key.

## 1. Why symmetric primitives come first in deployment

Most real-world encrypted traffic is protected with symmetric cryptography because it is much faster than public-key cryptography. Public-key methods usually help establish keys or verify identities, but once a session key exists, the bulk data is handled symmetrically.

Three primitive families appear constantly:

- **encryption** for confidentiality
- **hash functions** for digesting and commitment-like uses
- **message authentication codes (MACs)** for integrity and authenticity under a shared secret

Understanding the differences among these is necessary before studying public-key compositions.

## 2. Encryption versus hashing versus MACs

A **symmetric encryption scheme** turns plaintext into ciphertext using a secret key. Decryption should reverse that process for someone with the same key.

A **hash function** maps arbitrary input to a fixed-length digest. It is not meant to be reversible.

A **message authentication code** uses a secret key to produce a tag that the receiver can verify. Unlike a plain hash, a MAC depends on secret material and therefore supports authentication between sharing parties.

These are not interchangeable:

- a hash does not hide the message
- encryption alone does not necessarily detect tampering
- a MAC does not hide content

## 3. Modes, nonces, and authenticated encryption

Block ciphers like AES operate on fixed-size blocks. To encrypt longer messages securely, a **mode of operation** is needed. Modern practice often uses **authenticated encryption**, which combines confidentiality and integrity in one construction, such as AES-GCM or ChaCha20-Poly1305.

A **nonce** is a value that should not repeat under the same key for many constructions. Nonce reuse can be catastrophic because it can reveal relationships between plaintexts or break authentication guarantees.

## 4. Worked example: why a MAC is not a plain hash

Suppose two systems share a secret key `K = "s3cr3t"`.

They want to protect the message:

`M = "transfer:100"`

If they send only the hash:

`H(M)`

an attacker can replace the message with:

`M' = "transfer:900"`

and compute `H(M')` too, because hashing uses no secret.

Now suppose they use a keyed MAC:

`tag = MAC(K, M)`

The attacker can still see `M`, but cannot forge `MAC(K, M')` without the key.

The design lesson is:

- hashes help detect accidental change when both sides trust the source
- MACs help detect malicious tampering when a shared secret exists

Verification: the attacker can recompute a plain hash of a modified message, but cannot recompute a valid MAC without the shared secret.

## 5. Where symmetric cryptography fits in the module

This page comes before public-key cryptography because modern systems are hybrid. Public-key methods rarely replace symmetric protection; they support it. A secure mental model of deployed cryptography begins with what symmetric primitives do well and what they do not do on their own.

## 6. Common Mistakes

1. **Primitive conflation**: using a hash where a MAC is needed, or encryption where authentication is needed, breaks the security goal; identify the exact primitive required for each property.
2. **Nonce reuse**: repeating a nonce under the same key can destroy confidentiality or authenticity guarantees; enforce nonce uniqueness rules in the implementation.
3. **Mode neglect**: treating a block cipher as secure without specifying a mode of operation hides a critical design decision; always name the construction, not just the cipher.
4. **Hash-overtrust**: assuming a cryptographic hash authenticates a sender ignores the lack of secret input; use MACs or digital signatures for authenticity.
5. **Key-sharing sprawl**: using one symmetric key across too many roles or systems increases blast radius; segment keys by purpose and context.

## 7. Practical Checklist

- [ ] State whether the need is confidentiality, integrity, authenticity, or a combination.
- [ ] Use authenticated encryption for ordinary message protection unless there is a strong reason not to.
- [ ] Treat nonce management as part of the security design, not as a minor parameter choice.
- [ ] Use plain hashes for integrity-like checking only when adversarial tampering is not the main concern.
- [ ] Use MACs when both parties can share a secret and authenticity is required.
- [ ] Separate keys by algorithm, role, and purpose where possible.

## References

1. Dan Boneh and Victor Shoup, *A Graduate Course in Applied Cryptography*. [https://toc.cryptobook.us/](https://toc.cryptobook.us/)
2. Jonathan Katz and Yehuda Lindell, *Introduction to Modern Cryptography*. [https://www.routledge.com/Introduction-to-Modern-Cryptography/Katz-Lindell/p/book/9780815354369](https://www.routledge.com/Introduction-to-Modern-Cryptography/Katz-Lindell/p/book/9780815354369)
3. NIST, *Block Cipher Modes of Operation*. [https://csrc.nist.gov/projects/block-cipher-techniques](https://csrc.nist.gov/projects/block-cipher-techniques)
4. RFC 8439, *ChaCha20 and Poly1305 for IETF Protocols*. [https://www.rfc-editor.org/rfc/rfc8439](https://www.rfc-editor.org/rfc/rfc8439)
5. NIST FIPS 197, *Advanced Encryption Standard (AES)*. [https://csrc.nist.gov/pubs/fips/197/final](https://csrc.nist.gov/pubs/fips/197/final)
6. Ferguson, Schneier, and Kohno, *Cryptography Engineering*. [https://www.schneier.com/books/cryptography_engineering/](https://www.schneier.com/books/cryptography_engineering/)
7. Christof Paar and Jan Pelzl, *Understanding Cryptography*. [https://www.crypto-textbook.com/](https://www.crypto-textbook.com/)
