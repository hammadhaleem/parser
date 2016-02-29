#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from utils import *

class  OpenTimesByDay(object):
	"""docstring for  Day"""
	def __init__(self, day, lis):
		self.day = day 
		self.times = lis

	def __str__(self):
		return self.day	

	def __repr__(self):
		return "<"+self.day + ":" + Utils().listToString(self.times,",")[1:] +">"

class  OpenTimes(object):
	def __init__(self, time, days):
		self.time = time
		self.days = days
		
	def __str__(self):
		return self.time	

	def __repr__(self):
		return "<" + self.time + + ":" + Utils().listToString(self.days,",")[1:] +">"
