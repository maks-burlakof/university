#include <avr/io.h>

#include "motor.h"


void motor_init(Motor *motor, uint8_t in1, uint8_t in2, uint8_t en) {
    motor->in1_pin = in1;
    motor->in2_pin = in2;
    motor->en_pin = en;

    DDRB |= (1 << motor->in1_pin) | (1 << motor->in2_pin);
    DDRD |= (1 << motor->en_pin);
}

void motor_stop(Motor *motor) {
    // IN1, IN2 = LOW
    PORTB &= ~((1 << motor->in1_pin) | (1 << motor->in2_pin));

    OCR0A = 0; // Останавливаем ШИМ
}

void motor_forward(Motor *motor, uint8_t speed) {
    // IN1 = HIGH, IN2 = LOW
    PORTB |= (1 << motor->in1_pin);
    PORTB &= ~(1 << motor->in2_pin);

    OCR0A = speed; // Устанавливаем ШИМ
}

void motor_backward(Motor *motor, uint8_t speed) {
    // IN1 = LOW, IN2 = HIGH
    PORTB &= ~(1 << motor->in1_pin);
    PORTB |= (1 << motor->in2_pin);

    OCR0A = -speed; // Устанавливаем ШИМ
}

void motor_set_speed(Motor *motor, int16_t speed) {
    if (speed == 0) {
        motor_stop(&motor);
    } else if (speed > 0) {
        motor_forward(&motor, (uint8_t)speed);
    } else {
        motor_backward(&motor, (uint8_t)(-speed));
    }
}