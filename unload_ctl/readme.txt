# -*- coding: utf-8 -*-
oracle 控制文件 解析工具
控制文件默认路径： 控制文件的存储位置在参数文件中有指定.
win: $oracle_base\oradata\sid\control01.ctl    linux: $ORACLE_BASE/oradata/sid/control01.ctl
11g/12c 中 在闪回区 有一个control02.ctl, $ORACLE_BASE\fast_recovery_area\orcl\control02.ctl

结构不完全清楚


=============================================================================
history:
V1.0.0      2016-01-18
解析控制文件中的信息
V1.1.0      2016-01-31
完善功能，修复bugs



