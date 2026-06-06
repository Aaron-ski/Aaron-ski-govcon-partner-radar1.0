from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG_PATH = PROJECT_ROOT / "config" / "app.yaml"


@dataclass(frozen=True)
class Settings:
    raw: dict[str, Any]
    project_root: Path = PROJECT_ROOT

    @property
    def app_title(self) -> str:
        return str(self.raw["app"]["title"])

    @property
    def app_subtitle(self) -> str:
        return str(self.raw["app"]["subtitle"])

    @property
    def default_fiscal_year(self) -> int:
        return int(self.raw["app"]["default_fiscal_year"])

    @property
    def fiscal_years(self) -> list[int]:
        return [int(year) for year in self.raw["app"]["fiscal_years"]]

    @property
    def database_path(self) -> Path:
        return self.project_root / str(self.raw["database"]["path"])

    @property
    def sample_paths(self) -> dict[str, Path]:
        return {
            name: self.project_root / str(path)
            for name, path in self.raw["sample_data"].items()
        }

    @property
    def score_weights(self) -> dict[str, float]:
        return {
            name: float(weight)
            for name, weight in self.raw["scoring"]["weights"].items()
        }


@lru_cache(maxsize=1)
def load_settings(config_path: str | Path = DEFAULT_CONFIG_PATH) -> Settings:
    path = Path(config_path)
    with path.open("r", encoding="utf-8") as config_file:
        raw = yaml.safe_load(config_file)
    return Settings(raw=raw)
