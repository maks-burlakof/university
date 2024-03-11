.include "m328pdef.inc"

.def six  = r19
.def sixty = r20

sum:
	ldi r16, 0x00  ; 1й операнд
	ldi r17, 0x48  ; 2й операнд

	ldi r28, 0b01100110  ; (0x66)(102)
	ldi six, 0b00000110  ; (0x06)(6)
	ldi sixty, 0b01100000  ; (0x60)(96)
	neg six  ; (0xFA)(250)
	neg sixty  ; (0xA0)(160)
	add r16, r28  ; проверка на необходимость коррекции
	add r16, r17
	brhc correcth
	brcc correctc
	; adc r2,r3
end:
	rjmp end

correcth:
	; adc r2, r3
	add r16, six
	; cpse r2,r3
	; rjmp end
	clc
	; rjmp correctc
correctc:
	; adc r2,r3
	add r16, sixty
	rjmp end

; ответ в r16
