#!/usr/bin/env python3

#
# Copyright 2015 riteme
#

import sys
import os
from stat import *
from proj_conf import *


COLOR_NONE = '\033[0m'
COLOR_BLACK = '\033[30m'
COLOR_RED = '\033[31m'
COLOR_GREEN = '\033[32m'
COLOR_YELLOW = '\033[33m'
COLOR_BLUE = '\033[34m'
COLOR_PURPLE = '\033[35m'
COLOR_DARK_GREEN = '\033[36m'
COLOR_WHITE = '\033[37m'


def log_info(message):
    print(
        COLOR_GREEN + '(info)' + COLOR_NONE + ' ' + message
    )


def log_warning(message):
    print(
        COLOR_YELLOW + '(warn)' + COLOR_NONE + ' ' + message
    )


def log_error(message):
    print(
        COLOR_RED + '(error)' + COLOR_NONE + ' ' + message
    )


def log_fatal(message):
    print(
        COLOR_PURPLE + '(fatal)' + COLOR_NONE + ' ' + message
    )


def log_debug(message):
    if not DEBUG_OUTPUT:
        return

    print(
        COLOR_DARK_GREEN + '(debug)' + COLOR_NONE + ' ' + message
    )


def ParseParameters():
    """解析传入的参数
    会修改设置
    """

    for param in range(1, len(sys.argv)):
        if sys.argv[param] == '-debug':  # 调试模式
            DEBUG_MODE = True
        elif '-O' in sys.argv[param]:  # 设置优化
            OPTIMIZE_LEVEL = sys.argv[param][2:]
        # 使用clang
        elif sys.argv[param] == '-clang' or sys.argv[param] == '-clang++':
            COMPILER = 'clang++'
        elif sys.argv[param] == '-gcc' or sys.argv[param] == '-g++':  # 使用GCC
            COMPILER = 'g++'
        elif sys.argv[param] == '--help' or sys.argv[param] == '-h':  # 显示帮助
            print(
                """Usage:
                build.py [-debug] [-O0, 1, 2, 2.5, 3] [-clang] [-gcc] [-h]
                """
            )
            exit()
        else:
            log_error('Unknown parameter: {}'.format(sys.argv[param]))
            exit()


if __name__ != '__main__':
    # 警告使用者不应将此当做模块使用
    raise RuntimeWarning("It's not a module to load!")
else:
    # 执行准备脚本
    if PREPARE_SHELL != '':
        log_info('Performing preparation shell...')
        result = os.system('sh ' + PREPARE_SHELL)
        if result != 0:
            log_error(
                'Preparation shell failed with return code {}'.format(
                    result
                )
            )
            exit()

    # 如果有参数则进行解析
    if len(sys.argv) > 1:
        ParseParameters()

    command = ''

    # 展示版本号
    log_info('Program version: V{}'.format(VERSION))

    # 检查release目录是否存在
    try:
        st = os.stat('./release/').st_mode 
    except FileNotFoundError:
        log_warning('No release folder found. Make a new one.')
        os.mkdir('./release/')

    # 确定编译器
    log_info('Compiler: {}'.format(COMPILER))
    command += COMPILER + ' '

    # 为g++转换-Weverything
    if 'g' in COMPILER:
        new_list = []
        for item in COMPILER_WARNINGS:
            if item != 'everything':
                new_list.append(item)
            else:
                new_list.append('all')
                new_list.append('extra')
        COMPILER_WARNINGS = new_list

    # 确定C++版本
    log_info('C++ version: {}'.format(CXX_VERSION))
    command += '-std=' + CXX_VERSION + ' '

    # 确定STL库（libstdc++或libc++）
    if 'clang' in COMPILER:
        log_info('STL library: {}'.format(CXX_STDLIB))
        command += '-stdlib=' + CXX_STDLIB + ' '
    elif 'gcc' in COMPILER or 'g++' in COMPILER:
        log_warning("STL library setting ignored")

    # 加入源码路径
    for source in SOURCES:
        log_info('Add source: {}'.format(source))
        command += source + ' '

    # 添加警告参数
    log_info('Add warning parameters...')
    for warning in COMPILER_WARNINGS:
        command += '-W' + warning + ' '
    for ignoredWarning in COMPILER_IGNORE_WARNINGS:
        command += '-Wno-' + ignoredWarning + ' '

    # 添加链接库参数
    log_info('Add link parameters...')
    for library in COMPILER_LIBRARYS:
        command += '-l' + library + ' '
    for libraryDirectory in COMPILER_LIBRARYS_DIRECTORY:
        command += '-L' + libraryDirectory + ' '

    # 添加头文件参数
    log_info('Add include parameters...')
    for include in COMPILER_INCLUDES_DIRECTORY:
        command += '-I' + include + ' '
    for systemInclude in COMPILER_SYSTEM_INCLUDES_DIRECTORY:
        command += '-isystem' + ' ' + systemInclude + ' '

    # 添加文件输出参数
    log_info('Add other parameters...')
    output = OUTPUT_LOCATION
    if OUTPUT_WITH_VERSION:
        if OUTPUT_MODE == 'shared':
            # libXXX.so.version
            output += '.' + VERSION
        elif OUTPUT_MODE == 'executable':
            indexDot = os.path.basename(output).rfind('.')
            if indexDot == -1:
                # filename.version
                output += '.' + VERSION
            else:
                # filename.version.extension
                output = '{}.{}.{}'.format(
                    output[:len(os.path.dirname(output)) + indexDot + 1],
                    VERSION,
                    output[len(os.path.dirname(output)) + indexDot + 2:]
                )

    command += '-o ' + output + ' '

    # 添加动态库参数
    if OUTPUT_MODE == 'shared':
        command += '-fPIC -shared '

    # 调试和优化参数
    if DEBUG_MODE:
        command += '-g '
    else:  # 如果是调试模式则不开启优化，因为优化可能会打乱代码顺序
        command += {
            '0': '-O0',
            '1': '-O1',
            '2': '-O2',
            '2.5': '-Os',
            '3': '-O3'
        }.get(OPTIMIZE_LEVEL, '-O0')  # 默认为无优化

    command += ' '

    # 加入其余的参数
    command += ' '.join(COMPILER_OTHER_PARAMETERS)

    # 打印最终结果
    log_debug('Final shell: {}'.format(command))

    terminal_width, terminal_height = os.get_terminal_size()

    # 执行命令，开始编译
    log_info('Going to compile...')
    print(('{:=^' + str(terminal_width) + '}').format('BEGIN'))

    result = os.system(command)

    print(('{:=^' + str(terminal_width) + '}').format('END'))

    # 报告错误
    if result != 0:
        log_error('Compilion failed with return code {}'.format(result))

    # 链接程序到latest
    if OUTPUT_LINK_TO_LATEST and result == 0:

        # 如果已存在，则先删除，防止发生错误
        if os.path.exists(OUTPUT_LOCATION):
            os.remove(OUTPUT_LOCATION)

        result = os.system(
            'ln {} {}'.format(
                output,
                OUTPUT_LOCATION
            )
        )

        # 检查返回值
        if result != 0:
            log_error(
                'Output link failed with return code {}'.format(
                    result
                )
            )
            exit()

    # 执行清理脚本
    if CLEANUP_SHELL != '':
        log_info('Performing clean-up shell...')
        result = os.system('sh ' + CLEANUP_SHELL)
        if result != 0:
            log_error(
                'Clean-up shell failed with return code {}'.format(
                    result
                )
            )
            exit()

    # 报告结束
    log_info('Compilion end')
