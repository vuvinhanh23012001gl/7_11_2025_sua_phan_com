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
	 if(HAL_GPIO_ReadPin(axisX.driverInput.ALM.port, axisX.driverInput.ALM.pin)){
		snprintf((char*)txErrorString,sizeof(txErrorString),"erro:x\r\n");
	} else if(HAL_GPIO_ReadPin(axisY.driverInput.ALM.port, axisY.driverInput.ALM.pin)){
		machineStatus = MACHINE_ERROR;
		snprintf((char*)txErrorString,sizeof(txErrorString),"erro:y\r\n");
	}else if (HAL_GPIO_ReadPin(axisZ.driverInput.ALM.port, axisZ.driverInput.ALM.pin)){
		machineStatus = MACHINE_ERROR;
		snprintf((char*)txErrorString, sizeof(txErrorString),"erro:z\r\n");
	}
}
void eqHandleStatus(){
	eqStatusMonitor();

}
