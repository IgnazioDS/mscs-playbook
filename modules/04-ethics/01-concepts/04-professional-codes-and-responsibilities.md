# Professional Codes and Responsibilities

## Key Ideas

- Professional ethics in computing is not exhausted by employer loyalty; membership in a profession creates obligations to the public, affected users, and fellow practitioners.
- The ACM and IEEE codes matter because they express professional consensus about harm, honesty, competence, and accountability, not because they substitute for ethical reasoning.
- Whistleblowing is not ordinary disloyalty: when foreseeable harm is serious, internal channels fail, and evidence is credible, disclosure can become an ethical obligation.
- Conflicts of interest distort technical judgment long before they become bribery or corruption; unmanaged incentives can quietly bend design choices toward harmful outcomes.
- "I just wrote the code" fails ethically because participation in a harmful system does not disappear when responsibility is distributed across teams.

## 1. What It Is

Professional ethics concerns the obligations that attach to the role of
computing professional, not just to the private moral character of the person
occupying it. The central question is what engineers owe when their technical
work affects safety, rights, opportunity, and public trust.

### 1.1 Why professional ethics is distinct

An engineer operates inside institutions, under budgets, deadlines, incentives,
and hierarchy. Those conditions matter, but they do not erase responsibility.
Professional ethics exists precisely because powerful technical roles can cause
harm while appearing routine from the inside.

### 1.2 Core obligations

Across major computing codes, the recurring obligations are:

- avoid foreseeable harm,
- be honest about system capabilities and limits,
- maintain competence,
- respect privacy and confidentiality,
- disclose conflicts of interest,
- and support accountability and remediation.

## 2. The ACM and IEEE Codes

### 2.1 Descriptive register

The ACM Code of Ethics and Professional Conduct was updated in 2018. Its four
sections move from general ethical principles to professional responsibilities,
leadership obligations, and compliance.

The IEEE Code of Ethics was updated in 2020. It overlaps heavily with ACM on
public welfare, honesty, competence, fairness, and avoiding injury, but it is
shorter and more oath-like in form.

### 2.2 Analytical register

The ACM Code is most useful when applied section by section:

- **Section 1** frames the public-facing ethical principles, including
  contributing to society and avoiding harm.
- **Section 2** translates those principles into professional duties such as
  competence, review, and respect for rules unless they are ethically
  unjustified.
- **Section 3** emphasizes that leaders are responsible for the systems and
  cultures they create.
- **Section 4** makes compliance part of professional identity rather than a
  decorative appendix.

The IEEE Code complements ACM by stressing honesty, rejection of conflicts,
fair treatment, and willingness to disclose factors that might endanger the
public. Together they support a view of software engineering as a public-trust
profession rather than a purely private service role.

### 2.3 Limitation

Codes identify consensus obligations, but they do not settle every conflict.
They rarely tell a professional exactly when internal escalation becomes
external disclosure, or how to rank confidentiality against urgent public harm.

## 3. Whistleblowing, Conflict, and Organizational Pressure

### 3.1 Whistleblowing

Whistleblowing becomes ethically salient when three conditions converge:

1. the wrongdoing or foreseeable harm is serious,
2. internal reporting channels have failed or are not credible,
3. the whistleblower has evidence strong enough to justify escalation.

Whistleblowing is costly. Empirical work shows retaliation risk remains real,
which is why it should be treated neither as a casual first move nor as a
betrayal that is always out of bounds.

Frances Haugen's October 5, 2021 Senate testimony is a recent computing case:
the ethical claim was not simply that Meta had internal problems, but that the
company's own research allegedly showed systemic harms that public claims and
governance structures were not addressing. Daniel Ellsberg is useful as older
context because he made the same core point from another domain: secrecy and
institutional loyalty do not automatically override public-facing duties.

### 3.2 Conflicts of interest

Conflicts of interest in software engineering are often subtle:

- shipping pressure tied to compensation,
- evaluation metrics tied to growth rather than safety,
- vendor selection by people with undeclared financial ties,
- or review authority granted to teams that benefit from approval.

The ethical duty is not to eliminate every incentive. It is to disclose,
document, and manage them so they do not quietly corrupt judgment.

### 3.3 The "just following orders" problem

An engineer who knowingly enables harmful deployment cannot fully transfer
responsibility upward. Hierarchy changes what options are available. It does not
turn foreseeable harm into someone else's ethics problem.

### 3.4 Organizational ethics

Strong organizations make raising concerns legible:

- clear escalation routes,
- written records,
- retaliation protections,
- independent review,
- and leaders who are accountable for acting on concerns.

Without those features, "speak up internally first" can become a ritual that
absorbs objections without changing anything.

## 4. Case Study

**Case: Illustrative scenario - ranking system repurposed for punitive use**

