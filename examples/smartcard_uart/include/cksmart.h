/*
 * Description: cksmart.h - Define the system configuration, memory & IO base
 * address, flash size & address, interrupt resource for cksmart soc.
 *
 * Copyright (C) : 2008 Hangzhou C-SKY Microsystems Co.,LTD.
 * Author(s): Liu Bing (bing_liu@c-sky.com)
 * Contributors: Liu Bing
 * Date:  2010-06-26
 * Modify by liu jirang(jirang_liu@c-sky.com)  on 2012-10-13
 */

#ifndef __INCLUDE_CKSMART_H
#define __INCLUDE_CKSMART_H

/**************************************
 * MCU & Borads.
 *************************************/

/* CPU frequence definition */
#define CPU_DEFAULT_FREQ       10000000  /* Hz */
/* AHB frequence definition */
#define AHB_DEFAULT_FREQ       10000000   /* Hz */
/* APB frequence definition */
#define APB_DEFAULT_FREQ       10000000   /* Hz */

/*
 * define irq number of perpheral modules
 */

#define  CK_INTC_CORETIM	0
#define  CK_INTC_UART0		2



/***** VIC ******/
#define CK_INTC_BASEADDRESS			(0xE000E000)


/***** Uart *******/
#define CK_UART_ADDRBASE0			(volatile CK_UINT32 *)(0x00F15000)

#define CK_UART0_IRQID				CK_INTC_UART0

/**** Timer ****/
#define  CK_CORETIM_BASSADDR		(volatile CK_UINT32 *)(0xE000E010)
/*
 * Define number of the timer interrupt
 */
#define  CK_TIMER_IRQ0				CK_INTC_CORETIM



#endif /* __INCLUDE_CKRHEA_H */
