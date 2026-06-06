from __future__ import annotations

import streamlit as st

from govcon_radar.config import Settings
from govcon_radar.queries import agency_summary, capability_markets, contractor_rankings, executive_kpis
from govcon_radar.ui.charts import agency_obligation_bar, capability_pipeline_bar
from govcon_radar.ui.layout import format_currency, format_rate, render_page_header


def render_executive_overview(settings: Settings, fiscal_year: int) -> None:
    render_page_header(
        "Executive Overview",
        "Portfolio-level spending, competition, and partner opportunity signals.",
    )

    kpis = executive_kpis(fiscal_year, settings)
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total obligations", format_currency(kpis["obligations"]))
    col2.metric("Award count", f"{kpis['award_count']:,.0f}")
    col3.metric("Small-business obligations", format_currency(kpis["small_business_obligations"]))
    col4.metric("Avg competition rate", format_rate(kpis["competition_rate"]))

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
    st.dataframe(
        contractors[
            [
                "contractor",
                "primary_agency",
                "core_capability",
                "total_obligations",
                "composite_score",
                "small_business_partnering_rate",
            ]
        ].head(settings.raw["dashboards"]["executive_overview"]["top_contractors_limit"]),
        use_container_width=True,
        hide_index=True,
    )
