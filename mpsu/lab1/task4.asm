.include "m328pdef.inc"

start:
	ldi r17, 0x08  ; счетчик 8ми циклов
	ldi r25, 0x01  ; единица для операции "логическое или с присвоением" по определению значения флага С
	ldi r18, 0xE9  ; делимое
	mov r14, r18
	ldi r18, 0x08  ; делитель
	sts 0x0248, r18
	clr r18
	lds r19, 0x0248
m0:
	mov r16, r14  ;делимое копируется в отдельную ячейку для побитового смещения влево
	rol r16       ;смещение влево с записью утраченного разряда во флаг С
	mov r14, r16  ;значение после смещения копируется в начальную ячейку
	mov r16, r21  ;значение после смещения копируется в отдельную ячейку 21, хранящуюся остаток
	rol r16       ;второе смещение делимого влево 
	sub r16, r19  ;разность r16=r16-r19
	brcc m1       ;переход по метке m1 в случае равенства флага С нулю
	add r16, r19  ;возврат r16 к предыдущему значениею путем сложения r16=r16+r19
m1:
	mov r21, r16  ;копирование из r16 в r21
	in r26, SREG  ;ввод значений всех флагов(SERG) из пространства входа в регистр r26 
	andi r26, 0x01;логическое И между единицей и b0(в котором записан флаг С). в случае равенства нулевого бита ячейки единице возвращает в b0 единицу, иначе 0
	eor r26, r25  ;логическое исключающее ИЛИ(если бит b0=1, он обнуляется)
	out SREG, r26 ;вывод значения r26 в пространство входа(значение всех флагов кроме С - ноль, сам С либо 0 либо 1)
	mov r16, r20  ;копирование из r20 в r16
	rol r16       ;сдвиг r16 влево на один знак с записью флага С в b0 r16
	mov r20, r16  ;копирование из r16 в r20
	dec r17       ;счетчик команд r17=8-1=7. при отрицательном его значении следующая команда останавливает цикл
	brne m0       ;переход по метке m0 если значение флага Z ненулевое
	sts 0x0348, r16 ;запись частного в адресную ячейку 344
	sts 0x0349, r21 ;запись остатка в адресную ячейку 345
end:
	rjmp end
