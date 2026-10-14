import pandas as pd
from fintrack.clean import clean_transactions

def test_removes_missing_amounts(sample_df):
    """Test that rows with missing amounts are removed."""
    # Add a row with missing amount
    sample_df.loc[3] = ["2024-01-10", None, "Tesco", "Groceries", "HSBC", "test"]

    result = clean_transactions(sample_df)

    # should have 3 rows not 4 (missing amount row removed)
    assert len(result) == 3

def test_removes_duplicates(sample_df):
    """Test that duplicate rows are removed."""
    # Add exact duplicate of first row
    sample_df.loc[3] = ["2024-01-03", 42.50, "Starbucks", "Food", "HSBC", "coffee"]

    result = clean_transactions(sample_df)

    # should have 3 rows not 4 (duplicate removed)
    assert len(result) == 3

def test_standardizes_dates(sample_df):
    """Test that dates are converted to YYYY-MM-DD format."""
    result = clean_transactions(sample_df)

    # check first date is in correct format
    
    assert result["date"][0] == "2024-01-03"  