#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import argparse
import logging
import sys
from CskyGCCToolchain import CskyGccToolchain


def process(args):
    subparser_name = args.subparser_name
    toolchain = None
    if subparser_name == "csky-gcc":
        toolchain = CskyGccToolchain(args.triple, args.src, args.jobs, args.version, args.release_dir,
                                     args.rebuild, False, args.build_type,
                                     args.extra_config, args.type, args.host, args.dep_libs,
                                     args.cpu, args.endian, args.fpu,
                                     args.multilib, False, "", None,
                                     "", args.fake, args.disable_gdb)
        toolchain.run()


def option_init():
    parser = argparse.ArgumentParser(description="Toolchain build and test.")
    parent_parser = argparse.ArgumentParser(add_help=False)
    parent_parser.add_argument('--triple', help="The target triple", choices=["csky-unknown-elf",
                                                                              "csky-unknown-linux-gnu"],
                               required=True)
    parent_parser.add_argument('--host', help="The host type for cross build compiler", default="x86_64",
                               choices=["x86_64", "i386", "mingw", "Win32", "Win64"])
    parent_parser.add_argument('--src', help="The directory of source code",
                               required=True)
    parent_parser.add_argument('--jobs', help="Allow N jobs at once, -1 means -j", default=16, type=int)
    parent_parser.add_argument('--version', help="The version number of LLVM toolchain")
    parent_parser.add_argument('--release-dir', help="The directory holds release tar")
    parent_parser.add_argument('--rebuild', help="Rebuild the project", action="store_true")
    parent_parser.add_argument('--no-rebuild', help="Don't rebuild the project", dest="rebuild", action="store_false")
    parent_parser.set_defaults(rebuild=False)
    parent_parser.add_argument('--extra-config', help="Extra configuration arguments", default="", nargs="+")
    parent_parser.add_argument('--build-type', help="The build type of compiler", default="Release",
                               choices=["Release", "Debug", "RelWithDebInfo", "MinSizeRel"])
    parent_parser.add_argument('--fake', help="Print the command with executing", action="store_true")
    subparsers = parser.add_subparsers(title="Sub command", dest="subparser_name")
    subparsers.required = True
    gcc = argparse.ArgumentParser(add_help=False)
    gcc.add_argument('--dep-libs', help="The depend library path")
    gcc.add_argument('--multilib', help="Build multilib toolchain", action="store_true")
    gcc.add_argument('--no-multilib', help="Build single lib toolchain", dest="multilib", action="store_false")
    gcc.set_defaults(multilib=True)
    gcc.add_argument('--linux-headers', help="The linux headers tar file")
    gcc.add_argument('--type', help="The action of script", nargs="+", default=[],
                     choices=["release", "check-gcc", "check-binutils", "check-gdb", "doc"])
    csky_gcc = subparsers.add_parser('csky-gcc', help="CSKY GCC project build and test.",
                                     parents=[parent_parser, gcc])
    csky_gcc.add_argument('--cpu', help="The default cpu when build multilib, "
                                        "the single arch when build non-multilib", default="ck810f")
    csky_gcc.add_argument('--fpu', help="The default float abi when build multilib, "
                                        "the single float abi when build non-multilib",
                          choices=["soft", "softfp", "hard"], default="soft")
    csky_gcc.add_argument('--endian', help="The default endian when build multilib, "
                                           "the single endian when build non-multilib",
                          choices=["little", "big"], default="little")
    csky_gcc.add_argument('--disable-gdb', help="Don't build the gdb.", action="store_true")
    parser.set_defaults(func=process)
    logging.info(" ".join(sys.argv))
    args = parser.parse_args()
    args.func(args)
    return args


def main():
    logging.basicConfig(filename="build.log", format="%(asctime)s:%(levelname)s:%(message)s", level=logging.INFO)
    option_init()


if __name__ == "__main__":
    main()
