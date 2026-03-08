# Ethical Frameworks for Computing

## Key Ideas

- Ethical frameworks are lenses rather than algorithms: they organize what counts as a relevant reason, but they do not remove the need for judgment.
- Computing creates a distinctive ethical problem because small design choices can create invisible harms at scale, far from the engineers who made them.
- Descriptive facts, analytical reasoning, and normative conclusions must be separated explicitly; otherwise ethics writing collapses into advocacy or hand-waving.
- Consequentialism, deontology, virtue ethics, and contractualism illuminate different aspects of the same technical decision, and strong analysis usually needs more than one.
- Empirical evidence matters because it changes the inputs to ethical reasoning, but no dataset can by itself answer what engineers ought to do.

## 1. What It Is

Ethical reasoning in computing is the disciplined evaluation of design and
deployment choices that affect people, institutions, and public life. The goal
is not to turn philosophy into a checklist. The goal is to make technical
decisions answerable to defensible reasons.

### 1.1 The three registers

Ethics pages in this module use three registers. They should not be mixed
without warning.

| Register | Function | Typical markers |
| --- | --- | --- |
| Descriptive | States facts about systems, organizations, and outcomes | "The model was deployed...", "The ACM Code states..." |
| Analytical | Applies a framework to the facts and derives implications | "Under a consequentialist view...", "If Rawlsian fairness is used..." |
| Normative | States what ought to be done | "The team should...", "Deployment is not justified unless..." |

### 1.2 Why computing changes the ethical landscape

Computing systems differ from ordinary one-off decisions in four ways.

- **Scale**: one release can affect millions of people at once.
- **Opacity**: the people harmed by a system may not know a system acted on
  them, let alone why.
- **Pace**: deployment often outruns institutional review and legal response.
- **Distance**: the engineer who writes a component is rarely the person who
  sees the downstream harm.

These features make foreseeable-but-unintended harm a central ethical category
in computing.

## 2. The Four Core Frameworks

| Framework | Core principle | Strength | Limitation | Typical computing use |
| --- | --- | --- | --- | --- |
| Consequentialism | Choose the available action with the best overall outcome | Forces explicit accounting of harms and benefits | Aggregates welfare and can bury minority harms | Safety trade-offs, deployment risk, harm modeling |
| Deontology | Some actions are right or wrong regardless of outcomes | Protects autonomy, consent, and non-deception | Duties can conflict and remain underspecified | Privacy, disclosure duties, respect for users |
| Virtue ethics | Good action expresses good character and sound professional judgment | Highlights integrity, courage, honesty, and diligence | Gives weaker step-by-step action guidance | Professional conduct, escalation, culture |
| Contractualism / procedural justice | Rules are justified if affected parties could reasonably accept them under fair conditions | Centers legitimacy, participation, and fairness | Real institutions rarely match ideal bargaining conditions | Fairness, recourse, participatory governance |

### 2.1 Consequentialism

Consequentialism asks which available action minimizes harm or maximizes
well-being. In computing, this often looks like risk-benefit analysis:
expected model utility versus expected false positives, privacy loss, or
security exposure.

Its attraction is operational clarity. Its danger is that aggregate welfare can
look acceptable even when a system imposes concentrated harm on already
vulnerable groups.

### 2.2 Deontology

Deontological ethics begins from duties and constraints rather than totals.
Users must not be deceived, coerced, or treated merely as raw material for
optimization.

This framework is especially important for consent, privacy, and disclosure.
Even if a dark pattern increases adoption, the increase does not settle whether
the interface is permissible.

### 2.3 Virtue ethics

Virtue ethics asks what a practically wise and professionally excellent person
would do. It is useful when rules are incomplete and outcome estimates are
uncertain.

In engineering, virtue ethics emphasizes honesty about system limits, diligence
in evaluation, courage to raise concerns, and humility about uncertainty.

### 2.4 Contractualism and procedural justice

Contractualist reasoning asks whether those affected by a rule could reasonably
accept it under fair conditions. In computing, this often becomes a question
about fairness, representation, recourse, and whether affected communities had
meaningful participation.

This framework is strongest when systems distribute benefits and burdens
unevenly. It is weaker when the affected parties are diffuse, excluded, or
unable to bargain on anything like fair terms.

## 3. How to Apply a Framework

### 3.1 Descriptive register

Start with facts, not conclusions. Name the system, the stakeholders, the
decision point, and the observed or credible harms. If the facts are uncertain,
say so directly.

### 3.2 Analytical register

Apply a framework in four steps:

1. State the framework's core principle in one sentence.
2. Identify the case features that matter under that principle.
3. Derive what the framework implies.
4. State the framework's limitation in this case.

Weak analysis names a framework and restates the dilemma. Strong analysis makes
the framework do explanatory work.

### 3.3 Normative register

Normative claims should come only after the analysis. A conclusion such as
"the team should pause deployment" is rigorous only if it is either:

- supported by broad professional consensus, or
- derived from the earlier analytical steps.

### 3.4 Framework pluralism and moral uncertainty

Real decisions rarely line up cleanly. A model may increase aggregate welfare
while violating consent norms; a disclosure may satisfy duty but increase
short-term public risk. In these cases, practical heuristics matter:

