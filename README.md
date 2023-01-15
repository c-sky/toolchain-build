# toolchain-build

## BUILD toolchain

### Prerequisites

Several standard packages are needed to build the toolchain.

On Ubuntu, executing the following command should suffice:

    $ sudo apt-get install autoconf automake autotools-dev curl python3 libmpc-dev libmpfr-dev libgmp-dev gawk build-essential bison flex texinfo gperf libtool patchutils bc zlib1g-dev libexpat-dev

On Fedora/CentOS/RHEL OS, executing the following command should suffice:

    $ sudo yum install autoconf automake python3 libmpc-devel mpfr-devel gmp-devel gawk  bison flex texinfo patchutils gcc gcc-c++ zlib-devel expat-devel

### Code Download
First, download submodules' code<br>
`git submodule update --init`<br>
Second, use the script “build-csky-gcc.py” to build toolchain.<br>
C-SKY abi-v2 supports two versions of the toolchain to compile.<br>
### glibc
* Run the following command to build glibc linux toolchain:<br>
`./build-csky-gcc.py csky-gcc --src ./ --triple csky-unknown-linux-gnu`<br>

After the compilation is completed, the toolchain will be installed into the "build-gcc-csky-unknown-linux-gnu/Xuantie-800-gcc-linux-5.10.4-glibc-x86_64/" directory<br>
### elf
* Run the following command to build newlib elf toolchain:<br>
`./build-csky-gcc.py csky-gcc --src ./ --triple csky-unknown-elf`<br>

After the compilation is completed, the toolchain will be installed into the "build-gcc-csky-unknown-elf/Xuantie-800-gcc-elf-newlib-x86_64/" directory<br>
<br>

As mentioned above, you can use the script to compile all the toolchains, if you want to compile by yourself, you can add the "--fake" option to the build command to print out all the configuration and compile commands, for example:<br>

`./build-csky-gcc.py csky-gcc --src ./ --triple csky-unknown-elf --fake`<br>

## BUILD speed

* The script will build multilib version toolchain by default, which will take a long time to compile. If you only use one CPU, we recommend that you use the "--no-multilib" option to compile the single lib toolchain, which will be 5x faster than the multilib version. For example:<br>
`./build-csky-gcc.py csky-gcc --src ./ --triple csky-unknown-elf --no-multilib --cpu ck860f --fpu hard --endian little`<br>
* The build speed also depends on the CPU and memory of the host machine. If you have a powerful machine, you can use the "--jobs" option to specify the number of parallel compilation threads, -1 means using all cores, for example:<br>
`./build-csky-gcc.py csky-gcc --src ./ --triple csky-unknown-elf --jobs=-1`<br>

## Run gcc test

You can add option to run the gcc test to verify the correctness of the toolchain. For example:<br>
`./build-csky-gcc.py csky-gcc --src ./ --triple csky-unknown-elf --type check-gcc`<br>
  
## Others

Run the following command to get more information about the script:<br>
`./build-csky-gcc.py csky-gcc --help`<br>
