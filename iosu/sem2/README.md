# ИОСУ, семестр 7

🔑 Информационное обеспечение систем управления

Вариант выполненных заданий: 14

**Содержание:**

- [lab 1](lab1/)
- [lab 2](lab2/)
- [lab 3](lab3/)
- [lab 4](lab4/)
- [lab 5](lab5/)
- [lab 6](lab6/)

<hr>

## Quick overview

### System commands

- `sqlplus` - run sqlplus from the terminal
- `cl scr` - clear window
- `host cls` - clear window from the windows terminal
- `SET LIN 200` - line width

**Display schemas:**

- `SELECT username FROM dba_users;`
- `SELECT username FROM all_users;`

**Display tables inside schema:**

- `SELECT table_name FROM user_tables;`
- `SELECT owner, table_name FROM all_tables;`
- `SELECT table_name FROM all_tables WHERE owner = "MAKSIM";`

**Show schema:**

- `DESCRIBE table_name;`

```sql
SELECT column_name, data_type, data_length
FROM user_tab_columns
WHERE table_name = 'EMPLOYEES';
```

**Execute scripts:**

`@C:\scripts\myscript.sql`
