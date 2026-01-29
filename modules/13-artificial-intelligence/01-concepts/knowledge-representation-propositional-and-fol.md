# Knowledge Representation: Propositional and FOL

## Overview
Knowledge representation encodes facts and rules so agents can reason about the
world using logic.

## Why it matters
Logical representations enable explainable reasoning and structured inference.

## Key ideas
- Propositional logic uses boolean variables
- First-order logic (FOL) adds predicates and quantifiers
- Inference via resolution or forward/backward chaining
- Knowledge bases require consistency and updates

## Practical workflow
- Define symbols, predicates, and relations
- Encode facts and rules in a knowledge base
- Choose inference method based on query type
- Verify consistency after updates

## Failure modes
- Inconsistent or incomplete knowledge bases
- Exponential inference for large rule sets
- Ambiguous predicates and missing constraints
- Incorrect grounding of variables

## Checklist
- Validate with known entailments
- Keep symbol naming consistent
- Use incremental updates for scalability
- Track derivations for explainability

## References
- AIMA Chapter on Knowledge and Logic
- Resolution — https://en.wikipedia.org/wiki/Resolution_(logic)
