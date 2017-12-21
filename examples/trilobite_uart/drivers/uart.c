/*
  * Filename: uart.c
  * Description: this file contains the functions support uart operations
  * Copyright (C): Hangzhou C-Sky Microsystem Co, Ltd.   
  * Author(s): Shuli Wu (shuli_wu@c-sky.com), YUN YE (yun_ye@c-sky.com).   
  * Contributors: 
  * Date: Otc 10, 2008         
  */

#include "ck810.h"


#include "circlebuffer.h"
#include "uart.h"
#include "ckuart.h"
#include "intc.h"
#include "misc.h"

#define UARTID_MAX   sizeof(CK_Uart_Table) / sizeof(CKStruct_UartInfo) 
static void CK_Uart_Interrupt(CK_UINT32 irqid); 

/* the table of the uart serial ports */
static CKStruct_UartInfo CK_Uart_Table[] = 
{
  {0,CK_UART_ADDRBASE0,CK_UART0_IRQID,FALSE,NULL},
  {1,CK_UART_ADDRBASE1,CK_UART1_IRQID,FALSE,NULL},
//  {2,CK_UART_ADDRBASE2,CK_UART2_IRQID,FALSE,NULL},
};

/*
 * Make all the uarts in the idle state;
 * this function should be called before
 * INTC module working;
 */
void CK_Deactive_UartModule()
{
   int i;
   CKStruct_UartInfo *info;
   
   for( i = 0; i < UARTID_MAX; i++)
   {	   
       info = &(CK_Uart_Table[i]);
	   info->addr[CK_UART_LCR] = 0x83;
	   info->addr[CK_UART_DLL] = 0x1;
	   info->addr[CK_UART_DLH] = 0x0;
   }

}

/*
 * initialize the uart:
 * baudrate: 19200
 * date length: 8 bits
 * paity: None(disabled)
 * number of stop bits: 1 stop bit
 * query mode
 * return: SUCCESS
 */
CK_INT32 CK_Uart_Init( CK_Uart_Device uartid)
{
  CK_Uart_ChangeBaudrate(uartid,B19200);
  CK_Uart_SetParity(uartid,NONE);
  CK_Uart_SetWordSize(uartid,LCR_WORD_SIZE_8);
  CK_Uart_SetStopBit(uartid,LCR_STOP_BIT_1);
  CK_Uart_SetRXMode(uartid,TRUE);
  CK_Uart_SetTXMode(uartid,TRUE);
  return SUCCESS;
}


/* open the uart : 
 * set the callback function --- handler(void);
 * intilize the serial port,sending and receiving buffer;
 * intilize irqhandler ;
 * register irqhandler
 * return: SUCCESS or FAILURE
 */
CK_INT32 CK_Uart_Open(CK_Uart_Device uartid,void (*handler)(CK_INT8 error))
{
  CKStruct_UartInfo *info;
  PCKStruct_IRQHandler irqhander; 
  info = &(CK_Uart_Table[uartid]);
  if ((uartid < 0) || (uartid >= UARTID_MAX))
  {
    return FAILURE;
  }
  
  if (info->bopened)
  {
    return FAILURE;
  }
  CK_Uart_Init(uartid);
  
  
  /* intilize the sending and receiving buffers */
  CK_CircleBuffer_Init(
    &(info->txcirclebuffer), info->txbuffer, CK_UART_TXBUFFERSIZE);
  CK_CircleBuffer_Init(
    &(info->rxcirclebuffer), info->rxbuffer, CK_UART_RXBUFFERSIZE);
  info->handler = handler;
  
  /* intilize irqhandler */
  irqhander=&(info->irqhandler);
  irqhander->devname = "UART";
  irqhander->irqid = info->irq;
  irqhander->priority = info->irq;
  irqhander->handler = CK_Uart_Interrupt;
  irqhander->bfast = FALSE;
  irqhander->next = NULL; 
  
  /* register uart isr */
  CK_INTC_RequestIrq(&(info->irqhandler));	              
  info->bopened = TRUE;
  return SUCCESS;
}

