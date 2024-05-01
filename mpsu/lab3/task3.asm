.include "m328pdef.inc"
.cseg
.org $0000 jmp RESET      ;(Reset)
.org $0002 jmp Ext_INT0   ;(INT0) External Interrupt Request 0
.org $0004 jmp Ext_INT1   ;(INT1) External Interrupt Request 1
.org INT_VECTORS_SIZE     ;Конец таблицы прерываний

Ext_INT0:                 ;Обработчик прерывания по входу INT0
	cpi r22, 0x30         ;Сравнить с числом 48
	breq ret0             ;Выйти из блока если равно
	inc r18
	inc r22
	mov r20, r18
	cpi r20, 0x3A
	brne ret0             ;Выйти из блока если не равно
	ldi r18, 0x30
	inc r21
ret0:reti                 ;Выход из обработчика прерывания

Ext_INT1:                 ;Обработчик прерывания по входу INT1
	cpi r22, 0x00         ;Сравнить с числом 0
	breq ret1             ;Выйти из блока если равно
	dec r18
	dec r22
	cpi r18, 0x2F
	brne ret1             ;Выйти из блока если не равно
	ldi r18, 0x39
	dec r21
ret1:reti                 ;Выход из обработчика прерывания

Reset:                    
	ldi r16, Low(RAMEND)  ;Старт программы
	out SPL, r16          ;Обязательная инициализация стека
	ldi r16, High(RAMEND) ;Указатель стека устанавливается на конец ОЗУ
	out SPH, r16
	ldi r16, 0b00000011   ;Разрешить прерывания INT0 и INT1 локально
	out EIMSK, r16        
	ldi r16, 0b00001010   ;Настройка условия генерации прерывания по спаду входного сигнала
	sts EICRA, r16
	sei                   ;Разрешить прерывания глобально
	ldi r16, 0b11110000   ;Настройка на вывод линий 4..7
	out DDRD, r16         ;и на ввод линий 0..3 порта D
	rcall LCD_Init
	ldi r18, 0x30
	ldi r21, 0x30
	clr r22

main:
	sbis PINC, 0          ;Проверить кнопку RESET
	rjmp sbros            ;Если нажата, то перейти
	sts 0x203, r21
	sts 0x204, r18
	ldi r17, 0x05
	rcall LCD_Update
	rjmp main

sbros:
	clr r22               ;Сброс счётчика
	ldi r21, 0x30
	ldi r18, 0x30
	rjmp main

.include "hd44780.asm"
