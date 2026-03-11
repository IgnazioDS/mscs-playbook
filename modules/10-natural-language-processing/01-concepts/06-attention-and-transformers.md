# Attention and Transformers

## Key Ideas

- Attention lets a model weight different input positions dynamically instead of compressing all earlier context into one recurrent hidden state.
- Transformers build on self-attention to model token interactions in parallel, which improves training efficiency and long-range context handling.
- Positional information is necessary because self-attention alone does not encode sequence order.
- Multi-head attention allows the model to learn different interaction patterns across the same sequence.
- Transformers became dominant because they scale well with data and compute, not because recurrence stopped being conceptually useful.

## 1. Why Attention Changed NLP

Recurrent models pass information step by step, which makes long dependencies harder to preserve and training harder to parallelize. Attention addresses that by letting the model look directly at the most relevant tokens when producing a representation.

Instead of asking one hidden state to remember everything, the model computes which earlier tokens matter for the current decision and assigns them weights.

## 2. Self-Attention Intuition

In self-attention, each token creates:

- a **query**, which asks what information it needs
- a **key**, which indicates what information it offers
- a **value**, which carries the content to combine

Attention weights are larger when a query is strongly aligned with a key. The resulting token representation is a weighted combination of value vectors.

## 3. Transformer Building Blocks

### 3.1 Multi-Head Attention

Multiple attention heads allow the model to learn different relation types, such as syntactic agreement, entity references, or local phrase structure.

### 3.2 Positional Encoding

Because self-attention is permutation-invariant without extra information, transformers add positional signals so token order remains meaningful.

### 3.3 Feed-Forward Layers

After attention mixes context, position-wise feed-forward layers transform the representation further.

## 4. Worked Example: Attention over a Short Sentence

Suppose the sentence is:

```text
"the cat chased the mouse"
```

Assume we are computing the representation for `"chased"` and the model gives these attention weights:

```text
the(1)   -> 0.05
cat      -> 0.35
chased   -> 0.10
the(2)   -> 0.05
mouse    -> 0.45
```

### 4.1 Interpretation

The verb attends strongly to `cat` and `mouse`, which makes sense because they are the main semantic arguments.

### 4.2 Weighted Combination

If the corresponding value vectors are `v_1 ... v_5`, then the contextual representation for `"chased"` is:

```text
0.05*v_1 + 0.35*v_2 + 0.10*v_3 + 0.05*v_4 + 0.45*v_5
```

This gives the token a context-aware representation shaped by the full sentence.

Verification: the largest attention weights land on the subject and object tokens, so the representation for `"chased"` captures the most relevant local semantic structure.

## 5. Why Transformers Scaled Better

Transformers parallelize training across positions more effectively than recurrent models because token representations within a layer can be computed together. That made it practical to train much larger models on much larger corpora.

The tradeoff is that self-attention has significant memory and compute cost as sequence length grows. That is why context-window engineering and efficient attention variants remain important.

## 6. Common Mistakes

1. **Attention-as-explanation.** Treating attention weights as a complete explanation of model reasoning overstates what they show; use them as clues, not proofs.
2. **Ignoring position.** Forgetting that self-attention needs positional information leads to conceptual errors about order sensitivity; include positional encoding in the mental model.
3. **Scale blindness.** Assuming transformers are always cheap enough for long documents ignores attention cost growth; budget for context length and latency explicitly.
4. **Task leakage.** Fine-tuning or prompting without a held-out evaluation set can make transformer performance look stronger than it is; preserve evaluation rigor.
5. **Architecture worship.** Replacing simpler baselines automatically with transformers can hide unnecessary complexity; compare against sparse, embedding, or recurrent baselines first.

## 7. Practical Checklist

- [ ] Understand which task dependencies require long-range context.
- [ ] Keep tokenizer and positional assumptions aligned with the chosen model.
- [ ] Measure latency and memory alongside accuracy.
- [ ] Validate transformer gains against simpler baselines on the same split.
- [ ] Inspect failure cases involving truncation and long context.
- [ ] Treat attention visualizations as diagnostic aids rather than full explanations.

## 8. References

- Vaswani, Ashish, et al. "Attention Is All You Need." 2017. <https://arxiv.org/abs/1706.03762>
- Bahdanau, Dzmitry, Kyunghyun Cho, and Yoshua Bengio. "Neural Machine Translation by Jointly Learning to Align and Translate." 2015. <https://arxiv.org/abs/1409.0473>
- Rush, Alexander. "The Annotated Transformer." <https://nlp.seas.harvard.edu/2018/04/03/attention.html>
- Goldberg, Yoav. "A Primer on Neural Network Models for Natural Language Processing." 2016. <https://arxiv.org/abs/1510.00726>
- Jurafsky, Daniel, and James H. Martin. *Speech and Language Processing* (3rd draft). <https://web.stanford.edu/~jurafsky/slp3/>
- Wolf, Thomas, et al. "Transformers: State-of-the-Art Natural Language Processing." 2020. <https://aclanthology.org/2020.emnlp-demos.6/>
- Tay, Yi, Mostafa Dehghani, Dara Bahri, and Donald Metzler. "Efficient Transformers: A Survey." 2022. <https://arxiv.org/abs/2009.06732>
