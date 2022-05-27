#include "Serial.h"

volatile uint8_t dataReceivedFlag, receivedByte[2], byteNum = 0;

void UARTE0_UART0_IRQHandler()
{
  NRF_UART0->EVENTS_RXDRDY = 0;

  receivedByte[byteNum] = NRF_UART0->RXD;
	byteNum++;  
  if(byteNum > 1)
  {
    byteNum = 0;
    dataReceivedFlag = 1;
  }
}  

void serialBegin(void)
{
  NRF_GPIO->PIN_CNF[TX_PIN] = 1 << GPIO_PIN_CNF_DIR_Pos;
  NRF_UART0->BAUDRATE = BAUDRATE_VALUE;
  NRF_UART0->PSELTXD = TX_PIN;   
  NRF_UART0->PSELRXD = RX_PIN;     
  NRF_UART0->INTENSET = 1 << RXDRDY;
  NVIC_EnableIRQ(UARTE0_UART0_IRQn);    
  NRF_UART0->ENABLE = UART_ENABLE_VALUE;     
  NRF_UART0->TASKS_STARTTX = TX_START;   
  NRF_UART0->TASKS_STARTRX = RX_START;     
}

void serialSendByte(char byte)
{
  NRF_UART0->TXD = byte;    
  while(!NRF_UART0->EVENTS_TXDRDY);
  NRF_UART0->EVENTS_TXDRDY = 0;
}

void serialPrintln(char *string)
{
	while(*string != '\0')
	{
		serialSendByte(*string);
		string++;
	} 
	serialSendByte('\n');    
}
