#ifndef COMPONENTS_H
#define COMPONENTS_H

#include <avr/io.h>


#define SET_PIN_HIGH(PORT, PIN) ((PORT) |= (1 << (PIN)))
#define SET_PIN_LOW(PORT, PIN) ((PORT) &= ~(1 << (PIN)))

typedef struct {
    volatile uint8_t *port;
    volatile uint8_t *ddr;
} PortMapping;

extern PortMapping port_mappings[];

#endif