#ifndef ADC_H_
#define ADC_H_

#include "nrf.h"

#define SAMPLERATE_CC_VALUE             1

void adcInit(void);
void adcStartConversion(void);
void adcCalibrate(void);

extern unsigned int adcValue;

#endif /* ADC_H_ */