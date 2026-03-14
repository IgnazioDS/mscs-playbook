# Supported Contracts

The mini-platform currently accepts one external ingest contract.

## Accepted Contract

`order_created`
- `schema_version`: `1`
- required fields:
  - `schema_version`
  - `event_type`
  - `event_time`
  - `order_id`
  - `amount`
  - `currency`
  - `customer_id`

Validation rules:
- `schema_version` must be `1`
- `event_type` must be `order_created`
- `event_time` must be an ISO 8601 timestamp with a timezone offset
- `amount` must be numeric and greater than zero
- `currency` must be a 3-letter uppercase code
- unknown keys are rejected

Example:

```json
{
  "schema_version": 1,
  "event_type": "order_created",
  "event_time": "2026-01-27T12:00:00Z",
  "order_id": "O-1",
  "amount": 10.5,
  "currency": "USD",
  "customer_id": "C-1"
}
```

## Not Supported

- additional event types
- additional schema versions
- implicit schema upgrades at ingest time
- external schema registry integration
