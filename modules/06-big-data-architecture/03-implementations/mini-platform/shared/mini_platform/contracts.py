"""Versioned event contracts for the mini-platform ingest boundary."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, StringConstraints, field_validator


NonEmptyText = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
CurrencyCode = Annotated[str, StringConstraints(pattern=r"^[A-Z]{3}$")]
SupportedEventType = Literal["order_created"]
SupportedSchemaVersion = Literal[1]


class OrderCreatedV1(BaseModel):
    """Phase 3 contract for accepted order events."""

    model_config = ConfigDict(extra="forbid")

    schema_version: Literal[1]
    event_type: Literal["order_created"]
    event_time: datetime
    order_id: NonEmptyText
    amount: Annotated[float, Field(gt=0)]
    currency: CurrencyCode
    customer_id: NonEmptyText

    @field_validator("event_time")
    @classmethod
    def _require_timezone(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.tzinfo.utcoffset(value) is None:
            raise ValueError("event_time must include a timezone offset")
        return value.astimezone(timezone.utc)


CONTRACT_REGISTRY: dict[tuple[str, int], type[BaseModel]] = {
    ("order_created", 1): OrderCreatedV1,
}


def get_contract_model(event_type: str, schema_version: int) -> type[BaseModel] | None:
    return CONTRACT_REGISTRY.get((event_type, schema_version))


def supported_contracts() -> list[dict[str, object]]:
    return [
        {
            "event_type": event_type,
            "schema_version": schema_version,
            "model": model.__name__,
        }
        for (event_type, schema_version), model in sorted(CONTRACT_REGISTRY.items())
    ]
