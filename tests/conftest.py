
import pytest
import sqlite3
import pandas as pd
from fintrack.db import create_tables, insert_default_categories

@pytest.fixture
def test_db():
    """
    Create a fresh in-memory database for each test.
    Automatically destroyed after each test finishes.
    """
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row

    create_tables(conn)
    insert_default_categories(conn)
    yield conn
    conn.close()

@pytest.fixture
def sample_df():
    return pd.DataFrame({
        "date": ["2024-01-03", "2024-01-04", "2024-01-05"],
        "amount": [42.50, 120.00, 35.00],
        "merchant": ["Starbucks", "Amazon", "Zomato"],
        "category": ["Food", "Shopping", "Food"],
        "account": ["HSBC", "HSBC", "HSBC"],
        "note": ["coffee", "keyboard", "dinner"]
    })