# Image Representations and Preprocessing

## Key Ideas

- Computer vision starts from image representation choices such as resolution, channel layout, color space, and numeric range.
- Preprocessing standardizes inputs so the model sees stable image statistics across training and inference.
- Vision pipelines must preserve task-relevant structure, because resizing, cropping, or augmentation can remove exactly the signal the model needs.
- Input mismatches such as RGB versus BGR ordering or wrong normalization often create large quality drops that look like model failures.
- A reliable preprocessing pipeline is part of the model definition, not just a data-loading convenience.

## 1. Why Image Representation Matters

An image is not just "a picture." For a model, it is a tensor with explicit spatial dimensions, channels, and value ranges. Before any learning can happen, the engineer must decide how that tensor will be represented consistently.

Those choices influence:

- what visual detail is available
- how much compute is required
- whether pretrained weights remain compatible
- whether labels still make sense after transformation

## 2. Core Definitions

- **Resolution** is the image height and width in pixels.
- A **channel** stores one dimension of color or intensity, such as red, green, or blue.
- A **color space** defines how color is encoded, such as RGB, BGR, or HSV.
- **Normalization** rescales pixel values using predefined statistics.
- **Augmentation** applies label-preserving transformations to increase training diversity.

## 3. Common Preprocessing Decisions

### 3.1 Resolution and Aspect Ratio

Higher resolution preserves more detail but increases memory and latency. Lower resolution speeds training and inference but can destroy small objects or thin structures.

### 3.2 Color Space

Different libraries use different defaults. Many pretrained models expect RGB. Some classic pipelines use grayscale or HSV depending on the task.

### 3.3 Normalization

Models usually assume a particular input scale, such as `[0, 1]` floats or standardized channels using training-set mean and standard deviation.

## 4. Worked Example: Resize and Normalize an Input

Suppose an RGB image arrives as:

```text
height = 1,200
width = 1,600
channels = 3
dtype = uint8 in [0, 255]
```

The target model expects:

```text
224 x 224 RGB
float32 in [0, 1]
channel means = [0.5, 0.5, 0.5]
channel stds = [0.25, 0.25, 0.25]
```

### 4.1 Resize

Resize the image to `224 x 224`.

### 4.2 Scale

A pixel `[128, 64, 255]` becomes:

```text
[128/255, 64/255, 255/255]
= [0.502, 0.251, 1.000]
```

### 4.3 Normalize

Per channel:

```text
[(0.502 - 0.5)/0.25, (0.251 - 0.5)/0.25, (1.000 - 0.5)/0.25]
= [0.008, -0.996, 2.000]
```

That normalized vector is what the model actually receives.

Verification: the preprocessing pipeline transforms raw `uint8` RGB pixels into the standardized floating-point representation expected by the model.

## 5. Why Augmentation Needs Restraint

Augmentation helps generalization by simulating plausible variation, but only when the transform preserves label semantics.

Examples:

- horizontal flips may help for general object recognition
- horizontal flips can be wrong for OCR or left-right medical markers
- random crops can remove the object entirely if the task depends on full context

The rule is simple: augmentations should simulate real deployment variability, not arbitrary distortion.

## 6. Common Mistakes

1. **Channel-order mismatch.** Feeding BGR images into an RGB-trained model changes the input semantics immediately; make channel order explicit in the pipeline.
2. **Normalization drift.** Using different scaling or mean/std values at inference breaks compatibility with training; keep one shared preprocessing definition.
3. **Over-resizing.** Shrinking images too aggressively can erase small objects or text; choose resolution based on the target task, not just convenience.
4. **Label-breaking augmentation.** Applying flips, crops, or rotations without checking task semantics corrupts supervision; validate each augmentation against label meaning.
5. **Hidden preprocessing logic.** Spreading preprocessing across notebooks, dataloaders, and serving code causes drift; centralize and version the pipeline.

## 7. Practical Checklist

- [ ] Document image size, channel order, and normalization explicitly.
- [ ] Match preprocessing to the expectations of any pretrained model.
- [ ] Visualize augmented samples before training.
- [ ] Keep training and inference preprocessing implementations aligned.
- [ ] Choose resolution based on the smallest important visual detail.
- [ ] Version preprocessing parameters with model artifacts.

## 8. References

- Szeliski, Richard. *Computer Vision: Algorithms and Applications* (2nd ed.). Springer, 2022. <https://szeliski.org/Book/>
- Goodfellow, Ian, Yoshua Bengio, and Aaron Courville. *Deep Learning*. MIT Press, 2016. <https://www.deeplearningbook.org/>
- OpenCV. "Changing color spaces." <https://docs.opencv.org/4.x/df/d9d/tutorial_py_colorspaces.html>
- Shorten, Connor, and Taghi M. Khoshgoftaar. "A survey on Image Data Augmentation for Deep Learning." 2019. <https://arxiv.org/abs/1902.06110>
- Howard, Jeremy, and Sebastian Ruder. "Universal Language Model Fine-tuning for Transfer Learning" is NLP-focused, but the transfer-learning discipline carries over to input alignment. <https://aclanthology.org/P18-1031/>
- torchvision. "Model weights and preprocessing requirements." <https://pytorch.org/vision/stable/models.html>
- Albumentations. "Choosing augmentations." <https://albumentations.ai/docs/>
