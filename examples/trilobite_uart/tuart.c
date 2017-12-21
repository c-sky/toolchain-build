/*
 * tuart.c - Tests uart 
 *
 * Copyright (C): 2008~2010 Hangzhou C-SKY Microsystem Co.,LTD.
 * Author: Liu Bing  (bing_liu@c-sky.com)
 * Contributor: Liu Bing
 * Date: 2010-6-28
 */

#include "ck810.h"
#include "uart.h"
#include "misc.h"

extern CK_Uart_Device consoleuart;

CK_UINT8 data[14] = {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 
                     'K', 'L', 'M', 'N'};


/*****************************************************************************
CK_UART_TestMode: Tests work mode of uart, namely query mode and interrupt mode

INPUT: uartid - Number of uart transminting data
       uartb - Number of uart receiving data

RETURN: NULL

*****************************************************************************/
static void CK_UART_TestMode(CK_Uart_Device uartid)
{
  CK_UINT32 i;
  CK_UINT32 get;
  
///////////////////* Query mode *////////////////////////// 
  printf("\n\n\t- - - Testing uart mode...\n");
  printf("\r\t(query mode ): Output is---\n\t\t");
  for(i = 0; i < 14; i++)
  {
    CK_Uart_PutChar(uartid, data[i]);
  }
  printf("- - - [y/n] ");
  while(1)
  {
    get = CK_WaitForReply();
    if((get == 1) ||(get == 0))
    {
       break;
    }
    else
    {
      printf("\n\tPlease enter 'y' or 'n'   ");
    }
  }
  if(get == 1)
  {
    printf("\t- - -PASS\n");
  }
  else 
  {
    printf("\t- - -FAILURE\n");
  }
///////////////////* Interrupt mode *////////////////////////
  printf("\r\t(interrupt mode ): Output is---\n\t\t");
  /* Insure prompt information is displayed */
  delay(5000);
  /* Changes uart mode to interrupt mode */
  CK_Uart_Close(uartid);
  CK_Uart_Open(uartid, NULL);
  CK_Uart_SetRXMode(uartid, FALSE);
  CK_Uart_SetTXMode(uartid, FALSE);
  for(i = 0; i < 14; i++)
  {
    CK_Uart_PutChar(uartid, data[i]);
  }
  printf("- - - [y/n] ");
    while(1)
  {
    get = CK_WaitForReply();
    if((get == 1) ||(get == 0))
    {
       break;
    }
    else
    {
      printf("\n\tPlease enter 'y' or 'n'   ");
    }
  }
  if(get == 1)
  {
    printf("\t- - -PASS\n");
  }
  else 
  {
    printf("\t- - -FAILURE\n");
  }
}

/*****************************************************************************
CK_UART_TestBaudrate: Tests baudrate of uart

INPUT: uartid - Number of uart transminting data
       uartb - Number of uart receiving data

RETURN: NULL

*****************************************************************************/
static void CK_UART_TestBaudrate(CK_Uart_Device uartid)
{
  CK_UINT32 i;
  CK_UINT32 baudrate;
  CK_UINT32 get;  

  CK_UINT32 pB[] = {B9600, B14400, B38400, B57600, B115200, B19200};

  printf("\n\t- - - Test uart baudrate.\n");
  for(baudrate = 0; baudrate < sizeof(pB) / 4; baudrate++)
  {
    printf("\tBaudrate is %d? [y] ", pB[baudrate]);
    CK_Uart_ChangeBaudrate(uartid, pB[baudrate]);
    while(CK_WaitForReply() != 1)
    {
      printf("\n\tPlease enter 'y'   ");
    }
    printf(" :Output is ---\n\t\t");
    for(i = 0; i < 14; i++)
    { 
      CK_Uart_PutChar(uartid, data[i]);
      
    }
    printf("- - -[y/n] ");
    while(1)
    {
      get = CK_WaitForReply();
      if(get == 1 || get == 0)
      {
	break;
      }
      else
      {
        printf("\n\tPlease enter 'y' or 'n'   ");
      }
    }
    if(get == 1)
    {
      printf("\t- - -PASS\n");
    }
    else 
   {
      printf("\t- - -FAILURE\n");
    }

  }
  
}

