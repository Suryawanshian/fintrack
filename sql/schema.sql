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
