# Units and Dimensional Analysis

## Key Ideas

- Every physical quantity has both a numerical value and a unit, and dropping the unit silently changes the meaning of the number.
- Dimensional analysis checks whether an equation is structurally possible by verifying that both sides have the same dimensions.
- Unit conversion is multiplication by `1` written in a different form, so a correct conversion changes the unit without changing the underlying quantity.
- Offset units such as Celsius require different handling from ratio units such as Kelvin or meters; adding or multiplying them blindly produces incorrect results.
- The safest engineering practice is to choose canonical internal units, convert at boundaries, and make units explicit in names, schemas, and APIs.

## 1. What It Is

Units and dimensional analysis provide a systematic way to reason about quantities. A quantity is not just a number; it is a number attached to a measurement unit such as meters, seconds, bytes, joules, or dollars. Dimensional analysis then asks whether expressions involving those quantities are meaningful.

This matters in both mathematics and software. In mathematics, dimensional consistency helps detect impossible formulas. In software and data systems, unit discipline prevents silent errors such as mixing milliseconds with seconds, Celsius with Kelvin, or decimal megabytes with binary mebibytes.

### 1.1 Core Definitions

- A **quantity** is a measurable property expressed as a number times a unit.
- A **unit** is the agreed reference quantity used to express measurement values, such as `m`, `s`, or `kg`.
- A **dimension** describes the physical type of a quantity, such as length `L`, mass `M`, time `T`, or temperature `Theta`.
- A **derived unit** is built from base units, such as `m/s` for speed or `kg·m/s^2` for force.
- A formula is **dimensionally consistent** if all additive terms have the same dimensions and both sides of the equation have the same overall dimensions.
- A **ratio unit** has a true zero and supports meaningful multiplication and division, such as meters or kelvin.
- An **offset unit** has an arbitrary zero point, such as degrees Celsius, so differences behave differently from absolute values.

### 1.2 Why This Matters

Unit mistakes cause real failures. NASA’s Mars Climate Orbiter was lost because one part of the system produced impulse data in pound-seconds while another expected newton-seconds, creating a mismatch between imperial and metric units. NASA’s published postmortem and lesson summary both identify the missing unit discipline directly.

Less dramatic versions happen constantly in production systems: timeouts stored in seconds but interpreted as milliseconds, cloud billing values stored in dollars but aggregated as cents, storage quotas mixed between MB and MiB, or temperatures converted incorrectly because offset units were treated like ratio units. Dimensional checks are cheap compared with the cost of these failures.

## 2. Dimensions, Units, and Consistency

### 2.1 Dimensions vs Units

Dimensions and units are related but different.

- **Dimension** answers: what kind of quantity is this?
- **Unit** answers: how is that quantity measured?

For example:

- `3 m` and `300 cm` have the same dimension `L` and represent the same quantity.
- `5 m/s` and `18 km/h` have the same derived dimension `L/T`.
- `10 J` and `10 N·m` are equal as energy units, though the notation emphasizes different interpretations.

Dimensional analysis works at the level of dimensions, not specific units. It can detect that `distance = speed * time` is plausible because `L = (L/T) * T`, but it cannot tell whether you accidentally used hours where the code expected seconds.

### 2.2 Algebra of Dimensions

Dimensions obey algebraic rules.

If `x` has dimension `L` and `t` has dimension `T`, then:

- `x / t` has dimension `L/T`
- `x * t` has dimension `L T`
- `x^2` has dimension `L^2`

Addition and subtraction are stricter:

- `x + y` is valid only if `x` and `y` have the same dimensions.
- `5 m + 3 s` is meaningless.

This gives a quick structural test for equations. For example:

```text
s = ut + (1/2)at^2
```

is dimensionally consistent because:

```text
[L] = [L/T][T] + [L/T^2][T^2]
    = [L] + [L]
```

Both terms on the right reduce to length.

### 2.3 What Dimensional Analysis Can and Cannot Do

Dimensional analysis can:

- catch impossible formulas,
- verify that conversions are plausible,
- help derive the general form of relationships,
- and force consistent handling of derived quantities.

Dimensional analysis cannot:

- determine dimensionless constants such as `1/2` or `2π`,
- distinguish between different quantities with the same dimensions, such as torque and energy, both expressible as `N·m`,
- or guarantee that a numerically consistent formula is physically correct.

## 3. Conversions and Offset Units

### 3.1 Conversion as Multiplication by One

A unit conversion should preserve the quantity while changing its representation. The key idea is to multiply by a conversion factor equal to `1`.

Example:

```text
1 km = 1000 m
```

So converting `3.2 km` to meters is:

```text
3.2 km * (1000 m / 1 km) = 3200 m
```

The numerical value changes, but the underlying quantity does not.

### 3.2 Ratio Units

For ratio units, direct scaling works.

Examples:

- `1 min = 60 s`
- `1 MB = 10^6 bytes`
- `1 MiB = 2^20 bytes`

These units support multiplication and division in the usual way because zero means absence of the quantity.

### 3.3 Offset Units

Offset units are different because their zero point is arbitrary.

For temperature:

```text
K = °C + 273.15
```

This means:

- absolute temperatures in Celsius cannot be multiplied or ratio-compared as though Celsius were a ratio unit,
- but temperature **differences** satisfy `1 °C difference = 1 K difference`.

So:

- `20 °C` is not twice as hot as `10 °C`,
- but a change of `10 °C` is the same size as a change of `10 K`.

**Why this matters:** treating offset units like ratio units is one of the easiest ways to write code that passes superficial tests but fails on edge cases.

## 4. Worked Example

