/*
 * mIAI.c
 *
 *  Created on: Jun 26, 2025
 *      Author: lamdo
 */
#include "mIAI.h"
#include "FreeRTOS.h"
#include "task.h"
#include <cmsis_os.h>
#include "strings.h"
#include <stdio.h>
#include <string.h>
#include "mFunction.h"



bool isStopIAI = false;
uint8_t txIAIBuffer[2048]= {0};
uint8_t stepIAI = 0, iaiOnceTimes = 100;

bool IAI_Move(AXIS* axis, uint8_t target){
	axis->acknowledge.ACK_MOVE = false;
	axis->request.REQ_MOVE = false;
	while(HAL_GPIO_ReadPin(axis->driverInput.PEND.port, axis->driverInput.PEND.pin) && isStopIAI){
		vTaskDelay(pdMS_TO_TICKS(10));
	}
	if(!isStopIAI) return false;
	axis->position.targetPos.toPos = target;
	HAL_GPIO_WritePin(axis->driverOutput.PC1.port, 	axis->driverOutput.PC1.pin, 	(target & (1 << 0)) ? GPIO_PIN_SET : GPIO_PIN_RESET);
	HAL_GPIO_WritePin(axis->driverOutput.PC2.port, 	axis->driverOutput.PC2.pin, 	(target & (1 << 1)) ? GPIO_PIN_SET : GPIO_PIN_RESET);
	HAL_GPIO_WritePin(axis->driverOutput.PC4.port, 	axis->driverOutput.PC4.pin, 	(target & (1 << 2)) ? GPIO_PIN_SET : GPIO_PIN_RESET);
	HAL_GPIO_WritePin(axis->driverOutput.PC8.port, 	axis->driverOutput.PC8.pin, 	(target & (1 << 3)) ? GPIO_PIN_SET : GPIO_PIN_RESET);
	HAL_GPIO_WritePin(axis->driverOutput.PC16.port, axis->driverOutput.PC16.pin, 	(target & (1 << 4)) ? GPIO_PIN_SET : GPIO_PIN_RESET);
	HAL_GPIO_WritePin(axis->driverOutput.PC32.port, axis->driverOutput.PC32.pin, 	(target & (1 << 5)) ? GPIO_PIN_SET : GPIO_PIN_RESET);
	HAL_GPIO_WritePin(axis->driverOutput.PC64.port, axis->driverOutput.PC64.pin, 	(target & (1 << 6)) ? GPIO_PIN_SET : GPIO_PIN_RESET);
	HAL_GPIO_WritePin(axis->driverOutput.PC128.port,axis->driverOutput.PC128.pin, 	(target & (1 << 7)) ? GPIO_PIN_SET : GPIO_PIN_RESET);
	vTaskDelay(30);
	HAL_GPIO_WritePin(axis->driverOutput.CSTR.port, axis->driverOutput.CSTR.pin, GPIO_PIN_SET);
	while(!HAL_GPIO_ReadPin(axis->driverInput.PEND.port, axis->driverInput.PEND.pin) && isStopIAI){
		vTaskDelay(pdMS_TO_TICKS(3));
	}
	if(!isStopIAI) return false;
	vTaskDelay(pdMS_TO_TICKS(20));
	HAL_GPIO_WritePin(axis->driverOutput.CSTR.port, axis->driverOutput.CSTR.pin, GPIO_PIN_RESET);
	while(HAL_GPIO_ReadPin(axis->driverInput.PEND.port, axis->driverInput.PEND.pin) && isStopIAI){
		vTaskDelay(pdMS_TO_TICKS(3));
	}
	if(!isStopIAI) return false;
	vTaskDelay(pdMS_TO_TICKS(100));
//	axis->position.currentPos.PM1 	= HAL_GPIO_ReadPin(axis->driverInput.PM1.port,axis->driverInput.PM1.pin) == GPIO_PIN_RESET ? 1 : 0;
//	axis->position.currentPos.PM2 	= HAL_GPIO_ReadPin(axis->driverInput.PM2.port,axis->driverInput.PM2.pin) == GPIO_PIN_RESET ? 1 : 0;
//	axis->position.currentPos.PM4 	= HAL_GPIO_ReadPin(axis->driverInput.PM4.port,axis->driverInput.PM4.pin) == GPIO_PIN_RESET ? 1 : 0;
//	axis->position.currentPos.PM8 	= HAL_GPIO_ReadPin(axis->driverInput.PM8.port,axis->driverInput.PM8.pin) == GPIO_PIN_RESET ? 1 : 0;
//	axis->position.currentPos.PM16 	= HAL_GPIO_ReadPin(axis->driverInput.PM16.port,axis->driverInput.PM16.pin) == GPIO_PIN_RESET ? 1 : 0;
//	axis->position.currentPos.PM32 	= HAL_GPIO_ReadPin(axis->driverInput.PM32.port,axis->driverInput.PM32.pin) == GPIO_PIN_RESET ? 1 : 0;
//	axis->position.currentPos.PM64 	= HAL_GPIO_ReadPin(axis->driverInput.PM64.port,axis->driverInput.PM64.pin) == GPIO_PIN_RESET ? 1 : 0;
//	axis->position.currentPos.PM128 = HAL_GPIO_ReadPin(axis->driverInput.PM128.port,axis->driverInput.PM128.pin) == GPIO_PIN_RESET ? 1 : 0;
//	vTaskDelay(pdMS_TO_TICKS(20));
	if(axis->position.currentPos.nowPos != axis->position.targetPos.toPos)
		return false;
	axis->acknowledge.ACK_MOVE = true;
	return true;
}

