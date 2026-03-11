# Convolution and CNNs

## Key Ideas

- Convolutional neural networks learn spatial filters that reuse weights across image locations, making them efficient for grid-structured visual input.
- Early convolution layers capture local patterns such as edges and textures, while deeper layers combine them into higher-level features.
- CNNs remain strong vision baselines because they offer favorable accuracy-latency tradeoffs and are well understood operationally.
- Pooling, stride, normalization, and residual connections shape both model capacity and training stability.
- CNN performance depends as much on input alignment, optimization, and data quality as on architecture depth.

## 1. Why Convolution Helped Vision

Images have local spatial structure. Nearby pixels are more related than distant ones, and the same pattern may matter wherever it appears. Convolution encodes those assumptions directly:

- local connectivity
- weight sharing
- translation-aware feature extraction

That makes CNNs more parameter-efficient than dense networks applied directly to pixels.

## 2. Core Building Blocks

### 2.1 Convolution

A convolution layer applies a small learned kernel across the image to produce a feature map.

### 2.2 Pooling or Stride

Downsampling reduces spatial resolution and compute while increasing receptive field.

### 2.3 Nonlinearity and Normalization

Activation functions and normalization layers help the network learn expressive but stable transformations.

### 2.4 Residual Connections

Residual paths make deep networks easier to train by preserving gradient flow.

## 3. Why CNNs Still Matter

Even with modern transformer backbones, CNNs remain practical when:

- latency is tight
- hardware is limited
- the dataset is moderate in size
- local texture and shape cues dominate

Architectures such as ResNet and MobileNet remain common because they balance deployment cost and strong performance.

## 4. Worked Example: Feature Map Size

Suppose an input image has:

```text
height = 32
width = 32
channels = 3
```

Apply a convolution layer with:

```text
kernel size = 3
padding = 1
stride = 1
output channels = 16
```

### 4.1 Spatial Size

With stride `1` and padding `1`, the spatial size stays the same:

```text
output height = 32
output width = 32
```

### 4.2 Output Shape

The resulting feature map is:

```text
32 x 32 x 16
```

Now apply `2 x 2` pooling with stride `2`:

```text
16 x 16 x 16
```

The network has reduced spatial resolution by half while keeping the channel depth.

Verification: the convolution preserves the original spatial dimensions under same-padding, and the pooling step halves height and width as expected.

## 5. Design Tradeoffs

Deeper CNNs can model richer structure, but they also cost more to train and deploy. Larger feature maps improve detail retention but increase memory and latency. This is why CNN design is always about tradeoffs among:

- receptive field
- throughput
- model size
- task detail requirements

The correct backbone depends on the deployment setting, not only on leaderboard performance.

## 6. Common Mistakes

1. **Backbone cargo cult.** Choosing the largest CNN available without latency or memory constraints creates deployment pain; benchmark on target hardware.
2. **Pretraining mismatch.** Using pretrained weights with incompatible input normalization or resolution hurts quality immediately; align preprocessing exactly.
3. **Resolution neglect.** Downsampling too aggressively can destroy small-object or fine-text information; size the network to the task’s detail needs.
4. **Architecture-only focus.** Blaming the CNN for weak results when labels, preprocessing, or splits are flawed hides the true issue; debug the full pipeline.
5. **No baseline discipline.** Skipping simple CNN baselines for more complex architectures makes iteration slower; establish a strong reference model first.

## 7. Practical Checklist

- [ ] Start with a proven CNN backbone before trying more complex models.
- [ ] Match preprocessing to the expected pretrained input format.
- [ ] Measure memory, throughput, and latency on target hardware.
- [ ] Inspect validation failures involving small or fine-detail objects.
- [ ] Keep model depth and width proportional to the dataset and task.
- [ ] Compare CNN performance against transformer backbones on the same evaluation split.

## 8. References

- LeCun, Yann, et al. "Gradient-Based Learning Applied to Document Recognition." 1998. <http://yann.lecun.com/exdb/publis/pdf/lecun-01a.pdf>
- Krizhevsky, Alex, Ilya Sutskever, and Geoffrey Hinton. "ImageNet Classification with Deep Convolutional Neural Networks." 2012. <https://papers.nips.cc/paper/2012/hash/c399862d3b9d6b76c8436e924a68c45b-Abstract.html>
- He, Kaiming, et al. "Deep Residual Learning for Image Recognition." 2015. <https://arxiv.org/abs/1512.03385>
- Howard, Andrew G., et al. "MobileNets." 2017. <https://arxiv.org/abs/1704.04861>
- Szeliski, Richard. *Computer Vision: Algorithms and Applications* (2nd ed.). Springer, 2022. <https://szeliski.org/Book/>
- Goodfellow, Ian, Yoshua Bengio, and Aaron Courville. *Deep Learning*. MIT Press, 2016. <https://www.deeplearningbook.org/>
- torchvision. "Model zoo and preprocessing guidance." <https://pytorch.org/vision/stable/models.html>
