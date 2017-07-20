#!/usr/bin/python
#coding=utf-8

import re
import OS

class Args():
	_define    = []
	_help       = ""

	description = ""
	undefind    = []
	options     = {}
	errors      = []

	def __init__(self):
		pass

	def get(self, name):
		if name and name[0] == "-":
			opt = self.find(name)
			if opt:
				return self.options.get( opt["long"] or opt["shot"])
		return self.options.get(name)

	def define(self, shot, long, value, desc):
		tag  = None
		deft = None
		if value:
			value = value.strip()
		if desc:
			desc  = desc.strip()
		if shot and shot[0] != "-" or shot == "-":
			tag  = shot
			shot = None
		shot = shot and shot[1:]
		long = long and long[2:]
		if value:
			res  = re.match(r"^\= *(\w+$|\[ *\])", value)
			if res:
				val  = res.group(1)
				if val[0] == "[":
					deft = []
				elif val == "false":
					deft = False
				elif val == "true":
					deft = True
				else:
					deft = val
				if deft and (long or shot or tag):
					self.options[long or shot or tag] = deft
		self._define.append({
			"tag"    : tag,
			"shot"   : shot,
			"long"   : long,
			"default": deft,
			"value"  : value,
			"desc"   : desc or ""
		})

	def read(self, argv):
		count     = len(argv)
		pass_tags = []
		i         = 0
		while i < count:
			val = argv[i]
			if len(val) > 1 and val[0] == "-":
				if val[1] == "-":
					i = self.__read_argv(val, argv, i)
				else:
					for s in val[1:]:
						i = self.__read_argv("-"+s, argv, i)
			else:
				tag = "-"
				typ = list
				for opt in self._define:
					tag = opt.get("tag")
					if tag and tag not in pass_tags:
						typ = type(opt.get("default"))
						pass_tags.append(tag)
						break
					else:
						tag = "-"
				if typ == list:
					val = [val]
					while i+1 < len(argv) and argv[i+1][0] != "-":
						i += 1
						val.append(argv[i])
				self.__set_options(tag, val, typ)
			i += 1
		return self

	def find(self, key):
		if len(key) >= 2 and key[0] == "-":
			if key[1] == "-":
				key = key[2:]
				for opt in self._define:
					if opt["long"] == key:
						return opt
			else:
				key = key[1:]
				for opt in self._define:
					if opt["shot"] == key:
						return opt
		else:
			for opt in self._define:
				if opt["tag"] == key:
					return opt

	def help(self):
		if self._help:
			return self._help
		self._help = ""
		if self.description:
			self._help += self.description + "\n"
			
		if self._define:
			opts = ""
			for item in self._define:
				line = "    "
				if item.get("tag"):
					line += item.get("tag")
				elif item.get("shot"):
					line += "-" + item.get("shot")
					if item.get("long"):
						line += ", --"+item.get("long")
				elif item.get("long"):
					line += "--" + item.get("long")
				if item.get("value"):
					line += " "+item.get("value")
				if item.get("desc"):
					line += " " * (34 - len(line)) + "  "
					line += item.get("desc").replace("\n", "\n"+(" "*len(line)))
				opts += line + "\n"
			self._help += " Options:\n" + opts

		if type(self._help) == str:
			self._help = self._help.decode('utf-8')
		else:
			self._help = self._help.encode('utf-8')
		return self._help

	def __read_argv(self, key, argv, index):
		val = None
		opt = self.find(key) if self._define else {"long": key.replace("-", ""), "default": 1, "value" : "string"}
		if not opt:
			self.undefind.append(key)
			if key != "--help":
				self.errors.append('Undefind options "'+key+'"')
			return index
		typ = type(opt["default"])
		if opt["value"]:
			if typ == bool:
				val = True
			elif index+1 < len(argv) and argv[index+1][0] != "-":
				if typ == list:
					val   = [argv[index+1]]
					index += 1
					while index+1 < len(argv) and argv[index+1][0] != "-":
						val.append( argv[index+1] )
						index += 1
				else:
					val    = argv[index+1]
					index += 1
			else:
				val = opt["default"] != None and opt["default"] or ""
		else:
			val = True

		if val != None:
			self.__set_options(opt["long"] or opt["shot"], val, typ)
		return index

	def __set_options(self, key, value, typ):
		if typ == list:
			temp = self.options.get(key)
			if temp:
				if type(temp) != list:
					temp = [temp]
				if type(value) == list:
					temp += value
				else:
					temp.append(value)
			else:
				temp = value if type(value) == list else [value] 
			self.options[key] = temp
		else:
			self.options[key] = value

	@staticmethod
	def parse(option, argv = None, watch_help = False, check_error=False):
		typ = type(option)
		if typ is str or typ is unicode:
			args = OS.isfile(option) and read_file(option) or read_help(option)
		
		elif typ == dict:
			args             = Args()
			args.description = option.get("desc") or ""
			for item in option.get("options") or []:
				item += [None, None, None, None]
				args.define(item[0], item[1], item[2], item[3])
		elif typ == list:
			args = Args()
			argv = option
		
		else:
			args = Args()

		if argv:
			args.read(argv)
		if not args.get("help") and "--help" in args.undefind:
			args.options["help"] = True

		if watch_help and args.get("help"):
			print( args.help() )
			exit(0)
		if check_error and args.errors:
			import Echo
			Echo.echo( " ![" + "]\n ![".join(args.errors) + "]\n" )
			print( args.help() )
			exit(1)
		return args

def read_file(file):
	code = OS.read(file)
	if code:
		res = re.search(r"#\s+HELP DOCUMENT\s*((?:[ \t]*#[^\n]*\n)+)", code)
		if res:
			content = re.sub(r"(?m)^\s*#", "", res.group(1)).encode('utf-8')
			return read_help(content)

def read_help(content):
	content = re.sub(r"\t", "    ", content)
	sb_re  = r"(?:\[(?:\[(?:\[(?:\[[^\]]*\]|[^\]])*\]|[^\]])*\]|[^\]])*\]|\<[^>]+\>|\([^\)]+\))"
	syntax = re.compile(r" *(?:(-\w|-)?(?:, *)?(--[\w-]+)?|(\w+))( *\= *\w+| \w+| *\= *"+sb_re+"| *"+sb_re+")?( {2,}.*)?$")
	args   = Args()
	for s in content.split("\n"):
		if not s:
			continue
		res = syntax.search(s)
		if res and (res.group(1) or res.group(2) or res.group(3)):
			args.define(res.group(1) or res.group(3), res.group(2), res.group(4), res.group(5))
		else:
			if len(args._define) > 0:
				args._define[-1]["desc"] += "\n" + s.strip()
	args._help = content
	return args




