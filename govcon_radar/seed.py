from __future__ import annotations

from govcon_radar.config import load_settings
from govcon_radar.db import seed_database


def main() -> None:
    settings = load_settings()
    database_path = seed_database(settings)
    print(f"Seeded DuckDB database at {database_path}")


if __name__ == "__main__":
    main()
