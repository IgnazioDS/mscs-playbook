# Classical Features and Keypoints

## Overview
Classical vision uses hand-crafted features and keypoints to describe images for
matching, recognition, and geometry tasks.

## Why it matters
Feature-based pipelines can be fast, interpretable, and effective when data is
limited or compute is constrained.

## Key ideas
- Keypoints identify repeatable interest points
- Descriptors summarize local image patches
- Matching uses distance metrics and ratio tests
- RANSAC filters outliers for geometric consistency

## Practical workflow
- Detect keypoints (SIFT/ORB/FAST)
- Compute descriptors and match across images
- Use RANSAC to fit homography or fundamental matrix
- Evaluate match quality with inliers and reprojection error

## Failure modes
- Repetitive textures cause false matches
- Motion blur reduces keypoint stability
- Illumination changes hurt descriptor robustness
- Scale changes beyond descriptor limits

## Checklist
- Validate keypoint density and match counts
- Use geometric verification (RANSAC)
- Track inlier ratios across conditions
- Keep feature parameters versioned

## References
- SIFT — https://www.cs.ubc.ca/~lowe/papers/ijcv04.pdf
- ORB — https://ieeexplore.ieee.org/document/6126544
