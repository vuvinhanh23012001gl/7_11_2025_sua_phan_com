/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file           : main.h
  * @brief          : Header for main.c file.
  *                   This file contains the common defines of the application.
  ******************************************************************************
  * @attention
  *
  * Copyright (c) 2025 STMicroelectronics.
  * All rights reserved.
  *
  * This software is licensed under terms that can be found in the LICENSE file
  * in the root directory of this software component.
  * If no LICENSE file comes with this software, it is provided AS-IS.
  *
  ******************************************************************************
  */
/* USER CODE END Header */

/* Define to prevent recursive inclusion -------------------------------------*/
#ifndef __MAIN_H
#define __MAIN_H

#ifdef __cplusplus
extern "C" {
#endif

/* Includes ------------------------------------------------------------------*/
#include "stm32f4xx_hal.h"

/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */

/* USER CODE END Includes */

/* Exported types ------------------------------------------------------------*/
/* USER CODE BEGIN ET */

/* USER CODE END ET */

/* Exported constants --------------------------------------------------------*/
/* USER CODE BEGIN EC */

/* USER CODE END EC */

/* Exported macro ------------------------------------------------------------*/
/* USER CODE BEGIN EM */

/* USER CODE END EM */

void HAL_TIM_MspPostInit(TIM_HandleTypeDef *htim);

/* Exported functions prototypes ---------------------------------------------*/
void Error_Handler(void);

/* USER CODE BEGIN EFP */

/* USER CODE END EFP */

/* Private defines -----------------------------------------------------------*/
#define GPIO_IN_Z_HEND_Pin GPIO_PIN_2
#define GPIO_IN_Z_HEND_GPIO_Port GPIOE
#define GPIO_IN_Z_PEND_Pin GPIO_PIN_3
#define GPIO_IN_Z_PEND_GPIO_Port GPIOE
#define GPIO_IN_Z_SV_Pin GPIO_PIN_4
#define GPIO_IN_Z_SV_GPIO_Port GPIOE
#define GPIO_IN_Z_ALM_Pin GPIO_PIN_5
#define GPIO_IN_Z_ALM_GPIO_Port GPIOE
#define GPIO_IN_Y_PM1_Pin GPIO_PIN_6
#define GPIO_IN_Y_PM1_GPIO_Port GPIOE
#define GPIO_IN_Y_PM2_Pin GPIO_PIN_8
#define GPIO_IN_Y_PM2_GPIO_Port GPIOI
#define GPIO_IN_Y_PM4_Pin GPIO_PIN_13
#define GPIO_IN_Y_PM4_GPIO_Port GPIOC
#define GPIO_IN_Y_PM8_Pin GPIO_PIN_9
#define GPIO_IN_Y_PM8_GPIO_Port GPIOI
#define GPIO_IN_Y_PM16_Pin GPIO_PIN_10
#define GPIO_IN_Y_PM16_GPIO_Port GPIOI
#define GPIO_IN_Y_PM32_Pin GPIO_PIN_11
#define GPIO_IN_Y_PM32_GPIO_Port GPIOI
#define GPIO_IN_Y_PM64_Pin GPIO_PIN_0
#define GPIO_IN_Y_PM64_GPIO_Port GPIOF
#define GPIO_IN_Y_PM128_Pin GPIO_PIN_1
#define GPIO_IN_Y_PM128_GPIO_Port GPIOF
#define GPIO_IN_Y_HEND_Pin GPIO_PIN_2
#define GPIO_IN_Y_HEND_GPIO_Port GPIOF
#define GPIO_IN_Y_PEND_Pin GPIO_PIN_3
#define GPIO_IN_Y_PEND_GPIO_Port GPIOF
#define GPIO_IN_Y_SV_Pin GPIO_PIN_4
#define GPIO_IN_Y_SV_GPIO_Port GPIOF
#define GPIO_IN_Y_ALM_Pin GPIO_PIN_5
#define GPIO_IN_Y_ALM_GPIO_Port GPIOF
#define GPIO_IN_X_PM1_Pin GPIO_PIN_6
#define GPIO_IN_X_PM1_GPIO_Port GPIOF
#define GPIO_IN_X_PM2_Pin GPIO_PIN_7
#define GPIO_IN_X_PM2_GPIO_Port GPIOF
#define GPIO_IN_X_PM4_Pin GPIO_PIN_8
#define GPIO_IN_X_PM4_GPIO_Port GPIOF
#define GPIO_IN_X_PM8_Pin GPIO_PIN_9
#define GPIO_IN_X_PM8_GPIO_Port GPIOF
#define GPIO_IN_X_PM16_Pin GPIO_PIN_10
#define GPIO_IN_X_PM16_GPIO_Port GPIOF
#define GPIO_IN_X_PM32_Pin GPIO_PIN_0
#define GPIO_IN_X_PM32_GPIO_Port GPIOC
#define GPIO_IN_X_PM64_Pin GPIO_PIN_1
#define GPIO_IN_X_PM64_GPIO_Port GPIOC
#define GPIO_IN_X_PM128_Pin GPIO_PIN_2
#define GPIO_IN_X_PM128_GPIO_Port GPIOC
#define GPIO_IN_X_HEND_Pin GPIO_PIN_3
#define GPIO_IN_X_HEND_GPIO_Port GPIOC
#define GPIO_IN_X_PEND_Pin GPIO_PIN_1
#define GPIO_IN_X_PEND_GPIO_Port GPIOA
#define GPIO_IN_X_SV_Pin GPIO_PIN_2
#define GPIO_IN_X_SV_GPIO_Port GPIOH
#define GPIO_IN_X_ALM_Pin GPIO_PIN_3
#define GPIO_IN_X_ALM_GPIO_Port GPIOH
#define GPIO_OUT_Z_PC1_Pin GPIO_PIN_7
#define GPIO_OUT_Z_PC1_GPIO_Port GPIOA
#define GPIO_OUT_Z_PC2_Pin GPIO_PIN_0
#define GPIO_OUT_Z_PC2_GPIO_Port GPIOB
#define GPIO_OUT_Z_PC4_Pin GPIO_PIN_1
#define GPIO_OUT_Z_PC4_GPIO_Port GPIOB
#define GPIO_OUT_Z_PC8_Pin GPIO_PIN_11
#define GPIO_OUT_Z_PC8_GPIO_Port GPIOF
#define GPIO_OUT_Z_PC16_Pin GPIO_PIN_12
#define GPIO_OUT_Z_PC16_GPIO_Port GPIOF
#define GPIO_OUT_Z_PC32_Pin GPIO_PIN_13
#define GPIO_OUT_Z_PC32_GPIO_Port GPIOF
#define GPIO_OUT_Z_PC64_Pin GPIO_PIN_14
#define GPIO_OUT_Z_PC64_GPIO_Port GPIOF
#define GPIO_OUT_Z_PC128_Pin GPIO_PIN_15
#define GPIO_OUT_Z_PC128_GPIO_Port GPIOF
#define GPIO_OUT_Z_BKRL_Pin GPIO_PIN_0
#define GPIO_OUT_Z_BKRL_GPIO_Port GPIOG
#define GPIO_OUT_Z_HOME_Pin GPIO_PIN_1
#define GPIO_OUT_Z_HOME_GPIO_Port GPIOG
#define GPIO_OUT_Z_STP_Pin GPIO_PIN_7
#define GPIO_OUT_Z_STP_GPIO_Port GPIOE
#define GPIO_OUT_Z_CSTR_Pin GPIO_PIN_8
#define GPIO_OUT_Z_CSTR_GPIO_Port GPIOE
#define GPIO_OUT_Z_RES_Pin GPIO_PIN_9
#define GPIO_OUT_Z_RES_GPIO_Port GPIOE
#define GPIO_OUT_Z_SON_Pin GPIO_PIN_10
#define GPIO_OUT_Z_SON_GPIO_Port GPIOE
#define GPIO_OUT_X_PC1_Pin GPIO_PIN_11
#define GPIO_OUT_X_PC1_GPIO_Port GPIOE
#define GPIO_OUT_X_PC2_Pin GPIO_PIN_12
#define GPIO_OUT_X_PC2_GPIO_Port GPIOE
#define GPIO_OUT_X_PC4_Pin GPIO_PIN_13
#define GPIO_OUT_X_PC4_GPIO_Port GPIOE
#define GPIO_OUT_X_PC8_Pin GPIO_PIN_14
#define GPIO_OUT_X_PC8_GPIO_Port GPIOE
#define GPIO_OUT_X_PC16_Pin GPIO_PIN_15
#define GPIO_OUT_X_PC16_GPIO_Port GPIOE
#define GPIO_OUT_X_PC32_Pin GPIO_PIN_10
#define GPIO_OUT_X_PC32_GPIO_Port GPIOB
#define GPIO_OUT_X_PC64_Pin GPIO_PIN_11
#define GPIO_OUT_X_PC64_GPIO_Port GPIOB
#define GPIO_OUT_X_PC128_Pin GPIO_PIN_6
#define GPIO_OUT_X_PC128_GPIO_Port GPIOH
#define GPIO_OUT_X_BKRL_Pin GPIO_PIN_7
#define GPIO_OUT_X_BKRL_GPIO_Port GPIOH
#define GPIO_OUT_X_HOME_Pin GPIO_PIN_8
#define GPIO_OUT_X_HOME_GPIO_Port GPIOH
#define GPIO_OUT_X_STP_Pin GPIO_PIN_9
#define GPIO_OUT_X_STP_GPIO_Port GPIOH
#define GPIO_OUT_X_CSTR_Pin GPIO_PIN_10
#define GPIO_OUT_X_CSTR_GPIO_Port GPIOH
#define GPIO_OUT_X_RES_Pin GPIO_PIN_11
#define GPIO_OUT_X_RES_GPIO_Port GPIOH
#define GPIO_OUT_X_SON_Pin GPIO_PIN_12
#define GPIO_OUT_X_SON_GPIO_Port GPIOH
#define GPIO_OUT_Y_PC1_Pin GPIO_PIN_12
#define GPIO_OUT_Y_PC1_GPIO_Port GPIOB
#define GPIO_OUT_Y_PC2_Pin GPIO_PIN_13
#define GPIO_OUT_Y_PC2_GPIO_Port GPIOB
#define GPIO_OUT_Y_PC4_Pin GPIO_PIN_14
#define GPIO_OUT_Y_PC4_GPIO_Port GPIOB
#define GPIO_OUT_Y_PC8_Pin GPIO_PIN_15
#define GPIO_OUT_Y_PC8_GPIO_Port GPIOB
#define GPIO_OUT_Y_PC16_Pin GPIO_PIN_8
#define GPIO_OUT_Y_PC16_GPIO_Port GPIOD
#define GPIO_OUT_Y_PC32_Pin GPIO_PIN_9
#define GPIO_OUT_Y_PC32_GPIO_Port GPIOD
#define GPIO_OUT_Y_PC64_Pin GPIO_PIN_10
#define GPIO_OUT_Y_PC64_GPIO_Port GPIOD
#define GPIO_OUT_Y_PC128_Pin GPIO_PIN_11
#define GPIO_OUT_Y_PC128_GPIO_Port GPIOD
#define GPIO_OUT_Y_BKRL_Pin GPIO_PIN_12
#define GPIO_OUT_Y_BKRL_GPIO_Port GPIOD
#define GPIO_OUT_Y_HOME_Pin GPIO_PIN_13
#define GPIO_OUT_Y_HOME_GPIO_Port GPIOD
#define GPIO_OUT_Y_STP_Pin GPIO_PIN_14
#define GPIO_OUT_Y_STP_GPIO_Port GPIOD
#define GPIO_OUT_Y_CSTR_Pin GPIO_PIN_15
#define GPIO_OUT_Y_CSTR_GPIO_Port GPIOD
#define GPIO_OUT_Y_RES_Pin GPIO_PIN_2
#define GPIO_OUT_Y_RES_GPIO_Port GPIOG
#define GPIO_OUT_Y_SON_Pin GPIO_PIN_3
#define GPIO_OUT_Y_SON_GPIO_Port GPIOG
#define GPIO_OUT_LIGHT_BLUE_Pin GPIO_PIN_4
#define GPIO_OUT_LIGHT_BLUE_GPIO_Port GPIOG
#define GPIO_OUT_LIGHT_RED_Pin GPIO_PIN_5
#define GPIO_OUT_LIGHT_RED_GPIO_Port GPIOG
#define GPIO_OUT_LIGHT_YELLOW_Pin GPIO_PIN_6
#define GPIO_OUT_LIGHT_YELLOW_GPIO_Port GPIOG
#define GPIO_OUT_BUZZER_Pin GPIO_PIN_7
#define GPIO_OUT_BUZZER_GPIO_Port GPIOG
#define GPIO_OUT_LIGHT_RESET_Pin GPIO_PIN_8
#define GPIO_OUT_LIGHT_RESET_GPIO_Port GPIOG
#define TIM1_CH1_Pin GPIO_PIN_8
#define TIM1_CH1_GPIO_Port GPIOA
#define USB_OTG_FS_VID_Pin GPIO_PIN_2
#define USB_OTG_FS_VID_GPIO_Port GPIOI
#define USB_OTG_FS_VBUS_Pin GPIO_PIN_12
#define USB_OTG_FS_VBUS_GPIO_Port GPIOC

#define GPIO_IN_SW_START_Pin GPIO_PIN_10
#define GPIO_IN_SW_START_GPIO_Port GPIOG
#define GPIO_IN_SW_RESET_Pin GPIO_PIN_4
#define GPIO_IN_SW_RESET_GPIO_Port GPIOD
#define GPIO_IN_SW_STOP_Pin GPIO_PIN_5
#define GPIO_IN_SW_STOP_GPIO_Port GPIOD
#define GPIO_IN_SS_LEFT_Pin GPIO_PIN_6
#define GPIO_IN_SS_LEFT_GPIO_Port GPIOD
#define GPIO_IN_SS_RIGHT_Pin GPIO_PIN_7
#define GPIO_IN_SS_RIGHT_GPIO_Port GPIOD
#define GPIO_IN_SS_SAFE_Pin GPIO_PIN_9
#define GPIO_IN_SS_SAFE_GPIO_Port GPIOG
#define GPIO_IN_Z_PM1_Pin GPIO_PIN_8
#define GPIO_IN_Z_PM1_GPIO_Port GPIOB
#define GPIO_IN_Z_PM2_Pin GPIO_PIN_9
#define GPIO_IN_Z_PM2_GPIO_Port GPIOB
#define GPIO_IN_Z_PM4_Pin GPIO_PIN_0
#define GPIO_IN_Z_PM4_GPIO_Port GPIOE
#define GPIO_IN_Z_PM8_Pin GPIO_PIN_1
#define GPIO_IN_Z_PM8_GPIO_Port GPIOE
#define GPIO_IN_Z_PM16_Pin GPIO_PIN_4
#define GPIO_IN_Z_PM16_GPIO_Port GPIOI
#define GPIO_IN_Z_PM32_Pin GPIO_PIN_5
#define GPIO_IN_Z_PM32_GPIO_Port GPIOI
#define GPIO_IN_Z_PM64_Pin GPIO_PIN_6
#define GPIO_IN_Z_PM64_GPIO_Port GPIOI
#define GPIO_IN_Z_PM128_Pin GPIO_PIN_7
#define GPIO_IN_Z_PM128_GPIO_Port GPIOI

/* USER CODE BEGIN Private defines */

/* USER CODE END Private defines */

#ifdef __cplusplus
}
#endif

#endif /* __MAIN_H */
