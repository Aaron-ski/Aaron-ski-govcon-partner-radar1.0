# GovCon Partner Radar

Local-first Phase 1 MVP for exploring synthetic government contracting spending, agency demand signals, and prime contractor partner-fit indicators.

## Phase 1 Scope

- Streamlit application with dark mode default
- DuckDB local database seeded from local CSV files
- Executive Overview dashboard
- Agency Spending Explorer dashboard
- Prime Contractor Intelligence dashboard
- Configuration-driven paths, labels, fiscal years, and scoring weights
- Windows-friendly local development
- No live API calls

All included data is fictional sample data for product demonstration only.

## Quick Start

```powershell
py -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
.\.venv\Scripts\python -m govcon_radar.seed
.\.venv\Scripts\python -m streamlit run govcon_radar/app.py --server.address 127.0.0.1
```

Open the Streamlit URL shown in the terminal, usually `http://127.0.0.1:8501`.

## Dashboards

- **Executive Overview**: fiscal-year KPIs, agency obligation mix, capability pipeline, and top synthetic partner candidates.
- **Agency Spending Explorer**: agency filter, vehicle mix, obligation ranking, and spending detail table.
- **Prime Contractor Intelligence**: partner score filtering, contractor score scatter, and synthetic contractor profiles.

## Configuration

Edit `config/app.yaml` to change the generated database path, sample CSV paths, default fiscal year, dashboard limits, and scoring weights. The app reads this file at startup and seeds the DuckDB database automatically when `data/govcon_radar.duckdb` does not exist.

## Development Checks

```powershell
.\.venv\Scripts\python -m compileall govcon_radar
.\.venv\Scripts\python -m pytest
```

## Project Layout

```text
config/app.yaml                  Application configuration
data/sample/*.csv                Local synthetic datasets
data/govcon_radar.duckdb         Generated local DuckDB database
docs/implementation_plan.md      Phase 1 planning notes
govcon_radar/                    Application package
tests/                           Data-layer tests
```

## Data Boundary

Phase 1 does not call SAM.gov, USAspending, FPDS, agency APIs, or third-party data providers. The local DuckDB database is generated from CSV files in `data/sample`.
