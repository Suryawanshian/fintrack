
# FinTrack — My Learning Notes

## Commands I Use Every Day

- Activate venv: source venv/Scripts/activate
- Run pipeline: python run_pipeline.py
- Run analytics: python -m fintrack.analyze
- Delete Database: rm fintrack.db
- Git Workflow: git add . -> git commit -m "message" -> git push

## Concept: Virtual Environment (venv)
    WHAT: It is a virtual environment where all the required project libraries are stored separated from other projects in my computer.
    WHY:  keeps project libraries separate from other projects
          Project A needs pandas 1.0 and Project B needs pandas 2.0
          venv prevents conflict between them
    WHEN TO USE: every Python project
    EXAMPLE:  source venv/Scripts/activate

## Concept: pip + requirements.txt
    WHAT: pip installs libraries, requirements.txt lists them
    WHY: anyone can recreate your exact environment
    WHEN TO USE: after installing any new library
    EXAMPLE: pip install pandas → pip freeze > requirements.txt

## Concept: .gitignore
    WHAT: file that tells Git which files to never track
    WHY: some files should never go to GitHub
         venv/ → too large, recreatable
         .env  → contains secrets
         *.db  → binary file that changes constantly
    WHEN TO USE: always, set up before first commit
    EXAMPLE: .gitignore in FinTrack root folder

## Concept: SQLite
   WHAT: database stored as single file (fintrack.db)
   WHY: no server needed, perfect for local projects
        entire database = one file you can copy or delete
   WHEN TO USE: local apps, prototypes, small projects
   EXAMPLE: sqlite3.connect("fintrack.db") in db.py

## Concept: SQL Schema
    WHAT: blueprint defining table structure
    WHY: defines what data can be stored and how
    WHEN TO USE: before inserting any data
    EXAMPLE: sql/schema.sql — CREATE TABLE transactions(...)

## Concept: conn.commit()
    WHAT: saves changes permanently to database file
    WHY: without it changes exist only in RAM, lost when program ends
    WHEN TO USE: after every INSERT, UPDATE, DELETE
    EXAMPLE: conn.commit() in db.py after executemany()

## Concept: Parameterised Queries (?)
    WHAT: placeholders for values in SQL queries
    WHY: prevents SQL injection — user input treated as data not code
    WHEN TO USE: ANY time user input goes into a SQL query
    EXAMPLE: conn.execute("WHERE month = ?", (month,))

## Concept: ETL Pipeline
    WHAT: Extract, Transform, Load — standard data pattern
    WHY: separates concerns — loading, cleaning, storing are different jobs
    WHEN TO USE: any time you move data from one place to another
    EXAMPLE: run_pipeline.py in FinTrack
         Extract  → load_csv() reads CSV into DataFrame
         Transform→ clean_transactions() cleans data
         Load     → insert_transactions() saves to SQLite

## Concept: df.copy()
    WHAT: creates separate copy of DataFrame in RAM
    WHY: cleaning changes don't affect original raw data
         can always restart cleaning from original
    WHEN TO USE: always first line of any cleaning function
    EXAMPLE: df = df.copy() in clean_transactions()

## Concept: pd.to_datetime(errors='coerce')
    WHAT: converts text dates to real Python date objects
    WHY: CSV dates are just text, can't do date math on text
         errors='coerce' turns bad dates to NaN instead of crashing
    WHEN TO USE: any time you load dates from CSV or API
    EXAMPLE: df["date"] = pd.to_datetime(df["date"], errors="coerce")

## Concept: pd.to_numeric(errors='coerce')
    WHAT: converts text numbers to real Python numbers
    WHY: CSV amounts are text strings, can't do math on them
         errors='coerce' turns bad values to NaN instead of crashing
    WHEN TO USE: any time you load numbers from CSV
    EXAMPLE: df["amount"] = pd.to_numeric(df["amount"], errors="coerce")

## Concept: drop_duplicates()
    WHAT: removes rows that are identical in specified columns
    WHY: duplicate transactions would double count spending
    WHEN TO USE: after loading any external data
    EXAMPLE: df.drop_duplicates(subset=["date","amount","merchant"])

