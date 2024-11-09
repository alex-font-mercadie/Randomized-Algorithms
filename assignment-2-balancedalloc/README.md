# Ballanced Allocation

In this assignment we compare the performance of different different allocation strategies of balls into bins. The experiments simulate the distribution of loads across bins using various strategies and visualize the results.

## Table of Contents

- [Introduction](#introduction)
- [Getting Started](#getting-started)
- [Experiment Details](#experiment-details)
- [How to Run the Experiments](#how-to-run-the-experiments)
- [Results](#results)
- [Contributing](#contributing)
- [License](#license)

## Introduction

This Python code simulates set of experiments to empirically study and compare the gap Gn for (at lest) the three strategies one-, two- and (1 + β)-choices (with different values for the parameter β), as the number n of balls grows, until we reach the heavy-load scenario n = m2. It also simulates the the experiments in the b-batched setting, where balls arrive in batches of b balls, and the allocation strategy is applied as before, but the information on the load of the bins is the one available at the beginning of the batch

The primary goal is to compare the average gap between the maximum load and the load of each bin during the simulation.

## Getting Started

To get started with this project, follow the steps below to clone the repository and install the necessary dependencies.

### Prerequisites

- Python 3.6+: Download from [python.org](https://www.python.org/downloads/)
- Jupyter Notebook (for running the experiments interactively)
- Jupyter Notebook: Jupyter can be installed via `pip` or through the Anaconda distribution.
- Required Python packages:
  - `random`
  - `matplotlib`
  - `statistics`

You can install the required packages via pip:

```bash
pip install matplotlib
```

Note: random and statistics come pre-installed with Python.

### Installing Jupyter Notebook

#### Option 1: Using pip

1. Open a terminal (or Command Prompt on Windows).
2. Install Jupyter using pip by running the following command:

   ```bash
   pip install jupyter
   ```

#### Option 2: Using Anaconda
If you have the Anaconda distribution installed, Jupyter Notebook comes pre-installed. If not, you can install Anaconda from the link above.

