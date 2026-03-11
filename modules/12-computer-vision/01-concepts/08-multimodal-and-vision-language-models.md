# Multimodal and Vision-Language Models

## Overview
Vision-language models align images with text to enable retrieval, captioning,
and zero-shot classification.

## Why it matters
Multimodal models reduce labeling needs and enable flexible search and reasoning
over visual content.

## Key ideas
- Contrastive learning aligns image and text embeddings
- Zero-shot classification uses text prompts as labels
- Captioning and VQA combine visual and language features
- Dataset quality and alignment are critical

## Practical workflow
- Use a pretrained vision-language model for embeddings
- Build retrieval or classification on top of shared embeddings
- Calibrate thresholds for zero-shot predictions
- Evaluate on domain-specific queries and prompts

## Failure modes
- Prompt sensitivity for zero-shot tasks
- Bias from web-scale datasets
- Spurious correlations and shortcut learning
- Hallucinated captions without grounding

## Checklist
- Test multiple prompts for stability
- Log false positives/negatives by category
- Add grounding or retrieval for factual tasks
- Monitor for sensitive content leakage

## References
- CLIP — https://arxiv.org/abs/2103.00020
- BLIP — https://arxiv.org/abs/2201.12086
