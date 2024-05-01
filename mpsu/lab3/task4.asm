.include "m328pdef.inc"

.cseg
.org 0x0000 jmp reset        ;(Reset)
.org 0x0002 jmp lineA        ;(INT0) External Interrupt Request 0
.org 0x0004 jmp lineB        ;(INT1) External Interrupt Request 1
.org INT_VECTORS_SIZE        ;Конец таблицы прерываний

lineA:
	  in r18, PIND
	  andi r18, 0b00001100
	  cpi r18, 0x00
	  breq a
	  cpi r18, 0b00001100
	  breq a
	  cpse r17, r19
	  inc r17
	  rcall addsix
	  rjmp ret0

a:    cpi r17, 0x00
	  breq ret0
	  subi r17, 1
	  brhc ret0
	  subi r17, 0x06
ret0: reti

lineB:
	  in r18, PIND
	  andi r18, 0b00001100
	  cpi r18, 0x00
	  breq b
	  cpi r18, 0b00001100
	  breq b
	  cpi r17, 0x00
	  breq ret1
	  subi r17, 1
	  brhc ret1
	  subi r17, 0x06
      rjmp ret1

b:    cpse r17, r19
	  inc r17
	  rcall addsix
ret1: reti

reset:
	ldi r17, 0x24
	ldi r19, 0x48
	;настройка портов
	ldi r16, 0b00001111        ;Настройка на вывод линий 0..3 порта B
	out DDRB, r16
	ldi r16, 0b11110000        ;Настройка на вывод линий 4..7 D
	out DDRD, r16
	ldi r16, 0b00000000
	out DDRC, r16
	
	;настройка прерываний
	ldi r16, LOW(RAMEND)       ;Старт программы
	out SPL, r16               ;Обязательная инициализация стека
	ldi r16, HIGH(RAMEND)      ;Указатель стека устанавливается на конец ОЗУ
	out SPH, r16
	ldi r16, 0b00000011        ;Разрешить прерывания INT0 и INT1 локально
	out EIMSK, r16
	ldi r16, 0b00000101        ;Настройка условия генерации прерывания по изменению
	sts EICRA, r16
	sei                        ;Разрешить прерывания глобально

main:
	  sbis PINC, 0             ;Проверить кнопку RESET
	  ldi r17, 0x24	           ;Если нажата, то сброс счётчика

	  mov r16, r17
	  out PORTD, r16
	  out PORTB, r16
	  rjmp main
	
addsix:
	  ldi r16, 0x06 
	  add r17, r16
	  brhs c
	  sub r17, r16
c:	  ret
