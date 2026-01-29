# Vision Transformers and Modern Backbones

## Overview
Vision transformers (ViTs) and modern backbones use attention to model global
context and scale well with data.

## Why it matters
Attention-based backbones often outperform CNNs on large datasets and enable
strong transfer learning.

## Key ideas
- Patch embeddings convert images into token sequences
- Self-attention captures long-range dependencies
- Hybrid models combine convolutions with attention
- Scaling data and compute improves performance

## Practical workflow
- Start with pretrained weights for small datasets
- Tune patch size and input resolution
- Use fine-tuning with lower learning rates
- Monitor memory usage and batch size constraints

## Failure modes
- Data-hungry training requirements
- High memory usage for large resolutions
- Instability without warmup schedules
- Overfitting on small datasets

## Checklist
- Track GPU memory and throughput
- Use regularization (dropout, stochastic depth)
- Compare CNN baselines for cost/benefit
- Validate performance on distribution shifts

## References
- Vision Transformer — https://arxiv.org/abs/2010.11929
- Swin Transformer — https://arxiv.org/abs/2103.14030
