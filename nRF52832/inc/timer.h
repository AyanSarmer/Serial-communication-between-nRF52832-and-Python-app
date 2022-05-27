#ifndef TIMER_H_
#define TIMER_H_

#include "nrf.h"
#include "Serial.h"
#include "adc.h"

#define PSC_VALUE               5
#define CC_VALUE                50

void timerInit();

#endif /* TIMER_H_ */