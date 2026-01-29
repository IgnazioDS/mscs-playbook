from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict


class ClassificationResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    label: str
    confidence: float


class ExtractionResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    items: list[dict]


class SummaryResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    summary: str
    bullets: list[str]


class PlanResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    steps: list[str]
    tools: list[str]


def validate_json(model_cls: type[BaseModel], json_obj: Any) -> BaseModel:
    return model_cls.model_validate(json_obj)
