#ifndef INDICATOR_H
#define INDICATOR_H

#include "components.h"


typedef struct {
    uint8_t a_pin;
    uint8_t b_pin;
    uint8_t c_pin;
    uint8_t d_pin;
    PortMapping *port_mapping;
} Indicator;

extern uint8_t segment_map[10];

void indicator_init(Indicator *indicator, PortMapping *port_mapping, uint8_t a_pin, uint8_t b_pin, uint8_t c_pin, uint8_t d_pin);
void indicator_display_digit(Indicator *indicator, uint8_t digit);
void indicator_display_number(Indicator indicators[2], int16_t number);

#endif