from __future__ import annotations

import streamlit as st

from govcon_radar.config import Settings


PAGES = [
    "Executive Overview",
    "Agency Spending Explorer",
    "Prime Contractor Intelligence",
]


def render_sidebar(settings: Settings) -> tuple[str, int]:
    st.sidebar.title(settings.app_title)
    st.sidebar.caption(settings.app_subtitle)
    selected_page = st.sidebar.radio("Dashboard", PAGES)
    fiscal_year = st.sidebar.selectbox(
        "Fiscal year",
        settings.fiscal_years,
        index=settings.fiscal_years.index(settings.default_fiscal_year),
    )
    st.sidebar.divider()
    st.sidebar.info(
        "Dashboard runtime uses local CSV/DuckDB data only. Demo records are curated public-data rows "
        "or clearly labeled synthetic workflow records; no live API calls are made during page load."
    )
    return selected_page, int(fiscal_year)


def render_page_header(title: str, subtitle: str) -> None:
    st.title(title)
    st.caption(subtitle)


def format_currency(value: float) -> str:
    if value >= 1_000_000_000:
        return f"${value / 1_000_000_000:.2f}B"
    if value >= 1_000_000:
        return f"${value / 1_000_000:.1f}M"
    return f"${value:,.0f}"


def format_rate(value: float) -> str:
    return f"{value * 100:.1f}%"
