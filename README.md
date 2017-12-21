# toolchain-build

## BUILD toolchain
First, create a directory for building toolchain.<br>
Then enter the direcotry, and copy the script “build-csky-gcc.py” to this directory.<br>
C-SKY abi-v2 supports three versions of the toolchain to compile.<br>
### uclibc-ng
* Run the following command to download the required source code:<br>
`./build-csky-gcc.py --abi=abiv2 --tos=linux --libc=uclibc-ng --init`<br>
The code will be downloaded to the "source" directory under the current directory, you can also create your own "source" directory, and download the source code of the required components to the source directory<br>
* Execute the following command to compile the toolchain:<br>
`./build-csky-gcc.py --abi=abiv2 --tos=linux --libc=uclibc-ng`<br>
After the compilation is completed, the toolchain will be installed into the "install-csky-abiv2-linux-uclibc-ng" directory<br>
### glibc
* Run the following command to download the required source code:<br>
`./build-csky-gcc.py --abi=abiv2 --tos=linux --libc=glibc --init`<br>
* Execute the following command to compile the toolchain:<br>
`./build-csky-gcc.py --abi=abiv2 --tos=linux --libc=glibc`<br>

After the compilation is completed, the toolchain will be installed into the "install-csky-abiv2-linux-glibc" directory<br>
### elf
* Run the following command to download the required source code:<br>
`./build-csky-gcc.py --abi=abiv2 --tos=elf --init`<br>
* Execute the following command to compile the toolchain:<br>
`./build-csky-gcc.py --abi=abiv2 --tos=elf`<br>
After the compilation is completed, the toolchain will be installed into the "install-csky-abiv2-elf-minilibc" directory<br>
<br>
As mentioned above, you can use the script to compile all the toolchains, if you want to compile by yourself, you can add the "--fake" option to the build command to print out all the configuration and compile commands, for example:<br>

`./build-csky-gcc.py --abi=abiv2 --tos=linux --libc=uclibc-ng --fake`<br>



## BUILD qemu
* First, download the code:<br>
`git clone git@github.com:c-sky/qemu.git`<br>
* Second, create a directory for building, enter the directory, configure and build, for example:
`mkdir qemu_build`<br>
`cd qemu_build`<br>
`${QEMU_SOURCE_DIR}/configure --target-list="cskyv2-softmmu cskyv2-linux-user cskyv2eb-softmmu cskyv2eb-linux-user" --prefix=${QEMU_INSTALL_DIR}`<br>
`make; make install`<br>
* Now, Qemu is now installed, you can enter the installation directory to view the generated program. In the ${QEMU_INSTALL_DIR}/bin directory, you can see the following programs:
>qemu-system-cskyv2&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;--csky little-endian qemu system mode executive program<br>
>qemu-system-cskyv2eb&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;--csky big-endian qemu system mode executive program<br>
>qemu-cskyv2&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;--csky little-endian qemu user mode executive program<br>
>qemu-cskyv2eb&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;--csky big-endian qemu user mode executive program<br>
  
  

## Runing examples for test
There are three examples in the "examples" directory.<br>
### smartcard_uart
This example can used for ck801/ck802/ck803 elf, add the compiled toolchain and qemu program directory to the current PATH environment variable, execute the following command to run this program:<br>
`make clean`<br>
`make CPU=ck801/ck802/ck803`<br>
`qemu-system-cskyv2  -machine smart_card -cpu ck801/ck802/ck803 -nographic -kernel Uart.elf`<br>

You can see the output:<br>
>Testing uart...<br>
>Default configure: Baudrate --- 19200,Parity --- NONE,Wordsize --- 8. <br>
>- - -UART0 ready? [y]<br>
### trilobite_uart
This example can used for ck807/ck810 elf, add the compiled toolchain and qemu program directory to the current PATH environment variable, execute the following command to run this program:<br>
`make clean`<br>
`make CPU=ck807/ck810`<br>
`qemu-system-cskyv2  -machine smart_card -cpu ck807/ck810 -nographic -kernel Uart.elf`<br>

You can see the output:<br>
>Testing uart...<br>
>Default configure: Baudrate --- 19200,Parity --- NONE,Wordsize --- 8. <br>
>- - -UART0 ready? [y]<br>
### linux_hello
This example can used for ck807/ck810 linux, add the compiled toolchain and qemu program directory to the current PATH environment variable, execute the following command to run this program:<br>
`csky-abiv2-linux-gcc -mcpu=ck807/ck810 hello.c  -o hello --static`<br>
`qemu-cskyv2 -cpu ck807/ck810 hello`<br>

You can see the output:<br>
>"Hello World!"<br>
  
  