## Concept: GROUP BY
    WHAT: groups rows with same value so aggregate functions 
         calculate per group instead of whole table
    WHY: need spending per category not total of everything
    WHEN TO USE: any time you want summary per group
    EXAMPLE: SELECT category, SUM(amount) FROM transactions 
         GROUP BY category
         → gives total per category not overall total

## Concept: Aggregate Functions
    WHAT: SUM, COUNT, AVG, MAX, MIN — calculate across rows
    WHY: summarise large amounts of data into useful numbers
    WHEN TO USE: always with GROUP BY
    EXAMPLE: SUM(amount) → total spending
             COUNT(*) → number of transactions
             AVG(amount) → average transaction size

## Concept: Python Functions
    WHAT: reusable block of code that does one specific job
    WHY: write once, use many times, keeps code organised
    WHEN TO USE: any time you repeat the same logic
    EXAMPLE: spending_by_category(conn, month) in analyze.py
             def name(input: type) -> return_type:


## Concept: API Integration
    WHAT: fetching live data from external services over internet
    WHY: get real-time data (exchange rates, prices) automatically
    WHEN TO USE: when data changes frequently and needs to be current
    EXAMPLE: fetch_exchange_rates() in ingest.py
             requests.get(url) → response.json() → save to DB


## Concept: Environment Variables (.env)
    WHAT: storing secrets outside your code
    WHY: API keys in code → accidentally pushed to GitHub → security risk
    WHEN TO USE: any secret value (API keys, passwords, tokens)
    EXAMPLE: .env file with EXCHANGE_RATE_API_KEY=xxxxx
             os.getenv("EXCHANGE_RATE_API_KEY") reads it in Python

## Concept: try/except
    WHAT: handles errors without crashing the program
    WHY: external services fail — internet goes down, API times out
        without try/except → one failure crashes everything
    WHEN TO USE: any risky operation (API calls, file reads, DB queries)
    EXAMPLE: try: requests.get(url)
            except ConnectionError: print("no internet") return {}


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

## savings_rate
(income - total_spent) / income * 100
Negative means you spent more than you earned that month.


##  Rich CLI Dashboard

### Concept: Rich Library
WHAT: Python library that makes terminal output beautiful
WHY: plain print() is boring and hard to read
     Rich adds colors, tables, borders automatically
WHEN TO USE: any CLI tool where you want professional output
EXAMPLE: fintrack/cli.py — all dashboard output uses Rich

### Concept: Console
WHAT: main Rich object for printing to terminal
WHY: replaces basic print() with styled output
EXAMPLE: console = Console() → console.print(table)

### Concept: Table
    WHAT: creates formatted table with borders and columns
    WHY: data in rows/columns is much easier to read than plain text
    WHEN TO USE: showing lists of data (categories, merchants)
    EXAMPLE: show_summary() in cli.py
         table.add_column("Category", style="cyan")
         table.add_row("Food", "EUR 245.00", "7")
         All values must be strings — numbers need str()

### Concept: Panel
    WHAT: puts a box/border around a single piece of content
    WHY: highlights one important summary number
    WHEN TO USE: single important result (savings rate, total)
    EXAMPLE: show_savings() in cli.py
         Panel(content, title="Financial Summary", border_style="green")

### Concept: Conditional Formatting
    WHAT: changing visual appearance based on data values
    WHY: makes good/bad instantly obvious without reading numbers
    WHEN TO USE: any metric with good/bad threshold
    EXAMPLE: savings rate color in FinTrack
         >= 20% → green (healthy)
         >= 0%  → yellow (ok)
         < 0%   → red (danger)

## Concept: pytest (pytest Testing)
    WHAT: Python testing library
    WHY: proves your code works, catches bugs automatically
    WHEN TO USE: every project, every function
    EXAMPLE: tests/ folder in FinTrack, run with pytest tests/ -v

## Concept: assert
    WHAT: checks if something is true, fails test if not
    WHY: verifies function output matches what you expect
    EXAMPLE: assert len(result) == 3
             assert result[0]["category"] == "Shopping"

