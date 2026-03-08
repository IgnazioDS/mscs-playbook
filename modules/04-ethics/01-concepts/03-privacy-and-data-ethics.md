# Privacy and Data Ethics

## Key Ideas

- Privacy is not the same as secrecy: it is the ability to control when, how, and in what context information about a person flows.
- Contextual integrity is the most useful default framework for computing ethics because many data harms come from moving information across contexts rather than from publishing secrets.
- Meaningful consent requires information, voluntariness, specificity, and revocability; most notice-and-click interfaces satisfy the legal form of consent more often than its ethical substance.
- Data minimization is both a moral principle and an engineering discipline: unused data is not a dormant asset but latent risk.
- Differential privacy offers a formal guarantee against some privacy harms, but it does not solve every problem created by surveillance, coercion, or inappropriate data collection.

## 1. What It Is

Privacy concerns the conditions under which information about a person may be
observed, inferred, stored, combined, and used. In computing, the central risk
is rarely a single spectacular leak. It is the routine construction of systems
that make people legible in ways they neither expected nor meaningfully chose.

### 1.1 Privacy is broader than secrecy

- **Secrecy** asks whether information is hidden.
- **Confidentiality** asks whether an entrusted party keeps it protected.
- **Privacy** asks whether the flow itself is appropriate.

Someone can lose privacy even when the underlying facts were never secret. A
public location trail, shopping history, or contact graph can become invasive
when aggregated or repurposed.

### 1.2 The three dimensions of privacy

- **Informational privacy**: who knows what about a person.
- **Physical privacy**: protection against bodily or spatial intrusion.
- **Decisional privacy**: freedom to make intimate or political choices without
  coercive observation.

Computing systems most directly threaten informational privacy, but the harm
often cascades into the other two.

## 2. Contextual Integrity

### 2.1 Descriptive register

Helen Nissenbaum's contextual integrity framework treats privacy as appropriate
information flow relative to social context. A flow is evaluated by asking:

- what information is involved,
- who is sending it,
- who is receiving it,
- and under what transmission principle.

### 2.2 Analytical register

Under contextual integrity, the ethical question is not simply "was the data
public?" It is "did this new use respect the norms of the context in which the
data was originally shared?" A patient's symptom search, a student's classroom
submission, and a friend's geotagged photo each belong to different normative
contexts.

This framework is powerful because many modern privacy failures are context
shifts: fitness data to insurers, classroom analytics to disciplinary review,
or social graph data to political targeting.

### 2.3 Limitation

Contextual integrity can describe why a flow feels wrong without always telling
you what to do when the context itself is unjust or when multiple contexts
collide. It still needs supplementation from autonomy, welfare, or justice
arguments.

## 3. Consent, Minimization, and Formal Privacy

### 3.1 Meaningful consent

Consent is ethically meaningful only when it is:

- informed,
- voluntary,
- specific to a purpose,
- and revocable.

Consent banners and dense privacy policies often fail these conditions.
Information overload, coercive defaults, and dark patterns create the appearance
of permission without the substance of autonomous authorization.

### 3.2 Data minimization

Data minimization means collecting only the data necessary for a specific,
stated purpose and keeping it no longer than justified. This is not merely a
storage optimization tactic. It limits downstream misuse, breach exposure, and
function creep.

Engineers operationalize minimization through narrower schemas, shorter
retention, tighter access control, and deletion that actually works.

### 3.3 The aggregation problem

Individually mundane attributes can become sensitive in combination. Research
on mobile traces and de-anonymization shows that a few spatiotemporal points or
joined datasets can re-identify people at high rates. The ethical lesson is
that "not sensitive by itself" is an unstable category.

### 3.4 Differential privacy

Differential privacy gives a formal guarantee that the output of a computation
changes only slightly when any one person's data is added or removed. Informal
statement:

```text
For neighboring datasets D and D', a mechanism M is epsilon-DP if
P(M(D) in S) <= exp(epsilon) * P(M(D') in S)
for every measurable output set S.
```

Lower `epsilon` means stronger privacy and usually lower utility. Differential
privacy is valuable because it converts a vague promise into a quantifiable
trade-off. It does not justify collecting data in the first place, and it does
not address every contextual misuse.

## 4. Case Study

**Case: Cambridge Analytica and Facebook data sharing**

**Descriptive register. Situation:**  
A quiz application on Facebook collected data from people who installed it and,
through the platform rules then in force, also gathered data about many of
their friends. That data was later used for political profiling and campaign
targeting associated with Cambridge Analytica. Millions of people were affected
even though many never interacted with the app directly and did not understand
that their data would move from social networking into political influence
operations.

