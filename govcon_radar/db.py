from __future__ import annotations

from pathlib import Path

import duckdb

from govcon_radar.config import Settings, load_settings


TABLES = {
    "agencies": "agencies",
    "vendors": "vendors",
    "contract_vehicles": "contract_vehicles",
    "awards": "awards",
    "opportunities": "opportunities",
    "capture_notes": "capture_notes",
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
                CAST(strftime(a.start_date, '%Y') AS INTEGER) AS fiscal_year,
                g.agency_name AS agency,
                SUM(a.award_value) AS obligations,
                COUNT(*) AS award_count,
                SUM(CASE WHEN v.vendor_type = 'Small Business' THEN a.award_value ELSE 0 END) AS small_business_obligations,
                AVG(CASE WHEN v.vendor_type = 'Small Business' THEN 0.74 ELSE 0.57 END) AS competition_rate
            FROM awards a
            JOIN agencies g ON a.agency_id = g.agency_id
            JOIN vendors v ON a.vendor_id = v.vendor_id
            GROUP BY fiscal_year, agency
            """
        )
        conn.execute(
            """
            CREATE OR REPLACE VIEW contractor_rankings AS
            SELECT
                v.vendor_name AS contractor,
                'Sample' AS headquarters,
                MODE(g.agency_name) AS primary_agency,
                MODE(a.keywords) AS core_capability,
                SUM(a.award_value) AS total_obligations,
                COUNT(*) AS award_count,
                AVG(CASE WHEN v.vendor_type = 'Small Business' THEN 0.72 ELSE 0.36 END) AS small_business_partnering_rate,
                LEAST(95, 68 + COUNT(*) * 4) AS past_performance_score,
                CASE WHEN LOWER(MODE(a.keywords)) LIKE '%cyber%' THEN 92 ELSE 82 END AS cyber_readiness_score,
                LEAST(95, 65 + COUNT(DISTINCT a.agency_id) * 8 + COUNT(*) * 2) AS agency_alignment_score,
                LEAST(95, 62 + COUNT(*) * 5) AS partner_fit_score,
                ROUND(
                    (LEAST(95, 65 + COUNT(DISTINCT a.agency_id) * 8 + COUNT(*) * 2) * 0.30)
                    + (LEAST(95, 62 + COUNT(*) * 5) * 0.25)
                    + (LEAST(95, 68 + COUNT(*) * 4) * 0.20)
                    + (CASE WHEN MAX(a.end_date) <= DATE '2026-12-31' THEN 85 ELSE 65 END * 0.15)
                    + (CASE WHEN v.vendor_type = 'Large Business' THEN 78 ELSE 62 END * 0.10),
                    1
                ) AS composite_score,
                CASE
                    WHEN v.vendor_type = 'Large Business' THEN 'Likely prime/team lead with potential subcontractor lanes.'
                    ELSE 'Small-business profile may indicate partner or competitor ambiguity.'
                END AS notes
            FROM awards a
            JOIN vendors v ON a.vendor_id = v.vendor_id
            JOIN agencies g ON a.agency_id = g.agency_id
            GROUP BY v.vendor_id, v.vendor_name, v.vendor_type
            """
        )
        conn.execute(
            """
            CREATE OR REPLACE VIEW opportunity_scores AS
            SELECT
                o.opportunity_id,
                o.title,
                g.agency_name AS agency,
                g.office,
                o.notice_type,
                o.posted_date,
                o.due_date,
                o.naics,
                o.psc,
                o.keywords,
                o.url,
                CASE WHEN g.priority_tier = 1 THEN 25 WHEN g.priority_tier = 2 THEN 15 ELSE 5 END AS agency_relevance,
                CASE
                    WHEN LOWER(o.keywords) LIKE '%ai%' OR LOWER(o.keywords) LIKE '%rag%' THEN 25
                    WHEN LOWER(o.keywords) LIKE '%power bi%' OR LOWER(o.keywords) LIKE '%data%' THEN 20
                    ELSE 12
                END AS technical_match,
                16 AS contract_size_fit,
                CASE WHEN o.notice_type IN ('RFI', 'Sources Sought') THEN 18 ELSE 12 END AS teaming_potential,
                CASE WHEN o.due_date BETWEEN DATE '2025-06-15' AND DATE '2025-08-31' THEN 10 ELSE 6 END AS timing_score,
                (
                    CASE WHEN g.priority_tier = 1 THEN 25 WHEN g.priority_tier = 2 THEN 15 ELSE 5 END
                    + CASE
                        WHEN LOWER(o.keywords) LIKE '%ai%' OR LOWER(o.keywords) LIKE '%rag%' THEN 25
                        WHEN LOWER(o.keywords) LIKE '%power bi%' OR LOWER(o.keywords) LIKE '%data%' THEN 20
                        ELSE 12
                    END
                    + 16
                    + CASE WHEN o.notice_type IN ('RFI', 'Sources Sought') THEN 18 ELSE 12 END
                    + CASE WHEN o.due_date BETWEEN DATE '2025-06-15' AND DATE '2025-08-31' THEN 10 ELSE 6 END
                ) AS total_score
            FROM opportunities o
            JOIN agencies g ON o.agency_id = g.agency_id
            """
        )

    return settings.database_path


def ensure_database(settings: Settings | None = None) -> Path:
    settings = settings or load_settings()
    if not settings.database_path.exists():
        return seed_database(settings)
    return settings.database_path
