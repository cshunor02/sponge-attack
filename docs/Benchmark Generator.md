# Benchmark Prompt Generator

A lightweight Python script that generates a diverse, structured dataset of prompts for benchmarking Large Language Models (LLMs). This dataset can be used to evaluate model performance, robustness, and behavior across a wide range of prompt categories and complexities — including adversarial and nonsense prompts useful for stress-testing (e.g., sponge attacks).

---

## Features

- **Structured categories**: `qa`, `math`, `code`, `story`, `noise`, `mixed`
- **Subtype support**: `short`, `long`, and `wild` (in `mixed`)
- **Randomized output**: Shuffles prompts before export
- **Standard format**: Outputs in newline-delimited JSON (`.jsonl`)
- **Simple and dependency-free**: Uses only Python standard libraries

---

##  Output

The script outputs a `.jsonl` file located at:

```
inputs/benchmark_prompts.jsonl
```

Each line in the file is a JSON object of the form:

```json
{
  "id": 42,
  "category": "code",
  "subtype": "short",
  "prompt": "Write a Python function to reverse a string."
}
```

---

## How to Use

### Requirements

- Python 3.6+

### Run

```bash
python benchmarkGenerator.py
```

The script will generate the dataset and display:

```
Dataset with 160 prompts saved to 'inputs/benchmark_prompts.jsonl'
```

---

## Use Cases

- **Model evaluation**: Test LLMs against a curated, category-labeled dataset
- **Sponge attack simulation**: Includes "noise" and "mixed" categories that can induce high computational load
- **Prompt engineering research**: Supports reproducible benchmarking of model prompt sensitivity
- **Stress testing**: Covers both low-effort and high-effort reasoning tasks

---

## Why This Version?

- **Extensible**: Prompt data is modular and easy to edit
- **Randomized**: Output is shuffled to avoid prompt order bias
- **Standardized format**: Easily ingestible into most ML workflows
- **Safe and ethical**: Does not include model-specific vulnerabilities or exploitative payloads
- **Lightweight and fast**: No unnecessary overhead or external dependencies

---

## 📄 License

This script is intended for academic and research use. If redistributed, please provide attribution to the original author.

