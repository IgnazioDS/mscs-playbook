import pytest
from pydantic import ValidationError

from src.genai.schemas import (
    ClassificationResult,
    SummaryResult,
    validate_json,
)


def test_validate_json_success():
    result = validate_json(ClassificationResult, {"label": "billing", "confidence": 0.9})
    assert result.label == "billing"


def test_validate_json_failure():
    with pytest.raises(ValidationError):
        validate_json(SummaryResult, {"summary": "test"})