bool IAI_Home(AXIS* axis){
	axis->acknowledge.ACK_ORG = false;
	axis->request.REQ_ORG = false;
	HAL_GPIO_WritePin(axis->driverOutput.HOME.port, axis->driverOutput.HOME.pin, GPIO_PIN_SET);
	while(!HAL_GPIO_ReadPin(axis->driverInput.HEND.port, axis->driverInput.HEND.pin) && isStopIAI){
		vTaskDelay(pdMS_TO_TICKS(10));
	}
	if(!isStopIAI) return false;
	vTaskDelay(pdMS_TO_TICKS(30));
	HAL_GPIO_WritePin(axis->driverOutput.HOME.port, axis->driverOutput.HOME.pin, GPIO_PIN_RESET);
	while(!HAL_GPIO_ReadPin(axis->driverInput.HEND.port, axis->driverInput.HEND.pin) && isStopIAI){
		vTaskDelay(pdMS_TO_TICKS(10));
	}
	if(!isStopIAI) return false;
	axis->acknowledge.ACK_ORG = true;
	return true;
}

bool IAI_Pause(AXIS* axis){
	HAL_GPIO_WritePin(axis->driverOutput.STP.port, axis->driverOutput.STP.pin, GPIO_PIN_SET);
	return true;
}

bool IAI_Continues(AXIS* axis){
	HAL_GPIO_WritePin(axis->driverOutput.STP.port, axis->driverOutput.STP.pin, GPIO_PIN_RESET);
	return true;
}

bool IAI_Stop(AXIS* axis){
	HAL_GPIO_WritePin(axis->driverOutput.SON.port, axis->driverOutput.SON.pin, GPIO_PIN_RESET);
	return true;
}

bool IAI_Prepare(AXIS* axis){
	axis->request.REQ_PREPARE = false;
	axis->acknowledge.ACK_PREPARE = false;
	HAL_GPIO_WritePin(axis->driverOutput.SON.port, axis->driverOutput.SON.pin, GPIO_PIN_SET);
	while(HAL_GPIO_ReadPin(axis->driverInput.SV.port, axis->driverInput.SV.pin) && isStopIAI){
		vTaskDelay(pdMS_TO_TICKS(3));
	}
	HAL_GPIO_WritePin(axis->driverOutput.STP.port, axis->driverOutput.STP.pin, GPIO_PIN_SET);
	if(!isStopIAI) return false;
	axis->acknowledge.ACK_PREPARE = true;
	return true;
}
bool IAI_Clear(AXIS* axis){
	HAL_GPIO_WritePin(axis->driverOutput.BKRL.port, axis->driverOutput.BKRL.pin, GPIO_PIN_RESET);
	HAL_GPIO_WritePin(axis->driverOutput.CSTR.port, axis->driverOutput.CSTR.pin, GPIO_PIN_RESET);
	HAL_GPIO_WritePin(axis->driverOutput.HOME.port, axis->driverOutput.HOME.pin, GPIO_PIN_RESET);
	HAL_GPIO_WritePin(axis->driverOutput.RES.port, axis->driverOutput.RES.pin, GPIO_PIN_RESET);
	HAL_GPIO_WritePin(axis->driverOutput.STP.port, axis->driverOutput.STP.pin, GPIO_PIN_RESET);
	vTaskDelay(pdMS_TO_TICKS(20));
	return true;
}

