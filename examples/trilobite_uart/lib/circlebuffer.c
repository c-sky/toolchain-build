/*
 * Copyright (C): 2008 Hangzhou C-SKY Microsystem Co.,LTD.
 * Author: Lu Yongjiang  (yongjiang_lu@c-sky.com)
 * Contrbutior: Chunqiang Li
 * Date: 2008-10-28
 */
#include "datatype.h"
#include "circlebuffer.h"

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
        )
{
  pcirclebuffer->Buffer = buffer;
  pcirclebuffer->BufferSize = buffersize;
  pcirclebuffer->ReadPtr = pcirclebuffer->WritePtr = 0;
}

/*
 *clear the circlebuffer's write and read buffer,
 *restrore the Read position and  write position  to initial position
 *
 * pcirclebuffer :point to the circlebuffer
 */
void CK_CircleBuffer_Clear( PCKStruct_CircleBuffer pcirclebuffer)
{
  pcirclebuffer->ReadPtr = pcirclebuffer->WritePtr = 0;
}

/*
 * judge the circlebuffer is empty,if empty return TRUE else reutn FALSE.
 *
 * pcirclebuffer :point to the circlebuffer
 */

BOOL CK_CircleBuffer_IsEmpty(PCKStruct_CircleBuffer pcirclebuffer)
{
  return( pcirclebuffer->ReadPtr == pcirclebuffer->WritePtr);
}

/*
 * judge the circlebuffer is full,if full return TRUE else reutn FALSE.
 *
 * pcirclebuffer :point to the circlebuffer
 */
BOOL CK_CircleBuffer_IsFull(PCKStruct_CircleBuffer pcirclebuffer)
{
  return((pcirclebuffer->WritePtr + 1) % pcirclebuffer->BufferSize == pcirclebuffer->ReadPtr);
}

/*
 * if circlebuffer not empty then read a char from circlebuffer
 *
 *pcirclebuffer: point to the circlebuffer
 *ch           : pos to put the read ch
 *return value : read a char success then return TRUE else reture FALSE		
 */
 
BOOL CK_CircleBuffer_Read(PCKStruct_CircleBuffer pcirclebuffer,CK_UINT8* ch)
{
  if (CK_CircleBuffer_IsEmpty(pcirclebuffer))
    return FALSE;
  *ch = pcirclebuffer->Buffer[pcirclebuffer->ReadPtr];
  pcirclebuffer->ReadPtr = (pcirclebuffer->ReadPtr + 1) % pcirclebuffer->BufferSize;
  return TRUE;
}

/*
 * if circlebuffer not full then write a char to circlebuffer
 *
 *pcirclebuffer: point to the circlebuffer
 *ch           : the char will write to circlebuffer
 *return value : write success then return TRUE else reture FALSE   
 */
BOOL CK_CircleBuffer_Write(PCKStruct_CircleBuffer pcirclebuffer,CK_UINT8 ch)
{
  if(CK_CircleBuffer_IsFull(pcirclebuffer))
     return FALSE;
  pcirclebuffer->Buffer[pcirclebuffer->WritePtr] = ch;
  pcirclebuffer->WritePtr = (pcirclebuffer->WritePtr + 1) % pcirclebuffer->BufferSize;
  return SUCCESS; 

}

