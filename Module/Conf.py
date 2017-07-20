#!/usr/bin/python
#coding:utf-8

import re
from Args import Args
from Echo import Echo
from Hello import OS
from Hello import Conf


__def_conf = None

def repo_dir():
	import __main__
	conf = default()
	path = conf.value("repo")
	if not path:
		conf.value("repo", OS.join(__main__._dir_, "repo"))
	elif not OS.isabspath(path):
		conf.value("repo", OS.join(__main__._dir_, path))
	return conf.value("repo")

def default():
	global __def_conf
	if __def_conf:
		return __def_conf
	import __main__
	__def_conf = Conf.read(__main__._conf_, True)
	return __def_conf

def run(argv):
	import __main__

	args = Args.parse({
		"desc": " Hello Shell 配置模块",
		"options": [
			["file",    None,       "<file>",               "配置文件路径"],
			["options", None,       "=[] [name [= value]]", "查看或设置变量"],
			["-p",      "--prefix", "string",               "设置输出时变量名的前缀"]
		]
	}, argv, True, True)

	if not args.get("file"):
		Echo.echo(" ![缺少 path 参数, 例]: helloshell conf config.ini\n")
		Echo.echo(args.help())
		exit(1)

	conf_file = OS.filename(OS.realpath(args.get("file"))) + ".ini"
	pref      = args.get("prefix") + "_" if args.get("prefix") else ""

	

	if args.get("options"):
		option = []
		for arg in args.get("options"):
			ref = arg.split("=")
			if len(ref) == 1 or not ref[1]:
				option.append(arg)
			else:
				option.append(ref[0])
				option.append("=")
				option.append("=".join(ref[1:]))
		count  = len(option)
		need_create = False
		for arg in option:
			if arg == "=":
				need_create = True
				break
		conf   = Conf.read(conf_file, need_create)
		i = 0
		while i < count:
			name = option[i]
			if not name:
				continue
			if i+1 < count and option[i+1] == "=":
				i += 1
				if i+1 < count:
					i += 1
					conf.value(name, option[i])
				else:
					conf.value(name, None)
			i += 1
			value = conf.value(name)
			if value != None:
				if value == "true" or value == "false":
					print(pref + name + "=" + value +";")
				else:
					print(pref + name + "=\"" + value +"\";")

	else:
		conf = Conf.read(conf_file)
		if conf:
			for (k, v) in conf.options().items():
				if v == "true" or v == "false":
					print(pref + k + "=" + v +";")
				else:
					print(pref + k + "=\"" + v +"\";")