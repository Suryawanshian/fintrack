import time
import sqlite3
from fintrack.db import get_connection
from fintrack.clean import clean_transactions
from fintrack.ingest import load_csv

def load_large_dataset():
    """Load 10,000 transactions into a fresh database."""

    # create fresh in-memory database
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row

    # read schema
    with open("sql/schema.sql", "r") as f:
        conn.executescript(f.read())

    # load and clean large CSV

    df = load_csv("data/large_transactions.csv")
    df_clean = clean_transactions(df)

    # insert all rows

    rows = [
        (row["date"], row["amount"], row["merchant"],
         row["category"], row["account"], row["note"])
        for row in df_clean.to_dict("records")
    ]

    conn.executemany(
        "INSERT INTO transactions (date, amount, merchant, category, account, note) VALUES (?, ?, ?, ?, ?, ?)",
        rows
    )
    conn.commit()
    print(f"Loaded {len(rows)} transactions into test database")
    return conn 

def benchmark_query(conn, sql, params, label, runs=5):
    """Run a query multiple times and report average time."""

    times = []
    for _ in range(runs):
        start = time.perf_counter()
        conn.execute(sql, params).fetchall()
        end = time.perf_counter()
        times.append(end - start)

    avg_ms = (sum(times) / len(times)) * 1000
    print(f"{label}: {avg_ms:.2f}ms average ({runs} runs)")
    return avg_ms

def run_benchmarks():
    """Benchmark queries with and without indexes."""
    conn = load_large_dataset()

    queries = [
        (
            "Monthly spending by category",
            """SELECT category, SUM(amount)
            FROM transactions
            WHERE strftime('%Y-%m', date) = ?
            GROUP BY category""",
            ("2023-06",)
        ),
         (
            "Top merchants",
            """SELECT merchant, SUM(amount) as total
               FROM transactions
               GROUP BY merchant
               ORDER BY total DESC
               LIMIT 10""",
            ()
        ),
        (
            "Date range filter",
            """SELECT COUNT(*) FROM transactions
               WHERE date BETWEEN ? AND ?""",
            ("2023-01-01", "2023-06-30")
        )
    ] 

    print("\n=== WITHOUT INDEXES ===")
    for label, sql, params in queries:
        benchmark_query(conn, sql, params, label)

    print("\n=== ADDING INDEXES ===")
    conn.execute("CREATE INDEX idx_date ON transactions(date)")
    conn.execute("CREATE INDEX idx_category ON transactions(category)")
    conn.execute("CREATE INDEX idx_date_cat ON transactions(date, category)")
    conn.commit()
    print("Indexes created") 

    print("\n=== WITH INDEXES ===")
    for label, sql, params in queries:
        benchmark_query(conn, sql, params, label)
    
    conn.close()

if __name__ == "__main__":
    run_benchmarks()