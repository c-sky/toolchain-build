/*
 * Description: ckintc.h - Define the structure and state the interface for 
 * interrupt controller.
 * 
 * Copyright (C) : 2008 Hangzhou C-SKY Microsystems Co.,LTD.
 * Author(s): Jianyong Jiang (jianyong_jiang@c-sky.com)
              Dongqi Hu  (dongqi_hu@c-sky.com)
 * Contributors: Chunqiang Li
 * Date:  2008-09-26
 */

#ifndef _CKINTC_H_
#define _CKINTC_H_

#include "ck810.h"

/* define the registers structure of the interrupt controller */
typedef struct CKS_INTC
{
  CK_REG    ICR_ISR;
  CK_REG    Rev0;
  CK_REG    IFR;
  CK_REG    IPR;
  CK_REG    NIER;
  CK_REG    NIPR;
  CK_REG    FIER;
  CK_REG    FIPR;
  CK_REG    Rev[8];
  CK_REG    PR[8];
}CKStruct_INTC, *PCKStruct_INTC;

 
#define PCK_INTC    ((PCKStruct_INTC)CK_INTC_BASEADDRESS)


/*
 *  Bit Definition for the PIC Interrupt control register
 */
#define ICR_AVE   0x80000000  /* Select vectored interrupt */
#define ICR_FVE   0x40000000  /* Unique vector number for fast vectored*/
#define ICR_ME    0x20000000  /* Interrupt masking enabled */
#define	ICR_MFI	  0x10000000  /* Fast interrupt requests masked by MASK value */


#endif























