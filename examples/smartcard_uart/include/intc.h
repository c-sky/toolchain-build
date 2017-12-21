/*
 *  intr.h - Define the struct and interface for interrupt controller
 *
 *  Copyright (C):  2008 Hangzhou C-SKY Microsystems Co.,LTD.
 *  Author: Dongqi Hu  (dongqi_hu@c-sky.com)
 *          Jianyong Jiang  (jianyong_jiang@c-sky.com)
 *  Contributiors: Chunqiang Li  
 *  Date: 2008-09-26
 *  Modify by liu jirang(jirang_liu@c-sky.com)  on 2012-10-13
 */           

#ifndef _INTR_H_
#define _INTR_H_

#include "datatype.h"

#define CKCORE_VECTOR_SYS  32
#define CK_INTC_COUNT      32
#define CK_INTC_PRIO_LEVEL 4

// VSR table
extern  volatile unsigned int ckcpu_vsr_table[64];

/* define the data structure of interrupt description */
typedef struct CKS_IRQ_Handler{
      char        *devname;
      CK_UINT32   irqid;
      CK_UINT32    priority;
      void        (*handler)(CK_UINT32 irqid);
}CKStruct_IRQHandler, *PCKStruct_IRQHandler;

/* Statement of those functions which are used in intc.c*/
void CK_CPU_EnterCritical(CK_UINT32 *psr);
void CK_CPU_ExitCritical(CK_UINT32 psr);
void CK_INTC_EnNormalIrq(IN CK_UINT32 priority);
void CK_INTC_DisNormalIrq(IN CK_UINT32 priority);
CK_INT32 CK_INTC_RequestIrq(PCKStruct_IRQHandler priqhandler);
CK_INT32 CK_INTC_FreeIrq(INOUT PCKStruct_IRQHandler priqhandler);
void CK_CPU_EnAllNormalIrq(void);
void CK_CPU_DisAllNormalIrq(void);

#endif
