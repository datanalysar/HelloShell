#!/usr/bin/python
#coding:utf-8

import os
import File, Repo
from Echo import Echo
from Args import Args
from Hello import Yaml

_log      = None
_log_file = File.join(Repo._dir, ".helloshel")

def log():
	global _log
	if not _log:
		_log = Yaml.parse_file(_log_file)
		if _log:
			for i in range(len(_log)-1, -1, -1):
				if not File.exists(_log[i]["file"]):
					del _log[i]
		else:
			_log = []
	return _log

def save(typ, file, link):
	conf = log()
	for i in range(len(conf)-1, -1, -1):
		if conf[i].get("link") == link:
			del conf[i]
	conf.append({"type": typ, "file": file, "link": link})
	File.write(_log_file, Yaml.stringify(conf))

def exist(alias, target = None):
	if type(alias) is dict:
		target = alias.get("file")
		alias  = alias.get("link")
	if alias and target and File.islink(alias) and File.exists(target):
		return File.realpath(alias) == target
	return False

def search_link(target):
	res = []
	for item in log():
		if item["type"] != "link":
			continue
		if exist(item) and (target == item["file"] or File.issubpath(target, item["file"])):
			res.append(item)
	return res

def find_link(target):
	res = []
	for item in log():
		if item["type"] != "link":
			continue
		if target == item["file"] and exist(item):
			res.append(item)
	return res

def to_bin(file, alias):
	import __main__
	if not File.isfile(file):
		Echo.echo('![无法找到文件] "@['+file+']"')
		exit(1)

	if not alias:
		alias = File.filename(File.basename(file))

	if alias:
		to = File.join(__main__._bin_, alias)
		
		# if type(file) == unicode:
		# 	file = file.encode("utf-8")
		# if type(to) == unicode:
		# 	to = to.encode("utf-8")

		if File.exists(to):
			if Echo.input('"@['+to+']" 以存在，是否替换 (y/n): ').lower() != "y":
				exit(0)
			File.remove(to)
		save("link", file, to)
		os.symlink( file, to )		
		Echo.echo("成功链接到 bin 目录: $["+ file + "] -> @[" + to + "]")
		return to

def ls_bin():
	import __main__
	bin_dir = __main__._bin_
	res     = {}
	for sub in File.ls(bin_dir):
		if File.islink(sub):
			res[os.readlink(sub)] = sub
	return res


def choice():
	res     = []
	bin_map = ls_bin()
	for name in File.ls_name(Repo._dir, level=1):
		file = File.join(Repo._dir, name)
		if File.isfile(file):
			links = find_link(file)
			if links or bin_map.get(file):
				pass
				# res.append( [file, name, links[0]] )
			else:
				res.append( [file, name] )

	for i in range(0, len(res)):
		text = "  [$["+str(i)+"]]  @[" + res[i][1] + "]"
		# text += " -> #["+res[i][1]+"]"
		Echo.echo(text)

	sel = Echo.input( "$[请选择脚本编号]: ")
	if sel and sel.isdigit():
		i = int(sel)
		if i >= 0 and i < len(res):
			alias = Echo.input( "$[请输入别名, 默认为] @["+ File.filename(res[i][0], True) +"]: ")
			to_bin(res[i][0], alias)
	else:
		Echo.echo("![x...x]")


def run(argv):
	args = Args.parse({
		"desc": " 安装仓库中的脚本到系统环境变量中\n usage: helloshel link <script> [linkname]",
		"options": [
			["-l", "--list",   None,           "查看仓库内脚本"]
		]
	}, argv, True, True)

	if args.get("list"):
		Repo.list_repo()
		exit(0)

	if args.get("-"):
		ref = args.get("-")
		script = Repo.find_main(ref[0], select=True)
		if script:
			to_bin(script, len(ref) > 1 and ref[1])
			exit(0)
		else:
			Echo.echo("![没有找到脚本]: @["+ref[0]+"]")
			exit(1)

	choice()
	exit(0)