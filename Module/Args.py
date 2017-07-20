#!/usr/bin/python
#coding=utf-8

from Hello import Args
from Hello import OS

def run(argv):
	args = OS.isfile(argv[0]) and Args.parse(argv[0], argv[1:]) or Args.parse(argv)
	sh   = ""
	for k in args.options:
		val = args.options[k]
		typ = type(val)
		if typ is str:
			val = '"' + val + '"'
		elif typ is unicode:
			val = '"' + val + '"'
		elif typ is bool:
			val = val and "true" or "false"
		elif typ is list:
			ref = []
			for i in val:
				ref.append('"'+str(i)+'"')
			val = '('+" ".join(ref) + ')'
		else:
			val = str(val)
		sh += "argv_" + k.replace("-", "_").replace(" ", "_") + "=" + val.replace("\n", "\\n") + ";"
	
	sh += 'help_document="'+args.help().replace("\n", "\\n")+'";'
	
	if "--help" in args.undefind:
		sh += "argv_help=true;"
	if len(args.errors):
		sh += "argv_errors="+str(args.errors).replace("\n", "\\n")+";"
	
	print(sh)
	if len(args.errors):
		exit(1)
	
