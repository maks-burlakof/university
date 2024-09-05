.include "m328pdef.inc"
.cseg
.org $0000 rjmp Reset        ;Reset
.org $002A rjmp ADC_Int      ;преобразование ацп выполнено
.org INT_VECTORS_SIZE        ;конец таблицы прерываний
.def rd1l=r0                 ;делимое младший
.def rd1h=r1                 ;делимое старший
.def rd1u=r2                 ;временный регистр
.def rd2=r19                 ;делитель
.def rel=r4                  ;результат младший
.def reh=r5                  ;результат старший
.def acp=r17                 ; 
.def temp=r23
.def rez=r24

Reset:
	ldi r16,Low(RAMEND)      ;старт
    out SPL,r16              ;обязательная инициализация стека
    ldi r16,High(RAMEND)     ;указатель стека устанавливается
    out SPH,r16              ;на конец озу
    ldi r16, 0b11110000      ;настройка на вывод порта D
	out DDRD, r16
    ldi r16, 0b00001111      ;настройка на вывод порта B
    out DDRB, r16
    ldi r16,0
    out DDRC,r16             ;Port C - вход для ацп
    sei                      ;разрешить прерывания глобально
      
;          7     6     5     4     3     2     1     0
;ADMUX = REFS1 REFS0 ADLAR  MUX4  MUX3  MUX2  MUX1  MUX0

	ldi r16,0b00100000       ;опорное - напряжение питания
	sts ADMUX,r16            ;результат выравнивается влево
                             ;0-й канал АЦП

;           7    6     5     4     3     2     1     0
;ADCSRA = ADEN ADSC  ADATE ADIF  ADIE  ADPS2 ADPS1 ADPS0

	ldi r16,0b11001111       ;разрешить ацп-прерывание и CLK/128
	sts ADCSRA,r16           ;старт преобразования
	ldi rd2,0x7f
      
main:
	out portb,rez
	out portd,rez 
	rjmp main                ;бесконечный цикл

ADC_Int:
	lds acp,ADCH	         ;запись результата 
	ror acp                  ;оставляем 7 старших бит
	ldi temp, 0x30	         ;максимум шкалы (48)
	mul acp,temp             ;умножение

div16:                       ;начало процесса деления
	clr rd1u 
	clr reh 
	clr rel 
	inc rel

div8a:
	clc 
    rol rd1l 
    rol rd1h 
    rol rd1u
    brcs div8b 
    cp rd1u,rd2 
    brcs div8c 
  
div8b:
	sub rd1u,rd2
    sec 
    rjmp div8d 
  
div8c:
	clc 
  
div8d:
	rol rel 
    rol reh
    brcc div8a 
    mov rez,r4              ;конец процесса деления и сохранение результата в rez

HEX_to_BCD:                 ;перевод из шестнадцатиричной системы в десятичную
	clr     temp            ;очищаем вспомогательный регистр 

HEX_to_BCD_l: 
	subi    rez,10          ;temp = temp — 10
    brcs    HEX_to_BCD_2    ;прервать если перенос установлен	
    inc     temp            ;+1 в temp
    rjmp 	   HEX_to_BCD_l ;проходим по циклу

HEX_to_BCD_2: 
	subi    rez,-10         ;компенсация отрицательного значения r16
    swap    temp            ;меняем тетрады местами
    or      rez,temp        ;объединяем полученные значения в упакованный десятичный код
		
    lds r16,ADCSRA
    sbr r16,(1 << ADSC)
    sts ADCSRA,r16          ;запуск преобразования снова
    reti
