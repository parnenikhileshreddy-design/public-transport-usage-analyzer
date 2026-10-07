# Public Transport Usage Analyzer & Demand Prediction Dashboard

**Course End Project 9 — Batch-9 (Transportation)**  
**Team:** 25881A05DG, **25881A05DH**, 25881A05DJ  
**Student:** 25881A05DH

## Problem
Analyze public-transport usage to identify high-demand routes, low-utilization services and peak travel periods, then provide data-driven service-allocation recommendations.

## Dataset
The project is designed around the public **Public Transportation Usage Dataset** surfaced through Kaggle. Its published description reports 569,400 hourly observations, 88 columns, six cities, multiple transit modes, and variables such as boarding count, occupancy and delays. The dataset is described as a GTFS-inspired simulated urban-transit dataset and is released under CC0 1.0. Source: https://www.kaggle.com/code/amith1707/eda-transits-utilities-demo/input

Because the full source dataset is about 840 MB, this repository contains a small reproducible `sample_transport_data.csv` for immediate demonstration. For final submission, replace it with the downloaded source dataset after mapping the source columns to the project's required schema.

## Features
- Python data cleaning and validation
- Route-wise passenger analysis
- Peak-hour detection
- High/medium/low utilization classification
- SQLite DBMS storage
- SQL-ready route summaries
- Interactive Streamlit dashboard
- Plotly visualizations
- Random Forest demand-prediction extension
- Chronological train/test split to reduce temporal leakage

## Run
```bash
pip install -r requirements.txt
python src/generate_demo_data.py
python src/database.py
python src/analysis.py
python src/predict.py
streamlit run dashboard/app.py
```

## GitHub upload
Do not commit the 840 MB raw dataset. Keep it outside GitHub or use Git LFS if your instructor requires the full source file.

## Project structure
```text
public_transport_usage_analyzer/
├── data/
│   ├── raw/
│   └── processed/sample_transport_data.csv
├── database/transport.db
├── dashboard/app.py
├── docs/
├── outputs/
├── src/
│   ├── analysis.py
│   ├── database.py
│   ├── generate_demo_data.py
│   └── predict.py
├── requirements.txt
└── README.md
```
