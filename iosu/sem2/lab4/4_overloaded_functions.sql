-- 3. Overloaded Functions: Get average wear degree by provided equipment


CREATE OR REPLACE PACKAGE PKG_OVERLOADED_FUNCTIONS AS
    -- Function 1. Accepts NUMBER - equipment type ID
    FUNCTION FUNC_AVG_WEAR_DEGREE_BY_EQUIPMENT (p_equipment_type_id IN NUMBER) RETURN VARCHAR2;
    -- Function 2. Accepts VARCHAR2 - equipment type title
    FUNCTION FUNC_AVG_WEAR_DEGREE_BY_EQUIPMENT (p_equipment_type_title IN VARCHAR2) RETURN VARCHAR2;
END;
/

CREATE OR REPLACE PACKAGE BODY PKG_OVERLOADED_FUNCTIONS AS
    -- Function 1. Accepts NUMBER - equipment type ID

    FUNCTION FUNC_AVG_WEAR_DEGREE_BY_EQUIPMENT (
        p_equipment_type_id IN NUMBER
    ) RETURN VARCHAR2 IS
        v_average_wear NUMBER;
        v_equipment_type_name VARCHAR2(100);
    BEGIN
        -- Check if equipment type exists
        SELECT TITLE
        INTO v_equipment_type_name
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

        RETURN (
            'Performing search by equipment type ID. ' ||
            'Equipment: ' || v_equipment_type_name || ', ID: ' || p_equipment_type_id || '. ' ||
            'Average wear degree: ' || TO_CHAR(ROUND(v_average_wear, 2))
        );
    EXCEPTION
        WHEN NO_DATA_FOUND THEN
            RETURN 'Equipment type with ID ' || p_equipment_type_id || ' not found.';
        WHEN OTHERS THEN
            RETURN 'An exception occurred: ' || SQLERRM;
    END;


-- Function 2. Accepts VARCHAR2 - equipment type title

    FUNCTION FUNC_AVG_WEAR_DEGREE_BY_EQUIPMENT (
        p_equipment_type_title IN VARCHAR2
    ) RETURN VARCHAR2 IS
        v_average_wear NUMBER;
        v_equipment_type_id VARCHAR2(100);
    BEGIN
        -- Check if equipment type exists
        SELECT ID
        INTO v_equipment_type_id
        FROM EQUIPMENTTYPE
        WHERE TITLE = p_equipment_type_title;

        -- Calculate average wear degree for tools of the specified equipment type
        SELECT AVG(T.WEAR_DEGREE)
        INTO v_average_wear
        FROM TOOLS T
        JOIN TECHNOLOGICALMAPSTOOLS TMT ON T.ID = TMT.TOOLS_ID
        JOIN TECHNOLOGICALMAP TM ON TMT.TECHNOLOGICAL_MAP_ID = TM.ID
        JOIN EQUIPMENT E ON TM.EQUIPMENT_ID = E.ID
        WHERE E.TYPE_ID = v_equipment_type_id;

        RETURN (
            'Performing search by equipment type title. ' ||
            'Equipment: ' || p_equipment_type_title || ', ID: ' || v_equipment_type_id || '. ' ||
            'Average wear degree: ' || TO_CHAR(ROUND(v_average_wear, 2))
        );
    EXCEPTION
        WHEN NO_DATA_FOUND THEN
            RETURN 'Equipment type with title ' || p_equipment_type_title || ' not found.';
        WHEN OTHERS THEN
            RETURN 'An exception occurred: ' || SQLERRM;
    END;
END;
/


-- Run functions

SET SERVEROUTPUT ON;

SELECT OBJECT_NAME FROM USER_OBJECTS WHERE OBJECT_TYPE = 'FUNCTION';
SELECT OBJECT_NAME FROM USER_OBJECTS WHERE OBJECT_TYPE = 'PACKAGE';


BEGIN
    DBMS_OUTPUT.PUT_LINE('--------------------------------------------------------------------------------');
    DBMS_OUTPUT.PUT_LINE('AVG wear degree by equipment type ID: ');
    DBMS_OUTPUT.PUT_LINE(PKG_OVERLOADED_FUNCTIONS.FUNC_AVG_WEAR_DEGREE_BY_EQUIPMENT(1));

    DBMS_OUTPUT.PUT_LINE('--------------------------------------------------------------------------------');
    DBMS_OUTPUT.PUT_LINE('AVG wear degree by equipment type title: ');
    DBMS_OUTPUT.PUT_LINE(PKG_OVERLOADED_FUNCTIONS.FUNC_AVG_WEAR_DEGREE_BY_EQUIPMENT('Welding machine'));

    DBMS_OUTPUT.PUT_LINE('--------------------------------------------------------------------------------');
    DBMS_OUTPUT.PUT_LINE('AVG wear degree by equipment type ID: ');
    DBMS_OUTPUT.PUT_LINE(PKG_OVERLOADED_FUNCTIONS.FUNC_AVG_WEAR_DEGREE_BY_EQUIPMENT(1000));
END;
/
