# Boolean Algebra and Bit Operations

## Key Ideas

- Boolean algebra provides the formal rules for reasoning about true or false values, while bit operations apply the same logic to fixed-width binary representations.
- Bitwise operations are implementation-level tools for masks, flags, packed state, hashing primitives, and arithmetic tricks, but they are safe only when representation details are understood.
- The laws of Boolean algebra explain why expressions can be simplified, reordered, or converted into branch-free tests.
- Shifts, masks, and two's-complement conventions are precise operations, not informal shortcuts, so language and width assumptions must be stated.
- Bit manipulation is often faster and more memory-efficient than object-heavy representations, but only when the resulting invariants remain readable and correct.

## 1. What It Is

Boolean algebra studies expressions built from the values `true` and `false` using operations such as `and`, `or`, and `not`. A **bit** is a binary digit taking value `0` or `1`. Bitwise operators lift Boolean reasoning to each position of a machine word.

This topic matters because many systems tasks are fundamentally bit-level:

- permission flags,
- network protocol headers,
- compression formats,
- cryptographic primitives,
- Bloom filters,
- and SIMD-friendly packed state.

### 1.1 Core definitions

- `x and y` is true only when both operands are true.
- `x or y` is true when at least one operand is true.
- `not x` flips truth value.
- `x xor y` is true when exactly one operand is true.
- A **mask** is a bit pattern used to test, set, clear, or toggle selected bit positions.

## 2. Boolean Algebra Laws

The reason Boolean algebra matters is that it gives sound rewrite rules.

### 2.1 Fundamental laws

For Boolean values `x`, `y`, and `z`:

- Identity: `x and true = x`, `x or false = x`
- Domination: `x and false = false`, `x or true = true`
- Idempotence: `x and x = x`, `x or x = x`
- Complement: `x and not x = false`, `x or not x = true`
- Commutativity: `x and y = y and x`, `x or y = y and x`
- Distributivity: `x and (y or z) = (x and y) or (x and z)`
- De Morgan: `not (x and y) = (not x) or (not y)` and `not (x or y) = (not x) and (not y)`

These laws justify expression simplification and hardware logic minimization.

### 2.2 From logic to bits

For fixed-width bit strings, bitwise `and`, `or`, `xor`, and `not` apply independently to each position. For example:

```text
1101 and 1011 = 1001
1101 xor 1011 = 0110
```

The logic is identical; only the operands are vectors of bits instead of single truth values.

## 3. Bit Operations in Practice

### 3.1 Masks and flags

Suppose bit `k` represents whether capability `k` is enabled.

- Test bit `k`: `flags and (1 << k)`
- Set bit `k`: `flags or (1 << k)`
- Clear bit `k`: `flags and not (1 << k)`
- Toggle bit `k`: `flags xor (1 << k)`

This representation is compact and makes union-like operations cheap.

### 3.2 Shifts and representation

A left shift by one position multiplies an unsigned integer by `2` when no overflow occurs. A right shift by one position divides by `2` with rounding behavior that depends on signedness and language rules.

Because languages differ on signed shifts and overflow, implementation-aware writing must say whether the value is unsigned, what word width is assumed, and whether overflow is permitted.

### 3.3 Two's complement intuition

Most modern systems represent signed integers with **two's complement**. In width `w`, negation is performed as `not x + 1` modulo `2^w`.

This matters because bit tricks that seem purely algebraic are actually representation-dependent.

## 4. Worked Example

Assume an 8-bit permission byte where:

- bit `0` = read
- bit `1` = write
- bit `2` = execute
- bit `5` = audit

Start with:

```text
flags = 10100100
```

Reading from right to left, bits `2`, `5`, and `7` are set.

### 4.1 Test whether execute is enabled

Execute is bit `2`, so the mask is:

```text
00000100
```

Now compute:

```text
10100100
and 00000100
=   00000100
```

The result is nonzero, so execute is enabled.

### 4.2 Set write permission

Write is bit `1`, so OR with:

```text
00000010
```

```text
10100100
or  00000010
=   10100110
```

Now write is enabled.

### 4.3 Clear audit permission

Audit is bit `5`, so clear with the complement of `00100000`:

```text
not 00100000 = 11011111
```

```text
10100110
and 11011111
=   10000110
```

Audit is now disabled while the other set bits remain set.

Verification: the final byte `10000110` has bits `1`, `2`, and `7` enabled, exactly matching the intended operations of test execute, set write, and clear audit.

## 5. Pseudocode Pattern

```text
procedure update_flag(flags, bit_index, action):
    mask = 1 << bit_index

    if action == "set":
        return flags or mask
    if action == "clear":
        return flags and not mask
    if action == "toggle":
        return flags xor mask
    return flags
```

Time: `Theta(1)` worst case on a fixed-width machine word. Space: `Theta(1)`.

The crucial implementation detail is not the syntax but the assumption that `flags` has a known width and the shift is valid for `bit_index`.

## 6. Common Mistakes

1. **Width ambiguity.** Using bit tricks without naming the integer width can silently change behavior across platforms or languages; state the word size or use fixed-width types.
2. **Signed-shift confusion.** Assuming right shift on signed values always performs arithmetic or logical shifting leads to portability bugs; consult the language definition and prefer unsigned values when you mean raw bits.
3. **Mask inversion mistakes.** Writing `not mask` without constraining width can set unintended higher bits in languages with unbounded integers; intersect with the intended width when necessary.
4. **Boolean-bit conflation.** Treating logical operators and bitwise operators as interchangeable can produce wrong results on multi-bit values; use Boolean logic for predicates and bitwise logic for packed representations.
5. **Unreadable cleverness.** Compressing state into bits without documenting what each bit means makes maintenance and auditing harder; define the bit layout explicitly next to the code.

## 7. Practical Checklist

- [ ] State the bit width and signedness assumptions before discussing a bit trick.
- [ ] Name each flag position or mask instead of using unexplained literals.
- [ ] Use Boolean algebra laws to justify expression rewrites.
- [ ] Verify that shifts cannot exceed the word width.
- [ ] Prefer unsigned representations when the operation is about raw bits rather than arithmetic sign.
- [ ] Add a worked binary example when documenting masks or protocol fields.

## 8. References

- Bryant, Randal E., and David R. O'Hallaron. 2021. *Computer Systems: A Programmer's Perspective* (4th ed.). Pearson. <https://www.pearson.com/en-us/subject-catalog/p/computer-systems-a-programmers-perspective/P200000003479>
- Warren, Henry S. 2013. *Hacker's Delight* (2nd ed.). Addison-Wesley. <https://www.oreilly.com/library/view/hackers-delight-second/9780133084993/>
- Nisan, Noam, and Shimon Schocken. 2021. *The Elements of Computing Systems* (2nd ed.). MIT Press. <https://mitpress.mit.edu/9780262539807/the-elements-of-computing-systems/>
- ISO/IEC. 2011. *Programming Languages — C (N1570 Draft)*. <https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf>
- Oracle. 2025. *Java Language Specification, Java SE 25 Edition*. <https://docs.oracle.com/javase/specs/jls/se25/html/>
- Intel. 2025. *Intel 64 and IA-32 Architectures Software Developer's Manual*. <https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html>
