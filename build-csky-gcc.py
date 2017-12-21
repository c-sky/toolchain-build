#!/usr/bin/env python
# -*- coding: UTF-8 -*-

csky_sim_elf_exp = '''
load_generic_config "sim"

# No multilib flags needed by default.
process_multilib_options ""

# basic-sim.exp is a basic description for the standard Cygnus simulator.
load_base_board_description "basic-sim"

# The name of the directory in the build tree where the simulator lives.
setup_sim csky

# The compiler used to build for this board. This has *nothing* to do
# with what compiler is tested if we're testing gcc.
set_board_info compiler         "[find_gcc]"

# The basic set of flags needed to build "hello world" for this
# board. This board uses libgloss and newlib.

set csky_cflags "-march=ck803 -mlittle-endian -msoft-float"
set csky_ldflags "-nostartfiles crt0.S uart.c -lc"
set csky_bsp_srcdir "$srcdir/gcc.target/csky/arch/smartl/ck803/qemu"

load_lib copy-file.exp
gcc_copy_files "$csky_bsp_srcdir/csky.ld" $tmpdir
gcc_copy_files "$csky_bsp_srcdir/crt0.S" $tmpdir
gcc_copy_files "$csky_bsp_srcdir/uart.c" $tmpdir
gcc_copy_files "$csky_bsp_srcdir/ckuart.h" $tmpdir
gcc_copy_files "$csky_bsp_srcdir/uart.h" $tmpdir
gcc_copy_files "$csky_bsp_srcdir/ckconfig.h" $tmpdir
gcc_copy_files "$csky_bsp_srcdir/datatype.h" $tmpdir

set_board_info ldscript  "-Tcsky.ld"
set_board_info cflags   "[libgloss_include_flags] [newlib_include_flags] $csky_cflags"
set_board_info ldflags  "[libgloss_link_flags] [newlib_link_flags] $csky_ldflags"

# More time is needed to compile PlumHall tests
set_board_info gcc,timeout 60

# Make this variable go away, we don't need it.
unset csky_cflags
unset csky_ldflags
unset csky_bsp_srcdir
'''

csky_sim_linux_exp = '''
load_generic_config "sim"

# No multilib flags needed by default.
process_multilib_options ""

# basic-sim.exp is a basic description for the standard Cygnus simulator.
load_base_board_description "basic-sim"

# The name of the directory in the build tree where the simulator lives.
setup_sim csky

# The compiler used to build for this board. This has *nothing* to do
# with what compiler is tested if we're testing gcc.
set_board_info compiler         "[find_gcc]"

# The basic set of flags needed to build "hello world" for this
# board. This board uses libgloss and newlib.

set csky_cflags "-march=ck810 -mlittle-endian -msoft-float"

set_board_info cflags   "[libgloss_include_flags] [newlib_include_flags] $csky_cflags"
set_board_info ldflags  "[libgloss_link_flags] [newlib_link_flags]"

# This board doesn't use a linker script.
set_board_info ldscript ""

# More time is needed to compile PlumHall tests
set_board_info gcc,timeout 60

# Make this variable go away, we don't need it.
unset csky_cflags
'''

#import fcntl

import sys
import platform
import os
import time
from optparse import OptionParser

scritp_dirname, script_filename = os.path.split(os.path.abspath(sys.argv[0]))
source_dirname = scritp_dirname + "/" + "source" + "/"

