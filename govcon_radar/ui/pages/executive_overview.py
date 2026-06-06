from __future__ import annotations

import streamlit as st

from govcon_radar.config import Settings
from govcon_radar.queries import agency_summary, capability_markets, contractor_rankings, executive_kpis, opportunity_kpis
from govcon_radar.ui.charts import agency_obligation_bar, capability_pipeline_bar
from govcon_radar.ui.layout import format_currency, format_rate, render_page_header
from src.exports import csv_download


def render_executive_overview(settings: Settings, fiscal_year: int) -> None:
    render_page_header(
        "Executive Overview",
        "Portfolio-level spending, competition, and partner opportunity signals.",
    )

    kpis = executive_kpis(fiscal_year, settings)
    opportunity = opportunity_kpis(settings)
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Total obligations", format_currency(kpis["obligations"]))
    col2.metric("Award count", f"{kpis['award_count']:,.0f}")
    col3.metric("Opportunity count", f"{opportunity['opportunity_count']:,.0f}")
    col4.metric("Avg opportunity score", f"{opportunity['average_opportunity_score']:.1f}")
    col5.metric("Avg competition rate", format_rate(kpis["competition_rate"]))

    agencies = agency_summary(fiscal_year, settings)
    markets = capability_markets(settings)
    contractors = contractor_rankings(settings)

    left, right = st.columns([1.25, 1])
    with left:
        st.subheader("Agency obligation mix")
        st.plotly_chart(agency_obligation_bar(agencies), use_container_width=True)
    with right:
        st.subheader("Capability pipeline")
        st.plotly_chart(capability_pipeline_bar(markets), use_container_width=True)

    st.subheader("Top partner candidates")
    top_contractors = contractors[
        [
            "contractor",
            "primary_agency",
            "core_capability",
            "total_obligations",
            "composite_score",
            "small_business_partnering_rate",
        ]
    ].head(settings.raw["dashboards"]["executive_overview"]["top_contractors_limit"])
    st.dataframe(
        top_contractors,
        use_container_width=True,
        hide_index=True,
    )
    csv_download("Export partner candidates", top_contractors, "executive_partner_candidates.csv")
