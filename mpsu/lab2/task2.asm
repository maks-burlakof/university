.include "m328pdef.inc"
	mov r16, r14
	andi r16, 0b00000001  ; сброс
	breq zero  ; перейти если Z = 1
	ldi r17, 0x01
	sts 0x0200, r17
end:
	rjmp end
zero:
	sts 0x0200, r16
	rjmp end