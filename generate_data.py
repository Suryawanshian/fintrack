import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta

fake=Faker()

def generate_transactions(n: int = 10000) -> pd.DataFrame:
    """Generate n fake transactions for performance testing."""

    categories = ["Food","Shopping", "Transport","Entertainment", "Groceries"]

    merchants = {
        "Food" : ["Starbucks", "McDonalds", "Subway", 
                  "Zomato", "Deliveroo", " Pret"],
        "Shopping" : ["Amazon", "Zalando", "Zara",
                       "ASOS", "Currys", "Apple"],
        "Transport": ["Uber", "Bolt", "Dublin Bus", 
                      "Irish Rail", "Ryanair"],
        "Entertainment": ["Netflix", "Spotify", "Cinema", 
                          "Steam", "Vue"],
        "Groceries": ["Tesco", "Lidl", "Aldi", 
                      "Dunnes", "SuperValu"]
    }

    amount_ranges = {
        "Food": (3, 50),
        "Shopping": (20, 500),
        "Transport": (5, 100),
        "Entertainment": (10, 100),
        "Groceries": (20, 150)
    }

    rows = []
    start_date = datetime(2023, 1, 1)


    for _ in range(n):
        category = random.choice(categories)
        merchant = random.choice(merchants[category])
        min_amt, max_amt = amount_ranges[category]
        amount = round(random.uniform(min_amt, max_amt), 2)
        date = start_date + timedelta(days=random.randint(0, 365))

        rows.append({
            "date": date.strftime("%Y-%m-%d"),
            "amount": amount,
             "merchant": merchant,
            "category": category,
            "account": "HSBC",
            "note": fake.sentence(nb_words=3)
        })

    return pd.DataFrame(rows)

if __name__ == "__main__":

    print("Generating 10,000 transactions...")
    df = generate_transactions(10000)
    df.to_csv("data/large_transactions.csv", index=False)
    print(f"Generated {len(df)} transactions")
    print(f"Date range: {df['date'].min()} to {df['date'].max()}")
    print(f"Saved to data/large_transactions.csv")