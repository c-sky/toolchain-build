# toolchain-build

----------------------------BUILD toolchain----------------------------
First, create a directory for building toolchain.
Then enter the direcotry, and copy the script “build-csky-gcc.py” to this directory.
C-SKY abi-v2 supports three versions of the toolchain to compile.
------uclibc-ng------
1.Run the following command to download the required source code:
    ./build-csky-gcc.py --abi=abiv2 --tos=linux --libc=uclibc-ng --init
  The code will be downloaded to the "source" directory under the current directory, you can also create your own "source" directory, and download the source code of the required components to the source directory
2.Execute the following command to compile the toolchain:
    ./build-csky-gcc.py --abi=abiv2 --tos=linux --libc=uclibc-ng
  After the compilation is completed, the toolchain will be installed into the "install-csky-abiv2-linux-uclibc-ng" directory
------glibc------
1.Run the following command to download the required source code:
    ./build-csky-gcc.py --abi=abiv2 --tos=linux --libc=glibc --init
2.Execute the following command to compile the toolchain:
    ./build-csky-gcc.py --abi=abiv2 --tos=linux --libc=glibc
  After the compilation is completed, the toolchain will be installed into the "install-csky-abiv2-linux-glibc" directory
------elf------
1.Run the following command to download the required source code:
    ./build-csky-gcc.py --abi=abiv2 --tos=elf --init
2.Execute the following command to compile the toolchain:
    ./build-csky-gcc.py --abi=abiv2 --tos=elf
  After the compilation is completed, the toolchain will be installed into the "install-csky-abiv2-elf-minilibc" directory

As mentioned above, you can use the script to compile all the toolchains, if you want to compile by yourself, you can add the "--fake" option to the build command to print out all the configuration and compile commands, for example:
  ./build-csky-gcc.py --abi=abiv2 --tos=linux --libc=uclibc-ng --fake



----------------------------BUILD qemu----------------------------
First, download the code:
  git clone git@github.com:c-sky/qemu.git
Second, create a directory for building, enter the directory, configure and build, for example:
  mkdir qemu_build
  cd qemu_build
  ${QEMU_SOURCE_DIR}/configure --target-list="cskyv2-softmmu cskyv2-linux-user cskyv2eb-softmmu cskyv2eb-linux-user" --prefix=${QEMU_INSTALL_DIR}
  make; make install
Now, Qemu is now installed, you can enter the installation directory to view the generated program. In the ${QEMU_INSTALL_DIR}/bin directory, you can see the following programs:
  qemu-system-cskyv2             --csky little-endian qemu system mode executive program
  qemu-system-cskyv2eb           --csky big-endian qemu system mode executive program
  qemu-cskyv2                    --csky little-endian qemu user mode executive program
  qemu-cskyv2eb                  --csky big-endian qemu user mode executive program
  
  

----------------------------Runing examples for test----------------------------
There are three examples in the "examples" directory.
------smartcard_uart------
This example can used for ck801/ck802/ck803 elf, add the compiled toolchain and qemu program directory to the current PATH environment variable, execute the following command to run this program:
  make clean
  make CPU=ck801/ck802/ck803
  qemu-system-cskyv2  -machine smart_card -cpu ck801/ck802/ck803 -nographic -kernel Uart.elf
You can see the output:
  Testing uart...
  Default configure: Baudrate --- 19200,Parity --- NONE,Wordsize --- 8. 
  - - -UART0 ready? [y]
------trilobite_uart------
This example can used for ck807/ck810 elf, add the compiled toolchain and qemu program directory to the current PATH environment variable, execute the following command to run this program:
  make clean
  make CPU=ck807/ck810
  qemu-system-cskyv2  -machine smart_card -cpu ck807/ck810 -nographic -kernel Uart.elf
You can see the output:
  Testing uart...
  Default configure: Baudrate --- 19200,Parity --- NONE,Wordsize --- 8. 
  - - -UART0 ready? [y]
------linux_hello------
This example can used for ck807/ck810 linux, add the compiled toolchain and qemu program directory to the current PATH environment variable, execute the following command to run this program:
  csky-abiv2-linux-gcc -mcpu=ck807/ck810 hello.c  -o hello --static
  qemu-cskyv2 -cpu ck807/ck810 hello
You can see the output:
  "Hello World!"
  
  
