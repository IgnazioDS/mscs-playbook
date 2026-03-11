# Sequence Models: RNN, LSTM, and GRU

## Key Ideas

- Recurrent sequence models process tokens one step at a time while carrying a hidden state that summarizes past context.
- Vanilla recurrent neural networks struggle with long-range dependency learning because gradients can vanish or explode during training.
- LSTM and GRU architectures introduce gates that control memory retention and update flow, improving practical sequence learning.
- Recurrent models capture order explicitly, which made them important for tagging, sequence classification, and early neural language modeling.
- Even though transformers dominate many modern tasks, recurrent models remain useful for understanding sequence modeling tradeoffs and low-latency streaming scenarios.

## 1. Why Recurrent Models Were Important

Classical vector models ignore token order, and n-grams use only a short fixed history. Recurrent neural networks address both limits by reading a sequence token by token and updating a hidden state:

```text
h_t = f(x_t, h_{t-1})
```

This lets the model represent a context summary that changes as new tokens arrive.

## 2. Core Variants

### 2.1 Vanilla RNN

A vanilla RNN updates hidden state with a simple recurrent transformation. It is conceptually clean but hard to train on long dependencies.

### 2.2 LSTM

An **LSTM** uses gates to decide:

- what to forget
- what to write
- what to expose

This helps preserve useful information over longer spans.

### 2.3 GRU

A **GRU** simplifies the gating structure while keeping much of the same practical benefit.

## 3. Training Concerns

Recurrent models are usually trained with backpropagation through time. Important concerns include:

- exploding gradients
- vanishing gradients
- sequence padding and masking
- teacher forcing in sequence prediction settings

Gradient clipping is a common safeguard when exploding gradients appear.

## 4. Worked Example: Sentiment Signal Through a Sequence

Suppose a model reads:

```text
"the service was not good"
```

Assume a simplified hidden-state interpretation where positive values imply positive sentiment.

### 4.1 Stepwise Intuition

```text
after "the"      -> h_1 = 0.0
after "service"  -> h_2 = 0.1
after "was"      -> h_3 = 0.1
after "not"      -> h_4 = -0.4
after "good"     -> h_5 = -0.2
```

The important point is that the meaning of `"good"` depends on the prior state that already contains the negation cue from `"not"`.

### 4.2 Why Gated Models Help

If the sequence were much longer, a vanilla RNN might fail to preserve the negation effect by the time the final token arrives. LSTM and GRU gating make it easier to keep the relevant context active.

Verification: the hidden state after `"not"` changes the interpretation of `"good"`, which is exactly the kind of ordered dependency recurrent models were built to capture.

## 5. When Recurrent Models Still Make Sense

Recurrent models are still worth considering when:

- data is sequential and streaming
- model size must stay moderate
- training resources are limited
- strict left-to-right online processing matters

They are often less attractive than transformers when long-range dependencies, transfer learning, and large-scale parallel training are central.

## 6. Common Mistakes

1. **Ignoring sequence length.** Long sequences can destabilize training or hide information in vanilla RNNs; inspect length distributions and truncate or batch carefully.
2. **No gradient control.** Training without clipping or monitoring can let exploding gradients derail optimization; add safeguards early.
3. **Padding leakage.** Allowing padded positions to influence learning distorts sequence behavior; use masking or packed sequences properly.
4. **Baseline neglect.** Deploying recurrent models without comparing against simpler sparse or n-gram baselines obscures whether sequence modeling was necessary.
5. **Context overclaiming.** Assuming recurrent state always preserves long dependencies ignores practical limitations; verify on examples that require distant context.

## 7. Practical Checklist

- [ ] Measure sequence length distribution before choosing architecture settings.
- [ ] Start with a simple recurrent baseline before adding complexity.
- [ ] Use masking or packed batches for padded examples.
- [ ] Monitor gradient norms and apply clipping when needed.
- [ ] Evaluate on cases that explicitly require ordered context.
- [ ] Compare recurrent models against transformer and non-neural baselines on the same split.

## 8. References

- Elman, Jeffrey L. "Finding Structure in Time." 1990. <https://crl.ucsd.edu/~elman/Papers/fsit.pdf>
- Hochreiter, Sepp, and Jurgen Schmidhuber. "Long Short-Term Memory." 1997. <https://www.bioinf.jku.at/publications/older/2604.pdf>
- Cho, Kyunghyun, et al. "Learning Phrase Representations using RNN Encoder-Decoder for Statistical Machine Translation." 2014. <https://arxiv.org/abs/1406.1078>
- Goodfellow, Ian, Yoshua Bengio, and Aaron Courville. *Deep Learning*. MIT Press, 2016. <https://www.deeplearningbook.org/>
- Graves, Alex. *Supervised Sequence Labelling with Recurrent Neural Networks*. Springer, 2012.
- Jurafsky, Daniel, and James H. Martin. *Speech and Language Processing* (3rd draft). <https://web.stanford.edu/~jurafsky/slp3/>
- Olah, Christopher. "Understanding LSTM Networks." <https://colah.github.io/posts/2015-08-Understanding-LSTMs/>
