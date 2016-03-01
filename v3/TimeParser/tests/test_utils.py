#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import unittest

from TimeParser.classes import *

class TestUtil(unittest.TestCase):

	util_obj = Utils()
	
	def test_listToString_empty(self):
		util_obj = self.util_obj
		self.assertEqual( util_obj.listToString([]), '' )
		self.assertEqual( util_obj.listToString([1]), '1' )
		self.assertEqual( util_obj.listToString([1,2],","), ',1,2' )
		self.assertEqual( util_obj.listToString([1,"12"]), '112' )

	def test_sec_to_string(self):
		util_obj = self.util_obj
		self.assertEqual( util_obj.sec_to_string(0), '0000' )
		self.assertEqual( util_obj.sec_to_string(86400), '2400' )
		self.assertEqual( util_obj.sec_to_string(43200), '1200' )

	def test_toProperdays(self):
		util_obj = self.util_obj
		self.assertEqual( util_obj.toProperdays("sun"), '0')
		self.assertEqual( util_obj.toProperdays("mon"), '1')
		self.assertEqual( util_obj.toProperdays("tue"), '2')
		self.assertEqual( util_obj.toProperdays("wed"), '3')
		self.assertEqual( util_obj.toProperdays("thu"), '4')
		self.assertEqual( util_obj.toProperdays("fri"), '5')
		self.assertEqual( util_obj.toProperdays("sat;tue"), '0,1,2,6')
		self.assertEqual( util_obj.toProperdays("sun;mon"), '0,1')

	def test_timeToSeconds(self):
		util_obj = self.util_obj
		self.assertEqual( util_obj.timeToSeconds("0000"), 0)
		self.assertEqual( util_obj.timeToSeconds("1200"), 43200)
		self.assertEqual( util_obj.timeToSeconds("2400"), 86400)

	def test_timeSequence(self):
		util_obj = self.util_obj
		self.assertEqual( util_obj.timeSequence("0000","0001"), [0, 10, 20, 30, 40, 50, 60])
		self.assertEqual( util_obj.timeSequence("0000","0000"), [0])
