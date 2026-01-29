import numpy as np

from src.cv.features import harris_corners, sobel_edges, topk_keypoints


def test_edges_and_corners_on_square():
    gray = np.zeros((10, 10), dtype=np.float32)
    gray[3:7, 3:7] = 1.0
    edges = sobel_edges(gray)
    assert edges.sum() > 0.0
    response = harris_corners(gray)
    keypoints = topk_keypoints(response, k=4)
    assert len(keypoints) == 4
    assert keypoints[0][2] >= keypoints[-1][2]
