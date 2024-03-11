.include "m328pdef.inc"
	ldi r18, 0b00000101
	ldi r17, 0b11111010
	eor r14, r18  ; инверсия
	and r14, r17  ; сброс
	or r14, r18  ; установка в 1
end:
	rjmp end