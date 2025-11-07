/*
 * mFlow.c
 *
 *  Created on: Jun 26, 2025
 *      Author: lamdo
 */
#include "mFlow.h"
#include "FreeRTOS.h"
#include "task.h"
#include "mIAI.h"
#include "mVariable.h"
#include "mGPIO.h"
#include "mErrorHandle.h"

uint8_t machineMode = 0, stepORG = 0, stepRun = 0;
volatile bool isRun = false;


void eqControl() {

}

void eqModeORG() {


}

void eqModeMove() {
	//stepIAI = STEP_IAI_MOVE;
}

void eqModeAuto() {


}
