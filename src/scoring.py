from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from govcon_radar.config import PROJECT_ROOT


def load_scoring_weights(path: str | Path = PROJECT_ROOT / "config" / "scoring_weights.yml") -> dict[str, Any]:
    with Path(path).open("r", encoding="utf-8") as weights_file:
        return yaml.safe_load(weights_file)


def weighted_score(components: dict[str, float], weights: dict[str, float]) -> float:
    total_weight = sum(weights.values())
    if total_weight == 0:
        return 0
    return round(sum(components.get(name, 0) * weight for name, weight in weights.items()) / total_weight, 1)
