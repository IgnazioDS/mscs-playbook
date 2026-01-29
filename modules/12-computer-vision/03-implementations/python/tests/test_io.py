import numpy as np

from src.cv.io import load_image, save_image, to_grayscale


def test_save_load_roundtrip(tmp_path):
    arr = np.zeros((8, 8, 3), dtype=np.float32)
    arr[2:6, 2:6, :] = 1.0
    path = tmp_path / "img.png"
    save_image(path, arr)
    loaded = load_image(path)
    assert loaded.shape == (8, 8, 3)
    assert loaded.dtype == np.float32
    assert loaded.max() <= 1.0


def test_to_grayscale():
    arr = np.zeros((4, 4, 3), dtype=np.float32)
    arr[:, :, 0] = 1.0
    gray = to_grayscale(arr)
    assert gray.shape == (4, 4)
    assert gray.max() <= 1.0