bool IAI_ClearError(AXIS* axis){
	axis->request.REQ_RESET = false;
	axis->acknowledge.ACK_RESET = false;
	HAL_GPIO_WritePin(axis->driverOutput.RES.port, axis->driverOutput.RES.pin, GPIO_PIN_SET);
	while(!HAL_GPIO_ReadPin(axis->driverInput.ALM.port, axis->driverInput.ALM.pin) && isStopIAI){
		vTaskDelay(pdMS_TO_TICKS(10));
	}
	if(!isStopIAI) return false;
	vTaskDelay(pdMS_TO_TICKS(30));
	HAL_GPIO_WritePin(axis->driverOutput.RES.port, axis->driverOutput.RES.pin, GPIO_PIN_RESET);
	axis->acknowledge.ACK_RESET = true;
	return true;
}

void IAIMovingHandled(){
	switch(stepIAI){
	case STEP_IAI_WAIT:{
		iaiOnceTimes = 0;
		break;
	}
	case STEP_IAI_PREPARE_OPERATION:{
		if(iaiOnceTimes != STEP_IAI_PREPARE_OPERATION){
			axisX.request.REQ_PREPARE = true;
			axisY.request.REQ_PREPARE = true;
			axisZ.request.REQ_PREPARE = true;
			iaiOnceTimes = STEP_IAI_PREPARE_OPERATION;
		}
		if(axisX.acknowledge.ACK_PREPARE && axisY.acknowledge.ACK_PREPARE && axisZ.acknowledge.ACK_PREPARE){
			snprintf((char*)txIAIBuffer,sizeof(txIAIBuffer),"ready\n");
			axisX.acknowledge.ACK_PREPARE = false;
			axisY.acknowledge.ACK_PREPARE = false;
			axisZ.acknowledge.ACK_PREPARE = false;
			stepIAI = STEP_IAI_WAIT;
		}
		break;
	}
	case STEP_IAI_MOVE:{
		if(iaiOnceTimes != STEP_IAI_MOVE){
			memset(txIAIBuffer,0,sizeof(txIAIBuffer));
			if(axisX.position.currentPos.nowPos != axisX.position.targetPos.toPos)
				axisX.request.REQ_MOVE = true;
			if(axisY.position.currentPos.nowPos != axisY.position.targetPos.toPos)
				axisY.request.REQ_MOVE = true;
			if(axisZ.position.currentPos.nowPos != axisZ.position.targetPos.toPos)
				axisZ.request.REQ_MOVE = true;
			iaiOnceTimes = STEP_IAI_MOVE;
		}
		if(axisX.position.currentPos.nowPos == axisX.position.targetPos.toPos &&
				axisY.position.currentPos.nowPos == axisY.position.targetPos.toPos &&
				axisZ.position.currentPos.nowPos == axisZ.position.targetPos.toPos){
			snprintf((char*)txIAIBuffer,sizeof(txIAIBuffer),
					"cmd:%03d,%03d,%03d,%03d,ok\n",
					axisX.position.currentPos.nowPos,
					axisY.position.currentPos.nowPos,
					axisZ.position.currentPos.nowPos,
					currentLightValue);
			stepIAI = STEP_IAI_WAIT;
		}
		break;
	}
	case STEP_IAI_ORG:{
		if(iaiOnceTimes != STEP_IAI_ORG){
			iaiOnceTimes = STEP_IAI_ORG;
			axisX.request.REQ_ORG = true;
			axisY.request.REQ_ORG = true;
			axisZ.request.REQ_ORG = true;
		}
		stepIAI = STEP_IAI_WAIT;
		break;
	}
	case STEP_IAI_PAUSE:{
		axisX.pause(&axisX);
		axisY.pause(&axisY);
		axisZ.pause(&axisZ);
		break;
	}
	case STEP_IAI_STOP:{
		axisX.stop(&axisX);
		axisY.stop(&axisY);
		axisZ.stop(&axisZ);
		break;
	}
	case STEP_IAI_RESET:{
		if(iaiOnceTimes != STEP_IAI_RESET){
			axisX.request.REQ_RESET = true;
			axisY.request.REQ_RESET = true;
			axisZ.request.REQ_RESET = true;
			iaiOnceTimes = STEP_IAI_RESET;
		}
		if(axisX.acknowledge.ACK_RESET && axisY.acknowledge.ACK_RESET && axisZ.acknowledge.ACK_RESET){
			axisX.acknowledge.ACK_RESET = false;
			axisY.acknowledge.ACK_RESET = false;
			axisZ.acknowledge.ACK_RESET = false;
			stepIAI = STEP_IAI_WAIT;
		}
		break;
	}
	default :break;
	}

}

