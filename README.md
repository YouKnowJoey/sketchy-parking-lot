# Project Sketchy Parking Lot

## Project Objective
Our objective is to design a Python-based microservice suitable for integration into security analysis workflows that classifies parked webpages based on observed behavioral and content signals. The system will label parked webpages as suspicious, malicious, or benign. It is designed as a containerized Python pipeline to ensure consistent execution across environments.

## Approach
The system follows a multi-signal analytical approach that integrates data collection, feature extraction, and scoring into a unified pipeline. It processes parked web page data to capture a range of behavioral and content-based indicators, which are transformed into structured features for analysis. These features are evaluated using a combination of rule-based scoring and anomaly detection techniques to identify patterns associated with deceptive or abuse-prone infrastructure. The approach prioritizes scalability, modularity, and interpretability, allowing the system to adapt as additional signals and data sources are incorporated.

## Signals Considered
The system evaluates a diverse set of signals capturing structural, behavioral, and content-level characteristics of parked web pages. These include indicators derived from page content, redirect behavior, and observable patterns in page structure and composition. Features are designed to capture anomalies, repetition, monetization signals, and deviations from typical inactive page behavior.

## Project Structure
```text
sketchy-parking-lot/
├── models/
│   └── lid.176.ftz
├── notebooks/
│   └── wrangling_analysis.ipynb
├── outputs/
├── src/
│   ├── run_pipeline.py
│   ├── sketchy_features.py
│   ├── sketchy_lang_id.py
│   ├── sketchy_tokenizer.py
│   └── sketchy_unsupervised_models.py
├── .dockerignore
├── Dockerfile
├── README.md
├── requirements.txt
└── run_pipeline.sh
```

## Running the Project (Docker)
### Build the Docker image
From the root of the repository:
```bash
docker build -t sketchy-parking-lot .
```

### Run the pipeline
Execute the container:
```bash
docker run --rm \
  -u $(id -u):$(id -g) \
  -v "$(pwd)/data:/app/data" \
  -v "$(pwd)/outputs:/app/outputs" \
  sketchy-parking-lot
```

## Acknowledgments
This project was developed as part of a capstone project with the University of Arizona focused on suspicious pattern detection in parked and dormant web infrastructure.
