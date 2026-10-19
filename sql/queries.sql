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


-- CTE: Monthly spending with running total
WITH monthly AS (
    SELECT
        strftime('%Y-%m', date) AS month,
        SUM(amount) AS total_spent
    FROM transactions
    GROUP BY month
)
SELECT 
    month,
    total_spent,
    SUM(total_spent) OVER (ORDER BY month) AS running_total
FROM monthly
ORDER BY month;

-- Window function: Rank categories by spending each month
SELECT
    strftime('%Y-%m', date) AS month,
    category,
    SUM(amount) AS total_spent,
    RANK() OVER(
        PARTITION BY strftime('%Y-%m', date)
        ORDER BY SUM(amount) DESC
    ) AS spending_rank
    FROM transactions
    GROUP BY month, category
    ORDER BY month, spending_rank;

    -- Anomaly detection: transactions above 2x category average
    WITH category_stats AS(
        SELECT
            category,
            AVG(amount) AS avg_amount,
            AVG(amount) * AS threshold
        FROM transactions
        GROUP BY category
    )
    SELECT
        t.date,
        t.amount,
        t.merchant,
        t.category,
        ROUND(cs.avg_amount, 2) AS category_avg,
        ROUND(t.amount / cs.avg_amount, 2) AS times_above_avg
    FROM transactions t
    JOIN category_stats cs ON t.category = cs.category
    WHERE t.amount > cs.threshold
    ORDER BY times_above_avg DESC;


    -- Budget vs Actual Spending

    SELECT 
        c.name AS category,
        c.budget,
        COALESCE(SUM(t.amount), 0) AS total_spent,
        c.budget - COALESCE(SUM(t.amount), 0) AS remaining,
        ROUND(COALESCE(SUM(t.amount), 0) c.budget * 100, 1) AS pct_used
        FROM categories c
        LEFT JOIN transactions t
             ON c.name = t.category
             AND strftime('%Y-%m', t.date) = '2024-01'
        WHERE c.budget > 0
        GROUP BY c.name
        ORDER BY pct_used DESC;
        