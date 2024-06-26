# МПСУ, семестр 6

🔑 Микропроцессорные системы управления

**Содержание:**

- [lab 1](#1️⃣-lab-1-алгоритмы-арифметической-обработки-данных)
- [lab 2](#2️⃣-lab-2-алгоритмы-логической-обработки-данных)
- [lab 3](#3️⃣-lab-3-организация-ввода-и-вывода-информации-механизм-прерываний)

<hr>

## 1️⃣ lab 1. Алгоритмы арифметической обработки данных

**🔗 [Source code](lab1/)**

**Исходные данные:** $` R = 14, R1 = 15, ** = 48 `$.

> В задачах 1, 2, 3 код в метке init используется только для дебага, в решении его отражать не нужно.

### Задача 1

Написать программу сложения (вычитания) двух 8-разрядных двоичных чисел, одно из которых содержится в регистре R14, а второе – в ячейке памяти данных с адресом 0x0248. Результат поместить в память данных по адресу 0x0348. Исходные операнды задаются на этапе выполнения программы в режиме отладки.

| 1-й операнд | 2-й операнд | Сумма | C | N | V | S | Z | Разность | C | N | V | S | Z |
|-            |-            |-      |-  |-  |-  |-  |-  |-         |-  |-  |-  |-  |-  |
| 88          | 48          | D0    | 0 | 1 | 0 | 1 | 0 | 40       | 0 | 0 | 1 | 1 | 0 |
| 00          | 48          | 48    | 0 | 0 | 0 | 0 | 0 | B8       | 1 | 1 | 0 | 1 | 0 |
| FF          | 48          | 47    | 1 | 0 | 0 | 0 | 0 | B7       | 0 | 1 | 0 | 1 | 0 |

### Задача 2

Написать программу сложения (вычитания) двух 16-разрядных двоичных чисел, одно из которых содержится в регистрах R14, R15, а второе – в ячейках памяти данных с адресами 0x0248, 0x0249. Результат поместить в ячейки памяти данных с адресами 0x0348, 0x0349. Исходные операнды задаются на этапе выполнения программы в режиме отладки.

| 1-й операнд | 2-й операнд | Сумма | C | N | V | S | Z | Разность | C | N | V | S | Z |
|-            |-            |-      |-  |-  |-  |-  |-  |-         |-  |-  |-  |-  |-  |
| 8888        | 48AB        | D133  | 0 | 1 | 0 | 1 | 0 | 3FDD     | 0 | 0 | 1 | 1 | 0 |
| 0000        | AB48        | AB48  | 0 | 1 | 0 | 1 | 0 | 54B8     | 1 | 0 | 0 | 0 | 0 |
| FFFF        | A48B        | A48A  | 1 | 1 | 0 | 1 | 0 | 5B74     | 0 | 0 | 0 | 0 | 0 |

### Задача 3

Написать программу умножения 16-разрядного операнда, находящегося в ячейках памяти данных с адресами 0x0248, 0x0249 на 8-разрядный операнд 48, находящийся в регистре R14. Результат разместить в памяти данных, начиная с адреса 0x0348.

Программы проверить на примерах:  
1 ) 0002<sub>16</sub> • 48<sub>16</sub> = 000090<sub>16</sub>  
2 ) 0010<sub>16</sub> • 48<sub>16</sub> = 000480<sub>16</sub>  
3 ) 0100<sub>16</sub> • 48<sub>16</sub> = 004800<sub>16</sub>  
4 ) А48В<sub>16</sub> • 48<sub>16</sub> = 2E4718<sub>16</sub>

### Задача 4

Написать программу деления операнда 48, находящийся в регистре R14 на 8-разрядный операнд, находящийся в ячейке памяти данных с адресом 0x0248. Сохранить частное в ячейке памяти данных с адресом 0x0348, а остаток – в ячейке 0x0349. Написать коментарии, поясняющие принцип работы алгоритма. Время выполнения программы не должно зависеть от входных данных.

Программу проверить на примерах:  
1 ) 48<sub>16</sub> : 02<sub>16</sub> = 24(00)<sub>16</sub>  
2 ) 48<sub>16</sub> : 10<sub>16</sub> = 04(08)<sub>16</sub>  
3 ) 48<sub>16</sub> : 0F<sub>16</sub> = 04(0С)<sub>16</sub>

### Задача 5

Написать программу сложения (вычитания) двухразрядных двоично-десятичных чисел, одно из которых содержится в регистре R14, а второе – в ячейке памяти данных с адресом 0x0248.

| 1-й операнд | 2-й операнд | Сумма | Разность |
|-            |-            |-      |-         |
| 49          | 48          | 97    | 01       |
| 00          | 48          | 48    | 52       |
| 99          | 48          | 47    | 51       |

## 2️⃣ lab 2. Алгоритмы логической обработки данных

**🔗 [Source code](lab2/)**

**Исходные данные:** $` R = 14, R1 = 15, ** = 48, i = 0, j = 2, k = 4, l = 6 `$.

### Задача 1

Написать программу, которая позволяет установить, сбросить, инвертировать 0 и 2 биты заданного операнда, находящегося в регистре R14. Результат представить в виде таблицы. Программы проверить для операндов: FF<sub>16</sub>, F0<sub>16</sub>, 0F<sub>16</sub>, 00<sub>16</sub>.

