#!/usr/bin/python
#coding:utf-8

import sys
from Hello import Echo

def run(argv):
	text = " ".join(argv).replace("\\n", "\n")
	if sys.stdin.isatty():
		stdin = sys.stdin.read()
		Echo.stdout( stdin + text )
	else:
		Echo.echo( text )