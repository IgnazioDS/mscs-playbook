from src.patterns.strategy import NoDiscount, PercentageDiscount, PriceCalculator


def test_strategy_extension():
    calc = PriceCalculator(NoDiscount())
    assert calc.total(100.0) == 100.0

    calc.set_strategy(PercentageDiscount(0.1))
    assert calc.total(100.0) == 90.0
