.include "m328pdef.inc"
	clr r17       ; сброс счетчика
	ldi r20, 6
	ldi r18, 0x48
	ldi r16, 0x00
	out DDRC, r16
	ldi r16, 0b00001111  ; настройка на ввод линий 0-3 порта B
	out DDRB, r16
	ldi r16, 0b11110000  ; настройка на вывод линий 4-7 порта D
	out DDRD, r16
main:
	sbis PINC, 2  ; проверить кнопку reset
	clr r17       ; сброс счетчика если нажата
	sbic PINC, 0  ; проверить кнопку счетчика
	rjmp clearT   ; перейти если не нажата
	brts a
	cpse r17, r18
	inc r17
	rcall addsix
	set	  
a:
	mov r19, r17
	andi r19, 0b11110000
	out PORTD, r19
	mov r19, r17
	andi r19, 0b00001111
	out PORTB, r19
	rjmp main	  
clearT:
	clt
	rjmp a
addsix:
	add r17, r20
	brhs b
	sub r17, r20
b:
	ret
