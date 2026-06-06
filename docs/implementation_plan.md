# Phase 1 Implementation Plan

## Repository Review

The local checkout initially contained only Git metadata and no project files. The GitHub connector returned `404` for `Aaron-ski/Aaron-ski-govcon-partner-radar1.0`, and no remote was configured locally.

No XML specification files were present in the local repository, so this implementation is based on the user-provided Phase 1 requirements rather than XML-derived schemas or workflows.

## Missing Requirements

- Reachable GitHub repository access or confirmed repository name.
- XML specifications for entities, dashboard definitions, or data contracts.
- Exact source schemas for USAspending, SAM.gov, FPDS, or internal partner data.
- KPI formulas and expected thresholds for partner intelligence.
- Definition of target user roles and final hosting model.

## Technical Risks

- Synthetic sample data may not match future live source schemas.
- Contractor intelligence labels could be misunderstood as factual assessments unless clearly marked as sample data.
- DuckDB file creation and relative paths need to be stable on Windows.
- Future data size may require indexed/materialized analytical tables.
- Dashboard filters and metrics may need revision once XML specifications are available.

## Recommended Improvements

- Treat `config/app.yaml` as the source of truth for paths, default fiscal year, labels, and scoring weights.
- Keep a repeatable seed command for local database rebuilds.
- Add tests around config loading, database seeding, and analytical query outputs.
- Document the no-live-API boundary in README and UI.
- Add XML ingestion or schema validation only after the specifications are available.

## Proposed Folder Structure

```text
govcon_radar1.0/
  .streamlit/config.toml
  config/app.yaml
  data/sample/*.csv
  docs/implementation_plan.md
  govcon_radar/
    app.py
    config.py
    db.py
    queries.py
    seed.py
    ui/
      charts.py
      layout.py
      pages/
        agency_spending_explorer.py
        executive_overview.py
        prime_contractor_intelligence.py
  tests/
  README.md
  requirements.txt
```

## Build Sequence

1. Create scaffold, configuration, README, and local sample datasets.
2. Implement DuckDB connection, schema creation, and seed workflow.
3. Implement query layer for reusable dashboard metrics.
4. Build Streamlit dashboards with shared layout and Plotly charts.
5. Add tests and run compile/test verification locally.
6. Commit changes incrementally.