/* This function is used to close the uart 
 * clear the callback function
 * free the irq
 * return: SUCCESS or FAILURE
 */
 CK_INT32 CK_Uart_Close(CK_Uart_Device uartid) 
{
  CKStruct_UartInfo *info;
  
  info = &(CK_Uart_Table[uartid]);	
  if ((uartid >= 0) && (uartid < UARTID_MAX) && (info->bopened))
  {
    /* Stop UART interrupt. */
    /* Clear TX & RX circle buffer. */
    info->addr[CK_UART_IER] &= ~IER_RDA_INT_ENABLE;
    info->handler = NULL;
    CK_INTC_FreeIrq(&(info->irqhandler));
    info->bopened = 0;
    return SUCCESS;
  }
  return FAILURE;
}  

/*
 * This function is used to change the bautrate of uart.
 * Parameters:
 * uartid--a basepointer, could be one of UART0, UART1, UART2 or UART3.
 * baudrate--the baudrate that user typed in.
 * return: SUCCESS or FAILURE 
*/

CK_INT32 CK_Uart_ChangeBaudrate(
  CK_Uart_Device uartid, 
  CK_Uart_Baudrate baudrate
)
{
  CK_INT32 divisor;		
  CK_INT32 timecount;
  CKStruct_UartInfo *info;
  
  timecount=0; 	
  info = &(CK_Uart_Table[uartid]);	
  /*the baudrates that uart surported as follows:*/  
  if((baudrate == B4800) || (baudrate == B9600) ||
     (baudrate == B14400) || (baudrate == B19200) ||
     (baudrate == B38400) || (baudrate == B56000) ||
     (baudrate == B57600) || (baudrate == B115200))           
  {
    /*
     * DLH and DLL may be accessed when the UART is not 
     * busy(USR[0]=0) and the DLAB bit(LCR[7]) is set.
     */
    while((info->addr[CK_UART_USR] & USR_UART_BUSY)
  	  && (timecount < UART_BUSY_TIMEOUT))
    {
      timecount++;
    }
    if(timecount >= UART_BUSY_TIMEOUT)
    {
      return FAILURE;
    }
    else
    {
      /*baudrate=(seriak clock freq)/(16*divisor).*/
      divisor = ((APB_DEFAULT_FREQ / baudrate) >> 4);
      info->addr[CK_UART_LCR] |= LCR_SET_DLAB;
      /* DLL and DLH is lower 8-bits and higher 8-bits of divisor.*/
      info->addr[CK_UART_DLL] = divisor & 0xff;         
      info->addr[CK_UART_DLH] = (divisor >> 8) & 0xff;     
      /* 
       * The DLAB must be cleared after the baudrate is setted
       * to access other registers. 
       */    
      info->addr[CK_UART_LCR] &= (~LCR_SET_DLAB);
      info->baudrate = baudrate;
      return SUCCESS;
      }
    }
    return FAILURE;
}
				
/*
 * This function is used to enable or disable parity, also to set ODD or EVEN
 * parity.
 * Parameters:
 *   uartid--a basepointer, could be one of UART0, UART1, UART2 or UART3.
 *   parity--ODD=8, EVEN=16, or NONE=0.
 * return: SUCCESS or FAILURE
*/

