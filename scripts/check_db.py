import sqlite3


def main():
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()

    print("=== research_runs ===")
    for row in cursor.execute("SELECT id, run_id, thread_id, current_stage FROM research_runs"):
        print(row)

    print("\n=== evidence_items ===")
    for row in cursor.execute("SELECT id, evidence_id, run_id, source_name FROM evidence_items"):
        print(row)

    print("\n=== insights ===")
    for row in cursor.execute("SELECT id, insight_id, run_id, severity FROM insights"):
        print(row)

    print("\n=== reports ===")
    for row in cursor.execute("SELECT id, run_id, title FROM reports"):
        print(row)

    conn.close()


if __name__ == "__main__":
    main()