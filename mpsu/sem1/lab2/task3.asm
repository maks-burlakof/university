.include "m328pdef.inc"
	mov r17, r14
	andi r17, 0b00000101  ; проверка 0 и 2 битов
	cpi r17, 0b00000101  ; 0x05
	breq save  ; переход если Z = 1
	mov r17, r14
	andi r17, 0b01010000  ; выделение 4 и 6 битов
	ldi r18, 0b01000000  ; маска для инвертирования 6 бита
	eor r17, r18  ; инвертирование 6 бита
	cpi r17, 0b01010000  ;проверка 4 и 6 битов
	breq save
	sts 0x0248, r0
end:
	rjmp end
save:
	ldi r17, 0x01
	sts 0x0248, r17
	rjmp end