CK_INT32 CK_Uart_SetParity(
  CK_Uart_Device uartid, 
  CK_Uart_Parity parity
)
{
  CKStruct_UartInfo *info;
	
  info = &(CK_Uart_Table[uartid]);	
  CK_INT32 timecount;
  timecount = 0;
  /* PEN bit(LCR[3]) is writeable when the UART is not busy(USR[0]=0).*/
  while((info->addr[CK_UART_USR] & USR_UART_BUSY) &&
        (timecount < UART_BUSY_TIMEOUT))
  {
    timecount++;
  }
  if(timecount >= UART_BUSY_TIMEOUT)
  {
    return FAILURE;
  }
  else
  {
    switch(parity)
    {
      case NONE:     
	        /*CLear the PEN bit(LCR[3]) to disable parity.*/
	        info->addr[CK_UART_LCR] &= (~LCR_PARITY_ENABLE);
	  	break;
					
      case ODD:
		/* Set PEN and clear EPS(LCR[4]) to set the ODD parity. */  
		info->addr[CK_UART_LCR] |= LCR_PARITY_ENABLE;
		info->addr[CK_UART_LCR] &= LCR_PARITY_ODD; 
	  	break;
				  
      case EVEN:
		/* Set PEN and EPS(LCR[4]) to set the EVEN parity.*/
		info->addr[CK_UART_LCR] |= LCR_PARITY_ENABLE;
		info->addr[CK_UART_LCR] |= LCR_PARITY_EVEN;
		break;
				             
      default:
	        return FAILURE;
		break;				 
    }
    info->parity = parity;
    return SUCCESS;
  }
}
	
	
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
  CK_Uart_Device uartid,  
  CK_Uart_StopBit stopbit
)
{
  CKStruct_UartInfo *info;
	
  info = &(CK_Uart_Table[uartid]);	
  CK_INT32 timecount;
  timecount = 0;
  /* PEN bit(LCR[3]) is writeable when the UART is not busy(USR[0]=0).*/
  while((info->addr[CK_UART_USR] & USR_UART_BUSY) && 
        (timecount < UART_BUSY_TIMEOUT))
  {
    timecount++;
  }
  if(timecount >= UART_BUSY_TIMEOUT)
  {
    return FAILURE;
  }
  else
  {
    switch(info->stop)
    {
      case LCR_STOP_BIT_1:
        /* Clear the STOP bit to set 1 stop bit*/
        info->addr[CK_UART_LCR] &= LCR_STOP_BIT1;
        break;
				
      case LCR_STOP_BIT_2:
        /* 
         * If the STOP bit is set "1",we'd gotten 1.5 stop  
         * bits when DLS(LCR[1:0]) is zero, else 2 stop bits.
         */
         info->addr[CK_UART_LCR] |= LCR_STOP_BIT2;
         break;
				
      default:
	return FAILURE;
        break;
					
    }
  }
  info->stop = stopbit;
  return SUCCESS;
}
	
	
/*
 * We can use this function to reset the transmit data length,and we
 * have four choices:5, 6, 7, and 8 bits.
 * Parameters:
 * 	uartid--a basepointer, could be one of UART0, UART1, UART2 or UART3.
 * 	wordsize--the data length that user decides
 * return: SUCCESS or FAILURE
*/

CK_INT32 CK_Uart_SetWordSize(
  CK_Uart_Device uartid, 
  CK_Uart_WordSize wordsize)
{
  CKStruct_UartInfo *info;
  int timecount=0;

  info = &(CK_Uart_Table[uartid]);	
  /* DLS(LCR[1:0]) is writeable when the UART is not busy(USR[0]=0).*/
  while((info->addr[CK_UART_USR] & USR_UART_BUSY) &&
        (timecount < UART_BUSY_TIMEOUT))
  {
    timecount++;
  }
  if(timecount >= UART_BUSY_TIMEOUT)
  {
    return FAILURE;
  }
  else
  {
		
    /* The word size decides by the DLS bits(LCR[1:0]), and the 
     * corresponding relationship between them is:
     *    DLS   word size
     *	  00 -- 5 bits
     *		01 -- 6 bits
     *		10 -- 7 bits
     *		11 -- 8 bits
     */
    timecount = 0;
    switch(wordsize)
    {
      case WORD_SIZE_5:
        info->addr[CK_UART_LCR] &= LCR_WORD_SIZE_5;
        break;
				
      case WORD_SIZE_6:
        info->addr[CK_UART_LCR] &= 0xfd;
        info->addr[CK_UART_LCR] |= LCR_WORD_SIZE_6;
        break;
				
      case WORD_SIZE_7:
        info->addr[CK_UART_LCR] &= 0xfe;
        info->addr[CK_UART_LCR] |= LCR_WORD_SIZE_7;
        break;
               				
      case WORD_SIZE_8:
        info->addr[CK_UART_LCR]|= LCR_WORD_SIZE_8;
        break;
               				
      default:
        break;
    }			
  }
  info->word = wordsize;
  return SUCCESS;
}
	
	
/*
 * This function is used to set the transmit mode, interrupt mode or
 * query mode.
 * Parameters:
 * 	uartid--a basepointer, could be one of UART0, UART1, UART2 or UART3.
 *  bQuery--it indicates the transmit mode: TRUE - query mode, FALSE - 
 *  inerrupt mode
 * return: SUCCESS or FAILURE
*/

