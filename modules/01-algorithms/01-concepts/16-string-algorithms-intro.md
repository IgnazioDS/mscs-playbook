# String Algorithms Intro

## Key Ideas

- String algorithms exploit repeated structure in text, so preprocessing the pattern or the text can avoid re-checking characters that are already understood.
- Prefixes, suffixes, and overlaps are the central structural objects because they determine how far an algorithm can shift after a mismatch.
- Exact matching algorithms differ mainly in where they invest work: naive scanning spends no preprocessing time, KMP preprocesses the pattern, and suffix-based methods preprocess the text.
- Hash-based string methods can be very fast in the expected case, but collision handling determines whether correctness and worst-case guarantees are preserved.
- Choosing a string algorithm depends on query volume, alphabet size, update frequency, and whether the workload is one pattern in many texts, many patterns in one text, or repeated substring queries.

## 1. What It Is

String algorithms are algorithms for processing sequences of symbols drawn from an alphabet, such as characters in a document, DNA bases in a genome, or tokens in a log stream. The most common task is **pattern matching**: deciding whether a pattern string occurs in a text string and, if so, where.

### 1.1 Core Definitions

- A **string** is a finite sequence of symbols from an alphabet.
- A **text** is the larger string being searched.
- A **pattern** is the smaller string we want to find.
- A **prefix** of a string is a substring that starts at the first character.
- A **suffix** of a string is a substring that ends at the last character.
- A **proper prefix** or **proper suffix** is a prefix or suffix that is not the whole string.
- A **border** is a nonempty substring that is both a prefix and a suffix.

### 1.2 Why This Matters

Many practical systems spend real compute on string processing: search engines, intrusion detection, bioinformatics, editors, version-control tooling, and telemetry pipelines. A quadratic worst-case matcher may be acceptable on tiny inputs, but it becomes a bottleneck on large corpora or repeated queries.

## 2. Main Exact-Matching Strategies

### 2.1 Naive Scanning

The simplest algorithm aligns the pattern at every possible text position and compares characters one by one.

- Time: `O(nm)` worst case for text length `n` and pattern length `m`.
- Space: `Theta(1)` auxiliary space.

It is easy to write, but it repeats work after mismatches because it ignores overlap structure in the pattern.

### 2.2 Knuth-Morris-Pratt

The Knuth-Morris-Pratt (KMP) algorithm preprocesses the pattern into a table of fallback lengths, often called the prefix-function or longest-prefix-suffix table. When a mismatch occurs, the table tells the algorithm how much of the matched prefix can still be reused.

- Time: `Theta(n + m)` worst case.
- Space: `Theta(m)` auxiliary space.

KMP is useful when exact worst-case guarantees matter and the pattern is reused across multiple texts.

### 2.3 Rabin-Karp and Rolling Hashes

Rabin-Karp converts substrings into hash values so that most alignments can be compared numerically before any character-by-character verification.

- Time: `Theta(n + m)` expected case with well-behaved hashing and verification on hash hits.
- Time: `O(nm)` worst case if collisions are adversarial or verification is triggered too often.
- Space: `Theta(1)` auxiliary space beyond the rolling-hash state.

This approach is especially attractive when matching many patterns of the same length or when integrating with other hash-based indexing logic.

## 3. Text Indexing for Repeated Queries

### 3.1 Tries and Prefix Search

A **trie** stores many strings by sharing common prefixes. It is useful when the main operation is prefix lookup or dictionary matching rather than searching one long text.

### 3.2 Suffix Arrays and Suffix Trees

If one long text will be queried many times, it can be worth preprocessing the text itself rather than each pattern.

- A **suffix array** stores the starting positions of all suffixes in sorted order.
- A **suffix tree** stores all suffixes in a compressed trie-like structure.

These structures support repeated substring queries efficiently, but they increase implementation complexity and memory cost compared with KMP or Rabin-Karp.

## 4. Worked Example

Use KMP to find pattern:

```text
P = "ababd"
```

inside text:

```text
T = "ababcabcabababd"
```

### 4.1 Build the Prefix Table

For `P = a b a b d`, compute the longest proper prefix that is also a suffix for each prefix:

