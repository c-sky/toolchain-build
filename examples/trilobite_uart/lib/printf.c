
#include "stdarg.h"
#include "uart.h"

extern CK_Uart_Device consoleuart;

/******************************************************
*change the number to string
*
* uq : the number need to change
* base: the base of system(for example 2,8,10,16 as usual)
* buf: data buffer for change procedure and return result
* return value: the string  after change 
*********************************************************/
static char *numtostring (unsigned int uq, int base, char *buf )
{                               
  register char *p, *p0;
  int n = 0, i;

  p = buf;
  *buf = 0;
  do 
  {
    *buf ++ = "0123456789abcdef"[uq % base];
    n++;
  } while (uq /= base);
  p[n] = '\0';
        
  p0 = ++buf;
  if (base == 16 && n < 8)  //If Hex, the length is fixxed with 8 digitals
  {
    for (i = 0; i < 8 - n; i++)
    {
      p0[i] = '0';
    }
    for (; i < 8; i++)
    {
      p0[i] = p[8 - i - 1];
    }
    p0[8] = '\0';
  }
  else
  {
    for (i = 0; i < n; i++)
    {
      p0[i] = p[n - i - 1];
    }
    p0[n] = '\0';
  }

  return (p0);
}

/*
 * display the char on the console
 * ch: the char need to display
 */
int putchar(int ch)
{
  while(CK_Uart_PutChar(consoleuart,ch) != SUCCESS);
  return 0;
}

/*
 * display a string on the console
 * ptr: the string need to display
 */
int puts(const char *ptr)
{
   while(*ptr !='\0')
   {
     if (SUCCESS == CK_Uart_PutChar(consoleuart,*ptr))
       ptr++;
   }
   CK_Uart_PutChar(consoleuart,'\n');
   return 0;
}

/*
 * display a string on the console
 * ptr: the string need to display
 */
static int puts_without_enter(const char *ptr)
{
   while(*ptr !='\0')
   {
     if (SUCCESS == CK_Uart_PutChar(consoleuart,*ptr))
       ptr++;
   }
   return 0;
}

/*
 * receive a char from the console
 *return value: the char received from the console
 */
int getchar(void)
{
  CK_UINT8 ch;
  while(CK_Uart_GetChar(consoleuart,&ch) != SUCCESS);
  return ch;
}

/*
 * print the result after translated according to the format
 */
int printf ( const char *fmt, ... )
{
  const char *s;
  int        value;
  CK_UINT32        ptr;
  char       ch, buf[64], *pbuf;
  va_list    ap;

  va_start(ap, fmt);
  while (*fmt) 
  {
    if (*fmt != '%')
    {
      putchar(*fmt++);
      continue;
    }

    switch (*++fmt)
    {
      case 's':
        s = va_arg(ap, const char *);
         puts_without_enter(s);
         break;
      case 'd':
         value = va_arg(ap, int);
         if (value < 0)
         {
            putchar('-');
            value = 0 - value;
         }
         pbuf = numtostring((unsigned int)value, 10, buf);
         puts_without_enter(pbuf);
         break;
       case 'x':
         value = va_arg(ap,int);
         pbuf = numtostring((unsigned int)value, 16, buf);
         puts_without_enter(pbuf);
         break;
       case 'c':
          ch = (unsigned char)va_arg(ap, int);
          pbuf = &ch;     
          putchar(*pbuf);                         
          break;                  
//     case 'f':
//       f = va_arg(ap, float);
//       sprintf(buf, "%f\0", f);      
//       for (s = buf; *s; s ++)
//       {     
//          putchar(*s);                              
//        }
//        break;        
       case 'p':
         ptr = (unsigned) va_arg(ap, void *); 
         pbuf = numtostring(ptr, 16, buf);
         puts_without_enter(pbuf);
         break;  
       default:  
         putchar(*fmt);
         break;
    }
    fmt ++;
  }
  va_end(ap);
  return 0x01;   
}


