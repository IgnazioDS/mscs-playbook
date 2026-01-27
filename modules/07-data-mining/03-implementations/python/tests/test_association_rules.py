from src.mining.association_rules import apriori, generate_rules


def test_apriori_and_rules():
    transactions = [
        ["milk", "bread"],
        ["milk"],
        ["bread", "butter"],
        ["milk", "bread", "butter"],
    ]
    support_map = apriori(transactions, min_support=0.25)
    assert len(support_map) > 0

    rules = generate_rules(support_map, min_confidence=0.5)
    assert isinstance(rules, list)
    if rules:
        top = rules[0]
        assert top["support"] > 0
        assert top["confidence"] > 0
        assert top["lift"] > 0
        rules_again = generate_rules(support_map, min_confidence=0.5)
        assert rules == rules_again
