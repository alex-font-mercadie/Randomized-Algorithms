# Ballanced Allocation

This repository contains an implementation of different bin selection strategies for the **choice problem**, along with experiments that compare their performance. The experiments simulate the distribution of loads across bins using various strategies and visualize the results.

## Table of Contents

- [Introduction](#introduction)
- [Getting Started](#getting-started)
- [Experiment Details](#experiment-details)
- [How to Run the Experiments](#how-to-run-the-experiments)
- [Results](#results)
- [Contributing](#contributing)
- [License](#license)

## Introduction

This repository contains Python code for simulating and comparing different bin selection strategies used in load balancing. The experiment compares **one-choice**, **two-choice**, and several **beta-choice** methods, as well as combinations with different query types and batch sizes.

The primary goal is to compare the average gap between the maximum load and the load of each bin during the simulation.

## Getting Started

To get started with this project, follow the steps below to clone the repository and install the necessary dependencies.

### Prerequisites

- Python 3.6+
- Jupyter Notebook (for running the experiments interactively)
- Required Python packages:
  - `random`
  - `matplotlib`
  - `statistics`

You can install the required packages via pip:

```bash
pip install matplotlib
