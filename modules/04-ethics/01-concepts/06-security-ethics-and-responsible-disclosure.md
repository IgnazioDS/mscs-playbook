# Security Ethics and Responsible Disclosure

## Key Ideas

- Security ethics is about reducing harm under adversarial conditions, not about rewarding cleverness for its own sake.
- Vulnerability disclosure is a coordination problem between researchers, vendors, affected users, and the public, so timing is an ethical variable rather than a mere logistics detail.
- Coordinated disclosure is the professional default because both immediate publication and indefinite silence can impose avoidable public risk.
- Authorization, scope, and good-faith purpose are what separate defensible offensive security work from unethical intrusion.
- Legal permission and ethical permission can diverge: some research may be ethically justified while still carrying legal risk under laws such as the CFAA.

## 1. What It Is

Security ethics studies how professionals should act when they discover,
investigate, disclose, or exploit vulnerabilities. The central problem is that
information about a flaw can protect users or endanger them depending on how it
is handled.

### 1.1 The disclosure spectrum

| Approach | What it means | Main benefit | Main risk |
| --- | --- | --- | --- |
| Full disclosure | Publish immediately with technical detail | Maximizes public transparency and pressure on vendors | Can arm attackers before mitigations exist |
| Coordinated disclosure | Researcher and vendor coordinate remediation before publication | Balances patching time with eventual transparency | Can fail when vendors stall or deny |
| Responsible disclosure | Often used loosely for coordinated disclosure with researcher restraint | Emphasizes harm reduction | Sometimes too deferential and underspecified |
| Non-disclosure | Keep the issue private | Avoids public weaponization in the short term | Leaves users exposed and weakens accountability |

### 1.2 Why coordinated disclosure became the norm

CERT/CC helped institutionalize coordinated vulnerability disclosure as a way
to reduce harm while still getting critical information public. Current CISA
guidance preserves the same logic: when vendors are unresponsive, disclosure may
occur as early as 45 days after the initial contact attempt.

The point is not that 45 days is morally magical. The point is that indefinite
vendor control over publication is also unethical.

## 2. Offensive Security Research

### 2.1 Authorized work

Penetration testing, red-teaming, exploit development, and live-fire exercises
are ethically defensible when they are:

- authorized,
- scoped,
- proportionate to a legitimate security purpose,
- and conducted to avoid unnecessary harm.

### 2.2 Unsolicited research

Unsolicited testing is harder. The ethical case improves when the research is
narrow, good faith, minimally invasive, and stops immediately upon encountering
sensitive data or active compromise. The legal case may still remain uncertain.

### 2.3 Bug bounties

Bug bounty programs create a safer reporting channel, but they do not exhaust
the researcher's obligations. A bounty does not justify data access outside
scope, extortionate behavior, or publication without regard for user harm. It
also does not absolve vendors that define scope so narrowly that serious issues
fall outside the program.

## 3. Law, Good-Faith Research, and Live Incidents

### 3.1 Descriptive register

In the United States, the CFAA remains an important source of legal risk for
security research. The Department of Justice announced on May 19, 2022 that
good-faith security research should not be charged under its revised CFAA
policy.

### 3.2 Analytical register

That policy change matters, but it does not erase all legal ambiguity. Ethical
permission still depends on whether the work is actually aimed at improving
security and whether the researcher avoids unnecessary harm. "Research" used as
a cover for coercion, data extraction, or public recklessness is not good faith.

### 3.3 Discovering a live breach

Finding evidence of active compromise changes the duty. At that point the
primary obligation is harm reduction:

- stop exploratory activity,
- preserve enough evidence to make the report useful,
- notify the authorized owner or coordinator immediately,
- and do not publicize sensitive details while the breach is live.

## 4. Case Study

**Case: Critical flaw in medical device firmware**

**Descriptive register. Situation:**  
A researcher legally purchases an internet-connected insulin pump and, during
local firmware analysis, discovers a remotely reachable flaw that could allow
unauthorized command injection. The vendor acknowledges receipt but, after more
than 90 days, has not issued a patch, has not provided a mitigation timeline,
and continues marketing the product. Patients cannot easily apply their own
fixes and may not even know the device is vulnerable.

