import pandas as pd, sqlite3, pathlib

# 1. Load CSV (adjust path / delimiter as needed)
csv_path = pathlib.Path('data.csv')
if not csv_path.exists():
    raise FileNotFoundError('Place a CSV named data.csv in this folder.')

df = pd.read_csv(csv_path)

# 2. Create in‑memory SQLite DB and load DataFrame
conn = sqlite3.connect(':memory:')
# SQLite will infer column types; ensure a numeric column `value` exists.
df.to_sql('data', conn, index=False, if_exists='replace')

# 3. Simple aggregation via SQL
query = """
SELECT
    COUNT(*) AS row_count,
    SUM(value) AS total_value,
    AVG(value) AS avg_value
FROM data;
"""
result = conn.execute(query).fetchone()

# 4. Write a tiny report
report = (
    f"Rows: {result[0]}\n"
    f"Total value: {result[1]}\n"
    f"Average value: {result[2]:.2f}\n"
)
with open('report.txt', 'w') as f:
    f.write(report)

print('Report written to report.txt')

