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
	switch (machineMode) {
	case EQ_MODE_INIT: {
		machineOutputs.lightBlue = true;
		stepIAI = STEP_IAI_PREPARE_OPERATION;
		machineMode = EQ_MODE_WAIT;
		break;
	}
	case EQ_MODE_WAIT: {
		zz
			machineMode = EQ_MODE_ORG;
			stepORG = 0;
			machineOutputs.lightBtnReset = true;
			machineOutputs.lightYellow = false;
			machineOutputs.lightBtnStart = true;
		}else{
			machineOutputs.lightBtnStart = !machineOutputs.lightBtnStart;
			vTaskDelay(pdMS_TO_TICKS(300));
		}
		break;
//		machineOutputs.lightBtnReset = !machineOutputs.lightBtnReset;
//		machineOutputs.lightYellow = !machineOutputs.lightYellow;
//		vTaskDelay(pdMS_TO_TICKS(500));
//		if (machineInputs.btnReset && stepIAI == STEP_IAI_WAIT) {
//			machineMode = EQ_MODE_ORG;
//			stepORG = 0;
//			machineOutputs.lightBtnReset = true;
//			machineOutputs.lightYellow = false;
//			break;
//		}
//		break;
	}
	case EQ_MODE_PREPARE: {

		break;
	}
	case EQ_MODE_ORG: {
		eqModeORG();
		break;
	}
	case EQ_MODE_MOVE: {
		eqModeMove();
		break;
	}
	case EQ_MODE_AUTO: {
		if(machineStatus == MACHINE_RUN)
			eqModeAuto();
		break;
	}
	default:
		break;
	}
}

void eqModeORG() {
	switch(stepORG){
	case 0 :{
		stepIAI = STEP_IAI_ORG;
		stepORG = 1;
		machineOutputs.lightBlue = true;
		break;
	}
	case 1:{
		if(axisX.acknowledge.ACK_ORG && axisY.acknowledge.ACK_ORG && axisZ.acknowledge.ACK_ORG){
			axisX.acknowledge.ACK_ORG = false;
			axisY.acknowledge.ACK_ORG = false;
			axisZ.acknowledge.ACK_ORG = false;
			stepORG = 2;
		}
		break;
	}
	case 2:{
		if(machineInputs.sensorObjectLeft || machineInputs.sensorObjectRight){
			snprintf((char*)txBuffer,sizeof(txBuffer),"log:take_product_old\r\n");
			machineOutputs.lightYellow = !machineOutputs.lightYellow;
			vTaskDelay(pdMS_TO_TICKS(300));
		}else{

			machineOutputs.lightYellow = false;
			stepORG = 3;
			snprintf((char*)txBuffer,sizeof(txBuffer),"log:put_new_product\r\n");
		}
		break;
	}
	case 3:{
		//snprintf((char*)txBuffer,sizeof(txBuffer),"ready\n");
		machineMode = EQ_MODE_AUTO;
		stepRun = STEP_RUN_WAIT;
		machineOutputs.lightBtnStart = false;
		machineOutputs.lightBtnReset = false;
		snprintf((char*)txBuffer,sizeof(txBuffer),"log:went_org\r\n");
		stepORG = 1;
		break;
	}
	default : break;
	}
}

void eqModeMove() {
	//stepIAI = STEP_IAI_MOVE;
}

void eqModeAuto() {
	switch(stepRun){
	case STEP_RUN_WAIT:{
		if(machineInputs.sensorObjectLeft && machineInputs.sensorObjectRight){
			stepRun = STEP_RUN_INSERT_OBJECT;
			isRun = true;
		}
		break;
	}
	case STEP_RUN_INSERT_OBJECT:{
		if(machineInputs.sensorObjectLeft && machineInputs.sensorObjectRight)
		{
			if(machineInputs.sensorSafety){
				stepRun = STEP_RUN_REQ;
			}
		}else{
			stepRun = STEP_RUN_WAIT;
		}
		break;
	}
	case STEP_RUN_REQ:{
		if(txBuffer[0] == 0){
			snprintf((char*)txBuffer,sizeof(txBuffer),"ready\n");
			stepRun = STEP_RUN_WAIT_ACK;

		}
		break;
	}
	case STEP_RUN_WAIT_ACK:{
		if(!machineInputs.sensorObjectLeft && !machineInputs.sensorObjectRight){
			stepRun = STEP_RUN_WAIT;
			break;
		}
		if(axisX.position.currentPos.nowPos == 0 && axisY.position.currentPos.nowPos == 0 && isRun){
			snprintf((char*)txBuffer,sizeof(txBuffer),"ready\n");
			machineOutputs.lightBlue = !machineOutputs.lightBlue;
			vTaskDelay(pdMS_TO_TICKS(500));
		}else{
			isRun = false;
			machineOutputs.lightBlue = true;
		}
		if(axisX.position.currentPos.nowPos == 0 && axisY.position.currentPos.nowPos == 0 && !isRun){
			stepRun = STEP_RUN_RETURN;
			isRun = true;
		}

		break;
	}
	case STEP_RUN_RETURN:{
		if(!machineInputs.sensorObjectLeft && !machineInputs.sensorObjectRight && machineInputs.sensorSafety){
			stepRun = STEP_RUN_WAIT;
			machineOutputs.lightBlue = true;

		}else{
			machineOutputs.lightBlue = !machineOutputs.lightBlue;
			vTaskDelay(pdMS_TO_TICKS(300));
		}
		break;
	}
	default : break;
	}

}
