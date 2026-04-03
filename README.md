# Project Sketchy Parking Lot

## Overview
Containerized Python microservice that proactively monitors expired, parked, and dormant web infrastructure to detect deceptive or abuse-prone states. It analyzes layered signals of liveness across DNS, transport, HTTP behavior, JavaScript (JS) fingerprinting, and content features to distinguish between deceptive and legitimate inactive web pages.

## Project Objective

## Approach

## Signals Considered

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
│            
├── Dockerfile
├── requirements.txt        
├── .dockerignore           
├── run_pipeline.sh         
└── README.md


## Related Work and References

