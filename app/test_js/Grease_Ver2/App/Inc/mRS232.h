/*
 * mRS232.h
 *
 *  Created on: Jun 27, 2025
 *      Author: lamdo
 */

#ifndef INC_MRS232_H_
#define INC_MRS232_H_
#include "main.h"
#include "usbd_cdc_if.h"
#include "mVariable.h"

extern uint8_t UserRxBufferFS[APP_RX_DATA_SIZE];
extern bool isLineReceived;
extern uint8_t CDC_Transmit_FS(uint8_t* Buf, uint16_t Len);

void getCmdHandle(void);
void sendCmdHandle(void);
void processCommand(const char *input);
#endif /* INC_MRS232_H_ */
