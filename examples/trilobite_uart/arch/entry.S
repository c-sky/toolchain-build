/*
 * entry.S:
 * CKCORE exception, normal interrupt and fast interrupt entries.
 *
 * Copyright (C) 2012  Hangzhou C-SKY Microsystems Co., Ltd
 * Modify by liu jirang  on 2012-09-11
 */

#include "ck810.h"

.global default_exception_handler
.global hw_vsr_default_exception
.global hw_vsr_autovec
.global hw_vsr_fastautovec
.global hw_vsr_tlbmiss


.extern CK_Default_Exception_Handler   
.extern CK_INTC_InterruptService 
.extern CK_INTC_FastInterruptService


/*
 * default exception service routine, before r0 initialized
 */
	.text
	.balign 4
default_exception_handler:
	br	default_exception_handler
	rte

/*
 * Common exception  handler. Standard exceptions come through here first
 * tlb miss exception
 */
#if CONFIG_CKCPU_MMU
	.text
	.balign 4
hw_vsr_tlbmiss:

	/* save context */
	mtcr    a3, ss1
	mtcr    a2, ss2
	mtcr    a1, ss3
	mtcr    a0, ss4

	/* PFN is __origin ( + page size) or not */
	mfcr    a3, cr<4, 15>
	bclri	a3,	24
	lsri	a2, a3, 25   // 16M
	lrw     a1, __origin
	bclri	a1,	24
	lsri	a0, a1, 25   // 16M
	cmpne   a2, a0
	bf      2f

  /* not */
1:
	movi    a2, 0x00000016  //C = 010, D = 1, V = 1, G = 0, pfn = 0x0
	or      a3, a2
	mtcr    a3, cr<2, 15>  // MEL0
	bseti   a3, 24      // 16M
	mtcr    a3, cr<3, 15>  // MEL1
	bgeni   a2, 28     /* TLBWR */
	mtcr    a2, cr<8, 15>

	mfcr	a3, ss1
	mfcr	a2, ss2
	mfcr	a1, ss3
	mfcr	a0, ss4
	rte                      /*   Restore the psr and pc     */

  /* PFN is __origin ( + page size) */
2:
	mfcr	a3,	cr<4, 15>
	mtcr    a1, cr<4, 15>   // probe 0x04000000
	bgeni   a2, 31     /* TLBP */
	mtcr    a2, cr<8, 15>   
	mtcr    a3, cr<4, 15>   // set new vpn
	bclri	a3, 24          // MEL0 16M
	mfcr    a1, cr<0, 15>
	btsti   a1, 31
	bt      1b
	movi    a2, 64
	xor     a1, a2
	mtcr    a1, cr<0, 15>
	movi    a1, 0x00000016  //C = 010, D = 1, V = 1, G = 0, pfn = 0x0
	or      a3, a1
	mtcr    a3, cr<2, 15>	// MEL0
	bseti   a3, 24			// 16M
	mtcr    a3, cr<3, 15>	// MEL1
	bgeni   a1, 28     /* TLBWI */
	mtcr    a1, cr<8, 15>

	mfcr	a3, ss1
	mfcr	a2, ss2
	mfcr	a1, ss3
	mfcr	a0, ss4
	rte
#endif  /*CONFIG_CKCPU_MMU*/


/*
 * Common exception  handler. Standard exceptions come through here first
 */
	.text
	.balign 4
hw_vsr_default_exception:
	/* save context */
	subi    sp, 28             /* Allocate space for all registers */
	stw     a0, (sp, 0)
	stw     a1, (sp, 4)
	stw     a2, (sp, 8)
	stw     a3, (sp, 12)
	stw     t0, (sp, 16)
	stw     t1, (sp, 20)
	/* local registers need not be saved */
	stw     lr, (sp, 24)

	subi    sp, 8
	mfcr    a3, epsr
	stw     a3, (sp, 4)	/* save epsr registwr */
	mfcr    a2, epc
	stw     a2, (sp, 0)	/* save epc register */

	// enable ie ee for exception nesting
	psrset	ie, ee

	mfcr    a0, psr		/* Get psr register */
	lsri    a0, 16		/* Get vector in 7 bits */
	sextb   a0			/* Fill upper bytes with zero */
	mov     a1, sp		/* pass stack point to r1*/
	bsr    CK_Default_Exception_Handler   /* exception   VSR.*/

	ldw     a3, (sp, 0)
	mtcr    a3, epc		/* restore the epc */
	ldw     a2, (sp, 4)
	mtcr    a2, epsr	/* restore the epsr */
	addi    sp, 8

	/* restore all the regs */
	ldw     a0, (sp, 0)
	ldw     a1, (sp, 4)
	ldw     a2, (sp, 8)
	ldw     a3, (sp, 12)
	ldw     t0, (sp, 16)
	ldw     t1, (sp, 20)
	/* local registers need not be saved */
	ldw     lr, (sp, 24)
	addi    sp, 28

	rte

/*
 * Normal interrupt vector handler
 */
	.text
	.balign 4
hw_vsr_autovec:
	/* save context */
	subi    sp, 28             /* Allocate space for all registers */
	stw     a0, (sp, 0)
	stw     a1, (sp, 4)
	stw     a2, (sp, 8)
	stw     a3, (sp, 12)
	stw     t0, (sp, 16)
	stw     t1, (sp, 20)
	/* local registers need not be saved */
	stw     lr, (sp, 24)

	subi    sp, 8
	mfcr    a3, epsr
	stw     a3, (sp, 4)	/* save epsr registwr */
	mfcr    a2, epc
	stw     a2, (sp, 0)	/* save epc register */

	/* read the interrupt vector number from interrupt status register */
	lrw     a3, CK_INTC_BASEADDRESS
	ldw     a0, (a3, 0x0)
	movi    a2, 0x7f
	and     a0, a2
	bsr     CK_INTC_InterruptService

	ldw     a3, (sp, 0)
	mtcr    a3, epc		/* restore the epc */
	ldw     a2, (sp, 4)
	mtcr    a2, epsr	/* restore the epsr */
	addi    sp, 8

	/* restore all the regs */
	ldw     a0, (sp, 0)
	ldw     a1, (sp, 4)
	ldw     a2, (sp, 8)
	ldw     a3, (sp, 12)
	ldw     t0, (sp, 16)
	ldw     t1, (sp, 20)
	/* local registers need not be saved */
	ldw     lr, (sp, 24)
	addi    sp, 28

	rte

/*
 * Fast interrupt vector handler.
 */
	.text
	.balign 4
hw_vsr_fastautovec:
	/* read the interrupt vector number from interrupt status register */
	lrw     a3, CK_INTC_BASEADDRESS
	ldw     a0, (a3, 0x0)
	movi    a2, 0x7f
	and     a0, a2
	bsr     CK_INTC_FastInterruptService
	rfi		      /*   Restore the psr and pc     */