**Analytical register. Ethical analysis:**  
From a consequentialist perspective, immediate publication of weaponizable
details could expose patients to severe harm, so public safety weighs in favor
of coordinated disclosure rather than instant full disclosure. But indefinite
silence also carries serious harm because vulnerable devices remain deployed
without pressure or mitigation.  
From a deontological perspective, the researcher has a duty to warn affected
parties and not conceal a life-critical hazard simply because the vendor is
uncomfortable. The vendor, likewise, has a duty not to continue relying on user
ignorance.  
From a virtue-ethics perspective, the responsible researcher is neither
reckless nor passive. Prudence requires careful timing, accurate reporting, and
escalation when the vendor is nonresponsive.

**Analytical register. Competing considerations:**  
The strongest argument for delaying public disclosure is that exploit details
could reach attackers before hospitals or patients can mitigate. The strongest
argument for timed escalation is that the vendor's inertia should not control
the risk faced by patients indefinitely.

**Normative register. What a responsible professional would do:**  
Escalate through a coordinating body such as CISA or CERT/CC, publish a limited
advisory once coordinated timing is exhausted, avoid releasing exploit code
until mitigations exist, and center patient safety over both vendor reputation
and researcher self-promotion.

## 5. Common Mistakes

1. **Treating disclosure timing as a matter of personal style.** Timing is an
   ethical choice because it changes who bears risk and when. It should be
   justified in terms of patchability, exploitability, and public harm.
2. **Assuming a bounty program is the moral boundary.** Program rules matter,
   but they do not answer whether the research is good faith or whether the
   vendor's response is responsible. Ethics does not collapse into platform
   terms.
3. **Equating legality with ethicality.** Some actions may be ethically careful
   yet legally risky, and some legally permitted actions can still be reckless.
   Security professionals must analyze both.
4. **Continuing exploratory access after discovering real user data or an active
   compromise.** Curiosity becomes ethically dangerous once additional probing
   could worsen the incident. Stop, preserve what is needed, and notify.
5. **Publishing for attention rather than remediation.** Public advisories are
   often necessary, but publication framed around prestige rather than user
   safety corrupts the purpose of disclosure.

## 6. Practical Checklist

- [ ] Confirm authorization, scope, and purpose before any offensive security
      activity.
- [ ] Preserve a clear timeline of discovery, vendor contact, follow-up, and
      remediation status.
- [ ] Use coordinated disclosure as the default and document any reason for
      deviating from it.
- [ ] Stop probing immediately if you encounter sensitive user data or signs of
      an active breach.
- [ ] Escalate to a neutral coordinator when a vendor is unresponsive, hostile,
      or operating in critical infrastructure or medical contexts.
- [ ] Separate proof-of-concept evidence needed for remediation from exploit
      detail that would only increase attacker capability.
- [ ] Review both the legal environment and the organization's safe-harbor or
      vulnerability-disclosure policy before publishing.

## 7. References

- Kant, Immanuel. 1785. *Groundwork of the Metaphysics of Morals*. Various scholarly editions.
- Johnson, Deborah G. 2009. *Computer Ethics* (4th ed.). Pearson.
- Software Engineering Institute. 2017. *The CERT Guide to Coordinated Vulnerability Disclosure*. <https://www.sei.cmu.edu/documents/1945/2017_003_001_503340.pdf>
- ISO. 2018. *ISO/IEC 29147:2018 - Information Technology - Security Techniques - Vulnerability Disclosure*. <https://www.iso.org/standard/72311.html>
- CISA. 2026. Coordinated Vulnerability Disclosure Program. <https://www.cisa.gov/coordinated-vulnerability-disclosure-process>
- Bilge, Leyla, and Tudor Dumitras. 2012. Before We Knew It: An Empirical Study of Zero-Day Attacks in the Real World. *ACM CCS 2012*. <https://doi.org/10.1145/2382196.2382284>
- ACM. 2018. ACM Code of Ethics and Professional Conduct. <https://www.acm.org/code-of-ethics>
- U.S. Department of Justice. May 19, 2022. Department of Justice Announces New Policy for Charging Cases under the Computer Fraud and Abuse Act. <https://www.justice.gov/archives/opa/pr/department-justice-announces-new-policy-charging-cases-under-computer-fraud-and-abuse-act>
