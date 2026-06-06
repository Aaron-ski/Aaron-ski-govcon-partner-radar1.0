# GovCon Partner Radar

GovCon Partner Radar is a local-first Streamlit + DuckDB MVP for personal government contracting market intelligence.

It is designed to answer:

> Which agencies, opportunities, contracts, and prime contractors should I focus on over the next 12-24 months?

## Phase 1 Scope

- Streamlit application with dark mode default
- DuckDB local database seeded from local CSV files
- Executive Overview dashboard
- Agency Spending Explorer dashboard
- Prime Contractor Intelligence dashboard
- Configuration-driven scoring and dashboard settings
- CSV exports for dashboard tables
- Windows-friendly local development
- Public demo dataset under `data/demo/`
- No live API calls from dashboard runtime

The default app configuration uses a public demo dataset. Awards are curated from USAspending.gov public API results; SAM-style opportunities are synthetic demo records because SAM.gov API access requires a key.

## Quick Start

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
.\.venv\Scripts\python scripts\build_db.py
.\.venv\Scripts\python -m streamlit run app.py --server.address 127.0.0.1
```

Open the Streamlit URL shown in the terminal, usually `http://127.0.0.1:8501`.

## Dashboards

- **Executive Overview**: fiscal-year KPIs, spending by agency, capability pipeline, top primes, and immediate market focus recommendations.
- **Agency Spending Explorer**: filters for agency, office, NAICS, PSC, keyword, and date range with spending detail export.
- **Prime Contractor Intelligence**: partner priority scoring, score explanations, prime profiles, and exportable target list.

## Configuration

- `config/app.yaml`: app settings, database path, dashboard defaults, target agencies, and capability keywords.
- `config/demo.yaml`: explicit public demo configuration for Streamlit Community Cloud or local demo runs.
- `config/scoring_weights.yml`: configurable scoring weights from the XML scoring model.
- `.env.example`: safe placeholder for future API ingestion variables.

Phase 1 reads local CSV files and DuckDB only. USAspending and SAM.gov scripts are placeholders for future ingestion and are not called by Streamlit pages.

To force a specific config locally:

```powershell
$env:GOVCON_RADAR_CONFIG="config/demo.yaml"
.\.venv\Scripts\python scripts\build_db.py
.\.venv\Scripts\python -m streamlit run app.py --server.address 127.0.0.1
```

## Public Demo Data

Demo dataset location:

```text
data/demo/
```

Refresh date: `2026-06-06`

Sources and boundaries:

- Award rows: curated from public USAspending.gov API results for Department of Defense contract awards.
- Current award-year coverage: 45 records with 2025 start dates and 55 records with 2026 start dates.
- Opportunity rows: synthetic SAM-style records used to complete the demo workflow without requiring a SAM.gov API key.
- Not committed: `.env`, API keys, raw downloads, private capture notes, generated local DuckDB files.

Regenerate the committed demo CSVs with:

```powershell
.\.venv\Scripts\python scripts\create_demo_dataset.py
```

That command calls USAspending.gov and should only be run during an intentional demo-data refresh, not from dashboard page load.

## Streamlit Community Cloud Deployment

1. Push this repository to GitHub.
2. Go to [Streamlit Community Cloud](https://streamlit.io/cloud).
3. Create a new app from the GitHub repository.
4. Set the entrypoint to `app.py`.
5. Confirm `requirements.txt` is detected.
6. Deploy without adding API keys.

The deployed app builds or loads DuckDB from committed CSV files. It does not call USAspending.gov, SAM.gov, or any live API while users view dashboard pages.

Public app link: add the Streamlit Community Cloud URL here after deployment.

## Development Checks

```powershell
.\.venv\Scripts\python -m compileall app.py src scripts pages
.\.venv\Scripts\python -m pytest
```

## Project Layout

```text
app.py                         Streamlit entrypoint
config/                        YAML configuration
data/demo/                     Public demo CSVs safe for GitHub
data/sample/                   Local synthetic sample CSVs
data/govcon_radar.duckdb       Generated local DuckDB database
docs/implementation_plan.md    Phase 1 planning notes
pages/                         Streamlit dashboard modules
scripts/build_db.py            Manual CSV to DuckDB loader
scripts/ingest_*.py            Phase 2-safe placeholders
src/                           Data, scoring, chart, and export helpers
tests/                         Data-layer tests
*.xml                          Source specifications
```

## API Key Safety

Create a `.env` file locally for future ingestion work, but never commit it.

```env
SAM_API_KEY=replace_with_your_key
USA_SPENDING_BASE_URL=https://api.usaspending.gov
SAM_BASE_URL=https://api.sam.gov/prod/opportunities/v2/search
```

## Data Boundary

Phase 1 does not call SAM.gov, USAspending, FPDS, agency APIs, or third-party data providers during dashboard usage. The local DuckDB database is generated from CSV files in `data/demo` by default.