- look for overlap between frameworks before focusing on conflict,
- prefer reversible actions over irreversible ones when uncertainty is high,
- increase participatory review as stakes increase,
- and document residual moral disagreement instead of hiding it.

## 4. Case Study

**Case: Loan approval model with systematically higher denial rates**

**Descriptive register. Situation:**  
A lender deploys a credit model that predicts default risk from repayment
history, income stability, and proxy features derived from address and device
usage. Internal review shows that applicants from one racial group are denied
at materially higher rates than otherwise similar applicants, and the product
team cannot explain whether the disparity reflects real risk, biased labels, or
proxy discrimination. The model is accurate enough on average that executives
want to continue deployment while the team studies the disparity.

**Analytical register. Ethical analysis:**  
Consequentialism asks whether the welfare gained from more accurate default
prediction outweighs the harms of wrongful denial, downstream exclusion from
credit, and feedback loops that make future borrowing harder. If the disparity
comes from biased historical labels, aggregate accuracy understates harm rather
than justifying the system.  
Deontology asks whether applicants are being treated as autonomous persons or
merely as instruments for portfolio optimization. If the model uses opaque
proxies that applicants cannot contest or understand, it risks violating duties
of non-deception and respect.  
Virtue ethics asks what a conscientious engineer or risk officer would do under
uncertainty. A professionally serious team would treat the unexplained disparity
as a warning sign, not as a minor dashboard anomaly.  
Contractualist reasoning asks whether affected groups could reasonably accept a
decision rule they had no role in shaping and no meaningful path to challenge.
If the people who bear the denials lack recourse, the procedure is difficult to
justify as fair even before the causal story is complete.

**Analytical register. Competing considerations:**  
The strongest argument for continued deployment is that lenders must manage
default risk, and removing a predictive model can also create unfairness if
human underwriters are less consistent and more biased. The strongest argument
for pausing is that unexplained disparate denial in a high-stakes domain is a
foreseeable harm, and the burden of proof should rest on those continuing the
system rather than those challenging it.

**Normative register. What a responsible professional would do:**  
Pause any automated denial path, retain manual review for borderline cases, and
run a targeted audit of labels, proxy features, and group-level error rates.
Document the uncertainty, involve legal and risk stakeholders without treating
their approval as ethical clearance, and require recourse before redeployment.

## 5. Common Mistakes

1. **Sliding from facts to conclusions.** Teams often move from "the model
   reduced loss by 4%" to "therefore it is justified" without showing why the
   measured gain outweighs the harms. This is the is-ought fallacy in
   operational dress. State the descriptive result first, then show the ethical
   bridge.
2. **Using one framework as a shield.** A team may rely on consequentialist
   utility while ignoring consent or fairness constraints that another
   framework makes visible. The consequence is not rigor but tunnel vision.
   Apply at least two frameworks whenever stakes are high.
3. **Treating uncertainty as ethical permission.** Lack of perfect evidence is
   often used as a reason to continue shipping. In high-stakes settings,
   uncertainty about harm usually strengthens the case for caution because the
   affected party, not the builder, bears the downside.
4. **Confusing professional codes with proof.** The ACM or IEEE codes are
   evidence of professional consensus, not magic moral trump cards. Citing a
   code without analysis reduces ethics to authority rather than reasoning.
5. **Ignoring scale and feedback loops.** A decision that looks minor at the
   level of one user can become a structural harm at production scale. Ethical
   analysis in computing must include downstream amplification, not just the
   local action.

## 6. Practical Checklist

- [ ] Separate descriptive facts, analytical reasoning, and normative
      recommendations in your design document or review memo.
- [ ] Identify all stakeholder groups, including people acted on by the system
      who are not direct users or customers.
- [ ] Apply at least two ethical frameworks and note where they agree and
      where they conflict.
- [ ] Distinguish demonstrated harms from speculative harms, and attach the
      empirical evidence that supports each claim.
- [ ] Prefer reversible deployment choices when the ethical uncertainty is
      high and the possible harm is hard to remediate.
- [ ] Record who made the decision, what evidence they used, what objections
      were raised, and why the final decision was considered defensible.

## 7. References

- Aristotle. c. 4th century BCE. *Nicomachean Ethics*. Various scholarly editions.
- Kant, Immanuel. 1785. *Groundwork of the Metaphysics of Morals*. Various scholarly editions.
- Mill, John Stuart. 1863. *Utilitarianism*. <https://www.gutenberg.org/ebooks/11224>
- Rawls, John. 1971. *A Theory of Justice*. Harvard University Press.
- Johnson, Deborah G. 2009. *Computer Ethics* (4th ed.). Pearson.
- Floridi, Luciano, and Josh Cowls. 2019. A Unified Framework of Five Principles for AI in Society. *Harvard Data Science Review* 1(1). <https://doi.org/10.1162/99608f92.8cd550d1>
- Buolamwini, Joy, and Timnit Gebru. 2018. Gender Shades: Intersectional Accuracy Disparities in Commercial Gender Classification. *FAccT 2018*. <https://doi.org/10.1145/3287560.3287596>
- ACM. 2018. ACM Code of Ethics and Professional Conduct. <https://www.acm.org/code-of-ethics>
- IEEE. 2020. IEEE Code of Ethics. <https://www.ieee.org/about/corporate/governance/p7-8.html>
