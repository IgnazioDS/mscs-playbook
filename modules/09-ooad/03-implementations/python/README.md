# OOAD Patterns Cookbook (Python)

Small, runnable pattern examples with deterministic tests.

## Setup
- `python3 -m venv .venv`
- `source .venv/bin/activate`
- `pip install -r modules/09-ooad/03-implementations/python/requirements.txt`

## Tests
- `python -m pytest -q modules/09-ooad/03-implementations/python/tests`

## How to extend
- Strategy: add a new pricing policy class and register it with the client.
- Observer: add a new subscriber and subscribe it to the event bus.
- Factory Method: implement a new processor and add it to the factory map.
- Adapter: wrap a new legacy API behind the target interface.
- Decorator: wrap a service with additional behavior (logging/timing).
- Command: add a new command with execute/undo.
- Repository: add new query methods without exposing storage internals.
