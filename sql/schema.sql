-- FinTrack Database Schema
-- This file defines the structure of our database

CREATE TABLE IF NOT EXISTS transactions (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    date      TEXT NOT NULL,
    amount    REAL NOT NULL,
    merchant  TEXT,
    category  TEXT,
    account   TEXT,
    note      TEXT
);

CREATE TABLE IF NOT EXISTS categories (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    name    TEXT UNIQUE NOT NULL,
    budget  REAL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS exchange_rates (

    id INTEGER PRIMARY KEY AUTOINCREMENT,
    base TEXT NOT NULL,
    currency TEXT NOT NULL,
    rate     REAL NOT NULL,
    fetched_at TEXT NOT NULL
);

-- Indexes for query performance

CREATE INDEX IF NOT EXISTS idx_transactions_date    
        ON transactions(date);


CREATE INDEX IF NOT EXISTS idx_transactions_category
        ON transactions(category);

CREATE INDEX IF NOT EXISTS idx_transactions_date_category
        ON transactions(date, category);
        