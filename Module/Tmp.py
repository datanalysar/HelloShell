#!/usr/bin/python
#coding:utf-8

import Link, Conf
from Echo import Echo
from Args import Args
from Hello import OS

bash_tmp = """
#!/bin/sh

# HELP DOCUMENT
#
# 参数:
#   -c, --config =[]    测试添加配置文件    
#	-s, --say string	测试输出
#	-h, --help			查看帮助
#

# 读取参数
eval "$(helloshell args $0 $*)"
if [ $? != 0 ]; then
	echo "Argument Error:"
	echo $argv_errors
	exit 1
fi
if [ $argv_help ]; then
	echo "${help_document}"
	exit 1
fi

# 设置配置]
eval "$(helloshell conf $0 -p config)"
if [ $argv_config ]; then
	eval "$(helloshell conf $0 ${argv_config[*]} -p config)"
	echo "Config: $(helloshell conf $0 -p config)"
	exit
fi

# 有色彩的输出
if [ $argv_say ]; then
	echo "#g[Say]: ${argv_say}" | helloshell
else
	echo "#c[Hello] #r[world]" | helloshell
fi

""".lstrip()

python_tmp = """
#!/usr/bin/python
#coding:utf-8

import sys
sys.path.append("#_dir_#")
import Hello.Args
import Hello.Conf
import Hello.Echo
import Hello.OS

# HELP DOCUMENT
#
# 参数:
#	-t, --text string	示例
#	-h, --help			查看帮助
#

if __name__ == '__main__':

	# 示例:

	args = Hello.Args.parse(__file__, sys.argv[1:], True, True)
	print(args.options)

	conf = Hello.Conf.read(create=True)
	print( conf.filename )
	print( conf.value("test", "abc") )
	print( conf.value("test") )

	print(" - "*20)
	if args.get("text"):
		Hello.Echo.echo(args.get("text"))
	else:
		Hello.Echo.echo("#b[Hello] #g[world]!!")

""".lstrip()

def run(argv):
	args = Args.parse({
		"desc": " Hello Shell 创建脚本",
		"options": [
			["name", None, None, "脚本名称"],
			["-l", "--link", "alias name", "将新生成的脚本链接到 bin 目录中。\n默认使用文件名"]
		]
	}, argv, True, True)
	
	repo_path = Conf.repo_dir()
	basename  = args.get("name")

	if basename:
		import __main__
		file_name = OS.filename(basename)
		ext_name  = OS.extname(basename)
		path      = OS.join(repo_path, file_name, basename)

		if OS.isfile(path):
			if Echo.input('⚠️ "@['+path+']" 以存在，是否覆盖 (y/n): ').lower() != "y":
				exit(0)
		elif Echo.input('创建 "@['+path+']" (y/n): ').lower() != "y":
			exit(0)

		if not ext_name or ext_name == ".sh" or ext_name == ".bash":
			OS.write(path, bash_tmp, 0o777)

		elif ext_name == ".py":
			OS.write(path, python_tmp.replace("#_dir_#", __main__._dir_), 0o777)
		
		else:
			OS.write(path, "", 0o777)

		alias = args.get("link")
		if alias != None:
			Link.to_bin( path, alias )