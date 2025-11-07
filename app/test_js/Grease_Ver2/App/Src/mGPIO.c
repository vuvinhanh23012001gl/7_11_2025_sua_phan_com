/*
 * mGPIO.c
 *
 *  Created on: Jun 26, 2025
 *      Author: lamdo
 */

#include "mGPIO.h"
#include "mVariable.h"
#include "mIAI.h"
#include "mVariable.h"

uint8_t txGPIO[2048] = {0};
void gpioScan(){
//	if(stepIAI != STEP_IAI_MOVE){
		axisX.position.currentPos.PM1 = !HAL_GPIO_ReadPin(axisX.driverInput.PM1.port, axisX.driverInput.PM1.pin);
		axisX.position.currentPos.PM2 = !HAL_GPIO_ReadPin(axisX.driverInput.PM2.port, axisX.driverInput.PM2.pin);
		axisX.position.currentPos.PM4 = !HAL_GPIO_ReadPin(axisX.driverInput.PM4.port, axisX.driverInput.PM4.pin);
		axisX.position.currentPos.PM8 = !HAL_GPIO_ReadPin(axisX.driverInput.PM8.port, axisX.driverInput.PM8.pin);
		axisX.position.currentPos.PM16 = !HAL_GPIO_ReadPin(axisX.driverInput.PM16.port, axisX.driverInput.PM16.pin);
		axisX.position.currentPos.PM32 = !HAL_GPIO_ReadPin(axisX.driverInput.PM32.port, axisX.driverInput.PM32.pin);
		axisX.position.currentPos.PM64 = !HAL_GPIO_ReadPin(axisX.driverInput.PM64.port, axisX.driverInput.PM64.pin);
		axisX.position.currentPos.PM128 = !HAL_GPIO_ReadPin(axisX.driverInput.PM128.port, axisX.driverInput.PM128.pin);
		axisY.position.currentPos.PM1 = !HAL_GPIO_ReadPin(axisY.driverInput.PM1.port, axisY.driverInput.PM1.pin);
		axisY.position.currentPos.PM2 = !HAL_GPIO_ReadPin(axisY.driverInput.PM2.port, axisY.driverInput.PM2.pin);
		axisY.position.currentPos.PM4 = !HAL_GPIO_ReadPin(axisY.driverInput.PM4.port, axisY.driverInput.PM4.pin);
		axisY.position.currentPos.PM8 = !HAL_GPIO_ReadPin(axisY.driverInput.PM8.port, axisY.driverInput.PM8.pin);
		axisY.position.currentPos.PM16 = !HAL_GPIO_ReadPin(axisY.driverInput.PM16.port, axisY.driverInput.PM16.pin);
		axisY.position.currentPos.PM32 = !HAL_GPIO_ReadPin(axisY.driverInput.PM32.port, axisY.driverInput.PM32.pin);
		axisY.position.currentPos.PM64 = !HAL_GPIO_ReadPin(axisY.driverInput.PM64.port, axisY.driverInput.PM64.pin);
		axisY.position.currentPos.PM128 = !HAL_GPIO_ReadPin(axisY.driverInput.PM128.port, axisY.driverInput.PM128.pin);
		axisZ.position.currentPos.PM1 = !HAL_GPIO_ReadPin(axisZ.driverInput.PM1.port, axisZ.driverInput.PM1.pin);
		axisZ.position.currentPos.PM2 = !HAL_GPIO_ReadPin(axisZ.driverInput.PM2.port, axisZ.driverInput.PM2.pin);
		axisZ.position.currentPos.PM4 = !HAL_GPIO_ReadPin(axisZ.driverInput.PM4.port, axisZ.driverInput.PM4.pin);
		axisZ.position.currentPos.PM8 = !HAL_GPIO_ReadPin(axisZ.driverInput.PM8.port, axisZ.driverInput.PM8.pin);
		axisZ.position.currentPos.PM16 = !HAL_GPIO_ReadPin(axisZ.driverInput.PM16.port, axisZ.driverInput.PM16.pin);
		axisZ.position.currentPos.PM32 = !HAL_GPIO_ReadPin(axisZ.driverInput.PM32.port, axisZ.driverInput.PM32.pin);
		axisZ.position.currentPos.PM64 = !HAL_GPIO_ReadPin(axisZ.driverInput.PM64.port, axisZ.driverInput.PM64.pin);
		axisZ.position.currentPos.PM128 = !HAL_GPIO_ReadPin(axisZ.driverInput.PM128.port, axisZ.driverInput.PM128.pin);
	//}
	machineInputs.btnReset = HAL_GPIO_ReadPin(GPIO_IN_SW_RESET_GPIO_Port, GPIO_IN_SW_RESET_Pin) == GPIO_PIN_RESET ? true : false;
	machineInputs.btnStop = HAL_GPIO_ReadPin(GPIO_IN_SW_STOP_GPIO_Port, GPIO_IN_SW_STOP_Pin) == GPIO_PIN_RESET ? true : false;
	machineInputs.btnStart = HAL_GPIO_ReadPin(GPIO_IN_SW_START_GPIO_Port, GPIO_IN_SW_START_Pin) == GPIO_PIN_RESET ? true : false;
	machineInputs.sensorObjectLeft = HAL_GPIO_ReadPin(GPIO_IN_SS_LEFT_GPIO_Port, GPIO_IN_SS_LEFT_Pin) == GPIO_PIN_RESET ? true : false;
	machineInputs.sensorObjectRight = HAL_GPIO_ReadPin(GPIO_IN_SS_RIGHT_GPIO_Port, GPIO_IN_SS_RIGHT_Pin) == GPIO_PIN_RESET ? true : false;
	machineInputs.sensorSafety = HAL_GPIO_ReadPin(GPIO_IN_SS_SAFE_GPIO_Port, GPIO_IN_SS_SAFE_Pin) == GPIO_PIN_RESET ? true : false;
	machineInputs.swDoor = true;
	HAL_GPIO_WritePin(GPIO_OUT_LIGHT_BLUE_GPIO_Port, GPIO_OUT_LIGHT_BLUE_Pin, machineOutputs.lightBlue == true ? GPIO_PIN_SET : GPIO_PIN_RESET);
	HAL_GPIO_WritePin(GPIO_OUT_LIGHT_RED_GPIO_Port, GPIO_OUT_LIGHT_RED_Pin, machineOutputs.lightRed == true ? GPIO_PIN_SET : GPIO_PIN_RESET);
	HAL_GPIO_WritePin(GPIO_OUT_LIGHT_YELLOW_GPIO_Port, GPIO_OUT_LIGHT_YELLOW_Pin, machineOutputs.lightYellow == true ? GPIO_PIN_SET : GPIO_PIN_RESET);
	HAL_GPIO_WritePin(GPIO_OUT_BUZZER_GPIO_Port, GPIO_OUT_BUZZER_Pin, machineOutputs.buzzer == true ? GPIO_PIN_SET : GPIO_PIN_RESET);
	HAL_GPIO_WritePin(GPIO_OUT_LIGHT_RESET_GPIO_Port, GPIO_OUT_LIGHT_RESET_Pin, machineOutputs.lightBtnReset == true ? GPIO_PIN_SET : GPIO_PIN_RESET);
	checkAndSendInputChanges();
}


