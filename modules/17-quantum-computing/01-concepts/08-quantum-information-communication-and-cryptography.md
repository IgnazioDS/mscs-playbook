# Quantum Information, Communication, and Cryptography

## Key Ideas
- Quantum information theory studies what can be transmitted, shared, and protected when the information carrier is quantum rather than classical.
- Quantum communication protocols rely on entanglement, measurement, and no-cloning in ways that differ sharply from classical networking.
- Quantum key distribution (QKD) is a communication protocol family, not a general replacement for classical cryptography.
- Quantum cryptography should be distinguished from post-quantum cryptography, which protects classical systems against quantum attackers without using quantum hardware.
- Communication and cryptography applications reveal why foundational quantum principles matter operationally, not only algorithmically.

## 1. Why this page closes the module

The module starts from qubits and circuits, then moves through algorithms and resource realism. The final step is seeing how the same principles affect communication and security. This is a natural endpoint because it shows where quantum information changes system design beyond algorithmic speedups.

## 2. Quantum information and communication primitives

Quantum communication involves tasks such as:

- sending qubits over a channel
- distributing entanglement
- performing teleportation-like state transfer with classical side information
- detecting eavesdropping through disturbance

These possibilities arise because quantum states cannot generally be copied and because measurement changes the state being observed.

## 3. Quantum key distribution and its limits

QKD protocols such as BB84 aim to let two parties detect whether a key-establishment process has been disturbed by an eavesdropper. The idea is not that QKD makes all cryptography obsolete. Instead, it offers a specialized approach to key establishment under specific physical and infrastructure assumptions.

It is also important to separate:

- **quantum cryptography**, which uses quantum communication mechanisms
- **post-quantum cryptography**, which uses classical algorithms designed to resist quantum attacks

These are different responses to the quantum threat landscape.

## 4. Worked example: BB84-style disturbance intuition

Suppose Alice sends four qubits, each prepared in one of two bases:

- computational basis: `|0>`, `|1>`
- diagonal basis: `|+>`, `|->`

Bob measures each qubit in a randomly chosen basis.

After transmission, Alice and Bob publicly compare only which bases they used, not the bit values. They keep only positions where their bases matched.

Now imagine an eavesdropper Eve measures every qubit in a random basis before forwarding it.

When Eve guesses the wrong basis, she disturbs the state. Later, when Alice and Bob compare a sample of kept bits, they observe an error rate above the expected no-eavesdrop level.

The key intuition is:

- eavesdropping is detectable because measurement in the wrong basis alters the transmitted quantum state

Verification: the protocol's disturbance-detection logic depends on basis mismatch causing detectable errors in the kept sample.

## 5. Why this is not the whole security story

Quantum communication protocols still need:

- authentication of the classical channel
- trusted endpoint behavior
- practical hardware assumptions
- operational cost justification

Likewise, the threat that Shor's algorithm poses to RSA does not automatically make QKD the universal answer. Many systems will instead rely on post-quantum cryptographic schemes implemented on classical hardware.

## 6. Common Mistakes

1. **QKD-universality claim**: treating quantum key distribution as a universal replacement for ordinary cryptography ignores infrastructure and authentication requirements; explain its scope precisely.
2. **Quantum-vs-post-quantum confusion**: conflating quantum cryptography with post-quantum cryptography obscures two very different approaches; keep the terms distinct.
3. **Disturbance-handwave**: saying eavesdropping is "magically detectable" without connecting it to basis mismatch and measurement disturbance weakens the explanation; state the mechanism explicitly.
4. **Algorithm-only framing**: focusing only on Shor and Grover hides the broader information-theoretic consequences of quantum mechanics; include communication and security applications in the mental model.
5. **Hardware-agnostic optimism**: assuming theoretical protocol security directly implies easy deployment ignores channel loss, device trust, and operational complexity; discuss physical assumptions explicitly.

## 7. Practical Checklist

- [ ] Distinguish quantum communication protocols from classical post-quantum defenses.
- [ ] Explain how measurement disturbance supports eavesdropping detection in QKD.
- [ ] Remember that quantum protocols still need authenticated classical coordination.
- [ ] Tie any claimed security benefit to explicit physical and trust assumptions.
- [ ] Use this page to connect algorithmic quantum computing to communication and security system design.
- [ ] Avoid presenting QKD as a general-purpose answer to all quantum-era cryptographic problems.

## References

1. Michael A. Nielsen and Isaac L. Chuang, *Quantum Computation and Quantum Information*. [https://doi.org/10.1017/CBO9780511976667](https://doi.org/10.1017/CBO9780511976667)
2. Charles H. Bennett and Gilles Brassard, *Quantum Cryptography: Public Key Distribution and Coin Tossing*. [https://research.ibm.com/publications/quantum-cryptography-public-key-distribution-and-coin-tossing](https://research.ibm.com/publications/quantum-cryptography-public-key-distribution-and-coin-tossing)
3. John Watrous, *The Theory of Quantum Information*. [https://doi.org/10.1017/9781316848142](https://doi.org/10.1017/9781316848142)
4. Artur Ekert, *Quantum Cryptography Based on Bell's Theorem*. [https://doi.org/10.1103/PhysRevLett.67.661](https://doi.org/10.1103/PhysRevLett.67.661)
5. NIST, *Post-Quantum Cryptography Project*. [https://csrc.nist.gov/projects/post-quantum-cryptography](https://csrc.nist.gov/projects/post-quantum-cryptography)
6. John Preskill, *Lecture Notes for Physics 219/Computer Science 219*. [https://theory.caltech.edu/~preskill/ph219/](https://theory.caltech.edu/~preskill/ph219/)
7. IBM Quantum Learning, *Quantum Communication and Cryptography Materials*. [https://learning.quantum.ibm.com/](https://learning.quantum.ibm.com/)
