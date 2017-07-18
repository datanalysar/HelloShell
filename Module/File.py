#!/usr/bin/python
#coding:utf-8

import codecs, os
from os.path import *

def issubpath(parent, sub):
	parent = normpath(parent).split("/")
	sub    = normpath(sub).split("/")
	for i in range(0, len(parent)):
		if i >= len(sub) or parent[i] != sub[i]:
			return False
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

def remove(path):
	return os.remove(path)

def ls_name(target, level = 0):
	res = []
	if isdir(target):
		for sub in os.listdir(target):
			if sub[0] == ".":
				continue 
			res.append(sub)
			if level > 0 and isdir(join(target,sub)):
				for s in ls_name(join(target,sub), level-1):
					res.append(join(sub,s))
	return res

def ls(target, level = 0):
	res = ls_name(target, level = level)
	for i in range(0, len(res)):
		res[i] = join(target, res[i])
	return res

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