# Intellectual Property, Licensing, and Open Source

## Key Ideas

- Copyright in software protects expression rather than abstract ideas, which is why implementation details, source text, and creative structure matter more than general functionality alone.
- Licenses are not administrative boilerplate: they encode real moral and strategic commitments about sharing, reciprocity, control, and downstream freedom.
- The free-software and open-source traditions overlap in practice but differ in moral emphasis: one foregrounds user freedom, the other foregrounds collaborative development and adoption.
- License compatibility is an ethical as well as legal issue because incompatible choices can block reuse, fragment commons, and mislead downstream developers.
- Using open-source software creates obligations beyond bare compliance, especially when organizations benefit from critical community-maintained infrastructure without helping sustain it.

## 1. What It Is

Intellectual-property ethics in software concerns how code, models, training
data, and shared infrastructure may be created, reused, licensed, and governed.
The topic matters because software development depends heavily on reuse, and the
terms of reuse shape who benefits, who contributes back, and who bears the cost
of maintenance.

### 1.1 Copyright in software

Copyright generally protects the expression of software, including source code
text, object code, and some non-literal structure. It does not protect ideas,
algorithms in the abstract, or general functionality as such.

This idea-expression distinction matters because engineers often confuse
"inspired by," "compatible with," and "copied from." Those are not the same
thing legally or ethically.

## 2. License Families and Their Ethical Logic

| Family | Examples | Main permission pattern | Ethical philosophy |
| --- | --- | --- | --- |
| Proprietary | Commercial closed-source licenses | Use only under contract and often with redistribution limits | Control, monetization, and centralized stewardship |
| Permissive | MIT, BSD, Apache 2.0 | Broad reuse with limited conditions | Maximize adoption and interoperability |
| Weak copyleft | LGPL, MPL | Reciprocity on modified covered components, not always the full combined work | Preserve some sharing while enabling broader integration |
| Strong copyleft | GPL, AGPL | Derivative or networked use can trigger source-sharing obligations | Protect user freedom and prevent one-way appropriation |

### 2.1 Free software versus open source

Richard Stallman and the free-software movement argue primarily from freedom:
users should be able to run, study, modify, and share software. Eric Raymond
and the open-source movement emphasize development quality, practical adoption,
and collaborative efficiency.

The positions overlap on many licenses and communities. They differ on the
question "why does sharing matter?" Free software answers morally. Open source
more often answers pragmatically.

### 2.2 Why the distinction still matters

When the goal is moral argument about user autonomy or enclosure of the digital
commons, the free-software framing is often sharper. When the goal is industry
coordination and ecosystem uptake, the open-source framing is often more
persuasive to organizations that would resist explicitly moral language.

## 3. Compatibility, Reuse, and Maintenance

### 3.1 License compatibility

Compatibility asks whether code under two licenses can be combined and
redistributed under terms that satisfy both sets of obligations. This is partly
a legal question and partly a design question because architecture determines
where obligations attach.

| Combination | Usual result | Why it matters |
| --- | --- | --- |
| MIT or BSD into Apache 2.0 projects | Usually compatible | Permissive terms allow broad downstream reuse |
| MIT or BSD into GPL projects | Usually compatible | Permissive licenses can often flow into stronger reciprocity |
| Apache 2.0 into GPLv2-only projects | Commonly incompatible | Patent and notice terms do not line up cleanly |
| AGPL components in network services | High obligation risk for proprietary hosts | Network use can trigger source-sharing duties |

### 3.2 Obligations when using open source

At a minimum, organizations must preserve attribution, comply with notice
requirements, and honor the conditions of the chosen license. Ethically, that
is only the floor. Heavy reliance on underfunded infrastructure while treating
maintainers as free labor creates systemic fragility and unfair burden-sharing.

## 4. AI Training and Copyright

### 4.1 Descriptive register

Large AI systems are often trained on copyrighted material. As of March 8, 2026,
the legal treatment of training on copyrighted works remains unsettled across
multiple jurisdictions and cases. The U.S. Copyright Office's May 9, 2025
report on generative AI training frames the major arguments but does not resolve
the litigation.

### 4.2 Analytical register

Ethically, the core distinction is between two claims:

- training on works is transformative statistical learning that may not replace
  the market for the originals, and
- training on works appropriates value from creators whose labor made the model
  possible without consent, compensation, or governance input.

The disagreement is not purely legal. It turns on autonomy, fair terms of
cooperation, and how a digital commons should be sustained.

## 5. Case Study

**Case: Illustrative scenario - AGPL service embedded in a proprietary SaaS product**

