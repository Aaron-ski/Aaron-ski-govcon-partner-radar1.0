# GovCon Partner Radar — Codex Build Spec

GovCon Partner Radar is a local-first Streamlit + DuckDB MVP for personal government contracting market intelligence.

It is designed to answer:

> Which agencies, opportunities, contracts, and prime contractors should I focus on over the next 12-24 months?

## Recommended choices

- **Development environment:** Windows-friendly local Python virtual environment.
- **Dashboard:** Streamlit.
- **Storage:** DuckDB.
- **Data flow:** Ingest first, store locally, query locally.
- **Scoring:** Configurable YAML weights, not hardcoded.
- **Capture notes:** Include in MVP because public data alone will not capture relationship context.

## Why local-first?

The dashboard should not call live APIs during normal use. API calls should run through ingestion scripts, scheduled jobs, or manual refresh commands. This keeps the app fast, low-cost, and usable offline.

## API key safety

Create a `.env` file locally, but never commit it.

```env
SAM_API_KEY=replace_with_your_key
USA_SPENDING_BASE_URL=https://api.usaspending.gov
SAM_BASE_URL=https://api.sam.gov/prod/opportunities/v2/search
```

Commit `.env.example`, not `.env`.

Recommended `.gitignore`:

```gitignore
.env
data/raw/
data/processed/
data/*.duckdb
.venv/
__pycache__/
```

## Codex build order

1. Create the repository tree from `technical_architecture.xml`.
2. Create sample CSVs from `ingestion_pipeline.xml`.
3. Create `scripts/build_db.py`.
4. Create DuckDB query helpers.
5. Create Streamlit pages.
6. Add configurable scoring.
7. Add CSV exports.
8. Add placeholder ingestion scripts for USAspending and SAM.gov.
9. Keep API calls out of dashboard runtime.

## Local commands

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python scripts/build_db.py
streamlit run app.py
```

## File series

- `project_overview.xml`
- `product_requirements.xml`
- `technical_architecture.xml`
- `data_sources_and_schema.xml`
- `dashboard_pages.xml`
- `scoring_model.xml`
- `partner_radar_logic.xml`
- `ingestion_pipeline.xml`
- `implementation_plan.xml`
- `codex_build_instructions.xml`
- `README.md`

## Important notes

USAspending.gov provides official federal spending data and API access. SAM.gov Opportunities API requires a user API key. Use both through ingestion scripts, not dashboard page loads.
