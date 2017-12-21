/*
 * File : ckuart.h
 * Description: this file contains the macros support uart operations
 * Copyright (C):  2008 C-SKY Microsystem  Ltd.
 * Author(s):   Shuli wu  
 * E_mail:  shuli_wu@c-sky.com
 * Contributors: Yun Ye 
 * Date:  2008-9-25       
 */


#ifndef __CKUART_H__
#define __CKUART_H__

#include "ck810.h"
#include "datatype.h"
#include "uart.h"
#include "circlebuffer.h"
#include "intc.h"

/* UART registers addr definition */
#define CK_UART_RBR       0x00    /* Receive Buffer Register (32 bits, R) */
#define CK_UART_THR       0x00    /* Transmit Holding Register (32 bits, W) */
#define CK_UART_DLL       0x00    /* Divisor Latch(Low)  (32 bits, R/W) */
#define CK_UART_IER       0x01    /* Interrupt Enable Register (32 bits, R/W) */
#define CK_UART_DLH       0x01    /* Divisor Latch(High) (32 bits, R/W) */
#define CK_UART_IIR       0x02    /* Interrupt Identity Register (32 bits, R) */
#define CK_UART_FCR       0x02    /* fifo Countrol Register (32 bits, W) */
#define CK_UART_LCR       0x03    /* Line Control Register (32 bits, R/W) */
#define CK_UART_MCR       0x04    /* Modem Control Register (32 bits, W) */
#define CK_UART_LSR       0x05    /* Line Status Register (32 bits, R) */
#define CK_UART_MSR       0x06    /* Modem Status Register (32 bits, R/W) */
#define CK_UART_USR       0x1f    /* UART Status Register (32 bits, R/W) */


#define UART_BUSY_TIMEOUT      1000000
#define UART_RECEIVE_TIMEOUT   1000
#define UART_TRANSMIT_TIMEOUT  1000


/* UART register bit definitions */
/* CK5108 */

#define USR_UART_BUSY           0x01
#define LSR_DATA_READY          0x01
#define LSR_THR_EMPTY           0x20
#define IER_RDA_INT_ENABLE      0x01
#define IER_THRE_INT_ENABLE     0x02
#define IIR_NO_ISQ_PEND         0x01

#define LCR_SET_DLAB            0x80       /* enable r/w DLR to set the baud rate */
#define LCR_PARITY_ENABLE	    0x08       /* parity enabled */
#define LCR_PARITY_EVEN         0x10   /* Even parity enabled */
#define LCR_PARITY_ODD          0xef   /* Odd parity enabled */
#define LCR_WORD_SIZE_5         0xfc   /* the data length is 5 bits */
#define LCR_WORD_SIZE_6         0x01   /* the data length is 6 bits */
#define LCR_WORD_SIZE_7         0x02   /* the data length is 7 bits */
#define LCR_WORD_SIZE_8         0x03   /* the data length is 8 bits */
#define LCR_STOP_BIT1           0xfb   /* 1 stop bit */
#define LCR_STOP_BIT2           0x04  /* 1.5 stop bit */

#define CK_LSR_PFE              0x80     
#define CK_LSR_TEMT             0x40
#define CK_LSR_THRE             0x40
#define	CK_LSR_BI               0x10
#define	CK_LSR_FE               0x08
#define	CK_LSR_PE               0x04
#define	CK_LSR_OE               0x02
#define	CK_LSR_DR               0x01
#define CK_LSR_TRANS_EMPTY      0x20

#define CK_UART0_IRQID    CK_INTC_UART0
#define CK_UART1_IRQID    CK_INTC_UART1
#define CK_UART2_IRQID    CK_INTC_UART2

/*config the uart */

#define CK_UART_TXBUFFERSIZE 4096
#define CK_UART_RXBUFFERSIZE 4096
typedef struct CK_UART_Info_t {
  CK_UINT32 id;
  volatile CK_UINT32* addr;
  CK_UINT32 irq ;
  BOOL bopened;
  void  (* handler)(CK_INT8 error);
  CK_Uart_Baudrate baudrate;
  CK_Uart_Parity parity;
  CK_Uart_WordSize word;
  CK_Uart_StopBit stop; 
  BOOL btxquery; 
  BOOL brxquery; 
  CK_UINT8 txbuffer[CK_UART_TXBUFFERSIZE];
  CK_UINT8 rxbuffer[CK_UART_RXBUFFERSIZE];
  CKStruct_CircleBuffer txcirclebuffer; 
  CKStruct_CircleBuffer rxcirclebuffer;
  CKStruct_IRQHandler irqhandler;
} CKStruct_UartInfo, *PCKStruct_UartInfo;

#endif
