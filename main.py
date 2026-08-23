# test.py STM32F103C8T6 Register Parser | Core/Peripheral Dual Input + 32-bit Manual Bit Checkboxes
import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                             QLineEdit, QPushButton, QTextEdit, QLabel, QCompleter, QTableWidget, QTableWidgetItem, QCheckBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

# ====================== Cortex-M3 Core Registers ======================
CORE_CM3_REGS = {
    "STK_CTRL":     0xE000E010,
    "STK_LOAD":     0xE000E014,
    "STK_VAL":      0xE000E018,
    "STK_CALIB":    0xE000E01C,
    "NVIC_ISER0":   0xE000E100,
    "NVIC_ISER1":   0xE000E104,
    "NVIC_ISER2":   0xE000E108,
    "NVIC_ICER0":   0xE000E180,
    "NVIC_ICER1":   0xE000E184,
    "NVIC_ICER2":   0xE000E188,
    "NVIC_ISPR0":   0xE000E200,
    "NVIC_ISPR1":   0xE000E204,
    "NVIC_ISPR2":   0xE000E208,
    "NVIC_ICPR0":   0xE000E280,
    "NVIC_ICPR1":   0xE000E284,
    "NVIC_ICPR2":   0xE000E288,
    "NVIC_IABR0":   0xE000E300,
    "NVIC_IABR1":   0xE000E304,
    "NVIC_IABR2":   0xE000E308,
    "NVIC_IPR0":    0xE000E400,
    "NVIC_IPR1":    0xE000E404,
    "NVIC_IPR2":    0xE000E408,
    "NVIC_IPR3":    0xE000E40C,
    "NVIC_IPR4":    0xE000E410,
    "NVIC_IPR5":    0xE000E414,
    "NVIC_IPR6":    0xE000E418,
    "NVIC_IPR7":    0xE000E41C,
    "SCB_CPUID":    0xE000ED00,
    "SCB_ICSR":     0xE000ED04,
    "SCB_VTOR":     0xE000ED08,
    "SCB_AIRCR":    0xE000ED0C,
    "SCB_SCR":      0xE000ED10,
    "SCB_CCR":      0xE000ED14,
    "SCB_SHPR1":    0xE000ED18,
    "SCB_SHPR2":    0xE000ED1C,
    "SCB_SHPR3":    0xE000ED20,
    "SCB_SHCSR":    0xE000ED24,
    "SCB_CFSR":     0xE000ED28,
    "SCB_HFSR":     0xE000ED2C,
    "SCB_DFSR":     0xE000ED30,
    "SCB_MMFAR":    0xE000ED34,
    "SCB_BFAR":     0xE000ED38,
    "SCB_AFSR":     0xE000ED3C,
    "MPU_TYPE":     0xE000ED90,
    "MPU_CTRL":     0xE000ED94,
    "MPU_RNR":      0xE000ED98,
    "MPU_RBAR":     0xE000ED9C,
    "MPU_RASR":     0xE000EDA0,
}

