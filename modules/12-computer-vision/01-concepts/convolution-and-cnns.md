# Convolution and CNNs

## Overview
Convolutional neural networks (CNNs) learn spatial filters that detect patterns
like edges, textures, and objects.

## Why it matters
CNNs remain strong baselines for vision tasks with efficient inference and
well-understood training behavior.

## Key ideas
- Convolution applies shared filters across the image
- Pooling reduces spatial resolution and increases invariance
- Feature hierarchies capture low-to-high level patterns
- Batch normalization stabilizes training

## Practical workflow
- Choose a backbone (ResNet, MobileNet) based on latency needs
- Start with pretrained weights when possible
- Fine-tune with smaller learning rates
- Track receptive field vs object size

## Failure modes
- Overfitting on small datasets
- Vanishing gradients in deep stacks
- Poor performance on long-range dependencies
- Latency spikes with large feature maps

## Checklist
- Measure throughput on target hardware
- Verify input normalization matches pretrained weights
- Monitor training with validation curves
- Use mixed precision to speed up training

## References
- AlexNet — https://papers.nips.cc/paper/2012/hash/c399862d3b9d6b76c8436e924a68c45b-Abstract.html
- ResNet — https://arxiv.org/abs/1512.03385