**Descriptive register. Situation:**  
An engineer built a machine-learning system to prioritize customer-support
tickets by predicted urgency. Six months later, the engineer learns that another
team is using the same scores to rank employees whose cases are associated with
"high-friction interactions," and managers are treating the ranking as a
performance tool. Internal analyses show that employees serving non-native
English speakers and high-conflict regions are penalized more often. The
engineer's manager says the reuse is outside the original team's scope and asks
the engineer not to get involved.

**Analytical register. Ethical analysis:**  
Under the ACM Code's duty to avoid harm and be honest about system limits, the
engineer cannot treat this as a neutral reuse once the new context and harms are
known. The original model was not validated for employment decisions, and the
change in use changes the ethical and professional obligations.  
From a virtue-ethics perspective, professional courage and honesty require the
engineer to raise the issue even if doing so is inconvenient or politically
costly. Silence would display deference, not excellence.  
From a deontological perspective, employees are being treated as means if a
tool built for workflow triage is quietly converted into a disciplinary signal
without notice, explanation, or recourse.

**Analytical register. Competing considerations:**  
The strongest argument for deference is that product teams cannot control every
downstream use and that intervening across org boundaries can create confusion
and duplicated authority. The strongest argument for intervention is that known
misuse, once discovered, creates a fresh responsibility: scope boundaries do not
erase foreseeable harm.

**Normative register. What a responsible professional would do:**  
Document the repurposing, the known limitations, and the group-level harms;
raise the issue through the manager, responsible AI or ethics review channel,
and HR or legal if employment decisions are involved; and continue escalating if
the organization keeps using the tool without validation, notice, and appeal.
If internal avenues fail and the harm is serious, seek protected external advice
before disclosure rather than assuming loyalty requires silence.

## 5. Common Mistakes

1. **Treating codes as ceremonial.** Teams often link the ACM or IEEE code in a
   policy page and then ignore it in launch decisions. A code that never changes
   action is branding, not ethics.
2. **Waiting for certainty before escalating.** Professionals sometimes think
   they need courtroom-level proof before raising a concern. In practice, the
   duty is to escalate credible evidence of serious foreseeable harm early
   enough that mitigation is still possible.
3. **Confusing confidentiality with silence.** Confidentiality protects
   sensitive information; it does not require helping an organization continue a
   harmful practice unchallenged. The right response is usually controlled
   escalation, not immediate public disclosure and not passive compliance.
4. **Underestimating conflicts of interest.** Incentives shape judgment even
   when nobody is acting in obvious bad faith. Undisclosed conflicts make design
   reviews look objective while quietly biasing the outcome.
5. **Assuming hierarchy transfers responsibility.** An employer can order work,
   but it cannot absorb the entire ethical burden of carrying it out. When harm
   is foreseeable, participation itself becomes morally relevant.

## 6. Practical Checklist

- [ ] Map the decision or incident to specific ACM or IEEE principles before
      relying on general language about values.
- [ ] Record who owns the decision, who can stop deployment, and which internal
      channels exist for escalation.
- [ ] Disclose any financial, organizational, or incentive conflicts that could
      bias the review.
- [ ] Preserve contemporaneous documentation of the concern, including evidence,
      dates, and who was informed.
- [ ] Escalate internally before going external unless the internal path is
      clearly compromised or delay would create serious additional harm.
- [ ] When whistleblowing risk is real, seek protected legal or professional
      advice before disclosure instead of improvising.
- [ ] Distinguish disagreement about strategy from evidence of serious harm; not
      every product dispute is a whistleblowing case.

## 7. References

- Kant, Immanuel. 1785. *Groundwork of the Metaphysics of Morals*. Various scholarly editions.
- Johnson, Deborah G. 2009. *Computer Ethics* (4th ed.). Pearson.
- Vallor, Shannon. 2016. *Technology and the Virtues*. Oxford University Press. <https://doi.org/10.1093/acprof:oso/9780190498511.001.0001>
- ACM. 2018. ACM Code of Ethics and Professional Conduct. <https://www.acm.org/code-of-ethics>
- IEEE. 2020. IEEE Code of Ethics. <https://www.ieee.org/about/corporate/governance/p7-8.html>
- Mesmer-Magnus, Jessica R., and Chockalingam Viswesvaran. 2005. Whistleblowing in Organizations: An Examination of Correlates of Whistleblowing Intentions, Actions, and Retaliation. *Journal of Business Ethics* 62(3): 277-297. <https://doi.org/10.1007/s10551-005-0849-1>
- U.S. Senate Committee on Commerce, Science, and Transportation. October 5, 2021. *Protecting Kids Online: Testimony from a Facebook Whistleblower*. <https://www.commerce.senate.gov/2021/10/protecting%20kids%20online%3A%20testimony%20from%20a%20facebook%20whistleblower>
- Ellsberg, Daniel. 2002. *Secrets: A Memoir of Vietnam and the Pentagon Papers*. Viking.
