/*
 * mVariable.c
 *
 *  Created on: Jun 26, 2025
 *      Author: lamdo
 */

#include "mVariable.h"

volatile uint8_t mMachineMode = 0, mMachineStatus = 0;
volatile INPUTS machineInputs;
volatile OUTPUTS machineOutputs;
uint8_t rxBuffer[APP_RX_DATA_SIZE] = {0};
uint8_t txBuffer[APP_TX_DATA_SIZE] = {0};
volatile uint8_t pwmValue = 8;
