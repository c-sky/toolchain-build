/*
 * Copyright (C): 2008 Hangzhou C-SKY Microsystem Co.,LTD.
 * Author: Lu Yongjiang  (yongjiang_lu@c-sky.com)
 * Contrbutior: Chunqiang Li
 * Date: 2008-10-28
 */


#include <uart.h>

extern CK_Uart_Device consoleuart;
/* 
 * translate capital letter to small letter, or else 
 *
 * c     : the letter need to be translated
 *return value: the letter after translated
 */
char invertchar(char c)
{
  if(c <= 'z' && c >= 'a')
    return (c - 32);
  if(c < 'Z' && c > 'A')
    return (c + 32);
  return c;
}

/* 
 * translate capital letter in string  to small letter
 * str : the string need to be translated
 * return value : the string after translated
 */
char *tolower(char *str)
{
  char *sstr = str;

  if (!str)
  {
    return str;
  }
  for( ; *sstr ; sstr++)
  {
    if(*sstr<='Z' && *sstr >= 'A')
    {
      *sstr = *sstr + 32;
    }
  }
  return str;
}

/* 
 * translate small letter in string  to capital letter
 * str : the string need to be translated
 * return value : the string after translated 
 */
char *toupper(char *str)
{
  char *sstr = str;
  
  if (!str)
  {
    return str;
  }
  for( ; *sstr ; sstr++)
  {
     if(*sstr <= 'z' && *sstr >= 'a')
     {
       *sstr = *sstr - 32;
     }
  }
  return str;
}

/* 
 * translate ASCII code to BCD code
 * ascii : the ASCII code need to be translated 
 * return value: the BCD code correspond with the ASCII code
 */
CK_UINT8 asciitobcd(CK_UINT8 ascii)
{
  CK_UINT8  bcd = 0;
  if((ascii >= '0') && (ascii <= '9'))
  {
    bcd = ascii - '0';
  }
  else if((ascii >= 'A') && (ascii <= 'F'))
  {
    bcd = ascii - 'A' + 10;
  }
  else if((ascii >= 'a') && (ascii <= 'f'))
  {
    bcd = ascii - 'a' + 10;
  }

   return bcd;
}

/* 
  * translate string to hex 
  * 
  * pt: point to the string you want to translate
  * return value: the hex data correspond with the string
  */
CK_UINT32 asciitohex(CK_UINT8 *pt)
{
  CK_UINT32 hex=0;
  CK_UINT8 bcd;

  if (!pt)
  {
    return 0;
  }
  while(*pt) 
  {
    bcd = asciitobcd(*pt++);
    hex = hex << 4;
    hex = hex + bcd;
  }

  return hex;
}

/* 
  * translate string to dec 
  *
  * pt: point to the string you want to translate
  * return value: the decimal data correspond with the string
  */
CK_UINT32 asciitodec(CK_UINT8 *pt)
{
  CK_UINT32 dec=0;
  CK_UINT8 bcd;

  if (!pt)
  {
    return 0;
  }

  while(*pt) 
  {
    bcd = asciitobcd(*pt++);
    dec*=10;
    dec = dec + bcd;
  }

  return dec;
}

/* 
 * translate the string to num, both hex and dec 
 *
 * pt: point to the string you want to translate
 * retunr value: the number after translated
 */
CK_UINT32 asciitonum(CK_UINT8 *pt)
{
  if (!pt)
  {
    return 0;
  }

  if((pt[0]=='0')&&(pt[1]=='x'||pt[1]=='X'))
    return asciitohex(&pt[2]);
  return asciitodec(pt);
}
/*
 * wait some time
 *sec :how much second need wait;
 *
 */
void delay ( int sec )
{
    int i;
    volatile int j;

    for (i = 0x00; i < sec * 100; i ++)
        j = i;
}

/*
 * Use for user's reply, y or n.
 * Waiting for user to input with an end of ENTER key.
 * If it's 'y', return 1; else if 'n', return 0; others 2.
 */
CK_INT32 CK_WaitForReply()
{
  CK_UINT8 i;
  CK_UINT8 ch;
  char answer[20];

  for(i = 0; i < 20; i++)
  {
    answer[i] = '\0';
  }
  i = 0;
  while(1)
  {
    if(SUCCESS == CK_Uart_GetChar(consoleuart, &ch))
    {
      if (ch == '\n' || ch == '\r')
      {
        answer[i] = '\0';
        break;
      }
       if(ch == '\b')
      {
         if(i > 0)
         {
           i--;
           CK_Uart_PutChar(consoleuart,ch);
         }
      }
      else
      {
        answer[i++] = ch;
        CK_Uart_PutChar(consoleuart,ch);
      }
    }
  }
  if((i == 1) && (answer[0] == 'y'))
  {
    return 1;
  }
  else if((i == 1) && (answer[0] == 'n'))
  {
    return 0;
  }
  return 2;
}
