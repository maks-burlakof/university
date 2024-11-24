-- 2. Total: Number of tools for each equipment


SELECT
    e.id,
    e.title,
    et.title,
    COUNT(DISTINCT tmt.tools_id) AS unique_tools_count
FROM equipment e
LEFT JOIN equipmenttype et ON e.type_id = et.id
LEFT JOIN technologicalmap tm ON e.id = tm.equipment_id
LEFT JOIN technologicalmapstools tmt ON tm.id = tmt.technological_map_id
GROUP BY e.id, e.title, et.title
ORDER BY unique_tools_count DESC;
