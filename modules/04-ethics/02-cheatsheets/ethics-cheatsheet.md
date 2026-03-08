# Ethics Cheat Sheet

## Fairness Criteria Quick Reference

| Criterion | Definition | Intuitive meaning | Best fit | Main conflict |
| --- | --- | --- | --- | --- |
| Demographic parity | `P(Y_hat = 1 | G = A) = P(Y_hat = 1 | G = B)` | Groups receive positive outcomes at equal rates | Allocation or outreach decisions | Often conflicts with calibration when base rates differ |
| Equalized odds | Equal TPR and FPR across groups | Groups bear similar error burdens | High-stakes classification | Often conflicts with predictive parity |
| Predictive parity / calibration | Same score implies same empirical risk across groups | A score means the same thing for everyone | Risk scoring and ranking | Often conflicts with equalized odds |
| Individual fairness | Similar individuals treated similarly | Like cases treated alike | Domains with a defensible similarity metric | Hardest part is defining similarity |

## Decision Tree

### Facing an ethics question about a system?

```text
Is there established professional consensus or a code-based duty?
├─ Yes -> Follow the code-based obligation, document the reasoning, and verify the system actually matches the code's concern.
└─ No ->
   Is there documented empirical harm already?
   ├─ Yes -> Treat the harm as real, not speculative; analyze whether deployment can still be justified.
   └─ No ->
      Is the issue contested mainly in application rather than principle?
      ├─ Yes -> State the principle, identify the facts that remain uncertain, and use narrower deployment plus escalation.
      └─ No ->
         Are reasonable professionals split in principle?
         ├─ Yes -> Present the competing positions charitably, make the trade-off explicit, and do not decide unilaterally.
         └─ No ->
            Does organizational pressure conflict with your ethical analysis?
            ├─ Minor conflict -> Raise internally, document, and seek review.
            └─ Major conflict -> Escalate through formal channels and assess whistleblower protections.
```

## Compact Glossary

- **Descriptive register** - factual account of what a system or organization does.
- **Analytical register** - framework-based reasoning from facts to implications.
- **Normative register** - claim about what ought to be done.
- **Contextual integrity** - privacy framework asking whether information flow fits the norms of the original context.
- **Differential privacy** - formal guarantee limiting how much one person's data can affect a released result.
- **Specification gaming** - optimizer exploits the written objective while defeating the intended goal.
- **Coordinated disclosure** - reporting a vulnerability with time for remediation before public release.
- **Copyleft** - licensing model that conditions reuse on sharing source or modifications under similar terms.
- **Chilling effect** - lawful behavior changes because people know or fear they are being observed.
- **Recourse** - a real path for a person to contest, appeal, or correct a system decision.

## Key Formulas / Index Formulas

### Fairness metrics

```text
Demographic parity:
P(Y_hat = 1 | G = A) = P(Y_hat = 1 | G = B)
```

```text
Equalized odds:
P(Y_hat = 1 | Y = y, G = A) = P(Y_hat = 1 | Y = y, G = B)
for y in {0, 1}
```

```text
Positive predictive value by group:
PPV_g = (pi_g * TPR_g) / (pi_g * TPR_g + (1 - pi_g) * FPR_g)
```

If `pi_A != pi_B` and `TPR` and `FPR` are equal across groups, then `PPV_A != PPV_B`.
That is the core impossibility tension between equalized odds and predictive parity.

### Differential privacy

```text
M is epsilon-DP if
P(M(D) in S) <= exp(epsilon) * P(M(D') in S)
for all neighboring datasets D, D' and output sets S
```

## Debugging / Diagnosis

| Symptom | Likely reasoning error or root cause |
| --- | --- |
| "It is legal, so it is fine" | Legal compliance is being treated as ethical clearance |
| "We did not intend harm" | Responsibility is being reduced to intent instead of foreseeable impact |
| "The model is fair" | No fairness criterion has been named or justified |
| "Users clicked agree" | Consent is being treated as meaningful without checking coercion, comprehension, or revocability |
| "Security research means we can keep probing" | Good-faith research boundary is being confused with unlimited access |
| "The license is open source, so we can do anything" | License obligations and compatibility were ignored |
| "The tool is neutral; others decide how it is used" | The neutral-tool defense is obscuring foreseeable misuse and power asymmetry |

## When NOT to Use

| Tool / pattern | Avoid when |
| --- | --- |
| Demographic parity as the sole fairness target | qualification rates differ and error burdens matter more than selection rates |
| Consent as the primary privacy justification | users face dark patterns, dependency, or cannot realistically refuse |
| Full vulnerability disclosure immediately | exploit detail would likely create avoidable user harm before mitigation exists |
| Black-box explainability overlays | high-stakes decisions require inherently interpretable or more controllable models |
| Copyleft-licensed dependencies | the organization is unwilling to comply with reciprocity obligations |
| Surveillance features by default | necessity, minimization, oversight, and recourse are absent |

## References

- ACM. 2018. ACM Code of Ethics and Professional Conduct. <https://www.acm.org/code-of-ethics>
- Nissenbaum, Helen. 2004. Privacy as Contextual Integrity. *Washington Law Review* 79(1): 119-157. <https://digitalcommons.law.uw.edu/wlr/vol79/iss1/10>
- Dwork, Cynthia, Moritz Hardt, Toniann Pitassi, Omer Reingold, and Richard Zemel. 2012. Fairness Through Awareness. *ITCS 2012*. <https://doi.org/10.1145/2090236.2090255>
- Hardt, Moritz, Eric Price, and Nati Srebro. 2016. Equality of Opportunity in Supervised Learning. *arXiv*. <https://arxiv.org/abs/1610.02413>
- Chouldechova, Alexandra. 2017. Fair Prediction with Disparate Impact. *Big Data* 5(2). <https://doi.org/10.1089/big.2016.0047>
- NIST. 2023. *AI Risk Management Framework (AI RMF 1.0)*. <https://doi.org/10.6028/NIST.AI.100-1>
- Software Engineering Institute. 2017. *The CERT Guide to Coordinated Vulnerability Disclosure*. <https://www.sei.cmu.edu/documents/1945/2017_003_001_503340.pdf>
