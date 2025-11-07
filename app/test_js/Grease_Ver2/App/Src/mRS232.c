/*
 * mRS232.c
 *
 *  Created on: Jun 26, 2025
 *      Author: lamdo
 */
#include "mRS232.h"
#include "mIAI.h"
#include "mFlow.h"
#include "mFunction.h"
#include "mErrorHandle.h"
#include "usbd_cdc_if.h"
#include "FreeRTOS.h"
#include "task.h"
#include <string.h>
#include "main.h"
#include "mVariable.h"
#include "stdlib.h"
#include "stdio.h"
#include "string.h"
#include "mGPIO.h"
void getCmdHandle() {
	if (UserRxBufferFS[0] != 'c' && UserRxBufferFS[0] != '2' && UserRxBufferFS[0] != 'r' && UserRxBufferFS[0] != 'l' &&  UserRxBufferFS[0] != 'b'
			&&  UserRxBufferFS[0] != 'p'&&  UserRxBufferFS[0] != 'r'	&&  UserRxBufferFS[0] != 's'  &&  UserRxBufferFS[0] != 'b' &&  UserRxBufferFS[0] != 'm') {
		memset(UserRxBufferFS, 0, sizeof(UserRxBufferFS));
		return;
	}
	memcpy(rxBuffer, UserRxBufferFS, sizeof(UserRxBufferFS));
	memset(UserRxBufferFS, 0, sizeof(UserRxBufferFS));
	processCommand((char *)rxBuffer);

	char* cmd = strtok((char*)rxBuffer, ":");
	char* args = strtok(NULL, "\n");


	if (cmd && strcmp(cmd, "cmd") == 0 && args) {
		int xPos = 0, yPos = 0, zPos = 0, lightValue = 0;
		if (sscanf(args, "%d,%d,%d,%d", &xPos, &yPos, &zPos, &lightValue) == 4) {
			axisX.position.targetPos.toPos = (uint8_t)xPos;
			axisY.position.targetPos.toPos = (uint8_t)yPos;
			axisZ.position.targetPos.toPos = (uint8_t)zPos;
			targetLightValue = lightValue <= 100 ? lightValue : 15;
			stepIAI = STEP_IAI_MOVE;

//			char ok[] = "-> cmd ok\n";
//			CDC_Transmit_FS((uint8_t*)ok, strlen(ok));
//			vTaskDelay(pdMS_TO_TICKS(20));
		} else {
			char err[] = "log:-> cmd invalid format\n";
			CDC_Transmit_FS((uint8_t*)err, strlen(err));
			vTaskDelay(pdMS_TO_TICKS(20));
		}
	} else if (cmd && strcmp(cmd, "200OK") == 0) {
		uint8_t response[128] = {0};
		snprintf((char*)response, sizeof(response),
			"200OK,%03d,%03d,%03d,%03d\n",
			axisX.position.currentPos.nowPos, axisY.position.currentPos.nowPos,
			axisZ.position.currentPos.nowPos, currentLightValue);
		CDC_Transmit_FS(response, strlen((char*)response));
		vTaskDelay(pdMS_TO_TICKS(30));
	}else if(cmd && strcmp(cmd,"return") == 0){
		stepRun = STEP_RUN_RETURN;
	}
	memset(rxBuffer,0,sizeof(rxBuffer));
}