# ====================== STM32F103C8T6 Peripheral Register Address Map ======================
PERIPH_REGS = {
    "GPIOA_CRL":0x40010800, "GPIOA_CRH":0x40010804, "GPIOA_IDR":0x40010808,
    "GPIOA_ODR":0x4001080C, "GPIOA_BSRR":0x40010810,"GPIOA_BRR":0x40010814,"GPIOA_LCKR":0x40010818,
    "GPIOB_CRL":0x40010C00, "GPIOB_CRH":0x40010C04, "GPIOB_IDR":0x40010C08,
    "GPIOB_ODR":0x40010C0C, "GPIOB_BSRR":0x40010C10,"GPIOB_BRR":0x40010C14,"GPIOB_LCKR":0x40010C18,
    "GPIOC_CRL":0x40011000, "GPIOC_CRH":0x40011004, "GPIOC_IDR":0x40011008,
    "GPIOC_ODR":0x4001100C, "GPIOC_BSRR":0x40011010,"GPIOC_BRR":0x40011014,"GPIOC_LCKR":0x40011018,

    "AFIO_EVCR":0x40010000,"AFIO_MAPR":0x40010004,
    "AFIO_EXTICR1":0x40010008,"AFIO_EXTICR2":0x4001000C,
    "AFIO_EXTICR3":0x40010010,"AFIO_EXTICR4":0x40010014,

    "EXTI_IMR":0x40010400,"EXTI_EMR":0x40010404,"EXTI_RTSR":0x40010408,
    "EXTI_FTSR":0x4001040C,"EXTI_SWIER":0x40010410,"EXTI_PR":0x40010414,

    "RCC_CR":0x40021000,   "RCC_CFGR":0x40021004, "RCC_CIR":0x40021008,
    "RCC_APB2RSTR":0x4002100C,"RCC_APB1RSTR":0x40021010,
    "RCC_AHBENR":0x40021014,  "RCC_APB2ENR":0x40021018,"RCC_APB1ENR":0x4002101C,
    "RCC_BDCR":0x40021020, "RCC_CSR":0x40021024,

    "DMA1_ISR":0x40020000,"DMA1_IFCR":0x40020004,
    "DMA1_CCR1":0x40020008,"DMA1_CNDTR1":0x4002000C,"DMA1_CPAR1":0x40020010,"DMA1_CMAR1":0x40020014,
    "DMA1_CCR2":0x40020018,"DMA1_CNDTR2":0x4002001C,"DMA1_CPAR2":0x40020020,"DMA1_CMAR2":0x40020024,
    "DMA1_CCR3":0x40020028,"DMA1_CNDTR3":0x4002002C,"DMA1_CPAR3":0x40020030,"DMA1_CMAR3":0x40020034,
    "DMA1_CCR4":0x40020038,"DMA1_CNDTR4":0x4002003C,"DMA1_CPAR4":0x40020040,"DMA1_CMAR4":0x40020044,
    "DMA1_CCR5":0x40020048,"DMA1_CNDTR5":0x4002004C,"DMA1_CPAR5":0x40020050,"DMA1_CMAR5":0x40020054,
    "DMA1_CCR6":0x40020058,"DMA1_CNDTR6":0x4002005C,"DMA1_CPAR6":0x40020060,"DMA1_CMAR6":0x40020064,
    "DMA1_CCR7":0x40020068,"DMA1_CNDTR7":0x4002006C,"DMA1_CPAR7":0x40020070,"DMA1_CMAR7":0x40020074,

    "FLASH_ACR":0x40022000,"FLASH_KEYR":0x40022004,"FLASH_OPTKEYR":0x40022008,
    "FLASH_SR":0x4002200C,"FLASH_CR":0x40022010,"FLASH_AR":0x40022014,
    "FLASH_OBR":0x4002201C,"FLASH_WRPR":0x40022020,

    "PWR_CR":0x40007000,"PWR_CSR":0x40007004,
    "BKP_DR1":0x40006C00,"BKP_DR2":0x40006C04,"BKP_DR3":0x40006C08,"BKP_DR4":0x40006C0C,
    "BKP_DR5":0x40006C10,"BKP_DR6":0x40006C14,"BKP_DR7":0x40006C18,"BKP_DR8":0x40006C1C,
    "BKP_DR9":0x40006C20,"BKP_DR10":0x40006C24,"BKP_RTCCR":0x40006C28,"BKP_CR":0x40006C2C,"BKP_CSR":0x40006C30,

    "WWDG_CR":0x40002C00,"WWDG_CFR":0x40002C04,"WWDG_SR":0x40002C08,
    "IWDG_KR":0x40003000,"IWDG_PR":0x40003004,"IWDG_RLR":0x40003008,"IWDG_SR":0x4000300C,

    "TIM1_CR1":0x40012C00,"TIM1_CR2":0x40012C04,"TIM1_SMCR":0x40012C08,"TIM1_DIER":0x40012C0C,
    "TIM1_SR":0x40012C10,"TIM1_EGR":0x40012C14,"TIM1_CCMR1":0x40012C18,"TIM1_CCMR2":0x40012C1C,
    "TIM1_CCER":0x40012C20,"TIM1_CNT":0x40012C24,"TIM1_PSC":0x40012C28,"TIM1_ARR":0x40012C2C,
    "TIM1_RCR":0x40012C30,"TIM1_CCR1":0x40012C34,"TIM1_CCR2":0x40012C38,"TIM1_CCR3":0x40012C3C,"TIM1_CCR4":0x40012C40,
    "TIM1_BDTR":0x40012C44,"TIM1_DCR":0x40012C48,"TIM1_DMAR":0x40012C4C,

    "TIM2_CR1":0x40000000,"TIM2_CR2":0x40000004,"TIM2_SMCR":0x40000008,"TIM2_DIER":0x4000000C,
    "TIM2_SR":0x40000010,"TIM2_EGR":0x40000014,"TIM2_CCMR1":0x40000018,"TIM2_CCMR2":0x4000001C,
    "TIM2_CCER":0x40000020,"TIM2_CNT":0x40000024,"TIM2_PSC":0x40000028,"TIM2_ARR":0x4000002C,
    "TIM2_CCR1":0x40000034,"TIM2_CCR2":0x40000038,"TIM2_CCR3":0x4000003C,"TIM2_CCR4":0x40000040,"TIM2_DCR":0x40000048,"TIM2_DMAR":0x4000004C,

    "TIM3_CR1":0x40000400,"TIM3_CR2":0x40000404,"TIM3_SMCR":0x40000408,"TIM3_DIER":0x4000040C,
    "TIM3_SR":0x40000410,"TIM3_EGR":0x40000414,"TIM3_CCMR1":0x40000418,"TIM3_CCMR2":0x4000041C,
    "TIM3_CCER":0x40000420,"TIM3_CNT":0x40000424,"TIM3_PSC":0x40000428,"TIM3_ARR":0x4000042C,
    "TIM3_CCR1":0x40000434,"TIM3_CCR2":0x40000438,"TIM3_CCR3":0x4000043C,"TIM3_CCR4":0x40000440,"TIM3_DCR":0x40000448,"TIM3_DMAR":0x4000044C,

    "TIM4_CR1":0x40000800,"TIM4_CR2":0x40000804,"TIM4_SMCR":0x40000808,"TIM4_DIER":0x4000080C,
    "TIM4_SR":0x40000810,"TIM4_EGR":0x40000814,"TIM4_CCMR1":0x40000818,"TIM4_CCMR2":0x4000081C,
    "TIM4_CCER":0x40000820,"TIM4_CNT":0x40000824,"TIM4_PSC":0x40000828,"TIM4_ARR":0x4000082C,
    "TIM4_CCR1":0x40000834,"TIM4_CCR2":0x40000838,"TIM4_CCR3":0x4000083C,"TIM4_CCR4":0x40000840,"TIM4_DCR":0x40000848,"TIM4_DMAR":0x4000084C,

    "USART1_SR":0x40013800,"USART1_DR":0x40013804,"USART1_BRR":0x40013808,
    "USART1_CR1":0x4001380C,"USART1_CR2":0x40013810,"USART1_CR3":0x40013814,"USART1_GTPR":0x40013818,
    "USART2_SR":0x40004400,"USART2_DR":0x40004404,"USART2_BRR":0x40004408,
    "USART2_CR1":0x4000440C,"USART2_CR2":0x40004410,"USART2_CR3":0x40004414,"USART2_GTPR":0x40004418,
    "USART3_SR":0x40004800,"USART3_DR":0x40004804,"USART3_BRR":0x40004808,
    "USART3_CR1":0x4000480C,"USART3_CR2":0x40004810,"USART3_CR3":0x40004814,"USART3_GTPR":0x40004818,

    "SPI1_CR1":0x40013000,"SPI1_CR2":0x40013004,"SPI1_SR":0x40013008,"SPI1_DR":0x4001300C,
    "SPI1_CRCPR":0x40013010,"SPI1_RXCRCR":0x40013014,"SPI1_TXCRCR":0x40013018,
    "SPI2_CR1":0x40003800,"SPI2_CR2":0x40003804,"SPI2_SR":0x40003808,"SPI2_DR":0x4000380C,
    "SPI2_CRCPR":0x40003810,"SPI2_RXCRCR":0x40003814,"SPI2_TXCRCR":0x40003818,

    "I2C1_CR1":0x40005400,"I2C1_CR2":0x40005404,"I2C1_OAR1":0x40005408,"I2C1_OAR2":0x4000540C,
    "I2C1_DR":0x40005410,"I2C1_SR1":0x40005414,"I2C1_SR2":0x40005418,"I2C1_CCR":0x4000541C,"I2C1_TRISE":0x40005420,
    "I2C2_CR1":0x40005800,"I2C2_CR2":0x40005804,"I2C2_OAR1":0x40005808,"I2C2_OAR2":0x4000580C,
    "I2C2_DR":0x40005810,"I2C2_SR1":0x40005814,"I2C2_SR2":0x40005818,"I2C2_CCR":0x4000581C,"I2C2_TRISE":0x40005820,

    "ADC1_SR":0x40012400,"ADC1_CR1":0x40012404,"ADC1_CR2":0x40012408,"ADC1_SMPR1":0x4001240C,"ADC1_SMPR2":0x40012410,
    "ADC1_JOFR1":0x40012414,"ADC1_JOFR2":0x40012418,"ADC1_JOFR3":0x4001241C,"ADC1_JOFR4":0x40012420,
    "ADC1_HTR":0x40012424,"ADC1_LTR":0x40012428,"ADC1_SQR1":0x4001242C,"ADC1_SQR2":0x40012430,"ADC1_SQR3":0x40012434,
    "ADC1_JSQR":0x40012438,"ADC1_JDR1":0x4001243C,"ADC1_JDR2":0x40012440,"ADC1_JDR3":0x40012444,"ADC1_JDR4":0x40012448,"ADC1_DR":0x4001244C,

    "ADC2_SR":0x40012800,"ADC2_CR1":0x40012804,"ADC2_CR2":0x40012808,"ADC2_SMPR1":0x4001280C,"ADC2_SMPR2":0x40012810,
    "ADC2_JOFR1":0x40012814,"ADC2_JOFR2":0x40012818,"ADC2_JOFR3":0x4001281C,"ADC2_JOFR4":0x40012820,
    "ADC2_HTR":0x40012824,"ADC2_LTR":0x40012828,"ADC2_SQR1":0x4001282C,"ADC2_SQR2":0x40012830,"ADC2_SQR3":0x40012834,
    "ADC2_JSQR":0x40012838,"ADC2_JDR1":0x4001283C,"ADC2_JDR2":0x40012840,"ADC2_JDR3":0x40012844,"ADC2_JDR4":0x40012848,"ADC2_DR":0x4001284C,

    "CRC_DR":0x40023000,"CRC_IDR":0x40023004,"CRC_CR":0x40023008,
}

