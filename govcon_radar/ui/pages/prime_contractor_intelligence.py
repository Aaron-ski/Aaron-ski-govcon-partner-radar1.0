from __future__ import annotations

import streamlit as st

from govcon_radar.config import Settings
from govcon_radar.queries import contractor_rankings
from govcon_radar.ui.charts import contractor_score_scatter
from govcon_radar.ui.layout import format_currency, render_page_header
from src.exports import csv_download


def render_prime_contractor_intelligence(settings: Settings) -> None:
    render_page_header(
        "Prime Contractor Intelligence",
        "Synthetic partner-fit view across agency alignment, cyber readiness, and teaming posture.",
    )

    contractors = contractor_rankings(settings)
    min_score = st.slider(
        "Minimum partner score",
        min_value=60,
        max_value=95,
        value=int(settings.raw["dashboards"]["prime_contractor_intelligence"]["minimum_partner_score"]),
        step=1,
    )
    filtered = contractors[contractors["composite_score"] >= min_score]

    col1, col2, col3 = st.columns(3)
    col1.metric("Visible contractors", f"{len(filtered):,}")
    col2.metric("Median partner score", f"{filtered['composite_score'].median():.1f}")
    col3.metric("Total obligations", format_currency(float(filtered["total_obligations"].sum())))

    st.subheader("Partner score vs. obligations")
    st.plotly_chart(contractor_score_scatter(filtered), use_container_width=True)

    with st.expander("Score explanation", expanded=True):
        st.write(
            "Partner score combines agency relationship, capability alignment, repeated wins, "
            "expiring contract timing, and likely subcontractor need using configurable YAML weights."
        )

    st.subheader("Prime contractor profiles")
    profiles = filtered[
        [
            "contractor",
            "headquarters",
            "primary_agency",
            "core_capability",
            "total_obligations",
            "small_business_partnering_rate",
            "past_performance_score",
            "cyber_readiness_score",
            "agency_alignment_score",
            "composite_score",
            "notes",
        ]
    ]
    st.dataframe(
        profiles,
        use_container_width=True,
        hide_index=True,
    )
    csv_download("Export prime targets", profiles, "prime_contractor_targets.csv")
