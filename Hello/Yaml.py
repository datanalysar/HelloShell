#!/usr/bin/python
#coding:utf-8

import re, os, codecs

__arr_symble = "_i_s_a_r_r_a_y_"
__syntax_re  = re.compile(r'^(\s*)(?:(-?)\s*([\w \-\d]*)\s*:\s*(.*)|(-)\s*(.*))$')

def __lexer_split(value):
	ref = re.split(r"(?<!\\),", value)
	res = []
	count = len(ref) - 1
	i = -1
	while i < count:
		i += 1
		v = ref[i].strip()
		if not v:
			continue
		if v[0] == '"' or v[0] == "'":
			q = v[0]
			if len(v) <= 1 or v[-1] != q:
				v = ref[i]
				while i + 1 <= count:
					i += 1
					v += "," + ref[i]
					if ref[i][-1].strip() == q:
						break
		res.append(v)
	return res

def __parse_value(value):
	value = value.strip()
	if not value:
		return ""
	if (value[0] == "'" or value[0] == '"'):
		return value[1:-1]

	elif value[0] == "[" and value[-1] == "]":
		res = []
		for v in __lexer_split(value[1:-1].strip()):
			v = __parse_value(v)
			if v:
				res.append(v)
		return res

	elif value[0] == "{" and value[-1] == "}":
		res = {}
		for v in __lexer_split(value[1:-1].strip()):
			v = v.split(":")
			if len(v) >= 2:
				res[v[0].strip()] = __parse_value(":".join(v[1:]))
		return res

	elif value == "false":
		return False
	elif value == "true":
		return True
	elif value == "~":
		return None
	elif value.isdigit():
		return float(value)
	return value

def __read_block(lines, index, m = None):
	m  = m or __syntax_re.match(lines[index])
	m2 = None
	count = len(lines)
	if m:
		indent = len(re.sub(r'\t', "    ", m.group(1)))
		isarr  = m.group(2) or m.group(5)
		name   = m.group(3)
		value  = m.group(4) or m.group(6) or ""

		while index + 1 < count:
			m2 = __syntax_re.match(lines[index+1])
			if m2:
				break
			index += 1
			value += "\n" + lines[index]
		if value == "":
			value = {}
		else:
			value = __parse_value(value)
		return (index, indent, isarr, name, value, m2)

def __clear_yaml_tree(data):
	if type(data) == dict:
		if data.get(__arr_symble):
			data = data[__arr_symble]
		else:
			for k in data:
				data[k] = __clear_yaml_tree(data[k])
			return data
	if type(data) == list:
		for i in range(0, len(data)):
			data[i] = __clear_yaml_tree(data[i])
		return data
	return data

def __error(line, index):
	return Exception("[Hello Yaml Parser] Do not support the syntax", '"'+line+'", line '+str(index+1))

def parse( text ):
	lines       = re.sub(r'(?m)\s*#.*$|^\s*$', "", text).split("\n")
	yaml_tree   = {}
	level       = -1
	level_stack = []
	node_stack  = []
	m           = None
	count       = len(lines)
	i           = -1
	while i < count - 1:
		i += 1
		if not lines[i]:
			continue
		if lines[i] == "---":
			if len(yaml_tree) != 0:
				raise __error(lines[i], i)
			continue

		block = __read_block(lines, i, m)
		if not block:
			raise __error(lines[i], i)

		(i, indent, isarr, name, value, m) = block
		
		# 层级管理
		if level == -1:
			level_stack.append( indent )
		elif indent > level_stack[level]:
			level_stack.append( indent )	
		elif indent < level_stack[level]:
			while level >= 0 and indent <= level_stack[level]:
				level_stack.pop()
				level = len(level_stack) - 1
				if len(node_stack) > 0:
					node_stack.pop()
			level_stack.append(indent)
		else:
			node_stack.pop()
		level = len(level_stack) - 1

		node = {name: value or {}} if isarr and name else value

		if len(node_stack) > 0:
			last = node_stack[-1]
			typ  = type(last)
			if typ != dict:
				raise __error(lines[i], i)
			if isarr:
				if last.get(__arr_symble) == None:
					last[__arr_symble] = []
				last[__arr_symble].append(node)
			else:
				last[name] = node
		else:
			if isarr:
				if type(yaml_tree) == dict:
					yaml_tree = []
				yaml_tree.append(node)
			else:
				yaml_tree[name] = node
		node_stack.append(node)

	return __clear_yaml_tree(yaml_tree)

def parse_file( file ):
	if os.path.isfile(file):
		f = codecs.open(file, 'r', 'utf-8' )
		content = f.read().strip()
		if type(content) == unicode:
			content = content.encode("utf-8")
		f.close()
		return parse(content)

def stringify(data, indent=False):
	typ = type(data)

	if typ == dict:
		ref = []
		for key in data:
			temp = stringify(data[key], True)
			if indent:
				temp = temp.replace("\n", "\n    ")
			ref.append(key + ": " + temp)

		if indent:
			return "\n    " + "\n    ".join(ref)
		return "\n".join(ref)

	elif typ == list:
		ref = []
		for val in data:
			temp = stringify(val, False).replace("\n", indent and "\n    " or "\n  ")
			ref.append(temp)
		if indent:
			return "\n  - " + "\n  - ".join(ref)
		return "- " + "\n- ".join(ref)

	elif typ == str or typ == unicode:
		return '"'+data.replace("\"", "\\\"")+'"'
	elif typ == bool:
		return data and "true" or "false"
	elif data == None:
		return "~"
	else:
		return str(data)
