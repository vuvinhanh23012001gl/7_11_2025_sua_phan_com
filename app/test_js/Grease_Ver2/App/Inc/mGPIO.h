/*
 * mGPIO.h
 *
 *  Created on: Jun 26, 2025
 *      Author: lamdo
 */

#ifndef INC_MGPIO_H_
#define INC_MGPIO_H_
#include "main.h"
#include "stm32f4xx_hal.h"
#include <stdbool.h>
typedef struct {
	GPIO_TypeDef* port;
	uint16_t pin;
}GPIO_PIN;
void sendButtonStateChange(const char *name, bool state);
void checkAndSendInputChanges();

void gpioScan(void);
extern uint8_t txGPIO[2048];
#endif /* INC_MGPIO_H_ */