**Descriptive register. Situation:**  
A startup integrates an AGPL-licensed search component into its hosted platform
because it solves a difficult retrieval problem quickly. The component is
modified internally and exposed to customers only over the network, so product
leadership assumes no source-sharing obligation exists because the software is
never distributed as a desktop product. The legal team is consulted late, after
the architecture is already built around the component.

**Analytical register. Ethical analysis:**  
From a deontological perspective, continuing with the integration while relying
on a knowingly implausible reading of the license treats the upstream community
as a means rather than a party to fair terms. The AGPL's reciprocity condition
is part of the bargain, not an optional nuisance.  
From a consequentialist perspective, attempting to evade the license may save
short-term engineering time but creates later compliance, reputational, and
community trust costs. It also reinforces a pattern in which companies extract
from shared infrastructure without sustaining it.  
From a contractualist perspective, the startup is benefiting from a commons
while refusing terms that many contributors regard as necessary to keep the
commons from being enclosed.

**Analytical register. Competing considerations:**  
The strongest argument for the startup is that strong copyleft can make adoption
harder and may discourage organizations from using otherwise valuable software.
The strongest argument for compliance or replacement is that reciprocity is the
price of entry for that particular commons, and it is not ethically defensible
to accept the benefit while denying the condition.

**Normative register. What a responsible professional would do:**  
Stop treating license review as cleanup, decide early whether the organization
is willing to honor strong-copyleft obligations, and either comply fully or
replace the dependency before the product architecture depends on noncompliance.

## 6. Common Mistakes

1. **Thinking open source means no obligations.** Open source means licensed
   reuse, not unconditioned appropriation. Attribution, notice, reciprocity, and
   patent terms can all matter.
2. **Confusing popularity with compatibility.** A dependency can be widely used
   and still be a poor fit for your license strategy. Engineers should not wait
   for legal review to notice obvious incompatibilities.
3. **Reducing the free-software versus open-source debate to branding.** The
   distinction reflects different moral claims about freedom, community, and
   commercialization. Ignoring that difference makes licensing choices look more
   neutral than they really are.
4. **Treating AI training as automatically covered by old intuitions.** Model
   training raises real questions about reproduction, extraction, substitution,
   and compensation that existing doctrine has not fully resolved. "The law
   isn't settled" is a reason for caution, not for ethical indifference.
5. **Ignoring sustainability because the package is free.** Critical
   infrastructure maintained by a few unpaid people is a systemic risk. Ethical
   reuse includes supporting the ecosystem you depend on.

## 7. Practical Checklist

- [ ] Identify the license of every substantial dependency before architecture
      choices make replacement expensive.
- [ ] Check compatibility between your outbound license model and the inbound
      obligations of each dependency.
- [ ] Preserve attribution, notices, and patent terms rather than treating them
      as packaging details.
- [ ] Decide explicitly whether your organization is willing to comply with
      copyleft obligations before adopting copyleft components.
- [ ] For model training, separate what is legally uncertain from what is
      ethically contested, and document the rationale for dataset inclusion.
- [ ] Contribute back through funding, maintenance, security reporting, or code
      when your organization depends materially on community infrastructure.
- [ ] Involve legal review early, but do not outsource the ethical analysis to
      counsel alone.

## 8. References

- Mill, John Stuart. 1863. *Utilitarianism*. <https://www.gutenberg.org/ebooks/11224>
- U.S. Copyright Office. 2021. *Copyright Registration of Computer Programs (Circular 61)*. <https://www.copyright.gov/circs/circ61.pdf>
- U.S. Copyright Office. May 9, 2025. *Copyright and Artificial Intelligence, Part 3: Generative AI Training*. <https://copyright.gov/ai/Copyright-and-Artificial-Intelligence-Part-3-Generative-AI-Training-Report-Pre-Publication-Version.pdf>
- Open Source Initiative. 2007. The Open Source Definition. <https://opensource.org/osd>
- GNU Project. 2007. GNU General Public License, Version 3. <https://www.gnu.org/licenses/gpl-3.0.en.html>
- Stallman, Richard. 2002. Why Open Source Misses the Point of Free Software. <https://www.gnu.org/philosophy/open-source-misses-the-point.en.html>
- Raymond, Eric S. 1999. *The Cathedral and the Bazaar*. O'Reilly Media.
- Decan, Alexandre, Tom Mens, and Philippe Grosjean. 2019. An Empirical Comparison of Dependency Network Evolution in Seven Software Packaging Ecosystems. *Empirical Software Engineering* 24: 381-416. <https://doi.org/10.1007/s10664-017-9589-y>
- ACM. 2018. ACM Code of Ethics and Professional Conduct. <https://www.acm.org/code-of-ethics>
