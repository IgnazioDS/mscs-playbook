# Data Understanding and Profiling

## What it is

Systematic exploration of data distributions, missingness, types, and
relationships before modeling.

## Why it matters

Profiling exposes data quality risks and guides cleaning and feature decisions.

## Practical workflow steps

- Inspect schema and basic stats
- Quantify missingness and duplicates
- Visualize distributions and outliers
- Check target balance (if supervised)

## Failure modes

- Skipping profiling and discovering issues late
- Misinterpreting mixed data types
- Ignoring class imbalance

## Checklist

- Summary stats for numeric columns
- Missingness counts and rates
- Category cardinalities and top values
- Sanity checks on ranges and units

## References

- Exploratory Data Analysis (Tukey) — <https://www.wiley.com/en-us/Exploratory+Data+Analysis-p-9780201076165>
- pandas DataFrame.describe — <https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.describe.html>
