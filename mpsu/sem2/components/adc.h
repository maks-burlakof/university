#ifndef ADC_H
#define ADC_H

#include <stdint.h>

#define ADC_MIN 0
#define ADC_MAX 676
#define ADC_MAX_DISPLAY 15

void adc_init(void);
uint16_t adc_read(uint8_t channel);
int8_t adc_to_display(int16_t adc_value);

#endif