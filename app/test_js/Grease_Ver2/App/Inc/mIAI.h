/*
 * mIAI.h
 *
 *  Created on: Jun 26, 2025
 *      Author: lamdo
 */

#ifndef INC_MIAI_H_
#define INC_MIAI_H_

#include "stdint.h"
#include "stdbool.h"
#include "mGPIO.h"

typedef struct{
	GPIO_PIN	PM1 ;
	GPIO_PIN	PM2 ;
	GPIO_PIN	PM4 ;
	GPIO_PIN	PM8 ;
	GPIO_PIN	PM16 ;
	GPIO_PIN	PM32 ;
	GPIO_PIN	PM64 ;
	GPIO_PIN	PM128 ;
	GPIO_PIN	HEND ;
	GPIO_PIN	PEND ;
	GPIO_PIN	SV ;
	GPIO_PIN	ALM ;
}IAI_GPIO_INPUT;

typedef struct {
	GPIO_PIN	PC1;
	GPIO_PIN	PC2;
	GPIO_PIN	PC4;
	GPIO_PIN	PC8;
	GPIO_PIN	PC16;
	GPIO_PIN	PC32;
	GPIO_PIN	PC64;
	GPIO_PIN	PC128;
	GPIO_PIN	BKRL;
	GPIO_PIN	HOME;
	GPIO_PIN	STP;
	GPIO_PIN	CSTR;
	GPIO_PIN	RES;
	GPIO_PIN	SON;
}IAI_GPIO_OUTPUT;

typedef union{
	struct{
		uint8_t toPos;
	};
	struct{
		unsigned 	PC1 : 1;
		unsigned 	PC2 : 1;
		unsigned 	PC4 : 1;
		unsigned 	PC8 : 1;
		unsigned 	PC16 : 1;
		unsigned 	PC32 : 1;
		unsigned 	PC64 : 1;
		unsigned 	PC128 : 1;
	};
}DRIVER_POS_SET;

typedef union{
	struct{
		uint8_t nowPos;
	};
	struct{
		unsigned	PM1 : 1;
		unsigned	PM2 : 1;
		unsigned	PM4 : 1;
		unsigned	PM8 : 1;
		unsigned	PM16 : 1;
		unsigned	PM32 : 1;
		unsigned	PM64 : 1;
		unsigned	PM128 : 1;
	};
}DRIVER_POS_GET;

typedef struct {
	unsigned REQ_PREPARE 	: 1;
	unsigned REQ_ORG 	 	: 1;
	unsigned REQ_MOVE	 	: 1;
	unsigned REQ_RESET		: 1;
}REQ_CMD;

typedef struct{
	unsigned ACK_PREPARE	: 1;
	unsigned ACK_ORG		: 1;
	unsigned ACK_MOVE		: 1;
	unsigned ACK_RESET		: 1;
}ACK_CMD;

typedef enum{
	STEP_IAI_WAIT,
	STEP_IAI_PREPARE_OPERATION,
	STEP_IAI_RESET,
	STEP_IAI_MOVE,
	STEP_IAI_ORG,
	STEP_IAI_PAUSE,
	STEP_IAI_STOP,
}STEP_IAI;

//typedef struct {
//	unsigned HEND : 1;
//	unsigned PEND : 1;
//	unsigned SV : 1;
//	unsigned ALM : 1;
//}DRIVER_STATUS;
//
//typedef struct{
//	unsigned BKRL : 1;
//	unsigned HOME : 1;
//	unsigned STP : 1;
//	unsigned CSTR : 1;
//	unsigned RES : 1;
//	unsigned SON : 1;
//}DRIVER_CONTROL;

typedef struct{
	DRIVER_POS_SET targetPos;
	DRIVER_POS_GET currentPos;
}IAI_INFO;

typedef struct AXIS{
	IAI_INFO position;
	IAI_GPIO_INPUT driverInput;
	IAI_GPIO_OUTPUT driverOutput;
	REQ_CMD request;
	ACK_CMD acknowledge;
	bool (*move)(struct AXIS*, uint8_t);
	bool (*home)(struct AXIS*);
	bool (*pause)(struct AXIS* );
	bool (*continues)(struct AXIS*);
	bool (*stop)(struct AXIS* );
	bool (*clear)(struct AXIS* );
	bool (*clearError) (struct AXIS*);
	bool (*prepare)(struct AXIS* );
}AXIS;

void IAIMovingHandled();

extern AXIS axisX,axisY,axisZ;
extern bool isStopIAI;
extern uint8_t txIAIBuffer[2048];
extern uint8_t stepIAI, iaiOnceTimes;


#endif /* INC_MIAI_H_ */
