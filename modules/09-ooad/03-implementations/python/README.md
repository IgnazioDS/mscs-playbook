# OOAD Patterns Cookbook (Python)

Small, runnable pattern examples with deterministic tests.

## Quickstart
- `python3 -m venv .venv`
- `source .venv/bin/activate`
- `pip install -r modules/09-ooad/03-implementations/python/requirements.txt`
- `python -m pytest -q modules/09-ooad/03-implementations/python/tests`
- `python modules/09-ooad/03-implementations/python/src/mini_project/cli.py`

## Patterns cookbook
- Strategy: `src/patterns/strategy.py`
- Observer: `src/patterns/observer.py`
- Factory Method: `src/patterns/factory_method.py`
- Adapter: `src/patterns/adapter.py`
- Decorator: `src/patterns/decorator.py`
- Command: `src/patterns/command.py`
- Repository: `src/patterns/repository.py`

## Mini-project
- `python modules/09-ooad/03-implementations/python/src/mini_project/cli.py`
  - Demonstrates Strategy, Factory Method, Adapter, Observer, and Command in one flow

## Design docs
- `src/mini_project/docs/DESIGN.md`
- `src/mini_project/docs/adrs/0001-architecture-style.md`
- `src/mini_project/docs/adrs/0002-domain-events.md`
- `src/mini_project/docs/adrs/0003-repository-abstraction.md`
- `src/mini_project/docs/adrs/0004-payment-adapters.md`

## Reproducibility
- Tests are deterministic and use stable, in-memory IDs.
- CLI output is stable for the fixed scenario.

## How to extend
- Strategy: add a new pricing policy class and register it with the client.
- Observer: add a new subscriber and subscribe it to the event bus.
- Factory Method: implement a new processor and add it to the factory map.
- Adapter: wrap a new legacy API behind the target interface.
- Decorator: wrap a service with additional behavior (logging/timing).
- Command: add a new command with execute/undo.
- Repository: add new query methods without exposing storage internals.