ALL_REGS = {**CORE_CM3_REGS, **PERIPH_REGS}
CORE_NAME_LIST = sorted(CORE_CM3_REGS.keys())
PERIPH_NAME_LIST = sorted(PERIPH_REGS.keys())

# ====================== Bit Field Definitions ======================
REG_BITDEF = {
    # ---------- Peripheral: RCC ----------
    "RCC_CR":[
        (31,31,"PLLRDY","PLL clock ready flag"),(30,30,"PLLON","PLL enable"),
        (25,25,"CSSON","Clock security system enable"),(24,24,"HSEBYP","HSE clock bypass"),
        (23,23,"HSERDY","HSE clock ready flag"),(16,16,"HSEON","HSE clock enable"),
        (11,11,"HSIRDY","HSI clock ready flag"),(8,8,"HSION","HSI clock enable"),
        (7,0,"HSICAL","HSI clock calibration"),
    ],
    "RCC_CFGR":[
        (31,30,"MCO","Microcontroller clock output"),(27,22,"PLLMUL","PLL multiplication factor"),
        (21,21,"PLLXTPRE","HSE divider for PLL entry"),(20,20,"PLLSRC","PLL entry clock source"),
        (19,17,"ADCPRE","ADC prescaler"),(15,14,"PPRE2","APB high-speed prescaler (APB2)"),
        (12,10,"PPRE1","APB low-speed prescaler (APB1)"),(7,4,"HPRE","AHB prescaler"),
        (3,2,"SWS","System clock switch status (read-only)"),(1,0,"SW","System clock switch"),
    ],
    "RCC_APB2ENR":[
        (14,14,"TIM1EN","TIM1 clock enable"),(11,11,"SPI1EN","SPI1 clock enable"),
        (10,10,"USART1EN","USART1 clock enable"),(8,8,"ADC2EN","ADC2 clock enable"),
        (7,7,"ADC1EN","ADC1 clock enable"),(2,2,"IOPCEN","GPIOC clock enable"),
        (1,1,"IOPBEN","GPIOB clock enable"),(0,0,"IOPAEN","GPIOA clock enable"),
    ],
    "RCC_APB1ENR":[
        (23,23,"PWREN","Power interface clock enable"),(21,21,"BKPEN","Backup interface clock enable"),
        (20,20,"I2C2EN","I2C2 clock enable"),(19,19,"I2C1EN","I2C1 clock enable"),
        (14,14,"SPI2EN","SPI2 clock enable"),(4,4,"USART3EN","USART3 clock enable"),
        (3,3,"USART2EN","USART2 clock enable"),(2,2,"TIM4EN","TIM4 clock enable"),
        (1,1,"TIM3EN","TIM3 clock enable"),(0,0,"TIM2EN","TIM2 clock enable"),
    ],
    "RCC_AHBENR":[(2,2,"FLITFEN","FLASH interface clock enable"),(0,0,"DMA1EN","DMA1 clock enable")],

    # ---------- Peripheral: GPIO ----------
    "GPIOA_CRL":[
        (31,30,"MODE3","Port 3 mode"),(29,28,"CNF3","Port 3 configuration"),
        (27,26,"MODE2","Port 2 mode"),(25,24,"CNF2","Port 2 configuration"),
        (23,22,"MODE1","Port 1 mode"),(21,20,"CNF1","Port 1 configuration"),
        (19,18,"MODE0","Port 0 mode"),(17,16,"CNF0","Port 0 configuration"),
        (15,14,"MODE7","Port 7 mode"),(13,12,"CNF7","Port 7 configuration"),
        (11,10,"MODE6","Port 6 mode"),(9,8,"CNF6","Port 6 configuration"),
        (7,6,"MODE5","Port 5 mode"),(5,4,"CNF5","Port 5 configuration"),
        (3,2,"MODE4","Port 4 mode"),(1,0,"CNF4","Port 4 configuration"),
    ],
    "GPIOA_CRH":[
        (31,30,"MODE11","Port 11 mode"),(29,28,"CNF11","Port 11 configuration"),
        (27,26,"MODE10","Port 10 mode"),(25,24,"CNF10","Port 10 configuration"),
        (23,22,"MODE9","Port 9 mode"),(21,20,"CNF9","Port 9 configuration"),
        (19,18,"MODE8","Port 8 mode"),(17,16,"CNF8","Port 8 configuration"),
        (15,14,"MODE15","Port 15 mode"),(13,12,"CNF15","Port 15 configuration"),
        (11,10,"MODE14","Port 14 mode"),(9,8,"CNF14","Port 14 configuration"),
        (7,6,"MODE13","Port 13 mode"),(5,4,"CNF13","Port 13 configuration"),
        (3,2,"MODE12","Port 12 mode"),(1,0,"CNF12","Port 12 configuration"),
    ],
    "GPIOA_IDR":[(15,0,"IDR[15:0]","Port input data (read-only)")],
    "GPIOA_ODR":[(15,0,"ODR[15:0]","Port output data")],
    "GPIOA_BSRR":[(31,16,"BR[15:0]","Port reset bit (write 1 to clear pin)"),(15,0,"BS[15:0]","Port set bit (write 1 to set pin)")],
    "GPIOA_BRR":[(15,0,"BR[15:0]","Port reset bit (write 1 to clear pin)")],
    "GPIOA_LCKR":[(16,16,"LCKKEY","Lock key"),(15,0,"LCK[15:0]","Port lock bits")],

    # ---------- Peripheral: EXTI / AFIO ----------
    "EXTI_IMR":[(19,0,"MRx","Interrupt mask (1 = interrupt enabled)")],
    "EXTI_EMR":[(19,0,"MRx","Event mask (1 = event enabled)")],
    "EXTI_RTSR":[(19,0,"TRx","Rising trigger selection")],
    "EXTI_FTSR":[(19,0,"TRx","Falling trigger selection")],
    "EXTI_SWIER":[(19,0,"SWIERx","Software interrupt event generation")],
    "EXTI_PR":[(19,0,"PRx","Pending bit (write 1 to clear)")],
    "AFIO_MAPR":[
        (26,26,"SWJ_CFG","Serial wire JTAG configuration"),(15,15,"TIM4_REMAP","TIM4 remapping"),
        (14,14,"TIM3_REMAP","TIM3 remapping"),(13,12,"TIM2_REMAP","TIM2 remapping"),
        (11,10,"TIM1_REMAP","TIM1 remapping"),(9,9,"USART3_REMAP","USART3 remapping"),
        (8,8,"USART2_REMAP","USART2 remapping"),(7,7,"USART1_REMAP","USART1 remapping"),
        (6,6,"SPI1_REMAP","SPI1 remapping"),
    ],

    # ---------- Peripheral: USART ----------
    "USART1_CR1":[
        (13,13,"UE","USART enable"),(12,12,"M","Word length (0=8bit, 1=9bit)"),
        (10,10,"PCE","Parity control enable"),(9,9,"PS","Parity selection"),(3,3,"TE","Transmitter enable"),(2,2,"RE","Receiver enable"),
    ],
    "USART1_SR":[
        (7,7,"TXE","Transmit data register empty"),(6,6,"TC","Transmission complete"),
        (5,5,"RXNE","Read data register not empty"),(4,4,"IDLE","IDLE line detected"),
        (3,3,"ORE","Overrun error"),(2,2,"NE","Noise error"),
        (1,1,"FE","Framing error"),(0,0,"PE","Parity error"),
    ],

    # ---------- Peripheral: SPI ----------
    "SPI1_CR1":[
        (15,15,"BIDIMODE","Bidirectional data mode enable"),(11,11,"DFF","Data frame format (0=8bit, 1=16bit)"),
        (9,9,"SSM","Software slave management"),(6,6,"SPE","SPI enable"),(5,3,"BR","Baud rate control"),
        (2,2,"MSTR","Master selection"),(1,1,"CPOL","Clock polarity"),(0,0,"CPHA","Clock phase"),
    ],
    "SPI1_SR":[(7,7,"BSY","Busy flag"),(6,6,"OVR","Overrun flag"),(1,1,"TXE","Transmit buffer empty"),(0,0,"RXNE","Receive buffer not empty")],

    # ---------- Peripheral: I2C ----------
    "I2C1_CR1":[
        (15,15,"SWRST","Software reset"),(10,10,"ENGC","General call enable"),
        (8,8,"PEC","PEC enable"),(6,6,"ACK","Acknowledge enable"),(0,0,"PE","Peripheral enable"),
    ],
    "I2C1_CR2":[(7,6,"LAST","DMA last transfer"),(5,5,"DMAEN","DMA requests enable"),(2,0,"FREQ","Peripheral clock frequency")],

    # ---------- Peripheral: TIM ----------
    "TIM2_CR1":[
        (10,10,"ARPE","Auto-reload preload enable"),(7,7,"DIR","Counter direction"),
        (3,3,"UDIS","Update disable"),(0,0,"CEN","Counter enable"),
    ],
    "TIM2_SR":[(0,0,"UIF","Update interrupt flag")],

    # ---------- Peripheral: ADC ----------
    "ADC1_CR2":[
        (23,23,"SWSTART","Start conversion of regular channels"),(22,22,"JSWSTART","Start conversion of injected channels"),
        (11,11,"CONT","Continuous conversion mode"),(0,0,"ADON","A/D converter ON/OFF"),
    ],
    "ADC1_SR":[(4,4,"JEOC","Injected channel end of conversion"),(1,1,"EOC","Regular channel end of conversion"),(0,0,"AWD","Analog watchdog flag")],

    # ---------- Peripheral: PWR / FLASH / WWDG / IWDG / CRC ----------
    "PWR_CR":[(9,9,"DBP","Disable backup domain write protection"),(1,1,"PDDS","Power down deepsleep"),(0,0,"LPDS","Low-power deepsleep")],
    "PWR_CSR":[(2,2,"PVDO","PVD output"),(1,1,"SBF","Standby flag"),(0,0,"WUF","Wakeup flag")],
    "FLASH_ACR":[(4,4,"PRFTBE","Prefetch buffer enable"),(2,0,"LATENCY","Latency (wait states)")],
    "FLASH_SR":[(5,5,"EOP","End of operation"),(2,2,"PGERR","Programming error"),(0,0,"BSY","Busy flag")],
    "FLASH_CR":[(7,7,"STRT","Start bit"),(1,1,"PER","Page erase"),(0,0,"PG","Programming")],
    "WWDG_CR":[(7,7,"WDGA","Activation bit"),(6,0,"T[6:0]","7-bit counter")],
    "IWDG_KR":[(15,0,"KEY","Key value")],
    "IWDG_PR":[(2,0,"PR[2:0]","Prescaler divider")],
    "CRC_CR":[(0,0,"RESET","CRC reset")],

    # ====================== Core: SysTick ======================
    "STK_CTRL":[
        (16,16,"COUNTFLAG","Returns 1 if timer counted to 0 since last read"),
        (2,2,"CLKSOURCE","Clock source (0=external ref, 1=processor clock)"),
        (1,1,"TICKINT","SysTick exception request enable"),
        (0,0,"ENABLE","Counter enable"),
    ],
    "STK_LOAD":[(23,0,"RELOAD","Reload value (24-bit, counter loads this on underflow)")],
    "STK_VAL":[(23,0,"CURRENT","Current counter value (24-bit, read clears COUNTFLAG)")],
    "STK_CALIB":[
        (31,31,"NOREF","No reference clock provided (1=no external ref clock)"),
        (30,30,"SKEW","Calibration value is not exactly 10ms"),
        (23,0,"TENMS","Calibration value for 10ms (or 0 if unknown)"),
    ],

    # ====================== Core: SCB ======================
    "SCB_CPUID":[
        (31,24,"IMPLEMENTER","Implementer code (0x41 = ARM)"),
        (23,20,"VARIANT","Variant number (implementation defined)"),
        (19,16,"ARCHITECTURE","Architecture (0xF = Cortex-M family)"),
        (15,4,"PARTNO","Part number (0xC23 = Cortex-M3)"),
        (3,0,"REVISION","Revision number (p)"),
    ],
    "SCB_ICSR":[
        (31,31,"NMIPENDSET","NMI set-pending (write 1 to pend NMI)"),
        (28,28,"PENDSVSET","PendSV set-pending"),
        (27,27,"PENDSVCLR","PendSV clear-pending"),
        (26,26,"PENDSTSET","SysTick set-pending"),
        (25,25,"PENDSTCLR","SysTick clear-pending"),
        (23,23,"ISRPREEMPT","Interrupt pending and will be serviced after current"),
        (22,22,"ISRPENDING","Interrupt pending flag (excluding NMI/SysTick)"),
        (21,12,"VECTPENDING","Pending exception vector number"),
        (8,0,"VECTACTIVE","Active exception vector number (0=thread mode)"),
    ],
    "SCB_VTOR":[(31,7,"TBLOFF","Vector table base offset (bits 31:7, 25-bit)")],
    "SCB_AIRCR":[
        (31,16,"VECTKEY","Vector key (must write 0x05FA, reads 0xFA05)"),
        (15,15,"ENDIANESS","Data endianness (0=little, read-only)"),
        (10,8,"PRIGROUP","Interrupt priority grouping field"),
        (2,2,"SYSRESETREQ","System reset request"),
        (1,1,"VECTCLRACTIVE","Clear all active state bits (debug only)"),
        (0,0,"VECTRESET","Reserved for debug (do not use)"),
    ],
    "SCB_SCR":[
        (4,4,"SEVONPEND","Send event on pending bit enable"),
        (2,2,"SLEEPDEEP","Deep sleep enable (0=sleep, 1=deep sleep)"),
        (1,1,"SLEEPONEXIT","Sleep on exit from ISR (return to thread -> sleep)"),
    ],
    "SCB_CCR":[
        (9,9,"STKALIGN","Stack alignment on exception entry (0=8-byte, 1=4-byte)"),
        (8,8,"BFHFNMIGN","Bus fault / HardFault / NMI ignore (handler priority <=0)"),
        (3,3,"DIV_0_TRP","Divide by zero trap enable"),
        (2,2,"UNALIGN_TRP","Unaligned access trap enable"),
        (1,1,"USERSETMPEND","User mode SETPEND enable"),
        (0,0,"NONBASETHRDENA","Thread mode can be entered from base level"),
    ],
    "SCB_SHPR1":[
        (31,24,"PRI_6","Priority of system handler 6 (UsageFault)"),
        (23,16,"PRI_5","Priority of system handler 5 (BusFault)"),
        (15,8,"PRI_4","Priority of system handler 4 (MemManage)"),
    ],
    "SCB_SHPR2":[(31,24,"PRI_11","Priority of system handler 11 (SVCall)")],
    "SCB_SHPR3":[
        (31,24,"PRI_15","Priority of system handler 15 (SysTick)"),
        (23,16,"PRI_14","Priority of system handler 14 (PendSV)"),
    ],
    "SCB_SHCSR":[
        (18,18,"USGFAULTENA","UsageFault enable"),
        (17,17,"BUSFAULTENA","BusFault enable"),
        (16,16,"MEMFAULTENA","MemManage enable"),
        (8,8,"SVCALLPENDED","SVCall pending"),
        (7,7,"BUSFAULTPENDED","BusFault pending"),
        (6,6,"MEMFAULTPENDED","MemManage pending"),
        (5,5,"USGFAULTPENDED","UsageFault pending"),
        (4,4,"SYSTICKACT","SysTick active"),
        (3,3,"PENDSVACT","PendSV active"),
        (1,1,"SVCALLACT","SVCall active"),
        (0,0,"NMIACT","NMI active"),
    ],
    "SCB_CFSR":[
        # ---- UFSR (UsageFault Status, bits 31:16) ----
        (25,25,"DIVBYZERO","Divide by zero usage fault"),
        (24,24,"UNALIGNED","Unaligned access usage fault"),
        (19,19,"NOCP","No coprocessor usage fault"),
        (18,18,"INVPC","Invalid PC load usage fault"),
        (17,17,"INVSTATE","Invalid state usage fault"),
        (16,16,"UNDEFINSTR","Undefined instruction usage fault"),
        # ---- BFSR (BusFault Status, bits 15:8) ----
        (15,15,"BFARVALID","BusFault address register valid"),
        (12,12,"STKERR","BusFault on stacking for exception entry"),
        (11,11,"UNSTKERR","BusFault on unstacking for exception return"),
        (10,10,"IMPRECISERR","Imprecise data bus error"),
        (9,9,"PRECISERR","Precise data bus error"),
        (8,8,"IBUSERR","Instruction bus error"),
        # ---- MMFSR (MemManage Status, bits 7:0) ----
        (7,7,"MMARVALID","MemManage address register valid"),
        (5,5,"MSTKERR","MemManage on stacking for exception entry"),
        (4,4,"MUNSTKERR","MemManage on unstacking for exception return"),
        (1,1,"DACCVIOL","Data access violation"),
        (0,0,"IACCVIOL","Instruction access violation"),
    ],
    "SCB_HFSR":[
        (31,31,"DEBUG_VT","Debug event on HardFault (reserved for debug)"),
        (30,30,"FORCED","Forced HardFault (escalated from configurable fault)"),
        (1,1,"VECTTBL","Vector table read fault on exception entry"),
    ],
    "SCB_DFSR":[
        (4,4,"EXTERNAL","External debug request"),
        (3,3,"VCATCH","Vector catch"),
        (2,2,"DWTTRAP","DWT match"),
        (1,1,"BKPT","Breakpoint"),
        (0,0,"HALTED","Halt request"),
    ],
    "SCB_MMFAR":[(31,0,"ADDRESS","MemManage fault address (valid when MMARVALID=1)")],
    "SCB_BFAR":[(31,0,"ADDRESS","BusFault address (valid when BFARVALID=1)")],
    "SCB_AFSR":[(31,0,"IMPDEF","Implementation defined fault status")],

    # ====================== Core: MPU ======================
    "MPU_TYPE":[
        (23,16,"IREGION","Number of instruction regions (0 = unified MPU)"),
        (15,8,"DREGION","Number of data regions (e.g. 8 = 8 regions)"),
        (0,0,"SEPARATE","Separate flag (0 = unified, 1 = separate)"),
    ],
    "MPU_CTRL":[
        (2,2,"PRIVDEFENA","Privileged default memory map enable"),
        (1,1,"HFNMIENA","HardFault / NMI enable MPU during handler"),
        (0,0,"ENABLE","MPU enable"),
    ],
    "MPU_RNR":[(7,0,"REGION","Region number selected for RBAR/RASR")],
    "MPU_RBAR":[
        (31,5,"ADDR","Region base address (bits 31:5)"),
        (4,4,"VALID","Use REGION field to update RNR (1 = update)"),
        (3,0,"REGION","Region number (if VALID=1, also writes RNR)"),
    ],
    "MPU_RASR":[
        (28,28,"XN","Execute never (1 = instruction fetch prohibited)"),
        (26,24,"AP","Access permission (3-bit: 000=no access, 111=full access)"),
        (21,19,"TEX","Type extension field (3-bit, memory attributes)"),
        (18,18,"S","Shareable"),
        (17,17,"C","Cacheable"),
        (16,16,"B","Bufferable"),
        (15,8,"SRD","Subregion disable (8 bits, 1=disable subregion)"),
        (5,1,"SIZE","Region size (5-bit: N, region = 2^(N+1) bytes)"),
        (0,0,"ENABLE","Region enable"),
    ],
}

