#!/usr/bin/python
#coding:utf-8

import ConfigParser, re
import OS

class Conf():

	def __init__(self, file):
		self.file = file
		if not OS.isfile(file):
			OS.write(file, "")
		cp = ConfigParser.ConfigParser()
		cp.read(file)
		if not cp.has_section("def"):
			cp.add_section("def")
		if not cp.has_section("user"):
			cp.add_section("user")
		self.config_parser = cp

	def get(self, section, option):
		cp = self.config_parser
		if cp.has_section(section):
			if cp.has_option(section, option):
				return cp.get(section, option)

	def set(self, section, option, value):
		cp = self.config_parser
		if not cp.has_section(section):
			cp.add_section(section)
		return cp.set(section, option, value)

	def value(self, option, value = None):
		if value != None:
			self.set("user", option, value)
			self.save()
		return self.get("user", option) or self.get("def", option)

	def options(self):
		cp   = self.config_parser
		res = {}
		for k in cp.options("def") or []:
			res[k] = cp.get("def", k)
		for k in cp.options("user") or []:
			res[k] = cp.get("user", k)
		return res

	def save(self):
		self.config_parser.write(open(self.file, "w"))

	@staticmethod
	def read(file = None, create = False):
		import __main__
		if file == None or file == __main__.__file__:
			file = OS.filename(OS.realpath(__main__.__file__)) + ".ini"
		else:
			file = OS.realpath(file)
		if create == False:
			if not OS.isfile(file):
				return None
		return Conf(file)
