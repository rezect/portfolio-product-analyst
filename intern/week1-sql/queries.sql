-- 1. Топ-10 товаров по выручке
SELECT StockCode, Description, SUM(UnitPrice * Quantity) as cost FROM data
WHERE Quantity > 0
GROUP BY StockCode
ORDER BY cost DESC
LIMIT 10;

-- 2. Заказы по дням (первые 10 дат)
SELECT DATE(InvoiceDate) as day, COUNT(DISTINCT InvoiceNo) as Orders FROM data
WHERE Quantity > 0
GROUP BY day
ORDER BY day ASC
LIMIT 10;

-- 3. Средний чек по месяцам
SELECT STRFTIME("%Y-%m", InvoiceDate) as month_year, ROUND(AVG(Quantity * UnitPrice), 2) FROM data
WHERE Quantity > 0
GROUP BY month_year
ORDER BY month_year ASC;

-- 4. Топ-5 стран по количеству заказов
SELECT Country, COUNT(DISTINCT InvoiceNo) AS total_orders FROM data
WHERE Quantity > 0
GROUP BY Country
ORDER BY total_orders DESC
LIMIT 5;

-- 5. Товары с NULL CustomerID
WITH missing AS (
	SELECT COUNT(*) AS cnt FROM data WHERE CustomerID IS NULL
)
SELECT (SELECT cnt FROM missing) AS total_orders, ROUND((SELECT cnt FROM missing) * 1.0 / COUNT(*), 2) AS percent FROM data;