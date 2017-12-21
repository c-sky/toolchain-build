/*
 *circlebuffer.h - define structure and declare some function
 *	for circlebuffer.		
 *
 * Copyright (C): 2008 Hangzhou C-SKY Microsystem Co.,LTD.
 * Author: Lu Yongjiang  (yongjiang_lu@c-sky.com)
 * Contrbutior: Chunqiang Li
 * Date: 2008-10-28
 */

#ifndef __CIRCLEBUFFER_H_
#define __CIRCLEBUFFER_H_

#include "datatype.h"

typedef struct
{
  CK_UINT8 	*Buffer;
  CK_INT32	BufferSize;
  CK_INT32	ReadPtr;
  CK_INT32	WritePtr;
} CKStruct_CircleBuffer, *PCKStruct_CircleBuffer;


/*
 *initial the circlebuffer:set the circlebuffer buffer,BufferSize,
 *initial the Read position and  write position 
 *
 *pcirclebuffer : the circlebuffer need to initial
 *buffer :        the buffer needed by the circlebuffer
 *buffersize:     the size of buffer
 */
void CK_CircleBuffer_Init(
			PCKStruct_CircleBuffer pcirclebuffer,
			CK_UINT8 * buffer,
			CK_INT32 buffersize
			);


/*
 *clear the circlebuffer's write and read buffer,
 *restrore the Read position and  write position  to initial position
 *
 * pcirclebuffer :point to the circlebuffer
 */
void CK_CircleBuffer_Clear( PCKStruct_CircleBuffer pcirclebuffer);

/*
 * judge the circlebuffer is empty,if empty return TRUE else reutn FALSE.
 *
 * pcirclebuffer :point to the circlebuffer
 */
BOOL CK_CircleBuffer_IsEmpty(PCKStruct_CircleBuffer pcirclebuffer);

/*
 * judge the circlebuffer is full,if full return TRUE else reutn FALSE.
 *
 * pcirclebuffer :point to the circlebuffer
 */
BOOL CK_CircleBuffer_IsFull(PCKStruct_CircleBuffer pcirclebuffer); 

/*
 * if circlebuffer not empty then read a char from circlebuffer
 *
 *pcirclebuffer: point to the circlebuffer
 *ch           : pos to put the read ch
 *return value : read a char success then return TRUE else reture FALSE         
 */
BOOL CK_CircleBuffer_Read(PCKStruct_CircleBuffer pcirclebuffer,CK_UINT8* ch);

/*
 * if circlebuffer not full then write a char to circlebuffer
 *
 *pcirclebuffer: point to the circlebuffer
 *ch           : the char will write to circlebuffer
 *return value : write success then return TRUE else reture FALSE   
 */
BOOL CK_CircleBuffer_Write(PCKStruct_CircleBuffer pcirclebuffer,CK_UINT8 ch);

#endif
