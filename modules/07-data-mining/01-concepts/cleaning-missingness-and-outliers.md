# Cleaning, Missingness, and Outliers

## What it is

Techniques for handling missing values and outliers to stabilize downstream
mining and modeling.

## Why it matters

Unaddressed missingness and outliers can dominate distance metrics and bias
pattern discovery.

## Practical workflow steps

- Quantify missingness by column
- Choose imputation strategy (median/mode)
- Flag or cap outliers (IQR/winsorization)
- Recheck distributions after cleaning

## Failure modes

- Imputing without understanding missingness mechanism
- Over-aggressive outlier removal removing real signal
- Failing to log cleaning steps

## Checklist

- Missingness report with rates
- Imputation strategy per column
- Outlier thresholds documented
- Before/after distribution checks

## References

- Little and Rubin: Statistical Analysis with Missing Data — <https://www.wiley.com/en-us/Statistical+Analysis+with+Missing+Data%2C+3rd+Edition-p-9781119482260>
- scikit-learn SimpleImputer — <https://scikit-learn.org/stable/modules/generated/sklearn.impute.SimpleImputer.html>
