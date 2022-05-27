#ifndef _DS18B20_H_
#define _DS18B20_H_

#include "OneWire.h"

#define SKIP_ROM            0xCC
#define READ_SCRATCH_PAD    0xBE
#define CONVERT_T           0x44

#define CONVERT_DELAY       750 

#define MINUS               '1'
#define PLUS                '0'

void DS18B20Init(void);
void DS18B20ReadTemperature(void);

extern unsigned char temperatureSign, temperatureTens, temperatureUnits, temperatureFraction, temperatureFlag;
extern float temperature;

#endif /* _DS18B20_H_ */
