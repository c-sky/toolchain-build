#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import argparse
import os
import sys
import re


class Filter:
    def __init__(self):
        pass


def read_sum(files_dir):
    ret = []
    for root, dirs, files in os.walk(files_dir):
        for f in files:
            if f.endswith(".sum"):
                with open(os.path.join(root, f), "r") as fp:
                    for line in fp.readlines():
                        if line.startswith("FAIL") or line.startswith("XPASS") or line.startswith("ERROR"):
                            ret.append(line.strip())
    return ret


def create_whitelist(args):
    whitelist = read_sum(args.sumfiles_dir)
    with open(args.output, "w") as fp:
        fp.write("\n".join(whitelist))


def read_white_lists(white_list_files, is_gcc):
    if is_gcc:
        white_lists = dict()
    else:
        white_lists = set()
    for file_name in white_list_files:
        with open(file_name) as fp:
            content = fp.readlines()
            for line in content:
                line = line.strip()
                if len(line) == 0:
                    continue
                if line[0] == '#':
                    continue

                if is_gcc:
                    try:
                        key = line.split(' ')[1]
                    except IndexError:
                        print("Corrupt allowlist file?")
                        print("Each line must contail <STATUS>: .*")
                        print("e.g. FAIL: g++.dg/pr83239.C")
                        print("Or starts with # for comment")
                    if key not in white_lists:
                        white_lists[key] = []
                    white_lists[key].append(line)
                else:
                    white_lists.add(line)

    return white_lists


def analysis_cpu(cpu):
    match_obj = re.match(r"(\D+\d+)(.*)", cpu)
    cpu_base = match_obj.group(1)
    cpu_suffix = match_obj.group(2)
    return cpu_base, cpu_suffix


def filter_result(sumfiles_dir, tool, libc, cpu, whitelist_dir):
    whitelist_files = []
    unexpected_result_list = []
    is_gcc = tool == 'gcc'
    any_fail = False
    inner_dir = os.path.join(whitelist_dir, tool)

    def append_if_exist(filename):
        filepath = os.path.join(inner_dir, filename)
        if os.path.exists(filepath):
            whitelist_files.append(filepath)

    append_if_exist("common.log")
    append_if_exist(libc + ".log")
    if cpu:
        append_if_exist(cpu + ".log")
        cpu_base, cpu_suffix = analysis_cpu(cpu)
        for root, dirs, files in os.walk(inner_dir):
            for f in files:
                if f.startswith(cpu_base) and f.endswith(".log"):
                    base, suffix = analysis_cpu(f[:-4])
                    for flag in suffix:
                        if flag not in cpu_suffix:
                            break
                    else:
                        whitelist_files.append(os.path.join(root, f))
    whitelist = read_white_lists(whitelist_files, is_gcc)
    unexpected_results = read_sum(sumfiles_dir)

    if is_gcc:
        case_count = set()
        for ur in unexpected_results:
            key = ur.split(' ')[1]
            if key in whitelist and \
                    any(map(lambda x: ur.startswith(x),
                            whitelist[key])):
                # This item can be ignored
                continue
            else:
                unexpected_result_list.append(ur)
                case_count.add(key)
                any_fail = True
    else:
        for ur in unexpected_results:
            if ur not in whitelist:
                unexpected_result_list.append(ur)
                any_fail = True

    if len(unexpected_result_list) != 0:
        print("\t\t=== Unexpected fails ===")
        for ur in unexpected_result_list:
            print(ur)

    return not any_fail


def filter_result_ret(args):
    if filter_result(args.sumfiles_dir, args.tool, args.libc, args.cpu, args.whitelist_dir):
        sys.exit(0)
    else:
        sys.exit(1)


def option_init():
    parser = argparse.ArgumentParser(description="Testcase result filter")
    parent = argparse.ArgumentParser(add_help=False)
    parent.add_argument('--sumfiles-dir', help="The directory of test sum files", required=True)
    subparsers = parser.add_subparsers(title="Sub command", dest="subparser_name")
    subparsers.required = True
    create = subparsers.add_parser('create', help="Create a whitelist.", parents=[parent])
    create.add_argument('--output', help="The output file path", required=True)
    create.set_defaults(func=create_whitelist)
    filter_parser = subparsers.add_parser('filter', help="Do filter", parents=[parent])
    filter_parser.add_argument('--tool', help="The component name", default="gcc", choices=["gcc", "binutils"])
    filter_parser.add_argument('--libc', help="The libc name", default="glibc", choices=["glibc", "newlib"])
    filter_parser.add_argument('--cpu', help="The cpu name", default="")
    filter_parser.add_argument('--whitelist-dir', help="The directory of whitelist files", required=True)
    filter_parser.set_defaults(func=filter_result_ret)
    args = parser.parse_args()
    args.func(args)
    return args


if __name__ == "__main__":
    option_init()
