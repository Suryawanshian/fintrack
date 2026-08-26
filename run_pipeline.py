
from fintrack.db import get_connection, create_tables, insert_default_categories, insert_transactions
from fintrack.ingest import load_csv
from fintrack.clean import clean_transactions, summarize_clean
def run_pipeline(csv_path: str) -> None:
    """
    Run the full ETL pipeline:
    1. Extract - load CSV
    2. Transform -clean data
    3. Load- insert into SQLite
    """

    print("=" * 40)
    print("FINTRACK PIPELINE STARTING")
    print("=" * 40)

    # Step 1- Extract
    print("\n[1/3] Loading CSV...")
    raw_df = load_csv(csv_path)

    # Step 2 - Transform
    print("\n[2/3] Cleaning data...")
    clean_df = clean_transactions(raw_df) 
    summarize_clean(clean_df)

    #Step 3 - Load
    print("\n[3/3] Loading into database...")
    conn = get_connection()
    create_tables()
    insert_transactions(clean_df, conn)
    insert_default_categories()
    conn.close()


    print("\n" + "=" * 40)
    print("PIPELINE COMPLETE")
    print("=" * 40)

if __name__ == "__main__":
    run_pipeline("data/sample_transactions.csv")

