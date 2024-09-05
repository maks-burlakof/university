.include "m328pdef.inc"
.def num = r14
.def rez = r15
.cseg
	ldi r18, 0x0A
	ldi zl, LOW(array*2)
	ldi zh, HIGH(array*2)
init:
	ldi r16, 0x09
	clr rez
	lpm num, z+  ; взять из адресного пространства памяти программ число
main:
	dec r16
	lsl num
	brcc m1
	inc rez
m1:
	brne main
	dec r18
	breq end
	rjmp init
end:
	rjmp end
array:
	.db 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A