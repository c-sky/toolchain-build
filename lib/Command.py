#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import subprocess
import os
import errno
import shutil


class FindException(BaseException):
    def __init__(self, arg):
        self.args = arg

    def __str__(self):
        return "".join(self.args)


def execute_cmd(cmd, cwd=None, stdout=None):
    p = subprocess.Popen(cmd, shell=True, cwd=cwd, stdout=stdout, universal_newlines=True)
    (output, error_message) = p.communicate()
    if p.returncode:
        raise ValueError("Command execute failed.\n"
                         "The command is: {}".format(cmd))
    return output


def find(search_dir, filename):
    for relpath, dirs, files in os.walk(search_dir):
        if filename in files:
            file_path = os.path.join(search_dir, relpath, filename)
            break
    else:
        raise FindException("Can't find '{}' in '{}'.".format(filename, search_dir))
    return file_path


# Difference with the origin os.mkdir:
#   1. If the directory is existed, don't raise exception
#   2. If create parent directory if it's not exist
def extend_mkdir(directory, parent=True, clean=False):
    if os.path.exists(directory):
        if clean:
            shutil.rmtree(directory)
        else:
            return
    if parent:
        try:
            os.makedirs(directory)
        except OSError as exc:
            if exc.errno == errno.EEXIST and os.path.isdir(directory):
                pass
            else:
                raise exc
    else:
        os.mkdir(directory)


def abs_path(cwd, org_path):
    ret = org_path
    if org_path and not os.path.isabs(org_path):
        ret = os.path.join(cwd, org_path)
    return ret
