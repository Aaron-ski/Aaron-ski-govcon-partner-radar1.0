from __future__ import annotations

import streamlit as st

from govcon_radar.config import Settings
from govcon_radar.queries import agency_summary, spending_by_vehicle, spending_detail
from govcon_radar.ui.charts import agency_obligation_bar, vehicle_donut
from govcon_radar.ui.layout import format_currency, render_page_header


def render_agency_spending_explorer(settings: Settings, fiscal_year: int) -> None:
    render_page_header(
        "Agency Spending Explorer",
        "Drill into local sample obligations by agency, subagency, vehicle, NAICS, and PSC.",
    )

    agencies = agency_summary(fiscal_year, settings)
    agency_options = ["All Agencies", *agencies["agency"].tolist()]
    selected_agency = st.selectbox("Agency", agency_options)

    detail = spending_detail(fiscal_year, selected_agency, settings)
    vehicle = spending_by_vehicle(fiscal_year, selected_agency, settings)

    col1, col2, col3 = st.columns(3)
    col1.metric("Filtered obligations", format_currency(float(detail["obligations"].sum())))
    col2.metric("Filtered awards", f"{int(detail['award_count'].sum()):,}")
    col3.metric("Subagencies", f"{detail['subagency'].nunique():,}")

    left, right = st.columns([1.3, 1])
    with left:
        st.subheader("Agency ranking")
        st.plotly_chart(agency_obligation_bar(agencies), use_container_width=True)
    with right:
        st.subheader("Contract vehicle mix")
        st.plotly_chart(vehicle_donut(vehicle), use_container_width=True)

    st.subheader("Spending detail")
    st.dataframe(detail, use_container_width=True, hide_index=True)
