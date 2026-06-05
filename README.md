# Blue Stock Internship Project

## Mutual Fund Analytics Platform

A data analytics project that collects, cleans, analyses, and visualises Indian mutual fund data — including NAV history, fund master details, and live market data.

## Project Structure

```
BLUE_STOCK_INTERNSHIP/
├── data/
│   ├── raw/          → Original, untouched data files
│   └── processed/    → Cleaned and transformed data
├── notebooks/        → Jupyter notebooks for exploration
├── sql/              → SQL queries
├── dashboard/        → Dashboard files
├── reports/          → Final reports and charts
├── data_ingestion.py → Script to load and inspect CSV datasets
├── live_nav_fetch.py → Script to fetch live NAV from mfapi.in
├── requirements.txt  → Python dependencies
└── README.md         → This file
```

## Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Fetch live NAV data
python live_nav_fetch.py

# Load and inspect all datasets
python data_ingestion.py
```

## Data Sources

- **CSV Datasets**: Provided mutual fund datasets (fund_master, nav_history, etc.)
- **Live API**: [mfapi.in](https://api.mfapi.in) — Free Indian mutual fund NAV API

## Tech Stack

- Python 3.x (pandas, numpy, matplotlib, seaborn, plotly)
- SQL (SQLAlchemy)
- Jupyter Notebooks
- Git / GitHub
