/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file           : main.c
  * @brief          : Main program body
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
/* Includes ------------------------------------------------------------------*/
#include "main.h"
#include "cmsis_os.h"
#include "usb_device.h"

/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */
#include "mIAI.h"
#include "mVariable.h"
#include "mFunction.h"
#include "mFlow.h"
#include "mGPIO.h"
#include "mRS232.h"
#include "mErrorHandle.h"
/* USER CODE END Includes */

/* Private typedef -----------------------------------------------------------*/
/* USER CODE BEGIN PTD */

/* USER CODE END PTD */

/* Private define ------------------------------------------------------------*/
/* USER CODE BEGIN PD */
#define configUSE_TRACE_FACILITY 1
/* USER CODE END PD */

/* Private macro -------------------------------------------------------------*/
/* USER CODE BEGIN PM */

/* USER CODE END PM */

/* Private variables ---------------------------------------------------------*/
TIM_HandleTypeDef htim1;
TIM_HandleTypeDef htim4;
TIM_HandleTypeDef htim7;

/* Definitions for mTaskFlow */
osThreadId_t mTaskFlowHandle;
const osThreadAttr_t mTaskFlow_attributes = {
  .name = "mTaskFlow",
  .stack_size = 512 * 4,
  .priority = (osPriority_t) osPriorityNormal,
};
/* Definitions for mTaskGPIO */
osThreadId_t mTaskGPIOHandle;
const osThreadAttr_t mTaskGPIO_attributes = {
  .name = "mTaskGPIO",
  .stack_size = 256 * 4,
  .priority = (osPriority_t) osPriorityNormal,
};
/* Definitions for mTaskIAIX */
osThreadId_t mTaskIAIXHandle;
const osThreadAttr_t mTaskIAIX_attributes = {
  .name = "mTaskIAIX",
  .stack_size = 512 * 4,
  .priority = (osPriority_t) osPriorityNormal,
};
/* Definitions for myTaskCOM */
osThreadId_t myTaskCOMHandle;
const osThreadAttr_t myTaskCOM_attributes = {
  .name = "myTaskCOM",
  .stack_size = 512 * 4,
  .priority = (osPriority_t) osPriorityNormal,
};
/* Definitions for mTaskIAIY */
osThreadId_t mTaskIAIYHandle;
const osThreadAttr_t mTaskIAIY_attributes = {
  .name = "mTaskIAIY",
  .stack_size = 512 * 4,
  .priority = (osPriority_t) osPriorityNormal,
};
/* Definitions for mTaskIAIZ */
osThreadId_t mTaskIAIZHandle;
const osThreadAttr_t mTaskIAIZ_attributes = {
  .name = "mTaskIAIZ",
  .stack_size = 512 * 4,
  .priority = (osPriority_t) osPriorityNormal,
};
/* Definitions for mTaskIAI */
osThreadId_t mTaskIAIHandle;
const osThreadAttr_t mTaskIAI_attributes = {
  .name = "mTaskIAI",
  .stack_size = 512 * 4,
  .priority = (osPriority_t) osPriorityNormal,
};
/* USER CODE BEGIN PV */

/* USER CODE END PV */

/* Private function prototypes -----------------------------------------------*/
void SystemClock_Config(void);
static void MX_GPIO_Init(void);
static void MX_TIM1_Init(void);
static void MX_TIM7_Init(void);
static void MX_TIM4_Init(void);
void StartTaskFlow(void *argument);
void StartTaskGPIO(void *argument);
void StartTaskIAIX(void *argument);
void StartTaskCOM(void *argument);
void StartTaskIAIY(void *argument);
void StartTaskIAIZ(void *argument);
void StartTaskIAI(void *argument);

/* USER CODE BEGIN PFP */

/* USER CODE END PFP */

/* Private user code ---------------------------------------------------------*/
/* USER CODE BEGIN 0 */

/* USER CODE END 0 */

/**
  * @brief  The application entry point.
  * @retval int
  */
