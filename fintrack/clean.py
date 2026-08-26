import pandas as pd

def clean_transactions(df:pd.DataFrame) -> pd.DataFrame:
    """
    Clean raw transaction data.
    Takes messy dataframe, returns a clean one
    """
    #Step 1- make a copy there is no modification done on original
    df = df.copy()

    #Step 2- standardize column names
    #strip removes spaces, lower makes all lowercase
    df.columns = df.columns.str.strip().str.lower()

    #Step 3- standardize date format to YYYY-MM-DD

    df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.strftime("%Y-%m-%d")

    #Step 4- convert to a number
    #errors="coerce" turns anything that cant a number to Nan
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")

    #Step 5 - clean merchant names
    #strip removes spaces, title makes First letter Uppercase
    df["merchant"] = df["merchant"].str.strip().str.title()

    #Step 6 - fill missing categories
    df["category"] = df["category"].fillna("Unorganized")

    #Step 7- remove rows where amount or date is missing
    #we cant store transactions without them

    before = len(df)
    df = df.dropna(subset=["date","amount"])
    after = len(df)
    print(f"Removed {before-after}) rows with missing dates or amount")

    #Step 8 - remove duplicate rows
    #a duplicate rows with same date, amount and merchant

    before = len(df)
    df = df.drop_duplicates(subset=["date","amount","merchant"])
    after = len(df)
    print(f"Removed {before - after} duplicate rows")

    #Step 9 - reset index after dropping rows
    df=df.reset_index(drop=True)

    print(f"Final clean rows : {len(df)}")
    return df

def summarize_clean(df: pd.DataFrame) -> None:
    """Print Summary of Cleaned data"""
    print("\n--- Cleaned Data Summary ---")
    print(f"Total Transactions: {len(df)}")
    print(f"Date range: {df['date'].min()} to {df['date'].max()}")
    print(f"Total amount: EUR{df['amount'].sum():.2f}")
    print(f"Categories: {list(df["category"].unique())}")
    print(f"\n Missing values after cleaning:")
    print(df.isnull().sum())

if __name__=="__main__":
# Load the raw CSV

    raw_df = pd.read_csv("data/sample_transactions.csv")
    print(f"Raw rows loaded : {len(raw_df)}")

    #Clean it
    clean_df = clean_transactions(raw_df)

    #Summarize
    summarize_clean(clean_df)

    #Show Cleaned data
    print("\n--- First Clean 5 rows ---")
    print(clean_df[["date","amount","merchant","category"]].head())


