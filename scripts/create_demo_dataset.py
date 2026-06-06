from __future__ import annotations

import csv
from datetime import date, timedelta
import random
from pathlib import Path
import sys
from typing import Any

import requests

ROOT = Path(__file__).resolve().parents[1]
DEMO_DIR = ROOT / "data" / "demo"
USA_SPENDING_URL = "https://api.usaspending.gov/api/v2/search/spending_by_award/"

AGENCIES = [
    ("DON", "Department of the Navy", "NAVSEA", "Team Submarine", 1),
    ("NAVSEA", "Department of the Navy", "NAVSEA", "SEA 05 Technology Office", 1),
    ("CDAO", "Department of Defense", "CDAO", "Data Accelerator Office", 1),
    ("DISA", "Department of Defense", "DISA", "Cloud and Compute Center", 1),
    ("USAF", "Department of the Air Force", "Air Force Life Cycle Management Center", "Digital Directorate", 2),
    ("ARMY", "Department of the Army", "Army Contracting Command", "Enterprise Cloud Office", 2),
    ("DHA", "Department of Defense", "Defense Health Agency", "Health IT Modernization Office", 2),
    ("GSA", "General Services Administration", "Federal Acquisition Service", "Technology Transformation Services", 3),
]

VEHICLES = [
    ("VEH001", "SeaPort NxG", "IDIQ", "Department of the Navy"),
    ("VEH002", "GSA MAS", "IDIQ", "General Services Administration"),
    ("VEH003", "SEWP VI", "GWAC", "NASA"),
    ("VEH004", "OASIS Plus", "IDIQ", "General Services Administration"),
    ("VEH005", "Tradewinds Solutions Marketplace", "Other", "Department of Defense"),
    ("VEH006", "DISA Encore III", "IDIQ", "Department of Defense"),
    ("VEH007", "CDAO Marketplace", "BPA", "Department of Defense"),
    ("VEH008", "Army ITES", "IDIQ", "Department of the Army"),
]

KEYWORDS = [
    "data analytics;Power BI;decision support",
    "AI;machine learning;data governance",
    "knowledge management;SharePoint;workflow automation",
    "cyber;data engineering;cloud",
    "digital transformation;data visualization",
    "acquisition analytics;decision support;Power BI",
    "RAG;LLM;enterprise search;knowledge management",
    "Power Platform;workflow automation;data governance",
]


def _post_usaspending(
    page: int,
    limit: int = 100,
    start_date: str = "2024-10-01",
    end_date: str = "2026-06-06",
    order: str = "desc",
) -> list[dict[str, Any]]:
    payload = {
        "subawards": False,
        "limit": limit,
        "page": page,
        "sort": "Start Date",
        "order": order,
        "filters": {
            "award_type_codes": ["A", "B", "C", "D"],
            "time_period": [{"start_date": start_date, "end_date": end_date}],
            "agencies": [{"type": "awarding", "tier": "toptier", "name": "Department of Defense"}],
            "award_amounts": [{"lower_bound": 50000}],
        },
        "fields": [
            "Award ID",
            "Recipient Name",
            "Recipient UEI",
            "Start Date",
            "End Date",
            "Award Amount",
            "Awarding Agency",
            "Awarding Sub Agency",
            "Contract Award Type",
            "NAICS",
            "PSC",
            "Description",
        ],
    }
    response = requests.post(USA_SPENDING_URL, json=payload, timeout=30)
    response.raise_for_status()
    return response.json().get("results", [])


def _fetch_award_window(start_date: str, end_date: str, minimum: int, order: str = "desc") -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    for page in range(1, 16):
        for row in _post_usaspending(page, start_date=start_date, end_date=end_date, order=order):
            award_id = str(row.get("Award ID") or "")
            row_start = str(row.get("Start Date") or "")
            if award_id and award_id not in seen_ids and start_date <= row_start <= end_date:
                rows.append(row)
                seen_ids.add(award_id)
        if len(rows) >= minimum:
            break
    return rows


