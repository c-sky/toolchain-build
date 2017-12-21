/*
 *  intr.h - Define the struct and interface for interrupt controller
 *
 *  Copyright (C):  2008 Hangzhou C-SKY Microsystems Co.,LTD.
 *  Author: Dongqi Hu  (dongqi_hu@c-sky.com)
 *          Jianyong Jiang  (jianyong_jiang@c-sky.com)
 *  Contributiors: Chunqiang Li  
 *  Date: 2008-09-26
 *  Modify by liu jirang  on 2012-09-11
 */           

#ifndef _INTR_H_
#define _INTR_H_

#include "datatype.h"

#define CKCORE_VECTOR_SYS  32
#define CKCORE_VECTOR_AUTOVEC 10
#define CKCORE_VECTOR_FASTAUTOVEC  11
#define CKCORE_VECTOR_TLBMISS 14

/* define the data structure of interrupt description */
typedef struct CKS_IRQ_Handler{
      char        *devname;
      CK_UINT32   irqid;
      CK_UINT32    priority;
      void        (*handler)(CK_UINT32 irqid);
      BOOL        bfast;  
      struct CKS_IRQ_Handler  *next;  
}CKStruct_IRQHandler, *PCKStruct_IRQHandler;

// VSR table
extern  volatile unsigned int ckcpu_vsr_table[128];
/* Statement of those functions which are used in intc.c*/
void CK_CPU_EnAllNormalIrq(void);
void CK_CPU_DisAllNormalIrq(void);
void CK_CPU_EnAllFastIrq(void);
void CK_CPU_DisAllFastIrq(void);
void CK_CPU_EnterCritical(CK_UINT32 *psr);
void CK_CPU_ExitCritical(CK_UINT32 psr);
void CK_INTC_EnNormalIrq(IN CK_UINT32 priority);
void CK_INTC_DisNormalIrq(IN CK_UINT32 priority);
void CK_INTC_EnFastIrq(IN CK_UINT32 priority); 
void CK_INTC_DisFastIrq(IN CK_UINT32 priority);
void CK_INTC_MaskNormalIrq(IN CK_UINT32 primask);
void CK_INTC_UnMaskNormalIrq(void);
void CK_INTC_MaskFastIrq(IN CK_UINT32 primask);
void CK_INTC_UnMaskFastIrq(void);
CK_INT32 CK_INTC_RequestIrq(PCKStruct_IRQHandler priqhandler);
CK_INT32 CK_INTC_FreeIrq(INOUT PCKStruct_IRQHandler priqhandler);

#endif
