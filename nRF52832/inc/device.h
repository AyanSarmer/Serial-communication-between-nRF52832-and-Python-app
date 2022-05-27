#ifndef DEVICE_H_
#define DEVICE_H_

#include "PWM.h"
#include "Serial.h"
#include "adc.h"
#include "timer.h"
#include "DS18B20.h"

#define LED_IS_OFF              0
#define LED_IS_ON               1

void deviceInit();
void deviceControl();

#endif /* DEVICE_H_ */
