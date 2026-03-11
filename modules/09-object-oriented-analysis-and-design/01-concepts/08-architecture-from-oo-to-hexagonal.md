# Architecture from OO to Hexagonal

## Key Ideas

- Architecture is the large-scale expression of object-oriented design decisions about responsibilities, dependency direction, and boundary ownership.
- Hexagonal architecture isolates the application core from external systems by placing stable policy behind explicit ports and adapters.
- OO design principles such as cohesion, dependency inversion, and behavioral boundaries scale naturally into architectural rules.
- The value of hexagonal structure is not aesthetic purity; it is reducing the cost of replacing infrastructure and testing core behavior.
- Architecture should emerge from use cases and domain pressure, not from copying layer diagrams without a dependency rationale.

## 1. Why Architecture Follows OOAD

Architecture is often presented as a separate concern from object-oriented design, but the two are continuous. A class boundary answers "who owns this behavior?" An architectural boundary answers "which part of the system may depend on which other part?"

If the local object design is confused, the architecture will also be confused. Hexagonal architecture is one way to preserve good OOAD properties at module and application scale.

## 2. Ports and Adapters

### 2.1 Port

A **port** is an interface that defines how the application core interacts with something outside itself.

Examples:

- repository access
- payment charging
- notification sending

### 2.2 Adapter

An **adapter** is a concrete implementation of a port for one external technology or system.

Examples:

- SQL repository adapter
- Stripe payment adapter
- email notification adapter

### 2.3 Dependency Direction

The domain or application core depends on ports. Adapters depend on the same ports. Concrete frameworks and SDKs stay outside the core.

## 3. Worked Example: Order Processing Structure

Suppose an order application needs to:

- place orders
- charge payments
- send confirmation messages
- save order state

### 3.1 Hexagonal Slice

```text
Application Core
  PlaceOrderService
  Order aggregate
  PaymentPort
  NotificationPort
  OrderRepositoryPort

Adapters
  StripePaymentAdapter
  EmailNotificationAdapter
  PostgresOrderRepository
```

### 3.2 Dependency Trace

During one successful order placement:

```text
1. PlaceOrderService validates the command
2. Order aggregate enforces domain rules
3. PlaceOrderService calls PaymentPort.charge(70)
4. PlaceOrderService calls OrderRepositoryPort.save(order)
5. PlaceOrderService calls NotificationPort.send_confirmation(order_id)
```

The service depends only on ports, not on Stripe, Postgres, or SMTP details.

### 3.3 Benefit

To replace Stripe with another gateway, only the payment adapter changes if the port remains valid.

Verification: the application workflow depends on stable port contracts while infrastructure-specific knowledge remains confined to the adapters.

## 4. When Hexagonal Architecture Fits

Hexagonal architecture is especially useful when:

- infrastructure is likely to change
- the domain model contains real business rules
- the team needs fast core testing without heavy integration setup
- multiple adapters must satisfy the same use case

It may be unnecessary when the system is small, the domain is thin, and infrastructure volatility is low. In those cases, a simpler layered design may be enough.

## 5. Mapping OO Principles to Architecture

- SRP becomes clear module ownership.
- DIP becomes inward-facing dependency direction.
- ISP becomes focused ports rather than giant gateway interfaces.
- cohesion becomes keeping domain logic out of controllers and adapters.

This is why hexagonal architecture should be treated as a scaling of OOAD rather than as an unrelated pattern.

## 6. Common Mistakes

1. **Port explosion.** Creating one port per trivial method adds noise without improving flexibility; define ports around stable collaboration needs instead.
2. **Adapter leakage.** Letting framework types or SDK exceptions cross into the core defeats the boundary; translate them at the adapter edge.
3. **Anemic core.** Moving all logic into services while the domain model stays passive wastes the architecture; keep real policy and invariants in the core.
4. **Layer cargo cult.** Copying hexagonal diagrams without infrastructure volatility or domain depth adds complexity; justify the boundary with actual change pressure.
5. **Bidirectional dependencies.** Allowing the core to import adapters or frameworks reverses the intended architecture; enforce dependency direction in code structure and reviews.

## 7. Practical Checklist

- [ ] Identify which dependencies are external details and should sit behind ports.
- [ ] Keep domain and application code free of framework-specific imports.
- [ ] Define ports around stable use-case needs, not individual API calls.
- [ ] Translate infrastructure errors and payloads at the adapter boundary.
- [ ] Test core workflows with fake adapters before adding integration tests.
- [ ] Reassess whether hexagonal structure is earning its complexity in the current system.

## 8. References

- Cockburn, Alistair. "Hexagonal Architecture." <https://alistair.cockburn.us/hexagonal-architecture>
- Martin, Robert C. *Clean Architecture*. Prentice Hall, 2017.
- Evans, Eric. *Domain-Driven Design*. Addison-Wesley, 2003.
- Vernon, Vaughn. *Implementing Domain-Driven Design*. Addison-Wesley, 2013.
- Fowler, Martin. *Patterns of Enterprise Application Architecture*. Addison-Wesley, 2002.
- Palermo, Jeffrey. "The Onion Architecture." <https://jeffreypalermo.com/2008/07/the-onion-architecture-part-1/>
- Freeman, Steve, and Nat Pryce. *Growing Object-Oriented Software, Guided by Tests*. Addison-Wesley, 2009.
