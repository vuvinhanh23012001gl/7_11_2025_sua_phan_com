/*
 * mErrorHandle.c
 *
 *  Created on: Jun 27, 2025
 *      Author: lamdo
 */

#include "mErrorHandle.h"
#include "FreeRTOS.h"
#include "task.h"
#include "mIAI.h"
#include "mGPIO.h"
#include "mFlow.h"

uint8_t machineStatus = 0;
uint8_t txErrorString[2048] = {0};
uint8_t onceTimesError = 0;

void eqStatusPause(){
	axisX.pause(&axisX);
	axisY.pause(&axisY);
	axisZ.pause(&axisZ);
	machineOutputs.lightYellow = true;
	machineOutputs.buzzer = !machineOutputs.buzzer;
	vTaskDelay(pdMS_TO_TICKS(500));
}

void eqStatusStop(){
	machineOutputs.buzzer = true;
	machineOutputs.lightRed = true;
	machineOutputs.buzzer = !machineOutputs.buzzer;
	vTaskDelay(pdMS_TO_TICKS(500));
}

void eqStatusNormal(){

}

void eqStatusErrorHandle(){

}

void eqStatusMonitor(){
	static uint8_t last_stop = 0;
	if(!machineInputs.btnStop){
		machineStatus = MACHINE_STOP;
		snprintf((char*) txErrorString, sizeof(txErrorString),"log:PAUSE:PRESSStop\n");
		last_stop =  1;
	}
	else if(HAL_GPIO_ReadPin(axisX.driverInput.ALM.port, axisX.driverInput.ALM.pin)){
		machineStatus = MACHINE_ERROR;
		snprintf((char*)txErrorString,sizeof(txErrorString),"log:ERROX\r\n");
	} else if(HAL_GPIO_ReadPin(axisY.driverInput.ALM.port, axisY.driverInput.ALM.pin)){
		machineStatus = MACHINE_ERROR;
		snprintf((char*)txErrorString,sizeof(txErrorString),"log:ERROY\r\n");
	}else if (HAL_GPIO_ReadPin(axisZ.driverInput.ALM.port, axisZ.driverInput.ALM.pin)){
		machineStatus = MACHINE_ERROR;
		snprintf((char*)txErrorString, sizeof(txErrorString),"log:ERROZ\r\n");
	}else if(!machineInputs.swDoor && machineMode == EQ_MODE_AUTO && stepRun > STEP_RUN_INSERT_OBJECT){
		machineStatus = MACHINE_PAUSE;
		snprintf((char*)txErrorString,sizeof(txErrorString),"log:PAUSED:OPENDoor\r\n");
	}else if((!machineInputs.sensorSafety && machineMode == EQ_MODE_AUTO && stepRun > STEP_RUN_INSERT_OBJECT)
			&& !isRun){
		machineStatus = MACHINE_PAUSE;
		snprintf((char*)txErrorString, sizeof(txErrorString),"log:PAUSED:TOUCHSafety\r\n");
	}
	if(machineInputs.btnStop && last_stop){
		snprintf((char*)txErrorString, sizeof(txErrorString),"log:RELEASE_STOP\r\n");
		last_stop = 0;
	}
}
void eqHandleStatus(){
	eqStatusMonitor();
	switch(machineStatus){
	case MACHINE_RUN:{
		if(onceTimesError != EQ_STATUS_RUN){
			machineOutputs.lightYellow = false;
			machineOutputs.buzzer = false;
			machineOutputs.lightRed = false;
			onceTimesError = EQ_STATUS_RUN;
		}
		break;
	}
	case MACHINE_PAUSE:{
		onceTimesError = EQ_STATUS_PAUSED;
		if(machineInputs.swDoor && machineInputs.sensorSafety){
			machineStatus = machineStatus == EQ_STATUS_PAUSED ? EQ_STATUS_RUN : machineStatus;
			HAL_GPIO_WritePin(axisX.driverOutput.STP.port, axisX.driverOutput.STP.pin, GPIO_PIN_SET);
			HAL_GPIO_WritePin(axisY.driverOutput.STP.port, axisY.driverOutput.STP.pin, GPIO_PIN_SET);
			HAL_GPIO_WritePin(axisZ.driverOutput.STP.port, axisZ.driverOutput.STP.pin, GPIO_PIN_SET);
			machineOutputs.lightYellow = false;
			machineOutputs.buzzer = false;
		}
		else{
			HAL_GPIO_WritePin(axisX.driverOutput.STP.port, axisX.driverOutput.STP.pin, GPIO_PIN_RESET);
			HAL_GPIO_WritePin(axisY.driverOutput.STP.port, axisY.driverOutput.STP.pin, GPIO_PIN_RESET);
			HAL_GPIO_WritePin(axisZ.driverOutput.STP.port, axisZ.driverOutput.STP.pin, GPIO_PIN_RESET);
			machineOutputs.lightYellow = !machineOutputs.lightYellow;
			machineOutputs.buzzer = !machineOutputs.buzzer;
			vTaskDelay(pdMS_TO_TICKS(100));
		}
		break;
	}
	case MACHINE_ERROR:{
		onceTimesError = EQ_STATUS_ERROR;
		if(machineInputs.btnReset){
			HAL_GPIO_WritePin(axisX.driverOutput.RES.port, axisX.driverOutput.RES.pin, GPIO_PIN_SET);
			HAL_GPIO_WritePin(axisY.driverOutput.RES.port, axisY.driverOutput.RES.pin, GPIO_PIN_SET);
			HAL_GPIO_WritePin(axisZ.driverOutput.RES.port, axisZ.driverOutput.RES.pin, GPIO_PIN_SET);
			vTaskDelay(pdMS_TO_TICKS(50));
			HAL_GPIO_WritePin(axisX.driverOutput.RES.port, axisX.driverOutput.RES.pin, GPIO_PIN_RESET);
			HAL_GPIO_WritePin(axisY.driverOutput.RES.port, axisY.driverOutput.RES.pin, GPIO_PIN_RESET);
			HAL_GPIO_WritePin(axisZ.driverOutput.RES.port, axisZ.driverOutput.RES.pin, GPIO_PIN_RESET);
			HAL_GPIO_WritePin(axisX.driverOutput.STP.port, axisX.driverOutput.STP.pin, GPIO_PIN_SET);
			HAL_GPIO_WritePin(axisY.driverOutput.STP.port, axisY.driverOutput.STP.pin, GPIO_PIN_SET);
			HAL_GPIO_WritePin(axisZ.driverOutput.STP.port, axisZ.driverOutput.STP.pin, GPIO_PIN_SET);
			machineOutputs.lightYellow = false;
			machineOutputs.buzzer = false;
			machineStatus = EQ_STATUS_RUN;
		}else{
			machineOutputs.lightYellow = !machineOutputs.lightYellow;
			machineOutputs.buzzer = !machineOutputs.buzzer;
			vTaskDelay(pdMS_TO_TICKS(200));
		}
		break;
	}
	case MACHINE_STOP:{
		//HAL_GPIO_WritePin(axisX.driverOutput.SON.port, axisX.driverOutput.SON.pin, GPIO_PIN_RESET);
		//HAL_GPIO_WritePin(axisY.driverOutput.SON.port, axisY.driverOutput.SON.pin, GPIO_PIN_RESET);
		//HAL_GPIO_WritePin(axisZ.driverOutput.SON.port, axisZ.driverOutput.SON.pin, GPIO_PIN_RESET);
		machineOutputs.buzzer = true;
		machineOutputs.lightRed = true;
		if(machineInputs.btnStop){
			machineOutputs.buzzer = false;
			machineOutputs.lightRed = false;
			if(machineInputs.btnReset){
				snprintf((char*)txErrorString, sizeof(txErrorString),"log:PRESS_RESET_STOP\r\n");
				machineMode = EQ_MODE_WAIT;
				machineStatus = EQ_STATUS_RUN;
				machineOutputs.lightYellow = false;

			}else{
				machineOutputs.lightYellow = !machineOutputs.lightYellow;
				vTaskDelay(pdMS_TO_TICKS(300));
			}
		}

		break;
	}
	default : break;
	}
}
