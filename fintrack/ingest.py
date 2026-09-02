import os
import requests
from datetime import datetime
from dotenv import load_dotenv
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


def fetch_exchange_rates(base: str = "EUR") -> dict:
    """
    Fetch live exchange rates from ExchangeRate - API.
    base: the currency to change from default(EUR)
    Returns dictionary of currency codes and rates.
    """
    # Load environment variables from .env file
    
    load_dotenv()
    api_key = os.getenv("EXCHANGE_RATE_API_KEY")


    # Check if API key exists

    if not api_key:
        print("ERROR: EXCHANGE_RATE_API_KEY not found in .env file")
        return{}

    # Build the API url

    url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{base}"

    try:

        # Make the API request

        print(f"Fetching exchange rates for {base}....")
        response = requests.get(url, timeout=10)

        # Check if request was successful
        if response.status_code == 200:
            data = response.json()
            rates = data["conversion_rates"]
            print(f"Sucessfully fetched {len(rates)} exchange rates")
            return rates
        else:
            print(f"Error: API returned Status Code {response.status_code}")
            return {}

    except requests.exceptions.ConnectionError:
        print("ERROR: No internet Connection")
        return {}

    except requests.exceptions.Timeout:
        print("ERROR: Requests Timed Out after 10 seconds")
        return {}

    except Exception as e:
        print(f"ERROR: Unexpected error: {e}")
        return {}
    
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