# ====================== Repeated peripheral register aliases ======================
for g in ["GPIOB","GPIOC"]:
    REG_BITDEF[f"{g}_CRL"] = REG_BITDEF["GPIOA_CRL"]
    REG_BITDEF[f"{g}_CRH"] = REG_BITDEF["GPIOA_CRH"]
    REG_BITDEF[f"{g}_IDR"] = [(15,0,"IDR[15:0]","Port input data (read-only)")]
    REG_BITDEF[f"{g}_ODR"] = [(15,0,"ODR[15:0]","Port output data register")]
    REG_BITDEF[f"{g}_BSRR"] = [(31,16,"BR[15:0]","Port reset bit (write 1 to clear pin)"),(15,0,"BS[15:0]","Port set bit (write 1 to set pin)")]
    REG_BITDEF[f"{g}_BRR"] = [(15,0,"BR[15:0]","Port reset bit (write 1 to clear pin)")]
    REG_BITDEF[f"{g}_LCKR"] = [(16,16,"LCKKEY","Lock key"),(15,0,"LCK[15:0]","Port lock bits")]

for usart in ["USART2","USART3"]:
    REG_BITDEF[f"{usart}_CR1"] = REG_BITDEF["USART1_CR1"]
    REG_BITDEF[f"{usart}_SR"] = REG_BITDEF["USART1_SR"]

