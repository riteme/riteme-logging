#!/usr/bin/env python3
import os
import sys
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


def decide_compiler(config):
    """确定使用的编译器
    如果设置中使用的是clang，则使用设置中的编译器
    否则使用默认的clang++
    """

    if 'clang'in config:
        return config
    else:
        return 'clang++'


def gen_source_parameters(sources):
    """生成原代码文件参数
    因为SOURCES是定义为一个list
    """

    # 每个源文件用空格隔开
    return ' '.join(sources)


def gen_include_parameters(includes, systenIncludes):
    """生成头文件目录参数
    包含普通头文件目录和系统级头文件目录
    """

    include_parameters = ''

    include_parameters += ' '.join(map('-I{}'.format, includes))
    # for e in includes:
    #     include_parameters += '-I' + e

    # 在中间加入一个空格隔开
    include_parameters += ' '

    include_parameters += ' '.join(map('-isystem {}'.format, systenIncludes))
    # for e in systenIncludes:
    #     include_parameters += '-isystem' + ' ' + e

    return include_parameters


def gen_clang_warning_parameters(warnings,ignored_warnings):
    warning_parameter = ''

    for warning in warnings:
        warning_parameter += '-W' + warning + ' '
    for ignoredWarning in ignored_warnings:
        warning_parameter += '-Wno-' + ignoredWarning + ' '

    return warning_parameter


def gen_cppcheck_stds(stds):
    """生成cppcheck的std参数
    格式：--std=std1 --std=std2 ...
    """

    # std_parameters = ''

    # for e in stds:
    #     std_parameters += '--std={} '.format(e)

    # return std_parameters
    return ' '.join(map('--std={}'.format, stds))


def gen_cppcheck_enables(enables):
    """生成cppcheck的enable参数
    格式：enable1, enable2, ...
    """

    # 每个enable参数用逗号隔开
    return '--enable={}'.format(','.join(enables))


def clang_syntax_check():
    """使用clang -fsyntax-only进行语法检查
    该函数自己会有文字输出
    """

    terminal_width, terminal_height = os.get_terminal_size()

    if not CHECK_USE_CLANG_SYNTAX:
        log_info('Clang syntax ignored')
        return 0

    # 编译器，源文件，C++标准，头文件目录
    command = '{} -fsyntax-only {} -stdlib=libc++ -std={} {} {}'
    compiler = decide_compiler(COMPILER)
    sources = gen_source_parameters(SOURCES)
    includes = gen_include_parameters(
        COMPILER_INCLUDES_DIRECTORY,
        COMPILER_SYSTEM_INCLUDES_DIRECTORY
    )
    warnings = gen_clang_warning_parameters(
        CHECK_WARNINGS,
        CHECK_IGNORE_WARNINGS
    )

    print(('{:=^' + str(terminal_width) + '}').format('BEGIN clang syntax check'))

    result = os.system(command.format(
        compiler,
        sources,
        CXX_VERSION,
        includes,
        warnings
    ))

    print(('{:=^' + str(terminal_width) + '}').format('END clang syntax check'))

    log_info('Command clang -fsyntax-only returned {}'.format(result))

    # 添加一个额外的行来分隔各部分的输出
    print('')

    return result


def clang_static_analyze():
    """使用clang --analyze进行静态检查
    该函数会有文字输出
    """

    terminal_width, terminal_height = os.get_terminal_size()

    if not CHECK_USE_CLANG_ANALYZE:
        log_info('Clang static analyze ignored')
        return 0

    # 编译器，源文件，C++标准，头文件目录
    command = '{} --analyze {} -stdlib=libc++ -std={} {}'
    compiler = decide_compiler(COMPILER)
    sources = gen_source_parameters(SOURCES)
    includes = gen_include_parameters(
        COMPILER_INCLUDES_DIRECTORY,
        COMPILER_SYSTEM_INCLUDES_DIRECTORY
    )

    print(('{:=^' + str(terminal_width) + '}').format('BEGIN clang static analyze'))

    result = os.system(command.format(
        compiler,
        sources,
        CXX_VERSION,
        includes
    ))

    print(('{:=^' + str(terminal_width) + '}').format('END clang static analyze'))

    log_info('Command clang --analyze returned {}'.format(result))

    # 添加一个额外的行来分隔各部分的输出
    print('')

    return result


def cppcheck_static_check():
    """使用cppcheck进行静态检查
    该函数会有文字输出
    """

    terminal_width, terminal_height = os.get_terminal_size()

    if not CHECK_USE_CPPCHECK:
        log_info('Cppcheck static check ignored')
        return 0

    # C++标准，检查项（enable），源文件，头文件目录
    command = 'cppcheck {} {} {} {}'
    stds = gen_cppcheck_stds(CPPCHECK_STD)
    enables = gen_cppcheck_enables(CPPCHECK_ENABLE)
    sources = gen_source_parameters(SOURCES)
    includes = gen_include_parameters(
        COMPILER_INCLUDES_DIRECTORY,
        COMPILER_SYSTEM_INCLUDES_DIRECTORY
    )

    print(('{:=^' + str(terminal_width) + '}').format('BEGIN cppcheck static check'))

    result = os.system(command.format(
        stds,
        enables,
        sources,
        includes
    ))

    print(('{:=^' + str(terminal_width) + '}').format('END cppcehck static check'))

    log_info('Command cppcheck returned {}'.format(result))

    # 添加一个额外的行来分隔各部分的输出
    print('')

    return result


def main(argc, argv):
    """主函数
    如果语法检查未通过，则不进行静态检查
    避免不必要的麻烦
    """

    log_info('Start checking...')

    if clang_syntax_check() == 0:
        clang_static_analyze()
        cppcheck_static_check()
    else:
        log_error('Clang syntax check failed')

    log_info('Exited')


if __name__ == '__main__':
    main(len(sys.argv), sys.argv)
