#!/usr/bin/python
#coding:utf-8

import codecs, os, commands
from os.path import *

__join = os.path.join

system = os.system
cd     = os.chdir
pwd    = os.getcwd

def issubpath(parent, sub):
	parent = normpath(parent).split("/")
	sub    = normpath(sub).split("/")
	for i in range(0, len(parent)):
		if i >= len(sub) or parent[i] != sub[i]:
			return False
	return True

def isabspath(path):
	if path[0] == "/" or path[0] == "~":
		return True

def read(file):
	if isfile(file):
		f = codecs.open(file, 'r', 'utf-8' )
		content = f.read().strip()
		f.close()
		return content
	return ""

def write(file, content, mode=0o666):
	if not isfile(file):
		dr = dirname(file)
		if dr and not isdir(dr):
			os.makedirs(dr)
	f = open(file, 'w')
	f.write(content)
	f.close()
	os.chmod(file, mode)

def mkdirs(path):
	os.makedirs(path)

def remove(path):
	return os.remove(path)

def ls(target, level = 0, _abs = True):
	res = []
	for sub in (popen("ls "+target, "2>/dev/null") or "").split("\n"):
		if not sub or sub[0] == ".":
			continue
		abs_sub = join(target, sub)
		res.append(_abs and abs_sub or sub)
		if level > 0 and isdir(abs_sub):
			for s in ls(abs_sub, level-1, _abs = _abs):
				res.append( _abs and s or join(sub, s) )
	return res

def join(*paths):
	return normpath( __join(*paths) )

def realpath(path):
	if islink(path):
		return os.readlink(path)
	return abspath(path)

def filename(path, base=False):
	if base:
		path = basename(path)
	ref = splitext(path)
	if ref:
		return ref[0]
	return ""

def extname(path):
	ref = splitext(path)
	if ref and len(ref) > 1:
		return ref[1]
	return ""

def popen(*cmd):
	output = os.popen( " ".join(cmd) )
	return output.read()

def cmd(*cmd):
	return commands.getstatusoutput(" ".join(cmd)+" 2>/dev/null")