| Операнд | B<sub>i,j</sub> = 0 | B<sub>i,j</sub> = 1 | B<sub>i,j</sub> = NOT(B<sub>i,j</sub>) |
|-        |-                    |-                    |-                                       |
| FF      | FA                  | FF                  | FA                                     |
| F0      | 0A                  | 0F                  | 0A                                     |
| 0F      | F0                  | F5                  | F5                                     |
| 00      | 00                  | 05                  | 05                                     |

### Задача 2

Написать программу, обеспечивающую проверку 0-го бита заданного операнда, хранящегося в регистре R. Если результат равен 0, то в ячейку памяти данных 0x0200 поместить 0, иначе - поместить 1.
Программу проверить для следующих операндов: FF<sub>16</sub>, F0<sub>16</sub>, 0F<sub>16</sub>, 00<sub>16</sub>.

| Операнд | Результат |
| -       | -         |
| FF      | 01        |
| F0      | 00        |
| 0F      | 01        |
| 00      | 00        |

### Задача 3

Написать программу, обеспечивающую выполнение логической операции:

$$ y=x_{i} \cdot x_{j} + x_{k} \cdot NOT(x_{l}), $$

где 0, 2, 4, 6 – номера битов числа, содержащегося в регистре R14. Результат поместить в память данных по адресу 0x0248. Программу проверить для операндов: 1F<sub>16</sub>, 2B<sub>16</sub>, 0C<sub>16</sub>, A1<sub>16</sub>.

1F = 00011111, 1*1+1*1=1  
2B = 00101011, 1*0+0*1=0  
0C = 00001100, 0*1+0*1=0  
A1 = 10100001, 1*0+0*1=0

### Задача 4

Написать программу, обеспечивающую вычисление суммы единиц в массиве чисел, расположенном в памяти программ. Результат поместить в регистры R14, R15. Количество элементов в массиве – 10<sub>10</sub>. Программу протестировать на случайных числах.

### Задача 5

Написать программы умножения (деления) 16-разрядного беззнакового операнда на 4. Операнд расположен в регистрах R14, R15. Адрес результата – в памяти данных 0x0348, 0x0349, 0x034A. При делении остаток не сохранять. Программы проверить на примерах: 1) 0002<sub>16</sub> • (/) 4; 2) 0010<sub>16</sub> • (/) 4; 3) 0100<sub>16</sub> • (/) 4; 4) А48В<sub>16</sub> • (/) 4.

Указание: воспользоваться операциями логического сдвига влево/вправо.

| Операнд | *      | /    |
| -       | -      | -    |
| 0002    | 000008 | 0000 |
| 0010    | 000040 | 0004 |
| 0100    | 000400 | 0040 |
| A48B    | 02922C | 2922 |

## 3️⃣ lab 3. Организация ввода и вывода информации. Механизм прерываний

**🔗 [Source code](lab3/)**

**Исходные данные:** $` R = 14, R1 = 15, ** = 48, i = 0, j = 2, k = 4 `$.

### Задача 1

Написать программу, обеспечивающую отображение состояния клавиши, подключенной к линии 0 порта C с помощью светодиода, подключенного к линии 2 порта C (нажато – горит, отжато – не горит). Промоделировать работу схемы в Proteus.

### Задача 2

Написать программу, обеспечивающую подсчёт и отображение в десятичном формате нажатий на кнопку, подключенную к линии 0 портов C, D. Сброс в 0 клавишей на линии 2 портов C, D отладочной платформы Arduino UNO. При достижении значения счётчика числа 48, значение больше не увеличивать. Промоделировать работу схемы в Proteus. Отобразить счетчик на двух семисегментых индикаторах: старший - PortD4..7, младший - PortB0..3.

### Задача 3

Написать программу, обеспечивающую увеличение/уменьшение десятичного счётчика в зависимости от нажатия клавиш “+” или “-”, подключенных к линиям портов INT0, INT1 Arduino UNO. При опросе клавиш задействовать механизм внешнего прерывания. Сброс в 0 - клавишей на линии 0 порта C. При достижении значения счётчика 48 значение больше не увеличивать, а также не уменьшать менее 0. Промоделировать работу схемы в Proteus. Отобразить счетчик на ЖКИ с контроллером HD44780 начиная с позиции 4.

### Задача 4

Написать программу, обеспечивающую работу энкодера с отображением десятичного эквивалента поворота ручки энкодера. Сброс в 0 - клавишей на линии 0 порта C. Диапазон значения счётчика 00..48. Промоделировать работу схемы в Proteus. Отладочная платформа - Arduino UNO. При опросе энкодера, подключенного к линиям INT0 и INT1, задействовать механизм внешнего прерывания. Сброс вызывает установку счётчика в середину диапазона – число 24. Отобразить результат на двух семисегментых индикаторах: старший - PortD4..7, младший - PortB0..3.

### Задача 5

Написать программу, считывающую значение аналоговой величины на PortC0,1 в диапазоне 0..1023, и отображающую её на индикаторе в диапазоне 0..48. Опорное напряжение Vref принять равным 5В. Использовать обнаружение готовности данных по прерываниям.
