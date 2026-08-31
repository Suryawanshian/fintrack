sql

-- FinTrack Practice Queries
-- Run these to understand your data

-- 1. See all transactions
SELECT * FROM transactions;

-- 2. See all categories
SELECT * FROM categories;

-- 3. Insert a test transaction
INSERT INTO transactions (date, amount, merchant, category, account, note)
VALUES('2024-01-03', 42.50 , 'Starbucks' , 'Food', ' HDFC', 'morning coffee');

-- 4. Find all transactions over 500
SELECT date, amount, merchant, category
FROM transactions
WHERE amount > 500;

-- 5. Total spending per category
SELECT category, SUM(amount) AS total_spent
FROM transactions
GROUP BY category
ORDER BY total_spent DESC;

-- 6. Count transactions per category
SELECT category, COUNT(*) AS num_transactions
FROM transactions
GROUP BY category;

-- 7. Most expensive transaction
SELECT * FROM transactions
ORDER BY amount DESC
LIMIT 1;

-- 8. Transactions in January 2024
SELECT * FROM transactions
WHERE date BETWEEN '2024-01-01' AND '2024-01-31';

-- 9. Total spending per category for a specific month

SELECT
    category,
    SUM(amount) AS total_spent,
    COUNT(*) AS num_transactions
FROM transactions
WHERE strftime('%Y-%m', date) = '2024-01'
GROUP BY category
ORDER BY total_spent DESC;

-- 10. Top merchants by spending

SELECT
     merchant,
     SUM(amount) AS total_spent,
     COUNT(*) AS num_visits
FROM transactions
WHERE merchant IS NOT NULL 
GROUP BY merchant
ORDER BY total_spent DESC
LIMIT 5;

-- 11. Monthly Spending Total

SELECT
    strftime("%Y-%m", date) AS month,
    SUM(amount) AS total_spent,
    COUNT(*) AS num_transactions
FROM num_transactions
GROUP BY month
ORDER BY month DESC;

-- 12. Daily Average spending for the month

SELECT
    ROUND(SUM(amount) / COUNT(DISTINCT DATE), 2) AS daily_average
FROM transactions
WHERE strftime("%Y-%m", date) = '2024-01';