**Analytical register. Ethical analysis:**  
Contextual integrity treats this as a paradigmatic context collapse: social
relationship data shared in one context was repurposed for political
microtargeting in another. Even if the platform terms technically permitted
parts of the flow, the informational norms of the original context were not
preserved.  
From a deontological perspective, meaningful consent was absent for many of the
affected users because they neither authorized nor understood the political use
of their data. Treating social interaction data as campaign fuel reduced users
to means.  
From a consequentialist perspective, the relevant harms were not limited to
individual embarrassment. The flow created manipulation risk, democratic harm,
and large-scale loss of trust in online platforms.

**Analytical register. Competing considerations:**  
The strongest argument for permissive data sharing is that innovation in social
platforms and advertising often depends on rich developer ecosystems and large
data flows. The strongest argument against that permissiveness is that users
cannot meaningfully protect themselves when context shifts are hidden and the
network effects of others' consent expose them anyway.

**Normative register. What a responsible professional would do:**  
Reject friend-of-friend collection for secondary use, require purpose-specific
access controls, make revocation operational rather than symbolic, and treat
political profiling as a high-risk use that demands separate review and tighter
default restrictions.

## 5. Law as Context, Not Closure

### 5.1 Descriptive register

GDPR and CCPA create legal duties around notice, access, deletion, purpose
limitation, and data rights. They matter because they define enforceable
baselines and shape organizational incentives.

### 5.2 Analytical register

Legal compliance does not settle the ethical question. A system can satisfy the
letter of disclosure requirements while still relying on manipulative consent
flows or excessive collection. Law is often reactive and jurisdiction-specific;
ethics must address emergent harms before the statute book catches up.

## 6. Common Mistakes

1. **Treating public data as ethically free data.** Information can be public
   and still context-bound. Scraping, joining, and inferencing can violate
   privacy even when no secret was exposed.
2. **Using consent as a universal solvent.** Consent gathered through dark
   patterns, fatigue, or asymmetric dependence is not ethically decisive. It
   may satisfy a form field while failing the autonomy test.
3. **Collecting first and justifying later.** Teams often warehouse data "in
   case it becomes useful." The result is function creep, larger breach
   surfaces, and uses never contemplated at collection time.
4. **Assuming de-identification ends the problem.** Re-identification research
   shows that joined datasets and sparse traces can pierce weak anonymization.
   Privacy review must consider linkage attacks, not just direct identifiers.
5. **Reducing privacy to compliance.** A compliant banner and retention policy
   do not prove the data flow is appropriate. Ask whether the use would remain
   acceptable if the affected person understood it clearly.

## 7. Practical Checklist

- [ ] Identify the original context in which each data type was collected and
      test whether the planned use preserves that context's norms.
- [ ] Verify whether consent is informed, voluntary, specific, and revocable;
      if any condition fails, do not rely on consent as the main justification.
- [ ] Minimize collection, retention, and access scope before discussing
      encryption or anonymization.
- [ ] Model aggregation risk by asking what sensitive attributes could be
      inferred when datasets are combined.
- [ ] Use formal privacy techniques such as differential privacy when the task
      is aggregate analysis, and document the utility-privacy trade-off.
- [ ] Separate legal review from ethical review and record where legal approval
      does not fully answer the ethical concern.
- [ ] Provide users with a real path to deletion, export, and purpose-bound
      control over their data.

## 8. References

- Kant, Immanuel. 1785. *Groundwork of the Metaphysics of Morals*. Various scholarly editions.
- Nissenbaum, Helen. 2004. Privacy as Contextual Integrity. *Washington Law Review* 79(1): 119-157. <https://digitalcommons.law.uw.edu/wlr/vol79/iss1/10>
- Nissenbaum, Helen. 2010. *Privacy in Context*. Stanford University Press.
- Solove, Daniel J. 2007. "I've Got Nothing to Hide" and Other Misunderstandings of Privacy. *San Diego Law Review* 44: 745. <https://papers.ssrn.com/sol3/papers.cfm?abstract_id=998565>
- Dwork, Cynthia. 2006. Differential Privacy. *ICALP 2006*. <https://doi.org/10.1007/11787006_1>
- de Montjoye, Yves-Alexandre, Cesar A. Hidalgo, Michel Verleysen, and Vincent D. Blondel. 2013. Unique in the Crowd: The Privacy Bounds of Human Mobility. *Scientific Reports* 3. <https://doi.org/10.1038/srep01376>
- Information Commissioner's Office. 2018. *Investigation into the Use of Data Analytics in Political Campaigns*. <https://cy.ico.org.uk/media2/migrated/2260271/investigation-into-the-use-of-data-analytics-in-political-campaigns-final-20181105.pdf>
- ACM. 2018. ACM Code of Ethics and Professional Conduct. <https://www.acm.org/code-of-ethics>
- European Union. 2016. Regulation (EU) 2016/679 (General Data Protection Regulation). <https://eur-lex.europa.eu/eli/reg/2016/679/oj/eng>
