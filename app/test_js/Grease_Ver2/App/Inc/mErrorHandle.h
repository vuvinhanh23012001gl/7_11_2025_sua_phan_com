/*
 * mErrorHandle.h
 *
 *  Created on: Jun 27, 2025
 *      Author: lamdo
 */

#ifndef INC_MERRORHANDLE_H_
#define INC_MERRORHANDLE_H_
#include "mGPIO.h"
#include "mVariable.h"

typedef enum{
	EQ_STATUS_RUN,
	EQ_STATUS_PAUSED,
	EQ_STATUS_ERROR,
	EQ_STATUS_STOP,
}EQ_STATUS;

void eqStatusPause(void);
void eqStatusStop(void);
void eqStatusNormal(void);
void eqStatusErrorHandle(void);
void eqStatusMonitor(void);
void eqHandleStatus(void);

extern uint8_t machineStatus;
extern uint8_t txErrorString[2048];
extern uint8_t onceTimesError;


#endif /* INC_MERRORHANDLE_H_ */
