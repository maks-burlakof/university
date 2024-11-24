-- 3. Parametric: Tools with high level of degradation

SELECT
    t.id,
    t.title,
    t.total_amount,
    t.wear_degree
FROM tools t
WHERE t.wear_degree <: degradation_level
ORDER BY t.wear_degree;
