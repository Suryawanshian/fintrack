from fintrack.analyze import (
    spending_by_category,
    top_merchants,
    daily_average
)
from fintrack.db import insert_transactions
import pandas as pd

def test_spending_by_category(test_db):
    """Test that spending is correctly grouped by category"""
    # insert some test transactions
    df = pd.DataFrame({
        "date": ["2024-01-03", "2024-01-04", "2024-01-05"],
        "amount": [42.50, 120.00, 35.00],
        "merchant": ["Starbucks", "Amazon", "Zomato"],
        "category": ["Food", "Shopping", "Food"],
        "account": ["HSBC", "HSBC", "HSBC"],
        "note": ["coffee", "keyboard", "dinner"]
    })
    insert_transactions(df, test_db)

    result = spending_by_category(test_db,"2024-01")

    # should have two categories: Food and Shopping
    assert len(result) == 2

    # first result should be Shopping (highest spend)
    assert result[0]["category"] == "Shopping"
    assert result[0]["total_spent"] == 120.00


def test_top_merchants(test_db):
    """Test that top merchants returns correct number."""
    df = pd.DataFrame({
        "date": ["2024-01-03", "2024-01-04", "2024-01-05"],
        "amount": [42.50, 120.00, 35.00],
        "merchant": ["Starbucks", "Amazon", "Zomato"],
        "category": ["Food", "Shopping", "Food"],
        "account": ["HSBC", "HSBC", "HSBC"],
        "note": ["coffee", "keyboard", "dinner"]
    })
    insert_transactions(df, test_db)

    result = top_merchants(test_db, n=2)

    # should return only 2 merchants
    assert len(result) == 2

    # Amazon should be first (highest spend)
    assert result[0]["merchant"] == "Amazon"

def test_daily_average(test_db):
    """Test daily average calculation."""
    df = pd.DataFrame({
        "date": ["2024-01-03", "2024-01-03", "2024-01-04"],
        "amount": [40.00, 60.00, 100.00],
        "merchant": ["Starbucks", "Zomato", "Amazon"],
        "category": ["Food", "Food", "Shopping"],
        "account": ["HSBC", "HSBC", "HSBC"],
        "note": ["coffee", "lunch", "book"]
    })
    insert_transactions(df, test_db)

    result = daily_average(test_db, "2024-01")

    # total = 200, unique days = 2, average = 100
    assert result == 100.0