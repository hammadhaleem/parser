#!/usr/bin/env python
# -*- coding: utf-8 -*- 


import unittest

from TimeParser.classes import *

class TestClean(unittest.TestCase):


	def test_cleaned_strings(self):
		obj = stringCleaning("")
		obj.clean()
		self.assertEqual( obj.get_string().strip(" ") , "")

		obj = stringCleaning("Fri to Tue: 06:30 - 22:30")
		obj.clean()
		self.assertEqual( obj.get_string().strip(" ") , "fri-tue:06:30-22:30")
		
	def test_string_class(self):
		obj = stringCleaning("##########")
		self.assertEqual(obj.set_string(""),None)
		self.assertEqual(obj.get_string(),"")