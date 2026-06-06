from pathlib import Path

from govcon_radar.config import Settings, load_settings
from govcon_radar.db import seed_database
from govcon_radar.queries import agency_summary, contractor_rankings, executive_kpis


def _tmp_settings(tmp_path: Path) -> Settings:
    base = load_settings()
    raw = dict(base.raw)
    raw["database"] = {"path": str(tmp_path / "test.duckdb")}
    return Settings(raw=raw, project_root=base.project_root)


def test_seed_database_creates_queryable_tables(tmp_path):
    settings = _tmp_settings(tmp_path)

    database_path = seed_database(settings)
    fiscal_year = settings.default_fiscal_year
    kpis = executive_kpis(fiscal_year, settings)
    agencies = agency_summary(fiscal_year, settings)
    contractors = contractor_rankings(settings)

    assert database_path.exists()
    assert kpis["obligations"] > 0
    assert len(agencies) >= 3
    assert contractors.iloc[0]["composite_score"] >= contractors.iloc[-1]["composite_score"]
