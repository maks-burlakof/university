-- 6. Query with inner join


SELECT
    e.last_name,
    e.middle_name,
    e.first_name,
    p.title
FROM EMPLOYEE e
JOIN JOBPOSITION p ON e.job_position_id = p.id
ORDER BY p.title;
