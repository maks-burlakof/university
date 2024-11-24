-- Procedure: List of products created in specific period


CREATE OR REPLACE DIRECTORY REPORT_OUTPUT_DIR AS 'D:\bsuir\sem7\iosu\ORACLE_reports';


CREATE OR REPLACE PROCEDURE REPORT_MANUFACTURED_PRODUCTS (
    p_date_from IN DATE,
    p_date_to IN DATE,
    p_equipment_type_id IN NUMBER DEFAULT NULL,
    p_output_path IN VARCHAR2 DEFAULT NULL
) AS
    CURSOR c_production IS
        SELECT
            P.TITLE AS product_title,
            TM.MAP_NUMBER AS tech_map_number,
            ET.TITLE as equipment_type,
            SUM(PR.NUMBER_OF_REQUIRED_PRODUCTS) AS total_produced,
            SUM(PR.NUMBER_OF_DEFECTS) AS total_defects,
            ROUND(STDDEV((PR.NUMBER_OF_DEFECTS / PR.NUMBER_OF_REQUIRED_PRODUCTS) * 100), 2) AS stddev_produced
        FROM
            PRODUCTION PR
        JOIN
            TECHNOLOGICALMAP TM ON PR.TECHNOLOGICAL_MAP_ID = TM.ID
        JOIN
            PRODUCT P ON TM.PRODUCT_ID = P.ID
        JOIN
            EQUIPMENT E ON TM.EQUIPMENT_ID = E.ID
        JOIN
            EQUIPMENTTYPE ET ON E.TYPE_ID = ET.ID
        WHERE
            PR.START_DATE BETWEEN p_date_from AND p_date_to
            AND (p_equipment_type_id IS NULL OR ET.ID = p_equipment_type_id)
        GROUP BY
            P.TITLE, TM.MAP_NUMBER, ET.TITLE;

    v_product_title PRODUCT.TITLE%TYPE;
    v_tech_map_number TECHNOLOGICALMAP.MAP_NUMBER%TYPE;
    v_equipment_type EQUIPMENTTYPE.TITLE%TYPE;
    v_total_produced NUMBER;
    v_total_defects NUMBER;
    v_stddev_produced NUMBER;

    v_output_file UTL_FILE.FILE_TYPE;
    v_output_line VARCHAR2(4000);
    v_output_first BOOLEAN := TRUE;
    --v_output_dir VARCHAR2(255) := 'report_manufactured_products';
    --v_output_file_name VARCHAR2(255) := 'report_manufactured_products_' || TO_CHAR(SYSDATE, 'YYYYMMDDHH24MISS') || '.txt';
    --v_output_path VARCHAR2(255) := v_output_dir || v_output_file_name;

BEGIN
    IF p_date_from > p_date_to THEN
        RAISE_APPLICATION_ERROR(-20002, 'The start date must be less than or equal to the end date.');
    END IF;

    IF p_date_from > SYSDATE OR p_date_to > SYSDATE THEN
        RAISE_APPLICATION_ERROR(-20003, 'Dates cannot be in the future.');
    END IF;

    IF p_output_path IS NOT NULL THEN
        v_output_file := UTL_FILE.FOPEN('REPORT_OUTPUT_DIR', p_output_path, 'W');

        UTL_FILE.PUT_LINE(v_output_file, '{');
        UTL_FILE.PUT_LINE(v_output_file, '"products": [');
    END IF;

    DBMS_OUTPUT.PUT_LINE(CHR(10));
    DBMS_OUTPUT.PUT_LINE('Report for products created between ' || p_date_from || ' and ' || p_date_to);
    DBMS_OUTPUT.PUT_LINE(CHR(10));
    DBMS_OUTPUT.PUT_LINE(
        RPAD('Product Title', 30) || '| ' ||
        RPAD('TM Number', 10) || '| ' ||
        RPAD('Equipment', 20) || '| ' ||
        RPAD('Produced', 9) || '| ' ||
        RPAD('Defects', 8) || '| ' ||
        RPAD('Std Dev', 8)
    );
    DBMS_OUTPUT.PUT_LINE('----------------------------------------------------------------------------------------------');

    FOR r_production IN c_production LOOP
        v_product_title := r_production.product_title;
        v_tech_map_number := r_production.tech_map_number;
        v_equipment_type := r_production.equipment_type;
        v_total_produced := r_production.total_produced;
        v_total_defects := r_production.total_defects;
        v_stddev_produced := r_production.stddev_produced;

        DBMS_OUTPUT.PUT_LINE(
            RPAD(v_product_title, 30) || '| ' ||
            RPAD(v_tech_map_number, 10) || '| ' ||
            RPAD(v_equipment_type, 20) || '| ' ||
            RPAD(v_total_produced, 9) || '| ' ||
            RPAD(v_total_defects, 8) || '| ' ||
            RPAD(v_stddev_produced, 8)
        );

        IF p_output_path IS NOT NULL THEN
            IF NOT v_output_first THEN
                UTL_FILE.PUT_LINE(v_output_file, ',');
            END IF;

            v_output_first := FALSE;

            v_output_line := '  {"product_title": "' || v_product_title || '", ' ||
                             '"tech_map_number": "' || v_tech_map_number || '", ' ||
                             '"equipment_type": "' || v_equipment_type || '", ' ||
                             '"total_produced": ' || v_total_produced || ', ' ||
                             '"total_defects": ' || NVL(v_total_defects, 0) || ', ' ||
                             '"v_stddev_produced": ' || v_stddev_produced || '}';
            UTL_FILE.PUT_LINE(v_output_file, v_output_line);
        END IF;
    END LOOP;

    IF p_output_path IS NOT NULL THEN
        UTL_FILE.PUT_LINE(v_output_file, ']}');
        UTL_FILE.FCLOSE(v_output_file);
    END IF;

EXCEPTION
    WHEN NO_DATA_FOUND THEN
        DBMS_OUTPUT.PUT_LINE('No data found for the given period.');
    WHEN UTL_FILE.INVALID_PATH THEN
        DBMS_OUTPUT.PUT_LINE('Invalid file path specified.');
    WHEN UTL_FILE.INVALID_OPERATION THEN
        DBMS_OUTPUT.PUT_LINE('Invalid operation on the file.');
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('An error occurred: ' || SQLERRM);
        IF p_output_path IS NOT NULL THEN
            UTL_FILE.FCLOSE(v_output_file);
        END IF;
END;
/


SET SERVEROUTPUT ON;
EXEC REPORT_MANUFACTURED_PRODUCTS(TO_DATE('2024-01-01', 'YYYY-MM-DD'), TO_DATE('2024-10-20', 'YYYY-MM-DD'));
