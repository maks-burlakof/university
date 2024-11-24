-- 5. Total with date grouping


SELECT
    EXTRACT(YEAR FROM start_date) AS year_value,
    EXTRACT(MONTH FROM start_date) AS month_value,
    COUNT(*) AS total_productions
FROM production
GROUP BY EXTRACT(YEAR FROM start_date), EXTRACT(MONTH FROM start_date)
ORDER BY year_value, month_value;