CK_INT32 CK_Uart_SetTXMode(CK_Uart_Device uartid, BOOL bQuery)
{
  CKStruct_UartInfo *info;
	
  info = &(CK_Uart_Table[uartid]);	
  CK_INT32 timecount;
  timecount = 0;
  while((info->addr[CK_UART_USR] & USR_UART_BUSY) && 
        (timecount < UART_BUSY_TIMEOUT))
  {
    timecount++;
  }
  if(timecount >= UART_BUSY_TIMEOUT)
  {
    return FAILURE;
  }
  else
  {
    if(bQuery)
    {
      /* When query mode, disable the Transmit Holding Register Empty
       * Interrupt. To do this, we clear the ETBEI bit(IER[1]).
       */
      info->addr[CK_UART_IER] &= (~IER_THRE_INT_ENABLE);
      /* Refresh the uart info: transmit mode - query.*/
      info->btxquery = TRUE;
    }
    else
    {
      /* When interrupt mode, inable the Transmit Holding Register 
       * Empty Interrupt. To do this, we set the ETBEI bit(IER[1]).
       */
      info->addr[CK_UART_IER] |= IER_THRE_INT_ENABLE;
      /* Refresh the uart info: transmit mode - interrupt.*/
      info->btxquery = FALSE;
    }
  }
  return SUCCESS;
}
	
	
/*
 * This function is used to set the receive mode, interrupt mode or
 * query mode.
 * Parameters:
 * 	uartid--a basepointer, could be one of UART0, UART1, UART2 or UART3.
 *  bQuery--it indicates the receive mode: TRUE - query mode, FALSE - 
 *  interrupt mode
 * return: SUCCESS or FAILURE

*/
CK_INT32 CK_Uart_SetRXMode(CK_Uart_Device uartid, BOOL  bQuery)
{
  CKStruct_UartInfo *info;
	
  info = &(CK_Uart_Table[uartid]);	
  CK_INT32 timecount;
  timecount = 0;
  /* PEN bit(LCR[3]) is writeable when the UART is not busy(USR[0]=0).*/
  while((info->addr[CK_UART_USR] & USR_UART_BUSY) && 
        (timecount < UART_BUSY_TIMEOUT))
  {
    timecount++;
  }
  if(timecount >= UART_BUSY_TIMEOUT)
  {
    return FAILURE;
  }
  else
  {
    if(bQuery)
    {
       /* When query mode, disable the Received Data Available 
       * Interrupt. To do this, we clear the ERBFI bit(IER[0]).
       */
      info->addr[CK_UART_IER] &= (~IER_RDA_INT_ENABLE);
      /* Refresh the uart info: receive mode - query.*/
      info->brxquery = TRUE;
    }
    else
    {
      /* When interrupt mode, inable the Received Data Available 
       * Interrupt. To do this, we set the ERBFI bit(IER[0]).
       */
      info->addr[CK_UART_IER] |= IER_RDA_INT_ENABLE;
      /* Refresh the uart info: receive mode - interrupt.*/
      info->brxquery = FALSE;
    }
  }
  return SUCCESS;
}


/*
 * Register uart into powermanager.
 */
CK_INT32 CK_Uart_DriverInit()
{
  CK_Deactive_UartModule();
  return SUCCESS;
}

	
/* This function is used to get character,in query mode or interrupt mode.
 * Parameters:
 * 	 uartid--a basepointer, could be one of UART0, UART1, UART2 or UART3.
 *   brxquery--it indicates the receive mode: TRUE - query mode, FALSE - 
 *   interrupt mode
 * return: SUCCESS or FAILURE
 */
CK_INT32 CK_Uart_GetChar(IN CK_Uart_Device uartid, OUT CK_UINT8 *ch)
{
  CKStruct_UartInfo *info;
  
  if ((uartid < 0) || (uartid >= UARTID_MAX))
  {
    return FAILURE;
  }
  info = &(CK_Uart_Table[uartid]);
  if (!(info->bopened))
  {
    return FAILURE;
  }

  /*query mode*/ 
  if (info->brxquery)
  {
    while (!(info->addr[CK_UART_LSR] & LSR_DATA_READY));
       
  *ch = info->addr[CK_UART_RBR];
  return SUCCESS;	
  }
  else
  { /*irq mode*/
    if(TRUE == CK_CircleBuffer_Read(&(info->rxcirclebuffer), ch))
    return SUCCESS;
  }
  return FAILURE;
}

/* This function is used to get character,in query mode or interrupt mode.
 * Parameters:
 *       uartid--a basepointer, could be one of UART0, UART1, UART2 or UART3.
 *   brxquery--it indicates the receive mode: TRUE - query mode, FALSE - 
 *   interrupt mode
 * return: SUCCESS or FAILURE
 */
