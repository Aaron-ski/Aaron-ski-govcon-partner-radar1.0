from govcon_radar.config import load_settings


def test_load_settings_has_expected_phase_one_defaults():
    settings = load_settings()

    assert settings.app_title == "GovCon Partner Radar"
    assert settings.default_fiscal_year == 2024
    assert "agency_spending" in settings.sample_paths
    assert settings.database_path.name == "govcon_radar.duckdb"
