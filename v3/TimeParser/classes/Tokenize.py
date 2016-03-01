#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from utils import *
from dayAndTime import *

import re

class Token(object):
	def __init__(self, string):
		self.token = string
	
	def __str__(self):
		return self.token	

	def __repr__(self):
		return self.token

class DayToken(Token):
	def __init__(self, string):
		self.type = "day"
		Token.__init__(self,string)

	def __repr__(self):
		return self.token +":"+ self.type

class TimeToken(Token):
	def __init__(self, string):
		self.type = "time"
		Token.__init__(self,string)
		self.token = self.millitary_time(self.token)

	def __repr__(self):
		return self.token +":" +self.type


	def millitary_time(self , token):
		if re.findall(r"\d*\d\d\d-\d*\d\d\d" , token):
			return token

		if re.findall(r"\d*\d:?\d\d-\d*\d:?\d\d" , token):
			s1 = token.split("-")
			t1, t2 = s1[0] , s1[1]

			s1 = t1.split(":")
			t1 = s1[0] + s1[1]

			s1 = t2.split(":")
			t2 = s1[0] + s1[1]

			if (int(t1) > int(t2)):
				t2 = str(int(t2) + 2400)
			return t1 +"-" +t2


class stringToToken(object):
	vector  = []

	def __init__(self, string):
		self.string = string 
		
	def date_normal(self , stri):
		return re.findall(r"\d*\d:\d\d-\d*\d:\d\d|\d\d\d\d-\d\d\d\d" , stri)

	def days_find(self , stri):
		return re.findall(r"sun|mon|tue|wed|thu|fri|sat|and", stri)

	def parse(self):
		string = self.string + " "
		ptr = 0
		window = []
		literals = []
		while ptr < len(string):
			window.append(string[ptr])
			find_words = self.days_find(Utils().listToString(window))
			find_dates = self.date_normal(Utils().listToString(window))
			if len(find_words) > 0:
				for el in find_words:
					literals.append(DayToken(el))
				window = []

			elif len(find_dates)>0:
				for el in find_dates:
					literals.append(TimeToken(el))
				window = []

			ptr = ptr + 1
		self.vector = literals

	def extendliterals(self):
		dic = {}
		stri = ""
		dt = ""
		old = None
		for el in self.vector:
			if el.type is DAY:
				if dt is not "" : 
					stri = ""
				stri = stri + ";" +str(el)
				dt = ""
				old = "stri"
			elif el.type is TIME:
				dt = dt + ";" + str(el)
				try:
					dic[stri[1:]].append(dt[1:])
				except:
					dic[stri[1:]] = [dt[1:]]
				old = "dt"

		for k  in dic.keys():
			dic[k] = Utils().listToString(sorted(dic[k]),";") [1:]
		
		self.data_dic = {}
		for k  in dic.keys():
			days = Utils().toProperdays(k).split(",")
			times = set(dic[k].split(";"))
			for d in days:
				if d != "":
					try:
						self.data_dic[d] = list(set(self.data_dic[d] + list(times)))
					except:
						self.data_dic[d] = list(set([] + list(times)))
		

	def get_vector(self):
		return self.vector

	def to_dateTimeVector(self):
		self.dateTimeVector =[]
		for  k in self.data_dic.keys():
			
			self.dateTimeVector.append(OpenTimesByDay(k , self.data_dic[k]))

	def get_dateTimeVector(self):
		return self.dateTimeVector
