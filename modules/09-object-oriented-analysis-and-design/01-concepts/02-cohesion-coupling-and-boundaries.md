# Cohesion, Coupling, and Boundaries

## Key Ideas

- Cohesion measures whether a module's responsibilities belong together, while coupling measures how much one module depends on others.
- High cohesion and controlled coupling make change cheaper because engineers can modify one area without unpredictable ripple effects.
- Boundaries are design decisions that determine where knowledge stops, where dependencies point, and where testing can be isolated.
- Good boundaries do not eliminate dependencies; they make dependency direction deliberate and visible.
- Cohesion and coupling should be evaluated at class, package, and service boundaries, not only at the level of individual methods.

## 1. Why These Concepts Matter

Object-oriented systems become difficult to maintain when responsibilities spread across too many places or when modules know too much about each other. Cohesion and coupling give a language for diagnosing that problem.

A cohesive class groups behavior around one concept or one reason to change. A loosely coupled class depends on other modules through small, stable contracts rather than through deep implementation knowledge.

## 2. Definitions and Signals

### 2.1 Cohesion

**Cohesion** is the degree to which a module's elements support the same purpose.

Signals of high cohesion:

- methods operate on the same state
- the class name explains most methods naturally
- changes usually come from one kind of requirement

Signals of low cohesion:

- unrelated helper methods accumulate in one class
- the class needs many prefixes like `email_`, `invoice_`, and `report_`
- one class serves several use cases with little shared state

### 2.2 Coupling

**Coupling** is the degree to which a module depends on the internal details of another module.

Signals of high coupling:

- direct imports of concrete infrastructure classes
- knowledge of another module's private data shape
- chained calls across multiple objects to reach a value

## 3. Boundary Design

A **boundary** is the line where one part of the system stops being responsible and another part begins. Boundaries often appear between:

- domain and infrastructure
- application orchestration and domain rules
- public APIs and internal implementation
- one aggregate or subsystem and another

The best boundaries usually align with volatility. If payment processors change often, isolate that dependency. If pricing rules change often, keep them in a cohesive policy area rather than scattering them across controllers and persistence code.

## 4. Worked Example: Splitting a Low-Cohesion Class

Assume an `OrderProcessor` class currently does all of the following:

- validates order totals
- reserves inventory
- charges a payment gateway
- writes audit logs
- sends email notifications

### 4.1 Diagnose the Design

This class has at least four reasons to change:

1. pricing rules change
2. inventory workflow changes
3. payment integration changes
4. notification policy changes

That is low cohesion.

It is also tightly coupled because one class knows how every subsystem works.

### 4.2 Redesign

Split the responsibilities:

```text
Order
  + validate_total()

OrderSubmissionService
  + submit(order)

InventoryPort
PaymentPort
NotifierPort
AuditLogPort
```

### 4.3 Result

- `Order` owns order-specific validation.
- `OrderSubmissionService` coordinates the use case.
- ports reduce coupling to infrastructure.
- notification and logging can change independently.

Verification: the redesign reduces reasons to change per class and replaces direct infrastructure knowledge with narrow boundary contracts.

## 5. Heuristics for Healthier Modules

Ask three questions repeatedly:

1. What is this module responsible for?
2. What other modules must it know about to do that work?
3. If a requirement changes, how far does the change spread?

When the answers are vague, the design is probably vague too.

Boundary quality also appears in tests. If every unit test needs a full object graph and several real dependencies, the boundaries are probably too entangled.

## 6. Common Mistakes

1. **Name-based cohesion.** Giving a class a neat name does not make it cohesive; inspect whether its methods and fields actually support one responsibility.
2. **Interface theater.** Adding interfaces everywhere without reducing knowledge or coupling only adds ceremony; introduce abstractions at real seams of change.
3. **Leaky boundaries.** Passing infrastructure types deep into the domain spreads external concerns; translate them at the boundary instead.
4. **Chatty object graphs.** Requiring long chains like `a.b().c().d()` exposes too much internal structure; ask the owning object to provide the needed behavior directly.
5. **Layer confusion.** Letting domain code orchestrate transport, storage, or UI concerns blurs boundaries; keep each layer responsible for its own kind of work.

## 7. Practical Checklist

- [ ] State the single purpose of each important class or module.
- [ ] Count the independent reasons a class might change.
- [ ] Replace direct concrete dependencies with smaller boundary contracts where volatility exists.
- [ ] Translate framework and transport data at the system edge.
- [ ] Watch for long call chains that expose internals across modules.
- [ ] Use tests to confirm that domain behavior can run without infrastructure details.

## 8. References

- Parnas, David L. "On the Criteria To Be Used in Decomposing Systems into Modules." *Communications of the ACM*, 1972. <https://dl.acm.org/doi/10.1145/361598.361623>
- Martin, Robert C. *Agile Software Development, Principles, Patterns, and Practices*. Prentice Hall, 2002.
- Constantine, Larry, and Edward Yourdon. *Structured Design*. Prentice Hall, 1979.
- Evans, Eric. *Domain-Driven Design*. Addison-Wesley, 2003.
- Martin, Robert C. *Clean Architecture*. Prentice Hall, 2017.
- Fowler, Martin. "Inversion of Control Containers and the Dependency Injection Pattern." <https://martinfowler.com/articles/injection.html>
- Vernon, Vaughn. *Implementing Domain-Driven Design*. Addison-Wesley, 2013.
