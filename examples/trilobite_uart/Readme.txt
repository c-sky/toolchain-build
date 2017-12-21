Copyright (C): 2008~2010 Hangzhou C-SKY Microsystem Co.,LTD.
Author: Liu Bing  (bing_liu@c-sky.com)
Contributor: Liu Bing
Date: 2010-6-28

Project: Uart (support CDS & GNU make)

Description:  Uart0 demo. 
              Following the prompt to set bundrate, word size, parity, stop bit 
              for uart termination tool.

Directories:
1.UART --                  (main function & test function)
        |
         --- arch          (CPU initialization & exception entry)
        |
         --- drivers       (drivers required)
        |
         --- include       (common header files)
        |
         --- lib           (common functions)
         
Target: 
        cpu: ck810
        soc: ck810
        board:  

Usage:
        Under CDS:
            1. open CDS and select a new workspace
            2. import the 1.Uart project into the new workspace
               (project files: .cproject .project)
            3. build project
            4. new a debug configuration and debug the executable program
        
        Under Linux/windows console:
            1. cd 1.Uart
            2. make  (project files: Makefile Rules.make)
            3. csky-abiv2-elf-gdb Uart.elf(then connect target, download, run...)

Ohters:
        Uart0 used as the termination, Default setting: 19200, 8, none, 1  

output message when success:
Testing uart...
Default configure: Baudrate --- 19200,Parity --- NONE,Wordsize --- 8. 
- - -UART0 ready? [y] y

	- - - Testing uart mode...
	(query mode ): Output is---
		ABCDEFGHIJKLMN- - - [y/n] y	- - -PASS
	(interrupt mode ): Output is---
		ABCDEFGHIJKLMN- - - [y/n] y	- - -PASS

	- - - Test uart baudrate.
	Baudrate is 9600? [y]  y :Output is ---
		ABCDEFGHIJKLMN- - -[y/n] y	- - -PASS
	Baudrate is 14400? [y] y :Output is ---
		ABCDEFGHIJKLMN- - -[y/n] y	- - -PASS
	Baudrate is 38400? [y] y :Output is ---
		ABCDEFGHIJKLMN- - -[y/n] y	- - -PASS
	Baudrate is 56000? [y] y :Output is ---
		ABCDEFGHIJKLMN- - -[y/n] y	- - -PASS
	Baudrate is 57600? [y] y :Output is ---
		ABCDEFGHIJKLMN- - -[y/n] y	- - -PASS
	Baudrate is 115200? [y] y :Output is ---
		ABCDEFGHIJKLMN- - -[y/n] y	- - -PASS
	Baudrate is 19200? [y] y :Output is ---
		ABCDEFGHIJKLMN- - -[y/n] y	- - -PASS

	- - - Test uart parity. (Parity: 0 --- ODD, 1 --- EVEN, 2 --- NONE)
	Parity is 0? [y] y :Output is ---
		ABCDEFGHIJKLMN- - -[y/n] y	- - -PASS
	Parity is 1? [y] y :Output is ---
		ABCDEFGHIJKLMN- - -[y/n] y	- - -PASS
	Parity is 2? [y] y :Output is ---
		ABCDEFGHIJKLMN- - -[y/n] y	- - -PASS

	- - - Test uart wordsize.
	0 --- WORD_SIZE_5,
	1 --- WORD_SIZE_6,
	2 --- WORD_SIZE_7,
	3 --- WORD_SIZE_8
	Wordsize is 2? [y] y :Output is ---
		ABCDEFGHIJKLMN- - -[y/n] y	- - -PASS
	Wordsize is 3? [y] y :Output is ---
		ABCDEFGHIJKLMN- - -[y/n] y	- - -PASS

