#!/usr/bin/python
#coding:utf-8

import os, commands, re
from Echo import Echo

class GitRepo():

	_enable_echo = False

	def __init__(self, work_tree=None):
		self.work_tree = work_tree or os.getcwd()
		

	def echo(self):
		self._enable_echo = True
		return self

	def cmd(self, cmd, force=False, no_work=False):
		if self.work_tree and no_work == False:
			cmd = re.sub(r"^git ", "git --work-tree="+self.work_tree+" --git-dir="+os.path.join(self.work_tree, ".git")+" ", cmd.strip())
	
		if self._enable_echo:
			Echo.echo("#[hello git #] "+cmd)

		if not force and not os.path.exists(os.path.join(self.work_tree, ".git")):
			(status, output) = (1, "Not a git repository: !["+self.work_tree+"]")
		else:
			(status, output) = commands.getstatusoutput(cmd)

		if self._enable_echo:
			self._enable_echo = False
			Echo.echo("#[hello git -> " + output.replace("\n", "\nhello git -> ")+"]")
			if status != 0:
				exit(status)
		return (status, output)

	def exist(self):
		(status, output) = self.cmd("git branch")
		return status == 0

	def init(self):
		return self.cmd("git init "+self.work_tree, True, True)

	def add(self):
		return self.cmd("git add --all")

	def commit(self, message):
		return self.cmd("git commit --all -m \""+message+"\"")

	def status(self, abs_path = True):
		(status, output) = self.cmd("git status -s")
		if status == 0 and output.strip():
			res = []
			for l in output.split("\n"):
				m = re.match(r"\s*([^\s]+)\s+(.+)$", l)
				if m:
					file = abs_path and os.path.join(self.work_tree, m.group(2)) or m.group(2)
					res.append( {"state": m.group(1), "file": file} )
			return (0, output, res)
		return (status, output, [])

	def branchs(self):
		(status, output) = self.cmd("git branch")
		if status == 0:
			res = []
			for l in output.split("\n"):
				if l[0] == "*":
					res.append( l[1:].strip() )
				else:
					res.append( l.strip() )
			return res
		return []

	def branch(self):
		(status, output) = self.cmd("git branch")
		if status == 0:
			for l in output.split("\n"):
				if l[0] == "*":
					return l[1:].strip()

	def remote(self, add=None, name=None):
		if add:
			m = re.match(r"^(?:https?://)?(?:github\.com/)?([\w-]+/[\w-]+)(?:\.git)?$|^(?:git@)?github\.com:([\w-]+/[\w-]+)\.git$", add)
			if not m:
				return (99999, "地址不正确: "+add)
			git_add = m.group(1) or m.group(2)
			return self.cmd("git remote add " + (name or "origin") + " https://github.com/"+git_add+".git")
		else:
			(s, o) = self.cmd("git remote -v")
			if s == 0 and name:
				m = re.search(r"(?m)^\s*"+name+r"[ \t]+([^ ]+)[ \t]+\((\w+)\)[ \t]*$", o)
				if m:
					return (s, m.group(1))
			return (s, o)

	def pull(self, name="origin", branch="master", local_branch=None):
		cmd = "git pull "+name+" "+branch
		if local_branch:
			cmd += ":"+local_branch
		cmd += " --allow-unrelated-histories"
		return self.cmd(cmd)

	def fetch(self, name="origin", branch="master"):
		return self.cmd("git fetch "+name+" "+branch)

	def push(self, name="origin", branch="master"):
		old = self._enable_echo
		self._enable_echo = False
		loacl = self.branch() or "master"
		self._enable_echo = old
		return self.cmd("git push "+name+" "+loacl+":"+branch)

def new(work=None):
	return GitRepo(work)
