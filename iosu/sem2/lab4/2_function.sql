-- 2. Function: Tools with minimal amount


CREATE OR REPLACE FUNCTION FUNC_CHECK_TOOLS_STOCK
RETURN VARCHAR2
IS
    v_min_tool_title TOOLS.TITLE%TYPE;
    v_min_tool_amount TOOLS.TOTAL_AMOUNT%TYPE;
    v_stock_status VARCHAR2(100);
BEGIN
    SELECT TITLE, TOTAL_AMOUNT
    INTO v_min_tool_title, v_min_tool_amount
    FROM TOOLS
    ORDER BY TOTAL_AMOUNT
    FETCH FIRST 1 ROWS ONLY;

    IF v_min_tool_amount < 100 THEN
        v_stock_status := 'Remaining (' || v_min_tool_title || ' - ' || v_min_tool_amount || ' units)';
    ELSE
        v_stock_status := '';
    END IF;

    RETURN v_stock_status;

EXCEPTION
    WHEN NO_DATA_FOUND THEN
        RETURN 'No tools found in the database';
    WHEN OTHERS THEN
        RETURN 'An error occurred: ' || SQLERRM;
END;
/


-- Run the function

SET SERVEROUTPUT ON;

BEGIN
    DBMS_OUTPUT.PUT_LINE(FUNC_CHECK_TOOLS_STOCK);
END;
/
