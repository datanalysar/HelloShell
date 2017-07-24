#!/usr/bin/python
#coding:utf-8

import os, re
import Log
from Echo import Echo
from Hello import OS

__bash_profile = OS.expanduser("~/.bashrc")
if not OS.isfile(__bash_profile):
	__bash_profile = OS.expanduser("~/.bash_profile")

def read_bash():
	profile = OS.read(__bash_profile).encode("utf-8")
	pat = re.compile(r"(?m)^\s*alias([^=]+)\=(.+)$")
	pos = 0
	lis = []
	while True:
		m = pat.search(profile, pos)
		if m:
			name = m.group(1).strip()
			value = m.group(2).strip()
			if value[0] == "'" or value[0] == '"':
				value = value[1:-1]
			lis.append({"name": name, "value": value})
			pos = m.end() 
		else:
			break
	return lis

def add(name, value):
	Log.add_alias(name, value)
	ref = {"name": name, "value": value}
	if ref not in read_bash():
		OS.system('echo "alias '+name+'=\''+value+'\'" >> '+__bash_profile)
		Echo.echo("#y[执行如下命令，使别名生效]:\n  'source "+__bash_profile)

def delete(names):
	if type(names) != list:
		names = [names]
	Log.del_alias(names)
	profile = OS.read(__bash_profile)
	new = re.sub(r"(?m)\s*alias\s*("+"|".join(names)+r")\s*=.*$", "", profile)
	new = re.sub(r"(^|\n)\s*\n", "\1", new)
	if new != profile:
		OS.write(__bash_profile, new)
	Echo.echo("#y[执行如下命令，使别名生效]:")
	for name in names:
		Echo.echo("  unalias "+name)

def back():
	exist = read_bash()
	for d in Log.get("alias"):
		if d not in exist:
			OS.system('echo "alias '+d["name"]+'=\''+d["value"]+'\'" >> '+__bash_profile)
	Echo.echo("#y[执行如下命令，使别名生效]:\n  'source "+__bash_profile)

def ls():
	log   = Log.get("alias")
	exist = read_bash()
	for d in exist:
		if d in log:
			Echo.echo("  [$[✓]] alias $["+d["name"]+"]='!["+d["value"]+"]'")
		else:
			Echo.echo("  [![✓]] alias $["+d["name"]+"]='!["+d["value"]+"]'")
	for d in log:
		if d not in exist:
			Echo.echo("  [![?]] alias $["+d["name"]+"]='!["+d["value"]+"]'")

def run(argv):
	from Args import Args
	
	_help = """别名管理
usage: alias [name [= value]]
opations:
    -l, --list            查看现有别名
    -u, --update          还原别名
    -d, --del =[names]    删除别名
"""
	if not argv or argv[0] == "-h" or argv[0] == "--help":
		Echo.echo(_help)
		exit(0)

	if argv[0] == "-l" or argv[0] == "--list":
		ls()
		exit(0)

	if argv[0] == "-u" or argv[0] == "--update":
		ls()
		exit(0)

	if len(argv) >= 2 and (argv[0] == "-d" or argv[0] == "--del"):
		delete(argv[1:])
		ls()
		exit(0)

	ref = " ".join(argv).split("=")
	if len(ref) >= 2:
		add(ref[0].strip(), " ".join(ref[1:]).strip())
	else:
		Echo.echo("  ![参数不正确]：!["+" ".join(args.get("-"))+"]\n"+_help)