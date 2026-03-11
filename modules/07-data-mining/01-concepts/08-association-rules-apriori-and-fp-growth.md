# Association Rules: Apriori and FP-Growth

## Key Ideas

- Association-rule mining finds co-occurrence structure in transactional data by first identifying frequent itemsets and then evaluating candidate implication rules.
- Support, confidence, and lift answer different questions, so relying on one metric alone can produce misleading rule rankings.
- Apriori and FP-Growth solve the same broad task but use different computational strategies: Apriori prunes candidate itemsets level by level, while FP-Growth compresses transactions into a pattern tree.
- Useful rules are not just frequent; they must also be statistically credible, interpretable, and relevant to the decision context.
- The main practical dangers are combinatorial explosion, spurious high-confidence rules, and overinterpretation of rules generated from small supports.

## 1. What Association Rules Are

Association rules describe co-occurrence relationships such as "if a basket contains itemset A, it often also contains itemset B." They are common in market-basket analysis, bundle discovery, and behavioral co-occurrence mining.

### 1.1 Core Definitions

- An **itemset** is a set of items appearing together in a transaction.
- **Support** is the fraction of transactions containing an itemset.
- **Confidence** is the conditional rate at which the rule consequent appears when the antecedent appears.
- **Lift** compares observed co-occurrence to what would be expected if antecedent and consequent were independent.
- A **frequent itemset** is an itemset whose support meets a chosen threshold.

### 1.2 Why This Matters

Association rules can reveal meaningful shopping, browsing, or action patterns, but they can also generate large volumes of trivial or misleading rules. Threshold setting and interpretation discipline are central.

## 2. Apriori and FP-Growth

### 2.1 Apriori

Apriori uses the downward-closure idea: if an itemset is frequent, all of its subsets must also be frequent. This allows candidate pruning, but the method can still become expensive when support thresholds are low.

### 2.2 FP-Growth

FP-Growth compresses the transaction database into a frequent-pattern tree and mines the tree recursively. It often avoids large candidate-generation overhead.

### 2.3 Choosing Between Them

Apriori is conceptually simple and easy to explain. FP-Growth is often more efficient on larger datasets or lower support thresholds.

## 3. How to Evaluate Rules

### 3.1 Support

Support tells you whether the pattern is common enough to matter.

### 3.2 Confidence

Confidence tells you how often the consequent appears when the antecedent does, but it can be misleading when the consequent is common overall.

### 3.3 Lift

Lift helps detect whether the rule is stronger than chance co-occurrence under independence assumptions.

## 4. Worked Example: Support, Confidence, and Lift

Suppose there are `100` baskets with these counts:

```text
support(bread) = 30 baskets
support(butter) = 20 baskets
support(bread and butter) = 12 baskets
```

Consider the rule:

```text
bread -> butter
```

### 4.1 Compute Support

```text
support = 12 / 100 = 0.12
```

### 4.2 Compute Confidence

```text
confidence = support(bread and butter) / support(bread)
confidence = 12 / 30 = 0.40
```

### 4.3 Compute Lift

First compute support of `butter`:

```text
support(butter) = 20 / 100 = 0.20
```

Then:

```text
lift = confidence / support(butter)
lift = 0.40 / 0.20 = 2.0
```

The lift of `2.0` means bread baskets contain butter at twice the rate expected under independence.

Verification: the calculations are consistent because `12/100` gives support `0.12`, `12/30` gives confidence `0.40`, and dividing `0.40` by `0.20` yields lift `2.0`.

## 5. Common Mistakes

1. **Confidence-only ranking.** High confidence can be trivial when the consequent is already common; review lift and support together with confidence.
2. **Tiny-support overinterpretation.** Rules built on very few transactions are often unstable even if their metrics look strong; keep minimum support meaningful.
3. **Threshold collapse.** Setting support too low causes combinatorial explosion and floods the analysis with weak rules; bound the search space deliberately.
4. **Rule-as-causation thinking.** Co-occurrence does not imply causal influence; treat rules as descriptive patterns unless stronger evidence exists.
5. **Business-context omission.** Reporting mathematically interesting rules without checking whether they matter commercially or operationally reduces usefulness; connect rules to actions or hypotheses.

## 6. Practical Checklist

- [ ] Define minimum support high enough to avoid unstable or noisy rules.
- [ ] Review support, confidence, and lift together rather than in isolation.
- [ ] Cap itemset size when the search space becomes too large.
- [ ] Validate top rules against sample size and domain plausibility.
- [ ] Distinguish descriptive pattern discovery from causal claims.
- [ ] Export rule outputs with enough metadata for later review and comparison.

## 7. References

- mlxtend. 2026. *apriori*. <https://rasbt.github.io/mlxtend/user_guide/frequent_patterns/apriori/>
- mlxtend. 2026. *fpgrowth*. <https://rasbt.github.io/mlxtend/user_guide/frequent_patterns/fpgrowth/>
- Tan, Pang-Ning, Michael Steinbach, Anuj Karpatne, and Vipin Kumar. 2018. *Introduction to Data Mining* (2nd ed.). Pearson.
- Han, Jiawei, Micheline Kamber, and Jian Pei. 2011. *Data Mining: Concepts and Techniques* (3rd ed.). Morgan Kaufmann.
- mlxtend. 2026. *Association Rule Mining*. <https://rasbt.github.io/mlxtend/user_guide/frequent_patterns/association_rules/>
- Hahsler, Michael, Bettina Grün, and Kurt Hornik. 2005. arules - A Computational Environment for Mining Association Rules and Frequent Item Sets. <https://cran.r-project.org/web/packages/arules/index.html>
- Apache Spark. 2026. *FP-Growth*. <https://spark.apache.org/docs/latest/ml-frequent-pattern-mining.html>
