#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  oracle 控制文件的解析, 算法不够
import os.path
import struct

s = struct.unpack


def ctl_unload(f_name):
    f = open(f_name, 'rb')
