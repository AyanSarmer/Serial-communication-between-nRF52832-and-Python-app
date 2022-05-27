#ifndef PWM_H_
#define PWM_H_

#include "nrf.h"

#define PSEL_OUT_0_PIN          31
#define PSEL_OUT_1_PIN          30
#define PSEL_OUT_2_PIN          29

#define POLARITY_BIT            15
#define POLARITY_MASK           (1 << POLARITY_BIT)

#define PWM_CH0_DUTY            0
#define PWM_CH1_DUTY            0
#define PWM_CH2_DUTY            0

#define PWM_SEQ_0               PWM_CH0_DUTY | POLARITY_MASK
#define PWM_SEQ_1               PWM_CH1_DUTY | POLARITY_MASK
#define PWM_SEQ_2               PWM_CH2_DUTY | POLARITY_MASK

#define COUNTERTOP_VALUE        255

void pwmInit();

extern uint16_t pwmSeq[3];

#endif /* PWM_H_ */