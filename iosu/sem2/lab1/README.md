# Lab 1

## Task

- Создать собственную базу данных по полученному варианту
  - создать таблицы, указав автоинкрементные столбцы с помощью синтаксиса GENERATED и ограничения NOT NULL, где необходимо;
  - придумать и создать ограничения (CHECK, UNIQUE), добавить их в схему с помощью инструкции ALTER TABLE; 
  - создать индексы, синонимы, обосновать их необходимость;
  - внести данные в таблицы, хотя бы в одной из таблиц использовать для заполнения инструкцию INSERT ALL.

## Environment setup for Oracle Database 18c Express Edition Release 18.0

```oraclesqlplus
-- Connect as SYSTEM with your password
alter session set "_ORACLE_SCRIPT"=true;
CREATE USER TOOLSTORAGE IDENTIFIED BY YOUR_PASSWORD;
ALTER USER TOOLSTORAGE DEFAULT TABLESPACE users QUOTA UNLIMITED ON users;
ALTER USER TOOLSTORAGE TEMPORARY TABLESPACE temp;
GRANT CREATE SESSION, CREATE VIEW, ALTER SESSION, CREATE SEQUENCE TO TOOLSTORAGE;
GRANT CREATE SYNONYM, CREATE DATABASE LINK, RESOURCE , UNLIMITED TABLESPACE TO TOOLSTORAGE;
GRANT CREATE ANY DIRECTORY TO TOOLSTORAGE;
```

```oraclesqlplus
-- Create tables
@"D:\bsuir\sem7\iosu\labs\lab1\1_create_tables.sql"
SELECT table_name FROM user_tables;

-- Insert data
@"D:\bsuir\sem7\iosu\labs\lab1\2_insert_data.sql"
SELECT * FROM employee;
SELECT * FROM production;

-- Rollback
host cls
@"D:\bsuir\sem7\iosu\labs\lab1\3_rollback.sql"
SELECT table_name FROM user_tables;
```
