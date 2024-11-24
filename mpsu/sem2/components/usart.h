#ifndef USART_H
#define USART_H

#define F_CPU 16000000UL
#define BAUD 9600
#define UBRR F_CPU/16/BAUD-1

#include <stdint.h>

void usart_init(void);
void usart_transmit_char(char data);
void usart_transmit_string(const char *data);
void usart_transmit_number(int16_t number);

#endif