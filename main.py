#!/usr/bin/python
#coding:utf-8

import sys
from Hello import OS

_file_ = OS.realpath(__file__)
_dir_  = OS.dirname(_file_)
_conf_ = OS.join(_dir_, "config.ini")
_bin_  = OS.islink(__file__) and OS.dirname(__file__) or "/usr/local/bin"
_help_ = """
$[Hello Shell] 个人脚本管理
--------------------------------------------------------------
  usage   : helloshell $[<command>] [args]
  commands:
    $[new]                      新建脚本
    $[repo]                     配置仓库
    $[backup]                   备份仓库
    $[link]                     安装仓库中的脚本到系统环境变量中
    $[args] <file> [arguments]  解析参数为 shell 语法格式
    $[conf] <file> [options]    读写配置文件
    $[alias] [name [= value]]   别名管理
    $[echo]                     格式化输出，支持接收由管道传入参数
""".strip()

if __name__ == '__main__':
    cmd  = len(sys.argv) > 1 and sys.argv[1] or ""
    argv = len(sys.argv) > 2 and sys.argv[2:] or []
    if cmd == "repo":
        from Module import Repo
        Repo.run(argv)

    elif cmd == "backup":
        from Module import Repo
        Repo.run(["--backup"])

    elif cmd == "new":
        from Module import Tmp 
        Tmp.run(argv)

    elif cmd == "link":
        from Module import Link 
        Link.run(argv)

    elif cmd == "alias":
        from Module import Alias 
        Alias.run(argv)
        
    elif cmd == "args":
        from Module import Args
        Args.run(argv)
    
    elif cmd == "conf":
        from Module import Conf
        Conf.run(argv)

    elif cmd == "echo":
        from Module import Echo
        Echo.run(argv)

    else:
        from Hello import Echo
        if not sys.stdin.isatty():
            Echo.stdout( sys.stdin.read() )
        else:
            Echo.echo( _help_ )
            exit(1)