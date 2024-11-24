-- 4. Lisf of equipment and tools


SELECT
    e.title,
    t.title,
    tmt.number_of_required_tools
FROM equipment e
LEFT JOIN technologicalmap tm ON e.id = tm.equipment_id
LEFT JOIN technologicalmapstools tmt ON tm.id = tmt.technological_map_id
LEFT JOIN tools t ON tmt.tools_id = t.id
ORDER BY e.id;


-- Lisf of equipment and tools

SELECT
    e.id,
    e.title AS equipment_name,
    LISTAGG(t.title, ', ') WITHIN GROUP (ORDER BY t.title) AS tools_list
FROM equipment e
RIGHT JOIN technologicalmap tm ON e.id = tm.equipment_id
RIGHT JOIN technologicalmapstools tmt ON tm.id = tmt.technological_map_id
RIGHT JOIN tools t ON tmt.tools_id = t.id
GROUP BY e.id, e.title
ORDER BY e.id;


-- Dynamic PL/SQL query to get the data

DECLARE
    sql_query   VARCHAR2(4000);
    cols_list   VARCHAR2(4000);
BEGIN
    -- Get the list of equipment types to use in the pivot
    SELECT LISTAGG('''' || TITLE || ''' AS "' || TITLE || '"', ', ') WITHIN GROUP (ORDER BY TITLE)
    INTO cols_list
    FROM EQUIPMENTTYPE;

    -- Construct the dynamic SQL query
    sql_query := 'SELECT TOOL_TITLE, ' || cols_list || '
                  FROM (
                      SELECT
                          T.TITLE AS TOOL_TITLE,
                          ET.TITLE AS EQUIPMENT_TYPE,
                          COALESCE(TMTOOLS.NUMBER_OF_REQUIRED_TOOLS, 0) AS REQUIRED_TOOLS
                      FROM
                          TOOLS T
                      LEFT JOIN
                          TECHNOLOGICALMAPSTOOLS TMTOOLS ON T.ID = TMTOOLS.TOOLS_ID
                      LEFT JOIN
                          TECHNOLOGICALMAP TM ON TMTOOLS.TECHNOLOGICAL_MAP_ID = TM.ID
                      LEFT JOIN
                          EQUIPMENT E ON TM.EQUIPMENT_ID = E.ID
                      LEFT JOIN
                          EQUIPMENTTYPE ET ON E.TYPE_ID = ET.ID
                  )
                  PIVOT (
                      SUM(REQUIRED_TOOLS)
                      FOR EQUIPMENT_TYPE IN (' || cols_list || ')
                  )';

    -- Execute the dynamic SQL query
    EXECUTE IMMEDIATE sql_query;
END;
/
