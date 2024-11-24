-- 10. Query with EXISTS: List of products that have production records


SELECT
    p.id,
    p.title
FROM product p
WHERE EXISTS (
    SELECT 1
    FROM technologicalmap tm
    LEFT JOIN production pr ON tm.id = pr.technological_map_id
    WHERE tm.product_id = p.id
);
