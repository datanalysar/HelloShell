#!/usr/bin/python
#coding:utf-8

import ConfigParser, re
import OS

class Conf():

	def __init__(self, filename):
		self.filename = filename
		if not OS.isfile(filename):
			OS.write(filename, "")
		cp = ConfigParser.ConfigParser()
		cp.read(filename)
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
		self.config_parser.write(open(self.filename, "w"))

	@staticmethod
	def read(file = None, create = False):
		if file == None:
			import __main__
			file = OS.filename(OS.realpath(__main__.__file__)) + ".ini"
		if create == False:
			if not OS.isfile(file):
				return None
		return Conf(file)
