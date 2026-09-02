
# FinTrack — My Learning Notes

## Commands I Use Every Day

- Activate venv: source venv/Scripts/activate
- Run pipeline: python run_pipeline.py
- Run analytics: python -m fintrack.analyze
- Delete Database: rm fintrack.db
- Git Workflow: git add . -> git commit -m "message" -> git push

# Concepts in my words

## venv
It is a virtual environment where all the required project libraries are stored separated from other projects in my computer.

## SQLlite
 
Database is stored in my computer (fintrack.db)
To connect to it from python using sqlite3.connect
SQLite is NOT part of VS Code.
VS Code is where I write code.
SQLite is where I store data.

## Git

git add . -> Saves files in a box. It selects/stages files which are to be included in next commit.
git commit -m "message" -> It labels box
git push -> ship the box to Github

## DataFrame

Dataframe- pandas table in RAM
           temporary(deletes when program ends)
           used of cleaning data and transforming
           Unlike SQLite where data is permanently stored

## ETL
ETL:
Extract   → load CSV into pandas DataFrame
Transform → clean data (missing values, duplicates, NaN)
Load      → insert cleaned DataFrame into SQLite (fintrack.db)

## Group by

"Group BY splits rows into groups based on column's values, so aggregate functions(max,min,SUM,COUNT,AVG)
calculate results for each group instead for entire table

## Tuple

A collection of values in round brackets — like a list but fixed.
(month,)  ← tuple with one item, comma is essential
(month)   ← NOT a tuple, just brackets

SQLite needs a tuple as a sealed envelope containing values
to fill in the ? placeholders in SQL queries.
One ? = one value in the tuple.

## SQL injection
SQL injection is to prevent malicious user from inserting unwanted data into the database. ? prevents SQLite from considering any data entered by user as a command treat it as a normal text data

## conn.commit()
conn.commit() saves changes permanently to disk (fintrack.db)
Without it → changes exist only in RAM → lost when program ends
With it    → changes written to fintrack.db → permanent

## df.copy()

It creates a photocopy of your dataframe. So that while data cleaning like stripping whitespaces,removing duplicates, fixing dates they modify the copy not the original as if one realizes while performing data cleaning that cleaning logic is wrong the original df where csv is stored is untouched.

## pd.to_datetime(errors='coerce')
Converts text dates to real Python date objects.
errors='coerce' → unreadable dates become NaN instead of crashing.

## pd.to_numeric(errors='coerce')
Converts text numbers to real Python numbers.
errors='coerce' → unreadable values become NaN instead of crashing.

## savings_rate
(income - total_spent) / income * 100
Negative means you spent more than you earned that month.


"""
    def save_exchange_rates(rates: dict, base: str, conn)-> None:
        """
        Save fetched exchange rates to database
        """

        if not rates:
            print("No rates to save")
            return

        # Get Current timestamp

        fetched_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Prepare rows for insertion

        rows = [
            (base, currency, rate, fetched_at)
            for currency, rate in rates.items()
        ]

        conn.executemany(
            "INSERT INTO exchange_rates (base, currency, rate, fetched_at) VALUES (?, ?, ?, ?)",
            rows
        )

        conn.commit()
        print(f"Saved {len(rows)} exchange rates to database")

if __name__ == "__main__":

    #existing code

    df = load_csv("data/sample_transactions.csv")
    summarize(df)

    # New - test API

    from fintrack.db import get_connection, create_tables

    conn = get_connection()
    create_tables()

    rates = fetch_exchange_rates(base="EUR")

    if rates:
        print(f"\n Sample rates:")
        print(f"1 EUR = {rates.get('USD', 'N/A',)} USD")
        print(f"1 EUR = {rates.get('GBP', 'N/A',)} GBP")
        print(f"1 EUR = {rates.get('INR', 'N/A',)} INR")

        save_exchange_rates(rates, "EUR", conn)


    conn.close()
"""