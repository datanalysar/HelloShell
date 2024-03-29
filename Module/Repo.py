#!/usr/bin/python
#coding:utf-8

import os, re, sys, commands, time
import Git, Conf
from Echo import Echo
from Hello import OS
 
_dir = Conf.repo_dir()

def find_main(path, scan=True, select=False):
	if OS.islink(path):
		path = OS.realpath(path)
	
	if OS.isfile(path):
		return path
	if OS.isdir(path):
		name = OS.filename(path, True)
		for sub in OS.ls(path, _abs=False):
			subname = OS.filename(sub)
			if subname == name or subname == "main" or subname == "index":
				return sub

	for sub in OS.ls(_dir):
		if path == OS.basename(sub):
			ref = find_main(sub, scan = False)
			if ref:
				return ref
			if select:
				return Echo.select(OS.ls(sub), "请选择: ")

def set_repo(target):
	new_dir  = OS.abspath(target)
	if not OS.isdir(new_dir):
		if Echo.input('目录 "@['+new_dir+']" 不存在，是否创建 (y/n) %s: ').lower() != 'y':
			exit(0)
		os.makedirs(new_dir)

	if _dir != new_dir and OS.isdir(_dir):
		if Echo.input('⚠️ 是否迁移旧仓库 "@['+_dir+']" 到新目录 (y/n): ').lower() == 'y':
			os.system("mv -f " + _dir + "/* " + new_dir)
	Conf.default().value("repo", new_dir)
	list_repo()

def remote_repo(target):
	git   = Git.new(_dir)
	exist = git.exist()
	if not exist:
		git.echo().init()

	(status, output) = git.echo().remote(target, 'hello_shell')
	
	if status == 32768:
		(status, output) = git.remote(name = 'hello_shell')
		Echo.echo( '⚠️  远端仓库 (@[hello_shell]) 以存在:' )
		Echo.echo( '    '+output)
		if Echo.input('![是否替换 @[hello_shell]] (y/n): ').lower() != 'y':
			exit(0)
		git.echo().cmd('git remote remove hello_shell')
		(status, output) = git.echo().remote(target, 'hello_shell')

	if status == 99999:
		Echo.echo( '⚠️  不正确的 github 地址 "!['+target+']", 例：#[user_name/repo_name]' )
		exit(1)

	git.echo().remote()
	if status == 0:
		if not exist or Echo.input('![是否现在更新本地仓库] (y/n): ').lower() == 'y':
			git.echo().pull('hello_shell')

def get_status(file, _status = None):
	_status = _status or Git.new(_dir).status()[2]
	for item in _status:
		if file == item["file"] or OS.issubpath(file, item["file"]):
			return item["state"]

def ls_repo():
	import Link
	git        = Git.new(_dir)
	git_status = git.status()[2] or []
	bin_map    = Link.ls_bin()
	res = []
	for sub in OS.ls(_dir):
		state = get_status(sub, git_status) or ""
		if OS.isdir(sub):
			ref = Link.search_link(sub)
			if ref:
				for item in ref:
					res.append( {"state": get_status(item["file"], git_status) or state, "file": item["file"], "link": item["link"]} )
				continue
			else:
				main = find_main(sub)
				if main:
					sub  = OS.join(sub, main)
					state = get_status(sub, git_status) or state
		res.append( {"state": state, "file": sub, "link": bin_map.get(sub)} )
	return res

def list_repo():
	git         = Git.new(_dir)
	(s, remote) = git.remote( name = 'hello_shell')
	Echo.echo( 'Local  : @['+_dir+']' )
	Echo.echo( 'Remote : $['+remote+']' )
	Echo.echo( 'Scripts:' )
	for item in ls_repo():
		state = item["state"]
		name  = OS.relpath( item["file"], _dir)
		link  = item["link"]
		text = '  [!['+state+']]'+(' '*(2-len(state)))+' @['+name+']'
		if link:
			text += ' -> $[' + link+']'
		Echo.echo(text)

def update_repo(args):
	git = Git.new(_dir)
	(s, remote) = git.remote(name = 'hello_shell')
	if s == 0:
		import Link
		Echo.echo('将要从 $['+remote+'] 恢复到 @['+_dir+']: ')
		# git.echo().pull('hello_shell')

		ref = []
		for item in Link.log():
			print(item, Link.exist(item))

			if Link.exist(item):
				continue
			if item.get("file") and item.get("link"):
				ref.append( item )
		if ref:
			# and Echo.input('$[是否恢复链接] (y/n): ').lower() == "y"
			for item in ref:
				Link.to_bin(item["file"], item["link"])

def backup_repo(args):
	git = Git.new(_dir)
	(s, o, f) = git.status()
	if s == 0 and len(f) > 0:
		git.echo().add()
		git.echo().commit(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
	git.echo().push("hello_shell")

def run(argv):
	from Args import Args

	args = Args.parse({
		"desc": " Hello Shell 配置仓库模块",
		"options": [
			["-d", "--dir",    "<file>",       "设置本地仓库路径"],
			["-r", "--remote", "<github url>", "设置 github 仓库地址，例：[user]/[repo name]"],
			["-u", "--update",   None,         "从 github 仓库更新到本地"],
			["-b", "--backup", None,           "备份仓库到 github"]
		]
	}, argv, True, True)
	
	if len(argv) == 0:
		if OS.isdir(_dir):
			list_repo()
		else:
			print(args.help())
		exit(0)

	if args.get("dir"):
		set_repo(args.get("dir"))

	if args.get("remote"):
		remote_repo(args.get("remote"))

	if args.get("update"):
		update_repo(args)

	elif args.get("backup"):
		backup_repo(args)


