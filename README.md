
# FinTrack 

A personal finance analytics tool built with Python and SQLite. Ingests bank export CSVs, cleans the data, stores it in a local database, and surfaces spending insights through a terminal dashboard.

## Tech Stack
 - Python 3.11
 - SQLite (built into Python)
 - pandas, Rich, pytest


## Status

Under active development

## Quick Start
''' bash 
git clone https://github.com/Suryawanshian/fintrack.git
cd fintrack
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python fintrack/ingest.py
'''

## Features (planned)
- CSV ingestion and data cleaning
- SQlite database storage
- Spending analytics by category
- CLI dashboard with Rich
- Automated monthly reports
- Anomaly detection