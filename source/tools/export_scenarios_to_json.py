from __future__ import annotations

import json
import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "scenarios.db"
OUTPUT_PATH = BASE_DIR.parent / "cheatsheets" / "comparison-data.json"
TECH_ORDER = ["PostgreSQL", "Pandas", "NumPy", "PySpark"]
TECH_KEYS = {
    "PostgreSQL": "postgresql",
    "Pandas": "pandas",
    "NumPy": "numpy",
    "PySpark": "pyspark",
}


def sort_key(category: str) -> tuple[int, str]:
    prefix, _, rest = category.partition(".")
    try:
        return int(prefix.strip()), rest.strip()
    except ValueError:
        return 9999, category


def normalize_category(value: str | None) -> str:
    if not value:
        return "Uncategorized"
    return value.replace("�", "-").replace("  ", " ").strip()


def main() -> None:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    rows = cur.execute(
        """
        SELECT category, scenario_name, technology, code_snippet
        FROM scenarios
        ORDER BY category, scenario_name, technology
        """
    ).fetchall()
    conn.close()

    grouped: dict[str, dict[str, dict[str, str]]] = {}
    for category, scenario_name, technology, code_snippet in rows:
        category_name = normalize_category(category)
        scenario_map = grouped.setdefault(category_name, {})
        tech_map = scenario_map.setdefault(scenario_name, {})
        tech_map[technology] = code_snippet or "N/A"

    payload = []
    for category_name in sorted(grouped, key=sort_key):
        scenarios = []
        for scenario_name, tech_map in grouped[category_name].items():
            entry = {"scenario": scenario_name}
            entry.update(
                {TECH_KEYS[tech]: tech_map.get(tech, "N/A") for tech in TECH_ORDER}
            )
            scenarios.append(entry)
        scenarios.sort(key=lambda item: item["scenario"].lower())
        payload.append({"category": category_name, "scenarios": scenarios})

    OUTPUT_PATH.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(f"Wrote {len(payload)} categories to {OUTPUT_PATH}")
    print(f"Total scenarios: {sum(len(item['scenarios']) for item in payload)}")


if __name__ == "__main__":
    main()
