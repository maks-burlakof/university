-- Rollback: Dropping tables


-- Drop TechnologicalMapsTools table
BEGIN
    EXECUTE IMMEDIATE 'DROP TABLE TECHNOLOGICALMAPSTOOLS';
    DBMS_OUTPUT.PUT_LINE('Table TechnologicalMapsTools dropped successfully.');
EXCEPTION
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('Error dropping TechnologicalMapsTools: ' || SQLERRM);
END;
/


-- Drop Production table
BEGIN
    EXECUTE IMMEDIATE 'DROP TABLE PRODUCTION';
    DBMS_OUTPUT.PUT_LINE('Table Production dropped successfully.');
EXCEPTION
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('Error dropping Production: ' || SQLERRM);
END;
/


-- Drop TechnologicalMap table
BEGIN
    EXECUTE IMMEDIATE 'DROP TABLE TECHNOLOGICALMAP';
    DBMS_OUTPUT.PUT_LINE('Table TechnologicalMap dropped successfully.');
EXCEPTION
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('Error dropping TechnologicalMap: ' || SQLERRM);
END;
/


-- Drop Tools table
BEGIN
    EXECUTE IMMEDIATE 'DROP TABLE TOOLS';
    DBMS_OUTPUT.PUT_LINE('Table Tools dropped successfully.');
EXCEPTION
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('Error dropping Tools: ' || SQLERRM);
END;
/

BEGIN
    EXECUTE IMMEDIATE 'DROP INDEX IDX_TOOLS_WEAR_DEGREE';
    DBMS_OUTPUT.PUT_LINE('Index idx_tools_wear_degree dropped successfully.');
EXCEPTION
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('Error dropping index idx_tools_wear_degree: ' || SQLERRM);
END;
/


-- Drop Equipment table
BEGIN
    EXECUTE IMMEDIATE 'DROP TABLE EQUIPMENT';
    DBMS_OUTPUT.PUT_LINE('Table Equipment dropped successfully.');
EXCEPTION
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('Error dropping Equipment: ' || SQLERRM);
END;
/


-- Drop EquipmentType table
BEGIN
    EXECUTE IMMEDIATE 'DROP TABLE EQUIPMENTTYPE';
    DBMS_OUTPUT.PUT_LINE('Table EquipmentType dropped successfully.');
EXCEPTION
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('Error dropping EquipmentType: ' || SQLERRM);
END;
/


-- Drop Product table
BEGIN
    EXECUTE IMMEDIATE 'DROP TABLE PRODUCT';
    DBMS_OUTPUT.PUT_LINE('Table Product dropped successfully.');
EXCEPTION
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('Error dropping Product: ' || SQLERRM);
END;
/


-- Drop Employee table
BEGIN
    EXECUTE IMMEDIATE 'DROP TABLE EMPLOYEE';
    DBMS_OUTPUT.PUT_LINE('Table Employee dropped successfully.');
EXCEPTION
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('Error dropping Employee: ' || SQLERRM);
END;
/

BEGIN
    EXECUTE IMMEDIATE 'DROP INDEX IDX_EMPLOYEE_POSITION';
    DBMS_OUTPUT.PUT_LINE('Index idx_employee_position dropped successfully.');
EXCEPTION
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('Error dropping index idx_employee_position: ' || SQLERRM);
END;
/


-- Drop JobPosition table
BEGIN
    EXECUTE IMMEDIATE 'DROP TABLE JOBPOSITION';
    DBMS_OUTPUT.PUT_LINE('Table JobPosition dropped successfully.');
EXCEPTION
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('Error dropping JobPosition: ' || SQLERRM);
END;
/

BEGIN
   EXECUTE IMMEDIATE 'DROP SYNONYM EMPLOYEEJOBPOSITION';
   DBMS_OUTPUT.PUT_LINE('Synonym JobPositionSyn dropped successfully.');
EXCEPTION
   WHEN OTHERS THEN
       DBMS_OUTPUT.PUT_LINE('Error dropping synonym JobPositionSyn: ' || SQLERRM);
END;
/


COMMIT;
