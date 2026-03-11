# Classical Features and Keypoints

## Key Ideas

- Classical vision pipelines detect repeatable points or regions and describe them with hand-crafted features for matching and geometry tasks.
- Keypoints are useful because they reduce an image to stable local structures rather than treating every pixel as equally important.
- Descriptors such as SIFT or ORB summarize local patches so similar visual structures can be matched across views.
- Geometric verification, often with RANSAC, is necessary because local feature matching alone produces many false correspondences.
- Classical features remain valuable when data is limited, interpretability matters, or explicit geometry is part of the task.

## 1. Why Classical Features Still Matter

Modern deep learning dominates many vision tasks, but classical features still solve real problems well:

- image stitching
- visual localization
- motion estimation
- low-data matching

These methods are also instructive because they separate the pipeline into understandable parts: detect, describe, match, and verify.

## 2. Core Concepts

- A **keypoint** is an image location that is distinctive and repeatable under reasonable viewpoint or lighting changes.
- A **descriptor** is a numeric summary of the local patch around a keypoint.
- A **match** pairs two descriptors that appear similar.
- **RANSAC** is a robust fitting method that estimates a geometric model while rejecting outliers.

## 3. Common Pipeline Structure

### 3.1 Detect

Use a detector such as Harris, FAST, SIFT, or ORB to identify candidate points.

### 3.2 Describe

Compute a descriptor for each keypoint so local appearance can be compared across images.

### 3.3 Match

Match descriptors using a distance metric such as Euclidean or Hamming distance.

### 3.4 Verify

Use geometric constraints, often via homography or epipolar fitting, to reject false matches.

## 4. Worked Example: Inlier Ratio After Matching

Suppose two images of the same planar object produce:

```text
detected keypoints in image A = 300
detected keypoints in image B = 280
descriptor matches after ratio test = 60
matches kept as inliers by RANSAC = 42
```

### 4.1 Inlier Ratio

```text
inlier_ratio = 42 / 60 = 0.70
```

### 4.2 Interpretation

An inlier ratio of `0.70` means 70% of tentative matches are geometrically consistent with the fitted transformation. That suggests the match set is reasonably strong.

If only `8` matches survived from `60`, then:

```text
inlier_ratio = 8 / 60 ≈ 0.133
```

That would indicate poor repeatability, weak descriptors, or heavy viewpoint mismatch.

Verification: the example shows why raw match counts are insufficient and why geometric inlier checks are necessary before trusting a feature match set.

## 5. Where Classical Features Fail

Classical features can struggle with:

- repetitive textures
- heavy motion blur
- large illumination changes
- weak texture regions

They also depend strongly on hand-tuned detector and descriptor settings. That is why they are often paired with geometric priors or replaced by learned features in harder settings.

## 6. Common Mistakes

1. **Match-count optimism.** Treating many descriptor matches as success without geometric verification hides false correspondences; use inliers, not raw matches, as the main quality signal.
2. **Detector-descriptor confusion.** Tuning only the matcher while ignoring poor keypoint quality misses the root cause; inspect detection density and repeatability first.
3. **Texture blindness.** Expecting reliable matches in flat or repetitive regions leads to weak geometry; identify whether the scene actually contains distinctive local structure.
4. **Metric mismatch.** Using the wrong distance measure for a descriptor type degrades matching; binary descriptors often require Hamming-style comparison.
5. **No deployment validation.** Evaluating only on easy well-lit examples gives false confidence; test across blur, scale, lighting, and viewpoint changes.

## 7. Practical Checklist

- [ ] Visualize detected keypoints and their spatial coverage.
- [ ] Choose a descriptor and matching metric that are compatible.
- [ ] Use ratio tests or other filters before geometric fitting.
- [ ] Measure inlier ratio after RANSAC instead of trusting raw match count.
- [ ] Test robustness across blur, scale, and illumination changes.
- [ ] Keep detector and descriptor parameters versioned with experiments.

## 8. References

- Lowe, David G. "Distinctive Image Features from Scale-Invariant Keypoints." 2004. <https://www.cs.ubc.ca/~lowe/papers/ijcv04.pdf>
- Rublee, Ethan, et al. "ORB: An efficient alternative to SIFT or SURF." 2011. <https://ieeexplore.ieee.org/document/6126544>
- Harris, Chris, and Mike Stephens. "A Combined Corner and Edge Detector." 1988. <https://www.bmva.org/bmvc/1988/avc-88-023.pdf>
- Fischler, Martin A., and Robert C. Bolles. "Random Sample Consensus." 1981. <https://dl.acm.org/doi/10.1145/358669.358692>
- Szeliski, Richard. *Computer Vision: Algorithms and Applications* (2nd ed.). Springer, 2022. <https://szeliski.org/Book/>
- OpenCV. "Feature detection and description." <https://docs.opencv.org/4.x/db/d27/tutorial_py_table_of_contents_feature2d.html>
- Hartley, Richard, and Andrew Zisserman. *Multiple View Geometry in Computer Vision* (2nd ed.). Cambridge University Press, 2004.
