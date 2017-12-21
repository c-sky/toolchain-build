/*
 * crt0.S -- startup codes for CK-CPU.
 *
 * Define a exception vector table
 *
 * Initial PSR register.
 * Initial VBR register, relocate exception vector table.
 * Initial sp(stack pointer) register.
 * Initial BSS section to "0"
 * Then goto "main".
 *
 * Copyright (C) 2008~2015  Hangzhou C-SKY Microsystems Co., Ltd
 */

#include "cksmart.h"

.file "crt0.S"

/*
 * For importing variable or functions from script file "ckcpu.ld".
 */
.import __stack		/* The stack pointer from linking script file */
.import	__sbss		/* The end of bss from linking script file */
.import __ebss		/* The end of bss from linking script file */

/*
 * For importing variable or functions from other c or assemble files.
 */
.import main				/* The c codes entry */

/*
 * For importing variable or functions from entry.S.
 */
.import default_exception_handler /* default exception service routine */

/* For exporting varialbe or functions */
.export	ckcpu_vsr_table	/* Vector table base address. */
.export __start				/* The system entry. */

.section .exp_table
/* Vector table space. */

.align 10
ckcpu_vsr_table:

.long __start
.rept 127
.long default_exception_handler
.endr

/* The ckcpu startup codes. */
.text
	/*
	 *	
	 * This is the codes first entry point. This is where it all
	 * begins...
	 */

__start:
	/*
	 * Init psr value, enable exception, disable interrupt and fast interrupt.
	 * psr = 0x80000100
	 */
	lrw		a3,	0x80000100
	mtcr	a3, psr
	
	/*
	 * Setup initial vector base table for interrupts and exceptions
	 */
	lrw		a2, ckcpu_vsr_table
	mtcr	a2, vbr
	
	/* Initialize the normal stack pointer from the linker definition. */
	lrw		a1, __stack
	mov		sp, a1

	/*
	 * Zero out the bss region.
	 * NOTE: __sbss must align 4
	 */
	lrw		a3, __sbss	/* Get start of bss from linking script file */
	lrw		a2, __ebss	/* Get end of bss from linking script file */
	subu	a2, a3		/* Calculate size of bss */
	lsri	a2, 2		/* Size of whole words */
	cmpnei	a2, 0
	bf		__goto_c
	movi	a1, 0		/* Set zero value to write */
2:
	stw		a1, (a3)	/* Zero next word */
	addi	a3, 4		/* Increase bss pointer */
	subi	a2,	1		/* Decrease counter */
	cmpnei	a2,	0
	bt		2b			/* Repeat for all bss */
	
	/*
	 * Assember start up done, C codes start here.
	 */
__goto_c:
	bsr		main
	
	/* Should never get here. */
__exit:
	br	__exit
