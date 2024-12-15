# Lab 5: Триггеры

## Task

- Написать DML-триггер, регистрирующий изменение данных (вставку, обновление, удаление) в одной из таблиц БД.
  - Во вспомогательную таблицу LOG1 записывать, кто, когда (дата и время) и какое именно изменение произвел
  - для одного из столбцов сохранять старые и новые значения.

- Написать DDL-триггер, протоколирующий действия пользователей по созданию, изменению и удалению таблиц в схеме во вспомогательную таблицу LOG2 в определенное время и запрещающий эти действия в другое время.

- Написать системный триггер, добавляющий запись во вспомогательную таблицу LOG3, когда пользователь подключается или отключается. В таблицу логов записывается имя пользователя (USER), тип активности (LOGON или LOGOFF), дата (SYSDATE), количество записей в основной таблице БД.

- Написать триггеры, реализующие бизнес-логику (ограничения) в заданной вариантом предметной области.
  - Увеличение степени износа инструментов после изготовления. 
`TOOLS.WEAR_DEGREE -= (1 * TECHNOLOGICALMAPSTOOLS.NUMBER_OF_REQUIRED_TOOLS) * NUMBER_OF_REQUIRED_PRODUCTS`.
  - При создании записи изготовления кол-во требуемых инструментов не должно превышать количество имеющихся.
  - OPTIONAL: При создании записи изготовления требуемое количество инструментов резервируется на время всего изготовления.
  - При оформлении технологической карты контролировать рабочее время: понедельник – пятница с 8:00 до 17:00 (обед с 12:30 до 13:30) для оборудования и для рабочих, не допускать одновременной работы (график можно формировать самостоятельно, но не более 40 ч в неделю для каждого рабочего).
  - Следить за количеством инструмента на складе, его износом и соответствием определенному оборудованию при формировании карт.
  - Пополнять склад инструментов, если его количество достигает установленных минимальных значений.

  - Количество и тип триггеров (строковый или операторный, выполняется AFTER или BEFORE)  определять самостоятельно исходя из сути заданий и имеющейся схемы БД
  - учесть, что в некоторых вариантах первые два задания могут быть выполнены в рамках одного триггера, а также возможно возникновение мутации, что приведет к совмещению данного пункта лабораторной работы со следующим.
  - Третий пункт задания предполагает использование планировщика задач, который обязательно должен быть настроен на многократный запуск с использованием частоты, интервала и спецификаторов.

- Самостоятельно или при помощи преподавателя составить задание на триггер, который будет вызывать мутацию таблиц, и решить эту проблему одним из двух способов (при помощи переменных пакета и двух триггеров или при помощи COMPAUND-триггера).

- Написать триггер INSTEAD OF для работы с не обновляемым представлением, созданным после выполнения п. 2.4 задания к лабораторной работе №3, проверить DML-командами возможность обновления представления после включения триггера (логика работы триггера определяется спецификой предметной области варианта).