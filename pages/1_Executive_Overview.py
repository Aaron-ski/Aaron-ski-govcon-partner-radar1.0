import streamlit as st

from govcon_radar.config import load_settings
from govcon_radar.db import ensure_database
from govcon_radar.ui.pages.executive_overview import render_executive_overview


settings = load_settings()
ensure_database(settings)
fiscal_year = st.sidebar.selectbox("Fiscal year", settings.fiscal_years, index=settings.fiscal_years.index(settings.default_fiscal_year))
render_executive_overview(settings, int(fiscal_year))
