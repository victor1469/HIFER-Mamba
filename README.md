# HIFER-Mamba

> **HIFER-Mamba: High-frequency Information Feature Enhancement and Reconstruction for Image Super-Resolution**

[![Paper](https://img.shields.io/badge/Paper-TIP-red)]()
[![Project Page](https://img.shields.io/badge/Project-Website-blue)]()
[![License](https://img.shields.io/badge/License-MIT-green)]()

Official implementation of **HIFER-Mamba**, a frequency-aware Mamba framework for image super-resolution.

---

## Overview

HIFER-Mamba introduces three complementary components into the Mamba-based image restoration framework:

- **Frequency-aware Feature Enhancement**
- **Progressive Feature Integration**
- **Nonlinear State Enhancement**

These modules effectively improve high-frequency texture reconstruction and structural recovery while preserving the computational efficiency of state-space models.

---

## Motivation

Image super-resolution requires recovering fine textures while maintaining global structural consistency.

To address this challenge, HIFER-Mamba combines frequency-domain representation, progressive feature interaction, and nonlinear state modeling into a unified Mamba framework, enabling more accurate and visually pleasing image reconstruction.

---

## Framework

<p align="center">
<img src="figures/overview.png" width="95%">
</p>

**Figure 1.** Overall architecture of HIFER-Mamba.

---

## Pipeline

<p align="center">
<img src="assets/pipeline.svg" width="90%">
</p>

The proposed pipeline progressively extracts, enhances, and reconstructs image features through frequency-aware representation and nonlinear state-space modeling.

---

## Visual Results

<p align="center">
<img src="assets/results.svg" width="95%">
</p>

HIFER-Mamba reconstructs sharper textures and clearer structures than previous Mamba-based image restoration methods.

---

## Key Features

- ✅ Frequency-aware representation for enhanced texture reconstruction.
- ✅ Progressive feature integration across deep Mamba blocks.
- ✅ Nonlinear state enhancement for improved representation capability.
- ✅ Competitive PSNR/SSIM on five standard benchmark datasets.
- ✅ Stable optimization and efficient inference.

---

## Repository Structure

```
analysis/        Analysis scripts
datasets/        Training and testing datasets
experiments/     Training configurations and checkpoints
figures/         Figures used in the paper
results/         Reconstruction results
docs/            Project webpage
```

---

## Getting Started

### Training

```bash
python basicsr/train.py -opt options/train/train_HIFER_Mamba_x2.yml
```

### Testing

```bash
python basicsr/test.py -opt options/test/test_HIFER_Mamba_x2.yml
```

---

## Project Page

Coming soon.

---

## Citation

If you find this work useful, please consider citing:

```bibtex
@article{jiang2026hifermamba,
  title={HIFER-Mamba: High-frequency Information Feature Enhancement and Reconstruction for Image Super-Resolution},
  author={Nan Jiang and ...},
  journal={IEEE Transactions on Image Processing},
  year={2026}
}
```

---

## Acknowledgement

This project is built upon the excellent open-source projects **BasicSR** and **MambaIR**. We sincerely thank the original authors for making their code publicly available.
