#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import logging
import os
import time
import platform
from lib.Command import *
from lib.Version import Version


class CheckError(BaseException):
    def __init__(self, arg):
        self.args = arg

    def __str__(self):
        return "".join(self.args)


class Toolchain(object):
    def __init__(self, triple, src, jobs, version, release_dir, rebuild, short_dir,
                 extra_config, toolchain_type, host, build_type, fake):
        self.host = host
        self.fake = fake
        self.top_dir = os.getcwd()
        if short_dir:
            work_dir = self.gen_short_dir(self.top_dir)
        else:
            work_dir = "build-{}-{}".format(toolchain_type, triple)
        self.mkdir_nofake(work_dir)
        work_dir = os.path.join(self.top_dir, work_dir)
        self.work_dir = work_dir
        self.triple = triple
        if not os.path.isabs(src):
            src = os.path.join(os.getcwd(), src)
        self.src = src
        if jobs == -1:
            self.jobs = ""
        else:
            self.jobs = jobs
        self.version = version
        if release_dir is not None:
            if not os.path.isabs(release_dir):
                release_dir = os.path.join(os.getcwd(), release_dir)
            if not os.path.exists(release_dir):
                self.mkdir_nofake(release_dir)
        else:
            release_dir = work_dir
        self.release_dir = release_dir
        self.rebuild = rebuild
        self.short_dir = short_dir
        self.extra_config = extra_config
        self.test_result_dir = os.path.join(self.top_dir, "result")
        self.toolchain_type = toolchain_type
        self.build_type = build_type


    @property
    def stamps_dir(self):
        return os.path.join(self.build_dir, "stamps")

    @staticmethod
    def get_cpu_series(triple):
        cpu_series = ""
        if "csky" in triple:
            cpu_series = "Xuantie-800"
        elif "riscv" in triple:
            cpu_series = "Xuantie-900"
        assert cpu_series
        return cpu_series

    @property
    def cpu_series(self):
        return self.get_cpu_series(self.triple)

    @staticmethod
    def get_platform(triple):
        pf = "elf"
        if "linux" in triple:
            pf = "linux"
        return pf

    @property
    def platform(self):
        return self.get_platform(self.triple)

    @staticmethod
    def get_libc(triple):
        libc = "newlib"
        if "linux" in triple:
            if "musl" in triple:
                libc = "musl"
            elif "uclibc" in triple:
                libc = "uclibc"
            else:
                libc = "glibc"
        elif "csky" in triple and "none" not in triple and "unknown" not in triple:
            libc = "minilibc"
        return libc

    @property
    def libc(self):
        return self.get_libc(self.triple)

    # Give the CFLAGS for project don't use cmake.
    # Release usually define to '-O3 -DNDEBUG',
    # but project always build for release as default,
    # so don't override the default value here.
    def build_type_cflags(self):
        cflags_tb = {
            "Release": "",
            "Debug": "-O0 -g3",
            "RelWithDebInfo": "-O2 -g -DNDEBUG",
            "MinSizeRel": "-Os -DNDEBUG"
        }
        return cflags_tb[self.build_type]

    def tar_name(self, has_date=False):
        if self.platform == "linux":
            pf = "linux-{}".format(self.kernel_version)
        else:
            pf = self.platform
        libc = self.libc
        if libc == "musl":
            if "64" in self.triple:
                libc += "64"
            else:
                libc += "32"
        name_base = "{}-{}-{}-{}-{}".format(self.cpu_series, self.toolchain_type, pf,
                                            libc, self.host)
        if self.version is not None:
            name_base += "-{}".format(self.version)
        if has_date:
            return name_base + time.strftime("-%Y%m%d")
        else:
            return name_base

    @property
    def build_dir(self):
        if self.short_dir:
            ret = os.path.join(self.work_dir, "b")
        else:
            ret = os.path.join(self.work_dir, "build-" + self.tar_name())
        return ret

    @property
    def version_number(self):
        if self.platform == "linux":
            pf = "linux-{}".format(self.kernel_version)
        else:
            pf = self.platform
        return "{} {} {} {} Toolchain {} B{}".format(self.cpu_series, pf,
                                                     self.libc, self.toolchain_type,
                                                     self.version, time.strftime("-%Y%m%d"))

    @property
    def install_dir(self):
        return os.path.join(self.work_dir, self.tar_name())

    @staticmethod
    def read_kernel_version(version_file):
        with open(version_file, 'r') as f:
            for line in f.readlines():
                if line.startswith("#define LINUX_VERSION_CODE"):
                    version_number = int(line.split()[-1])
                    return Version.convert_version_to_str(version_number)
            else:
                assert False

    @property
    def kernel_version(self):
        version_file = os.path.join(self.src, "linux-headers", "include", "linux", "version.h")
        return self.read_kernel_version(version_file)

    def tar_release(self):
        archive_format = ".zip" if platform.uname()[0] == "Windows" else ".tar.gz"
        tar_file_date = "{}{}".format(self.tar_name(has_date=True), archive_format)
        tar_file_nodate = "{}{}".format(self.tar_name(has_date=False), archive_format)
        tar_file_date = os.path.join(self.release_dir, tar_file_date)
        tar_file_nodate = os.path.join(self.release_dir, tar_file_nodate)
        self.create_archive(tar_file_date, os.path.basename(self.install_dir),
                            self.work_dir, self.host == "mingw")
        self.copy(tar_file_date, tar_file_nodate)
        return tar_file_date

    @staticmethod
    def stamp_name(name):
        return ".stamp_" + name

    def add_stamp(self, name):
        if not os.path.exists(self.stamps_dir):
            self.mkdir_nofake(self.stamps_dir)
        self.touch(os.path.join(self.stamps_dir, self.stamp_name(name)))

    def has_stamp(self, name):
        return os.path.exists(os.path.join(self.stamps_dir, self.stamp_name(name)))

    def simple_stamp_build(self, name, config, make_target="", install_target="install"):
        if not self.has_stamp(name):
            build_dir = os.path.join(self.build_dir, "build-" + name)
            self.mkdir(build_dir, clean=True)
            self.execute(config, cwd=build_dir)
            self.execute(
                "make {} -j{} && make {} -j{}".format(
                    make_target, self.jobs, install_target, self.jobs
                ),
                cwd=build_dir
            )
            self.add_stamp(name)

    def execute(self, cmd, cwd=None, stdout=None):
        cmd_str = cmd
        if cwd is not None:
            cmd_str = "cd {} && {}".format(cwd, cmd)
        if self.fake:
            print(cmd_str)
            return ""
        else:
            logging.info(cmd_str)
            return execute_cmd(cmd, cwd, stdout)

    @staticmethod
    def execute_nofake(cmd, cwd=None, stdout=None):
        cmd_str = cmd
        if cwd is not None:
            cmd_str = "cd {} && {}".format(cwd, cmd)
        logging.info(cmd_str)
        return execute_cmd(cmd, cwd, stdout)

    def copy(self, src, dst):
        dst = dst.replace(" ", "\\ ")
        if type(src) == list:
            for f in src:
                f = f.replace(" ", "\\ ")
                self.execute('cp -a {} {}'.format(f, dst))
        else:
            src = src.replace(" ", "\\ ")
            self.execute('cp -a {} {}'.format(src, dst))

    def create(self, file_name, content):
        cmd = 'echo {} > {}'.format(content, file_name)
        if self.fake:
            print(cmd)
            return False
        else:
            logging.info(cmd)
            with open(file_name, "w") as fp:
                fp.write(content)
            return True

    def symlink(self, src, dst, cwd=""):
        old_cwd = ""
        if cwd:
            old_cwd = os.getcwd()
            self.chdir(cwd)
        if platform.uname()[0] == "Windows":
            self.copy(src, dst)
        else:
            cmd = "ln -s {} {}".format(src, dst)
            if self.fake:
                print(cmd)
            else:
                logging.info(cmd)
                os.symlink(src, dst)
        if old_cwd:
            self.chdir(old_cwd)

    def chdir(self, path):
        cmd = "cd {}".format(path)
        if self.fake:
            print(cmd)
        else:
            logging.info(cmd)
            os.chdir(path)

    def rm(self, path):
        cmd = "rm -rf {}".format(path)
        if self.fake:
            print(cmd)
        else:
            logging.info(cmd)
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)

    def touch(self, path):
        cmd = "touch {}".format(path)
        if self.fake:
            print(cmd)
        else:
            logging.info(cmd)
            with open(path, "a"):
                os.utime(path, None)

    @staticmethod
    def touch_nofake(path):
        cmd = "touch {}".format(path)
        logging.info(cmd)
        with open(path, "a"):
            os.utime(path, None)

    def mkdir(self, directory, parent=True, clean=False):
        cmd = "mkdir -p {}".format(directory)
        if self.fake:
            print(cmd)
        else:
            logging.info("mkdir: {}".format(directory))
            extend_mkdir(directory, parent, clean)

    @staticmethod
    def mkdir_nofake(directory, parent=True, clean=False):
        logging.info("mkdir: {}".format(directory))
        extend_mkdir(directory, parent, clean)

    def download_ftp(self, url, cwd=None):
        cmd = "wget -c -t3 -T 30 {}".format(url)
        self.execute(cmd, cwd=cwd)

    @staticmethod
    def download_ftp_nofake(url, cwd=None):
        cmd = "wget -c -t3 -T 30 {}".format(url)
        Toolchain.execute_nofake(cmd, cwd=cwd)

    @staticmethod
    def extract_cmd(archive, output_dir=""):
        if archive.endswith(".tar.gz"):
            if platform.uname()[0] == "Windows":
                cmd = "7z x -y {} && 7z x -y {}".format(archive, archive.replace(".tar.gz", ".tar"))
                output_dir_option = "-o"
            else:
                cmd = "tar -xzf {}".format(archive)
                output_dir_option = "-C "
        elif archive.endswith(".zip"):
            if platform.uname()[0] == "Windows":
                cmd = "7z x -y {}".format(archive)
                output_dir_option = "-o"
            else:
                cmd = "unzip {}".format(archive)
                output_dir_option = "-d "
        else:
            assert False
        if output_dir:
            cmd += " {}{}".format(output_dir_option, output_dir)
        return cmd

    def extract_from_archive(self, archive, output_dir="", cwd=None):
        cmd = self.extract_cmd(archive, output_dir)
        self.execute(cmd, cwd=cwd)

    @staticmethod
    def extract_from_archive_nofake(archive, output_dir="", cwd=None):
        cmd = Toolchain.extract_cmd(archive, output_dir)
        Toolchain.execute_nofake(cmd, cwd=cwd)

    def create_archive(self, output_file, input_file, cwd=None, dereference=False):
        if output_file.endswith(".tar.gz"):
            assert platform.uname()[0] != "Windows"
            if dereference:
                cmd = "tar --dereference -czf {} {}".format(output_file, input_file)
            else:
                cmd = "tar -czf {} {}".format(output_file, input_file)
        elif output_file.endswith(".zip"):
            if platform.uname()[0] == "Windows":
                cmd = "7z a -tzip -r {} {}".format(output_file, input_file)
            else:
                cmd = "zip -q -r {} {}".format(output_file, input_file)
        else:
            assert False
        self.execute(cmd, cwd=cwd)

    def append_path(self, path):
        cmd = "export PATH={}:$PATH".format(path)
        if self.fake:
            print(cmd)
        else:
            os.environ["PATH"] = "{}:{}".format(path, os.environ["PATH"])
            logging.info(cmd)

    @staticmethod
    def gen_short_dir(cwd):
        n = 0
        while os.path.exists(os.path.join(cwd, str(n))):
            n += 1
        return str(n)