AXIS axisX = {
		.position = {
				.targetPos 	= {{0}},
				.currentPos = {{0}},
		},
		.driverInput = {
				.PM1 	= {GPIOF, GPIO_PIN_6},
				.PM2 	= {GPIOF, GPIO_PIN_7},
				.PM4 	= {GPIOF, GPIO_PIN_8},
				.PM8 	= {GPIOF, GPIO_PIN_9},
				.PM16 	= {GPIOF, GPIO_PIN_10},
				.PM32 	= {GPIOC, GPIO_PIN_0},
				.PM64 	= {GPIOC, GPIO_PIN_1},
				.PM128 	= {GPIOC, GPIO_PIN_2},
				.HEND 	= {GPIOC, GPIO_PIN_3},
				.PEND 	= {GPIOA, GPIO_PIN_1},
				.SV 	= {GPIOH, GPIO_PIN_2},
				.ALM 	= {GPIOH, GPIO_PIN_3},
		},
		.driverOutput = {
				.PC1	= {GPIOE, GPIO_PIN_11},
				.PC2	= {GPIOE, GPIO_PIN_12},
				.PC4	= {GPIOE, GPIO_PIN_13},
				.PC8	= {GPIOE, GPIO_PIN_14},
				.PC16	= {GPIOE, GPIO_PIN_15},
				.PC32	= {GPIOB, GPIO_PIN_10},
				.PC64	= {GPIOB, GPIO_PIN_11},
				.PC128	= {GPIOH, GPIO_PIN_6},
				.BKRL	= {GPIOH, GPIO_PIN_7},
				.HOME	= {GPIOH, GPIO_PIN_8},
				.STP	= {GPIOH, GPIO_PIN_9},
				.CSTR	= {GPIOH, GPIO_PIN_10},
				.RES	= {GPIOH, GPIO_PIN_11},
				.SON	= {GPIOH, GPIO_PIN_12},
		},
		.request = {0},
		.acknowledge = {0},
		.move 	 	= IAI_Move,
		.home 	 	= IAI_Home,
		.pause 	 	= IAI_Pause,
		.continues 	= IAI_Continues,
		.stop 	 	= IAI_Stop,
		.prepare 	= IAI_Prepare,
		.clear 	 	= IAI_Clear,
		.clearError = IAI_ClearError,
};
AXIS axisY = {
		.position = {
				.targetPos 	= {{0}},
				.currentPos = {{0}},
		},
		.driverInput = {
				.PM1 	= {GPIOE, GPIO_PIN_6},
				.PM2 	= {GPIOI, GPIO_PIN_8},
				.PM4 	= {GPIOC, GPIO_PIN_13},
				.PM8 	= {GPIOI, GPIO_PIN_9},
				.PM16 	= {GPIOI, GPIO_PIN_10},
				.PM32 	= {GPIOI, GPIO_PIN_11},
				.PM64 	= {GPIOF, GPIO_PIN_0},
				.PM128 	= {GPIOF, GPIO_PIN_1},
				.HEND 	= {GPIOF, GPIO_PIN_2},
				.PEND 	= {GPIOF, GPIO_PIN_3},
				.SV 	= {GPIOF, GPIO_PIN_4},
				.ALM 	= {GPIOF, GPIO_PIN_5},
		},
		.driverOutput = {
				.PC1	= {GPIOB, GPIO_PIN_12},
				.PC2	= {GPIOB, GPIO_PIN_13},
				.PC4	= {GPIOB, GPIO_PIN_14},
				.PC8	= {GPIOB, GPIO_PIN_15},
				.PC16	= {GPIOD, GPIO_PIN_8},
				.PC32	= {GPIOD, GPIO_PIN_9},
				.PC64	= {GPIOD, GPIO_PIN_10},
				.PC128	= {GPIOD, GPIO_PIN_11},
				.BKRL	= {GPIOD, GPIO_PIN_12},
				.HOME	= {GPIOD, GPIO_PIN_13},
				.STP	= {GPIOD, GPIO_PIN_14},
				.CSTR	= {GPIOD, GPIO_PIN_15},
				.RES	= {GPIOG, GPIO_PIN_2},
				.SON	= {GPIOG, GPIO_PIN_3},
		},
		.request = {0},
		.acknowledge = {0},
		.move 	 	= IAI_Move,
		.home 	 	= IAI_Home,
		.pause 	 	= IAI_Pause,
		.continues 	= IAI_Continues,
		.stop 	 	= IAI_Stop,
		.prepare 	= IAI_Prepare,
		.clear 	 	= IAI_Clear,
		.clearError = IAI_ClearError,
};


