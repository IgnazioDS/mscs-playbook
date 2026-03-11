# Documentation, ADRs, and Design Docs

## Key Ideas

- Design documentation preserves architectural intent, tradeoffs, and decision context that code alone usually does not express clearly.
- A design document explains the problem, constraints, and proposed structure, while an architecture decision record captures one concrete decision and its consequences.
- Documentation is valuable only when it stays concise, specific, and close to the code it explains.
- ADRs reduce repeated debate by making alternatives and rationale explicit for future maintainers.
- OOAD documentation should focus on responsibilities, boundaries, and invariants rather than on reproducing implementation detail mechanically.

## 1. Why Design Documentation Matters

Object-oriented systems often fail not because the code is unreadable, but because the reasons behind the structure disappear. New engineers can see that a port exists or that a domain object has restricted mutation, yet they may not know why those choices were made.

Documentation helps preserve:

- problem framing
- chosen boundaries
- rejected alternatives
- operational consequences

Without that record, teams tend to repeat old debates or accidentally break intentional constraints during refactoring.

## 2. Design Docs vs ADRs

### 2.1 Design Document

A **design document** describes a larger proposed change or system shape. It often includes:

- background
- goals and non-goals
- current pain points
- proposed design
- alternatives considered
- migration and rollout notes

### 2.2 Architecture Decision Record

An **ADR** records one concrete architectural decision. A good ADR is short and usually contains:

- title
- status
- context
- decision
- consequences

## 3. Worked Example: Recording a Repository Abstraction Decision

Suppose a team is deciding whether the order application should depend directly on an ORM model or on a repository port.

### 3.1 Context

- the domain model has nontrivial invariants
- tests should run without a real database
- storage technology may change later

### 3.2 ADR Summary

```text
Title: Use a repository port for aggregate persistence
Status: Accepted
Context: Order workflows currently depend on ORM entities, making tests and domain boundaries harder to control.
Decision: The application core will depend on OrderRepositoryPort. Infrastructure adapters may use any storage mechanism.
Consequences: Domain tests become faster; adapters gain translation work; direct ORM convenience decreases.
```

### 3.3 Why This Helps

Future maintainers can see that the abstraction was chosen to protect domain boundaries and testing speed, not because the team wanted abstraction for its own sake.

Verification: the ADR captures context, decision, and consequences in a form that explains why the repository boundary exists and what tradeoff it introduced.

## 4. What Good Documentation Looks Like

Good design documentation is:

- short enough to read before coding
- specific to an actual decision
- updated when the design changes materially
- linked from the relevant code area

The purpose is to preserve design intent. Documentation that duplicates every class or method usually becomes stale faster than it creates value.

## 5. Documentation Workflow in Practice

For a significant OOAD change:

1. write a short design doc before implementation
2. record any important accepted decisions as ADRs
3. link the docs from the module or implementation README
4. revisit the docs when architecture changes materially

This workflow keeps the documentation proportional to the decision complexity.

## 6. Common Mistakes

1. **Novel-length docs.** Overly long design documents discourage reading and review; keep documents narrow and decision-centered.
2. **Decision-free summaries.** Documents that describe the code without stating tradeoffs or choices lose most of their value; record the actual decision and why it was made.
3. **Stale architecture notes.** Documentation that is not updated after major changes misleads maintainers; tie docs to the code area and review them during design changes.
4. **Hidden docs.** If ADRs live far from the implementation and are not linked, maintainers will miss them; keep discoverability part of the workflow.
5. **Template worship.** Filling every section of a generic template even when it adds no signal creates noise; adapt the structure to the importance of the decision.

## 7. Practical Checklist

- [ ] Write a design doc for changes that alter responsibilities, boundaries, or workflows materially.
- [ ] Record accepted architectural decisions in short ADRs with context and consequences.
- [ ] Link design docs and ADRs from the nearest relevant README or code area.
- [ ] Document the rejected alternatives when they affect future choices.
- [ ] Update documentation when the design changes in a way that invalidates the rationale.
- [ ] Keep diagrams and prose focused on the parts future maintainers actually need to understand.

## 8. References

- Nygard, Michael. "Documenting Architecture Decisions." <https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions>
- Fowler, Martin. "Architecture Decision Records." <https://martinfowler.com/articles/architectural-decision-records.html>
- Rozanski, Nick, and Eoin Woods. *Software Systems Architecture* (2nd ed.). Addison-Wesley, 2011.
- Bass, Len, Paul Clements, and Rick Kazman. *Software Architecture in Practice* (4th ed.). Addison-Wesley, 2021.
- Brown, Simon. *Software Architecture for Developers*. Leanpub, 2022.
- Richards, Mark, and Neal Ford. *Fundamentals of Software Architecture*. O'Reilly, 2020.
- C4 Model. "Documentation." <https://c4model.com/>
