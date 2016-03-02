#!/usr/bin/env python
# -*- coding: utf-8 -*- 


import unittest

from TimeParser.classes import *

class Test_day_and_time(unittest.TestCase):


	def test_creation(self):
		obj = OpenTimesByDay("1",[])
		
		self.assertEqual( str(obj) , '1' )
		self.assertEqual ( obj.__repr__()  , '<1:>') 

		obj = OpenTimesByDay("1",[1,2,3,4])
		
		self.assertEqual( str(obj) , '1' )
		self.assertEqual ( obj.__repr__()  , '<1:1,2,3,4>') 

	def test_eq_operator(self):
		obj = OpenTimesByDay("1",[1,2,3,4])
		self.assertEqual ( obj , OpenTimesByDay("1",[1,2,3,4]))

	def test_minus(self):
		obj = OpenTimesByDay("1",[1,2,3,4])
		self.assertEqual (  obj.minus_7([1,2,3,4]) , [1,2,3,4] )
		self.assertEqual (  obj.minus_7([8,9,10,11]) , [1,2,3,4] )

	def test_time(self):
		obj = OpenTimes("",[])
		self.assertEqual( str(obj) , '' )

		obj = OpenTimes("11:30-12:30",[])
		self.assertEqual( str(obj) , '11:30-12:30' )

	def test_objects(self):
		obj =  OpenTimesByDay(6 , ['0000-2300'] )
		self.assertEqual( obj.generate_day_sequence() , [(1, [13]), (1, [6])])
		obj = OpenTimesByDay(1 ,['1200-1430', '0700-2300', '1200-1430', '0700-1030'])
		self.assertEqual( obj.generate_day_sequence() ,[(1, [8]), (1, [1])])



