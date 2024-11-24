-- 2. Trigger DDL. Log user behavior on CREATE, UPDATE or DELETE on tables in schema in specific times and disallow it in other times.


-- Create table LOG2

CREATE TABLE LOG2 (
    USERNAME VARCHAR2(30),
    OPERATION_TYPE VARCHAR2(30),
    OPERATION_SUCCESS NUMBER(1),
    OPERATION_DATE TIMESTAMP,
    OBJECT_NAME VARCHAR2(100)
);


-- Create DDL trigger

CREATE OR REPLACE TRIGGER TRG_SCHEMA_CHANGES
AFTER CREATE OR ALTER OR DROP
ON SCHEMA
DECLARE
    v_username VARCHAR2(30);
    v_success NUMBER(1) := 1;
BEGIN
    SELECT USER INTO v_username FROM DUAL;

    IF
        TO_CHAR(SYSTIMESTAMP AT TIME ZONE 'Europe/Moscow', 'DY', 'NLS_DATE_LANGUAGE=ENGLISH') IN ('SAT', 'SUN')
    OR
        TO_CHAR(SYSTIMESTAMP AT TIME ZONE 'Europe/Moscow', 'HH24:MI') NOT BETWEEN '09:00' AND '17:00'
    THEN
        v_success := 0;
    END IF;

    INSERT INTO LOG2 (
        USERNAME, OPERATION_TYPE, OPERATION_SUCCESS, OPERATION_DATE, OBJECT_NAME
    ) VALUES (
        v_username, ORA_SYSEVENT, v_success, SYSTIMESTAMP, ORA_DICT_OBJ_NAME
    );

    IF v_success = 0 THEN
        RAISE_APPLICATION_ERROR(-20002, 'DDL operations are not allowed in that time. You can update schema only in 9AM-6PM and not in weekends');
    END IF;
END;
/


-- DROP trigger
-- DROP TRIGGER TRG_SCHEMA_CHANGES
