import pandas as pd

def load_csv(filepath:str) -> pd.DataFrame:
    """Load transactions from a CSV file and return a DataFrame."""
    df = pd.read_csv(filepath)
    print(f"Loaded {len(df)} rows from {filepath}")
    print(f"Columns: {list(df.columns)}")
    return df

def summarize(df: pd.DataFrame) -> None:
    """Print  quick summary of the loaded data."""
    print(f"\n---Summary---")
    print(f"Total rows:  {len(df)}")
    print(f"Missing values:\n{df.isnull().sum()}")
    print(f"\nFirst 3 rows:")
    print(df.head(3))

if __name__ == "__main__":
    df = load_csv("data/sample_transactions.csv")
    summarize(df)