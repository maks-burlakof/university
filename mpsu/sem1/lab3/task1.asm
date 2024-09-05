.include "m328pdef.inc"
	ldi r16, 0b00000000  ; настройтка на ввод
	out DDRC, r16
	ldi r16, 0b00000100  ; настройка на вывод
	out DDRC, r16
main:
	sbic PINC, 0
	rjmp skip
	out PORTC, r16
	rjmp main
skip:
	out PORTC, r2
	rjmp main
