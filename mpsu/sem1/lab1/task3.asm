.include "m328pdef.inc"

init:
	ldi r16, 0xAB  ; запись в 0x0248, 0x0249
	ldi r17, 0xDC
	sts 0x0248, r16
	sts 0x0249, r17
	ldi r16, 0xFE  ; запись в r14
	mov r14, r16
	clr r16
	clr r17
main:
	lds r19, 0x0248
	lds r18, 0x0249
	mul r18, r14  ; мл.б. на r14
	sts 0x034A, r0
	mov r20, r1  ; ст.б.произведения
	mul r19, r14  ; ст.б. на r14
	add r0, r20  ; мл.б.произведения + ст.б.произведения
	adc r1, r21  ; ст.б.произведения + пустое + флаг полупереноса
	sts 0x0348, r1
	sts 0x0349, r0
end:
	rjmp end
