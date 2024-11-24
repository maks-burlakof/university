#ifndef MOTOR_H
#define MOTOR_H

#include <stdint.h>


typedef struct {
    uint8_t in1_pin;
    uint8_t in2_pin;
    uint8_t en_pin;
} Motor;

void motor_init(Motor *motor, uint8_t in1, uint8_t in2, uint8_t en);
void motor_stop(Motor *motor);
void motor_forward(Motor *motor, uint8_t speed);
void motor_backward(Motor *motor, uint8_t speed);
void motor_set_speed(Motor *motor, int16_t speed);

#endif