/*
 * mFlow.h
 *
 *  Created on: Jun 26, 2025
 *      Author: lamdo
 */

#ifndef INC_MFLOW_H_
#define INC_MFLOW_H_
#include "mFunction.h"
#include "mGPIO.h"
#include "mRS232.h"
#include "mVariable.h"

typedef enum{
	EQ_MODE_INIT,
	EQ_MODE_WAIT,
	EQ_MODE_PREPARE,
	EQ_MODE_ORG,
	EQ_MODE_MOVE,
	EQ_MODE_AUTO
}EQ_MODE;

typedef enum{
	STEP_RUN_WAIT,
	STEP_RUN_INSERT_OBJECT,
	STEP_RUN_REQ,
	STEP_RUN_WAIT_ACK,
	STEP_RUN_RETURN,
}STEP_RUN;

void eqControl(void);
void eqModeORG(void);
void eqModeMove(void);
void eqModeAuto(void);

extern uint8_t machineMode, stepORG, stepRun;
extern volatile bool isRun;

#endif /* INC_MFLOW_H_ */
