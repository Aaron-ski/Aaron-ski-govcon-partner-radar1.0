from govcon_radar.config import load_settings
from govcon_radar.db import ensure_database
from govcon_radar.ui.pages.prime_contractor_intelligence import render_prime_contractor_intelligence


settings = load_settings()
ensure_database(settings)
render_prime_contractor_intelligence(settings)
