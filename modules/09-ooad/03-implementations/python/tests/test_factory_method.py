import pytest

from src.patterns.factory_method import BankTransferProcessor, PaymentProcessorFactory


def test_factory_creates_correct_type():
    processor = PaymentProcessorFactory.create("bank")
    assert isinstance(processor, BankTransferProcessor)


def test_factory_rejects_unknown_type():
    with pytest.raises(ValueError):
        PaymentProcessorFactory.create("crypto")
