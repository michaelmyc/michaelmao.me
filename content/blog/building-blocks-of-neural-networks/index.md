---
title: "Building Blocks of Neural Networks"
subtitle: ""
date: 2023-10-01T23:30:46+08:00
draft: false
unlisted: false
series: "Building Blocks of Neural Networks"
seriesNumber: 0
tags: ["deep-learning"]
description: "Purpose, Disclaimer, and Table of Content"
coverImage: "" # a 5:1 image with important content in the center 3:1 zone for best effect
autonumbering: false
katex:
  enable: false
  singleDollarDeliminator: true
---

![animated convolution operation on a padded 2D array](convolution.mp4 "convolution operation on a padded 2D array")

## Purpose

This series goes over the basic building blocks of Neural Networks, following the API provided by [PyTorch](https://pytorch.org/). 

The PyTorch documentation provides good explanation of the API, the calculation made, and the shapes of the inputs, outputs, and weights. However, dense text descriptions and mathematical formulas aren't necessarily intuitive. This series aims to provide intuition at a glance to serve as a reference/memo that supplements the PyTorch documentation. 

## Disclaimer

This series follows the conventions in [PyTorch 2.1.0](https://pytorch.org/docs/2.1/). The concepts discussed should apply to other deep learning frameworks and future PyTorch releases but there may be caveats and differences in nomenclature. 

## Table of Content

1. [Linear Layers](/blog/linear-layers)
1. [Convolutional Layers](/blog/convolutional-layers)
1. [Transformer Blocks](/blog/transformer-blocks)

---

Special thanks for [3Blue1Brown](https://www.3blue1brown.com/) and community members for the fantastic [manim](https://www.manim.community/) library that powers all the animations in this series.