#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from Toolchain import Toolchain
from lib.Command import *

class GCCToolchain(Toolchain):
    def __init__(self, triple, src, jobs, version, release_dir, rebuild, short_dir,
                 extra_config, host, build_type, dep_libs_dir, fake, multilib, run_type):
        super(GCCToolchain, self).__init__(triple, src, jobs, version, release_dir, rebuild, short_dir,
                                           extra_config, "gcc", host, build_type, fake)
        self.multilib = multilib
        self.dep_libs_dir = dep_libs_dir
        self._real_dep_lib = ""
        self.run_type = run_type

    @property
    def real_dep_lib(self):
        if self.dep_libs_dir is None:
            return ""
        if not self._real_dep_lib:
            dep_libs_dir = abs_path(os.getcwd(), self.dep_libs_dir)
            if dep_libs_dir.endswith(".tar.gz"):
                self.extract_from_archive_nofake(dep_libs_dir, cwd=self.build_dir)
                lib_path = find(self.build_dir, "libmpc.a")
                lib_path = os.path.split(os.path.dirname(lib_path))[0]
            else:
                lib_path = dep_libs_dir
            self._real_dep_lib = lib_path
        return self._real_dep_lib

    @property
    def dep_libs_config(self):
        if self.dep_libs_dir is None:
            return ""
        config = '--with-mpfr="{}" --with-gmp="{}" --with-mpc="{}"'.format(
            self.real_dep_lib, self.real_dep_lib, self.real_dep_lib
        )
        if "riscv" in self.triple:
            config += ' --with-gcc-dep-libs="{}"'.format(self.real_dep_lib)
        return config

    @property
    def multilib_rules(self):
        if not self.multilib:
            return [["", "."]]
        gcc = self.triple + "-gcc"
        if self.host != "mingw":
            gcc = os.path.join(self.install_dir, "bin", gcc)
        multilib_rules_str = self.execute_nofake("{} --print-multi-lib".format(gcc), stdout=subprocess.PIPE)
        multilib_rules = []
        added_pathes = {}
        for line in multilib_rules_str.split():
            _, opt_str = line.split(";")
            opt = opt_str.replace("@", " -")
            # Calculate the path here instead of reading from multilib rules to avoid
            # recounting the options in MULTILIB_DEFAULTS.
            path = self.execute_nofake("{} {} -print-multi-directory".format(gcc, opt), stdout=subprocess.PIPE).strip()
            if path not in added_pathes:
                multilib_rules.append([opt, path])
                added_pathes[path] = ""
        return multilib_rules

    def get_dep_lib(self, dep_libs_dir):
        if dep_libs_dir is None:
            return None
        dep_libs_dir = abs_path(os.getcwd(), dep_libs_dir)
        if dep_libs_dir.endswith("tar.gz"):
            self.extract_from_archive_nofake(dep_libs_dir, cwd=self.build_dir)
            lib_path = find(self.build_dir, "libmpc.a")
            lib_path = os.path.split(os.path.dirname(lib_path))[0]
            return lib_path
        else:
            return dep_libs_dir