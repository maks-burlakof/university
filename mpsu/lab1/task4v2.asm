.include "m328pdef.inc"

init:
	ldi r16, 0x48  ; делимое
	mov r14, r16
	clr r16
	lds r15, 0x0248  ; делитель
	ldi r21, 0x09  ; счетчик
division:
	rol r14
	dec r21
	brne remainder  ; перейти если Z != 0
	sts 0x0348, r14
	sts 0x0349, r16
end:
	rjmp end
remainder:
	rol r16  ; с учетом С
	sub r16, r15
	brcc remainder2  ; перейти если С = 0
	add r16, r15
	clc  ; очистить С
	rjmp division
remainder2:
	sec
	rjmp division

; r14 - делимое и частное, r15 - делитель, r16 - остаток
