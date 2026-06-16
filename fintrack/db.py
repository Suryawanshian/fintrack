
import sqlite3
import os

#Path to the database file
DB_PATH = "fintrack.db"

def get_connection():
    """  Create and return a connection to the SQLite database"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    """Read schema.sql and create all tables in the database"""
    schema_path = os.path.join("sql", "schema.sql")

    with open(schema_path, "r") as f:
        schema_sql = f.read()

    conn = get_connection()
    conn.executescript(schema_sql)
    conn.commit()
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


def insert_default_categories():
    """Insert default spending categories with budgets."""
    categories = [
        ("Food", 4000),
        ("Transport",2000),
        ("Shopping", 5000),
        ("Entertainment",2000),
        ("Groceries",3000),
        ("Uncategorized", 0),

    ]

    conn = get_connection()
     
    conn.executemany(
        "INSERT OR IGNORE INTO categories (name, budget) VALUES (?, ?)",
        categories
    )

    conn.commit()
    conn.close()
    print("Default categories inserted")

if __name__ == "__main__":
    #Create tables
    create_tables()

    insert_default_categories()

    # Insert 3 test transactions
    insert_transaction("2024-01-03",42.50,"Starbucks", "Food", "HDFC", "coffee")
    insert_transaction("2024-01-04",1200.00,"Amazon", "Shopping", "HDFC", "keyboard")
    insert_transaction("2024-01-05",350.00, "Zomato", "Food", "HDFC", "dinner")

    #Fetch and print all transactions
    print("\n--- All transactions ---")
    rows = get_all_transactions()
    for row in rows:
        print(f"{row['date']} | INR{row['amount']} | {row['merchant']} | {row['category']}")

    #Fetch transactions over 500
    print("\n--- Transactions over INR500 ---")
    big = get_transactions_over(500)
    for row in big:
        print(f"{row['date']} | INR{row['amount']} | {row['merchant']}")