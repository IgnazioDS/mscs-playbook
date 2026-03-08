# Surveillance, Civil Liberties, and Power

## Key Ideas

- Surveillance is not just data collection; it is a power relation in which one party gains visibility into another without reciprocal exposure.
- The ethical harm of surveillance includes chilling effects, unequal power, discriminatory error, and the normalization of monitoring as a condition of ordinary life.
- Contextual integrity explains why many surveillance systems feel wrong even when the observed acts were "public": the data is being repurposed across contexts and at a scale humans did not choose.
- Facial recognition and predictive policing concentrate risk on already over-policed communities, so accuracy improvements alone do not resolve the legitimacy problem.
- Engineers cannot hide behind the "neutral tool" defense when they knowingly build systems whose primary function is coercive monitoring.

## 1. What It Is

Surveillance systems collect, aggregate, infer, and act on information about
people in ways that expand the power of states, firms, or peers over those being
observed. In computing, surveillance becomes especially potent when automation
turns constant observation into searchable history, behavioral prediction, and
real-time intervention.

### 1.1 A taxonomy of surveillance

| Type | Typical actor | Typical goal |
| --- | --- | --- |
| State surveillance | police, intelligence, border agencies | policing, control, intelligence, deterrence |
| Corporate surveillance | platforms, advertisers, brokers, employers | monetization, optimization, labor management |
| Peer surveillance | individuals, communities, harassment networks | reputation control, social pressure, abuse |
| Counter-surveillance | journalists, activists, watchdogs | accountability against concentrated power |

### 1.2 Why surveillance is ethically distinctive

Surveillance changes behavior even when no sanction follows. People adapt to
being observed. They search less, associate less freely, and self-censor more.
That is why the harm is broader than any single arrest, ad, or recommendation.

## 2. Chilling Effects, Context, and Power

### 2.1 Chilling effects

Penney's study of Wikipedia traffic after the Snowden revelations found a
decline in visits to privacy-sensitive articles, suggesting that surveillance
can suppress lawful inquiry. This is a consequentialist harm with constitutional
and democratic significance.

### 2.2 Contextual integrity

Contextual integrity is especially useful here. A person walking on a street,
ringing a doorbell, or appearing in a neighborhood camera feed is not thereby
granting permission for persistent identification, fusion across databases, or
sharing with law enforcement without limit. Surveillance usually violates the
norms of the original context by changing recipient, purpose, and persistence
all at once.

### 2.3 Power asymmetry

Surveillance is rarely evenly distributed. The powerful monitor the less
powerful far more often than the reverse. That asymmetry matters because the
same technical system that feels convenient in a low-power setting can become
coercive when attached to policing, immigration, employment, or welfare
administration.

## 3. Facial Recognition, Predictive Systems, and Civil Liberties

### 3.1 Facial recognition in law enforcement

NIST's FRVT work shows demographic performance differentials in face-recognition
systems. That does not mean every deployment is equally error-prone, but it does
mean the burden of proof is on deployers, especially in policing contexts where
one false match can cascade into wrongful detention or arrest.

Public reporting has now documented multiple U.S. wrongful arrest cases in which
facial recognition contributed to the initial misidentification. Accuracy claims
therefore cannot remain abstract.

### 3.2 Predictive policing and social scoring

Predictive systems often learn from historical enforcement data, which means
they can reproduce earlier policing patterns while appearing objective. Social
credit and behavioral-risk systems raise the same problem at a wider scale:
they convert observation into administrative leverage.

The ethical issue is not only bad prediction. It is the legitimacy of the
institutional use of prediction in the first place.

## 4. Case Study

**Case: PRISM and Section 702 surveillance**

**Descriptive register. Situation:**  
The PRISM disclosures made public that U.S. intelligence collection under
Section 702 relied on large-scale acquisition of communications data from major
internet providers under legal authorities largely invisible to ordinary users.
Subsequent PCLOB reporting has provided detailed public analysis of the program's
structure, safeguards, and civil-liberties implications. The technical lesson is
that infrastructure built for communication can be repurposed into infrastructure
for state visibility.

**Analytical register. Ethical analysis:**  
From a consequentialist perspective, the strongest argument for such programs is
that intelligence collection may prevent serious harms, including terrorism and
foreign threats. But those benefits must be weighed against chilling effects,
mission creep, and the long-term democratic cost of normalized bulk access.  
From a deontological perspective, people are entitled to more than secret
internal assurances that rights will be respected. Systems of hidden monitoring
strain duties of transparency, autonomy, and respect for persons.  
From a contractualist perspective, it is difficult to argue that the public has
meaningfully accepted a surveillance regime whose technical operation and scope
were largely opaque until disclosed.