void processCommand(const char *input) {
    static int prevYellow = -1;
    static int prevRed = -1;
    static int prevBlue = -1;
    static int prevBuzzer = -1;
    static int prevBtnReset = -1;
    if (strcmp(input, "led_yellow:on") == 0) {
        if (prevYellow != 1) {
            machineOutputs.lightYellow = 1;
            prevYellow = 1;

        }
    } else if (strcmp(input, "led_yellow:off") == 0) {
        if (prevYellow != 0) {
            machineOutputs.lightYellow = 0;
            prevYellow = 0;
        }
    } else if (strcmp(input, "led_red:on") == 0) {
        if (prevRed != 1) {
            machineOutputs.lightRed = 1;
            prevRed = 1;

        }
    } else if (strcmp(input, "led_red:off") == 0) {
        if (prevRed != 0) {
            machineOutputs.lightRed = 0;
            prevRed = 0;

        }
    } else if (strcmp(input, "led_blue:on") == 0) {
        if (prevBlue != 1) {
            machineOutputs.lightBlue = 1;
            prevBlue = 1;

        }
    } else if (strcmp(input, "led_blue:off") == 0) {
        if (prevBlue != 0) {
            machineOutputs.lightBlue = 0;
            prevBlue = 0;

        }
    } else if (strcmp(input, "buzzer:on") == 0) {
        if (prevBuzzer != 1) {
            machineOutputs.buzzer = 1;
            prevBuzzer = 1;

        }
    } else if (strcmp(input, "buzzer:off") == 0) {
        if (prevBuzzer != 0) {
            machineOutputs.buzzer = 0;
            prevBuzzer = 0;

        }
    } else if (strcmp(input, "btn_led_reset:on") == 0) {
        if (prevBtnReset != 1) {
            machineOutputs.lightBtnReset = 1;
            prevBtnReset = 1;

        }
    } else if (strcmp(input, "btn_led_reset:off") == 0) {
        if (prevBtnReset != 0) {
            machineOutputs.lightBtnReset = 0;
            prevBtnReset = 0;

        }
    }
    else if (strcmp(input, "starus_all") == 0){
    	char data_status_all[64]= "";


    	snprintf(data_status_all, sizeof(data_status_all),
    	         "status_all:%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d\n",
    	         machineOutputs.lightYellow, machineOutputs.lightRed, machineOutputs.lightBlue,
    	         machineOutputs.buzzer, machineOutputs.lightBtnReset, machineInputs.btnReset,
    	         machineInputs.btnStop, machineInputs.btnStart, machineInputs.sensorObjectLeft,
    	         machineInputs.sensorObjectRight, machineInputs.sensorSafety);
    	CDC_Transmit_FS((uint8_t *)data_status_all, strlen(data_status_all));
    }
    else if (strcmp(input, "move_to_org") == 0){
    	stepIAI = STEP_IAI_PREPARE_OPERATION;
    	vTaskDelay(pdMS_TO_TICKS(30));
    	stepIAI = STEP_IAI_ORG;
    }
    else if (strcmp(input, "pause") == 0){
    	HAL_GPIO_WritePin(axisX.driverOutput.STP.port, axisX.driverOutput.STP.pin, GPIO_PIN_RESET);
    	HAL_GPIO_WritePin(axisY.driverOutput.STP.port, axisY.driverOutput.STP.pin, GPIO_PIN_RESET);
    	HAL_GPIO_WritePin(axisZ.driverOutput.STP.port, axisZ.driverOutput.STP.pin, GPIO_PIN_RESET);
    }
    else if (strcmp(input, "run") == 0){
		HAL_GPIO_WritePin(axisX.driverOutput.STP.port, axisX.driverOutput.STP.pin, GPIO_PIN_SET);
		HAL_GPIO_WritePin(axisY.driverOutput.STP.port, axisY.driverOutput.STP.pin, GPIO_PIN_SET);
		HAL_GPIO_WritePin(axisZ.driverOutput.STP.port, axisZ.driverOutput.STP.pin, GPIO_PIN_SET);
    }
}



void sendCmdHandle(){
//	CDC_Transmit_FS(UserRxBufferFS, sizeof(UserRxBufferFS));
//	vTaskDelay(pdMS_TO_TICKS(30));
	if(txBuffer[0] == 0){
		if(txErrorString[0] != '\0'){
			memcpy(txBuffer,txErrorString,sizeof(txErrorString));
			memset(txErrorString,0,sizeof(txErrorString));
		}else if(txIAIBuffer[0] != '\0'){
			memcpy(txBuffer, txIAIBuffer, sizeof(txIAIBuffer));
			memset(txIAIBuffer,0,sizeof(txIAIBuffer));
		}
		else if(txGPIO[0] != '\0'){
					memcpy(txBuffer, txGPIO, sizeof(txGPIO));
					memset(txGPIO,0,sizeof(txGPIO));
	   }

	}
	if(txBuffer[0] != 0){
		CDC_Transmit_FS(txBuffer, strlen((char*)txBuffer));
		vTaskDelay(pdMS_TO_TICKS(30));
		memset(txBuffer,0,sizeof(txBuffer));
	}
//	uint8_t tmp[200] ={0};
//	snprintf((char*) tmp,sizeof(tmp),"IAI STEP : %d Mode: %d RUN:%d SS:%d\n",
//			stepIAI,machineMode, stepRun,machineInputs.sensorSafety);
//	CDC_Transmit_FS(tmp, strlen((char*)tmp));
//	vTaskDelay(pdMS_TO_TICKS(30));
}
