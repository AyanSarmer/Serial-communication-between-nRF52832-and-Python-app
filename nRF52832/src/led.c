#include "led.h"

void ledInit()
{
    NRF_GPIO->PIN_CNF[LED] = 1 << GPIO_PIN_CNF_DIR_Pos;  
}

void ledOn()
{
    NRF_GPIO->OUTSET |= 1 << LED;
}

void ledOff()
{
    NRF_GPIO->OUTCLR |= 1 << LED;
}
