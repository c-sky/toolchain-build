#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import re


class Version(object):
    def __init__(self, ver, n):
        self.__layer = n
        if type(ver) == int:
            self.__ver = ver
        elif type(ver) == str:
            self.__ver = self.convert_version_to_int(ver, n)

    def __str__(self):
        return self.convert_version_to_str(self.__ver, self.__layer)

    def __eq__(self, other):
        return self.number == other.number

    def __lt__(self, other):
        return self.number < other.number

    @property
    def number(self):
        return self.__ver

    @property
    def layer(self):
        return self.__layer

    @staticmethod
    def convert_version_to_int(version, n=3):
        pattern = ".".join([r"(\d+)"] * n)
        match_obj = re.match(pattern, version)
        assert match_obj is not None
        vn = 0
        for i in range(n):
            vn += (int(match_obj.group(i + 1)) << (8 * (n - i - 1)))
        return vn

    @staticmethod
    def convert_version_to_str(version, n=3):
        assert n > 0
        vn = []
        for i in reversed(range(n)):
            cn = version >> (8 * i)
            version -= cn << (8 * i)
            vn.append(str(cn))
        return ".".join(vn)