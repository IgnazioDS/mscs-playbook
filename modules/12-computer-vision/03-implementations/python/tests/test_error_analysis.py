import numpy as np

from src.cv.error_analysis import confusion_matrix, worst_k_examples


def test_confusion_matrix():
    y_true = [0, 0, 1, 1]
    y_pred = [0, 1, 1, 0]
    cm = confusion_matrix(y_true, y_pred, labels=[0, 1])
    assert cm.tolist() == [[1, 1], [1, 1]]


def test_worst_k_examples():
    y_true = [0, 0, 1, 1]
    y_pred = [0, 1, 1, 0]
    probs = np.array(
        [
            [0.9, 0.1],
            [0.4, 0.6],
            [0.4, 0.6],
            [0.8, 0.2],
        ],
        dtype=np.float32,
    )
    worst = worst_k_examples(y_true, y_pred, probs, k=2)
    assert [item[0] for item in worst] == [3, 1]
