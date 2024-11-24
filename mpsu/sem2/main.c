#include <avr/io.h>
#include <util/delay.h>
#include <stdlib.h>

#include "components.h"
#include "usart.h"
#include "adc.h"
#include "motor.h"
#include "indicator.h"


#define MOT_IN_PORT PORTB
#define MOT_IN1_PIN 2  // PB2
#define MOT_IN2_PIN 3  // PB3
#define MOT_EN_PORT PORTD
#define MOT_EN_PIN 0 // PD0

#define SEG1_PORT PORTD
#define SEG1_A_PIN 4  // PD4
#define SEG1_B_PIN 5  // PD5
#define SEG1_C_PIN 6  // PD6
#define SEG1_D_PIN 7  // PD7

#define SEG2_PORT PORTC
#define SEG2_A_PIN 0  // PA0
#define SEG2_B_PIN 1  // PA1
#define SEG2_C_PIN 2  // PA2
#define SEG2_D_PIN 3  // PA3


void vApplicationIdleHook(void) {
    __asm__ __volatile__("nop");
}

int main(void) {
    usart_init();
    usart_transmit_string("Hello, proteus!\r\n");
    
    Indicator indicators[2];
    indicator_init(&indicators[0], &port_mappings[2], SEG1_A_PIN, SEG1_B_PIN, SEG1_C_PIN, SEG1_D_PIN);
    indicator_init(&indicators[1], &port_mappings[1], SEG2_A_PIN, SEG2_B_PIN, SEG2_C_PIN, SEG2_D_PIN);
    // indicator_display_number(indicators, 27);

    adc_init();
    
    // Motor motor;
    // motor_init(&motor, MOT_IN1_PIN, MOT_IN2_PIN, MOT_EN_PIN);

    uint16_t adc_value;
    int16_t display_value;
    
    while(1) {
        adc_value = adc_read(0);
        display_value = adc_to_display(adc_value);
        // speed = ((adc_value - 338) * 255) / 338; // Преобразуем в -255..255

        // Display to USART
        usart_transmit_string("ADC: ");
        usart_transmit_number(adc_value);
        usart_transmit_string("\r\n");

        // Display to 7-segment
        indicator_display_number(indicators, display_value);

        // motor_set_speed(&motor, speed);
        // indicator_display_number(speed / 16);

        // usart_transmit_string("Motor speed: ");
        // usart_transmit_number(speed);
        // usart_transmit_char('\n');
    }
}
