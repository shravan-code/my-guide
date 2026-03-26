import sqlite3


def safe_text(value):
    return str(value).encode("ascii", "ignore").decode()


conn = sqlite3.connect("scenarios.db")
cursor = conn.cursor()

print(
    "Total scenarios:", cursor.execute("SELECT COUNT(*) FROM scenarios").fetchone()[0]
)
print("\nScenarios by technology:")
for row in cursor.execute(
    "SELECT technology, COUNT(*) FROM scenarios GROUP BY technology ORDER BY COUNT(*) DESC"
):
    print(f"  {safe_text(row[0])}: {row[1]}")

print("\nSample scenarios (first 5):")
print(f"{'ID':<4} {'Technology':<12} {'Name':<40} {'Code Snippet'}")
print("-" * 100)
for row in cursor.execute(
    "SELECT id, technology, scenario_name, substr(code_snippet,1,50) FROM scenarios LIMIT 5"
):
    code_preview = safe_text((row[3] or "")[:30])
    print(
        f"{row[0]:<4} {safe_text(row[1]):<12} {safe_text(row[2])[:40]:<40} {code_preview}"
    )

conn.close()
