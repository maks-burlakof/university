.include "m328pdef.inc"

init:
	ldi r21, 0x88  ; запись в r14, r15
	ldi r20, 0x88
	mov r15, r21
	mov r14, r20
main:
	lds r19, 0x0248
	lds r18, 0x0249
	sub r15, r18 ; мл. б., сложение add, вычитание sub
	sbc r14, r19 ; ст. б., сложение adc, вычитание sbc
	sts 0x0348, r14
	sts 0x0349, r15
end:
	rjmp end

; ответ в r14 r15
