from src.mini_project.infrastructure.payments import PaymentProcessorFactory


def test_paypal_adapter_charges_in_dollars():
    factory = PaymentProcessorFactory()
    processor = factory.create("paypal")
    result = processor.charge(2500)
    assert result == "paypal:25.00"
