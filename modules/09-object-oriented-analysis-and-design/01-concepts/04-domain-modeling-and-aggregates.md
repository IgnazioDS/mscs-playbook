# Domain Modeling and Aggregates

## Key Ideas

- Domain modeling represents business concepts as entities, value objects, policies, and events rather than as raw tables or transport payloads.
- An aggregate is a consistency boundary that defines which objects must be updated together to preserve invariants.
- Aggregate roots protect internal rules by controlling access to the state of the objects they own.
- Good aggregates are small enough to change safely and large enough to enforce one coherent set of invariants.
- Persistence concerns should support the model, not determine its boundaries.

## 1. Why Domain Modeling Comes Before Persistence

If a design starts from database tables, domain behavior often ends up scattered across services, repositories, and controllers. Domain modeling reverses that order. It starts from business meaning and asks what the system must always keep true.

For example, an order system may need to guarantee:

- an order cannot be paid before it is submitted
- the total must equal the sum of its lines
- a shipment cannot contain lines from another order

Those are domain rules. They should live in the model that owns the state.

## 2. Core Building Blocks

### 2.1 Entities

An **entity** has identity that persists over time, such as `Order` or `Customer`.

### 2.2 Value Objects

A **value object** is defined by its attributes rather than identity, such as `Money` or `Address`. Value objects are often immutable because replacement is safer than partial mutation.

### 2.3 Aggregates

An **aggregate** is a cluster of related objects that must remain consistent as a unit. The **aggregate root** is the only object external code should use to modify that cluster.

## 3. Choosing Aggregate Boundaries

Aggregate boundaries are driven by invariants and transaction needs.

Good questions:

- Which rules must hold immediately after one operation?
- Which objects must be updated together?
- Which changes can be coordinated asynchronously instead?

If two objects do not need immediate consistency, they usually do not belong in the same aggregate.

## 4. Worked Example: Order Aggregate

Suppose an order system has these rules:

- line quantity must be positive
- order total must equal the sum of line subtotals
- only submitted orders may be paid

### 4.1 Candidate Model

```text
Order (aggregate root)
  - order_id
  - status
  - lines
  + add_line(product_id, quantity, unit_price)
  + total()
  + submit()
  + mark_paid()

OrderLine
  - product_id
  - quantity
  - unit_price
```

### 4.2 Enforcing Invariants

`Order.add_line()` checks `quantity > 0`.

`Order.total()` computes:

```text
(2 * 15) + (1 * 40) = 70
```

`Order.mark_paid()` is allowed only if:

```text
status == "submitted"
```

### 4.3 Why `OrderLine` Is Not an Aggregate Root

An `OrderLine` should not be edited independently by unrelated services because the order total and order status rules belong to the whole order.

Verification: `Order` is the correct aggregate root because all listed invariants involve order-level state and must be preserved together.

## 5. Signs of Bad Aggregate Design

An aggregate is too large when:

- it loads a large object graph for one small change
- many users or processes contend on the same root
- unrelated invariants are forced into the same transaction

An aggregate is too small when:

- invariants must be repaired outside the root
- external code mutates child objects directly
- consistency depends on callers remembering several steps

## 6. Common Mistakes

1. **Table-shaped modeling.** Mirroring the database schema in the object model produces anemic behavior; design around domain rules and ownership instead.
2. **Oversized aggregates.** Pulling many concepts into one root increases contention and complexity; keep only immediately consistent objects together.
3. **Public child mutation.** Letting callers edit internal entities directly bypasses invariants; funnel changes through the aggregate root.
4. **Identity confusion.** Treating value objects like mutable entities makes equality and updates harder; use immutable value semantics where identity is unnecessary.
5. **Repository leakage.** Allowing repositories to reconstruct domain rules in queries or services weakens the model; keep invariants in domain methods.

## 7. Practical Checklist

- [ ] Write down the invariants that must hold after each operation.
- [ ] Choose aggregate roots based on immediate consistency needs.
- [ ] Keep value objects immutable when practical.
- [ ] Expose behavior-rich methods instead of public field mutation.
- [ ] Keep persistence concerns outside the aggregate interface.
- [ ] Revisit boundaries if one aggregate becomes a performance or contention hotspot.

## 8. References

- Evans, Eric. *Domain-Driven Design*. Addison-Wesley, 2003.
- Vernon, Vaughn. *Implementing Domain-Driven Design*. Addison-Wesley, 2013.
- Khononov, Vlad. *Learning Domain-Driven Design*. O'Reilly, 2021.
- Fowler, Martin. *Patterns of Enterprise Application Architecture*. Addison-Wesley, 2002.
- Young, Greg. "A Decade of DDD, CQRS, Event Sourcing." <https://www.youtube.com/watch?v=LDW0QWie21s>
- Brandolini, Alberto. *Introducing EventStorming*. Leanpub, 2021.
- Fowler, Martin. "DDD Aggregate." <https://martinfowler.com/bliki/DDD_Aggregate.html>
