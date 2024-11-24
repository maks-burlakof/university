-- Triggers that implements business logic


-- TRIGGER: for decreasing wear degree for used tools in production

CREATE OR REPLACE TRIGGER TRG_BUSINESSLOGIC_DECREASE_TOOLS_WEAR_DEGREE_AFTER_PRODUCTION
AFTER INSERT OR UPDATE ON PRODUCTION
FOR EACH ROW
DECLARE
    v_wear_degree_coefficient NUMBER := 1;
    v_wear_degree_decrement NUMBER;
BEGIN
    FOR rec IN (
        SELECT
            t.ID AS tool_id,
            tmt.NUMBER_OF_REQUIRED_TOOLS AS required_tools
        FROM TECHNOLOGICALMAPSTOOLS tmt
        JOIN TOOLS t ON t.ID = tmt.TOOLS_ID
        WHERE tmt.TECHNOLOGICAL_MAP_ID = :NEW.TECHNOLOGICAL_MAP_ID
    )
    LOOP
        IF :OLD.NUMBER_OF_REQUIRED_PRODUCTS IS NOT NULL THEN
            v_wear_degree_decrement := ROUND(v_wear_degree_coefficient * rec.required_tools * (:NEW.NUMBER_OF_REQUIRED_PRODUCTS - :OLD.NUMBER_OF_REQUIRED_PRODUCTS));
        ELSE
            v_wear_degree_decrement := ROUND(v_wear_degree_coefficient * rec.required_tools * :NEW.NUMBER_OF_REQUIRED_PRODUCTS);
        END IF;

        -- TODO: handle situation when wear degree is less than 0

        IF v_wear_degree_decrement != 0 THEN
            IF v_wear_degree_decrement < 0 THEN
                DBMS_OUTPUT.PUT_LINE('Increasing wear degree for tool with ID ' || rec.tool_id || ' by ' || v_wear_degree_decrement);
            ELSE
                DBMS_OUTPUT.PUT_LINE('Decreasing wear degree for tool with ID ' || rec.tool_id || ' by ' || v_wear_degree_decrement);
            END IF;

            UPDATE TOOLS
            SET WEAR_DEGREE = WEAR_DEGREE - v_wear_degree_decrement
            WHERE ID = rec.tool_id;
        END IF;
    END LOOP;

EXCEPTION
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('An error occurred while updating wear degree: ' || SQLERRM);
END;
/

-- TEST: TRG_BUSINESSLOGIC_DECREASE_TOOLS_WEAR_DEGREE_AFTER_PRODUCTION

SET SERVEROUTPUT ON;

DECLARE
    v_technological_map_id NUMBER := 19;
    v_production_start_date DATE := SYSDATE - 1;
    v_production_end_date DATE := SYSDATE;
    v_production_number_of_required_products NUMBER := 10;
    v_production_number_of_required_products_updated NUMBER := 20;
    v_production_number_of_defects NUMBER := 1;

    FUNCTION GET_TOOLS_WEAR_DEGREE(p_technological_map_id NUMBER) RETURN SYS_REFCURSOR IS
        v_cursor SYS_REFCURSOR;
    BEGIN
        OPEN v_cursor FOR
            SELECT
                T.TITLE,
                T.WEAR_DEGREE
            FROM TOOLS T
            LEFT JOIN TECHNOLOGICALMAPSTOOLS TMT ON T.ID = TMT.TOOLS_ID
            WHERE TMT.TECHNOLOGICAL_MAP_ID = p_technological_map_id;
        RETURN v_cursor;
    END;
BEGIN
    SAVEPOINT test_start;
    DBMS_OUTPUT.PUT_LINE('TEST: TRG_BUSINESSLOGIC_DECREASE_TOOLS_WEAR_DEGREE_AFTER_PRODUCTION');


    -- Test 1. Before production INSERT

    DECLARE
        v_cursor SYS_REFCURSOR;
        v_title TOOLS.TITLE%TYPE;
        v_wear_degree TOOLS.WEAR_DEGREE%TYPE;
    BEGIN
        v_cursor := GET_TOOLS_WEAR_DEGREE(v_technological_map_id);
        DBMS_OUTPUT.PUT_LINE('Tools data before production:');
        LOOP
            FETCH v_cursor INTO v_title, v_wear_degree;
            EXIT WHEN v_cursor%NOTFOUND;
            DBMS_OUTPUT.PUT_LINE(RPAD(v_title, 30) || '| ' || RPAD(v_wear_degree, 6));
        END LOOP;
        CLOSE v_cursor;
    END;


    -- Test 2: After production INSERT

    INSERT INTO PRODUCTION (TECHNOLOGICAL_MAP_ID, START_DATE, END_DATE, NUMBER_OF_REQUIRED_PRODUCTS, NUMBER_OF_DEFECTS)
    VALUES (v_technological_map_id, v_production_start_date, v_production_end_date, v_production_number_of_required_products, v_production_number_of_defects);

    DECLARE
        v_cursor SYS_REFCURSOR;
        v_title TOOLS.TITLE%TYPE;
        v_wear_degree TOOLS.WEAR_DEGREE%TYPE;
    BEGIN
        v_cursor := GET_TOOLS_WEAR_DEGREE(v_technological_map_id);
        DBMS_OUTPUT.PUT_LINE('Tools data after production insert:');
        LOOP
            FETCH v_cursor INTO v_title, v_wear_degree;
            EXIT WHEN v_cursor%NOTFOUND;
            DBMS_OUTPUT.PUT_LINE(RPAD(v_title, 30) || '| ' || RPAD(v_wear_degree, 6));
        END LOOP;
        CLOSE v_cursor;
    END;


    -- Test 3: After production UPDATE

    UPDATE PRODUCTION
    SET NUMBER_OF_REQUIRED_PRODUCTS = v_production_number_of_required_products_updated
    WHERE
        TECHNOLOGICAL_MAP_ID = v_technological_map_id
        AND START_DATE = v_production_start_date
        AND END_DATE = v_production_end_date
        AND NUMBER_OF_REQUIRED_PRODUCTS = v_production_number_of_required_products
        AND NUMBER_OF_DEFECTS = v_production_number_of_defects;

    DECLARE
        v_cursor SYS_REFCURSOR;
        v_title TOOLS.TITLE%TYPE;
        v_wear_degree TOOLS.WEAR_DEGREE%TYPE;
    BEGIN
        v_cursor := GET_TOOLS_WEAR_DEGREE(v_technological_map_id);
        DBMS_OUTPUT.PUT_LINE('Tools data after production update:');
        LOOP
            FETCH v_cursor INTO v_title, v_wear_degree;
            EXIT WHEN v_cursor%NOTFOUND;
            DBMS_OUTPUT.PUT_LINE(RPAD(v_title, 30) || '| ' || RPAD(v_wear_degree, 6));
        END LOOP;
        CLOSE v_cursor;
    END;

    ROLLBACK TO test_start;
END;
/
