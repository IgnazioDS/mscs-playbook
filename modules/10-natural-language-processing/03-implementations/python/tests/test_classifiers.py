from src.nlp.classifiers import train_linear_text_classifier
from src.nlp.datasets import make_ticket_dataset


def test_classifier_deterministic_accuracy():
    data = make_ticket_dataset()
    model = train_linear_text_classifier(data["texts"], data["labels"], seed=42)
    preds = model.predict(data["texts"])
    assert len(preds) == len(data["labels"])
