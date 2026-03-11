# Text Preprocessing and Tokenization

## Key Ideas

- Text preprocessing converts raw text into a stable representation so later models do not waste capacity on avoidable noise.
- Tokenization splits text into units such as words, subwords, or characters, and that choice directly affects vocabulary size, context handling, and model compatibility.
- Preprocessing should preserve task-relevant signals such as negation, casing, punctuation, or entity boundaries instead of applying generic cleanup blindly.
- The preprocessing and tokenization pipeline must be identical across training, validation, and inference or evaluation becomes misleading.
- Tokenization is not merely string splitting; it is part of the modeling assumption because it defines what the model can observe and count.

## 1. Why Preprocessing Exists

Raw text is messy. It contains inconsistent whitespace, encoding artifacts, punctuation variation, emojis, casing changes, typos, and markup. Preprocessing standardizes those surface forms so the model focuses on meaningful variation instead of accidental formatting differences.

The right amount of preprocessing depends on the task. A sentiment model may need punctuation and negation, while a keyword search baseline may benefit from lighter normalization and stopword handling. The point is not maximal cleanup. The point is controlled representation.

## 2. Core Definitions

- **Normalization** changes raw text into a more consistent form, such as lowercasing or Unicode normalization.
- **Tokenization** splits text into units the model will treat as symbols.
- A **vocabulary** is the set of token types the model can represent directly.
- An **out-of-vocabulary token** is a token not present in the vocabulary.
- A **subword tokenizer** breaks words into smaller pieces so rare or unseen words can still be represented compositionally.

## 3. Common Tokenization Choices

### 3.1 Word Tokenization

Word tokenization is intuitive and works well for classical pipelines, but it struggles with rare words, morphology, and unseen spellings.

### 3.2 Character Tokenization

Character tokenization avoids out-of-vocabulary failures, but sequences become longer and semantic units become harder to learn.

### 3.3 Subword Tokenization

Subword tokenization balances the tradeoff by representing common words as single units and rare words as smaller pieces. This is why it is common in modern neural NLP systems.

## 4. Worked Example: Build a Small Pipeline

Suppose the raw sentence is:

```text
"I can't believe   ACME-42 shipped late again!"
```

Assume the task is sentiment or service triage, so we want to preserve negation and product identifiers.

### 4.1 Normalization

Apply:

- collapse repeated whitespace
- lowercase alphabetic text
- keep apostrophes and hyphens because they carry signal here

Result:

```text
"i can't believe acme-42 shipped late again!"
```

### 4.2 Word-Level Tokenization

One reasonable tokenization is:

```text
["i", "can't", "believe", "acme-42", "shipped", "late", "again", "!"]
```

### 4.3 What a Bad Pipeline Would Do

If the pipeline removed punctuation, apostrophes, and hyphens too aggressively, it might produce:

```text
["i", "can", "t", "believe", "acme", "42", "shipped", "late", "again"]
```

Now the negation cue in `"can't"` is damaged, and the product identifier is fragmented.

Verification: the better pipeline preserves both the negative expression and the product token, which are likely to matter for downstream classification.

## 5. Choosing a Pipeline in Practice

Ask three questions:

1. Which surface cues matter for the task?
2. Which model family will consume the tokens?
3. Which tokenizer was used for any pretrained model you plan to reuse?

If you use a pretrained transformer, its tokenizer is effectively part of the model. Replacing it casually usually harms performance because embeddings and token boundaries no longer align.

## 6. Common Mistakes

1. **Over-normalization.** Removing negations, punctuation, or case distinctions can erase signal; keep only the transformations that support the task.
2. **Train-test mismatch.** Using different preprocessing logic during inference invalidates evaluation; ship one shared pipeline for all stages.
3. **Tokenizer-model mismatch.** Feeding text through a different tokenizer than the pretrained model expects breaks the representation; use the model-aligned tokenizer unless there is a deliberate retraining plan.
4. **Vocabulary leakage.** Building vocabularies on the full dataset leaks validation information; fit vocabulary statistics on training data only.
5. **Language-blind assumptions.** Applying English-specific heuristics to multilingual or morphologically rich text degrades token quality; adapt preprocessing to the language and script.

## 7. Practical Checklist

- [ ] Define which text cues must be preserved for the task.
- [ ] Use the same preprocessing code in training, evaluation, and inference.
- [ ] Fit vocabularies and normalization statistics on training data only.
- [ ] Inspect tokenization on real examples before training.
- [ ] Keep tokenizer choice aligned with the model family you will use.
- [ ] Version the pipeline so experiments remain reproducible.

## 8. References

- Jurafsky, Daniel, and James H. Martin. *Speech and Language Processing* (3rd draft). <https://web.stanford.edu/~jurafsky/slp3/>
- Manning, Christopher D., Prabhakar Raghavan, and Hinrich Schutze. *Introduction to Information Retrieval*. Cambridge University Press, 2008. <https://nlp.stanford.edu/IR-book/>
- Sennrich, Rico, Barry Haddow, and Alexandra Birch. "Neural Machine Translation of Rare Words with Subword Units." 2016. <https://aclanthology.org/P16-1162/>
- Kudo, Taku, and John Richardson. "SentencePiece." 2018. <https://aclanthology.org/D18-2012/>
- spaCy. "Tokenization." <https://spacy.io/usage/linguistic-features#tokenization>
- Hugging Face. "Tokenizers Summary." <https://huggingface.co/docs/transformers/tokenizer_summary>
- Unicode Consortium. "Unicode Standard Annex #15: Unicode Normalization Forms." <https://unicode.org/reports/tr15/>