CK_INT32 CK_Uart_GetCharUnBlock(IN CK_Uart_Device uartid, OUT CK_UINT8 *ch)
{
  CKStruct_UartInfo *info;

  if ((uartid < 0) || (uartid >= UARTID_MAX))
  {
    return FAILURE;
  }
  info = &(CK_Uart_Table[uartid]);
  if (!(info->bopened))
  {
    return FAILURE;
  }

  /*query mode*/
  if (info->brxquery)
  {
    if (info->addr[CK_UART_LSR] & LSR_DATA_READY)
    {
      *ch = info->addr[CK_UART_RBR];
      return SUCCESS;
    }
  }
  else
  { /*irq mode*/
    if(TRUE == CK_CircleBuffer_Read(&(info->rxcirclebuffer), ch))
    return SUCCESS;
  }
  return FAILURE;
}

/* This function is used to transmit character,in query mode or interrupt mode.
 * Parameters:
 * 	 uartid--a basepointer, could be one of UART0, UART1, UART2 or UART3.
 *   brxquery--it indicates the receive mode: TRUE - query mode, FALSE - 
 *   interrupt mode
 * Return: SUCCESS or FAILURE.
 */
CK_INT32 CK_Uart_PutChar(CK_Uart_Device uartid, CK_UINT8 ch)
{
  CKStruct_UartInfo *info;
  CK_UINT8 temp;

  if ((uartid < 0) || (uartid >= UARTID_MAX))
  {
    return FAILURE;
  }
  info = &(CK_Uart_Table[uartid]);
  if (!(info->bopened))
  {
    return FAILURE;
  }
  /*query mode*/
  if (info->btxquery)
  {
    while ((!(info->addr[CK_UART_LSR] & CK_LSR_TRANS_EMPTY)));
    if(ch == '\n')
    {
      info->addr[CK_UART_THR] = '\r';
      delay(10);
    }
    
    
    info->addr[CK_UART_THR] = ch;
    
    return SUCCESS;
  }
   
  /*irq mode*/
  else
  {
    if(ch == '\n')
    {
      CK_CircleBuffer_Write(&(info->txcirclebuffer), '\r');
      CK_CircleBuffer_Write(&(info->txcirclebuffer), ch);
     }
     else
     {
       CK_CircleBuffer_Write(&(info->txcirclebuffer), ch);
     } 
     if(info->addr[CK_UART_LSR] & 0x20)
     {
       CK_CircleBuffer_Read(&(info->txcirclebuffer), &temp);
       info->addr[CK_UART_THR] = temp;
     }
  }
  return SUCCESS;
}


/*
 * This function is the interrupt service function of uart
 * Parameters:
 *            irqid - Interrupt number of uart.
 * Return: NULL.
 */
static void CK_Uart_Interrupt(CK_UINT32 irqid)
{
  CKStruct_UartInfo *info;
  CK_INT8 int_state;
  CK_UINT8 txrxdata;
  CKEnum_Uart_Error error;
  CK_INT8 i;

  for(i = 0; i < UARTID_MAX; i++)
  {
    info = &(CK_Uart_Table[i]);
    if(info->irq == irqid)
    {
       break;
    }
  }
  if(i >= UARTID_MAX)
  {
    printf("Uart%d not exist\n",i);
  }
  int_state = info->addr[CK_UART_IIR] & 0xf;
  if((int_state == 0x2) && !(info->btxquery))
  {
    if(!CK_CircleBuffer_IsEmpty(&(info->txcirclebuffer)))
    {
      CK_CircleBuffer_Read(&(info->txcirclebuffer), &txrxdata);
      info->addr[CK_UART_THR] = txrxdata;
    }
  }
  if((int_state == 0x4) && !(info->brxquery))
  {
    txrxdata = info->addr[CK_UART_RBR];
    CK_CircleBuffer_Write(&(info->rxcirclebuffer), txrxdata);
    if(txrxdata == 3 )           /*CTRL+C ASCII code is 3 */
    {
      error = CK_Uart_CTRL_C;
      info->handler(error);
    }
  }
}

void CK_UART_ClearRxBuffer(CK_Uart_Device uartid)
{
  CKStruct_UartInfo *info;
  info = &(CK_Uart_Table[uartid]);
  CK_CircleBuffer_Clear(&(info->rxcirclebuffer));
}




