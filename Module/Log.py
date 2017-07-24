#!/usr/bin/python
#coding:utf-8

import os, re
from Hello import OS

_log      = None

def log_file():
	import Repo
	return OS.join(Repo._dir, ".helloshel")

def get( tp = None):
	global _log
	if not _log:
		_log = {"link": [], "alias": []}
		lis = OS.read( log_file() ).split("\n")
		pat = re.compile(r"^\s*\[(link|alias)\]\s*\[((?:\[(?:\[[^\]]*\]|[^\]])*\]|[^\]])*)\](.+)$")
		for text in lis:
			m = pat.match(text)
			if m:
				typ   = m.group(1)
				name  = m.group(2).strip()
				value = m.group(3).strip()[1:-1].strip()
				if typ == "link":
					if OS.exists(name):
						ref = {"file": name, "link": value}
						if ref not in _log["link"]:
							_log["link"].append( ref )
				elif typ == "alias":
					ref = {"name": name, "value": value}
					if ref not in _log["alias"]:
						_log["alias"].append( ref )
	if tp:
		return _log.get(tp)
	return _log

def add_link(file, link):
	log = get()
	ref = {"file": file, "link": link}
	if ref not in log["link"]:
		log["link"].append( ref )
		save()

def add_alias(name, value):
	log = get()
	for d in log["alias"]:
		if d["name"] == name:
			d["name"] = value
			save()
			return
	log["alias"].append( {"name": name, "value": value} )
	save()
		

def del_link(file):
	link = get()["link"]
	old  = len(alias)
	if not OS.islink(file):
		for i in range(old-1, -1, -1):
			if link[i]["file"] == file:
				del link[i]
	else:
		for i in range(old-1, -1, -1):
			if link[i]["link"] == file:
				del link[i]
	if old != len(alias):
		save()

def del_alias(names):
	alias = get()["alias"]
	old   = len(alias)
	if type(names) != list:
		names = [names]
	for i in range(old-1, -1, -1):
		if alias[i]["name"] in names:
			del alias[i]
	if old != len(alias):
		save()

def save():
	if _log :
		lis = []
		for d in _log["alias"]:
			lis.append( "[alias] ["+d["name"]+"] ["+d["value"]+"]" )
		for d in _log["link"]:
			lis.append( "[link] ["+d["file"]+"] ["+d["link"]+"]" )
		OS.write(log_file(), "\n".join(lis))






