#include <avr/io.h>

#include "components.h"


PortMapping port_mappings[] = {
    {&PORTB, &DDRB},  // 0
    {&PORTC, &DDRC},  // 1
    {&PORTD, &DDRD},  // 2
};