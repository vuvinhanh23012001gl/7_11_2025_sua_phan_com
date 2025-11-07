/*
 * mVariable.h
 *
 *  Created on: Jun 26, 2025
 *      Author: lamdo
 */

#ifndef INC_MVARIABLE_H_
#define INC_MVARIABLE_H_

#include "stdint.h"
#include "stdbool.h"
#include "usbd_cdc_if.h"

typedef enum{
	MODE_WAIT,
	MODE_ORG,
	MODE_RUN,
	MODE_MANUAL
}MACHINE_MODE;

typedef enum{
	MACHINE_RUN,
	MACHINE_ERROR,
	MACHINE_PAUSE,
	MACHINE_STOP,
}MACHINE_STATUS;

typedef struct {
	unsigned btnStart : 1;
	unsigned btnStop : 1;
	unsigned btnReset : 1;
	unsigned sensorSafety : 1;
	unsigned sensorObjectLeft : 1;
	unsigned sensorObjectRight : 1;
	unsigned swDoor : 1;
}INPUTS;

typedef struct{
	unsigned lightRed : 1;
	unsigned lightBlue : 1;
	unsigned lightYellow : 1;
	unsigned lightBtnReset : 1;
	unsigned lightBtnStart : 1;
	unsigned buzzer : 1;
}OUTPUTS;



extern volatile INPUTS machineInputs;
extern volatile OUTPUTS machineOutputs;
extern uint8_t rxBuffer[APP_RX_DATA_SIZE];
extern uint8_t txBuffer[APP_TX_DATA_SIZE];
extern volatile uint8_t pwmValue;


#endif /* INC_MVARIABLE_H_ */