/*****************************************************************************
CK_UART_TestParity: Tests Parity of uarts

INPUT: uartid - Number of uart transminting data
       uartb - Number of uart receiving data

RETURN: NULL

*****************************************************************************/
static void CK_UART_TestParity(CK_Uart_Device uartid)
{
  CK_Uart_Parity parity;
  CK_UINT32 i;
  CK_UINT32 get;

  printf("\n\t- - - Test uart parity. (Parity: 0 --- ODD, 1 --- EVEN, 2 --- NONE)\n");
  for(parity = 0; parity < 3; parity++)
  {
    printf("\tParity is %d? [y] ", parity);
    CK_Uart_SetParity(uartid, parity);
    while(CK_WaitForReply() != 1)
    {
      printf("\n\tPlease enter 'y'   ");
    }
    printf(" :Output is ---\n\t\t");
    for(i = 0; i < 14; i++)
    {
      CK_Uart_PutChar(uartid, data[i]);
    }

    printf("- - -[y/n] ");
    while(1)
    {
      get = CK_WaitForReply();
      if(get == 1 || get == 0)
      {
        break;
      }
      else
      {
        printf("\n\tPlease enter 'y' or 'n'   ");
      }
     }
    if(get == 1)
    {
      printf("\t- - -PASS\n");
    }
    else
   {
      printf("\t- - -FAILURE\n");
    }

  }

}


/*****************************************************************************
CK_UART_TestWordSize: Tests word size of uarts.

INPUT: uartid - Number of uart transminting data
       uartb - Number of uart receiving data

RETURN: NULL

*****************************************************************************/
static void CK_UART_TestWordSize(
  CK_Uart_Device uartid
)
{
  CK_Uart_WordSize wordsize;
  CK_UINT32 i;
  CK_UINT32 get;  

  printf("\n\t- - - Test uart wordsize.\n");
  printf("\t0 --- WORD_SIZE_5,\n\t1 --- WORD_SIZE_6,\n"
         "\t2 --- WORD_SIZE_7,\n\t3 --- WORD_SIZE_8\n");
  for(wordsize = 2; wordsize < 4; wordsize++)
  {
    printf("\tWordsize is %d? [y] ", wordsize);
    CK_Uart_SetWordSize(uartid, wordsize);
    while(CK_WaitForReply() != 1)
    {
      printf("\n\tPlease enter 'y'   ");
    }
    printf(" :Output is ---\n\t\t");
    for(i = 0; i < 14; i++)
    {
      CK_Uart_PutChar(uartid, data[i]);
    }

    printf("- - -[y/n] ");
    while(1)
    {
      get = CK_WaitForReply();
      if(get == 1 || get == 0)
      {
        break;
      }
      else
      {
        printf("\n\tPlease enter 'y' or 'n'   ");
      }
     }
    if(get == 1)
    {
      printf("\t- - -PASS\n");
    }
    else
   {
      printf("\t- - -FAILURE\n");
    }

  }
 
}

/*****************************************************************************
CK_UART_Test: Main function of uart testing 

INPUT: NULL

RETURN: NULL

*****************************************************************************/
void CK_UART_Test()
{
  CK_UINT32 get;
  CK_Uart_Device uartid = consoleuart;

  printf("Testing uart...");
  printf("\nDefault configure: Baudrate --- 19200,");
  printf("Parity --- NONE,");
  printf("Wordsize --- 8. ");
  printf("\n- - -UART%d ready? [y] ", uartid);

  while(1)
  {
    get = CK_WaitForReply();
    if((get == 1))
    {
       break;
    }
    else
    {
      printf("\nPlease enter 'y'   ");
    }
  }
  CK_UART_TestMode(uartid);
  /*
   * After have tested uart mode, Baudrate, Parity and WordSize are tested in
   * interrupt mode here, so you can stop testing process by press CTRL+C.
   */
  CK_UART_TestBaudrate(uartid);
  CK_UART_TestParity(uartid);
  CK_UART_TestWordSize(uartid);
  
  /* Recover uart to default configure.*/
  delay(10000);
  CK_Uart_Close(uartid);
}

