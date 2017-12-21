/*
 * File: misc.h 
 * Description: declare some base functions
 *
 *
 * Copyright (C):  2008 C-SKY Microsystem  Ltd.
 * Author(s): Yongjiang Lu   (yongjiang_lu@c-sky.com)
 * Contributors: Chunqiang Li 
 * Date:         2008-9-26
 */
#ifndef __MISC_H__ 
#define __MISC_H__

#include "datatype.h"

/* 
 * translate small letter in string  to capital letter 
 */
char* toupper(char* str);

/* 
 * translate capital letter in string  to small letter 
 */
char* tolower(char* str);

/* 
 * translate capital letter to small letter, or else 
 */
char invertchar(char c);

/* 
 * translate string to BCD codes 
 */
CK_UINT8 asciitobcd(CK_UINT8 ascii);

/* 
 * translate string to hex 
 * 
 * pt: point to the string you want to translate
 */
CK_UINT32 asciitohex(CK_UINT8 *pt);

/* 
 * translate string to dec 
 *
 * pt: point to the string you want to translate
 */
CK_UINT32 asciitodec(CK_UINT8 *pt);

/* 
 * translate string to num, both hex and dec 
 *
 * pt: point to the string you want to translate
 */
CK_UINT32 asciitonum(CK_UINT8 *pt);
#define aton(str) asciitonum(str)

void delay ( int sec );

int printf ( const char *fmt, ... );
/*
 * display the char on the console
 */
int putchar(int ch);

/*
 * display a string on the console
 */
int puts(const char *ptr);

/*
 * receive a char from the console
 */
int getchar(void);

/*
 * Use for user's reply, y or n.
 * Waiting for user to input with an end of ENTER key.
 * If it's 'y', return 1; else if 'n', return 0; others 2.
 */
CK_INT32 CK_WaitForReply();

#if DEBUG 
      #define dbg_printf  printf
#else
      #define dbg_printf
#endif

#define DEST_NOR_FLASH  0
#define DEST_NAND_FLASH 1
#define DEST_MEMORY     2

#endif
