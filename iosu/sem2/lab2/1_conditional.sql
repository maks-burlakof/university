-- 1. Conditional: Tools with highest usage count


SELECT
    t.id,
    t.title,
    t.total_amount,
    t.wear_degree,
    COUNT(p.technological_map_id) AS usage_count
FROM tools t
LEFT JOIN technologicalmapstools tmt ON t.id = tmt.tools_id
LEFT JOIN technologicalmap tm ON tmt.technological_map_id = tm.id
LEFT JOIN production p ON tm.id = p.technological_map_id
GROUP BY t.id, t.title, t.total_amount, t.wear_degree
HAVING COUNT(p.technological_map_id) > 0
ORDER BY usage_count DESC;


-- 1. Conditional: Production with defects percentage higher than 10%

SELECT
    technological_map_id,
    start_date,
    end_date,
    number_of_required_products,
    number_of_defects,
    ROUND((number_of_defects / number_of_required_products) * 100, 2) AS defect_percentage
FROM production
WHERE (number_of_defects / number_of_required_products) * 100 > 2
ORDER BY defect_percentage DESC;