int main(void)
{

  /* USER CODE BEGIN 1 */

  /* USER CODE END 1 */

  /* MCU Configuration--------------------------------------------------------*/

  /* Reset of all peripherals, Initializes the Flash interface and the Systick. */
  HAL_Init();

  /* USER CODE BEGIN Init */

  /* USER CODE END Init */

  /* Configure the system clock */
  SystemClock_Config();

  /* USER CODE BEGIN SysInit */

  /* USER CODE END SysInit */

  /* Initialize all configured peripherals */
  MX_GPIO_Init();
  MX_TIM1_Init();
  MX_TIM7_Init();
  MX_TIM4_Init();
  /* USER CODE BEGIN 2 */

  /* USER CODE END 2 */

  /* Init scheduler */
  osKernelInitialize();

  /* USER CODE BEGIN RTOS_MUTEX */
  /* add mutexes, ... */
  /* USER CODE END RTOS_MUTEX */

  /* USER CODE BEGIN RTOS_SEMAPHORES */
  /* add semaphores, ... */
  /* USER CODE END RTOS_SEMAPHORES */

  /* USER CODE BEGIN RTOS_TIMERS */
  /* start timers, add new ones, ... */
  MX_USB_DEVICE_Init();
  MX_TIM1_Init();
  MX_TIM4_Init();
  MX_TIM7_Init();
  HAL_TIM_PWM_Start(&htim1, TIM_CHANNEL_1);
  HAL_TIM_Base_Start(&htim4);
  HAL_TIM_Base_Start(&htim7);

  /* USER CODE END RTOS_TIMERS */

  /* USER CODE BEGIN RTOS_QUEUES */
  stepIAI = STEP_IAI_WAIT;
  machineMode = EQ_MODE_INIT;
  isStopIAI = true;
  HAL_GPIO_WritePin(USB_OTG_FS_VID_GPIO_Port, USB_OTG_FS_VID_Pin, GPIO_PIN_SET);
  vTaskDelay(pdMS_TO_TICKS(300));
  /* USER CODE END RTOS_QUEUES */

  /* Create the thread(s) */
  /* creation of mTaskFlow */
  mTaskFlowHandle = osThreadNew(StartTaskFlow, NULL, &mTaskFlow_attributes);

  /* creation of mTaskGPIO */
  mTaskGPIOHandle = osThreadNew(StartTaskGPIO, NULL, &mTaskGPIO_attributes);

  /* creation of mTaskIAIX */
  mTaskIAIXHandle = osThreadNew(StartTaskIAIX, NULL, &mTaskIAIX_attributes);

  /* creation of myTaskCOM */
  myTaskCOMHandle = osThreadNew(StartTaskCOM, NULL, &myTaskCOM_attributes);

  /* creation of mTaskIAIY */
  mTaskIAIYHandle = osThreadNew(StartTaskIAIY, NULL, &mTaskIAIY_attributes);

  /* creation of mTaskIAIZ */
  mTaskIAIZHandle = osThreadNew(StartTaskIAIZ, NULL, &mTaskIAIZ_attributes);

  /* creation of mTaskIAI */
  mTaskIAIHandle = osThreadNew(StartTaskIAI, NULL, &mTaskIAI_attributes);

  /* USER CODE BEGIN RTOS_THREADS */
  /* add threads, ... */
  /* USER CODE END RTOS_THREADS */

  /* USER CODE BEGIN RTOS_EVENTS */
  /* add events, ... */
  /* USER CODE END RTOS_EVENTS */

  /* Start scheduler */
  osKernelStart();

  /* We should never get here as control is now taken by the scheduler */

  /* Infinite loop */
  /* USER CODE BEGIN WHILE */
  while (1)
  {
    /* USER CODE END WHILE */

    /* USER CODE BEGIN 3 */
  }
  /* USER CODE END 3 */
}

/**
  * @brief System Clock Configuration
  * @retval None
  */
void SystemClock_Config(void)
{
  RCC_OscInitTypeDef RCC_OscInitStruct = {0};
  RCC_ClkInitTypeDef RCC_ClkInitStruct = {0};

  /** Configure the main internal regulator output voltage
  */
  __HAL_RCC_PWR_CLK_ENABLE();
  __HAL_PWR_VOLTAGESCALING_CONFIG(PWR_REGULATOR_VOLTAGE_SCALE1);

  /** Initializes the RCC Oscillators according to the specified parameters
  * in the RCC_OscInitTypeDef structure.
  */
  RCC_OscInitStruct.OscillatorType = RCC_OSCILLATORTYPE_HSE;
  RCC_OscInitStruct.HSEState = RCC_HSE_ON;
  RCC_OscInitStruct.PLL.PLLState = RCC_PLL_ON;
  RCC_OscInitStruct.PLL.PLLSource = RCC_PLLSOURCE_HSE;
  RCC_OscInitStruct.PLL.PLLM = 4;
  RCC_OscInitStruct.PLL.PLLN = 168;
  RCC_OscInitStruct.PLL.PLLP = RCC_PLLP_DIV2;
  RCC_OscInitStruct.PLL.PLLQ = 7;
  if (HAL_RCC_OscConfig(&RCC_OscInitStruct) != HAL_OK)
  {
    Error_Handler();
  }

  /** Initializes the CPU, AHB and APB buses clocks
  */
  RCC_ClkInitStruct.ClockType = RCC_CLOCKTYPE_HCLK|RCC_CLOCKTYPE_SYSCLK
                              |RCC_CLOCKTYPE_PCLK1|RCC_CLOCKTYPE_PCLK2;
  RCC_ClkInitStruct.SYSCLKSource = RCC_SYSCLKSOURCE_PLLCLK;
  RCC_ClkInitStruct.AHBCLKDivider = RCC_SYSCLK_DIV1;
  RCC_ClkInitStruct.APB1CLKDivider = RCC_HCLK_DIV4;
  RCC_ClkInitStruct.APB2CLKDivider = RCC_HCLK_DIV2;

  if (HAL_RCC_ClockConfig(&RCC_ClkInitStruct, FLASH_LATENCY_5) != HAL_OK)
  {
    Error_Handler();
  }
}

/**
  * @brief TIM1 Initialization Function
  * @param None
  * @retval None
  */