AXIS axisZ = {
		.position={
				.targetPos 	= {{0}},
				.currentPos = {{0}},
		},
		.driverInput = {
				.PM1 	= {GPIOB, GPIO_PIN_8},
				.PM2 	= {GPIOB, GPIO_PIN_9},
				.PM4 	= {GPIOE, GPIO_PIN_0},
				.PM8 	= {GPIOE, GPIO_PIN_1},
				.PM16 	= {GPIOI, GPIO_PIN_4},
				.PM32 	= {GPIOI, GPIO_PIN_5},
				.PM64 	= {GPIOI, GPIO_PIN_6},
				.PM128 	= {GPIOI, GPIO_PIN_7},
				.HEND 	= {GPIOE, GPIO_PIN_2},
				.PEND 	= {GPIOE, GPIO_PIN_3},
				.SV 	= {GPIOE, GPIO_PIN_4},
				.ALM 	= {GPIOE, GPIO_PIN_5},
		},
		.driverOutput = {
				.PC1	= {GPIOA, GPIO_PIN_7},
				.PC2	= {GPIOB, GPIO_PIN_0},
				.PC4	= {GPIOB, GPIO_PIN_1},
				.PC8	= {GPIOF, GPIO_PIN_11},
				.PC16	= {GPIOF, GPIO_PIN_12},
				.PC32	= {GPIOF, GPIO_PIN_13},
				.PC64	= {GPIOF, GPIO_PIN_14},
				.PC128	= {GPIOF, GPIO_PIN_15},
				.BKRL	= {GPIOG, GPIO_PIN_0},
				.HOME	= {GPIOG, GPIO_PIN_1},
				.STP	= {GPIOE, GPIO_PIN_7},
				.CSTR	= {GPIOE, GPIO_PIN_8},
				.RES	= {GPIOE, GPIO_PIN_9},
				.SON	= {GPIOE, GPIO_PIN_10},
		},
		.request = {0},
		.acknowledge = {0},
		.move 	 	= IAI_Move,
		.home 	 	= IAI_Home,
		.pause 	 	= IAI_Pause,
		.continues 	= IAI_Continues,
		.stop 	 	= IAI_Stop,
		.prepare 	= IAI_Prepare,
		.clear 	 	= IAI_Clear,
		.clearError = IAI_ClearError,
};

