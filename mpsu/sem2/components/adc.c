#include <avr/io.h>
#include <util/delay.h>

#include "adc.h"


void adc_init(void) {
    // Настраиваем опорное напряжение на AVCC и выбираем канал ADC5 (MUX[3:0] = 0101)
    ADMUX = (1 << REFS0) | (1 << MUX2) | (1 << MUX0);
    // Включаем АЦП, разрешаем делитель на 64 (для частоты АЦП 125 кГц при F_CPU = 8 МГц)
    ADCSRA = (1 << ADEN) | (1 << ADPS2) | (1 << ADPS1);
    _delay_ms(10);
}

uint16_t adc_read(uint8_t channel) {
    ADCSRA |= (1 << ADSC);  // Запускаем преобразование
    while (ADCSRA & (1 << ADSC));  // Ждём завершения преобразования (пока бит ADSC не станет равным 0)
    return ADC;  // Возвращаем 10-битный результат (ADCL и ADCH)
}

int8_t adc_to_display(int16_t adc_value) {
    int16_t display_value;
    int16_t adc_mid = (ADC_MAX + ADC_MIN) / 2;
    display_value = (adc_value - adc_mid) * ADC_MAX_DISPLAY / (adc_mid - ADC_MIN);
    
    if (display_value > ADC_MAX_DISPLAY) {
        display_value = ADC_MAX_DISPLAY;
    } else if (display_value < -ADC_MAX_DISPLAY) {
        display_value = -ADC_MAX_DISPLAY;
    }

    return (int8_t)display_value;
}

int16_t adc_to_motor_speed(int16_t adc_value) {
    int16_t adc_mid = (ADC_MAX + ADC_MIN) / 2;
    int16_t speed_mid = adc_value - adc_mid;
    int16_t speed = (speed_mid * 255) / adc_mid; // -255..255
    return speed;
}