def cmd_exec(options, cmd, out = True, fake = True):
	make_src = "make "
	make_dst = make_src + "-j"
	if options.makejob:
		make_dst += options.makejob
	if cmd.find(make_src) != -1:
		cmd = cmd.replace(make_src, make_dst + " ")

	if options.fake and fake:
		print "exec command: " + cmd
		return ("", "fake command :)\n", 0)
	if sys.version_info >= (2, 4):
		import subprocess
		if out:
			p = subprocess.Popen(cmd, shell=True,
		          stderr=subprocess.PIPE, close_fds=True)
		else:
			p = subprocess.Popen(cmd, shell=True,
		          stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
		(o, e) = p.communicate()
		r = p.returncode
	else:
		p = os.popen(cmd)
		o = p.read()
		e = "error"
		r = p.close()
		if r is None: r = 0
	return (o, e, r)

def cmd_exec_is_error(r, e):
	t = False

	if r != 0:
		t = True
	if t:
		print "\n--> start error output\n"
		print "error code: %d" % r
		print "%s" % e
		print "<-- end error output\n"
	return t

def get_component(options, mm):
	opt = options.parser.has_option(mm)
	if opt:
		mm = getattr(options, mm.lstrip("-").replace("-", "_"))

	mm = mm.split(".")
	if mm[0] not in component.keys():
		print "\n*** component '%s' is not supported :( ***\n*** Please use -h for more detail ***\n" % mm[0]
		sys.exit(2)

	stage_nums = len(component[mm[0]]["worker"])
	stage = stage_nums - 1

	if len(mm) > 1:
		stage = int(mm[1])
		if stage >= stage_nums:
			print "\n*** stage %s is out of max stage %s of component '%s' ***\n" \
				  % (stage, stage_nums - 1, mm[0])
			sys.exit(2)
	mm = mm[0]
	#print "\n<-- get component: '%s' stage: %s" % (mm, stage)
	return (mm, stage)

def get_target_name(options):
	name = "csky-%s-%s" % (options.abi, options.tos)
	if options.abi == "abiv1":
		name = "csky-%s" % options.tos
	return name

def get_target_dir(options):
	debug = ""
	if options.debug:
		debug = "-" + "debug4" + " ".join(options.debug)
		debug = debug.replace(" ", "_")

	time = ""
	if options.time:
		time = "-" + time.strftime('%Y_%m_%d', time.localtime(time.time()))

	# keep this attr last :)
	no_multilib = ""
	if options.no_multilib:
		no_multilib = "-" + "nomultilib4" + " ".join(options.no_multilib)
		no_multilib = no_multilib.replace(" ", "_")
		no_multilib = no_multilib.replace("=", "-")

	tdir = build_cmd(options, "%s-%s%s%s%s", (get_target_name(options), options.libc, debug, time, no_multilib))
	tdir = tdir.strip()
	return tdir

def build_cmd(options, fformat, vvar = None):
	cmd_f = fformat + " "
	cmd_p = vvar

	cmd = cmd_f
	if cmd_p is not None:
		cmd = cmd_f % cmd_p

	cc = cmd.split(" ")
	for c in cc:
		for patten in options.cmd_compatibility:
			for p in patten.keys():
				if c.find(p) != -1:
					cmd = cmd.replace(c, patten[p])
	return cmd

def build_cmd_compatibility(options, cmd, cmd_replace = ""):
	c = {cmd : cmd_replace}
	if c not in options.cmd_compatibility:
		options.cmd_compatibility.append(c)

def cmd_exec_with_checkerr(options, cmd, out = True, fake = True):
	path = "export PATH=%s:$PATH;" % options.tcprefix
	cmd = path + cmd
	(o, e, r) = cmd_exec(options, cmd, out, fake)
	if cmd_exec_is_error(r, e):
		print "exec command: " + cmd
		sys.exit(2)
	return o

def cmd_exec_ret_with_checkerr(options, cmd):
	return cmd_exec_with_checkerr(options, cmd, False, False).strip()

def build_return(options, mm, stage = 0):
	if "cmd_post" in component[mm].keys():
		cmd_exec_with_checkerr(options, component[mm]["cmd_post"])
	f = get_finished_target(options, mm, stage)
	cmd_exec_with_checkerr(options, "touch '%s'" % f)
	build_log(options, os.path.basename(f))
	os.chdir(scritp_dirname)

def build_start(options, mm, stage = 0):
	m = mm
	if len(component[mm]["worker"]) != 1: m += "." + str(stage)
	print "\n====> start building component '%s' ... ..." % m

	component[mm]["append"] = ""
	# used for post exec
	component[mm]["cmd_post"] = ""

	if "bos" in component[mm].keys():
		print "--> current building platform/os is \"%s\"" % sys.platform
		component[mm]["bos"](options, mm, sys.platform)

	if "tos" in component[mm].keys():
		tos = component[mm]["tos"]
		isFunction = hasattr(tos, '__call__')
		if isFunction:
			tos(options, mm, options.tos, stage)
		else:
			if options.tos in component[mm]["tos"].keys():
				tos = component[mm]["tos"][options.tos]
				isFunction = hasattr(tos, '__call__')
				if isFunction:
					tos(options, mm, options.tos, stage)
				else:
					component[mm]["append"] += tos + " "

	if "default" in component[mm].keys():
		component[mm]["append"] += component[mm]["default"] + " "

	if get_component_is_debug(options, mm):
		if "debug" in component[mm].keys():
			component[mm]["append"] += component[mm]["debug"] + " "
		else:
			print "<-- current component do not support debug version"

	attr = mm.replace("-", "_") + "_build"
	bdir = getattr(options, attr)

	if options.rbuild:
		cmd_exec_with_checkerr(options, "rm -rf %s" % bdir)

	f = get_finished_target(options, mm, stage)

	if options.update:
		(umm, ustage) = get_component(options, options.update)
		if umm == mm and ustage == stage:
			options.update = "%s.%s.update" % (umm, str(ustage))
		if options.update.split(".")[-1] == "update":
			print "--> recompile the module %s, it depends on %s" % (os.path.basename(f), options.update.split(".")[:-2])
			cmd_exec_with_checkerr(options, "rm -rf %s" % f)
			cmd_exec_with_checkerr(options, "rm -rf %s.*" % f)

	if build_is_finished(options, f):
		return ""
	if not os.path.isdir(bdir):
		cmd_exec_with_checkerr(options, "mkdir -p %s" % bdir)
	if os.path.isdir(bdir):
		os.chdir(bdir)
	return bdir

def get_finished_target(options, mm, stage = None, extra = None):
	if stage == None:
		(mm, stage) = get_component(options, mm)
	f = ".%s.%s" % (mm, str(stage))
	if extra is not None:
		f += ".%s" % str(extra)
	f = f.replace("'", "")
	attr = mm.replace("-", "_") + "_build"
	bdir = getattr(options, attr)
	return bdir + "/" + f

def build_is_finished(options, target, real = False):
	if not real:
		if options.rbuild:
			return False
		if options.command:
			return False
		if options.update and options.update.split(".")[-1] == "update":
			return False
	if os.path.isfile(target):
		t = os.path.basename(target)
		print "<-- current component '%s' has finished" % t.strip(".")
		build_log(options, "%s has already finished" % t)
		return True
	return False

def build_binutils(options, argv):
	cmd = build_cmd(options, "rm -rf ./* && %s/configure", options.binutils_src)
	cmd += build_cmd(options, "%s", platform.machine())
	cmd += build_cmd(options, "--target=%s --with-cskyabi=%s", (get_target_name(options), options.abi[-1]))
	cmd += build_cmd(options, "%s", component["binutils"]["append"])
	cmd += build_cmd(options, "--prefix=%s/", options.prefix)
	cmd += build_cmd(options, "&& make && make install")
	cmd_exec_with_checkerr(options, cmd)

def build_gdb(options, argv):
	cmd = build_cmd(options, "rm -rf ./* && %s/configure", options.gdb_src)
	cmd += build_cmd(options, "%s", platform.machine())
	cmd += build_cmd(options, "--target=%s", get_target_name(options))
	cmd += build_cmd(options, "%s", component["gdb"]["append"])
	cmd += build_cmd(options, "--prefix=%s/", options.prefix)
	cmd += build_cmd(options, "&& make && make install")
	cmd_exec_with_checkerr(options, cmd)

def build_gcc_initial(options, argv):
	component["gcc"]["append"] += "--enable-languages=c \
	--disable-threads --disable-libssp --disable-libgomp --disable-libmudflap \
	--disable-libquadmath --disable-libatomic --disable-nls \
	--without-headers --with-newlib "
	build_gcc_base(options)

def build_gcc(options, argv):
	component["gcc"]["append"] += "--enable-languages=c,c++ \
	--enable-libssp --disable-nls \
	--with-lib=%s/%s/lib/ " % (options.prefix, get_target_name(options))
	build_gcc_base(options)

	# FIXME: compatibility qemu exec libs
	if options.tos.startswith('linux'):
		install = get_gcc_multilib_install_dir(options, argv)
		base, libdir = install.split("/libc/")
		p = "./"
		if libdir: p = "".join(["../" for i in range(len(libdir.strip("/").split("/")))])
		cmd = build_cmd(options, "cd %s/lib", install)
		cmd += build_cmd(options, "&& for i in `find ../%s/../lib/%s -name 'lib*.so*'`; do\n", (p, libdir))
		cmd += build_cmd(options, "if [ ! -f `basename $i` ] ; then\nln -s $i `basename $i`\nfi")
		cmd += build_cmd(options, "\ndone")
		cmd_exec_with_checkerr(options, cmd)

def build_gcc_base(options):
	cmd = build_cmd(options, "rm -rf ./* && %s/configure", options.gcc_src)
	cmd += build_cmd(options, "--target=%s --with-cskyabi=%s", (get_target_name(options), options.abi))
	cmd += build_cmd(options, "%s", component["gcc"]["append"])
	cmd += build_cmd(options, "--prefix=%s/", options.prefix)

	if options.no_multilib is not None:
		cmd += build_cmd(options, "--disable-multilib")
		cmd += build_cmd(options, "--with-cpu=%s", get_gcc_multilib_opt(options.no_multilib, "mcpu", "="))
		cmd += build_cmd(options, "--with-endian=%s", get_gcc_multilib_opt(options.no_multilib, "-endian").replace('-endian', "").lstrip("m"))
		cmd += build_cmd(options, "--with-float=%s", get_gcc_multilib_opt(options.no_multilib, "-float").replace('-float', "").lstrip("m"))

	if options.gcc_dep_libs:
		deps = options.gcc_dep_libs.replace(" ", "").split(",")
		libs = {"--with-mpc" : deps[0], "--with-mpfr" : deps[0], "--with-gmp" : deps[0]}
		gcc_dep_libs = ""
		for (k, v) in libs.items():
			if deps: v = deps.pop(0)
			gcc_dep_libs += "%s=%s " % (k, v)
		cmd += build_cmd(options, "%s", gcc_dep_libs)

	cmd += build_cmd(options, "&& make && make install")
	cmd_exec_with_checkerr(options, cmd)

def build_gcc_bos(options, mm, bos):
	if bos.startswith('darwin'):
		if not options.gcc_dep_libs:
			mpc = os.listdir("/usr/local/Cellar/libmpc")[0]
			mpfr = os.listdir("/usr/local/Cellar/mpfr")[0]
			gmp = os.listdir("/usr/local/Cellar/gmp")[0]
			component[mm]["append"] += "--with-mpc=/usr/local/Cellar/libmpc/%s \
			--with-mpfr=/usr/local/Cellar/mpfr/%s \
			--with-gmp=/usr/local/Cellar/gmp/%s " % (mpc, mpfr, gmp)

def build_gcc_tos(options, mm, tos, stage = 0):

	if tos.startswith('elf'):
		component[mm]["append"] += "--enable-sjlj-exceptions --disable-shared "
		if stage:
			component[mm]["append"] += "--disable-threads "
			component[mm]["append"] += "--with-headers=%s/%s/include " % (options.prefix, get_target_name(options))

	if tos.startswith('linux'):
		component[mm]["append"] += "--enable-shared \
		--with-cskylibc=%s \
		--with-sysroot=%s/%s/libc/ " % \
		(options.libc, options.prefix, get_target_name(options))

		if stage:
			component[mm]["append"] += "--enable-threads=posix --disable-libgomp --disable-libmudflap \
			--enable-poison-system-directories "
			component[mm]["append"] += "--with-headers=%s/%s/libc/usr/include " % (options.prefix, get_target_name(options))
			component[mm]["append"] += "--with-build-sysroot=%s/%s/libc/ " % (options.prefix, get_target_name(options))
			component[mm]["append"] += "--with-build-time-tools=%s/bin " % options.prefix
		if not stage:
			cmd = "cd %s " % options.prefix
   			cmd += '&& find . -name crtn.o -print -exec rm -rf {} \; '
   			cmd += '&& find . -name crti.o -print -exec rm -rf {} \; '
			component[mm]["cmd_post"] = cmd

def build_gcc_compatibility(options, component_chain):
	if not get_component_version(options, "gcc") >= "6.3.0":
		# compatibility option
		if options.no_multilib:
			opts = component["gcc"]["no-multilib"][options.abi]
			if options.no_multilib != opts:
				print "<-- do not support non-default configuration for no multilib"
				return False
		# compatibility cmd
		build_cmd_compatibility(options, "--with-cpu")
		build_cmd_compatibility(options, "--with-endian")
		build_cmd_compatibility(options, "--with-float")
	return True

def build_gcc_multilib(options, param):
	multilib_opt = []
	multilib_exp = []
	# extend for gcc multilib option
	multilib_opt_extend = []

	def opts_is_exceptions(opts, exptab):
		for exp in exptab:
			issubset = True
			for e in exp:
				if e not in opts:
					if e.startswith("!") and e.lstrip("!") not in opts:
						continue
					issubset = False
					break;
			if issubset:
				#print "<-- remove by exceptin table item: %s" % exp
				return True
		return False

	def get_multilib_table(opttab, exptab):
		#print "<-- multilib option set: %s" % opttab
		#print "<-- multilib exceptin table: %s" % exptab
		def get_multilib_table_do(opttab, item, i, exptab):
			tab = []
			for opt in opttab[i]:
				item[i] = opt
				if i < len(item) - 1:
					tab += get_multilib_table_do(opttab, item, i + 1, exptab)
				else:
					#print "<-- create option table item = %s" % item
					if (opts_is_exceptions(item, exptab)):
						continue
					tab.append(list(item))
			return tab
		item = [0 for i in range(len(opttab))]
		return get_multilib_table_do(opttab, item, 0, exptab)

	if options.no_multilib is not None:
		contents = []
		for i in options.no_multilib:
			contents += ["MULTILIB_OPTIONS = " + i]
	else:
		fname = "%s/gcc/config/csky/%s_t-csky-%s" % (options.gcc_src, options.abi, options.tos)
		fd = open(fname)
		contents = fd.readlines()
		fd.close()
		# TODO: In gcc rules, one 'attr' of MULTILIB_OPTIONS
		# shoud be combined with 2 status ('attr' or '!attr')
		# so we need to compatible with gcc
		for i in contents:
			if i.startswith("MULTILIB_OPTIONS") and "/" not in i:
				v = get_gcc_multilib_opt([i], "", "=")
				v = "/" + v[0] + "$" + v[1:]
				get_gcc_multilib_opt(contents, i, "rs", get_gcc_multilib_opt([i], "=", "av", v), True)
	if param:
		contents.extend(param)

	for line in contents:
		line = line.strip()

		if line == "":
			continue
		if line.startswith("#"):
			continue

		if "@" in line:
			if not eval(line[line.index("@") + 1:]):
				continue
			line = line[:line.index("@")]

		if line.find(".MULTILIB_OPTIONS") != -1:
			multilib_opt_extend.append(line)
			continue

		if line.startswith("MULTILIB_OPTIONS") and line.split("=")[1] != "":
			opt = line[line.index("=") + 1:].strip().split(" ")
			for i in opt:
				i = i.split("/")
				multilib_opt.append(i)

		if (line.startswith("MULTILIB_EXCEPTIONS") or line.startswith("MULTILIB_EXCLUSIONS")) and line.split("=")[1] != "":
			exp = line[line.index("=") + 1:].strip().split(" ")
			for i in exp:
				i = i.replace("*", "").split("/")
				multilib_exp.append(i)

	tab = get_multilib_table(multilib_opt, multilib_exp)

	# compatibility for gcc multilib option
	for t in tab:
		if not get_gcc_multilib_opt(t, "mcpu="):
			opts = component["gcc"]["no-multilib"][options.abi]
			get_gcc_multilib_opt(t, "", "as", get_gcc_multilib_opt(opts, "mcpu="))

		for i in multilib_opt_extend:
			opts = i[:i.index(".")].strip().strip('(').strip(')').split('|')
			for opt in opts:
				get_gcc_multilib_opt(t, opt, "as", get_gcc_multilib_opt([i], "MULTILIB_OPTIONS", "MULTILIB_OPTIONS="), True)
	return tab

def get_gcc_multilib_opt(tab, match_str, operator = "", replace = "", all_match = False):

	ret = ""
	if tab is None: return ret

	for i in tab:

		if all_match and i != match_str:
			continue

		index = i.find(match_str)
		if index == -1:
			continue

		if operator == "":
			ret = i
		if "=" in operator:
			ret = i[i.index(operator) + len(operator):]
			ret = ret.strip()
		if operator == "k":
			ret = i[:i.index(match_str)]
		if operator == "r":
			ret = replace
		if operator == "av":
			i = i.strip()
			i += replace
			ret = i
		if operator == "as":
			tab.append(replace)
			ret = replace
		if operator == "rs":
			ret = tab[tab.index(i)]
			tab[tab.index(i)] = replace

		break
	return ret

# TODO: need to parser gcc's file to get multilib dir
def get_gcc_multilib_install_dir(options, argv = "", root = None):
	if root is None:
		install = "%s/%s/libc/" % (options.prefix, get_target_name(options))
	else:
		install = root + "/"

	if options.no_multilib:
		return install

	# multilib dir level: endian/cpu/fp/fabi/stm
	if (get_gcc_multilib_opt(argv, "mbig-endian") != ""):
		install += "/big"

	dirs = {
		""		: { "mcpu=ck807f" : "ck807",
				},
		"elf"	: {	"mcpu=ck801" : "ck801", "mcpu=ck802"   : "ck802",
					"mcpu=ck803" : "ck803", "mcpu=ck803sf" : "ck803s",
					"mcpu=ck803f" : "ck803", "mcpu=ck860" : "ck860",
				},
	}
	for (k, v) in dirs.items():
		if k and not options.tos.startswith(k):
			continue
		cpu = get_gcc_multilib_opt(argv, "mcpu=")
		if cpu in v.keys():
			install += "/%s" % v[cpu]
			break

	if (get_gcc_multilib_opt(argv, "mhard-float") != ""):
		install += "/hard-fp"

	v = get_gcc_multilib_opt(argv, "mfloat-abi", "=")
	if v: install += "/fabi" + v

	if (get_gcc_multilib_opt(argv, "mstm") != "") or (get_gcc_multilib_opt(argv, "mmultiple-stld") != ""):
		install += "/stm"

	return install

def get_gcc_multilib_compiler_flags(options, mm, argv = "", f = ""):
	flag = ""
	flags = { "" 					: "-O2",
			  "mcpu" 				: "",
			  "-float" 				: "",
			  "mpic" 				: "-fPIC",
			  "mstm"				: "",
			  "mmultiple-stld" 		: "",
			  "-endian"				: "",
			  "mfloat-abi=v2" 		: "",
	}
	if f: flags = f

	for (k, v) in flags.items():
		if not k and v:
			flag += build_cmd(options, v)
			continue
		if get_gcc_multilib_opt(argv, k):
			if not v: v = "-" + get_gcc_multilib_opt(argv, k)
			flag += build_cmd(options, v)
	# TODO: put debug attr into argv
	if get_component_is_debug(options, mm):
		flag += build_cmd(options, "-g")

	return flag

def build_minilibc(options, argv):
	cmd = build_cmd(options, "tar -zxf %s/elf_minilibc_base.tar.gz;", options.minilibc_src)
	cmd += build_cmd(options, "cp -rf csky-abiv2-elf/* %s/csky-abiv2-elf", options.prefix)
	cmd_exec_with_checkerr(options, cmd)

def build_uclibc(options, argv):
	cmd = "rm -rf ./* && cp -af %s/* ." % options.uclibc_src
	cmd_exec_with_checkerr(options, cmd)

	if os.path.isfile(".config"):
		cmd_exec_with_checkerr(options, "make distclean && rm -rf .config")

	cmd = "cp -af ckcore-linux-uClibc.config .config"
	cmd_exec_with_checkerr(options, cmd)

	# special do
	cpu = get_gcc_multilib_opt(argv, "mcpu", "=")
	cpu = cpu.replace("f", "")
	if cpu == "ck610": cpu = "ck610m"

	change = {
		"CROSS_COMPILER_PREFIX" 		: [get_target_name(options) + "-", True],
		"UCLIBC_EXTRA_CFLAGS" 			: [get_gcc_multilib_opt(argv, "mfloat-abi=v2", "r", "-mfloat-abi=v2"), True],

		"ARCH_STM" 						: ["y", get_gcc_multilib_opt(argv, "mstm") or get_gcc_multilib_opt(argv, "mmultiple-stld")],
		"ARCH_HAS_NO_STM" 				: ["y", not (get_gcc_multilib_opt(argv, "mstm") or get_gcc_multilib_opt(argv, "mmultiple-stld"))],

		"CONFIG_CSKY_ABIV2"				: ["y", options.abi == "abiv2"],
		"ARCH_DELAY_SLOT"				: ["y", False],

		"ARCH_BIG_ENDIAN" 				: ["y", get_gcc_multilib_opt(argv, "mbig-endian")],
		"ARCH_WANTS_BIG_ENDIAN" 		: ["y", get_gcc_multilib_opt(argv, "mbig-endian")],
		"ARCH_LITTLE_ENDIAN" 			: ["y", not get_gcc_multilib_opt(argv, "mbig-endian")],
		"ARCH_WANTS_LITTLE_ENDIAN" 		: ["y", not get_gcc_multilib_opt(argv, "mbig-endian")],

		"UCLIBC_HAS_MMU"				: ["y", True],
		"ARCH_USE_MMU" 					: ["y", True],
		"ARCH_HAS_MMU"					: ["y", True],
		"ARCH_HAS_NO_MMU"				: ["y", False],
		"EXCLUDE_BRK"					: ["y", False],
		"MALLOC_SIMPLE"					: ["y", False],
		"MALLOC_STANDARD"				: ["y", True],
		"MALLOC_GLIBC_COMPAT"			: ["y", True],

		"HAS_FPU"						: ["y", get_gcc_multilib_opt(argv, "mhard-float")],
		"UCLIBC_HAS_FPU"				: ["y", get_gcc_multilib_opt(argv, "mhard-float")],

		"DOPIC" 						: ["y", get_gcc_multilib_opt(argv, "mpic")],
		"HAVE_SHARED"					: ["y", True],

		"UCLIBC_HAS_STRING_GENERIC_OPT" : ["y", True],
		"UCLIBC_HAS_STRING_ARCH_OPT"	: ["y", True],

		"KERNEL_HEADERS"				: [options.linux_libc_headers_install, True],

		"DODEBUG"						: ["y", get_component_is_debug(options, "uclibc")],
	}
	change["CONFIG_" + cpu.upper()] = ["y", True]

	fn = ".config"
	if not os.path.isfile(fn):
		return

	fd = open(fn)
	contents = fd.readlines()
	fd.close()
	for i in range(len(contents)):
		contents[i] = contents[i].strip()

		for k in change.keys():
			if (contents[i].find(k + "=") != -1) or (contents[i].find(" " + k + " is not set") != -1):
				enable = change[k][1]
				if not enable: continue

				v = "\"%s\"" % change[k][0]
				if change[k][0] == "y": v = "%s" % change[k][0]
				#print "old: " + contents[i]
				#print "new: %s=%s" % (k, v)
				cmd = "sed -i '%ds:.*:%s=%s:' %s" % (i + 1, k, v, fn)
				cmd_exec_with_checkerr(options, cmd)

	cmd = "make oldconfig KERNEL_SOURCE=%s && make clean && make" % (options.linux_libc_headers_install + "/../")
	cmd_exec_with_checkerr(options, cmd)

	cmd = "cd lib/ && ln -s ld-uClibc-0.9.33.2.so ld.so.1"
	cmd_exec_with_checkerr(options, cmd)

	if not os.path.isfile("lib/crt0.o"):
		cmd_exec_with_checkerr(options, "cp lib/crt1.o lib/crt0.o")

	install = get_gcc_multilib_install_dir(options, argv)
	cmd = "make install PREFIX=%s " % install
	cmd_exec_with_checkerr(options, cmd)

	install = "%s/%s/libc/" % (options.prefix, get_target_name(options))
   	cmd = "cd %s && mv usr/include tmpinclude " % install
   	cmd += '&& for i in `find . -name "include"` ; do\nrm -rf $i\ndone '
   	cmd += '&& mv tmpinclude usr/include '
   	cmd_exec_with_checkerr(options, cmd)

def build_uclibc_ng(options, argv):
	cmd = "rm -rf ./* && cp -af %s/* ." % options.uclibc_ng_src
	cmd_exec_with_checkerr(options, cmd)

	if os.path.isfile(".config"):
		cmd_exec_with_checkerr(options, "make distclean")

	change = [get_gcc_multilib_opt(argv, "mcpu", "=").strip("f") + get_gcc_multilib_opt(argv, "mhard-float", "r", "f"),
			  get_gcc_multilib_opt(argv, "mbig-endian", "r", "be") or "le",
			 ]
	config = "_".join(change) + "_defconfig"
	cmd_exec_with_checkerr(options, "make ARCH=csky %s" % config)

	cmd = build_cmd(options, "sed -i '/^KERNEL_HEADERS.*/d' .config")
	cmd += build_cmd(options, "&& echo 'KERNEL_HEADERS=\"%s\"' >> .config", options.linux_libc_headers_install)
	cmd_exec_with_checkerr(options, cmd)
	cmd = build_cmd(options, "sed -i '/^UCLIBC_EXTRA_CFLAGS.*/d' .config")
	cmd += build_cmd(options, "&& echo 'UCLIBC_EXTRA_CFLAGS=\"%s\"' >> .config", get_gcc_multilib_opt(argv, "mfloat-abi=v2", "r", "-mfloat-abi=v2"))
	cmd_exec_with_checkerr(options, cmd)

	cmd = "make oldconfig KERNEL_SOURCE=%s && make clean && make" % (options.linux_libc_headers_install + "/../")
	cmd_exec_with_checkerr(options, cmd)

	cmd = "cd lib/ && ln -s ld-uClibc.so.1 ld.so.1"
	cmd_exec_with_checkerr(options, cmd)

	if not os.path.isfile("lib/crt0.o"):
		cmd_exec_with_checkerr(options, "cp lib/crt1.o lib/crt0.o")

	install = get_gcc_multilib_install_dir(options, argv)
	cmd = "make install PREFIX=%s " % install
	cmd_exec_with_checkerr(options, cmd)

	install = "%s/%s/libc/" % (options.prefix, get_target_name(options))
	cmd = "cd %s && mv usr/include tmpinclude " % install
	cmd += '&& for i in `find . -name "include"` ; do\nrm -rf $i\ndone '
	cmd += '&& mv tmpinclude usr/include '
	cmd_exec_with_checkerr(options, cmd)

def build_linux_libc_headers(options, argv):
	if not get_gcc_multilib_opt(options.linux_libc_headers_src_attr, "type=inc"):
		if not os.path.isdir("kernel"):
			cmd = "ln -s %s kernel" % options.linux_libc_headers_src
			cmd_exec_with_checkerr(options, cmd)
		options.linux_libc_headers_src = options.linux_libc_headers_build
		cmd = "cd kernel && make mrproper && make ARCH=csky INSTALL_HDR_PATH=%s headers_install " % options.linux_libc_headers_src
		cmd_exec_with_checkerr(options, cmd)

	cmd = build_cmd(options, "mkdir -p %s;", options.linux_libc_headers_install)
	cmd += build_cmd(options, "cp -af %s/include/* %s;", (options.linux_libc_headers_src, options.linux_libc_headers_install))
	cmd_exec_with_checkerr(options, cmd)

def build_glibc_compatibility(options, component_chain):
	if not get_component_version(options, "glibc") >= "2.25":
		build_cmd_compatibility(options, "libc_cv_ld_gnu_indirect_function")
	return True

def build_glibc(options, argv):
	cmd = build_cmd(options, "rm -rf ./* && %s/configure", options.glibc_src)
	cmd += build_cmd(options, "--host=%s --target=%s", (get_target_name(options), get_target_name(options)))
	cmd += build_cmd(options, "--with-headers=%s", options.linux_libc_headers_install)
	cmd += build_cmd(options, "--prefix=/usr/ libc_cv_slibdir=/lib libc_cv_libdir=/usr/lib/")

	t = {"CC"  : "gcc", "CXX" : "g++", "AS"  : "as", "LD"  : "ld"}
	endian = get_gcc_multilib_opt(argv, "mbig-endian", "r", "EB") or "EL"
	for i in t.keys():
		cmd += build_cmd(options, '%s=\"%s-%s -%s -%s\"', (i, get_target_name(options), t[i], get_gcc_multilib_opt(argv, "mcpu"), endian))

	cmd += build_cmd(options, "CFLAGS=\"%s\"", get_gcc_multilib_compiler_flags(options, "glibc", argv))
	cmd += build_cmd(options, "CPPFLAGS=\"%s\"", get_gcc_multilib_compiler_flags(options, "glibc", argv))
	cmd += build_cmd(options, 'LDFLAGS=\"-L</lib>  -Wl,-s \"')

	cmd += build_cmd(options, "--enable-shared \
	--enable-kernel=2.6.25 \
	--disable-check-abi \
	--disable-profile \
	--enable-bounded \
	--enable-stackguard-randomization \
	--disable-all-warnings \
	--disable-build-nscd \
	--disable-nscd \
	--enable-obsolete-rpc \
	--enable-static-nss \
	libc_cv_forced_unwind=yes \
	libc_cv_ctors_header=yes \
	libc_cv_c_cleanup=yes \
	libc_cv_pic_default=yes \
	libc_cv_gcc_static_libgcc= ")

	fp = get_gcc_multilib_opt(argv, "mhard-float", "r", "--with-fp") or "--without-fp"
	cmd += build_cmd(options, fp)

	cmd += build_cmd(options, "libc_cv_ld_gnu_indirect_function=no")

	cmd += build_cmd(options, "%s", component["glibc"]["append"])

	install = get_gcc_multilib_install_dir(options, argv)
	cmd += build_cmd(options, "&& make && make install install_root=%s", install)
	cmd_exec_with_checkerr(options, cmd)

	# rename lib*.a -> lib*_pic.a if use "-fPIC"
	if get_gcc_multilib_opt(argv, "mpic"):
		install += "/usr/lib/"
		cmd = "cd %s " % install
		cmd += '&& for i in `find . -type f -name \'lib*.a\' | sed -e \'s/lib\///\'` ; do\nmv $i `echo $i | sed -e \'s/\.a/_pic.a/\'`;\ndone '
		cmd_exec_with_checkerr(options, cmd)

	# cp crt1.o to crt0.o
	cmd = "cd %s " % options.prefix
   	cmd += '&& for i in `find . -name "crt1.o"` ; do\ncp $i `echo ${i} | sed \'s/crt1/crt0/\'`\ndone '
   	cmd_exec_with_checkerr(options, cmd)

   	install = "%s/%s/libc/" % (options.prefix, get_target_name(options))
   	cmd = "cd %s && mv usr/include tmpinclude " % install
   	cmd += '&& for i in `find . -name "include"` ; do\nrm -rf $i\ndone '
   	cmd += '&& mv tmpinclude usr/include '
   	cmd_exec_with_checkerr(options, cmd)

def get_component_chain(options, mm):
	(m, stage) = get_component(options, mm)
	deps = ""
	if "worker" in component[m].keys():
		deps = component[m]["worker"][stage][1]

	mm = [mm]
	if not deps:
		return mm
	deps = deps.replace(" ", "").split(",")
	for m in deps:
		m = get_component_chain(options, m)
		# remove dup deps
		for i in m:
			if i in mm:
				mm.remove(i)
		mm = m + mm
	return mm

def get_component_valid_chain(options, mm, init = False, get_components = False):
	chain = []
	for m in mm:
		c = get_component_chain(options, m)
		if not chain:
			chain = c
		else:
			# set index of last match of new chain
			ii = ""
			for i in c:
				if i in chain: ii = i
				else: break
			# insert new chain in to chain pool
			if ii:
				c = c[c.index(ii) + 1:]
				for i in range(len(c)):
					chain.insert(chain.index(ii) + 1 + i, c[i])
			else:
				chain.extend(c)

	for m in chain:
		if m not in component.keys():
			attr = m.lstrip("-").replace("-", "_")
			if hasattr(options, attr):
				v = getattr(options, attr)
				chain[chain.index(m)] = v

	if options.no_deps:
		if "*" in options.no_deps:
			chain = [mm[0]]
		else:
			for m in options.no_deps:
				if m in chain:
					chain.remove(m)

	cchain = []
	for m in chain:
		(m, stage) = get_component(options, m)
		if m not in cchain: cchain.append(m)
		if not init:
			url = get_component_url(options, m)
			if url["type"] != "local":
				if "url" not in component[m].keys():
					continue
				print "\n<-- component '%s' source code dir is not valid, please run with additional command '--init'" % m
				return ""

	if get_components: chain = cchain
	return chain

def get_component_valid_compatibility(options, component_chain):
	for mm in component_chain:
		(mm, stage) = get_component(options, mm)
		if "compatibility" in component[mm].keys():
			if not component[mm]["compatibility"](options, component_chain):
				print "<-- current component '%s' version '%s' has some compatibility problems" % (mm, get_component_version(options, mm))
				return False
	return True

def get_component_url(options, mm):
	url = {}
	attr = mm.replace("-", "_") + "_src"
	t = getattr(options, attr)
	if os.path.isdir(t):
		url = {"type" : "local", "url" : t}
	else:
		# FIXME: compatibility format between cmd and url
		v = getattr(options, attr + "_attr")
		if v: t += "," + ",".join(v)
		url = {"type" : "url", "url" : t}
	return url

def get_component_is_debug(options, mm):
	if mm and options.debug and mm in options.debug:
		return True
	return False

def get_component_version(options, mm):
	v = ""
	if mm == "gcc":
		cmd = build_cmd(options, "cat %s/gcc/BASE-VER", options.gcc_src)
		v = cmd_exec_ret_with_checkerr(options, cmd)
	if mm == "glibc":
		cmd = build_cmd(options, "cat %s/version.h", options.glibc_src)
		ret = cmd_exec_ret_with_checkerr(options, cmd).split()
		v = ret[ret.index("VERSION") + 1].strip("\"")
	return v

def build_toolchain_env(options, mm):

	def get_toolchain_component_url_cmd(options, m, url):
		s = url.split(",")
		url = s[0]
		opt = s[1:]
		cmd = ""

		if url.startswith("ssh://"):
			if url.startswith("ssh://@"): url = url.replace("@", options.user + "@")

			cmd = build_cmd(options, "git clone %s %s", (url, source_dirname + "/" + m))
			cmd += build_cmd(options, "%s", " ".join(opt))

                if url.startswith("git@"):
			cmd = build_cmd(options, "git clone %s %s", (url, source_dirname + "/" + m))
			cmd += build_cmd(options, "%s", " ".join(opt))

		return cmd

	def build_toolchain_component(options, mm):
		info = get_component_url(options, mm)
		type = info["type"]
		url = info["url"]

		if type == "local":
			print "\n<-- component '%s' source code url ['%s'] is ok" % (mm, url)
			return

		# append all urls into ss, the first url is prefer
		ss = [url]
		if "url" in component[mm].keys():
			ss += [component[mm]["url"]]

		cmd = ""
		for s in ss:
			cmd = get_toolchain_component_url_cmd(options, mm, s)
			if not cmd: continue

			print "\n--> " + cmd
			(o, e, r) = cmd_exec(options, cmd)
			if cmd_exec_is_error(r, e):
				cmd = ""
				continue
			break
		if not cmd:
			print "\n<-- component '%s' source code url %s is not valid" % (mm, ss)

	component_chain = get_component_valid_chain(options, mm, True, True)
	print "\n====> toolchain components = %s" % str(component_chain)

	for mm in component_chain:
		sdir = getattr(options, mm.replace("-", "_") + "_src")
		if options.command:
			if os.path.isdir(sdir):
				os.chdir(sdir)
				cmd_exec_with_checkerr(options, options.command)
				os.chdir(scritp_dirname)
			continue
		build_toolchain_component(options, mm)

def build_worker(options, mm, stage = 0):

	if options.command and not options.command.startswith("@"):
		cmd_exec_with_checkerr(options, options.command)
		return

	worker = component[mm]["worker"][stage][0]

	if "multilib" in component[mm].keys():
		param = component[mm]["multilib"]
		tab = build_gcc_multilib(options, param)

		for i in tab:
			i = tuple(i)
			print "\n--> multilib option: %s" % str(i)
			f = get_finished_target(options, mm, stage, i)
			if build_is_finished(options, f):
				continue
			worker(options, i)
			cmd_exec_with_checkerr(options, "touch '%s'" % f)
			build_log(options, os.path.basename(f))
	else:
		worker(options, "")

def build_log(options, log, init = False):
	if not os.path.isdir(options.build):
		cmd_exec_with_checkerr(options, "mkdir -p %s" % options.build)
	options.log = options.build + "/build.log"
	opt = ">"
	if not init: opt = ">>"
	cmd_exec_with_checkerr(options, "echo \"%s\" %s %s" % (str(log), opt, options.log))

# TODO: simplify dir path
def build_init(options):
	options.cmd_compatibility = []

	if options.no_deps:
		options.no_deps = options.no_deps.replace(" ", "").split(",")

	if options.no_multilib is not None:
		opts = component["gcc"]["no-multilib"][options.abi]
		opts += component["gcc"]["no-multilib"]["common"]
		opts.sort()
		if options.no_multilib:
			options.no_multilib = options.no_multilib.replace(" ", "").split(",")
		else:
			options.no_multilib = opts
		for i in ["mcpu", "-endian", "-float"]:
			if not get_gcc_multilib_opt(options.no_multilib, i):
				opt = get_gcc_multilib_opt(opts, i)
				options.no_multilib.append(opt)
		options.no_multilib.sort()

	if options.debug:
		options.debug = options.debug.replace(" ", "").split(",")
		if "*" in options.debug: options.debug = component.keys()

	if options.addon:
		options.addon = options.addon.replace(" ", "").split(",")
		if "*" in options.addon: options.addon = addons.keys()

	if not options.build:
		if not options.prefix:
			options.build = scritp_dirname + "/build-" + get_target_dir(options)
		else:
			options.build, name = os.path.split(os.path.abspath(options.prefix))
			options.build += "/build-" + name
	elif not options.build.startswith("/"):
		options.build = scritp_dirname + "/" + options.build

	if not options.prefix:
		options.prefix = scritp_dirname + "/install-" + get_target_dir(options)
	elif not options.prefix.startswith("/"):
		options.prefix = scritp_dirname + "/" + options.prefix

	if not options.tcprefix:
		options.tcprefix = options.prefix + "/bin/"

	options.linux_libc_headers_install = "%s/%s/libc/usr/include/" % (options.prefix, get_target_name(options))

	for m in component.keys():
		opt = m.replace("-", "_") + "_src"
		t = getattr(options, opt).split(",")
		setattr(options, opt, t[0])
		setattr(options, opt + "_attr", t[1:])
		opt = m.replace("-", "_") + "_build"
		setattr(options, opt, options.build + "/" + m)

def main():
	global component

	parser = OptionParser(version="%prog 2.41")

	parser.add_option("--abi", dest="abi", default=profile["abi"][0],
	                  help=("select abi version (default: %s)" % profile["abi"][0]), metavar=str(profile["abi"]))

	parser.add_option("--tos", dest="tos", default=profile["tos"][0],
	                  help=("select target os (default: %s)" % profile["tos"][0]), metavar=str(profile["tos"]))

	parser.add_option("--libc", dest="libc", default=profile["libc"][0],
	                  help=("select libc (default: %s)" % profile["libc"][0]), metavar=str(profile["libc"]))

	parser.add_option("-m", dest="component",
					  help="select the component(with dependents) to build", metavar=str(component.keys()))

	parser.add_option("--addon", dest="addon",
					  help="enable addon to build (\"*\" means enable all addons, multiple addons are splited by \",\")", metavar=str(addons.keys()))

	parser.add_option("--no-deps", dest="no_deps", help="ignore the dependent components if it exist (\"*\" means ignore all deps, multiple components are splited by \",\")")

	parser.add_option("--no-multilib", dest="no_multilib", default=None, help="set '--no-multilib= ' as default option or select specific lib option if it exist \
					  (you can find option format from build print log according to keywords 'multilib option'. multiple options are splited by \",\")")

	parser.add_option("--update", dest="update", help="rebuild the component and which are dependent on that if it exist")

	parser.add_option("--debug", dest="debug",
					  help="create debug version of specific component (\"*\" means all components, multiple components are splited by \",\")")

	parser.add_option("-c", "--command", dest="command", help="shell command string to been executed")

	parser.add_option("-r", "--rbuild",
					  action="store_true", dest="rbuild", default=False,
					  help="delete target & build if it exist")

	parser.add_option("--init",
					  action="store_true", dest="init", default=False,
	                  help="only initialize/check the building env(source code) if it exist")

	# helpers
	parser.add_option("--user", dest="user", default=os.environ['USER'],
	                  help=("set git user (default: %s)" % os.environ['USER']))

	parser.add_option("--makejob", dest="makejob", default="1",
					  help="allow N jobs at once to speed up build (default: 1, '--makejob= ' means the max speed)")

	parser.add_option("--time",
					  action="store_true", dest="time", default=False,
	                  help="append timestamp with output dirs")

	parser.add_option("--fake",
					  action="store_true", dest="fake", default=False,
	                  help="print build command without any real execution if it exist")

	# dirs
	parser.add_option("--prefix", dest="prefix", help="select install dir")

	parser.add_option("--build", dest="build", help="select build dir")

	parser.add_option("--gcc-dep-libs", dest="gcc_dep_libs", help="select dependent libs(libmpc/mpfr/gmp) dir of gcc, multiple dirs are splited by \",\"")

	parser.add_option("--tcprefix", dest="tcprefix", help="select toolchain bin dir")

	component = dict(component, **addons)

	for m in component.keys():
		opt = m + "-src"
		h = "select %s source code dir (default: %s/%s)" % (m, source_dirname, m)
		if "comment" in component[m].keys(): h += " %s" % component[m]["comment"]
		parser.add_option("--" + opt, dest=opt.replace("-", "_"), default=source_dirname + "/" + m, help=(h))

	(options, args) = parser.parse_args()
	options.parser = parser

	build_init(options)

	mm = ["gcc"]
	if options.component:
		mm = [options.component]
	if options.addon:
		mm += options.addon

	mm.append("gdb")
	if options.init:
		build_toolchain_env(options, mm)
		return

	component_chain = get_component_valid_chain(options, mm)
	if not component_chain: return
	print "\n====> components chain = %s" % str(component_chain)

	if not get_component_valid_compatibility(options, component_chain): return

	build_log(options, "command line:\t" + " ".join(sys.argv), True)
	build_log(options, "component build chain:\t" + str(component_chain))

	for mm in component_chain:
		(mm, stage) = get_component(options, mm)
		if not build_start(options, mm, stage):
			continue
		build_worker(options, mm, stage)
		build_return(options, mm, stage)

	print "\n====> success to build component chain: %s" % str(component_chain)
	print "--> install dir: %s\n" % options.prefix


profile = {
	"abi"		: ["abiv2", "abiv1"],
	"libc"		: ["minilibc", "glibc", "uclibc", "uclibc-ng"],
	"tos"		: ["elf", "linux", "ecos"],
}

component = {
        "binutils"	: { "url"		: "git@github.com:c-sky/binutils-gdb.git",
					"debug" 	: 'CFLAGS="-g -O0" CXXFLAGS="-g -O0"',
					"default" 	: '--disable-gdb --disable-werror',
					"worker" 	: [(build_binutils, "")],
					"tos" 		: {"linux" : "--with-sysroot=yes"},
				  },

        "gcc"		: { "url"		: "git@github.com:c-sky/gcc.git",
					"debug" 	: 'CFLAGS="-g -O0" CXXFLAGS="-g -O0"',
					"worker" 	: [(build_gcc_initial, "binutils"), (build_gcc, "--libc")],
					"bos" 		: build_gcc_bos,
					"tos" 		: build_gcc_tos,
					"no-multilib"
								: { "common" : ["mlittle-endian", "msoft-float"],
									"abiv1"  : ["mcpu=ck610f"],
									"abiv2"  : ["mcpu=ck810f"],
								  },
					"compatibility"
								: build_gcc_compatibility,
				  },

        "minilibc"	: { "url"		: "git@github.com:c-sky/toolchain-build.git",
					"worker" 	: [(build_minilibc, "gcc.0")],
				  },

	"uclibc"	: { "url"		: "ssh://@192.168.0.78:29418/tools/uClibc, --branch csky-uclibc-0.9.33.2",
					"worker" 	: [(build_uclibc, "linux-libc-headers, gcc.0")],
					# Don't need to build static library specially, because the static
					# library will be created when build "do share library build".
					"multilib"	: ["MULTILIB_OPTIONS=mpic"]
				  },

        "uclibc-ng"	: { "url"		: "git@github.com:c-sky/uclibc-ng.git, --depth=1",
					"worker" 	: [(build_uclibc_ng, "linux-libc-headers, gcc.0")],
					"multilib"	: ["MULTILIB_OPTIONS=mpic"]
				  },

        "glibc"		: { "url"		: "git@github.com:c-sky/glibc.git",
					"worker" 	: [(build_glibc, "linux-libc-headers, gcc.0")],
					"multilib"	: ["MULTILIB_OPTIONS=mpic/mno-pic"],
					"compatibility"
								: build_glibc_compatibility,
				  },

	"linux-libc-headers"		:
				  {
                                      "url"		: "git@github.com:c-sky/linux-4.9.y.git, --depth=1",
				  	"worker" 	: [(build_linux_libc_headers, "")],
				  	"comment"	: "this is dir of linux kernel source code as default because the headers are geted from that :) \
				  				  also you can set pure linux include dir like '--linux-libc-headers-src=$(your/include/../path),type=inc' \
				  				  "
				  },
	"gdb"	:
		{
			"url"	: "git@github.com:c-sky/binutils-gdb.git,  --branch=gdb-7.12-branch-csky",
			"default" 	: '--disable-ld --disable-gas --disable-binutils --disable-gold --disable-gprof --without-auto-load-safe-path --with-python=no --disable-sim --enable-install-libbfd',
			"worker" 	: [(build_gdb, "")],
		},
}


def build_libcc_rt(options, argv):

	cmd = build_cmd(options, "rm -rf ./* && %s/configure.nolink", options.libcc_rt_src)
	cmd += build_cmd(options, "--host=%s", get_target_name(options))
	cmd += build_cmd(options, "CFLAGS=\"%s\"", get_gcc_multilib_compiler_flags(options, "libcc-rt", argv))

	install = "%s/%s/lib" % (options.prefix, get_target_name(options))
	cmd += build_cmd(options, "--libdir=%s", get_gcc_multilib_install_dir(options, argv, install))

	cmd += build_cmd(options, "&& make && make install")

	cmd_exec_with_checkerr(options, cmd)


# TODO: get installed gcc tools to run test
# TODO: save ok/failed tmp object to specific target dir
# TODO: only patched for debuging
def build_gcc_test(options, argv):

	def get_gcc_test_compiler_flags(options, argv):
		flags = { "mccrt" 				: "",
				  "mfloat-abi=v2" 		: "",
		}
		return get_gcc_multilib_compiler_flags(options, "", argv, flags)

	def build_gcc_test_patch(options, argv, do):
		patchd = options.gcc_src + "/gcc/testsuite/gcc.target/csky/patches"
		attrs = list(argv)
		if not do: attrs.reverse()

		for attr in attrs:
			patchf = patchd + "/" + attr + ".patch"

			if not os.path.isfile(patchf):
				continue
			f = patchd + "/" + "." + attr + ".patched"
			if os.path.isfile(f) and do:
				continue
			if not os.path.isfile(f) and not do:
				continue

			cmd = build_cmd(options, "cd %s", options.gcc_src)
			cmd += build_cmd(options, "&& patch -p1 < %s", patchf)
			if not do: cmd += build_cmd(options, "-R")
			cmd_exec_with_checkerr(options, cmd)

			cmd = "touch %s" % f
			if not do: cmd = "rm -rf %s" % f
			cmd_exec_with_checkerr(options, cmd)

	opt = (options.command and options.command.strip("@").split(",")) or []

	for i in ["mcpu", "-endian", "-float"]:
		o = get_gcc_multilib_opt(opt, i)
		a = get_gcc_multilib_opt(argv, i)
		if o and a and o != a:
			print "<-- current config is filtered out by option '%s'" % o
			return
	for i in argv:
		if i in opt:
			continue
		if "no-" in i:
			ii = i.replace("no-", "")
		else:
			ii = i[0] + "no-" + i[1:]
		if ii in opt:
			print "<-- current config is filtered out by option '%s'" % ii
			return

	debug = (get_component_is_debug(options, "gcc-test") and "-v -v -v") or ""
	debug = get_gcc_multilib_opt(opt, "debug", "=") or debug

	deja = get_gcc_multilib_opt(opt, "deja", "=") or ("DEJAGNU" in os.environ and os.environ["DEJAGNU"])
	if not deja:
		cmd = build_cmd(options, "echo 'lappend boards_dir = \"%s\"' > site.exp", options.gcc_test_build)
		cmd_exec_with_checkerr(options, cmd)
		deja = options.gcc_test_build + "/site.exp"

	cpu = get_gcc_multilib_opt(argv, "mcpu", "=")
	cpu = get_gcc_multilib_opt(opt, "mcpu", "=") or cpu
	cpu = cpu.replace("f", "")

	endian = get_gcc_multilib_opt(argv, "-endian")
	endian = get_gcc_multilib_opt(opt, "-endian") or endian

	fp = get_gcc_multilib_opt(argv, "-float")
	fp = get_gcc_multilib_opt(opt, "-float") or fp

	machine = get_gcc_multilib_opt(argv, "machine", "=")
	machine = get_gcc_multilib_opt(opt, "machine", "=") or machine or "smartl"

	board = get_gcc_multilib_opt(opt, "board", "=")
	if not board:
		board = "csky-sim-%s-" % options.tos
		board += "@".join(argv).replace("=", "-").replace("-", "_").replace("@", "-")
		if os.path.isdir(options.gcc_test_build):
			fd = open(board + ".exp", "w"); fd.write(eval("csky_sim_%s_exp" % options.tos)); fd.close()
		# TODO: merge cflags with get_gcc_multilib_compiler_flags
		cflags = "-march=%s -%s -%s %s" % (cpu, endian, fp, get_gcc_test_compiler_flags(options, argv))
		cmd = build_cmd(options, "sed -i 's/^set csky_cflags.*/set csky_cflags \"%s\"/' %s.exp", (cflags, board))
		if options.tos.startswith("elf"):
			bsp_srcdir = "$srcdir\/gcc.target\/csky\/arch\/%s\/%s\/qemu" % (machine, cpu)
			cmd += build_cmd(options, "&& sed -i 's/^set csky_bsp_srcdir.*/set csky_bsp_srcdir \"%s\"/' %s.exp", (bsp_srcdir, board))
		cmd_exec_with_checkerr(options, cmd)

	testcase = get_gcc_multilib_opt(opt, "testcase", "=") or ""

	endian = (endian == "mbig-endian" and "eb") or ""
	if fp == "mhard-float": cpu += "f"
	simdef = { "elf" 	: "qemu-system-cskyv%s%s -nographic -machine %s -cpu %s -kernel" % (options.abi[-1], endian, machine, cpu),
			   "linux"	: "qemu-cskyv%s%s -cpu %s -L %s" % (options.abi[-1], endian, cpu, get_gcc_multilib_install_dir(options, argv))
	}
	sim = simdef[options.tos]
	cmd_exec_with_checkerr(options, "which %s" % sim.split(" ")[0])

	outdir = options.gcc_test_build + "/" + board
	if debug: outdir += "-debug"

	build_gcc_test_patch(options, argv, True)
	cmd = build_cmd(options, "cd %s", options.gcc_build)
	cmd += build_cmd(options, "&& mkdir -p %s", outdir)
	cmd += build_cmd(options, "&& DEJAGNU=%s", deja)
	cmd += build_cmd(options, "make check RUNTESTFLAGS=\"--target_board=%s %s SIM='%s' --outdir=%s %s\"", (board, testcase, sim, outdir, debug))
	cmd_exec_with_checkerr(options, cmd)
	build_gcc_test_patch(options, argv, False)
	print "\n--> gcc-test install dir: %s" % outdir

addons = {
	"libcc-rt"	: { "url"		: "ssh://@192.168.0.78:29418/tools/libcc-runtime",
					"worker" 	: [(build_libcc_rt, "gcc.0")],
					"multilib"	: ""
				  },

	"gcc-test"	: { "worker" 	: [(build_gcc_test, "gcc")],
					"multilib"	: ["(mcpu=ck810f|mcpu=ck807f).MULTILIB_OPTIONS=machine=smarth",
								   "MULTILIB_OPTIONS=mccrt/mno-ccrt @ build_is_finished(options, get_finished_target(options, \"libcc-rt\"), True)"],
					"comment"	: "use option '-c' and start with \"@\" parameter if you want to run selected tests. \
								  additional option are [deja, board, machine, testcase, debug]. \
								  ",
				  },
}


if __name__ == "__main__":
	os.chdir(scritp_dirname)
	main()
