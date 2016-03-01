#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import unittest

from TimeParser.classes import *

class TestUtil(unittest.TestCase):

	def test_listToString_empty(self):
		self.assertEqual( Utils().listToString([]), '' )
		self.assertEqual( Utils().listToString([1]), '1' )
		self.assertEqual( Utils().listToString([1,2],","), ',1,2' )
		self.assertEqual( Utils().listToString([1,"12"]), '112' )


