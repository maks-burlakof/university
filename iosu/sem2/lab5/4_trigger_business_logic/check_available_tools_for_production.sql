-- Triggers that implements business logic


-- TRIGGER: check available amount of tools that required for production

CREATE OR REPLACE TRIGGER TRG_BUSINESSLOGIC_CHECK_AVAILABLE_TOOLS_FOR_PRODUCTION
BEFORE INSERT ON PRODUCTION
FOR EACH ROW
DECLARE
    v_required_tools_for_production NUMBER;
BEGIN
    -- TODO: handle situation if production updated, not inserted

    FOR rec IN (
        SELECT
            t.ID AS tool_id,
            t.TITLE as tool_title,
            t.TOTAL_AMOUNT as available_quantity,
            tmt.NUMBER_OF_REQUIRED_TOOLS AS required_tools
        FROM TECHNOLOGICALMAPSTOOLS tmt
        JOIN TOOLS t ON t.ID = tmt.TOOLS_ID
        WHERE tmt.TECHNOLOGICAL_MAP_ID = :NEW.TECHNOLOGICAL_MAP_ID
    )
    LOOP
        v_required_tools_for_production := rec.required_tools * :NEW.NUMBER_OF_REQUIRED_PRODUCTS;
        IF v_required_tools_for_production > rec.available_quantity THEN
            RAISE_APPLICATION_ERROR(-20001, 'Required tools exceed available quantity.');
        END IF;
    END LOOP;
END;
/


-- TEST: TRG_BUSINESSLOGIC_CHECK_AVAILABLE_TOOLS_FOR_PRODUCTION

DECLARE
    v_technological_map_id NUMBER := 19;
    v_production_start_date DATE := SYSDATE - 1;
    v_production_end_date DATE := SYSDATE;
    v_production_number_of_required_products NUMBER := 1;
    v_production_number_of_required_products_invalid NUMBER := 9999999;
    v_production_number_of_defects NUMBER := 1;
BEGIN
    -- Test 1. Insert valid data
    SAVEPOINT test_start_1;
    BEGIN
        INSERT INTO PRODUCTION (TECHNOLOGICAL_MAP_ID, START_DATE, END_DATE, NUMBER_OF_REQUIRED_PRODUCTS, NUMBER_OF_DEFECTS)
        VALUES (v_technological_map_id, v_production_start_date, v_production_end_date, v_production_number_of_required_products, v_production_number_of_defects);
        DBMS_OUTPUT.PUT_LINE('Insert successful: Valid data.');
    EXCEPTION
        WHEN OTHERS THEN
            DBMS_OUTPUT.PUT_LINE('Error: ' || SQLERRM);
            DBMS_OUTPUT.PUT_LINE('This error is not expected.');
    END;
    ROLLBACK TO test_start_1;

    -- Test 2: Insert invalid data
    SAVEPOINT test_start_2;
    BEGIN
        INSERT INTO PRODUCTION (TECHNOLOGICAL_MAP_ID, START_DATE, END_DATE, NUMBER_OF_REQUIRED_PRODUCTS, NUMBER_OF_DEFECTS)
        VALUES (v_technological_map_id, v_production_start_date, v_production_end_date, v_production_number_of_required_products_invalid, v_production_number_of_defects);
    EXCEPTION
        WHEN OTHERS THEN
            DBMS_OUTPUT.PUT_LINE('Error: ' || SQLERRM);
            DBMS_OUTPUT.PUT_LINE('This is expected error. Required tools exceed available quantity.');
    END;
    ROLLBACK TO test_start_2;
END;
/
