#ifndef _UART_H_
#define _UART_H_

#include "nrf.h"

#define TX_PIN              26 
#define RX_PIN              27
#define UART_ENABLE_VALUE   4
#define BAUDRATE_VALUE      0x00275000  
#define TX_START            1
#define TX_STOP             1
#define RX_START            1
#define RX_STOP             1
#define RXDRDY              2

void serialBegin(void);
void serialSendByte(char byte);
void serialPrintln(char *string);

extern volatile uint8_t dataReceivedFlag, receivedByte[2], byteNum;

#endif /* _UART_H_ */
