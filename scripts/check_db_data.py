"""检查 app.db 中的实际数据"""
import sqlite3

conn = sqlite3.connect("app.db")
cur = conn.cursor()

# 列出所有表
tables = cur.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
print("=== 所有表 ===")
for t in tables:
    name = t[0]
    count = cur.execute(f"SELECT COUNT(*) FROM [{name}]").fetchone()[0]
    print(f"  {name}: {count} rows")

print()

# 查看 research_runs 表
print("=== research_runs ===")
rows = cur.execute("SELECT run_id, current_stage, user_request FROM research_runs ORDER BY rowid DESC LIMIT 5").fetchall()
for r in rows:
    print(f"  run_id={r[0]}, stage={r[1]}, request={r[2][:50]}")

print()

# 查看最新 run_id 的各类数据
if rows:
    latest_run_id = rows[0][0]
    print(f"=== 最新 run_id: {latest_run_id} ===")
    
    for table_name in ["evidence_items", "themes", "insights", "personas", "journey_maps", "recommendations", "reports", "approvals", "eval_records"]:
        try:
            count = cur.execute(f"SELECT COUNT(*) FROM [{table_name}] WHERE run_id=?", (latest_run_id,)).fetchone()[0]
            print(f"  {table_name}: {count}")
        except Exception as e:
            print(f"  {table_name}: ERROR - {e}")

    # 检查所有 run_id 的数据分布
    print()
    print("=== 所有 run_id 的证据数量 ===")
    all_runs = cur.execute("SELECT run_id, current_stage FROM research_runs ORDER BY rowid").fetchall()
    for run_id, stage in all_runs:
        try:
            ev_count = cur.execute("SELECT COUNT(*) FROM evidence_items WHERE run_id=?", (run_id,)).fetchone()[0]
            th_count = cur.execute("SELECT COUNT(*) FROM themes WHERE run_id=?", (run_id,)).fetchone()[0]
            ins_count = cur.execute("SELECT COUNT(*) FROM insights WHERE run_id=?", (run_id,)).fetchone()[0]
            print(f"  {run_id}: stage={stage}, evidence={ev_count}, themes={th_count}, insights={ins_count}")
        except Exception as e:
            print(f"  {run_id}: ERROR - {e}")

conn.close()
