import numpy as np

from src.cv.preprocess import normalize, random_crop, random_flip, resize


def test_resize_shape():
    arr = np.ones((10, 20, 3), dtype=np.float32)
    resized = resize(arr, (6, 8))
    assert resized.shape == (6, 8, 3)


def test_normalize():
    arr = np.ones((2, 2, 3), dtype=np.float32)
    normed = normalize(arr, mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
    assert np.allclose(normed, 1.0)


def test_random_flip_deterministic():
    arr = np.arange(9, dtype=np.float32).reshape(3, 3)
    flipped_a = random_flip(arr, seed=42, p=1.0)
    flipped_b = random_flip(arr, seed=42, p=1.0)
    assert np.array_equal(flipped_a, flipped_b)


def test_random_crop_deterministic():
    arr = np.arange(25, dtype=np.float32).reshape(5, 5)
    crop_a = random_crop(arr, (3, 3), seed=0)
    crop_b = random_crop(arr, (3, 3), seed=0)
    assert np.array_equal(crop_a, crop_b)
    assert crop_a.shape == (3, 3)