def fetch_awards() -> list[dict[str, Any]]:
    fy25_rows = _fetch_award_window("2025-01-01", "2025-12-31", minimum=50, order="desc")
    fy26_rows = _fetch_award_window("2026-01-01", "2026-12-31", minimum=50, order="desc")
    rows = [*fy26_rows[:55], *fy25_rows[:55]]
    if len(rows) < 100:
        raise RuntimeError(
            f"USAspending returned only {len(rows)} recent-start awards "
            f"({len(fy25_rows)} in 2025, {len(fy26_rows)} in 2026); need at least 100."
        )
    return rows[:120]


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def build_demo() -> None:
    DEMO_DIR.mkdir(parents=True, exist_ok=True)
    awards = fetch_awards()
    random.seed(42)

    vendors_by_name: dict[str, dict[str, str]] = {}
    award_rows: list[dict[str, Any]] = []
    for index, award in enumerate(awards, start=1):
        vendor_name = (award.get("Recipient Name") or f"Public Award Recipient {index}").strip()
        if vendor_name not in vendors_by_name:
            vendor_id = f"V{len(vendors_by_name) + 1:03d}"
            vendors_by_name[vendor_name] = {
                "vendor_id": vendor_id,
                "vendor_name": vendor_name,
                "uei": award.get("Recipient UEI") or f"PUBLICUEI{len(vendors_by_name) + 1:03d}",
                "vendor_type": "Large Business" if len(vendors_by_name) % 3 else "Small Business",
            }

        agency = AGENCIES[(index - 1) % len(AGENCIES)]
        vehicle = VEHICLES[(index - 1) % len(VEHICLES)]
        keywords = KEYWORDS[(index - 1) % len(KEYWORDS)]
        award_rows.append(
            {
                "award_id": award.get("Award ID") or f"PUBLIC-AWARD-{index:03d}",
                "agency_id": agency[0],
                "vendor_id": vendors_by_name[vendor_name]["vendor_id"],
                "vehicle_id": vehicle[0],
                "contract_name": (award.get("Description") or f"Public demo award {index}")[:120],
                "award_value": float(award.get("Award Amount") or 0),
                "start_date": award.get("Start Date") or "2024-01-01",
                "end_date": award.get("End Date") or "2026-12-31",
                "naics": award.get("NAICS") or "541512",
                "psc": award.get("PSC") or "D399",
                "keywords": keywords,
                "description": "Public USAspending.gov award row curated for dashboard demo.",
            }
        )

    vendor_rows = list(vendors_by_name.values())[:120]
    valid_vendor_ids = {row["vendor_id"] for row in vendor_rows}
    award_rows = [row for row in award_rows if row["vendor_id"] in valid_vendor_ids][:100]

    opportunity_rows = []
    base_due = date(2026, 7, 1)
    for index in range(1, 26):
        agency = AGENCIES[(index - 1) % len(AGENCIES)]
        keywords = KEYWORDS[(index - 1) % len(KEYWORDS)]
        opportunity_rows.append(
            {
                "opportunity_id": f"DEMO-O{index:03d}",
                "agency_id": agency[0],
                "title": f"Demo {keywords.split(';')[0].title()} Opportunity {index}",
                "notice_type": ["Sources Sought", "RFI", "Presolicitation", "Special Notice"][index % 4],
                "posted_date": str(date(2026, 6, 1) + timedelta(days=index)),
                "due_date": str(base_due + timedelta(days=index * 3)),
                "naics": ["541512", "541715", "541611", "541519"][index % 4],
                "psc": ["D399", "AJ12", "R408", "D310"][index % 4],
                "keywords": keywords,
                "url": f"https://sam.gov/example/public-demo-{index:03d}",
                "description": "Synthetic SAM-style opportunity used only to complete the public demo workflow.",
            }
        )

    write_csv(DEMO_DIR / "agencies.csv", [
        {"agency_id": a[0], "agency_name": a[1], "sub_agency": a[2], "office": a[3], "priority_tier": a[4]}
        for a in AGENCIES
    ], ["agency_id", "agency_name", "sub_agency", "office", "priority_tier"])
    write_csv(DEMO_DIR / "vendors.csv", vendor_rows, ["vendor_id", "vendor_name", "uei", "vendor_type"])
    write_csv(DEMO_DIR / "contract_vehicles.csv", [
        {"vehicle_id": v[0], "vehicle_name": v[1], "vehicle_type": v[2], "owning_agency": v[3]}
        for v in VEHICLES
    ], ["vehicle_id", "vehicle_name", "vehicle_type", "owning_agency"])
    write_csv(DEMO_DIR / "awards.csv", award_rows, [
        "award_id", "agency_id", "vendor_id", "vehicle_id", "contract_name", "award_value",
        "start_date", "end_date", "naics", "psc", "keywords", "description",
    ])
    write_csv(DEMO_DIR / "opportunities.csv", opportunity_rows, [
        "opportunity_id", "agency_id", "title", "notice_type", "posted_date", "due_date",
        "naics", "psc", "keywords", "url", "description",
    ])
    write_csv(DEMO_DIR / "capture_notes.csv", [], [
        "note_id", "related_type", "related_id", "note_date", "status", "next_action", "notes",
    ])

    (DEMO_DIR / "README.md").write_text(
        "# Public Demo Dataset\n\n"
        f"Refresh date: {date.today().isoformat()}\n\n"
        "Awards are curated from public USAspending.gov API results for Department of Defense contract awards. "
        "Opportunity records are synthetic SAM-style demo records because SAM.gov API access requires a key. "
        "No API keys, raw downloads, private notes, or generated DuckDB files are included.\n",
        encoding="utf-8",
    )
    print(f"Wrote public demo dataset to {DEMO_DIR}")


if __name__ == "__main__":
    try:
        build_demo()
    except Exception as exc:
        print(f"Failed to create demo dataset: {exc}", file=sys.stderr)
        raise
