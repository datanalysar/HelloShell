#!/usr/bin/python
#coding:utf-8

import re, sys

def color(text):
	patt = re.compile(r"#([rgbcdw])\[|(?!\\)(\]|\[)|([!@#$^])\[")
	color_map = {
		"r": "\033[91m", "!": "\033[91m",
		"g": "\033[92m", "$": "\033[92m",
		"b": "\033[34m", "^": "\033[34m",
		"c": "\033[36m", "@": "\033[96m",
		"d": "\033[90m", "#": "\033[90m",
		"w": "\033[37m", "~": "\033[37m"
	}
	ignore = 0
	passs  = 0
	last   = False
	res    = ""
	i      = 0
	while True:
		m = patt.search(text, i)
		if not m:
			if i < len(text):
				res += text[i:]
			break
		c = m.group(1) or m.group(2) or m.group(3)
		res += text[i: m.start()]
		color = color_map.get(c)
		if color:
			ignore += 1
			last = True
			res  += color
		elif c == "]":
			if last:
				if ignore > 0:
					ignore = max(0, ignore - 1)
					res += "\033[0m"
				else:
					passs = max(0, passs - 1)
					res += m.group(0)
			else:
				if passs > 0 or ignore <= 0:
					passs = max(0, passs - 1)
					res += m.group(0)
				else:
					ignore = max(0, ignore - 1)
					res += "\033[0m"
		else:
			if c == "[":
				last = False
				passs += 1
			res += m.group(0)
		i = m.end()
	return res

def echo( text):
	print(color(text))

def stdout( text):
	sys.stdout.write(color(text))

def input( prompt = "", limit = None, right = None):
	prompt = color(prompt)
	if limit:
		prompt = prompt.replace("%s", "["+"/".join(limit)+"]")
	if right and type(right) != list:
		right = [right] 
	while True:
		res = raw_input(prompt)
		if limit and res not in limit:
			continue
		if right:
			return res in right
		return res

def select(options, prompt = ": ", needful=False):
	for i in range(0, len(options)):
		echo("  [$["+str(i)+"]]  @[" + str(options[i]) + "]")
	while True:
		res = input(prompt)
		if res:
			if res.isdigit():
				i = int(res)
				if i < len(options):
					return options[i]
			if res in options:
				return res
		if needful:
			continue
		break
