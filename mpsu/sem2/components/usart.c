#include <avr/io.h>
#include "usart.h"

void usart_init() {
    UBRR0H = (UBRR >> 8);
    UBRR0L = UBRR;
    UCSR0B = (1 << TXEN0);  // turn on transmitter
    UCSR0C = (1 << UCSZ01) | (1 << UCSZ00);  // 8-bit data format, 1 stop bit
}

void usart_transmit_char(char data) {
    while (!(UCSR0A & (1 << UDRE0))); // Wait for empty transmit buffer
    UDR0 = data;  // Put data into buffer, sends the data
}

void usart_transmit_string(const char *data) {
    while (*data) {
        usart_transmit_char(*data++);
    }
}

void usart_transmit_number(int16_t number) {
    char buffer[6]; // -32768..32767
    itoa(number, buffer, 10);
    usart_transmit_string(buffer);
}