```text
index:   0 1 2 3 4
char:    a b a b d
lps:     0 0 1 2 0
```

Explanation:

- At index `0`, only `"a"` exists, so `lps[0] = 0`.
- At index `2`, prefix `"aba"` has border `"a"`, so `lps[2] = 1`.
- At index `3`, prefix `"abab"` has border `"ab"`, so `lps[3] = 2`.
- At index `4`, `"ababd"` has no nonempty border, so `lps[4] = 0`.

### 4.2 Scan the Text

Track text index `i` and pattern index `j`.

1. `i = 0..3`: characters match as `a b a b`, so `j = 4`.
2. At `i = 4`, text has `c` but pattern expects `d`. Use the table:

```text
j = lps[3] = 2
```

3. Compare again at the same text position `i = 4`. Pattern index `2` expects `a`, but text still has `c`, so:

```text
j = lps[1] = 0
```

4. Resume scanning. After several character checks, matching restarts at text index `10`.
5. From `T[10..14] = "ababd"`, all characters match and `j` reaches `5`, the pattern length.

So the pattern occurs starting at index:

```text
10
```

Verification: the substring `T[10..14]` is exactly `"ababd"`, matching the pattern, so the reported start index `10` is correct.

## 5. Pseudocode Pattern

```text
procedure kmp_search(text, pattern, lps):
    i = 0
    j = 0

    while i < length(text):
        if text[i] == pattern[j]:
            i = i + 1
            j = j + 1
            if j == length(pattern):
                return i - j
        else if j > 0:
            j = lps[j - 1]
        else:
            i = i + 1

    return -1
```

Time: `Theta(n + m)` worst case, assuming the prefix table is built in `Theta(m)` worst-case time. Space: `Theta(m)` auxiliary space for the prefix table.

## 6. Common Mistakes

1. **Substring-structure neglect.** Rechecking characters from scratch after every mismatch wastes the very overlap information that linear-time algorithms use; compute and exploit pattern structure when repeated mismatches are expected.
2. **Hash-without-verification.** Returning a match immediately after a rolling-hash collision can produce false positives; verify candidate matches unless the hash family and application justify a probabilistic answer.
3. **Wrong-workload choice.** Building a suffix structure for one query or using naive scanning for millions of repeated queries misallocates preprocessing effort; match the algorithm to the query pattern.
4. **Indexing off-by-one errors.** Prefix tables, substring intervals, and match-start calculations are sensitive to indexing conventions; trace a concrete example before trusting the implementation.
5. **Alphabet-model blindness.** Ignoring alphabet size and encoding details can break assumptions about character comparisons, memory layout, or hashing; define the symbol model before analyzing performance.

## 7. Practical Checklist

- [ ] State whether the workload is one pattern in one text, one pattern in many texts, or many patterns in one text.
- [ ] Use naive scanning only when input sizes are small enough that worst-case `O(nm)` behavior is harmless.
- [ ] Prefer KMP when exact matching and linear worst-case time matter.
- [ ] Use rolling hashes only when collision handling and verification rules are explicit.
- [ ] Consider tries or suffix-based indexing when the same corpus will be queried repeatedly.
- [ ] Validate the algorithm on examples with repeated prefixes, not just random-looking strings.

## 8. References

- Cormen, Thomas H., Charles E. Leiserson, Ronald L. Rivest, and Clifford Stein. 2022. *Introduction to Algorithms* (4th ed.). MIT Press. <https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/>
- Gusfield, Dan. 1997. *Algorithms on Strings, Trees, and Sequences*. Cambridge University Press.
- Crochemore, Maxime, Christophe Hancart, and Thierry Lecroq. 2007. *Algorithms on Strings*. Cambridge University Press.
- Knuth, Donald E., James H. Morris, and Vaughan R. Pratt. 1977. Fast Pattern Matching in Strings. *SIAM Journal on Computing* 6(2): 323-350. <https://doi.org/10.1137/0206024>
- Princeton University. 2026. *KMP (Algorithms, 4th ed.)*. <https://algs4.cs.princeton.edu/code/javadoc/edu/princeton/cs/algs4/KMP.html>
- Princeton University. 2026. *Substring Search*. <https://algs4.cs.princeton.edu/53substring/>
