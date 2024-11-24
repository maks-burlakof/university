-- 5. Test all created functions and procedures.

BEGIN
    -- Procedure: REPORT_MANUFACTURED_PRODUCTS

    DBMS_OUTPUT.PUT_LINE('================================================================================');
    DBMS_OUTPUT.PUT_LINE('Procedure: REPORT_MANUFACTURED_PRODUCTS from global scope.');
    DBMS_OUTPUT.PUT_LINE('Successful execution.');
    REPORT_MANUFACTURED_PRODUCTS(TO_DATE('2024-01-01', 'YYYY-MM-DD'), TO_DATE('2024-10-20', 'YYYY-MM-DD'));

    DBMS_OUTPUT.PUT_LINE('================================================================================');
    DBMS_OUTPUT.PUT_LINE('Procedure: REPORT_MANUFACTURED_PRODUCTS from global scope.');
    DBMS_OUTPUT.PUT_LINE('Successful execution with optional EquipmentType ID.');
    REPORT_MANUFACTURED_PRODUCTS(TO_DATE('2024-01-01', 'YYYY-MM-DD'), TO_DATE('2024-10-20', 'YYYY-MM-DD'), 1);

    DBMS_OUTPUT.PUT_LINE('================================================================================');
    DBMS_OUTPUT.PUT_LINE('Procedure: REPORT_MANUFACTURED_PRODUCTS from global scope.');
    DBMS_OUTPUT.PUT_LINE('Successful execution with optional output filename.');
    REPORT_MANUFACTURED_PRODUCTS(TO_DATE('2024-01-01', 'YYYY-MM-DD'), TO_DATE('2024-10-20', 'YYYY-MM-DD'), NULL, 'test-manufactured-products-report.json');

    DBMS_OUTPUT.PUT_LINE('================================================================================');
    DBMS_OUTPUT.PUT_LINE('Procedure: REPORT_MANUFACTURED_PRODUCTS from global scope.');
    DBMS_OUTPUT.PUT_LINE('Successful execution: no data from given date range.');
    REPORT_MANUFACTURED_PRODUCTS(TO_DATE('2024-10-26', 'YYYY-MM-DD'), TO_DATE('2024-10-27', 'YYYY-MM-DD'));


    -- Function: FUNC_CHECK_TOOLS_STOCK

    DBMS_OUTPUT.PUT_LINE('================================================================================');
    DBMS_OUTPUT.PUT_LINE('Function: FUNC_CHECK_TOOLS_STOCK from global scope.');
    DBMS_OUTPUT.PUT_LINE('Successful execution.');
    DBMS_OUTPUT.PUT_LINE(FUNC_CHECK_TOOLS_STOCK);


    -- Function overloaded 1: FUNC_AVG_WEAR_DEGREE_BY_EQUIPMENT
    
    DBMS_OUTPUT.PUT_LINE('================================================================================');
    DBMS_OUTPUT.PUT_LINE('Function overloaded 1: FUNC_AVG_WEAR_DEGREE_BY_EQUIPMENT from package PKG_OVERLOADED_FUNCTIONS.');
    DBMS_OUTPUT.PUT_LINE('Successful execution.');
    DBMS_OUTPUT.PUT_LINE(PKG_OVERLOADED_FUNCTIONS.FUNC_AVG_WEAR_DEGREE_BY_EQUIPMENT(1));

    DBMS_OUTPUT.PUT_LINE('================================================================================');
    DBMS_OUTPUT.PUT_LINE('Function overloaded 1: FUNC_AVG_WEAR_DEGREE_BY_EQUIPMENT from package PKG_OVERLOADED_FUNCTIONS.');
    DBMS_OUTPUT.PUT_LINE('Unsuccessful execution: do data found with provided Equipment ID.');
    DBMS_OUTPUT.PUT_LINE(PKG_OVERLOADED_FUNCTIONS.FUNC_AVG_WEAR_DEGREE_BY_EQUIPMENT(10000));


    -- Function overloaded 2: FUNC_AVG_WEAR_DEGREE_BY_EQUIPMENT
    
    DBMS_OUTPUT.PUT_LINE('================================================================================');
    DBMS_OUTPUT.PUT_LINE('Function overloaded 2: FUNC_AVG_WEAR_DEGREE_BY_EQUIPMENT from package PKG_OVERLOADED_FUNCTIONS.');
    DBMS_OUTPUT.PUT_LINE('Successful execution.');
    DBMS_OUTPUT.PUT_LINE(PKG_OVERLOADED_FUNCTIONS.FUNC_AVG_WEAR_DEGREE_BY_EQUIPMENT('Welding machine'));

    DBMS_OUTPUT.PUT_LINE('================================================================================');
    DBMS_OUTPUT.PUT_LINE('Function overloaded 1: FUNC_AVG_WEAR_DEGREE_BY_EQUIPMENT from package PKG_OVERLOADED_FUNCTIONS.');
    DBMS_OUTPUT.PUT_LINE('Unsuccessful execution: do data found with provided Equipment Title.');
    DBMS_OUTPUT.PUT_LINE(PKG_OVERLOADED_FUNCTIONS.FUNC_AVG_WEAR_DEGREE_BY_EQUIPMENT('Not-existing equipment'));
END;
/