REG_BITDEF["SPI2_CR1"] = REG_BITDEF["SPI1_CR1"]
REG_BITDEF["SPI2_SR"] = REG_BITDEF["SPI1_SR"]

for t in ["TIM3","TIM4"]:
    REG_BITDEF[f"{t}_CR1"] = REG_BITDEF["TIM2_CR1"]
    REG_BITDEF[f"{t}_SR"] = REG_BITDEF["TIM2_SR"]

REG_BITDEF["I2C2_CR1"] = REG_BITDEF["I2C1_CR1"]
REG_BITDEF["I2C2_CR2"] = REG_BITDEF["I2C1_CR2"]
REG_BITDEF["ADC2_CR2"] = REG_BITDEF["ADC1_CR2"]
REG_BITDEF["ADC2_SR"] = REG_BITDEF["ADC1_SR"]

# ====================== Repeated NVIC core register aliases ======================
# ISER / ICER / ISPR / ICPR / IABR: each is a 32-bit mask of interrupt enable/pending/active bits
_NVIC_MASK_DESC = {
    "ISER": ("SETENA","Interrupt set-enable (write 1 to enable IRQ)"),
    "ICER": ("CLRENA","Interrupt clear-enable (write 1 to disable IRQ)"),
    "ISPR": ("SETPEND","Interrupt set-pending (write 1 to pend IRQ)"),
    "ICPR": ("CLRPEND","Interrupt clear-pending (write 1 to unpend IRQ)"),
    "IABR": ("ACTIVE","Interrupt active flag (read-only)"),
}
for _prefix, (_fname, _desc) in _NVIC_MASK_DESC.items():
    for _i in range(3):
        REG_BITDEF[f"NVIC_{_prefix}{_i}"] = [(31,0,_fname,_desc)]

