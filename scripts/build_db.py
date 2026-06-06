from __future__ import annotations

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from govcon_radar.config import load_settings
from govcon_radar.db import seed_database


def main() -> None:
    database_path = seed_database(load_settings())
    print(f"Built DuckDB database at {database_path}")


if __name__ == "__main__":
    main()
