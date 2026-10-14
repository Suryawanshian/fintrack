
import sqlite3
import os

#Path to the database file
DB_PATH = "fintrack.db"

def get_connection():
    """  Create and return a connection to the SQLite database"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def create_tables(conn=None):
    """Read schema.sql and create all tables in the database"""
    schema_path = os.path.join("sql", "schema.sql")

    with open(schema_path, "r") as f:
        schema_sql = f.read()

    close_after = False
    if conn is None:
        conn = get_connection()
        close_after= True

    
    conn.executescript(schema_sql)
    conn.commit()
    if close_after:
        conn.close()
    
    print("Database tables created successfully")




def insert_transaction(date, amount, merchant, category, account, note):
    """Insert a single transaction into the database."""
    conn = get_connection()

    sql = """
        INSERT INTO transactions (date, amount, merchant, category, account, note)
        VALUES(?, ?, ?, ?, ?, ?)
        """
    
    conn.execute(sql, (date, amount, merchant, category, account, note))
    conn.commit()
    conn.close()
    print(f"Inserted: {merchant} - {amount}")

def get_all_transactions():
    """Fetch all transactions from the database."""
    conn = get_connection()

    rows = conn.execute("SELECT * FROM transactions").fetchall()
    conn.close()

    return rows

def get_transactions_over(amount):
    """Fetch transactions above a certain amount."""
    conn = get_connection()

    rows = conn.execute(
        "SELECT date, amount, merchant, category FROM transactions WHERE amount > ?",
        (amount,)
    ).fetchall()

    conn.close()
    return rows


def insert_default_categories(conn=None):
    """Insert default spending categories with budgets."""
    categories = [
        ("Food", 4000),
        ("Transport",2000),
        ("Shopping", 5000),
        ("Entertainment",2000),
        ("Groceries",3000),
        ("Uncategorized", 0),

    ]
    close_after=False
    if conn is None:
        conn = get_connection()
        close_after = True

     
    conn.executemany(
        "INSERT OR IGNORE INTO categories (name, budget) VALUES (?, ?)",
        categories
    )

    conn.commit()
    if close_after:
        conn.close()
    
    print("Default categories inserted")

if __name__ == "__main__":
    #Create tables
    create_tables()

    insert_default_categories()

    # Insert 3 test transactions
    insert_transaction("2024-01-03",42.50,"Starbucks", "Food", "HSBC", "coffee")
    insert_transaction("2024-01-04",1200.00,"Amazon", "Shopping", "HSBC", "keyboard")
    insert_transaction("2024-01-05",350.00, "Deliveroo", "Food", "HSBC", "dinner")

    #Fetch and print all transactions
    print("\n--- All transactions ---")
    rows = get_all_transactions()
    for row in rows:
        print(f"{row['date']} | EUR{row['amount']} | {row['merchant']} | {row['category']}")

    #Fetch transactions over 500
    print("\n--- Transactions over EUR500 ---")
    big = get_transactions_over(500)
    for row in big:
        print(f"{row['date']} | EUR{row['amount']} | {row['merchant']}")


def insert_transactions(df, conn):
    """
    Insert a cleaned DataFrame into the transactions table.
    Uses executemany for speed - inserts all rows in one operation.
    """

    # Convert DataFrame rows into a list of Tuples
    # Each tuple is one row to insert

    rows =[
        (
            row["date"],
            row["amount"],
            row["merchant"],
            row["category"],
            row["account"],
            row["note"]
        )
        for row in df.to_dict("records")
    ]

    sql = """
            INSERT INTO transactions( date, amount, merchant, category, account, note)
            VALUES(?,?,?,?,?,?)
        """
    conn.executemany(sql, rows)
    conn.commit()
    print(f"Inserted {len(rows)} transactions into database")
    