# Protocols, PKI, and Key Management

## Key Ideas
- Cryptographic primitives become useful only when they are assembled into protocols with clear message formats, identities, and key lifecycles.
- Public-key infrastructure (PKI) exists to bind identities to public keys through certificates and trust chains.
- Key management includes generation, storage, rotation, revocation, and destruction, and it is often the real failure point in deployed systems.
- A secure primitive can still fail inside an insecure protocol because context, sequencing, and validation matter.
- Protocol review should focus on authentication, freshness, downgrade resistance, and operational recovery, not only on algorithm names.

## 1. Why primitives are not enough

A cipher, signature scheme, or key-agreement method does not by itself describe a secure system. Real systems need to answer:

- who is talking to whom
- how keys are distributed and validated
- how replay is prevented
- what happens when a key is compromised
- how old keys are retired

These are protocol and operations questions. Many high-impact failures happen here rather than inside the underlying primitive.

## 2. Public-key infrastructure

PKI is the machinery that connects public keys to identities. A certificate typically states that a public key belongs to a subject and is vouched for by a certificate authority.

Important PKI concepts include:

- certificate chains
- trust anchors
- revocation
- expiration
- subject validation

The point is not only to distribute keys. It is to distribute keys with a trust statement that recipients can evaluate.

## 3. Key management as a security lifecycle

Key management includes:

- generating keys with enough entropy
- storing keys securely
- separating keys by purpose
- rotating keys when needed
- revoking compromised keys
- destroying keys that should no longer exist

This is where operational reality enters cryptography. A perfect algorithm does not help if private keys are copied into logs, never rotated, or remain active long after compromise.

## 4. Worked example: why certificate validation matters

Suppose a client connects to `api.example.com` over TLS and receives a certificate containing:

- subject name `api.example.com`
- public key `K_pub`
- signature from a certificate authority the client trusts

The client should validate at least:

1. the certificate chain leads to a trusted root
2. the certificate is currently valid in time
3. the hostname matches `api.example.com`
4. the handshake proves possession of the matching private key

If hostname validation is skipped, an attacker with a valid certificate for a different domain may still impersonate the endpoint in some settings.

The lesson is that "certificate present" is not enough. The certificate must match the intended identity and trust context.

Verification: the example shows that successful validation requires chain, time, name, and key-possession checks, not just receipt of a certificate blob.

## 5. Why this is the end of the module

This page comes last because it depends on understanding the primitives first. Once the reader knows what symmetric encryption, public-key systems, and signatures do, the final step is learning how those pieces are composed and maintained in real systems.

## 6. Common Mistakes

1. **Primitive-only thinking**: assuming strong algorithms guarantee a secure system ignores protocol and operations failures; evaluate how primitives are composed and managed.
2. **Certificate-surface checking**: checking that a certificate exists without validating name, chain, and lifetime leaves impersonation risks; perform full certificate validation.
3. **Key-lifecycle neglect**: failing to rotate, revoke, or scope keys appropriately increases compromise impact; treat key management as an ongoing process.
4. **Context-free reuse**: using one key across multiple roles or environments makes incidents harder to contain; separate keys by purpose and trust domain.
5. **No compromise plan**: designing for normal operation only means key exposure turns into prolonged outage or silent misuse; define rotation and recovery procedures in advance.

## 7. Practical Checklist

- [ ] Treat protocol design and key management as part of cryptography, not as peripheral operations.
- [ ] Validate certificates fully, including hostname, chain, and validity interval.
- [ ] Separate keys by role, environment, and cryptographic purpose.
- [ ] Maintain documented rotation and revocation procedures.
- [ ] Check that protocols include authentication, replay resistance, and downgrade resistance where relevant.
- [ ] Plan incident response for key compromise before deployment.

## References

1. Ferguson, Schneier, and Kohno, *Cryptography Engineering*. [https://www.schneier.com/books/cryptography_engineering/](https://www.schneier.com/books/cryptography_engineering/)
2. RFC 5280, *Internet X.509 Public Key Infrastructure Certificate and CRL Profile*. [https://www.rfc-editor.org/rfc/rfc5280](https://www.rfc-editor.org/rfc/rfc5280)
3. RFC 8446, *The Transport Layer Security (TLS) Protocol Version 1.3*. [https://www.rfc-editor.org/rfc/rfc8446](https://www.rfc-editor.org/rfc/rfc8446)
4. NIST SP 800-57, *Recommendation for Key Management*. [https://csrc.nist.gov/pubs/sp/800/57/pt1/r5/final](https://csrc.nist.gov/pubs/sp/800/57/pt1/r5/final)
5. Dan Boneh and Victor Shoup, *A Graduate Course in Applied Cryptography*. [https://toc.cryptobook.us/](https://toc.cryptobook.us/)
6. OWASP, *Transport Layer Protection and Certificate Guidance*. [https://cheatsheetseries.owasp.org/](https://cheatsheetseries.owasp.org/)
7. Jonathan Katz and Yehuda Lindell, *Introduction to Modern Cryptography*. [https://www.routledge.com/Introduction-to-Modern-Cryptography/Katz-Lindell/p/book/9780815354369](https://www.routledge.com/Introduction-to-Modern-Cryptography/Katz-Lindell/p/book/9780815354369)