**Analytical register. Competing considerations:**  
The strongest defense of intelligence surveillance is that democratic states
have genuine duties to protect the public from severe threats and cannot disclose
every operational detail. The strongest criticism is that secrecy plus scale
removes the ordinary checks that make coercive power answerable to those who
live under it.

**Normative register. What a responsible professional would do:**  
Design surveillance-related systems under a presumption of minimization,
necessity, auditing, and independent oversight; resist building "collect first,
govern later" architectures; and treat civil-liberties impact as a primary
design input rather than a public-relations afterthought.

## 5. Common Mistakes

1. **Treating surveillance as harmless if the data was visible in public.**
   Persistent identification, cross-database linking, and long-term retention
   change the meaning of "public." Scale and searchability are part of the harm.
2. **Reducing the debate to accuracy.** A perfectly accurate surveillance system
   can still be unjustified if the monitoring itself is illegitimate. Accuracy
   is relevant, but it is not the whole argument.
3. **Assuming only bad actors are chilled.** Empirical work shows lawful users
   also self-censor under surveillance. That makes surveillance a civil-liberties
   issue, not merely a crime-control tool.
4. **Treating engineers as neutral implementers.** Building indexing, matching,
   retention, or sharing systems for surveillance is not morally empty just
   because another actor presses the final button.
5. **Ignoring who bears the burden.** Surveillance harms are usually distributed
   unevenly across race, class, citizenship, and political vulnerability.
   Analysis that ignores power will systematically misread the stakes.

## 6. Practical Checklist

- [ ] Identify who is being surveilled, who benefits, and who has the power to
      challenge misuse or error.
- [ ] Test whether the information flow violates the norms of the context in
      which the data was originally generated.
- [ ] Evaluate chilling effects, not just direct enforcement outcomes.
- [ ] Require documented necessity, minimization, retention limits, and external
      oversight before building surveillance features.
- [ ] Do not rely on facial recognition or predictive systems for enforcement
      decisions without independent evidence beyond the automated output.
- [ ] Record demographic error rates, recourse mechanisms, and auditability for
      any identification or risk-scoring system.
- [ ] Escalate if the primary use case is coercive monitoring with weak public
      accountability or no meaningful appeal path.

## 7. References

- Rawls, John. 1971. *A Theory of Justice*. Harvard University Press.
- Nissenbaum, Helen. 2004. Privacy as Contextual Integrity. *Washington Law Review* 79(1): 119-157. <https://digitalcommons.law.uw.edu/wlr/vol79/iss1/10>
- Solove, Daniel J. 2007. "I've Got Nothing to Hide" and Other Misunderstandings of Privacy. *San Diego Law Review* 44: 745. <https://papers.ssrn.com/sol3/papers.cfm?abstract_id=998565>
- Penney, Jonathon W. 2016. Chilling Effects: Online Surveillance and Wikipedia Use. *Berkeley Technology Law Journal* 31(1). <https://doi.org/10.15779/Z38SS13>
- Garvie, Clare, Alvaro Bedoya, and Jonathan Frankle. 2016. *The Perpetual Line-Up: Unregulated Police Face Recognition in America*. Georgetown Law Center on Privacy and Technology. <https://www.perpetuallineup.org/>
- Grother, Patrick, Mei Ngan, and Kayee Hanaoka. 2019. *Face Recognition Vendor Test (FRVT) Part 3: Demographic Effects* (NIST IR 8280). <https://doi.org/10.6028/NIST.IR.8280>
- Privacy and Civil Liberties Oversight Board. September 28, 2023. *Report on the Surveillance Program Operated Pursuant to Section 702 of the Foreign Intelligence Surveillance Act*. <https://documents.pclob.gov/prod/Documents/OversightReport/8ca320e5-01d3-4d6a-8106-3384aad6ff31/2023%20PCLOB%20702%20Report%20-%20Nov%2017%202023%20-%201446.pdf>
- American Civil Liberties Union. 2020. Man Wrongfully Arrested Because Face Recognition Can't Tell Black People Apart. <https://www.aclu.org/press-releases/man-wrongfully-arrested-because-face-recognition-cant-tell-black-people-apart>
- ACM. 2018. ACM Code of Ethics and Professional Conduct. <https://www.acm.org/code-of-ethics>
