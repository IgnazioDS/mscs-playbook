# OOAD Foundations and UML Lite

## Key Ideas

- Object-oriented analysis and design starts by modeling responsibilities, collaborations, and change boundaries before choosing implementation details.
- An object is useful when it owns both state and behavior, so good OOAD avoids turning classes into passive data containers.
- Lightweight diagrams are communication tools, not deliverables for their own sake, and should stay tightly aligned with important code paths.
- A design becomes easier to evolve when responsibilities are explicit, dependencies are visible, and each class has a narrow reason to change.
- OOAD is strongest when it focuses on domain concepts and use cases rather than on framework structure or storage concerns.

## 1. What OOAD Is

Object-oriented analysis identifies the important concepts, behaviors, and interactions in a system. Object-oriented design then turns that understanding into a set of collaborating classes, interfaces, and boundaries.

The goal is not to maximize the number of classes. The goal is to make change predictable. If a use case changes, the engineer should be able to see which objects are responsible, which collaborators are affected, and where the change should stop.

### 1.1 Core Terms

- An **object** is a runtime entity with state and behavior.
- A **class** defines the structure and behavior shared by similar objects.
- A **responsibility** is a reason an object exists and the work it must perform.
- A **collaboration** is an interaction between objects to complete a use case.
- A **boundary** is a separation point where changes should be contained.

## 2. Why Lightweight Modeling Helps

OOAD is most useful before a codebase becomes rigid. A short modeling pass clarifies:

- which concepts belong in the domain model
- which behaviors must be coordinated
- which dependencies should be isolated
- which objects are likely to change together

This reduces two common failures. First, engineers often create "manager" classes that absorb unrelated work. Second, teams often let storage schemas or API payloads drive the object model even when those concerns should stay outside the core design.

## 3. UML Lite Instead of Full Formalism

UML Lite means using only the smallest diagram set needed to explain the design.

### 3.1 Class Diagram Essentials

A class diagram should usually show:

- key classes and interfaces
- major associations
- ownership or composition where it matters
- important public operations

It should not try to mirror every field or method.

### 3.2 Sequence Diagram Essentials

A sequence diagram shows the order of calls in a use case. It is useful when the same behavior spans several objects and timing or coordination matters.

For most engineering work, a single class diagram plus one or two sequence diagrams is enough to communicate intent.

## 4. Worked Example: From Use Case to Objects

Suppose a team needs a simple order-submission flow with these rules:

- a customer submits an order
- the order total must be positive
- the order is reserved before payment
- the payment gateway is external

### 4.1 Analysis View

The main domain concepts are:

- `Order`
- `OrderLine`
- `InventoryReservation`
- `PaymentGateway`

The use case suggests that `PaymentGateway` is not a domain entity. It is an external dependency.

### 4.2 Design View

A lightweight class model might be:

```text
Order
  - lines
  - status
  + total()
  + mark_reserved()
  + mark_paid()

OrderService
  + submit_order(order_data)

InventoryPort
  + reserve(order)

PaymentPort
  + charge(order_id, amount)
```

### 4.3 Sequence of One Use Case

```text
1. OrderService builds Order from input
2. Order.total() validates total > 0
3. OrderService calls InventoryPort.reserve(order)
4. Order.mark_reserved()
5. OrderService calls PaymentPort.charge(order_id, amount)
6. Order.mark_paid()
```

### 4.4 Why This Is Better Than a Single Manager Class

If all logic lived in `OrderManager`, three concerns would mix:

- domain validation
- orchestration of external systems
- order state changes

Separating them makes responsibilities testable and easier to modify.

Verification: `Order` owns order state and invariants, while `OrderService` coordinates the use case and the ports isolate infrastructure dependencies.

## 5. How to Use OOAD in Practice

Start with one concrete use case. Identify the nouns that have behavior, not just the nouns that appear in the UI or database. Assign responsibilities explicitly. Then draw the smallest diagram that lets another engineer understand the collaboration.

If two classes always change together, the boundary is probably wrong. If a class mostly forwards calls, it may not deserve to exist. If a class both enforces domain rules and talks to infrastructure, it is usually carrying too many concerns.

## 6. Common Mistakes

1. **Data-bag classes.** Treating objects as structs with getters and setters pushes all behavior elsewhere; move invariants and state transitions back into the object that owns the data.
2. **Framework-first modeling.** Starting from controllers, ORM models, or endpoints distorts the domain model; begin with use cases and domain responsibilities instead.
3. **Diagram overload.** Documenting every method and relationship creates stale artifacts; keep diagrams selective and focused on the highest-value flows.
4. **Manager-class gravity.** Centralizing all decisions in service or manager classes hides ownership boundaries; split responsibilities so domain objects enforce their own rules.
5. **Unclear change boundaries.** If a single requirement touches many unrelated classes, the design is leaking responsibilities; redraw boundaries around cohesive behavior.

## 7. Practical Checklist

- [ ] Start from a specific use case before drawing classes.
- [ ] Name the main responsibilities of each object in one sentence.
- [ ] Keep domain rules inside the objects that own the affected state.
- [ ] Draw only the class and sequence diagrams needed to explain the design.
- [ ] Isolate external systems behind explicit interfaces or ports.
- [ ] Revisit the model when two classes repeatedly change together.

## 8. References

- Fowler, Martin. *UML Distilled* (3rd ed.). Addison-Wesley, 2003.
- Larman, Craig. *Applying UML and Patterns* (3rd ed.). Prentice Hall, 2004.
- Evans, Eric. *Domain-Driven Design*. Addison-Wesley, 2003.
- Booch, Grady. *Object-Oriented Analysis and Design with Applications* (3rd ed.). Addison-Wesley, 2007.
- Wirfs-Brock, Rebecca, Brian Wilkerson, and Lauren Wiener. *Designing Object-Oriented Software*. Prentice Hall, 1990.
- Fowler, Martin. "UML." <https://martinfowler.com/bliki/UmlSketch.html>
- Cockburn, Alistair. "Use Cases and Object Thinking." <https://alistair.cockburn.us/>
