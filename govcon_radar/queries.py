from __future__ import annotations

import pandas as pd

from govcon_radar.config import Settings, load_settings
from govcon_radar.db import connect, ensure_database


def _fetch_df(sql: str, params: list[object] | None = None, settings: Settings | None = None) -> pd.DataFrame:
    settings = settings or load_settings()
    ensure_database(settings)
    with connect(settings, read_only=True) as conn:
        return conn.execute(sql, params or []).fetchdf()


def executive_kpis(fiscal_year: int, settings: Settings | None = None) -> dict[str, float]:
    df = _fetch_df(
        """
        SELECT
            SUM(obligations) AS obligations,
            SUM(award_count) AS award_count,
            SUM(small_business_obligations) AS small_business_obligations,
            AVG(competition_rate) AS competition_rate
        FROM agency_spending
        WHERE fiscal_year = ?
        """,
        [fiscal_year],
        settings,
    )
    row = df.iloc[0]
    return {
        "obligations": float(row["obligations"] or 0),
        "award_count": float(row["award_count"] or 0),
        "small_business_obligations": float(row["small_business_obligations"] or 0),
        "competition_rate": float(row["competition_rate"] or 0),
    }


def agency_summary(fiscal_year: int, settings: Settings | None = None) -> pd.DataFrame:
    return _fetch_df(
        """
        SELECT agency, obligations, award_count, small_business_obligations, competition_rate
        FROM agency_year_summary
        WHERE fiscal_year = ?
        ORDER BY obligations DESC
        """,
        [fiscal_year],
        settings,
    )


def spending_by_vehicle(fiscal_year: int, agency: str | None = None, settings: Settings | None = None) -> pd.DataFrame:
    where = "WHERE fiscal_year = ?"
    params: list[object] = [fiscal_year]
    if agency and agency != "All Agencies":
        where += " AND agency = ?"
        params.append(agency)
    return _fetch_df(
        f"""
        SELECT contract_vehicle, SUM(obligations) AS obligations, SUM(award_count) AS award_count
        FROM agency_spending
        {where}
        GROUP BY contract_vehicle
        ORDER BY obligations DESC
        """,
        params,
        settings,
    )


def spending_detail(fiscal_year: int, agency: str | None = None, settings: Settings | None = None) -> pd.DataFrame:
    where = "WHERE fiscal_year = ?"
    params: list[object] = [fiscal_year]
    if agency and agency != "All Agencies":
        where += " AND agency = ?"
        params.append(agency)
    return _fetch_df(
        f"""
        SELECT agency, subagency, naics, psc, contract_vehicle, obligations, award_count,
               small_business_obligations, competition_rate
        FROM agency_spending
        {where}
        ORDER BY obligations DESC
        """,
        params,
        settings,
    )


def contractor_rankings(settings: Settings | None = None) -> pd.DataFrame:
    return _fetch_df(
        """
        SELECT contractor, headquarters, primary_agency, core_capability, total_obligations,
               award_count, small_business_partnering_rate, past_performance_score,
               cyber_readiness_score, agency_alignment_score, partner_fit_score,
               composite_score, notes
        FROM contractor_rankings
        ORDER BY composite_score DESC, total_obligations DESC
        """,
        settings=settings,
    )


def capability_markets(settings: Settings | None = None) -> pd.DataFrame:
    return _fetch_df(
        """
        SELECT capability, agency, estimated_pipeline, competition_intensity,
               small_business_pull, priority_signal
        FROM capability_markets
        ORDER BY estimated_pipeline DESC
        """,
        settings=settings,
    )
