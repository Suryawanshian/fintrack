import sqlite3
def spending_by_category(conn, month: str) -> list:
    """
    Returns total spending for a month by category.
    month format: 'YYYY-MM' example '2024-01' 
    """
    sql = """
            SELECT
                category,
                SUM(amount) AS total_spent,
                COUNT(*) AS num_transactions
            FROM transactions
            WHERE strftime('%Y-%m', date) = ?
            GROUP BY category
            ORDER BY total_spent DESC

          """
    rows = conn.execute(sql, (month,)).fetchall()
    return [dict(row) for row in rows]

def top_merchants(conn, n: int = 10) -> list:
    """
    Returns top n merchnats by total spending.
    n defaults to 10 if not specified.
    """
    sql="""
        SELECT 
            merchant,
            SUM(amount) AS total_spent,
            COUNT(*) AS num_visits
        FROM transactions
        WHERE merchant IS NOT NULL
        GROUP BY merchant
        ORDER BY total_spent DESC
        LIMIT ?
    """
    rows = conn.execute(sql, (n,)).fetchall()
    return [dict(row) for row in rows]

def monthly_totals(conn) -> list:
    """
    Returns total spending for month
    """
    sql ="""
        SELECT
            strftime('%Y-%m', date) AS month,
            SUM(amount) AS total_spent,
            COUNT(*) AS num_transactions
        FROM transactions
        Group BY month
        ORDER BY month ASC

       """

    rows= conn.execute(sql).fetchall()
    return [dict(row) for row in rows]

def daily_average(conn, month: str) -> float:
    """
    Returns average daily spending for a month
    """

    sql = """
          SELECT
                ROUND(SUM(amount) / COUNT(DISTINCT DATE), 2) AS daily_average
          FROM transactions
          WHERE strftime('%Y-%m', date) = ?

          """
    row = conn.execute(sql, (month,)).fetchone()
    return row["daily_average"] if row else 0.0

def savings_rate(conn, income: float, month: str) -> float:
    """
    Return savings rate as a percentage.
    savings rate = (income - spending) / income * 100

    """
    sql ="""
            SELECT SUM(amount) AS total_spent
            FROM transactions
            WHERE strftime('%Y-%m', date) = ?
        """

    row = conn.execute(sql, (month, )).fetchone()
    total_spent = row["total_spent"] if row["total_spent"] else 0.0
    savings = income - total_spent
    rate = (savings / income) * 100
    return round(rate, 2)

if __name__ == "__main__":
    from fintrack.db import get_connection

    conn = get_connection()

    # Test 1 - spending by category
    print("\n--- Spending By Category (January 2024) ---")
    categories = spending_by_category(conn, "2024-01")
    for cat in categories:
        print(f"{cat['category']:<20} EUR{cat['total_spent']:.2f} ({cat['num_transactions']} transactions)")

    # Test 2 - top merchants
    print("\n---- Top 5 merchants ----")
    merchants = top_merchants(conn, n=5)
    for m in merchants:
        print(f"{m['merchant']:<20} EUR{m['total_spent']:.2f} ({m['num_visits']} visits)")

    # Test 3 - monthly totals
    print("\n--- Monthly totals ---")
    months = monthly_totals(conn)
    for month in months:
        print(f"{month['month']} EUR{month['total_spent']:.2f} ({month['num_transactions']} transactions)")   

    # Test 4 - daily average
    print("\n--- Daily Average (January 2024) ---")
    avg = daily_average(conn, "2024-01")
    print(f"Daily average: EUR{avg:.2f}")

    # Test 5 - savings rate
    print("\n--- Savings Rate (January 2024) ---")
    rate = savings_rate(conn, income=5000.0, month="2024-01")
    print(f"Savings rate: {rate}%")

    conn.close
        