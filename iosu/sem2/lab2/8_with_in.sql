-- 8. Query with IN with subquery
-- List of Employees that have equipment

SELECT
    first_name,
    last_name
FROM employee
WHERE
    id IN (
        SELECT responsible_employee_id FROM equipment
    );
