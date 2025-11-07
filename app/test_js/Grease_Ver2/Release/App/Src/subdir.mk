################################################################################
# Automatically-generated file. Do not edit!
# Toolchain: GNU Tools for STM32 (13.3.rel1)
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../App/Src/mErrorHandle.c \
../App/Src/mFlow.c \
../App/Src/mFunction.c \
../App/Src/mGPIO.c \
../App/Src/mIAI.c \
../App/Src/mRS232.c \
../App/Src/mVariable.c 

OBJS += \
./App/Src/mErrorHandle.o \
./App/Src/mFlow.o \
./App/Src/mFunction.o \
./App/Src/mGPIO.o \
./App/Src/mIAI.o \
./App/Src/mRS232.o \
./App/Src/mVariable.o 

C_DEPS += \
./App/Src/mErrorHandle.d \
./App/Src/mFlow.d \
./App/Src/mFunction.d \
./App/Src/mGPIO.d \
./App/Src/mIAI.d \
./App/Src/mRS232.d \
./App/Src/mVariable.d 


# Each subdirectory must supply rules for building sources it contributes
App/Src/%.o App/Src/%.su App/Src/%.cyclo: ../App/Src/%.c App/Src/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m4 -std=gnu11 -DUSE_HAL_DRIVER -DSTM32F407xx -c -I../USB_DEVICE/App -I../App/Inc -I../USB_DEVICE/Target -I../Core/Inc -I../Drivers/STM32F4xx_HAL_Driver/Inc -I../Drivers/STM32F4xx_HAL_Driver/Inc/Legacy -I../Middlewares/ST/STM32_USB_Device_Library/Core/Inc -I../Middlewares/ST/STM32_USB_Device_Library/Class/CDC/Inc -I../Drivers/CMSIS/Device/ST/STM32F4xx/Include -I../Drivers/CMSIS/Include -I../Middlewares/Third_Party/FreeRTOS/Source/include -I../Middlewares/Third_Party/FreeRTOS/Source/CMSIS_RTOS_V2 -I../Middlewares/Third_Party/FreeRTOS/Source/portable/GCC/ARM_CM4F -Os -ffunction-sections -fdata-sections -Wall -fstack-usage -fcyclomatic-complexity -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfpu=fpv4-sp-d16 -mfloat-abi=hard -mthumb -o "$@"

clean: clean-App-2f-Src

clean-App-2f-Src:
	-$(RM) ./App/Src/mErrorHandle.cyclo ./App/Src/mErrorHandle.d ./App/Src/mErrorHandle.o ./App/Src/mErrorHandle.su ./App/Src/mFlow.cyclo ./App/Src/mFlow.d ./App/Src/mFlow.o ./App/Src/mFlow.su ./App/Src/mFunction.cyclo ./App/Src/mFunction.d ./App/Src/mFunction.o ./App/Src/mFunction.su ./App/Src/mGPIO.cyclo ./App/Src/mGPIO.d ./App/Src/mGPIO.o ./App/Src/mGPIO.su ./App/Src/mIAI.cyclo ./App/Src/mIAI.d ./App/Src/mIAI.o ./App/Src/mIAI.su ./App/Src/mRS232.cyclo ./App/Src/mRS232.d ./App/Src/mRS232.o ./App/Src/mRS232.su ./App/Src/mVariable.cyclo ./App/Src/mVariable.d ./App/Src/mVariable.o ./App/Src/mVariable.su

.PHONY: clean-App-2f-Src

