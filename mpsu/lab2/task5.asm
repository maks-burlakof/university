.include "m328pdef.inc"
; умножение
	lsl r14
	adc r19,r21
	lsl r15
	adc r14, r21
	lsl r19
	lsl r14
	adc r19, r21
	lsl r15
	adc r14, r21
	sts 0x0348, r19
	sts 0x0349, r14
	sts 0x034A, r15
end:
	rjmp end

; деление
;	ldi r19, 0b10000000
;	lsr r15
;	lsr r14
;	adc r2, r3
;	cpse r2, r3
;	add r15, r19
;	lsr r15
;	lsr r14
;	adc r3, r4
;	cpse r3, r4
;	add r15, r19
;	sts 0x0348, r14
;	sts 0x0349, r15
;end:
;	rjmp end