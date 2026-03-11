# Refactoring Techniques and Smells

## Key Ideas

- Refactoring improves internal design without changing externally observable behavior.
- Code smells are warning signals about change cost and design drift, not automatic proof that a rewrite is necessary.
- Small, behavior-preserving refactors are safer and more informative than broad rewrites because each step exposes whether the design is actually improving.
- Tests, characterization examples, and clear invariants are the safety net that makes refactoring reliable.
- Refactoring is most effective when it targets a specific design pressure such as duplication, oversized classes, or hidden dependencies.

## 1. Why Refactoring Matters

OO designs decay over time because requirements change unevenly. New responsibilities accumulate in the easiest existing location, conditionals multiply, and the original boundaries blur. Refactoring is the disciplined process for restoring structure before the system becomes too expensive to change.

The key constraint is behavioral stability. Refactoring is not feature work. It is design improvement under a fixed external contract.

## 2. Common Smells in OO Systems

### 2.1 Large Class

A class that carries many fields, many reasons to change, or many unrelated methods often needs decomposition.

### 2.2 Long Method

Long methods often hide implicit concepts that deserve names and boundaries.

### 2.3 Divergent Change

If one class changes for many unrelated features, cohesion is weak.

### 2.4 Shotgun Surgery

If one requirement forces many small edits across the codebase, responsibilities are scattered.

### 2.5 Feature Envy

If a method manipulates another object's data more than its own, the behavior may belong elsewhere.

## 3. Worked Example: Extracting Policy from a Large Method

Assume `InvoiceService.finalize_invoice()` currently:

- calculates tax
- applies discounts
- validates payment terms
- formats customer messages

### 3.1 Smell Diagnosis

This method mixes pricing policy, credit policy, and presentation text. That is both long-method and divergent-change pressure.

### 3.2 Refactoring Steps

1. Add characterization tests for representative invoice cases.
2. Extract tax logic into `TaxPolicy`.
3. Extract discount logic into `DiscountPolicy`.
4. Move message formatting into a presenter or formatter object.

### 3.3 Concrete Trace

Original invoice:

```text
subtotal = 200
tax_rate = 0.08
discount = 20
```

Result before refactoring:

```text
total = 200 - 20 + 16 = 196
```

After extracting policies, the same inputs still produce:

```text
DiscountPolicy.apply(200) = 180
TaxPolicy.apply(180, 0.08) = 14.4
final total = 194.4
```

This reveals a useful issue: the original ordering of tax and discount was ambiguous. The refactor exposed a business rule that needed clarification.

Verification: the refactor succeeded structurally because pricing responsibilities moved into focused policy objects, and it also surfaced a hidden domain rule that needed an explicit decision.

## 4. Safe Refactoring Workflow

Refactoring is safest when done in tight loops:

1. identify the smell
2. define the behavior that must remain stable
3. add tests or characterization examples
4. make one small change
5. rerun checks

This process lowers risk and makes design progress measurable.

## 5. Refactoring vs Rewriting

Rewrites are tempting when the current design feels messy, but they discard behavioral knowledge encoded in the existing system. Refactoring keeps that knowledge in place while improving structure incrementally.

A rewrite is justified only when:

- the external contract is changing radically
- the current design blocks even basic incremental change
- migration risk has been planned explicitly

## 6. Common Mistakes

1. **Behavior-change mixing.** Combining refactors with feature changes hides regressions; separate structural cleanup from new behavior whenever possible.
2. **No safety net.** Changing design without tests or characterization cases turns refactoring into guesswork; capture current behavior first.
3. **Smell absolutism.** Treating every smell as a mandatory fix wastes effort; prioritize smells that are increasing present change cost.
4. **Big-bang cleanup.** Large reorganizations create review and rollback risk; prefer small reversible steps with frequent verification.
5. **Symptom fixing only.** Renaming classes without redistributing responsibilities leaves the real design problem intact; move behavior to the correct owner.

## 7. Practical Checklist

- [ ] Name the smell and the specific maintenance problem it causes.
- [ ] Freeze the current behavior with tests or examples before changing structure.
- [ ] Make one focused refactor at a time.
- [ ] Re-run tests after every small step.
- [ ] Stop when the design pressure is relieved instead of polishing endlessly.
- [ ] Separate domain decisions discovered during refactoring into explicit business rules.

## 8. References

- Fowler, Martin. *Refactoring* (2nd ed.). Addison-Wesley, 2018.
- Kerievsky, Joshua. *Refactoring to Patterns*. Addison-Wesley, 2004.
- Feathers, Michael. *Working Effectively with Legacy Code*. Prentice Hall, 2004.
- Opdyke, William F. *Refactoring Object-Oriented Frameworks*. PhD thesis, University of Illinois, 1992.
- Martin, Robert C. *Clean Code*. Prentice Hall, 2008.
- Refactoring.Guru. "Code Smells." <https://refactoring.guru/refactoring/smells>
- Fowler, Martin. "Code Smell." <https://martinfowler.com/bliki/CodeSmell.html>
