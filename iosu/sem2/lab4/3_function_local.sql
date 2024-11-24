-- 3. Local Function: Get average wear degree by provided equipment type


SET SERVEROUTPUT ON;


DECLARE
    v_equipment_type_id NUMBER;
    v_result VARCHAR2(200);

    FUNCTION FUNC_AVG_WEAR_DEGREE_BY_EQUIPMENT_TYPE (
        p_equipment_type_id IN NUMBER
    ) RETURN VARCHAR2 IS
        v_average_wear NUMBER;
        v_equipment_name VARCHAR2(100);
    BEGIN
        -- Check if equipment type exists
        SELECT TITLE
        INTO v_equipment_name
        FROM EQUIPMENTTYPE
        WHERE ID = p_equipment_type_id;

        -- Calculate average wear degree for tools of the specified equipment type
        SELECT AVG(T.WEAR_DEGREE)
        INTO v_average_wear
        FROM TOOLS T
        JOIN TECHNOLOGICALMAPSTOOLS TMT ON T.ID = TMT.TOOLS_ID
        JOIN TECHNOLOGICALMAP TM ON TMT.TECHNOLOGICAL_MAP_ID = TM.ID
        JOIN EQUIPMENT E ON TM.EQUIPMENT_ID = E.ID
        WHERE E.TYPE_ID = p_equipment_type_id;

        RETURN 'Equipment: ' || v_equipment_name || ', Average wear degree: ' || TO_CHAR(ROUND(v_average_wear, 2));
    EXCEPTION
        WHEN NO_DATA_FOUND THEN
            RETURN 'Equipment type with ID ' || p_equipment_type_id || ' not found.';
        WHEN OTHERS THEN
            RETURN 'An exception occurred: ' || SQLERRM;
    END FUNC_AVG_WEAR_DEGREE_BY_EQUIPMENT_TYPE;

BEGIN
    -- Ask user to enter equipment type ID
    DBMS_OUTPUT.PUT_LINE('Enter Equipment type ID :');
    v_equipment_type_id := &equipment_type_id;

    -- Call the function
    v_result := FUNC_AVG_WEAR_DEGREE_BY_EQUIPMENT_TYPE(v_equipment_type_id);
    DBMS_OUTPUT.PUT_LINE('-------------------------------------------------------------------');
    DBMS_OUTPUT.PUT_LINE('Function output:');
    DBMS_OUTPUT.PUT_LINE(v_result);
END;
/
