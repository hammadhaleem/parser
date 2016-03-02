#!/usr/bin/env python
# -*- coding: utf-8 -*- 


import unittest

from TimeParser.classes import *

class TestTokens(unittest.TestCase):


	def test_parsing(self):

		tokens = stringToToken("fri-tue:06:30-22:30")
		tokens.parse()
		tokens.extendliterals()
		tokens.to_dateTimeVector()
		dic  = {'1': ['0630-2230'], '0': ['0630-2230'], '2': ['0630-2230'], '5': ['0630-2230'], '6': ['0630-2230']}
		
		
		dateTimeVector = []
		for  k in dic:
			dateTimeVector.append(OpenTimesByDay(k ,dic[k]))

		self.assertEqual(tokens.data_dic , dic)
		self.assertEqual(tokens.get_dateTimeVector() ,dateTimeVector)



		tokens = stringToToken("mon-fri:6:30-20:30")
		tokens.parse()
		tokens.extendliterals()

		tokens.to_dateTimeVector()
		dic  = {'1': ['630-2030'], '3': ['630-2030'], '2': ['630-2030'], '5': ['630-2030'], '4': ['630-2030']}
		
		
		dateTimeVector = []
		for  k in dic:
			dateTimeVector.append(OpenTimesByDay(k ,dic[k]))

		self.assertEqual(tokens.data_dic , dic)
		self.assertEqual(tokens.get_dateTimeVector() ,dateTimeVector)
