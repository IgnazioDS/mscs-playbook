# Design Patterns: When and Why

## Key Ideas

- Design patterns are named solutions to recurring design pressures, not recipes to apply automatically.
- A pattern is useful only when it addresses a specific force such as variable construction, optional behavior, or interchangeable algorithms.
- Patterns improve communication because they give teams a shared vocabulary for structure and tradeoffs.
- Composition-based patterns often age better than inheritance-heavy ones because they localize variability more precisely.
- The cost of a pattern is extra indirection, so the design should justify that cost with expected extension or simplification.

## 1. Why Patterns Matter

Patterns compress experience. They let engineers say "strategy" or "adapter" and immediately communicate the role of a set of objects, the kind of variability involved, and the likely tradeoffs.

That said, patterns are not goals. The goal is a clear design. If a direct function or a small class solves the problem cleanly, adding a pattern can make the code worse.

## 2. Common Pattern Forces

Patterns usually respond to one of three forces:

- **creation pressure**, where object construction varies
- **behavioral pressure**, where algorithms or workflows vary
- **structural pressure**, where incompatible interfaces or optional layers must fit together

Examples:

- Strategy handles interchangeable behavior.
- Factory Method or Abstract Factory handles variable construction.
- Adapter handles incompatible interfaces.
- Decorator handles optional behavior layering.

## 3. Worked Example: Choosing Strategy Instead of Conditionals

A pricing system supports three discount modes:

- no discount
- percentage discount
- loyalty discount

An initial implementation might use:

```text
if customer_tier == "none":
    total = subtotal
elif customer_tier == "promo":
    total = subtotal * 0.9
elif customer_tier == "loyalty":
    total = subtotal - 15
```

### 3.1 When the Design Starts to Strain

The conditional becomes harder to maintain when:

- discount rules change independently
- more discount types are added
- tests need to isolate each policy

### 3.2 Pattern-Based Design

Use a strategy interface:

```text
DiscountPolicy
  + apply(subtotal)
```

Concrete strategies:

- `NoDiscountPolicy`
- `PercentageDiscountPolicy`
- `LoyaltyDiscountPolicy`

For `subtotal = 120`:

```text
NoDiscountPolicy -> 120
PercentageDiscountPolicy(10%) -> 108
LoyaltyDiscountPolicy(15) -> 105
```

### 3.3 Why Strategy Fits

The variability is behavioral, and each rule can evolve separately. Strategy makes that variation explicit without making the rest of the checkout code care about discount details.

Verification: Strategy is justified here because discount behavior varies independently and the caller can depend on one stable `apply(subtotal)` contract.

## 4. Pattern Selection Heuristics

Choose a pattern only when it simplifies one of these:

- adding a new variant
- testing behavior in isolation
- integrating incompatible components
- layering optional behavior
- separating stable policy from changing detail

If the pattern mainly adds indirection and no likely extension point exists, keep the simpler design.

## 5. Patterns and Domain Language

The best pattern names support, rather than replace, domain language. For example, `DiscountPolicy` is better than a generic `StrategyContext` because it communicates both the pattern role and the business meaning.

This is one reason patterns should often be embedded in the domain rather than exposed as textbook structures.

## 6. Common Mistakes

1. **Pattern-first design.** Starting from a catalog entry instead of a concrete design pressure leads to ornamental abstractions; identify the force before naming the solution.
2. **Vocabulary inflation.** Using pattern names as status markers obscures simpler explanations; use pattern terminology only when it clarifies the design.
3. **Inheritance overuse.** Reaching for subclass hierarchies when composition would localize change better creates rigid code; prefer object composition for independent variation.
4. **Premature factories.** Abstracting construction before multiple creation paths exist adds ceremony with little payoff; introduce factories when construction complexity or variability is real.
5. **Hidden simplicity.** Wrapping trivial logic in several collaborating classes makes maintenance harder; remove the pattern if it no longer earns its cost.

## 7. Practical Checklist

- [ ] State the specific design pressure before choosing a pattern.
- [ ] Prefer domain-specific names for pattern participants.
- [ ] Use composition when behavior varies independently.
- [ ] Confirm that the pattern improves testing or extension, not just terminology.
- [ ] Remove or simplify patterns that no longer solve an active problem.
- [ ] Keep the public API smaller than the internal pattern structure.

## 8. References

- Gamma, Erich, Richard Helm, Ralph Johnson, and John Vlissides. *Design Patterns*. Addison-Wesley, 1994.
- Freeman, Eric, and Elisabeth Robson. *Head First Design Patterns* (2nd ed.). O'Reilly, 2020.
- Fowler, Martin. *Patterns of Enterprise Application Architecture*. Addison-Wesley, 2002.
- Buschmann, Frank, et al. *Pattern-Oriented Software Architecture, Volume 1*. Wiley, 1996.
- Kerievsky, Joshua. *Refactoring to Patterns*. Addison-Wesley, 2004.
- Refactoring.Guru. "Design Patterns." <https://refactoring.guru/design-patterns>
- Martin, Robert C. *Agile Software Development, Principles, Patterns, and Practices*. Prentice Hall, 2002.
