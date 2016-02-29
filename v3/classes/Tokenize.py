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
	day_seq = ["sun","mon","tue","wed","thu","fri","sat","sun","mon","tue","wed","thu","fri","sat"]
	mapp = {
		"sun": 0,
		"mon": 1,
		"tue": 2,
		"wed": 3,
		"thu": 4,
		"fri": 5,
		"sat": 6
	}

	def timeToSeconds(self, number):
		if len(number) < 4:
			n1 = number[0:1]
			n2 = number[1:]
		else:
			n1 = number[0:2]
			n2 = number[2:]
		if int(n1) < 10:
			n1 = "0"+n1 
		if int(n2) < 10:
			n2 = "0"+n2
		return int(n1)*60*60 + int(n2)*60

	def __init__(self, string):
		self.string = string 
		
	def date_normal(self , stri):
		return re.findall(r"\d*\d:\d\d-\d*\d:\d\d|\d\d\d\d-\d\d\d\d" , stri)

	def days_find(self , stri):
		return re.findall(r"sun|mon|tue|wed|thu|fri|sat|and", stri)

	def timeSequence(self , number1 , number2 , step = conf_step):

		lis = list()
		number1 = self.timeToSeconds(number1)
		number2 = self.timeToSeconds(number2) +step
		while  number1 < number2:
			lis.append(number1)
			number1 = number1 + step
		return lis 

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
			days = self.toProperdays(k).split(",")
			times = set(dic[k].split(";"))
			time_intervals = []
			for time in times :
				time = time.split("-")
				time_intervals =list( set(sorted(time_intervals + self.timeSequence(time[0], time[1])))) #self.timeSequence(time[0], time[1])
				
			for d in days:
				try:
					sets = sorted(set(list(set(self.data_dic[d])) + time_intervals))
					self.data_dic[d] =  sets
				except Exception as e:
					self.data_dic[d] = sorted(list(set(time_intervals)))
				
		
		new_dic = {}
		for k in self.data_dic.keys():
			if k != '':
				new_dic[k] = self.getDistinctIntervals(self.data_dic[k])
		
		self.data_dic = new_dic

	def getDistinctIntervals(self, time_list):
		interval = []
		old = time_list[0]
		prev = None
		for item in time_list:
			if prev is not None and item - prev != conf_step :
				interval.append( self.sec_to_string(old) +"-"+ self.sec_to_string(prev))
				old = item
				prev = item
			prev = item
		interval.append( self.sec_to_string(old)+"-"+self.sec_to_string(time_list.pop())) 
		return interval

	def sec_to_string(self, seconds):
		hr = int((seconds) / 3600)
		mini = (seconds - (hr*60*60))/60
		if hr < 10:
			hr = "0" +str(hr)
		if mini < 10:
			mini = "0" +str(mini)
		return str(hr) + str(mini)
	def get_day_seq(self, elems):
		rem = ['and' , 'None']
		e1 = elems[0]
		e2 = elems[1]
		ret = []
		if e1 in rem and e2 in rem:
			return []
		if e1 in rem:
			return [e2]
		if e2 in rem:
			return [e1]

		pt1 = -1
		pt2 = -1
		i = 0

		while i < len(self.day_seq):
			if pt2 is -1 and pt1 is -1:
				if e1 == self.day_seq[i] :
					pt1 = i
			if pt2 is -1 and pt1 is not -1:
				if e2 == self.day_seq[i] :
					pt2 = i
			i = i + 1
		return self.day_seq[pt1:pt2+1]

	def toProperdays(self , days_stri):
		days = days_stri.split(";")
		old = None
		lis = []
		for day in days:
			if  old is not None:
				lis.append((old,day))

			old = day

		lis.append(("None", old))
		other_lis = []
		for elem in lis:
			other_lis = other_lis+ self.get_day_seq(elem)

		ret = [] 
		for i in set(other_lis):
			ret.append(self.mapp[i])
		days_stri= Utils().listToString(sorted(ret),",")
		
		return days_stri[1:]

	def get_vector(self):
		return self.vector

	def to_dateTimeVector(self):
		self.dateTimeVector =[]
		for  k in self.data_dic.keys():
			self.dateTimeVector.append(OpenTimesByDay(k , self.data_dic[k]))

	def get_dateTimeVector(self):
		return self.dateTimeVector
