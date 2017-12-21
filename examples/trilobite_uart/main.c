/*
 * main.c - main function Modulation.
 *
 * Copyright (C): 2008~2010 Hangzhou C-SKY Microsystem Co.,LTD.
 * Author: Liu Bing  (bing_liu@c-sky.com)
 * Contributor: Liu Bing
 * Date: 2010-6-28
 *
 */


#include "datatype.h"
#include "ck810.h"
#include "uart.h"
#include "misc.h"

CK_Uart_Device consoleuart = CONFIG_TERMINAL_UART;
extern void CK_Exception_Init (void);
extern void CK_INTC_Init(void);
extern void CK_UART_Test();

/* 
 * initialize the device registered 
 */
static void CK_Drivers_Init(void)
{
	CK_Uart_DriverInit();
    CK_INTC_Init();
	
}


static void CK_Console_CallBack(CK_INT8 error)
{   
  if(error==CK_Uart_CTRL_C)
  {
    CK_UART_ClearRxBuffer(consoleuart);
  }
  
} 

static void CK_Console_Init()
{
  CK_Uart_Open(consoleuart,CK_Console_CallBack);
}

/* 
 * the main function of Uart demo project
 */
int main ( void )
{
    CK_Drivers_Init();
    CK_Exception_Init();
    CK_Console_Init();	

    printf ("\n");
    {
	    /*
	     * Call the uart test case.
         */
    	CK_UART_Test();
    } 

    return 0x00;
}


