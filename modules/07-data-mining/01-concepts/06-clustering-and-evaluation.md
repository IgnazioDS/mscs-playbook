# Clustering and Evaluation

## Key Ideas

- Clustering groups observations by similarity without target labels, so the meaning of similarity and the representation of the data determine the result as much as the algorithm does.
- Clustering output is a proposed structure, not a discovered truth, and it must be validated through internal metrics, stability checks, and domain interpretation.
- Different clustering families make different assumptions: k-means prefers compact spherical groups, hierarchical methods expose nested structure, and density-based methods can isolate irregular groups and noise.
- Evaluation should ask both whether the clusters are well formed and whether they are useful for the downstream purpose such as segmentation, summarization, or anomaly triage.
- Feature scaling and preprocessing are central because distance-based clustering is highly sensitive to geometry.

## 1. What Clustering Is

Clustering is the task of partitioning or organizing observations so that items within a group are more similar to one another than to items in other groups under a chosen similarity definition.

### 1.1 Core Definitions

- A **cluster** is a group of similar observations.
- A **centroid** is a representative center used in methods such as k-means.
- **Inertia** is the sum of squared distances from points to their assigned centroid.
- A **silhouette score** measures how well a point fits its own cluster relative to neighboring clusters.
- **Density-based clustering** groups points based on dense regions rather than fixed centers.

### 1.2 Why This Matters

Clustering is often used for customer segmentation, document grouping, exploratory summarization, and data simplification. But because there is no label to prove the answer, weak evaluation can turn arbitrary structure into false confidence.

## 2. Major Clustering Families

### 2.1 Partitioning Methods

k-means and related methods assign each point to one of a fixed number of clusters. They are efficient and common, but they depend heavily on scale, initialization, and the choice of `k`.

### 2.2 Hierarchical Methods

Hierarchical clustering produces a nested grouping structure and can reveal multi-level organization, though it may be more computationally expensive and sensitive to linkage choices.

### 2.3 Density-Based Methods

Methods such as DBSCAN can identify clusters of irregular shape and mark sparse points as noise. They are useful when compact-center assumptions are unrealistic.

## 3. How to Evaluate Clustering Results

### 3.1 Internal Metrics

Internal metrics such as silhouette score and inertia summarize compactness and separation, but they only evaluate the chosen geometry.

### 3.2 Stability Checks

If small changes in seed, sample, or preprocessing produce very different clusters, the discovered structure may be too fragile to use.

### 3.3 Domain Validation

A segmentation is useful only if cluster profiles differ in ways that matter operationally, such as spending pattern, product mix, or behavior frequency.

## 4. Worked Example: Simple Silhouette Comparison

Suppose a team compares two clustering choices on the same preprocessed dataset:

```text
k = 2 -> silhouette = 0.38
k = 3 -> silhouette = 0.57
```

They also compute the mean distance-to-centroid within clusters:

```text
k = 2 -> mean_within_distance = 1.9
k = 3 -> mean_within_distance = 1.2
```

### 4.1 Compare Silhouette Scores

```text
0.57 > 0.38
```

So `k = 3` has better separation under the silhouette criterion.

### 4.2 Compare Within-Cluster Tightness

```text
1.2 < 1.9
```

So `k = 3` also yields tighter average clusters in this comparison.

### 4.3 Interpret the Result

Under these internal metrics, `k = 3` is the stronger candidate. That still does not prove that three clusters are the best business segmentation. The next step would be to inspect cluster profiles and check stability across seeds.

Verification: the metric comparison is internally consistent because `0.57` exceeds `0.38` and `1.2` is smaller than `1.9`, so both criteria favor `k = 3` in the stated example.

## 5. Common Mistakes

1. **Cluster realism assumption.** Treating every cluster as a natural category confuses algorithmic grouping with validated structure; check whether the grouping is meaningful in the domain.
2. **Unscaled-distance misuse.** Running distance-based clustering on incompatible feature scales lets one variable dominate the result; standardize or otherwise normalize when appropriate.
3. **Single-metric certainty.** Declaring success from one internal score hides fragility and interpretability issues; combine internal metrics with stability and profile review.
4. **Forced-k habit.** Choosing `k` because it feels reasonable rather than because the data and task support it leads to arbitrary segmentation; compare multiple candidates explicitly.
5. **Profile neglect.** Reporting cluster IDs without describing what distinguishes them makes the result hard to use; inspect feature summaries and behavior differences by cluster.

## 6. Practical Checklist

- [ ] Scale or otherwise normalize features before distance-based clustering.
- [ ] Compare multiple clustering choices rather than selecting one by default.
- [ ] Use at least one internal metric and one stability-oriented check.
- [ ] Review cluster profiles in domain terms before presenting results as actionable.
- [ ] Record preprocessing choices because they strongly affect the cluster geometry.
- [ ] Reassess clustering usefulness against the actual segmentation use case.

## 7. References

- Tan, Pang-Ning, Michael Steinbach, Anuj Karpatne, and Vipin Kumar. 2018. *Introduction to Data Mining* (2nd ed.). Pearson.
- Han, Jiawei, Micheline Kamber, and Jian Pei. 2011. *Data Mining: Concepts and Techniques* (3rd ed.). Morgan Kaufmann.
- scikit-learn. 2026. *Selecting the number of clusters with silhouette analysis on KMeans clustering*. <https://scikit-learn.org/stable/auto_examples/cluster/plot_kmeans_silhouette_analysis.html>
- scikit-learn. 2026. *Clustering*. <https://scikit-learn.org/stable/modules/clustering.html>
- Ester, Martin, et al. 1996. A Density-Based Algorithm for Discovering Clusters in Large Spatial Databases with Noise. <https://aaai.org/papers/kdd96-037-a-density-based-algorithm-for-discovering-clusters-in-large-spatial-databases-with-noise/>
- Hennig, Christian, Marina Meila, Fionn Murtagh, and Roberto Rocci, eds. 2015. *Handbook of Cluster Analysis*. CRC Press.
- Kaufman, Leonard, and Peter J. Rousseeuw. 2009. *Finding Groups in Data*. Wiley.
