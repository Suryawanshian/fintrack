
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
Tuple items are ordered, unchangeable, and allow duplicate values.
Tuple items are indexed, the first item has index [0], the second item has index [1] etc.

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

## Day 5 - API Integration

## Environment Variables

Secrets/data stored in .env file - never pushed to GitHub.
.gitignore protects .env automatically.
Read in Python using os.getenv("KEY_NAME").
load_dotenv() loads .env file into Python.

## requests library

Makes HTTP calls to external APIs.
response.status_code == 200 means success.
response.json() converts API response to Python dict.
timeout=10 means give up after 10 seconds.

### try/except

Handles errors without crashing the program.
try -> attempt risky operation,
except SpecificError -> handle that specific failure.
Always return {} or None on failure, never crash

## API key security rules

Never hardcore API keys in Python files.
Never commit .env to GitHub.
Always use .env + os.getenv()
Always create .env example for other developers



### Rich library
console = Console() → main printing object
Table() → creates bordered tables
Panel() → creates a box around single content
box.ROUNDED → curved border style

### table.add_column("Name", style="cyan")
Adds a column header with optional color

### table.add_row("value1", "value2")
Adds one row — all values must be strings
Numbers need str() to convert them

### Panel vs Table
Table → multiple rows of data (list of things)
Panel → single highlighted summary (one important thing)

### Conditional formatting
if rate >= 20 → green border
if rate >= 0  → yellow border
else          → red border
Changes visual based on data value




## Concept: CTE (Common Table Extension)
WHAT: temporary named result used inside SQL query using WITH keyword
WHY:  makes complex queries readable by breaking them into named steps instead of one giant query
WHEN TO USE: when same calculation needed more than once in a query
Example: WITH monthly AS('
    SELECT strftime('%Y-%m',date) AS month,
            SUM(amount) AS total_spent
    FROM transactions
    GROUP BY month
)
 → creates temporary "monthly" table
 → main query then reads from it cleanly

 ## Concept: Window function
 WHAT: used for calculation across related rows while keeping individual rows visible
 WHY: when you need individual data and summary in same result
 WHEN TO USE: 
    - running totals (cumulative spending over months)
    - rankings (which category spent most in this month)
    - comparing each row to group average
 EXAMPLE: SUM(total_spent) OVER (ORDER BY month) AS running_total
         shows each month AND cumulative total together

## Concept: Anomaly Detection
WHAT: automatically finding transactions unusually different from normal
WHY:  impossible to manually check hundreds of transactions
WHEN TO USE: 
    - detect fraud or unsual spending
    - flag outliers in any dataset
    - automatic alerts without manual checking
EXAMPLE: transactions > 2x category average flagged in FinTrack
         Yamamori EUR 850 = 6.21x Food average → automatically flagged