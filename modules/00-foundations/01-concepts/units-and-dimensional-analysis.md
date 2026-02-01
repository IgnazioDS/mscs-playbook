# Units and Dimensional Analysis

## What it is
A discipline for tracking units and dimensional consistency across formulas and
systems.

## Why it matters
Many production incidents come from silent unit mismatches (ms vs s, MB vs MiB,
USD vs cents). Unit checks prevent expensive errors.

## Core ideas
- Every quantity has a unit
- Equations must be dimensionally consistent
- Use canonical internal units and convert at boundaries

## Example
Latency budgets in milliseconds should be stored in a single unit and converted
only at the UI boundary.

## Pitfalls
- Mixing data sources with different unit conventions
- Ignoring offset units (e.g., Celsius vs Kelvin)
- Converting twice or not at all in ETL pipelines

## References
- Thompson, *Dimensional Analysis and Its Applications*
- NASA unit conversion failure case studies
