.include "m328pdef.inc"

init:
	ldi r16, 0x00  ; ������ � r14
	mov r14, r16
	ldi r17, 0x48  ; ������ � 0x0248
	sts 0x0248, r17
main:
	lds r18, 0x0248
	sub r14, r18  ; sub ��� ���������, add ��������
	sts 0x0348, r14
end:
	rjmp end
