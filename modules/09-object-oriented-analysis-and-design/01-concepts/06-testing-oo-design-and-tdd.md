# Testing OO Design and TDD

## Key Ideas

- Tests reveal design quality because cohesive, loosely coupled objects are easier to exercise through stable public behavior.
- Test-driven development is most useful as a design-feedback loop, not as a ritual for maximizing test count.
- OO tests should target observable behavior and boundary contracts rather than private implementation details.
- Fakes, stubs, and spies are valuable when they isolate external dependencies without forcing brittle coupling to call sequences.
- A design that is hard to test is often signaling confused responsibilities or missing seams.

## 1. Why Testing Belongs in OOAD

Testing is not only a verification technique. It is also a design diagnostic. If a class requires database setup, time control, network access, and deep object graphs before any behavior can be exercised, the class is probably carrying too many responsibilities.

Well-designed object-oriented systems usually make testing easier because:

- responsibilities are narrow
- boundaries are explicit
- behavior is observable through public methods
- infrastructure can be replaced behind interfaces

## 2. TDD as Design Feedback

Test-driven development means writing a failing test, adding the smallest code to pass it, and then refactoring with the safety of a green test suite.

The design value comes from the pressure it creates:

- unclear API names become obvious
- oversized classes become awkward to instantiate
- hidden dependencies become difficult to substitute

TDD is therefore a way to expose design friction early.

## 3. What to Test in OO Systems

Prefer these test targets:

- domain invariants
- state transitions
- use-case outcomes
- boundary contracts

Avoid anchoring tests to:

- private helper methods
- internal call order that clients do not observe
- exact data structure choices unless performance behavior requires it

## 4. Worked Example: Testing an Order Submission Service

Suppose `OrderSubmissionService` must:

- reject zero-total orders
- reserve inventory
- charge payment
- mark the order as paid on success

### 4.1 Behavior-Oriented Test Sketch

```text
given order total = 70
and inventory reservation succeeds
and payment charge succeeds
when submit(order)
then order status == "paid"
```

### 4.2 Boundary Setup

Use two fakes:

```text
FakeInventoryPort.reserve(order) -> success
FakePaymentPort.charge(order_id, amount) -> success
```

### 4.3 Expected Outcome

The service should:

1. validate the order
2. reserve inventory
3. charge `70`
4. mark the order as paid

This test focuses on observable business behavior. It does not need to inspect private helper methods or internal loops.

Verification: the test is about the service contract and domain outcome, while external variability is isolated behind fake ports.

## 5. Choosing Test Doubles Carefully

- A **stub** provides canned data.
- A **fake** is a lightweight working implementation, often in memory.
- A **spy** records interactions for later assertions.
- A **mock** is a programmable test double that verifies expected interactions.

Fakes are often the least brittle choice for OOAD because they preserve behavior focus. Overuse of mocks can lock tests to internal collaboration details and make refactoring unnecessarily painful.

## 6. Common Mistakes

1. **Private-method testing.** Reaching into internals couples tests to implementation structure; test the public behavior that clients actually depend on.
2. **Over-mocking.** Verifying every call sequence makes refactoring expensive and fragile; use fakes or broader assertions when collaboration order is not the contract.
3. **Infrastructure-heavy units.** Pulling real databases or networks into unit tests hides design problems; isolate external dependencies behind replaceable boundaries.
4. **Behavior-blind assertions.** Checking only that a method was called can miss whether the domain outcome is correct; assert on state transitions and business results too.
5. **TDD cargo cult.** Writing trivial tests after the design is already fixed gives little feedback; use tests to shape interfaces while decisions are still cheap.

## 7. Practical Checklist

- [ ] Write tests around public behavior and domain outcomes.
- [ ] Keep domain logic executable without real infrastructure.
- [ ] Prefer fakes and stubs over brittle interaction-heavy mocks.
- [ ] Use TDD when an API or collaboration is still taking shape.
- [ ] Refactor aggressively only while tests remain green.
- [ ] Treat hard-to-test code as a design smell, not just a tooling inconvenience.

## 8. References

- Beck, Kent. *Test-Driven Development: By Example*. Addison-Wesley, 2002.
- Meszaros, Gerard. *xUnit Test Patterns*. Addison-Wesley, 2007.
- Freeman, Steve, and Nat Pryce. *Growing Object-Oriented Software, Guided by Tests*. Addison-Wesley, 2009.
- Fowler, Martin. *Refactoring* (2nd ed.). Addison-Wesley, 2018.
- Feathers, Michael. *Working Effectively with Legacy Code*. Prentice Hall, 2004.
- Martin, Robert C. *Clean Architecture*. Prentice Hall, 2017.
- Fowler, Martin. "Mocks Aren't Stubs." <https://martinfowler.com/articles/mocksArentStubs.html>
