# Association Rules: Apriori and FP-Growth

## What it is

Methods for discovering frequent itemsets and rule relationships in transactional
data (e.g., market baskets).

## Why it matters

Association rules help explain co-occurrence patterns and drive recommendations
or bundling strategies.

## Practical workflow steps

- Convert data into transactions
- Mine frequent itemsets with a support threshold
- Generate rules with confidence and lift
- Review top rules for business relevance

## Failure modes

- Too low support causing combinatorial explosion
- Spurious rules due to small sample sizes
- Ignoring lift and relying only on confidence

## Checklist

- Support/confidence/lift thresholds defined
- Itemset size bounded
- Rules reviewed for plausibility
- Metrics reported with sample size

## References

- Fast Algorithms for Mining Association Rules (Agrawal, Srikant) — <https://doi.org/10.14778/1920841.1920842>
- Frequent Pattern Growth (Han et al.) — <https://doi.org/10.1145/335191.335372>
