# Deep Learning Training Loop

## What it is
Iterative optimization of a neural network using batches, gradients, and updates.

## Why it matters
Understanding the loop helps diagnose overfitting, instability, and data issues.

## Core idea
Forward pass → compute loss → backpropagate gradients → update parameters.

## Common pitfalls
- Learning rate too high/low
- No validation monitoring
- Data leakage in preprocessing

## Debug checklist
- Track train/val loss curves
- Use early stopping or checkpoints
- Verify deterministic seeds

## References
- *Deep Learning* (Goodfellow et al.)
- *Neural Networks and Deep Learning* (Nielsen)
