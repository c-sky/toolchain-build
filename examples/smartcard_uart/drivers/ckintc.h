/*
 * Description: ckintc.h - Define the structure and state the interface for 
 * interrupt controller.
 * 
 * Copyright (C) : 2008 Hangzhou C-SKY Microsystems Co.,LTD.
 * Author(s): Jianyong Jiang (jianyong_jiang@c-sky.com)
              Dongqi Hu  (dongqi_hu@c-sky.com)
 * Contributors: Chunqiang Li
 * Date:  2008-09-26
 * Modify by liu jirang(jirang_liu@c-sky.com)  on 2012-10-13
 */

#ifndef _CKINTC_H_
#define _CKINTC_H_

#include "cksmart.h"

/* define the registers structure of the interrupt controller */
typedef struct CKS_INTC
{
	CK_REG  REV0[64];
	CK_REG	ISER;
	CK_REG	REV1[15];
	CK_REG	IWER;
	CK_REG	REV2[15];
	CK_REG	ICER;
	CK_REG	REV3[15];
	CK_REG	IWDR;
	CK_REG	REV4[15];
	CK_REG	ISPR;
	CK_REG  REV5[31];
	CK_REG	ICPR;
	CK_REG  REV6[95];
	CK_REG	IPR[8];
}CKStruct_INTC, *PCKStruct_INTC;

 
#define PCK_INTC    ((PCKStruct_INTC)CK_INTC_BASEADDRESS)


/*
 *  Bit Definition for the PIC Interrupt control register
 */


#endif























