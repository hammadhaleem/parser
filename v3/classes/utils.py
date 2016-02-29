#!/usr/bin/env python
# -*- coding: utf-8 -*- 

DAY = "day"
TIME = "time"
conf_step = 10
class Utils(object):
	def listToString(self, lis ,deli = ""):
		stri = ""
		for i in lis:
			stri = stri + deli + str(i) 
		return stri
		