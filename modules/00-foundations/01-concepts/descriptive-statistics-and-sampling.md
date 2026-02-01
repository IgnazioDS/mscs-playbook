# Descriptive Statistics and Sampling

## What it is
A compact toolkit for summarizing data (center, spread, shape) and for reasoning
about sample-based estimates of population quantities.

## Why it matters
Most pipelines start with data sanity checks and summary metrics. If you cannot
trust the basics (mean, variance, sampling error), downstream modeling and
decisions are unreliable.

## Core ideas
- Central tendency: mean, median, mode
- Spread: variance, standard deviation, IQR
- Shape: skewness, heavy tails, outliers
- Sampling error: estimate vs truth, confidence intervals

## Example
A revenue dataset with a long tail: median is more stable than mean for
reporting typical customer value.

## Pitfalls
- Reporting means without uncertainty
- Mixing populations (e.g., new vs returning users)
- Ignoring outliers and data collection bias

## References
- Freedman, Pisani, Purves, *Statistics*
- OpenIntro Statistics (descriptive stats chapters)
