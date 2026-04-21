
import sqlite3

conn = sqlite3.connect("app.db")
cur = conn.cursor()

tables = [
    "research_runs",
    "evidence_items",
    "themes",
    "insights",
    "personas",
    "journey_maps",
    "recommendations",
    "reports",
    "approvals",
    "trace_records",
]

for table in tables:
    try:
        count = cur.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        print(f"{table}: {count}")
    except Exception as e:
        print(f"{table}: ERROR -> {e}")

conn.close()