#!/usr/bin/python
#coding=utf-8

from Hello import Args
from Hello import OS


def shell_str(text):
	text = text.replace('"', '\\"')
	text = text.replace("\n", "\\n")
	return '"' + text + '"'

def shell_arr(arr):
	ref = []
	for v in arr:
		ref.append(shell_str(str(v)))
	return '('+' '.join(ref) + ')'

def run(argv):
	args = OS.isfile(argv[0]) and Args.parse(argv[0], argv[1:]) or Args.parse(argv)
	sh   = ''
	for k in args.options:
		val = args.options[k]
		typ = type(val)
		if typ is str or typ is unicode:
			val = shell_str(val)
		elif typ is bool:
			val = val and 'true' or 'false'
		elif typ is list:
			val = shell_arr(val)
		else:
			val = shell_str(str(val))
		sh += 'argv_' + k.replace('-', '_').replace(' ', '_') + '=' + val + ';'
	
	sh += 'help_document='+shell_str(args.help())+';'
	
	if len(args.errors):
		sh += 'argv_errors='+shell_arr(args.errors)+';'
	if '--help' in args.undefind:
		sh += 'argv_help=true;'
	print(sh)
	if len(args.errors):
		exit(1)
	
