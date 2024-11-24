#include <avr/io.h>
#include <util/delay.h>

#include "components.h"
#include "indicator.h"


uint8_t segment_map[10] = {
    0b0000,  // 0
    0b0001,  // 1
    0b0010,  // 2
    0b0011,  // 3
    0b0100,  // 4
    0b0101,  // 5
    0b0110,  // 6
    0b0111,  // 7
    0b1000,  // 8
    0b1001,  // 9
};

void indicator_init(
    Indicator *indicator,
    PortMapping *port_mapping,
    uint8_t a_pin,
    uint8_t b_pin,
    uint8_t c_pin,
    uint8_t d_pin
    ) {
    indicator->a_pin = a_pin;
    indicator->b_pin = b_pin;
    indicator->c_pin = c_pin;
    indicator->d_pin = d_pin;
    indicator->port_mapping = port_mapping;

    *(port_mapping->ddr) |= (1 << indicator->a_pin)
        | (1 << indicator->b_pin)
        | (1 << indicator->c_pin)
        | (1 << indicator->d_pin);
}

void indicator_display_digit(Indicator *indicator, uint8_t digit) {
    uint8_t display_digit = segment_map[digit];

    for (uint8_t i = 0; i < 4; i++) {
        if (display_digit & (1 << i)) {
            SET_PIN_HIGH(*(indicator->port_mapping->port), indicator->a_pin + i);
        } else {
            SET_PIN_LOW(*(indicator->port_mapping->port), indicator->a_pin + i);
        }
    }
}

void indicator_display_number(Indicator indicators[2], int16_t number) {
    indicator_display_digit(&indicators[0], abs(number) / 10);
    indicator_display_digit(&indicators[1], abs(number) % 10);
    _delay_ms(10);
}