#include <avr/io.h>
#include <util/delay.h>
#include <stdlib.h>


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

#define SET_PIN_HIGH(PORT, PIN) ((PORT) |= (1 << (PIN)))
#define SET_PIN_LOW(PORT, PIN) ((PORT) &= ~(1 << (PIN)))

#define ADC_MIN 0
#define ADC_MAX 676
#define ADC_MAX_DISPLAY 15

#define F_CPU 16000000UL
#define BAUD 9600
#define UBRR F_CPU/16/BAUD-1


typedef struct {
    volatile uint8_t *port;
    volatile uint8_t *ddr;
} PortMapping;

typedef struct {
    uint8_t a_pin;
    uint8_t b_pin;
    uint8_t c_pin;
    uint8_t d_pin;
    PortMapping *port_mapping;
} Indicator;

typedef struct {
    uint8_t in1_pin;
    uint8_t in2_pin;
    uint8_t en_pin;
    PortMapping *in_port_mapping;
    PortMapping *en_port_mapping;
} Motor;

PortMapping port_mappings[] = {
    {&PORTB, &DDRB},  // 0
    {&PORTC, &DDRC},  // 1
    {&PORTD, &DDRD},  // 2
};

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

void motor_init(
    Motor *motor,
    uint8_t in1_port,
    uint8_t in2_port,
    uint8_t en_port,
    PortMapping *in_port_mapping,
    PortMapping *en_port_mapping
) {
    motor->in1_pin = in1_port;
    motor->in2_pin = in2_port;
    motor->en_pin = en_port;
    motor->in_port_mapping = in_port_mapping;
    motor->en_port_mapping = en_port_mapping;

    pinMode(10, OUTPUT);  // in1
    pinMode(11, OUTPUT);  // in2
    pinMode(0, OUTPUT);  // en1

    digitalWrite(10, LOW);  // in1
    digitalWrite(11, LOW);  // in2
    digitalWrite(0, LOW);  // en1
}

void motor_stop(Motor *motor) {
    // usart_transmit_string("Motor STOP\r\n");

    digitalWrite(10, LOW);  // in1
    digitalWrite(11, LOW);  // in2
    digitalWrite(0, LOW);  // en1

    // SET_PIN_LOW(*(motor->in_port_mapping->port), motor->in1_pin);
    // SET_PIN_LOW(*(motor->in_port_mapping->port), motor->in2_pin);
    // SET_PIN_HIGH(*(motor->en_port_mapping->port), motor->en_pin);
}

void motor_forward(Motor *motor, uint8_t speed) {
    // usart_transmit_string("Motor FORWARD\r\n");
    // usart_transmit_number(speed);

    analogWrite(10, speed);  // in1
    digitalWrite(11, LOW);  // in2
    digitalWrite(0, HIGH);  // en1

    // SET_PIN_HIGH(*(motor->in_port_mapping->port), motor->in1_pin);
    // SET_PIN_LOW(*(motor->in_port_mapping->port), motor->in2_pin);
    // SET_PIN_HIGH(*(motor->en_port_mapping->port), motor->en_pin);
}

void motor_backward(Motor *motor, uint8_t speed) {
    // usart_transmit_string("Motor BACKWARD\r\n");
    // usart_transmit_number(speed);

    digitalWrite(10, LOW);  // in1
    analogWrite(11, abs(speed));  // in2
    digitalWrite(0, HIGH);  // en1

    // SET_PIN_LOW(*(motor->in_port_mapping->port), motor->in1_pin);
    // SET_PIN_HIGH(*(motor->in_port_mapping->port), motor->in2_pin);
    // SET_PIN_HIGH(*(motor->en_port_mapping->port), motor->en_pin);
}

void motor_set_speed(Motor *motor, int16_t speed) {
    if (speed == 0) {
        motor_stop(motor);
    } else if (speed > 0) {
        motor_forward(motor, (uint8_t)speed);
    } else {
        motor_backward(motor, (uint8_t)(-speed));
    }
}


Indicator indicators[2];
Motor motor;
int32_t adc_value, display_value, speed;


void setup() {
    usart_init();
    usart_transmit_string("Hello, proteus!\r\n");
    
    indicator_init(&indicators[0], &port_mappings[2], SEG1_A_PIN, SEG1_B_PIN, SEG1_C_PIN, SEG1_D_PIN);
    indicator_init(&indicators[1], &port_mappings[1], SEG2_A_PIN, SEG2_B_PIN, SEG2_C_PIN, SEG2_D_PIN);

    adc_init();

    motor_init(&motor, MOT_IN1_PIN, MOT_IN2_PIN, MOT_EN_PIN, &port_mappings[0], &port_mappings[2]);
}

void loop() {
    adc_value = adc_read(0);
    display_value = adc_to_display(adc_value);
    speed = ((adc_value - 338) * 255) / 338; // Преобразуем в -255..255

    // Display to USART
    usart_transmit_string("ADC: ");
    usart_transmit_number(adc_value);
    usart_transmit_string("\r\n");

    indicator_display_number(indicators, display_value);

    motor_set_speed(&motor, speed);

    usart_transmit_string("Motor speed: ");
    usart_transmit_number(speed);
    usart_transmit_string("\r\n");

    _delay_ms(100);
}