# IPR0..IPR7: each holds four 8-bit priority fields (only upper 4 bits implemented on STM32)
for _i in range(8):
    _base = _i * 4
    REG_BITDEF[f"NVIC_IPR{_i}"] = [
        (31,24,f"PRI_{_base+3}",f"Priority of IRQ {_base+3}"),
        (23,16,f"PRI_{_base+2}",f"Priority of IRQ {_base+2}"),
        (15,8, f"PRI_{_base+1}",f"Priority of IRQ {_base+1}"),
        (7,0,  f"PRI_{_base+0}",f"Priority of IRQ {_base+0}"),
    ]


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("STM32F103C8T6 | Core/Peripheral Dual-Input Register Parser | 32-bit Bit Checkboxes")
        self.resize(1420,940)
        w = QWidget()
        self.setCentralWidget(w)
        lay = QVBoxLayout(w)

        h1 = QHBoxLayout()
        # Core register input
        self.le_core_reg = QLineEdit()
        self.le_core_reg.setPlaceholderText("Core register, e.g. SCB_CPUID, NVIC_ISER0")
        comp_core = QCompleter(CORE_NAME_LIST)
        comp_core.setCaseSensitivity(Qt.CaseInsensitive)
        comp_core.setFilterMode(Qt.MatchContains)
        self.le_core_reg.setCompleter(comp_core)
        self.le_core_reg.editingFinished.connect(self.on_core_edit_done)

        # Peripheral register input
        self.le_periph_reg = QLineEdit()
        self.le_periph_reg.setPlaceholderText("Peripheral register, e.g. RCC_APB2ENR, GPIOA_CRL")
        comp_periph = QCompleter(PERIPH_NAME_LIST)
        comp_periph.setCaseSensitivity(Qt.CaseInsensitive)
        comp_periph.setFilterMode(Qt.MatchContains)
        self.le_periph_reg.setCompleter(comp_periph)
        self.le_periph_reg.editingFinished.connect(self.on_periph_edit_done)

        self.le_addr = QLineEdit()
        self.le_addr.setReadOnly(True)
        self.le_val_hex = QLineEdit()
        self.le_val_hex.setPlaceholderText("Hex, e.g. 0x12345678")
        self.le_val_dec = QLineEdit()
        self.le_val_dec.setPlaceholderText("Decimal, e.g. 305419896")

        self.btn_parse = QPushButton("Parse Bit Fields")
        self.btn_parse.clicked.connect(self.do_parse)
        self.btn_zero = QPushButton("Clear All")
        self.btn_zero.clicked.connect(self.all_zero)
        self.btn_set = QPushButton("Set All")
        self.btn_set.clicked.connect(self.all_one)

        h1.addWidget(QLabel("[Core]"))
        h1.addWidget(self.le_core_reg, stretch=2)
        h1.addWidget(QLabel("[Periph]"))
        h1.addWidget(self.le_periph_reg, stretch=2)
        h1.addWidget(QLabel("Addr:"))
        h1.addWidget(self.le_addr, stretch=1)
        h1.addWidget(QLabel("Hex:"))
        h1.addWidget(self.le_val_hex, stretch=1)
        h1.addWidget(QLabel("Dec:"))
        h1.addWidget(self.le_val_dec, stretch=1)
        h1.addWidget(self.btn_parse)
        h1.addWidget(self.btn_zero)
        h1.addWidget(self.btn_set)
        lay.addLayout(h1)

        # ========== 32-bit checkbox area: bit31~bit0, two rows of 16 ==========
        self.bit_checks = []
        grid_bit = QGridLayout()
        for bitpos in range(32):
            cb = QCheckBox(f"{bitpos:2d}")
            cb.stateChanged.connect(self.on_bit_check_changed)
            self.bit_checks.append(cb)
            row = 0 if bitpos <16 else 1
            col = bitpos if bitpos<16 else (bitpos-16)
            grid_bit.addWidget(cb, row, col)
        lay.addLayout(grid_bit)

        self.table_bit = QTableWidget()
        self.table_bit.setColumnCount(4)
        self.table_bit.setHorizontalHeaderLabels(["Bit Range","Field Name","Description","Current Value (dec/bin)"])
        self.table_bit.horizontalHeader().setStretchLastSection(True)
        lay.addWidget(self.table_bit, stretch=2)

        self.text_out = QTextEdit()
        mono_font = QFont("Consolas")
        mono_font.setPointSize(10)
        self.text_out.setFont(mono_font)
        lay.addWidget(self.text_out, stretch=1)

        self.le_val_hex.textChanged.connect(self.on_hex_text_change)
        self.le_val_dec.textChanged.connect(self.on_dec_text_change)
        self.current_reg_name = ""
        self.current_value = 0

    def on_core_edit_done(self):
        name = self.le_core_reg.text().strip()
        self.le_periph_reg.blockSignals(True)
        self.le_periph_reg.setText("")
        self.le_periph_reg.blockSignals(False)
        self._select_reg(name)

    def on_periph_edit_done(self):
        name = self.le_periph_reg.text().strip()
        self.le_core_reg.blockSignals(True)
        self.le_core_reg.setText("")
        self.le_core_reg.blockSignals(False)
        self._select_reg(name)

    def _select_reg(self,name):
        self.table_bit.setRowCount(0)
        self.text_out.setPlainText("")
        self.current_reg_name = ""
        self._set_value(0)
        if name not in ALL_REGS:
            self.le_addr.setText("Register not found")
            return
        addr = ALL_REGS[name]
        self.le_addr.setText(f"0x{addr:08X}")
        self.current_reg_name = name
        bit_list = REG_BITDEF.get(name, [])
        self.table_bit.setRowCount(len(bit_list))
        for row, (bs,be,fname,desc) in enumerate(bit_list):
            self.table_bit.setItem(row,0,QTableWidgetItem(f"{bs}:{be}"))
            self.table_bit.setItem(row,1,QTableWidgetItem(fname))
            self.table_bit.setItem(row,2,QTableWidgetItem(desc))
            self.table_bit.setItem(row,3,QTableWidgetItem("-"))

    def _set_value(self, val):
        """Single source of truth: update both input boxes and all 32 checkboxes."""
        val = val & 0xFFFFFFFF
        self.current_value = val
        self.le_val_hex.blockSignals(True)
        self.le_val_hex.setText(f"0x{val:08X}")
        self.le_val_hex.blockSignals(False)
        self.le_val_dec.blockSignals(True)
        self.le_val_dec.setText(str(val))
        self.le_val_dec.blockSignals(False)
        for bitpos in range(32):
            cb = self.bit_checks[bitpos]
            cb.blockSignals(True)
            cb.setChecked((val >> bitpos) & 1 == 1)
            cb.blockSignals(False)

    def on_hex_text_change(self):
        """Hex input edited: parse and sync decimal + checkboxes."""
        txt = self.le_val_hex.text().strip()
        try:
            val = int(txt, 0)
        except ValueError:
            return
        self._set_value(val)

    def on_dec_text_change(self):
        """Decimal input edited: parse and sync hex + checkboxes."""
        txt = self.le_val_dec.text().strip()
        try:
            val = int(txt, 10)
        except ValueError:
            return
        self._set_value(val)

    def on_bit_check_changed(self):
        """Checkbox changed: compute 32-bit value and sync both input boxes."""
        val = 0
        for bitpos in range(32):
            cb = self.bit_checks[bitpos]
            if cb.isChecked():
                val |= (1 << bitpos)
        self._set_value(val)

    def all_zero(self):
        self._set_value(0)

    def all_one(self):
        self._set_value(0xFFFFFFFF)

    def do_parse(self):
        reg_name = self.current_reg_name
        if not reg_name or reg_name not in ALL_REGS:
            self.text_out.setPlainText("Error: please select a register in the [Core] or [Periph] input box first")
            return
        val = self.current_value & 0xFFFFFFFF
        lines = []
        lines.append(f"Register: {reg_name}")
        lines.append(f"Address: {self.le_addr.text()}")
        lines.append(f"Input Value: 0x{val:08X}  Decimal: {val}")
        lines.append(f"32-bit Binary: {val:032b}")
        lines.append("-"*80)

        bit_list = REG_BITDEF.get(reg_name, [])
        for row,(bs,be,fname,desc) in enumerate(bit_list):
            bw = bs - be + 1
            mask = ((1<<bw)-1) << be
            fv = (val & mask) >> be
            bstr = format(fv,f'0{bw}b')
            self.table_bit.setItem(row,3,QTableWidgetItem(f"{fv}/{bstr}"))
            lines.append(f"[{bs:2d}:{be:<2d}] {fname:<20s} = {bstr}({fv:<3d}) | {desc}")
        lines.append("-"*80)
        bitnum = []
        bitval = []
        for pos in range(31,-1,-1):
            bitnum.append(f"{pos:2d}")
            bitval.append(f"{(val>>pos)&1:2d}")
        lines.append("Bit Index (all 32 bits):  "+" ".join(bitnum))
        lines.append("Bit Value (all 32 bits):  "+" ".join(bitval))
        self.text_out.setPlainText("\n".join(lines))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
