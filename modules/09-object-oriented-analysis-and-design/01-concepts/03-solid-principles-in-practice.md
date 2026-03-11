# SOLID Principles in Practice

## Key Ideas

- SOLID is a set of design principles for managing change pressure in object-oriented systems rather than a checklist for maximizing abstraction.
- The principles are most useful when they are applied to a concrete source of volatility such as changing policies, multiple implementations, or substitutable behavior.
- Overapplying SOLID can create needless indirection, so each principle should be justified by a real maintenance problem.
- Dependency inversion and interface segregation are especially valuable at integration boundaries where concrete dependencies change faster than domain rules.
- Liskov substitution is about preserving behavioral expectations, not merely matching method signatures.

## 1. Why SOLID Exists

SOLID is a compact summary of several recurring OO design lessons. The common thread is reducing the blast radius of change. A design that follows SOLID well tends to keep responsibilities narrow, extensions local, and dependencies pointed toward stable abstractions.

## 2. The Five Principles

### 2.1 Single Responsibility Principle

A class should have one primary reason to change. This does not mean one method. It means one cohesive responsibility.

### 2.2 Open/Closed Principle

Software should be open for extension but closed for modification. In practice, this means new behavior should often be added through composition, policies, or strategy objects instead of editing a central conditional every time.

### 2.3 Liskov Substitution Principle

If one type substitutes for another, existing client expectations should still hold. A subtype that throws on valid base-class operations violates the contract even if the signatures match.

### 2.4 Interface Segregation Principle

Clients should depend only on the operations they actually need. Large "god interfaces" create accidental coupling and force implementations to support irrelevant methods.

### 2.5 Dependency Inversion Principle

High-level policy should not depend directly on low-level detail. Both should depend on stable abstractions.

## 3. Worked Example: Replacing a Conditional Payment Design

Suppose a checkout service charges payments with a large branch:

```text
if payment_type == "card":
    use StripeClient
elif payment_type == "invoice":
    create AccountsReceivableEntry
elif payment_type == "wallet":
    call WalletGateway
```

Each new payment method requires editing the same service.

### 3.1 Design Pressure

- new payment methods are likely
- gateway details differ
- checkout policy should stay stable

### 3.2 Refactoring Toward SOLID

Introduce a shared abstraction:

```text
PaymentMethod
  + charge(order_id, amount)
```

Concrete implementations:

- `CardPaymentMethod`
- `InvoicePaymentMethod`
- `WalletPaymentMethod`

Then the checkout service depends on `PaymentMethod`, not on each gateway.

### 3.3 Outcome

- OCP improves because a new payment type can be added with a new implementation.
- DIP improves because checkout depends on an abstraction.
- ISP can also improve if each client depends only on the charging behavior it needs.

Verification: the checkout service remains unchanged when a new payment type is introduced, while the extension work is localized to a new `PaymentMethod` implementation.

## 4. When SOLID Helps and When It Hurts

SOLID helps when:

- requirements vary across implementations
- integrations are unstable
- policies should outlive infrastructure
- behavior must be extended repeatedly

SOLID hurts when:

- abstraction is added before a second use case exists
- interfaces duplicate one implementation exactly with no volatility
- inheritance is used where simple composition would be clearer

Good OOAD uses SOLID to reduce real change cost, not to satisfy style rules.

## 5. Behavioral Contracts Matter

LSP deserves extra care because it is often misunderstood. If a `ReadOnlyRepository` inherits from `Repository` but throws on `save`, the subtype is not truly substitutable. The problem is not syntax. The problem is broken client expectation.

That is why OO design should define contracts in behavioral terms:

- what inputs are valid
- what effects are guaranteed
- what invariants are preserved

## 6. Common Mistakes

1. **Acronym worship.** Applying SOLID mechanically without a change-pressure argument creates abstract but brittle designs; explain what change each abstraction is protecting against.
2. **Inheritance reflex.** Using subclassing to satisfy OCP often creates fragile hierarchies; prefer composition when behavior varies independently.
3. **Fake substitutability.** Reusing a base interface while changing behavioral guarantees breaks clients; define contracts around actual shared behavior.
4. **Oversized interfaces.** Packing unrelated methods into one contract forces clients to depend on too much; split interfaces by use case.
5. **Detail-driven policies.** Letting use-case code call concrete gateways, ORMs, or SDKs directly undermines DIP; depend on narrow abstractions instead.

## 7. Practical Checklist

- [ ] Identify which requirements are likely to change repeatedly.
- [ ] Use SRP to separate unrelated reasons to change.
- [ ] Apply OCP only where extension is more likely than replacement.
- [ ] Check that subtype behavior preserves client expectations, not just signatures.
- [ ] Keep interfaces small enough that each client needs most of their methods.
- [ ] Point orchestration code at abstractions instead of concrete infrastructure.

## 8. References

- Martin, Robert C. *Agile Software Development, Principles, Patterns, and Practices*. Prentice Hall, 2002.
- Martin, Robert C. *Clean Architecture*. Prentice Hall, 2017.
- Liskov, Barbara H., and Jeannette M. Wing. "A Behavioral Notion of Subtyping." *ACM Transactions on Programming Languages and Systems*, 1994. <https://dl.acm.org/doi/10.1145/197320.197383>
- Meyer, Bertrand. *Object-Oriented Software Construction* (2nd ed.). Prentice Hall, 1997.
- Fowler, Martin. *Refactoring* (2nd ed.). Addison-Wesley, 2018.
- Bloch, Joshua. *Effective Java* (3rd ed.). Addison-Wesley, 2018.
- Martin, Robert C. "The Dependency Inversion Principle." <https://web.archive.org/web/20240201000000*/http://www.objectmentor.com/resources/articles/dip.pdf>
