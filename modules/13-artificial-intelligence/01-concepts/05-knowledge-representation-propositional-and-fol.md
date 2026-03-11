# Knowledge Representation: Propositional and FOL

## Key Ideas

- Knowledge representation encodes facts, relations, and rules so an agent can reason about them symbolically.
- Propositional logic represents boolean facts, while first-order logic adds predicates, variables, and quantifiers for richer structure.
- Expressiveness matters because a representation that cannot state the needed distinctions forces brittle workarounds elsewhere in the system.
- Inference quality depends on both the logical formalism and the clarity and consistency of the encoded knowledge base.
- Symbolic representations are most useful when explainability, explicit rules, and compositional structure matter more than purely statistical pattern matching.

## 1. Why Knowledge Representation Matters

Reasoning systems need a language for expressing what is true, what follows from what, and what constraints the world obeys. Knowledge representation provides that language.

Without it, an agent may have data but no structured way to infer consequences such as:

- if all mammoths are extinct and Manny is a mammoth, then Manny is extinct
- if a room is occupied, it cannot be assigned to another meeting at the same time

## 2. Propositional vs First-Order Logic

### 2.1 Propositional Logic

Propositional logic uses atomic statements such as:

```text
rain
alarm_on
door_locked
```

It is simple and useful, but it cannot naturally express general rules over objects.

### 2.2 First-Order Logic

First-order logic adds:

- predicates
- constants
- variables
- quantifiers

This allows statements like:

```text
forall x, Mammoth(x) -> Extinct(x)
```

which is much more expressive than enumerating every mammoth separately.

## 3. Inference Basics

Once facts and rules are encoded, the agent can perform inference using methods such as:

- forward chaining
- backward chaining
- resolution

The right method depends on the query style and the form of the knowledge base.

## 4. Worked Example: Simple First-Order Inference

Knowledge base:

```text
forall x, Student(x) -> EligibleForLibrary(x)
Student(Ada)
```

### 4.1 Instantiate the Rule

Substitute `Ada` for `x`:

```text
Student(Ada) -> EligibleForLibrary(Ada)
```

### 4.2 Apply the Known Fact

Since `Student(Ada)` is true, infer:

```text
EligibleForLibrary(Ada)
```

The query succeeds.

Verification: the general rule plus the fact about Ada entail that Ada is eligible for the library.

## 5. Representation Tradeoffs

The most important questions are:

- what distinctions must the system express?
- what kinds of inference must it support?
- how large and dynamic is the knowledge base?

A richer representation is not always better. More expressiveness often means harder inference. The right representation is the smallest one that states the needed structure clearly.

## 6. Common Mistakes

1. **Representation mismatch.** Using propositional logic for problems that require relations and quantification creates awkward brittle encodings; switch to a richer formalism when the domain demands it.
2. **Symbol inconsistency.** Changing predicate meaning or naming conventions across the knowledge base breaks inference clarity; keep a stable ontology.
3. **Implicit assumptions.** Leaving key constraints unstated causes incorrect conclusions; encode important domain rules explicitly.
4. **Inference overreach.** Choosing a very expressive formalism without considering inference cost can make the system impractical; balance expressiveness with tractability.
5. **Grounding errors.** Instantiating variables incorrectly or ambiguously leads to invalid reasoning; test entailments on small examples first.

## 7. Practical Checklist

- [ ] Choose the simplest representation that can express the needed rules.
- [ ] Define predicates and symbols consistently before expanding the knowledge base.
- [ ] Test the representation on a few known entailments and non-entailments.
- [ ] Keep important domain constraints explicit instead of relying on human intuition.
- [ ] Match the inference method to the query style and scale of the problem.
- [ ] Document ontology assumptions so future updates stay consistent.

## 8. References

- Russell, Stuart, and Peter Norvig. *Artificial Intelligence: A Modern Approach* (4th ed.). Pearson, 2020.
- Genesereth, Michael R., and Nils J. Nilsson. *Logical Foundations of Artificial Intelligence*. Morgan Kaufmann, 1987.
- Brachman, Ronald J., and Hector J. Levesque. *Knowledge Representation and Reasoning*. Morgan Kaufmann, 2004.
- Poole, David, and Alan Mackworth. *Artificial Intelligence: Foundations of Computational Agents* (2nd ed.). Cambridge University Press, 2017. <https://artint.info/2e/html/ArtInt2e.html>
- Robinson, J. A. "A Machine-Oriented Logic Based on the Resolution Principle." 1965. <https://dl.acm.org/doi/10.1145/321250.321253>
- Berkeley AIMA knowledge representation materials. <https://aima.cs.berkeley.edu/>
- Davis, Ernest, and Gary Marcus. "Commonsense Reasoning and Commonsense Knowledge in Artificial Intelligence." 2015. <https://cacm.acm.org/research/commonsense-reasoning-and-commonsense-knowledge-in-artificial-intelligence/>
