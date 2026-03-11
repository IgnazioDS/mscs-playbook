# Security Goals, Threat Models, and Hardness Assumptions

## Key Ideas
- Cryptography is not only about formulas; it is about what guarantee a system is supposed to provide against which adversary.
- Security goals such as confidentiality, integrity, authenticity, and forward secrecy are distinct and require different constructions.
- A threat model defines attacker capabilities, such as eavesdropping, tampering, chosen-plaintext access, or chosen-ciphertext access.
- Hardness assumptions explain why breaking a scheme is believed to be computationally infeasible, but they do not replace careful protocol design.
- A mathematically interesting transformation becomes cryptography only when its security claim is stated precisely.

## 1. Why cryptography starts with goals

It is possible to build a mathematically elegant system that is useless for the real problem because the wrong goal was chosen. Encryption protects confidentiality, but it does not by itself ensure integrity. Hashing detects accidental differences, but without a secret it does not authenticate a sender.

This is why cryptography begins with questions like:

- what should an attacker be unable to learn
- what modifications should be detectable
- who is allowed to prove authorship
- what compromise should remain local rather than spreading to past sessions

Without precise goals, scheme selection becomes guesswork.

## 2. Threat models and attack surfaces

A **threat model** describes what the attacker can do. Examples:

- observe ciphertexts
- choose plaintexts and see corresponding ciphertexts
- tamper with messages in transit
- submit chosen ciphertexts for decryption
- compromise endpoint storage or key material

The same scheme can be acceptable under one threat model and unacceptable under another. This is why "works in the lab" and "secure in deployment" are very different claims.

## 3. Security notions and hardness assumptions

Modern cryptography formalizes goals with security notions such as indistinguishability under chosen-plaintext attack or existential unforgeability under chosen-message attack. These definitions are paired with **hardness assumptions**, such as:

- factoring large composite integers is hard
- the discrete logarithm problem is hard in a chosen group

Hardness assumptions are not proofs that attacks are impossible. They are reasons to believe attacks are computationally impractical under stated conditions.

## 4. Worked example: why confidentiality and integrity are different

Suppose a team wants to protect an API token sent from client to server. They consider two options:

1. encryption only
2. encryption plus authentication

Assume the attacker can intercept and alter messages in transit.

If the team uses encryption only, the token contents may be hidden, but the attacker may still:

- replay an old encrypted token
- replace the ciphertext with another valid-looking blob
- exploit malleability if the encryption mode allows controlled modification

If the team uses authenticated encryption, the receiver checks both:

- whether the message decrypts
- whether the authenticity tag verifies

The design insight is:

- confidentiality answers "can the attacker read it"
- integrity/authenticity answer "can the attacker modify or fake it"

Verification: the example separates secrecy from tamper resistance, which are distinct security goals under the stated active-attacker model.

## 5. Why this page belongs before concrete schemes

Readers often encounter cryptosystems as a list of named algorithms. That encourages cargo-cult design. This page comes first because later pages on symmetric, public-key, and protocol design only make sense if the reader can state what each primitive is supposed to guarantee and under what assumptions.

## 6. Common Mistakes

1. **Goal conflation**: assuming encryption automatically provides integrity or authenticity leads to incomplete designs; map each requirement to an explicit primitive or construction.
2. **Threat-model omission**: evaluating a scheme without stating attacker capabilities makes the security claim meaningless; write down the adversary powers before choosing a design.
3. **Hardness absolutism**: saying a problem is "impossible" rather than "assumed hard" overstates the claim; keep computational assumptions explicit and conditional.
4. **Primitive substitution**: using hashes, ciphers, or signatures interchangeably because they all look cryptographic produces broken protocols; match the primitive to the exact security property.
5. **Protocol blindness**: focusing only on the algorithm while ignoring key handling, nonce reuse, and message context misses real-world failure modes; evaluate the whole construction, not just the math core.

## 7. Practical Checklist

- [ ] State the exact security goal before selecting an algorithm.
- [ ] Write down the attacker's capabilities and access assumptions.
- [ ] Separate confidentiality, integrity, authenticity, and forward secrecy in design discussions.
- [ ] Treat hardness assumptions as conditional reasoning, not as absolute guarantees.
- [ ] Check whether the deployment environment changes the threat model materially.
- [ ] Evaluate the protocol and key lifecycle, not only the primitive name.

## References

1. Jonathan Katz and Yehuda Lindell, *Introduction to Modern Cryptography*. [https://www.routledge.com/Introduction-to-Modern-Cryptography/Katz-Lindell/p/book/9780815354369](https://www.routledge.com/Introduction-to-Modern-Cryptography/Katz-Lindell/p/book/9780815354369)
2. Dan Boneh and Victor Shoup, *A Graduate Course in Applied Cryptography*. [https://toc.cryptobook.us/](https://toc.cryptobook.us/)
3. NIST, *Glossary and Security Publications Index*. [https://csrc.nist.gov/](https://csrc.nist.gov/)
4. Christof Paar and Jan Pelzl, *Understanding Cryptography*. [https://www.crypto-textbook.com/](https://www.crypto-textbook.com/)
5. Phillip Rogaway and Thomas Shrimpton, *A Provable-Security Treatment of the Key-Wrap Problem*. [https://web.cs.ucdavis.edu/~rogaway/papers/](https://web.cs.ucdavis.edu/~rogaway/papers/)
6. Ferguson, Schneier, and Kohno, *Cryptography Engineering*. [https://www.schneier.com/books/cryptography_engineering/](https://www.schneier.com/books/cryptography_engineering/)
7. NIST SP 800 Series, *Cryptographic Standards*. [https://csrc.nist.gov/publications/sp800](https://csrc.nist.gov/publications/sp800)