void sendButtonStateChange(const char *name, bool state) {
    snprintf((char*)txGPIO, sizeof(txGPIO), "%s:%s\r\n", name, state ? "1" : "0");
}

void checkAndSendInputChanges() {

    static bool prevBtnReset = false;
    static bool prevBtnStop = false;
    static bool prevBtnStart = false;
    static bool prevSensorLeft = false;
    static bool prevSensorRight = false;
    static bool prevSensorSafety = false;
    static bool prevSwDoor = false;

    if (machineInputs.btnReset != prevBtnReset) {
        sendButtonStateChange("btn_reset", machineInputs.btnReset);
        prevBtnReset = machineInputs.btnReset;
    }
    if (machineInputs.btnStop != prevBtnStop) {
        sendButtonStateChange("btn_stop", machineInputs.btnStop);
        prevBtnStop = machineInputs.btnStop;
    }
    if (machineInputs.btnStart != prevBtnStart) {
        sendButtonStateChange("btn_start", machineInputs.btnStart);
        prevBtnStart = machineInputs.btnStart;
    }
    if (machineInputs.sensorObjectLeft != prevSensorLeft) {
        sendButtonStateChange("sensor_left", machineInputs.sensorObjectLeft);
        prevSensorLeft = machineInputs.sensorObjectLeft;
    }
    if (machineInputs.sensorObjectRight != prevSensorRight) {
        sendButtonStateChange("sensor_right", machineInputs.sensorObjectRight);
        prevSensorRight = machineInputs.sensorObjectRight;
    }
    if (machineInputs.sensorSafety != prevSensorSafety) {
        sendButtonStateChange("sensor_safety", machineInputs.sensorSafety);
        prevSensorSafety = machineInputs.sensorSafety;
    }
    if (machineInputs.swDoor != prevSwDoor) {
        sendButtonStateChange("sw_door", machineInputs.swDoor);
        prevSwDoor = machineInputs.swDoor;
    }
}

