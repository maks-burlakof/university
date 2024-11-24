-- 4. Check immutable view


-- Success: Retrieve all records from the view
SELECT * FROM VIEW_MALE_EMPLOYEES;


-- Success: Update the one record in view
UPDATE VIEW_MALE_EMPLOYEES
SET FIRST_NAME = 'John'
WHERE EMPLOYEE_ID = 1;


-- Failure: Update the one record in view: The column does not exist in the view
UPDATE VIEW_MALE_EMPLOYEES
SET MIDDLE_NAME = 'F'
WHERE EMPLOYEE_ID = 2;


-- Failure: Update the one record in view: Gender field is immutable
UPDATE VIEW_MALE_EMPLOYEES
SET GENDER = 'F'
WHERE EMPLOYEE_ID = 3;


-- Failure: Update the one record in view: JOB_POSITION represents a non-key preserved table
UPDATE VIEW_MALE_EMPLOYEES
SET JOB_POSITION = 'Supply manager'
WHERE EMPLOYEE_ID = 1;


-- Failure: Insert into view because the view has JOINs
INSERT INTO VIEW_MALE_EMPLOYEES (FIRST_NAME, LAST_NAME, GENDER)
VALUES ('Alex', 'Smith', 'M');


-- Failure: Delete from view because the view has JOINs
DELETE FROM VIEW_MALE_EMPLOYEES
WHERE EMPLOYEE_ID = 3;
