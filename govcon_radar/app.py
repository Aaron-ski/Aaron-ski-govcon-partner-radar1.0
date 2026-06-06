from __future__ import annotations

from pathlib import Path
import sys

import streamlit as st

if __package__ is None or __package__ == "":
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from govcon_radar.config import load_settings
from govcon_radar.db import ensure_database
from govcon_radar.ui.layout import render_sidebar
from govcon_radar.ui.pages.agency_spending_explorer import render_agency_spending_explorer
from govcon_radar.ui.pages.executive_overview import render_executive_overview
from govcon_radar.ui.pages.prime_contractor_intelligence import render_prime_contractor_intelligence


def main() -> None:
    settings = load_settings()
    ensure_database(settings)

    st.set_page_config(
        page_title=settings.app_title,
        page_icon="bar_chart",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    selected_page, fiscal_year = render_sidebar(settings)

    if selected_page == "Executive Overview":
        render_executive_overview(settings, fiscal_year)
    elif selected_page == "Agency Spending Explorer":
        render_agency_spending_explorer(settings, fiscal_year)
    else:
        render_prime_contractor_intelligence(settings)


if __name__ == "__main__":
    main()
