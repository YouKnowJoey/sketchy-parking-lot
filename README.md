# Project Sketchy Parking Lot

## Overview

## Project Objective
Our objective is to design a Python-based system suitable for integration into security analysis workflows that classifies parked webpages based on observed behavioral and content signals. The system will label parked webpages as either malicious or benign. It is designed as a containerized Python pipeline to ensure consistent execution across environments.

## Approach
The system follows a multi-signal analytical approach that integrates data collection, feature extraction, and scoring into a unified pipeline. It processes parked web page data to capture a range of behavioral and content-based indicators, which are transformed into structured features for analysis. These features are evaluated using a combination of rule-based scoring and anomaly detection techniques to identify patterns associated with deceptive or abuse-prone infrastructure. The approach prioritizes scalability, modularity, and interpretability, allowing the system to adapt as additional signals and data sources are incorporated.

## Signals Considered
The system evaluates a diverse set of signals capturing structural, behavioral, and content-level characteristics of parked web pages. These include indicators derived from page content, redirect behavior, and observable patterns in page structure and composition. Features are designed to capture anomalies, repetition, monetization signals, and deviations from typical inactive page behavior.

## Running the Project (Docker)
### Build the Docker image

## Project Structure
The repository is organized to separate exploratory work, feature construction, and execution of the pipeline:

```text
sketchy-parking-lot/
├── data/
│   └──raw/
├── notebooks/
│   └── wrangling_analysis.ipynb
├── src/
│   ├── run_pipeline.py
│   ├── features.py
│   └── scoring.py
├── outputs/
├── Dockerfile
├── requirements.txt
├── .dockerignore
├── run_pipeline.sh
└── README.md
```

## Related Work and References