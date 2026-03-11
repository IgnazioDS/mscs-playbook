# Cryptography and Number Theory

This module connects the mathematical foundations of modular arithmetic and finite fields to the practical design of modern cryptographic systems. It is organized so the reader learns the number theory needed for the algorithms, the security language needed for the claims, and the protocol context needed for deployment.

## Why This Module Matters

Cryptography is where mathematics, systems design, and adversarial thinking meet. It provides tools for confidentiality, integrity, authentication, and trust establishment, but those tools only work when the underlying algebra, threat model, and key lifecycle are all understood together. This module gives a compact but coherent path through that stack.

## Recommended Reading Path

1. [Modular Arithmetic and the Euclidean Algorithm](01-concepts/01-modular-arithmetic-and-the-euclidean-algorithm.md)
2. [Primes, Totients, and Fast Exponentiation](01-concepts/02-primes-totients-and-fast-exponentiation.md)
3. [Chinese Remainder Theorem and Finite Fields](01-concepts/03-chinese-remainder-theorem-and-finite-fields.md)
4. [Security Goals, Threat Models, and Hardness Assumptions](01-concepts/04-security-goals-threat-models-and-hardness-assumptions.md)
5. [Symmetric Encryption, Hashes, and Message Authentication](01-concepts/05-symmetric-encryption-hashes-and-message-authentication.md)
6. [Public-Key Cryptography and Key Exchange](01-concepts/06-public-key-cryptography-and-key-exchange.md)
7. [RSA and Padding](01-concepts/07-rsa-and-padding.md)
8. [Elliptic Curves and Modern Signatures](01-concepts/08-elliptic-curves-and-modern-signatures.md)
9. [Protocols, PKI, and Key Management](01-concepts/09-protocols-pki-and-key-management.md)

## Module Map

- [Concepts](01-concepts/README.md): the main theory and systems sequence
- [Cheatsheets](02-cheatsheets/README.md): compact reminders for arithmetic, primitives, and protocol vocabulary
- [Python Implementations](03-implementations/python/README.md): a future home for arithmetic demos and protocol helpers
- [TypeScript Implementations](03-implementations/typescript/README.md): a future home for web-oriented demos and teaching utilities
- [Case Studies](04-case-studies/README.md): practical cryptographic design scenarios
- [Exercises](05-exercises/README.md): derivations, protocol reasoning, and implementation prompts
- [Notes](06-notes/README.md): supporting observations and follow-up reading

## Suggested Workflow

1. Learn the first three pages as algebraic prerequisites.
2. Read the security-goals page before attaching meaning to any algorithm name.
3. Treat symmetric and public-key cryptography as complementary layers rather than competing alternatives.
4. End with protocols and key management so the module closes on deployment reality instead of isolated primitives.

## Prerequisites

- comfort with basic discrete mathematics
- willingness to work through modular arithmetic examples by hand
- interest in how mathematical assumptions become system guarantees
