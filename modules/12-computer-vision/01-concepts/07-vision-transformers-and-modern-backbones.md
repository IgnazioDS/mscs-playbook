# Vision Transformers and Modern Backbones

## Key Ideas

- Vision transformers represent images as sequences of patches and use attention to model long-range spatial interactions.
- Modern backbones include both transformer-based and hybrid architectures, so the design choice is about tradeoffs rather than a simple CNN replacement story.
- Transformer backbones often scale well with data and transfer learning, but they can be more memory-intensive and sensitive to training setup.
- Patch size, image resolution, and pretraining regime strongly influence transformer performance.
- Backbone choice should be guided by task scale, deployment constraints, and data availability rather than by benchmark fashion alone.

## 1. Why Vision Backbones Evolved

CNNs are strong at local pattern extraction, but their inductive bias toward local neighborhoods can limit direct access to long-range interactions. Vision transformers address that by representing the image as a sequence of patch tokens and applying self-attention across them.

This makes global context easier to model, especially when large-scale pretraining data is available.

## 2. How Vision Transformers Work

### 2.1 Patch Embeddings

An image is split into fixed-size patches, and each patch is projected into a token embedding.

### 2.2 Self-Attention

Attention lets each patch interact with all others in the same layer, which helps capture global dependencies.

### 2.3 Hierarchical Variants

Architectures such as Swin use local windows and hierarchical stages to reduce cost and recover multiscale structure.

## 3. CNNs vs ViTs in Practice

CNNs often remain attractive when:

- data is limited
- latency must be low
- hardware is constrained

Vision transformers often become attractive when:

- strong pretraining is available
- transfer learning matters
- global context is important

This is why "modern backbone" is a better framing than "transformers replace CNNs."

## 4. Worked Example: Patch Count and Sequence Length

Suppose an image is:

```text
224 x 224
```

with patch size:

```text
16 x 16
```

### 4.1 Number of Patches

Along each dimension:

```text
224 / 16 = 14
```

Total patch tokens:

```text
14 * 14 = 196
```

If a class token is added, the transformer sequence length becomes:

```text
197
```

### 4.2 Why This Matters

Smaller patches increase token count, which raises attention cost. Larger patches reduce cost but may discard local detail.

Verification: patch size directly determines token sequence length, which in turn affects memory use and fine-detail representation.

## 5. Modern Backbone Selection

When choosing a backbone, consider:

- image resolution
- task type
- pretrained checkpoint availability
- latency and memory budget
- data scale

The "best" backbone is the one that meets task requirements within operational constraints.

## 6. Common Mistakes

1. **Benchmark imitation.** Adopting a transformer backbone because it leads a public benchmark can waste compute on small or latency-sensitive tasks; benchmark against a strong CNN baseline first.
2. **Patch-size neglect.** Using overly large patches can erase fine detail, while tiny patches can explode memory; tune patch size to the task and resolution.
3. **Pretraining blindness.** Vision transformers often rely heavily on strong pretraining; comparing an unprepared ViT to a pretrained CNN can be misleading.
4. **Cost underestimation.** Attention memory and throughput constraints grow quickly with sequence length; profile on target hardware rather than assuming feasibility.
5. **Backbone-only focus.** Changing the backbone without revisiting preprocessing, training schedule, and task head leaves gains unrealized; treat the system as a whole.

## 7. Practical Checklist

- [ ] Compare modern backbones against a strong CNN baseline on the same split.
- [ ] Choose patch size and resolution together.
- [ ] Prefer pretrained checkpoints when data is limited.
- [ ] Measure memory and throughput on target hardware.
- [ ] Revisit optimization schedule when switching backbone families.
- [ ] Validate performance on the task’s hardest visual cases, not only average accuracy.

## 8. References

- Dosovitskiy, Alexey, et al. "An Image is Worth 16x16 Words." 2021. <https://arxiv.org/abs/2010.11929>
- Liu, Ze, et al. "Swin Transformer." 2021. <https://arxiv.org/abs/2103.14030>
- Touvron, Hugo, et al. "Training data-efficient image transformers & distillation through attention." 2021. <https://arxiv.org/abs/2012.12877>
- Tolstikhin, Ilya, et al. "MLP-Mixer." 2021. <https://arxiv.org/abs/2105.01601>
- He, Kaiming, et al. "Masked Autoencoders Are Scalable Vision Learners." 2022. <https://arxiv.org/abs/2111.06377>
- Szeliski, Richard. *Computer Vision: Algorithms and Applications* (2nd ed.). Springer, 2022. <https://szeliski.org/Book/>
- torchvision. "Computer vision models." <https://pytorch.org/vision/stable/models.html>
