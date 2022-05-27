#include "adc.h"

unsigned int adcValue;

void adcInit(void)
{
    NRF_SAADC->CH[0].PSELP |= (SAADC_CH_PSELP_PSELP_AnalogInput0 << SAADC_CH_PSELP_PSELP_Pos);
    NRF_SAADC->CH[0].PSELN = (SAADC_CH_PSELN_PSELN_NC << SAADC_CH_PSELN_PSELN_Pos);
    NRF_SAADC->CH[0].CONFIG	= (SAADC_CH_CONFIG_GAIN_Gain1_4 << SAADC_CH_CONFIG_GAIN_Pos) 
                            | (SAADC_CH_CONFIG_REFSEL_VDD1_4 << SAADC_CH_CONFIG_REFSEL_Pos)
                            | (SAADC_CH_CONFIG_TACQ_3us << SAADC_CH_CONFIG_TACQ_Pos)		
                            | (SAADC_CH_CONFIG_MODE_SE << SAADC_CH_CONFIG_MODE_Pos)	
                            | (SAADC_CH_CONFIG_BURST_Enabled << SAADC_CH_CONFIG_BURST_Pos);                             
    NRF_SAADC->RESOLUTION = (SAADC_RESOLUTION_VAL_8bit << SAADC_RESOLUTION_VAL_Pos);                                
    NRF_SAADC->OVERSAMPLE |= (SAADC_OVERSAMPLE_OVERSAMPLE_Over2x << SAADC_OVERSAMPLE_OVERSAMPLE_Pos);                            
    NRF_SAADC->SAMPLERATE |= (SAADC_SAMPLERATE_MODE_Timers << SAADC_SAMPLERATE_MODE_Pos) | (SAMPLERATE_CC_VALUE << SAADC_SAMPLERATE_CC_Pos);    
    NRF_SAADC->RESULT.MAXCNT = 1;                
    NRF_SAADC->RESULT.PTR = (uint32_t)&adcValue;
    NRF_SAADC->ENABLE = SAADC_ENABLE_ENABLE_Enabled << SAADC_ENABLE_ENABLE_Pos;
    adcCalibrate();     
}

void adcStartConversion(void)
{             
    NRF_SAADC->TASKS_START = 1; 
    while(!NRF_SAADC->EVENTS_STARTED);
	NRF_SAADC->EVENTS_STARTED = 0;                   
    NRF_SAADC->TASKS_SAMPLE = 1;
    while(!NRF_SAADC->EVENTS_RESULTDONE);
    NRF_SAADC->EVENTS_RESULTDONE = 0;
}    

void adcCalibrate(void)
{
    NRF_SAADC->TASKS_CALIBRATEOFFSET = 1;
    while (!NRF_SAADC->EVENTS_CALIBRATEDONE);
    NRF_SAADC->EVENTS_CALIBRATEDONE = 0;   
}