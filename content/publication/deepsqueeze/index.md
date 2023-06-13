---
title: "DeepSqueeze: Deep Semantic Compression for Tabular Data"
subtitle: ""
authors: "Amir Ilkhechi, Andrew Crotty, Alex Galakatos, Yicong Mao, Grace Fan, Xiran Shi, Ugur Cetintemel"
date: 2023-06-13T01:09:56-07:00
draft: false
weight: 0
description: "SIGMOD 2020"
coverImage: "deepsqueeze.png" # a 5:1 image with important content in the center 3:1 zone for best effect
autonumbering: false
katex:
  enable: true
  singleDollarDeliminator: true
---

![Deepsqueeze architecture](deepsqueeze-tall.png "Deepsqueeze architecture")

## Abstract

With the rapid proliferation of large datasets, efficient data compression has become more important than ever. Columnar compression techniques (e.g., dictionary encoding, runlength encoding, delta encoding) have proved highly effective for tabular data, but they typically compress individual columns without considering potential relationships among columns, such as functional dependencies and correlations. Semantic compression techniques, on the other hand, are designed to leverage such relationships to store only a subset
of the columns necessary to infer the others, but existing approaches cannot effectively identify complex relationships
across more than a few columns at a time.

We propose DeepSqeeze, a novel semantic compression framework that can efficiently capture these complex relationships within tabular data by using autoencoders to map tuples to a lower-dimensional representation. DeepSqeeze also supports guaranteed error bounds for lossy compression of numerical data and works in conjunction with common columnar compression formats. Our experimental evaluation
uses real-world datasets to demonstrate that DeepSqeeze can achieve over a 4× size reduction compared to state-of-the-art alternatives.