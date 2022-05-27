#include "device.h"
#include <stdio.h>

void deviceInit() 
{	        
    serialBegin();
    timerInit();
    adcInit();
    pwmInit();
    DS18B20Init();
    DS18B20ReadTemperature();
}

void deviceControl()
{           
    if(dataReceivedFlag)
    {
        dataReceivedFlag = 0;
        if(receivedByte[0] == '0')
        {
            pwmSeq[0] = (unsigned int)receivedByte[1] | POLARITY_MASK;
            NRF_PWM0->TASKS_SEQSTART[0] = 1;
        }
        else if(receivedByte[0] == '1')
        {
            pwmSeq[1] = (unsigned int)receivedByte[1] | POLARITY_MASK;
            NRF_PWM0->TASKS_SEQSTART[0] = 1;
        }
        else if(receivedByte[0] == '2')
        {
            pwmSeq[2] = (unsigned int)receivedByte[1] | POLARITY_MASK;
            NRF_PWM0->TASKS_SEQSTART[0] = 1;
        }         
    }                      

    if(temperatureFlag)
    {
        temperatureFlag = 0;
        NRF_TIMER2->INTENSET = 0;
        serialSendByte('t');        
        serialSendByte(temperatureSign);
        serialSendByte(temperatureTens + 48);
        serialSendByte(temperatureUnits + 48);
        serialSendByte(temperatureFraction + 48);
        NRF_TIMER2->INTENSET = (1 << TIMER_INTENSET_COMPARE0_Pos);
        DS18B20ReadTemperature();
    }    
}