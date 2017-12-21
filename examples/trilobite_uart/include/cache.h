/*
 * cache.h - CKCORE cpu cache flush interface
 * 
 * Copyright (C): 2008 2009 Hangzhou C-SKY Microsystem Co.,LTD.
 * Author: Ye Yun  (yun_ye@c-sky.com)
 * Contrbutior: Chunqiang Li
 * Date: 2008-12-29
 */

#ifndef __BOOTLOAD_INCLUDE_CACHE_H
#define __BOOTLOAD_INCLUDE_CACHE_H

/*
 * Cache handling functions
 */
static inline void __flush_cache_all(void)
{
  register long __b;

  __asm__ __volatile__ ("movi	%0, 0x33\n\t"
                        "mtcr	%0, cr17"
                        : "=r" (__b)); 
}


/*
 * Instruction Cache handling functions
 */
static inline void __flush_icache(void)
{
  register long __b;

  __asm__ __volatile__ ("movi	%0, 0x11\n\t"
                        "mtcr	%0, cr17"
                        : "=r" (__b)); 
}

/*
 * Data Cache handling functions
 */
static inline void __flush_dcache(void)
{
  register long __b;

  __asm__ __volatile__ ("movi	%0, 0x32\n\t"
                        "mtcr	%0, cr17"
                        : "=r" (__b)); 
}


/*
 * Data Cache handling functions
 */
static inline void __clear_dcache(void)
{
  register long __b;

  __asm__ __volatile__ ("movi	%0, 0x22\n\t"
                        "mtcr	%0, cr17"
                        : "=r" (__b));
}


#define CK_Cache_FlushAll()     __flush_cache_all()
#define CK_Cache_FlushI()       __flush_icache()
#define CK_Cache_FlushD()       __flush_dcache()

#endif /* __BOOTLOAD_INCLUDE_CACHE_H */
