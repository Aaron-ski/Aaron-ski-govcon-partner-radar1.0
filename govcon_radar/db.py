from __future__ import annotations

from pathlib import Path

import duckdb

from govcon_radar.config import Settings, load_settings


TABLES = {
    "agency_spending": "agency_spending",
    "prime_contractors": "prime_contractors",
    "capability_markets": "capability_markets",
}


def connect(settings: Settings | None = None, read_only: bool = False) -> duckdb.DuckDBPyConnection:
    settings = settings or load_settings()
    settings.database_path.parent.mkdir(parents=True, exist_ok=True)
    return duckdb.connect(str(settings.database_path), read_only=read_only)


def seed_database(settings: Settings | None = None) -> Path:
    settings = settings or load_settings()
    settings.database_path.parent.mkdir(parents=True, exist_ok=True)

    with connect(settings) as conn:
        for table_name, sample_key in TABLES.items():
            csv_path = settings.sample_paths[sample_key]
            if not csv_path.exists():
                raise FileNotFoundError(f"Missing sample data file: {csv_path}")
            conn.execute(f"CREATE OR REPLACE TABLE {table_name} AS SELECT * FROM read_csv_auto(?)", [str(csv_path)])

        conn.execute(
            """
            CREATE OR REPLACE VIEW agency_year_summary AS
            SELECT
                fiscal_year,
                agency,
                SUM(obligations) AS obligations,
                SUM(award_count) AS award_count,
                SUM(small_business_obligations) AS small_business_obligations,
                AVG(competition_rate) AS competition_rate
            FROM agency_spending
            GROUP BY fiscal_year, agency
            """
        )
        conn.execute(
            """
            CREATE OR REPLACE VIEW contractor_rankings AS
            SELECT
                *,
                ROUND(
                    (small_business_partnering_rate * 100 * 0.20)
                    + (past_performance_score * 0.25)
                    + (cyber_readiness_score * 0.20)
                    + (agency_alignment_score * 0.25)
                    + (partner_fit_score * 0.10),
                    1
                ) AS composite_score
            FROM prime_contractors
            """
        )

    return settings.database_path


def ensure_database(settings: Settings | None = None) -> Path:
    settings = settings or load_settings()
    if not settings.database_path.exists():
        return seed_database(settings)
    return settings.database_path