static void MX_TIM1_Init(void)
{

  /* USER CODE BEGIN TIM1_Init 0 */

  /* USER CODE END TIM1_Init 0 */

  TIM_ClockConfigTypeDef sClockSourceConfig = {0};
  TIM_MasterConfigTypeDef sMasterConfig = {0};
  TIM_OC_InitTypeDef sConfigOC = {0};
  TIM_BreakDeadTimeConfigTypeDef sBreakDeadTimeConfig = {0};

  /* USER CODE BEGIN TIM1_Init 1 */

  /* USER CODE END TIM1_Init 1 */
  htim1.Instance = TIM1;
  htim1.Init.Prescaler = 8;
  htim1.Init.CounterMode = TIM_COUNTERMODE_UP;
  htim1.Init.Period = 499;
  htim1.Init.ClockDivision = TIM_CLOCKDIVISION_DIV1;
  htim1.Init.RepetitionCounter = 0;
  htim1.Init.AutoReloadPreload = TIM_AUTORELOAD_PRELOAD_DISABLE;
  if (HAL_TIM_Base_Init(&htim1) != HAL_OK)
  {
    Error_Handler();
  }
  sClockSourceConfig.ClockSource = TIM_CLOCKSOURCE_INTERNAL;
  if (HAL_TIM_ConfigClockSource(&htim1, &sClockSourceConfig) != HAL_OK)
  {
    Error_Handler();
  }
  if (HAL_TIM_PWM_Init(&htim1) != HAL_OK)
  {
    Error_Handler();
  }
  sMasterConfig.MasterOutputTrigger = TIM_TRGO_RESET;
  sMasterConfig.MasterSlaveMode = TIM_MASTERSLAVEMODE_DISABLE;
  if (HAL_TIMEx_MasterConfigSynchronization(&htim1, &sMasterConfig) != HAL_OK)
  {
    Error_Handler();
  }
  sConfigOC.OCMode = TIM_OCMODE_PWM1;
  sConfigOC.Pulse = currentLightValue;
  sConfigOC.OCPolarity = TIM_OCPOLARITY_HIGH;
  sConfigOC.OCNPolarity = TIM_OCNPOLARITY_HIGH;
  sConfigOC.OCFastMode = TIM_OCFAST_DISABLE;
  sConfigOC.OCIdleState = TIM_OCIDLESTATE_RESET;
  sConfigOC.OCNIdleState = TIM_OCNIDLESTATE_RESET;
  if (HAL_TIM_PWM_ConfigChannel(&htim1, &sConfigOC, TIM_CHANNEL_1) != HAL_OK)
  {
    Error_Handler();
  }
  sBreakDeadTimeConfig.OffStateRunMode = TIM_OSSR_DISABLE;
  sBreakDeadTimeConfig.OffStateIDLEMode = TIM_OSSI_DISABLE;
  sBreakDeadTimeConfig.LockLevel = TIM_LOCKLEVEL_OFF;
  sBreakDeadTimeConfig.DeadTime = 0;
  sBreakDeadTimeConfig.BreakState = TIM_BREAK_DISABLE;
  sBreakDeadTimeConfig.BreakPolarity = TIM_BREAKPOLARITY_HIGH;
  sBreakDeadTimeConfig.AutomaticOutput = TIM_AUTOMATICOUTPUT_DISABLE;
  if (HAL_TIMEx_ConfigBreakDeadTime(&htim1, &sBreakDeadTimeConfig) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN TIM1_Init 2 */

  /* USER CODE END TIM1_Init 2 */
  HAL_TIM_MspPostInit(&htim1);

}

/**
  * @brief TIM4 Initialization Function
  * @param None
  * @retval None
  */
static void MX_TIM4_Init(void)
{

  /* USER CODE BEGIN TIM4_Init 0 */

  /* USER CODE END TIM4_Init 0 */

  TIM_ClockConfigTypeDef sClockSourceConfig = {0};
  TIM_MasterConfigTypeDef sMasterConfig = {0};

  /* USER CODE BEGIN TIM4_Init 1 */

  /* USER CODE END TIM4_Init 1 */
  htim4.Instance = TIM4;
  htim4.Init.Prescaler = 0;
  htim4.Init.CounterMode = TIM_COUNTERMODE_UP;
  htim4.Init.Period = 65535;
  htim4.Init.ClockDivision = TIM_CLOCKDIVISION_DIV1;
  htim4.Init.AutoReloadPreload = TIM_AUTORELOAD_PRELOAD_DISABLE;
  if (HAL_TIM_Base_Init(&htim4) != HAL_OK)
  {
    Error_Handler();
  }
  sClockSourceConfig.ClockSource = TIM_CLOCKSOURCE_INTERNAL;
  if (HAL_TIM_ConfigClockSource(&htim4, &sClockSourceConfig) != HAL_OK)
  {
    Error_Handler();
  }
  sMasterConfig.MasterOutputTrigger = TIM_TRGO_RESET;
  sMasterConfig.MasterSlaveMode = TIM_MASTERSLAVEMODE_DISABLE;
  if (HAL_TIMEx_MasterConfigSynchronization(&htim4, &sMasterConfig) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN TIM4_Init 2 */

  /* USER CODE END TIM4_Init 2 */

}

/**
  * @brief TIM7 Initialization Function
  * @param None
  * @retval None
  */
static void MX_TIM7_Init(void)
{

  /* USER CODE BEGIN TIM7_Init 0 */

  /* USER CODE END TIM7_Init 0 */

  TIM_MasterConfigTypeDef sMasterConfig = {0};

  /* USER CODE BEGIN TIM7_Init 1 */

  /* USER CODE END TIM7_Init 1 */
  htim7.Instance = TIM7;
  htim7.Init.Prescaler = 0;
  htim7.Init.CounterMode = TIM_COUNTERMODE_UP;
  htim7.Init.Period = 65535;
  htim7.Init.AutoReloadPreload = TIM_AUTORELOAD_PRELOAD_DISABLE;
  if (HAL_TIM_Base_Init(&htim7) != HAL_OK)
  {
    Error_Handler();
  }
  sMasterConfig.MasterOutputTrigger = TIM_TRGO_RESET;
  sMasterConfig.MasterSlaveMode = TIM_MASTERSLAVEMODE_DISABLE;
  if (HAL_TIMEx_MasterConfigSynchronization(&htim7, &sMasterConfig) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN TIM7_Init 2 */

  /* USER CODE END TIM7_Init 2 */

}

/**
  * @brief GPIO Initialization Function
  * @param None
  * @retval None
  */
static void MX_GPIO_Init(void)
{
  GPIO_InitTypeDef GPIO_InitStruct = {0};
  /* USER CODE BEGIN MX_GPIO_Init_1 */

  /* USER CODE END MX_GPIO_Init_1 */

  /* GPIO Ports Clock Enable */
  __HAL_RCC_GPIOE_CLK_ENABLE();
  __HAL_RCC_GPIOI_CLK_ENABLE();
  __HAL_RCC_GPIOC_CLK_ENABLE();
  __HAL_RCC_GPIOF_CLK_ENABLE();
  __HAL_RCC_GPIOH_CLK_ENABLE();
  __HAL_RCC_GPIOA_CLK_ENABLE();
  __HAL_RCC_GPIOB_CLK_ENABLE();
  __HAL_RCC_GPIOG_CLK_ENABLE();
  __HAL_RCC_GPIOD_CLK_ENABLE();

  /*Configure GPIO pin Output Level */
  HAL_GPIO_WritePin(GPIO_OUT_Z_PC1_GPIO_Port, GPIO_OUT_Z_PC1_Pin, GPIO_PIN_RESET);

  /*Configure GPIO pin Output Level */
  HAL_GPIO_WritePin(GPIOB, GPIO_OUT_Z_PC2_Pin|GPIO_OUT_Z_PC4_Pin|GPIO_OUT_X_PC32_Pin|GPIO_OUT_X_PC64_Pin
                          |GPIO_OUT_Y_PC1_Pin|GPIO_OUT_Y_PC2_Pin|GPIO_OUT_Y_PC4_Pin|GPIO_OUT_Y_PC8_Pin, GPIO_PIN_RESET);

  /*Configure GPIO pin Output Level */
  HAL_GPIO_WritePin(GPIOF, GPIO_OUT_Z_PC8_Pin|GPIO_OUT_Z_PC16_Pin|GPIO_OUT_Z_PC32_Pin|GPIO_OUT_Z_PC64_Pin
                          |GPIO_OUT_Z_PC128_Pin, GPIO_PIN_RESET);

  /*Configure GPIO pin Output Level */
  HAL_GPIO_WritePin(GPIOG, GPIO_OUT_Z_BKRL_Pin|GPIO_OUT_Z_HOME_Pin|GPIO_OUT_Y_RES_Pin|GPIO_OUT_Y_SON_Pin
                          |GPIO_OUT_LIGHT_BLUE_Pin|GPIO_OUT_LIGHT_RED_Pin|GPIO_OUT_LIGHT_YELLOW_Pin|GPIO_OUT_BUZZER_Pin
                          |GPIO_OUT_LIGHT_RESET_Pin , GPIO_PIN_RESET);

  /*Configure GPIO pin Output Level */
  HAL_GPIO_WritePin(GPIOE, GPIO_OUT_Z_STP_Pin|GPIO_OUT_Z_CSTR_Pin|GPIO_OUT_Z_RES_Pin|GPIO_OUT_Z_SON_Pin
                          |GPIO_OUT_X_PC1_Pin|GPIO_OUT_X_PC2_Pin|GPIO_OUT_X_PC4_Pin|GPIO_OUT_X_PC8_Pin
                          |GPIO_OUT_X_PC16_Pin, GPIO_PIN_RESET);

  /*Configure GPIO pin Output Level */
  HAL_GPIO_WritePin(GPIOH, GPIO_OUT_X_PC128_Pin|GPIO_OUT_X_BKRL_Pin|GPIO_OUT_X_HOME_Pin|GPIO_OUT_X_STP_Pin
                          |GPIO_OUT_X_CSTR_Pin|GPIO_OUT_X_RES_Pin|GPIO_OUT_X_SON_Pin, GPIO_PIN_RESET);

  /*Configure GPIO pin Output Level */
  HAL_GPIO_WritePin(GPIOD, GPIO_OUT_Y_PC16_Pin|GPIO_OUT_Y_PC32_Pin|GPIO_OUT_Y_PC64_Pin|GPIO_OUT_Y_PC128_Pin
                          |GPIO_OUT_Y_BKRL_Pin|GPIO_OUT_Y_HOME_Pin|GPIO_OUT_Y_STP_Pin|GPIO_OUT_Y_CSTR_Pin, GPIO_PIN_RESET);

  /*Configure GPIO pin Output Level */
  HAL_GPIO_WritePin(USB_OTG_FS_VID_GPIO_Port, USB_OTG_FS_VID_Pin, GPIO_PIN_RESET);

  /*Configure GPIO pins : GPIO_IN_Z_HEND_Pin GPIO_IN_Z_PEND_Pin GPIO_IN_Z_SV_Pin GPIO_IN_Z_ALM_Pin
                           GPIO_IN_Y_PM1_Pin GPIO_IN_Z_PM4_Pin GPIO_IN_Z_PM8_Pin */
  GPIO_InitStruct.Pin = GPIO_IN_Z_HEND_Pin|GPIO_IN_Z_PEND_Pin|GPIO_IN_Z_SV_Pin|GPIO_IN_Z_ALM_Pin
                          |GPIO_IN_Y_PM1_Pin|GPIO_IN_Z_PM4_Pin|GPIO_IN_Z_PM8_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_INPUT;
  GPIO_InitStruct.Pull = GPIO_PULLUP;
  HAL_GPIO_Init(GPIOE, &GPIO_InitStruct);

  /*Configure GPIO pins : GPIO_IN_Y_PM2_Pin GPIO_IN_Y_PM8_Pin GPIO_IN_Y_PM16_Pin GPIO_IN_Y_PM32_Pin
                           GPIO_IN_Z_PM16_Pin GPIO_IN_Z_PM32_Pin GPIO_IN_Z_PM64_Pin GPIO_IN_Z_PM128_Pin */
  GPIO_InitStruct.Pin = GPIO_IN_Y_PM2_Pin|GPIO_IN_Y_PM8_Pin|GPIO_IN_Y_PM16_Pin|GPIO_IN_Y_PM32_Pin
                          |GPIO_IN_Z_PM16_Pin|GPIO_IN_Z_PM32_Pin|GPIO_IN_Z_PM64_Pin|GPIO_IN_Z_PM128_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_INPUT;
  GPIO_InitStruct.Pull = GPIO_PULLUP;
  HAL_GPIO_Init(GPIOI, &GPIO_InitStruct);

  /*Configure GPIO pins : GPIO_IN_Y_PM4_Pin GPIO_IN_X_PM32_Pin GPIO_IN_X_PM64_Pin GPIO_IN_X_PM128_Pin
                           GPIO_IN_X_HEND_Pin USB_OTG_FS_VBUS_Pin */
  GPIO_InitStruct.Pin = GPIO_IN_Y_PM4_Pin|GPIO_IN_X_PM32_Pin|GPIO_IN_X_PM64_Pin|GPIO_IN_X_PM128_Pin
                          |GPIO_IN_X_HEND_Pin|USB_OTG_FS_VBUS_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_INPUT;
  GPIO_InitStruct.Pull = GPIO_PULLUP;
  HAL_GPIO_Init(GPIOC, &GPIO_InitStruct);

  /*Configure GPIO pins : GPIO_IN_Y_PM64_Pin GPIO_IN_Y_PM128_Pin GPIO_IN_Y_HEND_Pin GPIO_IN_Y_PEND_Pin
                           GPIO_IN_Y_SV_Pin GPIO_IN_Y_ALM_Pin GPIO_IN_X_PM1_Pin GPIO_IN_X_PM2_Pin
                           GPIO_IN_X_PM4_Pin GPIO_IN_X_PM8_Pin GPIO_IN_X_PM16_Pin */
  GPIO_InitStruct.Pin = GPIO_IN_Y_PM64_Pin|GPIO_IN_Y_PM128_Pin|GPIO_IN_Y_HEND_Pin|GPIO_IN_Y_PEND_Pin
                          |GPIO_IN_Y_SV_Pin|GPIO_IN_Y_ALM_Pin|GPIO_IN_X_PM1_Pin|GPIO_IN_X_PM2_Pin
                          |GPIO_IN_X_PM4_Pin|GPIO_IN_X_PM8_Pin|GPIO_IN_X_PM16_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_INPUT;
  GPIO_InitStruct.Pull = GPIO_PULLUP;
  HAL_GPIO_Init(GPIOF, &GPIO_InitStruct);

  /*Configure GPIO pin : GPIO_IN_X_PEND_Pin */
  GPIO_InitStruct.Pin = GPIO_IN_X_PEND_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_INPUT;
  GPIO_InitStruct.Pull = GPIO_PULLUP;
  HAL_GPIO_Init(GPIO_IN_X_PEND_GPIO_Port, &GPIO_InitStruct);

  /*Configure GPIO pins : GPIO_IN_X_SV_Pin GPIO_IN_X_ALM_Pin */
  GPIO_InitStruct.Pin = GPIO_IN_X_SV_Pin|GPIO_IN_X_ALM_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_INPUT;
  GPIO_InitStruct.Pull = GPIO_PULLUP;
  HAL_GPIO_Init(GPIOH, &GPIO_InitStruct);

  /*Configure GPIO pin : GPIO_OUT_Z_PC1_Pin */
  GPIO_InitStruct.Pin = GPIO_OUT_Z_PC1_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
  GPIO_InitStruct.Pull = GPIO_PULLDOWN;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_MEDIUM;
  HAL_GPIO_Init(GPIO_OUT_Z_PC1_GPIO_Port, &GPIO_InitStruct);

  /*Configure GPIO pins : GPIO_OUT_Z_PC2_Pin GPIO_OUT_Z_PC4_Pin GPIO_OUT_X_PC32_Pin GPIO_OUT_X_PC64_Pin
                           GPIO_OUT_Y_PC1_Pin GPIO_OUT_Y_PC2_Pin GPIO_OUT_Y_PC4_Pin GPIO_OUT_Y_PC8_Pin */
  GPIO_InitStruct.Pin = GPIO_OUT_Z_PC2_Pin|GPIO_OUT_Z_PC4_Pin|GPIO_OUT_X_PC32_Pin|GPIO_OUT_X_PC64_Pin
                          |GPIO_OUT_Y_PC1_Pin|GPIO_OUT_Y_PC2_Pin|GPIO_OUT_Y_PC4_Pin|GPIO_OUT_Y_PC8_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
  GPIO_InitStruct.Pull = GPIO_PULLDOWN;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_MEDIUM;
  HAL_GPIO_Init(GPIOB, &GPIO_InitStruct);

  /*Configure GPIO pins : GPIO_OUT_Z_PC8_Pin GPIO_OUT_Z_PC16_Pin GPIO_OUT_Z_PC32_Pin GPIO_OUT_Z_PC64_Pin
                           GPIO_OUT_Z_PC128_Pin */
  GPIO_InitStruct.Pin = GPIO_OUT_Z_PC8_Pin|GPIO_OUT_Z_PC16_Pin|GPIO_OUT_Z_PC32_Pin|GPIO_OUT_Z_PC64_Pin
                          |GPIO_OUT_Z_PC128_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
  GPIO_InitStruct.Pull = GPIO_PULLDOWN;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_MEDIUM;
  HAL_GPIO_Init(GPIOF, &GPIO_InitStruct);

  /*Configure GPIO pins : GPIO_OUT_Z_BKRL_Pin GPIO_OUT_Z_HOME_Pin GPIO_OUT_Y_RES_Pin GPIO_OUT_Y_SON_Pin */
  GPIO_InitStruct.Pin = GPIO_OUT_Z_BKRL_Pin|GPIO_OUT_Z_HOME_Pin|GPIO_OUT_Y_RES_Pin|GPIO_OUT_Y_SON_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
  GPIO_InitStruct.Pull = GPIO_PULLDOWN;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_MEDIUM;
  HAL_GPIO_Init(GPIOG, &GPIO_InitStruct);

  /*Configure GPIO pins : GPIO_OUT_Z_STP_Pin GPIO_OUT_Z_CSTR_Pin GPIO_OUT_Z_RES_Pin GPIO_OUT_Z_SON_Pin
                           GPIO_OUT_X_PC1_Pin GPIO_OUT_X_PC2_Pin GPIO_OUT_X_PC4_Pin GPIO_OUT_X_PC8_Pin
                           GPIO_OUT_X_PC16_Pin */
  GPIO_InitStruct.Pin = GPIO_OUT_Z_STP_Pin|GPIO_OUT_Z_CSTR_Pin|GPIO_OUT_Z_RES_Pin|GPIO_OUT_Z_SON_Pin
                          |GPIO_OUT_X_PC1_Pin|GPIO_OUT_X_PC2_Pin|GPIO_OUT_X_PC4_Pin|GPIO_OUT_X_PC8_Pin
                          |GPIO_OUT_X_PC16_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
  GPIO_InitStruct.Pull = GPIO_PULLDOWN;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_MEDIUM;
  HAL_GPIO_Init(GPIOE, &GPIO_InitStruct);

  /*Configure GPIO pins : GPIO_OUT_X_PC128_Pin GPIO_OUT_X_BKRL_Pin GPIO_OUT_X_HOME_Pin GPIO_OUT_X_STP_Pin
                           GPIO_OUT_X_CSTR_Pin GPIO_OUT_X_RES_Pin GPIO_OUT_X_SON_Pin */
  GPIO_InitStruct.Pin = GPIO_OUT_X_PC128_Pin|GPIO_OUT_X_BKRL_Pin|GPIO_OUT_X_HOME_Pin|GPIO_OUT_X_STP_Pin
                          |GPIO_OUT_X_CSTR_Pin|GPIO_OUT_X_RES_Pin|GPIO_OUT_X_SON_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
  GPIO_InitStruct.Pull = GPIO_PULLDOWN;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_MEDIUM;
  HAL_GPIO_Init(GPIOH, &GPIO_InitStruct);

  /*Configure GPIO pins : GPIO_OUT_Y_PC16_Pin GPIO_OUT_Y_PC32_Pin GPIO_OUT_Y_PC64_Pin GPIO_OUT_Y_PC128_Pin
                           GPIO_OUT_Y_BKRL_Pin GPIO_OUT_Y_HOME_Pin GPIO_OUT_Y_STP_Pin GPIO_OUT_Y_CSTR_Pin */
  GPIO_InitStruct.Pin = GPIO_OUT_Y_PC16_Pin|GPIO_OUT_Y_PC32_Pin|GPIO_OUT_Y_PC64_Pin|GPIO_OUT_Y_PC128_Pin
                          |GPIO_OUT_Y_BKRL_Pin|GPIO_OUT_Y_HOME_Pin|GPIO_OUT_Y_STP_Pin|GPIO_OUT_Y_CSTR_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
  GPIO_InitStruct.Pull = GPIO_PULLDOWN;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_MEDIUM;
  HAL_GPIO_Init(GPIOD, &GPIO_InitStruct);

  /*Configure GPIO pins : GPIO_OUT_LIGHT_BLUE_Pin GPIO_OUT_LIGHT_RED_Pin GPIO_OUT_LIGHT_YELLOW_Pin GPIO_OUT_BUZZER_Pin
                           GPIO_OUT_LIGHT_RESET_Pin */
  GPIO_InitStruct.Pin = GPIO_OUT_LIGHT_BLUE_Pin|GPIO_OUT_LIGHT_RED_Pin|GPIO_OUT_LIGHT_YELLOW_Pin|GPIO_OUT_BUZZER_Pin
                          |GPIO_OUT_LIGHT_RESET_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
  GPIO_InitStruct.Pull = GPIO_PULLDOWN;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
  HAL_GPIO_Init(GPIOG, &GPIO_InitStruct);

  /*Configure GPIO pin : USB_OTG_FS_VID_Pin */
  GPIO_InitStruct.Pin = USB_OTG_FS_VID_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
  GPIO_InitStruct.Pull = GPIO_PULLDOWN;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
  HAL_GPIO_Init(USB_OTG_FS_VID_GPIO_Port, &GPIO_InitStruct);

  /*Configure GPIO pins : GPIO_IN_SW_RESET_Pin GPIO_IN_SW_STOP_Pin GPIO_IN_SS_LEFT_Pin GPIO_IN_SS_RIGHT_Pin */
  GPIO_InitStruct.Pin = GPIO_IN_SW_RESET_Pin|GPIO_IN_SW_STOP_Pin|GPIO_IN_SS_LEFT_Pin|GPIO_IN_SS_RIGHT_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_INPUT;
  GPIO_InitStruct.Pull = GPIO_PULLUP;
  HAL_GPIO_Init(GPIOD, &GPIO_InitStruct);

  /*Configure GPIO pin : GPIO_IN_SS_SAFE_Pin */
  GPIO_InitStruct.Pin = GPIO_IN_SS_SAFE_Pin | GPIO_IN_SW_START_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_INPUT;
  GPIO_InitStruct.Pull = GPIO_PULLUP;
  HAL_GPIO_Init(GPIOG, &GPIO_InitStruct);

  /*Configure GPIO pins : GPIO_IN_Z_PM1_Pin GPIO_IN_Z_PM2_Pin */
  GPIO_InitStruct.Pin = GPIO_IN_Z_PM1_Pin|GPIO_IN_Z_PM2_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_INPUT;
  GPIO_InitStruct.Pull = GPIO_PULLUP;
  HAL_GPIO_Init(GPIOB, &GPIO_InitStruct);

  /* USER CODE BEGIN MX_GPIO_Init_2 */

  /* USER CODE END MX_GPIO_Init_2 */
}

/* USER CODE BEGIN 4 */

/* USER CODE END 4 */

/* USER CODE BEGIN Header_StartTaskFlow */
/**
  * @brief  Function implementing the mTaskFlow thread.
  * @param  argument: Not used
  * @retval None
  */
/* USER CODE END Header_StartTaskFlow */
void StartTaskFlow(void *argument)
{
  /* init code for USB_DEVICE */
  MX_USB_DEVICE_Init();
  /* USER CODE BEGIN 5 */
  /* Infinite loop */
  for(;;)
  {
	eqHandleStatus();
	eqControl();
    osDelay(1);
  }
  /* USER CODE END 5 */
}

/* USER CODE BEGIN Header_StartTaskGPIO */
/**
* @brief Function implementing the mTaskGPIO thread.
* @param argument: Not used
* @retval None
*/
/* USER CODE END Header_StartTaskGPIO */
void StartTaskGPIO(void *argument)
{
  /* USER CODE BEGIN StartTaskGPIO */
  /* Infinite loop */
  for(;;)
  {
	gpioScan();

    osDelay(1);
  }
  /* USER CODE END StartTaskGPIO */
}

/* USER CODE BEGIN Header_StartTaskIAIX */
/**
* @brief Function implementing the mTaskIAIX thread.
* @param argument: Not used
* @retval None
*/
/* USER CODE END Header_StartTaskIAIX */
void StartTaskIAIX(void *argument)
{
  /* USER CODE BEGIN StartTaskIAIX */
  /* Infinite loop */
  for(;;)
  {
	if(axisX.request.REQ_PREPARE){
		axisX.prepare(&axisX);
	}else if(axisX.request.REQ_MOVE){
		axisX.move(&axisX,axisX.position.targetPos.toPos);
	}else if (axisX.request.REQ_ORG){
		axisX.home(&axisX);
	}else if(axisX.request.REQ_RESET){
		axisX.clearError(&axisX);
	}
    osDelay(1);
  }
  /* USER CODE END StartTaskIAIX */
}

/* USER CODE BEGIN Header_StartTaskCOM */
/**
* @brief Function implementing the myTaskCOM thread.
* @param argument: Not used
* @retval None
*/
/* USER CODE END Header_StartTaskCOM */
void StartTaskCOM(void *argument)
{
  /* USER CODE BEGIN StartTaskCOM */
  /* Infinite loop */
  for(;;)
  {
	  //Z : Max 12
	  //X : Max 110
	  //Y : Max 75
	  getCmdHandle();
	  sendCmdHandle();
	  osDelay(30);

//	  char msg[512];
//	  int len = 0;
//
//	  len += snprintf(msg + len, sizeof(msg) - len, "IAIX Stack Free: %lu\n", uxTaskGetStackHighWaterMark(mTaskIAIXHandle));
//	  len += snprintf(msg + len, sizeof(msg) - len, "IAIY Stack Free: %lu\n", uxTaskGetStackHighWaterMark(mTaskIAIYHandle));
//	  len += snprintf(msg + len, sizeof(msg) - len, "IAIZ Stack Free: %lu\n", uxTaskGetStackHighWaterMark(mTaskIAIZHandle));
//	  len += snprintf(msg + len, sizeof(msg) - len, "IAI Stack Free: %lu\n",  uxTaskGetStackHighWaterMark(mTaskIAIHandle));
//	  len += snprintf(msg + len, sizeof(msg) - len, "COM Stack Free: %lu\n",  uxTaskGetStackHighWaterMark(myTaskCOMHandle));
//	  len += snprintf(msg + len, sizeof(msg) - len, "GPIO Stack Free: %lu\n", uxTaskGetStackHighWaterMark(mTaskGPIOHandle));
//	  len += snprintf(msg + len, sizeof(msg) - len, "FLOW Stack Free: %lu\n", uxTaskGetStackHighWaterMark(mTaskFlowHandle));
//
//	  CDC_Transmit_FS((uint8_t*)msg, len);
//	  osDelay(300);
   }
  /* USER CODE END StartTaskCOM */
}

/* USER CODE BEGIN Header_StartTaskIAIY */
/**
* @brief Function implementing the mTaskIAIY thread.
* @param argument: Not used
* @retval None
*/
/* USER CODE END Header_StartTaskIAIY */
void StartTaskIAIY(void *argument)
{
  /* USER CODE BEGIN StartTaskIAIY */
  /* Infinite loop */
  for(;;)
  {
	  if(axisY.request.REQ_PREPARE){
	  	axisY.prepare(&axisY);
	  }else if(axisY.request.REQ_MOVE){
	  	axisY.move(&axisY,axisY.position.targetPos.toPos);
	  }else if (axisY.request.REQ_ORG){
	  	axisY.home(&axisY);
	  }else if(axisY.request.REQ_RESET){
	  	axisY.clearError(&axisY);
	  }
    osDelay(1);

  }
  /* USER CODE END StartTaskIAIY */
}

/* USER CODE BEGIN Header_StartTaskIAIZ */
/**
* @brief Function implementing the mTaskIAIZ thread.
* @param argument: Not used
* @retval None
*/
/* USER CODE END Header_StartTaskIAIZ */
void StartTaskIAIZ(void *argument)
{
  /* USER CODE BEGIN StartTaskIAIZ */
  /* Infinite loop */
  for(;;)
  {
	  if(axisZ.request.REQ_PREPARE){
	  	axisZ.prepare(&axisZ);
	  }else if(axisZ.request.REQ_MOVE){
	  	axisZ.move(&axisZ,axisZ.position.targetPos.toPos);
	  }else if (axisZ.request.REQ_ORG){
	  	axisZ.home(&axisZ);
	  }else if(axisZ.request.REQ_RESET){
	  	axisZ.clearError(&axisZ);
	  }
    osDelay(1);
  }
  /* USER CODE END StartTaskIAIZ */
}

/* USER CODE BEGIN Header_StartTaskIAI */
/**
* @brief Function implementing the mTaskIAI thread.
* @param argument: Not used
* @retval None
*/
/* USER CODE END Header_StartTaskIAI */
void StartTaskIAI(void *argument)
{
  /* USER CODE BEGIN StartTaskIAI */
  /* Infinite loop */
  for(;;)
  {
	IAIMovingHandled();
	if(currentLightValue != targetLightValue){
		currentLightValue = targetLightValue;
		HAL_TIM_PWM_Stop(&htim1, TIM_CHANNEL_1);
		MX_TIM1_Init();
		HAL_TIM_PWM_Start(&htim1, TIM_CHANNEL_1);
	}
    osDelay(1);
  }
  /* USER CODE END StartTaskIAI */
}

/**
  * @brief  This function is executed in case of error occurrence.
  * @retval None
  */
void Error_Handler(void)
{
  /* USER CODE BEGIN Error_Handler_Debug */
  /* User can add his own implementation to report the HAL error return state */
  __disable_irq();
  while (1)
  {
  }
  /* USER CODE END Error_Handler_Debug */
}

#ifdef  USE_FULL_ASSERT
/**
  * @brief  Reports the name of the source file and the source line number
  *         where the assert_param error has occurred.
  * @param  file: pointer to the source file name
  * @param  line: assert_param error line source number
  * @retval None
  */
void assert_failed(uint8_t *file, uint32_t line)
{
  /* USER CODE BEGIN 6 */
  /* User can add his own implementation to report the file name and line number,
     ex: printf("Wrong parameters value: file %s on line %d\r\n", file, line) */
  /* USER CODE END 6 */
}
#endif /* USE_FULL_ASSERT */
