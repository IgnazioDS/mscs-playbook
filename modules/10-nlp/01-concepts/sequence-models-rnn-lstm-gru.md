# Sequence Models: RNN, LSTM, GRU

## Overview
Recurrent models process sequences by maintaining hidden state across tokens.

## Why it matters
They model order and context, enabling tagging and sequence prediction tasks.

## Key ideas
- RNNs suffer from vanishing gradients
- LSTM/GRU add gates to preserve memory
- Teacher forcing during training

## Practical workflow
- Tokenize and pad sequences
- Choose RNN variant and hidden size
- Monitor overfitting and gradient stability

## Failure modes
- Overfitting on small datasets
- Exploding/vanishing gradients
- Poor handling of long dependencies

## Checklist
- Validate sequence length distribution
- Use gradient clipping
- Compare against simpler baselines

## References
- Hochreiter & Schmidhuber (LSTM) — https://www.bioinf.jku.at/publications/older/2604.pdf
- GRU — https://arxiv.org/abs/1406.1078