## Concept: Fixtures (@pytest.fixture)
    WHAT: reusable setup code shared across tests
    WHY: avoids repeating setup in every test
    WHEN TO USE: any setup needed by multiple tests
    EXAMPLE: test_db fixture in conftest.py
             creates fresh in-memory database for each test
             yield conn → test runs → conn.close() automatically

## Concept: In-Memory Database (:memory:)
    WHAT: SQLite database in RAM, not saved to disk
    WHY: tests shouldn't touch real database
        fresh database for every test, no leftover data
    EXAMPLE: sqlite3.connect(":memory:") in conftest.py

## Concept: AAA Pattern
    WHAT: Arrange, Act, Assert — structure of every test
    WHY: makes tests readable and consistent
    EXAMPLE:
        Arrange → sample_df.loc[3] = [...None...]  (add bad row)
        Act     → result = clean_transactions(df)  (run function)
        Assert  → assert len(result) == 3          (check result)

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

## Concept: Jinja2 Templating
    WHAT: fills html template with python data
    WHY: separates data (Python) from presentation (HTML)
    WHEN TO USE: generating HTML reports, emails, any dynamic HTML
    EXAMPLE: report.html template filled by report.py
            {{ month }} → replaced with "2024-01"
            {% for cat in categories %} → loops through data

##  Concept: Separation of Concerns
    WHAT: keeping different parts of code separate
    WHY: easier to change design without touching logic
    EXAMPLE: report.html = design, report.py = logic
            change HTML → doesn't affect Python
            change Python → doesn't affect HTML

## Concept: CI/CD (Continuous Integration)
    WHAT: automatically running tests on every code push
    WHY: catches broken code before anyone sees it
        proves code works publicly with green checkmark
    WHEN TO USE: every real project should have CI
    EXAMPLE: .github/workflows/ci.yml in FinTrack
            runs pytest automatically on every git push
    
## Concept: GitHub Actions
    WHAT: GitHub's built in automation tool
    WHY: free, built into GitHub, no extra setup needed
    HOW IT WORKS:
    1. You push code
    2. GitHub creates fresh Linux computer
    3. Installs Python + dependencies
    4. Runs pytest
    5. Shows green ✅ or red ❌



## Concept: Database Indexes
    WHAT: data structure that speeds up database queries
    WHY : without index SQLite scans every row
          with index SQLite goes directly to matching rows
          20 rows → no difference, both fast
          10,000 rows → small difference
          1,000,000 rows → index is 100x faster, no index = unusable
    WHEN TO USE: Add an index on any column you frequently search by.
                In FinTrack: date and category are searched in every query.
    HOW TO CREATE: CREATE INDEX idx_date ON transactions(date);
                    - now WHERE date = '2024-01-03' is instant
    IMPORTANT GOTCHA I LEARNED: strftime('%Y-%m', date) breaks the index.
                    SQLite can't use the date index when you transform the date first.
                    The index stores '2024-01-03' but you're searching for '2024-01'.
                    They don't match → index ignored → full table scan.
    
## Concept: Composite Index
    WHAT: An Index on two columns combined
          Like a phone book sorted by last name and first name.
    
    Example from FINTRACK: CREATE INDEX idx_date_cat ON transactions(date, category);
            - speeds up: WHERE date = ? GROUP BY category
            - both conditions use one index instead of two

## Concept: Benchmark
    WHAT: Measuring exactly how fast your code runs with real numbers.


## SQL : WHERE vs HAVING

    WHERE: filters individual rows before BEFORE grouping
    HAVING: filters rows AFTER grouping

    USE WHERE for regular columns:
    WHERE amount > 100 - only rows where amount more than 100

    USE HAVING for SUM/COUNT/AVG:
    HAVING SUM(amount) > 100 - only groups where total is more than 100

    ORDER of clauses:

    SELECT
    FROM
    WHERE
    GROUP BY
    HAVING
    ORDER BY

    EXAMPLE FROM DRILL:
    SELECT category, SUM(amount) AS total_spent
    FROM transactions
    GROUP BY category
    HAVING SUM(amount) > 100
   -only shows categories where total spending exceeds 100                


