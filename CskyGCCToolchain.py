#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import re
from lib.Command import *
from GCCToolchain import GCCToolchain
from Toolchain import CheckError
from lib import TestFilter


class CskyGccToolchain(GCCToolchain):
    def __init__(self, triple, src, jobs, version, release_dir, rebuild, short_dir,
                 build_type, extra_config, run_type, host, dep_libs_dir, cpu, endian, fpu, multilib, ccrt, test_opt,
                 linux_headers, test_cpu, fake, disable_gdb):
        super(CskyGccToolchain, self).__init__(triple, src, jobs, version, release_dir, rebuild, short_dir,
                                               extra_config, host,
                                               build_type, dep_libs_dir, fake, multilib, run_type)
        self.cpu = cpu
        self.endian = endian
        self.fpu = fpu
        self.disable_gdb = disable_gdb
        self.mkdir_nofake(self.build_dir, clean=rebuild)
        self.mkdir_nofake(self.install_dir, clean=rebuild)
        self.mkdir_nofake(self.stamps_dir)

    def run(self):
        self.build()
        self.test()

    @property
    def sysroot(self):
        return os.path.join(self.install_dir, self.triple, "libc")

    @property
    def kernel_header(self):
        return os.path.join(self.src, "linux-headers", "include")

    def uclibc_config(self, opt):
        if self.endian == "little":
            endian = "ARCH_LITTLE_ENDIAN=y\n# ARCH_WANTS_BIG_ENDIAN is not set"
        else:
            endian = "# ARCH_WANTS_LITTLE_ENDIAN is not set\nARCH_WANTS_BIG_ENDIAN=y"
        extra_flag = "-O2 {}".format(opt)
        config = '''#
# Automatically generated file; DO NOT EDIT.
# uClibc-ng 1.0.29 C Library Configuration
#
# TARGET_aarch64 is not set
# TARGET_alpha is not set
# TARGET_arc is not set
# TARGET_arm is not set
# TARGET_avr32 is not set
# TARGET_bfin is not set
# TARGET_c6x is not set
# TARGET_cris is not set
TARGET_csky=y
# TARGET_frv is not set
# TARGET_h8300 is not set
# TARGET_hppa is not set
# TARGET_i386 is not set
# TARGET_ia64 is not set
# TARGET_lm32 is not set
# TARGET_m68k is not set
# TARGET_metag is not set
# TARGET_microblaze is not set
# TARGET_mips is not set
# TARGET_nds32 is not set
# TARGET_nios2 is not set
# TARGET_or1k is not set
# TARGET_powerpc is not set
# TARGET_sh is not set
# TARGET_sparc is not set
# TARGET_sparc64 is not set
# TARGET_tile is not set
# TARGET_x86_64 is not set
# TARGET_xtensa is not set

#
# Target Architecture Features and Options
#
TARGET_ARCH="csky"
FORCE_OPTIONS_FOR_ARCH=y
TARGET_SUBARCH="abiv2"
CSKY_ABIV2=y
# CSKY_ABIV1 is not set

#
# Using ELF file format
#
ARCH_ANY_ENDIAN=y
{}
ARCH_WANTS_LITTLE_ENDIAN=y
ARCH_HAS_MMU=y
ARCH_USE_MMU=y
UCLIBC_HAS_FLOATS=y
UCLIBC_HAS_FPU=y
DO_C99_MATH=y
DO_XSI_MATH=y
UCLIBC_HAS_LONG_DOUBLE_MATH=y
KERNEL_HEADERS="{}"
HAVE_DOT_CONFIG=y

#
# General Library Settings
#
DOPIC=y
HAVE_SHARED=y
# FORCE_SHAREABLE_TEXT_SEGMENTS is not set
LDSO_LDD_SUPPORT=y
# LDSO_CACHE_SUPPORT is not set
LDSO_PRELOAD_ENV_SUPPORT=y
# LDSO_PRELOAD_FILE_SUPPORT is not set
# LDSO_STANDALONE_SUPPORT is not set
# LDSO_PRELINK_SUPPORT is not set
# UCLIBC_STATIC_LDCONFIG is not set
LDSO_RUNPATH=y
LDSO_RUNPATH_OF_EXECUTABLE=y
LDSO_SAFE_RUNPATH=y
LDSO_SEARCH_INTERP_PATH=y
LDSO_LD_LIBRARY_PATH=y
# LDSO_NO_CLEANUP is not set
UCLIBC_CTOR_DTOR=y
# LDSO_GNU_HASH_SUPPORT is not set
# HAS_NO_THREADS is not set
# UCLIBC_HAS_LINUXTHREADS is not set
UCLIBC_HAS_THREADS_NATIVE=y
UCLIBC_HAS_THREADS=y
UCLIBC_HAS_TLS=y
PTHREADS_DEBUG_SUPPORT=y
UCLIBC_HAS_SYSLOG=y
UCLIBC_HAS_LFS=y
# MALLOC is not set
# MALLOC_SIMPLE is not set
MALLOC_STANDARD=y
UCLIBC_DYNAMIC_ATEXIT=y
UCLIBC_HAS_UTMPX=y
UCLIBC_HAS_UTMP=y
UCLIBC_SUSV2_LEGACY=y
UCLIBC_SUSV3_LEGACY=y
# UCLIBC_SUSV3_LEGACY_MACROS is not set
UCLIBC_SUSV4_LEGACY=y
# UCLIBC_STRICT_HEADERS is not set
# UCLIBC_HAS_STUBS is not set
UCLIBC_HAS_SHADOW=y
UCLIBC_HAS_PROGRAM_INVOCATION_NAME=y
UCLIBC_HAS___PROGNAME=y
UCLIBC_HAS_PTY=y
ASSUME_DEVPTS=y
UNIX98PTY_ONLY=y
UCLIBC_HAS_GETPT=y
UCLIBC_HAS_LIBUTIL=y
UCLIBC_HAS_TM_EXTENSIONS=y
UCLIBC_HAS_TZ_CACHING=y
UCLIBC_HAS_TZ_FILE=y
UCLIBC_HAS_TZ_FILE_READ_MANY=y
UCLIBC_TZ_FILE_PATH="/etc/TZ"
UCLIBC_FALLBACK_TO_ETC_LOCALTIME=y

#
# Advanced Library Settings
#
UCLIBC_PWD_BUFFER_SIZE=256
UCLIBC_GRP_BUFFER_SIZE=256

#
# Support various families of functions
#
UCLIBC_LINUX_SPECIFIC=y
UCLIBC_HAS_GNU_ERROR=y
UCLIBC_BSD_SPECIFIC=y
UCLIBC_HAS_BSD_ERR=y
UCLIBC_HAS_OBSOLETE_BSD_SIGNAL=y
# UCLIBC_HAS_OBSOLETE_SYSV_SIGNAL is not set
# UCLIBC_NTP_LEGACY is not set
# UCLIBC_SV4_DEPRECATED is not set
UCLIBC_HAS_REALTIME=y
UCLIBC_HAS_ADVANCED_REALTIME=y
UCLIBC_HAS_EPOLL=y
UCLIBC_HAS_XATTR=y
UCLIBC_HAS_PROFILING=y
UCLIBC_HAS_CRYPT_IMPL=y
UCLIBC_HAS_SHA256_CRYPT_IMPL=y
UCLIBC_HAS_SHA512_CRYPT_IMPL=y
UCLIBC_HAS_CRYPT=y
UCLIBC_HAS_NETWORK_SUPPORT=y
UCLIBC_HAS_SOCKET=y
UCLIBC_HAS_IPV4=y
UCLIBC_HAS_IPV6=y
UCLIBC_USE_NETLINK=y
UCLIBC_SUPPORT_AI_ADDRCONFIG=y
# UCLIBC_HAS_BSD_RES_CLOSE is not set
UCLIBC_HAS_COMPAT_RES_STATE=y
# UCLIBC_HAS_EXTRA_COMPAT_RES_STATE is not set
UCLIBC_HAS_RESOLVER_SUPPORT=y

#
# String and Stdio Support
#
UCLIBC_HAS_STRING_GENERIC_OPT=y
UCLIBC_HAS_STRING_ARCH_OPT=y
UCLIBC_HAS_STDIO_FUTEXES=y
UCLIBC_HAS_CTYPE_TABLES=y
UCLIBC_HAS_CTYPE_SIGNED=y
# UCLIBC_HAS_CTYPE_UNSAFE is not set
UCLIBC_HAS_CTYPE_CHECKED=y
# UCLIBC_HAS_CTYPE_ENFORCED is not set
UCLIBC_HAS_WCHAR=y
UCLIBC_HAS_LIBICONV=y
UCLIBC_HAS_LIBINTL=y
# UCLIBC_HAS_LOCALE is not set
# UCLIBC_BUILD_MINIMAL_LOCALE is not set
# UCLIBC_BUILD_ALL_LOCALE is not set
UCLIBC_HAS_HEXADECIMAL_FLOATS=y
UCLIBC_HAS_GLIBC_CUSTOM_PRINTF=y
UCLIBC_PRINTF_SCANF_POSITIONAL_ARGS=9
# UCLIBC_HAS_STDIO_BUFSIZ_256 is not set
# UCLIBC_HAS_STDIO_BUFSIZ_512 is not set
# UCLIBC_HAS_STDIO_BUFSIZ_1024 is not set
# UCLIBC_HAS_STDIO_BUFSIZ_2048 is not set
UCLIBC_HAS_STDIO_BUFSIZ_4096=y
# UCLIBC_HAS_STDIO_BUFSIZ_8192 is not set
UCLIBC_HAS_STDIO_BUILTIN_BUFFER_NONE=y
# UCLIBC_HAS_STDIO_BUILTIN_BUFFER_4 is not set
# UCLIBC_HAS_STDIO_BUILTIN_BUFFER_8 is not set
# UCLIBC_HAS_STDIO_SHUTDOWN_ON_ABORT is not set
UCLIBC_HAS_STDIO_GETC_MACRO=y
UCLIBC_HAS_STDIO_PUTC_MACRO=y
UCLIBC_HAS_STDIO_AUTO_RW_TRANSITION=y
# UCLIBC_HAS_FOPEN_LARGEFILE_MODE is not set
UCLIBC_HAS_FOPEN_EXCLUSIVE_MODE=y
# UCLIBC_HAS_FOPEN_CLOSEEXEC_MODE is not set
UCLIBC_HAS_GLIBC_CUSTOM_STREAMS=y
UCLIBC_HAS_PRINTF_M_SPEC=y
UCLIBC_HAS_ERRNO_MESSAGES=y
# UCLIBC_HAS_SYS_ERRLIST is not set
UCLIBC_HAS_SIGNUM_MESSAGES=y
# UCLIBC_HAS_SYS_SIGLIST is not set
UCLIBC_HAS_GNU_GETOPT=y
UCLIBC_HAS_GETOPT_LONG=y
UCLIBC_HAS_GNU_GETSUBOPT=y
# UCLIBC_HAS_ARGP is not set

#
# Big and Tall
#
UCLIBC_HAS_REGEX=y
UCLIBC_HAS_FNMATCH=y
UCLIBC_HAS_WORDEXP=y
UCLIBC_HAS_NFTW=y
UCLIBC_HAS_FTW=y
# UCLIBC_HAS_FTS is not set
UCLIBC_HAS_GLOB=y
UCLIBC_HAS_GNU_GLOB=y

#
# Library Installation Options
#
RUNTIME_PREFIX="/"
DEVEL_PREFIX="/usr"
MULTILIB_DIR="lib"
HARDWIRED_ABSPATH=y

#
# Security options
#
# UCLIBC_HAS_SSP is not set
UCLIBC_BUILD_RELRO=y
UCLIBC_BUILD_NOW=y
UCLIBC_BUILD_NOEXECSTACK=y

#
# Development/debugging options
#
CROSS_COMPILER_PREFIX="{}"
UCLIBC_EXTRA_CFLAGS="{}"
# DODEBUG is not set
# DOSTRIP is not set
# DOASSERTS is not set
# SUPPORT_LD_DEBUG is not set
# SUPPORT_LD_DEBUG_EARLY is not set
# UCLIBC_MALLOC_DEBUGGING is not set
UCLIBC_HAS_BACKTRACE=y
WARNINGS="-Wall"
# EXTRA_WARNINGS is not set

        '''.format(endian, self.kernel_header, self.triple + "-", extra_flag)
        return config

    def has_float_isa(self, opt=""):
        if self.multilib:
            s = opt
        else:
            s = self.fpu
        return "softfp" in s or "hard" in s

    def size_prefer(self, opt=""):
        if self.multilib:
            s = opt
        else:
            s = self.cpu
        return "801" in s or "802" in s

    def build_libc(self):
        self.append_path(os.path.join(self.install_dir, "bin"))
        if self.libc == "newlib":
            config_cmd = '{} --target={} --enable-newlib-io-long-double --enable-newlib-io-long-long ' \
                         '--enable-newlib-io-c99-formats --enable-newlib-retargetable-locking ' \
                         '--prefix={} CFLAGS_FOR_TARGET="-g0 -O2"'.format(
                os.path.join(self.src, "newlib", "configure"), self.triple, self.install_dir
            )
            self.simple_stamp_build("newlib", config_cmd)
            return
        for opt, path in self.multilib_rules:
            if path == ".":
                tmp = ""
            else:
                tmp = path.replace("/", "-")
                if not tmp.startswith("-"):
                    tmp = "-" + tmp
            build_name = "{}{}".format(self.libc, tmp)
            if not self.has_stamp(build_name):
                build_dir = os.path.join(self.build_dir, "build-" + build_name)
                if self.libc == "glibc":
                    self.mkdir(build_dir, clean=True)
                    if self.has_float_isa(opt):
                        fp_option = "--with-fp"
                    else:
                        fp_option = "--without-fp"
                    config_cmd = '{} CC="{}" CXX="{}" AS="{}" LD="{}" --host={} ' \
                                 'libc_cv_forced_unwind=yes --target={} ' \
                                 '--prefix=/usr/ CFLAGS="-O2 -fexceptions -Wno-unused-variable -fPIC {}" ' \
                                 'CPPFLAGS="-O2 -fexceptions {}" ' \
                                 'LDFLAGS="-L</lib> -Wl,-s " --enable-kernel=2.6.25 ' \
                                 '--disable-check-abi --disable-profile ' \
                                 '--enable-bounded --enable-stackguard-randomization --disable-all-warnings ' \
                                 '--enable-shared {} libc_cv_ctors_header=yes libc_cv_c_cleanup=yes ' \
                                 'libc_cv_pic_default=yes libc_cv_gcc_static_libgcc= --with-headers={} ' \
                                 '--disable-build-nscd --disable-nscd --enable-obsolete-rpc --enable-static-nss ' \
                                 'libc_cv_slibdir=/lib libc_cv_libdir=/usr/lib/ ' \
                                 'libc_cv_ld_gnu_indirect_function=no'.format(
                                    os.path.join(self.src, "glibc", "configure"), self.triple + "-gcc " + opt,
                                    self.triple + "-g++ " + opt, self.triple + "-as " + opt, self.triple + "-ld",
                                    self.triple, self.triple, opt, opt, fp_option, self.kernel_header
                                 )
                    self.execute(config_cmd, cwd=build_dir)
                    self.execute("make -j{} && "
                                 "make install -j{} install_root={}".format(self.jobs, self.jobs,
                                                                            os.path.join(self.sysroot, path)),
                                 cwd=build_dir)
                elif self.libc == "uclibc":
                    if os.path.exists(build_dir):
                        self.rm(build_dir)
                    self.copy(os.path.join(self.src, "uclibc"), build_dir)
                    self.create(os.path.join(build_dir, ".config"), self.uclibc_config(opt))
                    self.execute("make oldconfig && make -j{}".format(self.jobs), cwd=build_dir)
                    self.symlink("ld-uClibc.so.1", "ld.so.1", cwd=os.path.join(build_dir, "lib"))
                    self.copy(os.path.join(build_dir, "lib", "crt1.o"), os.path.join(build_dir, "lib", "crt0.o"))
                    self.execute("make install -j{} PREFIX={}".format(self.jobs, os.path.join(self.sysroot, path)),
                                 cwd=build_dir)
                elif self.libc == "minilibc":
                    if os.path.exists(build_dir):
                        self.rm(build_dir)
                    self.copy(os.path.join(self.src, "minilibc"), build_dir)
                    float_opt = "-DCONFIG_CSKY_FPU" if self.has_float_isa(opt) else ""
                    optimize_size = "-Os" if self.size_prefer(opt) else ""
                    cflags = "{} {} {}".format(opt, float_opt, optimize_size)
                    self.execute('CFLAGS="{}" TOOLCHAIN_PREFIX={}- PREFIX={}/ DEVEL_PREFIX={}/ INSTALL_SUB_DIR={} '
                                 'make -j{} install'.format(cflags, self.triple, self.install_dir, self.triple,
                                                            path, self.jobs),
                                 cwd=build_dir)
                self.add_stamp(build_name)

    def build(self):
        host_config = ""
        if self.host == "i386":
            host_config = 'CXX="g++ -m32" CC="gcc -m32"'
        elif self.host == "mingw":
            host_config = '--host=i686-w64-mingw32'
        config_cmd = '{} {} --disable-werror --with-included-gettext --disable-gdb ' \
                     '--target={} --prefix={} --with-sysroot=yes --enable-any'.format(
                        os.path.join(self.src, "binutils", "configure"), host_config,
                        self.triple, self.install_dir
                     )
        self.simple_stamp_build("binutils", config_cmd)
        if self.platform == "linux" and not self.has_stamp("install-linux-header"):
            target_dir = os.path.join(self.sysroot, "usr")
            self.mkdir(target_dir, parent=True)
            self.copy(self.kernel_header, target_dir)
            self.add_stamp("install-linux-header")
        config_cmd = '{} {} --enable-languages=c --target={} --prefix={} ' \
                     '--without-headers --with-newlib --disable-shared --disable-libssp ' \
                     '--disable-libgomp --disable-libmudflap --disable-threads ' \
                     '--with-cskylibc={} --disable-libquadmath --disable-libatomic ' \
                     '--with-sysroot={} --with-pkgversion="{}" {} '.format(
                        os.path.join(self.src, "gcc", "configure"), host_config, self.triple,
                        self.install_dir, self.libc, self.sysroot, self.version_number, self.dep_libs_config
                     )
        if not self.multilib:
            config_cmd += ' --disable-multilib --with-cpu={} --with-endian={} --with-float={}'.format(
                self.cpu, self.endian, self.fpu
            )
        self.simple_stamp_build("gcc-stage1", config_cmd)
        if self.libc == "glibc" and not self.has_stamp("remove-crt"):
            while True:
                try:
                    self.rm(find(self.install_dir, "crtn.o"))
                except FindException:
                    break
            while True:
                try:
                    self.rm(find(self.install_dir, "crti.o"))
                except FindException:
                    break
            self.add_stamp("remove-crt")
        if self.libc == "minilibc" and not self.has_stamp("install-minilibc-header"):
            build_dir = os.path.join(self.src, "minilibc")
            self.execute("make install_headers PREFIX={}/ DEVEL_PREFIX={}/".format(self.install_dir, self.triple),
                         cwd=build_dir)
            self.add_stamp("install-minilibc-header")
        self.build_libc()
        if self.libc == "glibc" and not self.has_stamp("fix-crt0-and-include"):
            for root, dirs, files in os.walk(self.sysroot):
                for f in files:
                    if f == "crt1.o":
                        self.copy(os.path.join(root, f), os.path.join(root, "crt0.o"))
                for d in dirs:
                    if d == "include" and not os.path.samefile(root, os.path.join(self.sysroot, "usr")):
                        self.rm(os.path.join(root, d))
            self.add_stamp("fix-crt0-and-include")
        if not self.has_stamp("gcc-stage2"):
            build_dir = os.path.join(self.build_dir, "build-gcc-stage2")
            self.mkdir(build_dir, clean=True)
            config_cmd = '{} {} ' \
                         '--target={} --prefix={} --with-lib={} ' \
                         '--with-pkgversion="{}" {} '.format(
                            os.path.join(self.src, "gcc", "configure"), host_config, self.triple,
                            self.install_dir, os.path.join(self.install_dir, self.triple, "lib"),
                            self.version_number, self.dep_libs_config
                         )
            if self.platform == "linux":
                config_cmd += '--enable-shared --enable-libssp --enable-tls --enable-libgomp --disable-libmudflap ' \
                              '--enable-languages=c,c++ --with-build-sysroot={} --with-sysroot={} ' \
                              '--enable-poison-system-directories --with-cskylibc={} ' \
                              '--with-headers={} '.format(
                                  self.sysroot, self.sysroot, self.libc, os.path.join(self.sysroot, "usr", "include")
                              )
            else:
                config_cmd += '--enable-sjlj-exceptions --disable-shared --disable-libssp ' \
                              '--enable-languages=c,c++ --with-headers={} '.format(
                                  os.path.join(self.install_dir, self.triple, "include")
                              )
            if self.libc == "newlib":
                config_cmd += '--with-newlib '
            if self.platform == "elf":
                config_cmd += '--disable-threads '
            else:
                config_cmd += '--enable-threads=posix '
            if not self.multilib:
                config_cmd += ' --disable-multilib --with-cpu={} --with-endian={} --with-float={} '.format(
                    self.cpu, self.endian, self.fpu
                )
            self.execute(config_cmd, cwd=build_dir)
            self.execute("make -j{} && make install -j{}".format(self.jobs, self.jobs), cwd=build_dir)
            self.add_stamp("gcc-stage2")
        if self.platform == "linux" and not self.has_stamp("copy-lib"):
            for _, path in self.multilib_rules:
                self.copy(os.path.join(self.install_dir, self.triple, "lib", path, "*"),
                          os.path.join(self.sysroot, path, "usr", "lib"))
            self.add_stamp("copy-lib")
        if not self.has_stamp("build-genromfs") and os.path.exists(os.path.join(self.src, "genromfs")):
            build_dir = os.path.join(self.build_dir, "build-genromfs")
            if os.path.exists(build_dir):
                self.rm(build_dir)
            self.copy(os.path.join(self.src, "genromfs"), build_dir)
            self.execute("make -j{}".format(self.jobs), cwd=build_dir)
            self.copy(os.path.join(build_dir, "genromfs"), os.path.join(self.install_dir, "bin"))
            self.add_stamp("build-genromfs")
        if not self.disable_gdb:
            config_cmd = '{} {} --target={} --prefix={} --disable-werror --disable-ld --disable-binutils ' \
                         '--disable-gas --disable-gold --disable-gprof --without-auto-load-safe-path ' \
                         '--with-libexpat-prefix={} --with-python=no --disable-sim --enable-install-libbfd ' \
                         '--with-pkgversion="{}"'.format(
                            os.path.join(self.src, "gdb", "configure"), host_config, self.triple, self.install_dir,
                            self.real_dep_lib, self.version_number
                         )
            if self.host == "mingw":
                config_cmd += ' CXXFLAGS="-std=gnu++11 -O2"'
            self.simple_stamp_build("gdb", config_cmd)
        # build gdbserver
        if not self.disable_gdb and self.platform == "linux":
            for opt, path in self.multilib_rules:
                if path == ".":
                    tmp = ""
                else:
                    tmp = path.replace("/", "-")
                    if not tmp.startswith("-"):
                        tmp = "-" + tmp
                build_name = "gdb-server{}".format(tmp)
                config_cmd = '{} CFLAGS="-O2 {}" CXXFLAGS="-O2 {}" --host={} --prefix={} --disable-gdb'.format(
                                 os.path.join(self.src, "gdb", "configure"), opt, opt,
                                 self.triple, os.path.join(self.sysroot, path, "usr")
                             )
                self.simple_stamp_build(build_name, config_cmd, "all-gdbserver", "install-gdbserver")

    def test(self):
        if "check-gcc" in self.run_type:
            config_cmd = '{} --prefix={}'.format(os.path.join(self.src, "dejagnu", "configure"), self.install_dir)
            self.simple_stamp_build("dejagnu", config_cmd)
            # FIXME csky-sim.exp has not been upstream yet, copy it to install dir manually
            self.copy(os.path.join(self.src, "csky-sim.exp"),
                      os.path.join(self.install_dir, "share", "dejagnu", "baseboards"))
            config_cmd = '{} --prefix={} --target-list=cskyv2-linux-user'.format(
                os.path.join(self.src, "qemu", "configure"), self.install_dir
            )
            self.simple_stamp_build("qemu", config_cmd)
            for opt, path in self.multilib_rules:
                if path == ".":
                    tmp = ""
                else:
                    tmp = path.replace("/", "-")
                    if not tmp.startswith("-"):
                        tmp = "-" + tmp
                build_name = "check-gcc{}".format(tmp)
                if not self.multilib:
                    cpu = self.cpu
                else:
                    match_obj = re.search(r"mcpu=(\S+)", opt)
                    if match_obj is not None:
                        cpu = match_obj.group(1)
                    else:
                        cpu = "ck810f"
                # FIXME: Change ck803rx to ck803erx cause qemu may miss some instrutions.
                if cpu.startswith("ck803") and "r" in cpu and "e" not in cpu:
                    cpu = cpu.replace("ck803", "ck803e")
                cpu_opt = "-cpu " + cpu
                if not self.has_stamp(build_name):
                    if self.platform == "linux":
                        sim = "qemu-cskyv2"
                        sysroot = os.path.join(self.sysroot, path)
                        sim_opt = "{} -r {} -L {} -csky-extend denormal=on".format(
                            cpu_opt, self.kernel_version, sysroot
                        )
                    else:
                        sim = "qemu-system-cskyv2" if opt.find("big-endian") == -1 else "qemu-system-cskyv2eb"
                        sim_opt = "{} -csky-extend denormal=on -semihosting -M smartl -nographic -kernel ".format(cpu_opt)
                    self.execute('DEJAGNU_SIM_INCLUDE_FLAGS="-msim" DEJAGNU_SIM={} DEJAGNU_SIM_OPTIONS="{}" '
                                 'make check-gcc RUNTESTFLAGS="--target_board=csky-sim/{}" -j{}'.format(
                                    sim, sim_opt, "/".join(opt.split()), self.jobs),
                                 cwd=os.path.join(self.build_dir, "build-gcc-stage2"))
                    self.add_stamp(build_name)
                if not self.has_stamp(build_name + "-pass"):
                    if not TestFilter.filter_result(os.path.join(self.build_dir, "build-gcc-stage2"), "gcc",
                                                    self.libc, cpu, os.path.join(self.src, "test", "whitelist")):
                        raise CheckError("GCC has unexpected fail testcases.")
                    else:
                        self.add_stamp(build_name + "-pass")
