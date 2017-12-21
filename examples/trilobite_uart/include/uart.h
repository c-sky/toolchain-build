/*
 * File : uart.h
 * Description: this file contains the macros support uart operations
 * Copyright (C):  2008 C-SKY Microsystem  Ltd.
 * Author(s):   Shuli wu  
 * E_mail:  shuli_wu@c-sky.com
 * Contributors: Yun Ye 
 * Date:  2008-9-25       
 */

#ifndef __UART_H__
#define __UART_H__

#include "datatype.h"


/************************************
 * (8 data bitbs, ODD, 1 stop bits)
 ***********************************/
#define BAUDRATE   19200
/*
 * Terminal uart to use
 */
#define  CONFIG_TERMINAL_UART UART0

//////////////////////////////////////////////////////////////////////////////////////////
typedef enum{ 
  B4800=4800,
  B9600=9600,
  B14400=14400,
  B19200=19200,
  B56000=56000,
  B38400=38400,
  B57600=57600,
  B115200=115200
}CK_Uart_Baudrate;


typedef enum{
  UART0,
  UART1,
  UART2,
  UART3 
}CK_Uart_Device;

typedef enum{
  WORD_SIZE_5,
  WORD_SIZE_6,
  WORD_SIZE_7,
  WORD_SIZE_8
}CK_Uart_WordSize;

typedef enum{
  ODD,
  EVEN,
  NONE
}CK_Uart_Parity;

typedef enum{
	  LCR_STOP_BIT_1,
		LCR_STOP_BIT_2
}CK_Uart_StopBit;


typedef enum{
    CK_Uart_CTRL_C = 0,
    CK_Uart_FrameError = 1,
    CK_Uart_ParityError = 2
}CKEnum_Uart_Error;

CK_INT32 CK_Uart_DriverInit();


/////////////////////////////////////////////////////////////////
/* open the uart : 
 * set the callback function --- handler(void);
 * intilize the serial port,sending and receiving buffer;
 * intilize irqhandler ;
 * register irqhandler
 * return: SUCCESS or FAILURE
 */
CK_INT32 CK_Uart_Open( CK_Uart_Device uartid,void (*handler)(CK_INT8 error));

/* This function is used to close the uart 
 * clear the callback function
 * free the irq
 * return: SUCCESS or FAILURE
 */
 CK_INT32 CK_Uart_Close( CK_Uart_Device uartid);
 
 /*
 * This function is used to change the bautrate of uart.
 * Parameters:
 * uartid--a basepointer, could be one of UART0, UART1, UART2 or UART3.
 * baudrate--the baudrate that user typed in.
 * return: SUCCESS or FAILURE 
*/

CK_INT32 CK_Uart_ChangeBaudrate(
     CK_Uart_Device uartid,  CK_Uart_Baudrate baudrate);
    
/*
 * This function is used to enable or disable parity, also to set ODD or EVEN
 * parity.
 * Parameters:
 *   uartid--a basepointer, could be one of UART0, UART1, UART2 or UART3.
 *   parity--ODD=8, EVEN=16, or NONE=0.
 * return: SUCCESS or FAILURE
*/

CK_INT32 CK_Uart_SetParity(
     CK_Uart_Device uartid,  CK_Uart_Parity parity);

/*
 * We can call this function to set the stop bit--1 bit, 1.5 bits, or 2 bits.
 * But that it's 1.5 bits or 2, is decided by the wordlenth. When it's 5 bits,
 * there are 1.5 stop bits, else 2.
 * Parameters:
 *   uartid--a basepointer, could be one of UART0, UART1, UART2 or UART3.
 *	 stopbit--it has two possible value: STOP_BIT_1 and STOP_BIT_2.
 * return: SUCCESS or FAILURE
*/

CK_INT32 CK_Uart_SetStopBit(
     CK_Uart_Device uartid,  CK_Uart_StopBit stopbit);

/*
 * We can use this function to reset the transmit data length,and we
 * have four choices:5, 6, 7, and 8 bits.
 * Parameters:
 * 	uartid--a basepointer, could be one of UART0, UART1, UART2 or UART3.
 * 	wordsize--the data length that user decides
 * return: SUCCESS or FAILURE
*/

CK_INT32 CK_Uart_SetWordSize(CK_Uart_Device uartid,  CK_Uart_WordSize wordsize);
    
/*
 * This function is used to set the transmit mode, interrupt mode or
 * query mode.
 * Parameters:
 * 	uartid--a basepointer, could be one of UART0, UART1, UART2 or UART3.
 *  bQuery--it indicates the transmit mode: TRUE - query mode, FALSE - 
 *  inerrupt mode
 * return: SUCCESS or FAILURE
*/

CK_INT32 CK_Uart_SetTXMode( CK_Uart_Device uartid, BOOL  bQuery);

/*
 * This function is used to set the receive mode, interrupt mode or
 * query mode.
 * Parameters:
 * 	uartid--a basepointer, could be one of UART0, UART1, UART2 or UART3.
 *  bQuery--it indicates the receive mode: TRUE - query mode, FALSE - 
 *  interrupt mode
 * return: SUCCESS or FAILURE

*/
CK_INT32 CK_Uart_SetRXMode( CK_Uart_Device uartid, BOOL bQuery);

/* This function is used to get character,in query mode or interrupt mode.
 * Parameters:
 * 	 uartid--a basepointer, could be one of UART0, UART1, UART2 or UART3.
 *   brxquery--it indicates the receive mode: TRUE - query mode, FALSE - 
 *   interrupt mode
 * return: SUCCESS or FAILURE
 */
CK_INT32 CK_Uart_GetChar(CK_Uart_Device uartid,  CK_UINT8 *ch);

/* This function is used to transmit character,in query mode or interrupt mode.
 * Parameters:
 * 	 uartid--a basepointer, could be one of UART0, UART1, UART2 or UART3.
 *   brxquery--it indicates the receive mode: TRUE - query mode, FALSE - 
 *   interrupt mode
 * Return: SUCCESS or FAILURE.
 */
CK_INT32 CK_Uart_PutChar(CK_Uart_Device uartid, CK_UINT8 ch);

/*
 * initialize the uart:
 * baudrate: 19200
 * date length: 8 bits
 * paity: None(disabled)
 * number of stop bits: 1 stop bit
 * query mode
 * return: SUCCESS
 */
CK_INT32 CK_Uart_Init( CK_Uart_Device uartid);

/*
 */
CK_INT32 CK_Uart_ConfigDMA(
 CK_Uart_Device uartid,
 char *buffer,
 BOOL btx,
 CK_INT32 txrxsize,
 void (*handler)()
);

/* 
 */
void CK_Uart_StartDMARxTx (void);

void CK_UART_ClearRxBuffer(CK_Uart_Device uartid);

/* This function is used to get character,in query mode or interrupt mode*/
CK_INT32 CK_Uart_GetCharUnBlock(IN CK_Uart_Device uartid, OUT CK_UINT8 *ch);
#endif
