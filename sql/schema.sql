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