Suppose a service-level objective gives a latency budget of `250 ms`, but an internal configuration store expects timeouts in seconds.

### 4.1 Correct Conversion

Start with the quantity:

```text
250 ms
```

Use the conversion factor:

```text
1 s = 1000 ms
```

Convert:

```text
250 ms * (1 s / 1000 ms) = 0.25 s
```

So the correct stored value is:

```text
0.25 s
```

### 4.2 Derived Quantity Check

Now suppose a queue drains `400` requests per second and you want to estimate how many requests can be processed within the latency budget.

Rate:

```text
400 requests / s
```

Time budget:

```text
0.25 s
```

Multiply:

```text
(400 requests / s) * (0.25 s) = 100 requests
```

The seconds cancel, leaving a count of requests.

### 4.3 Incorrect Conversion Example

If someone mistakenly stores `250` as seconds instead of milliseconds, the computed capacity becomes:

```text
(400 requests / s) * (250 s) = 100000 requests
```

This is wrong by a factor of `1000`.

Verification: `250 ms = 0.25 s`, and `400 requests/s * 0.25 s = 100 requests`. The units cancel correctly and the result has the expected dimension of a count. Correct.

## 5. Practical Engineering Patterns

### 5.1 Canonical Internal Units

Choose one internal unit per quantity type and use it everywhere inside the system.

Examples:

- durations stored internally in seconds or nanoseconds,
- money stored internally in cents,
- storage measured internally in bytes,
- temperatures stored internally in kelvin when absolute thermodynamic calculations are required.

Convert only at boundaries such as user interfaces, reports, partner APIs, and ingestion pipelines.

### 5.2 Make Units Explicit in Interfaces

Units should appear in at least one of these places:

- variable names, such as `timeout_ms` or `size_bytes`,
- schema fields and documentation,
- API contracts,
- and test cases.

A raw field name like `timeout` or `memory_limit` is weaker than `timeout_ms` or `memory_limit_mib` because it forces the reader to guess.

### 5.3 Track Binary vs Decimal Storage Units

Storage units are a common source of confusion.

- `1 kB = 1000 bytes`
- `1 KiB = 1024 bytes`
- `1 MB = 10^6 bytes`
- `1 MiB = 2^20 bytes`

These are not interchangeable. A system that mixes MB and MiB can drift noticeably at scale, especially in quotas, billing, and throughput reporting.

## 6. Pseudocode Pattern

```text
procedure convert_ms_to_s(duration_ms):
    -- convert milliseconds to seconds using a canonical ratio
    return duration_ms / 1000
```

Time: `Theta(1)` in all cases. Space: `Theta(1)` auxiliary space.

This is intentionally simple because the important part is not the arithmetic; it is the explicit contract that the input is milliseconds and the output is seconds.

## 7. Common Mistakes

1. **Silent unit mismatch.** Combining values from sources that use different units, such as milliseconds and seconds, produces results that may be numerically plausible but wrong by a constant factor.
2. **Offset-unit arithmetic.** Treating Celsius like a ratio unit leads to invalid multiplications, averages, or comparisons of absolute temperatures; convert to kelvin when absolute thermodynamic calculations matter.
3. **Double conversion.** Converting a value at ingestion and then converting it again downstream multiplies the error instead of correcting it; document where canonicalization happens and do it once.
4. **Dimension-breaking addition.** Adding quantities with different dimensions, such as bytes plus seconds or meters plus meters-per-second, produces meaningless formulas that should be rejected immediately.
5. **MB-MiB confusion.** Treating decimal and binary storage units as interchangeable introduces systematic discrepancies in capacity planning, billing, and monitoring.

## 8. Practical Checklist

- [ ] Choose one canonical internal unit for each quantity type and document it.
- [ ] Put units in variable names, schema fields, or API docs when ambiguity is possible.
- [ ] Check that every additive term in a formula has the same dimensions.
- [ ] Convert at system boundaries, not repeatedly inside the computation pipeline.
- [ ] Distinguish offset units from ratio units before averaging, scaling, or comparing values.
- [ ] Verify whether storage quantities use decimal (`MB`) or binary (`MiB`) units.
- [ ] Add tests with deliberately mismatched units to confirm that validation catches them.

## References

- Bureau International des Poids et Mesures. 2025. *The International System of Units (SI), 9th edition, updated 2025*. <https://www.bipm.org/en/publications/si-brochure>
- NIST. 2008. *Guide for the Use of the International System of Units (SI), Special Publication 811*. <https://physics.nist.gov/cuu/pdf/sp811.pdf>
- NIST. 2019. *The International System of Units (SI), NIST SP 330-2019*. <https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.330-2019.pdf>
- NASA. 1999. *Mars Climate Orbiter Mishap Investigation Board Phase I Report*. <https://llis.nasa.gov/llis_lib/pdf/1009464main1_0641-mr.pdf>
- NASA. *Mars Climate Orbiter Mishap Investigation Board lesson summary*. <https://llis.nasa.gov/lesson/641>
- Physics LibreTexts. *Units and dimensions*. <https://phys.libretexts.org/Bookshelves/University_Physics/Book%3A_Introductory_Physics_-_Building_Models_to_Describe_Our_World_%28Martin_Neary_Rinaldo_and_Woodman%29/02%3A_Comparing_Model_and_Experiment/2.02%3A_Units_and_dimensions>
- Physics LibreTexts. *Dimensional Analysis*. <https://phys.libretexts.org/Workbench/PH_245_Textbook_V2/01%3A_Module_0_-_Mathematical_Foundations/1.01%3A_Objective_0.a./1.1.04%3A_Dimensional_Analysis>
