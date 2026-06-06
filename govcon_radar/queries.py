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


def opportunity_kpis(settings: Settings | None = None) -> dict[str, float]:
    df = _fetch_df(
        """
        SELECT
            COUNT(*) AS opportunity_count,
            AVG(total_score) AS average_opportunity_score
        FROM opportunity_scores
        """,
        settings=settings,
    )
    row = df.iloc[0]
    return {
        "opportunity_count": float(row["opportunity_count"] or 0),
        "average_opportunity_score": float(row["average_opportunity_score"] or 0),
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
    where = "WHERE CAST(strftime(a.start_date, '%Y') AS INTEGER) = ?"
    params: list[object] = [fiscal_year]
    if agency and agency != "All Agencies":
        where += " AND g.agency_name = ?"
        params.append(agency)
    return _fetch_df(
        f"""
        SELECT cv.vehicle_name AS contract_vehicle, SUM(a.award_value) AS obligations, COUNT(*) AS award_count
        FROM awards a
        JOIN agencies g ON a.agency_id = g.agency_id
        JOIN contract_vehicles cv ON a.vehicle_id = cv.vehicle_id
        {where}
        GROUP BY cv.vehicle_name
        ORDER BY obligations DESC
        """,
        params,
        settings,
    )


def spending_detail(
    fiscal_year: int,
    agency: str | None = None,
    office: str | None = None,
    naics: str | None = None,
    psc: str | None = None,
    keyword: str | None = None,
    settings: Settings | None = None,
) -> pd.DataFrame:
    where = "WHERE CAST(strftime(a.start_date, '%Y') AS INTEGER) = ?"
    params: list[object] = [fiscal_year]
    if agency and agency != "All Agencies":
        where += " AND g.agency_name = ?"
        params.append(agency)
    if office and office != "All Offices":
        where += " AND g.office = ?"
        params.append(office)
    if naics and naics != "All NAICS":
        where += " AND a.naics = ?"
        params.append(naics)
    if psc and psc != "All PSC":
        where += " AND a.psc = ?"
        params.append(psc)
    if keyword:
        where += " AND LOWER(a.keywords || ' ' || a.description) LIKE ?"
        params.append(f"%{keyword.lower()}%")
    return _fetch_df(
        f"""
        SELECT
            g.agency_name AS agency,
            g.sub_agency AS subagency,
            g.office,
            v.vendor_name AS vendor,
            cv.vehicle_name AS contract_vehicle,
            a.contract_name,
            a.award_value AS obligations,
            a.start_date,
            a.end_date,
            a.naics,
            a.psc,
            a.keywords
        FROM awards a
        JOIN agencies g ON a.agency_id = g.agency_id
        JOIN vendors v ON a.vendor_id = v.vendor_id
        JOIN contract_vehicles cv ON a.vehicle_id = cv.vehicle_id
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


def opportunity_scores(settings: Settings | None = None) -> pd.DataFrame:
    return _fetch_df(
        """
        SELECT opportunity_id, title, agency, office, notice_type, posted_date, due_date,
               naics, psc, keywords, url, agency_relevance, technical_match,
               contract_size_fit, teaming_potential, timing_score, total_score
        FROM opportunity_scores
        ORDER BY total_score DESC, due_date ASC
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
