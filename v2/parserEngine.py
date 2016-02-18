#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import re
class RegexParser(object):

	data_dic = {}
	
	day_seq = ["sun","mon","tue","wed","thu","fri","sat","sun","mon","tue","wed","thu","fri","sat"]
	number = "0,1,2,3,4,5,6,0,1,2,3,4,5,6"
	mapp = {
		"sun": 0,
		"mon": 1,
		"tue": 2,
		"wed": 3,
		"thu": 4,
		"fri": 5,
		"sat": 6
	}

	chinese_to_english = [
		("星期一至五","mon.-fri."),
		("星期六、日及公眾假期","sat.-sun.&public holidays"),
		("早餐(星期一至六)","Breakfast (Weekday)"),
		("早餐(星期日及公眾假期)","Breakfast (Sunday and Public Holiday)"),
		("星期日", "sun"),
		("至六","sat "),
		("至日","sun "),
		("一至" , "to"),
		("星期","mon "),
		("午餐","lunch"),
		("晚餐","dinner"),
		("露台咖啡廳","Verandah Café "),
		("糕點及三文治於","cakes and sandwiches only available from "),
		("供應"," daily"),
		("至五", "fri "),
		("\n", ";"),
		("一", " - "),
		("weekday","mon to fri"),
		("–"," - ")
	]

	def listToString(self , lis ,deli = ""):
		stri = ""
		for i in lis:
			stri = stri + deli + str(i) 
		return stri

	def date_normal(self , stri):
		return re.findall(r"\d*\d:\d\d-\d*\d:\d\d|\d\d\d\d-\d\d\d\d" , stri)

	def days_find(self , stri):
		return re.findall(r"sun|mon|tue|wed|thu|fri|sat|and", stri)

	def __init__(self, string):
		super(RegexParser, self).__init__()
		self.string = string

	def transformations(self):
		string = self.string

		for i in self.chinese_to_english : 
			string = string.replace(i[0],i[1])
		
		string  = string.lower()
		
		string  = str(re.sub(r' *to *', "-", string ))
		string  = str(re.sub(r' *- *', "-",  string ))
		string  = str(re.sub(r' *: *', ":",  string ))
		string  = str(re.sub(r' *& *', " and ",  string ))
		string  = string.replace(".", "")
		string  = string.replace("\\n", ";")
		self.string = string

	def millitary_time(self , time):
		if re.findall(r"\d*\d\d\d-\d*\d\d\d" , time):
			return time
		if re.findall(r"\d*\d:?\d\d-\d*\d:?\d\d" , time):
			s1 = time.split("-")
			t1, t2 = s1[0] , s1[1]

			s1 = t1.split(":")
			t1 = s1[0] + s1[1]

			s1 = t2.split(":")
			t2 = s1[0] + s1[1]

			if (int(t1) > int(t2)):
				t2 = str(int(t2) + 2400)
			return t1 +"-" +t2

	def timeToSeconds(self, number):
		return int(number[0:1])*60*60 + int(number[2:])*60


	# takes two numbers in strings
	def timeSequence(self , number1 , number2 , step = 30):
		lis = []
		number1 = self.timeToSeconds(number1)
		number2 = self.timeToSeconds(number2) +step
		while  number1 < number2:
			lis.append(number1)
			number1 = number1 + step
		return lis

	def primitive_parser(self):
		string = self.string + " "
		ptr = 0
		window = []
		literals = []
		while ptr < len(string):
			window.append(string[ptr])
			find_words = self.days_find(self.listToString(window))
			find_dates = self.date_normal(self.listToString(window))
			if len(find_words) > 0:
				for el in find_words:
					literals.append("X"+el)
				window = []

			elif len(find_dates)>0:
				for el in find_dates:
					literals.append(self.millitary_time(el))
				window = []
			ptr = ptr + 1
		self.literals = literals

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
		days_stri= self.listToString(sorted(ret),",")
		
		return days_stri[1:]

	def extendliterals(self):
		dic = {}
		stri = ""
		dt = ""
		old = None
		for el in self.literals:
			if el[0] == "X":
				if dt is not "" : 
					stri = ""
				stri = stri + ";" +el[1:]
				dt = ""
				old = "stri"
			else:
				dt = dt + ";" + el
				dic[stri[1:]] = dt[1:]
				old = "dt"

		for k  in dic.keys():
			days = self.toProperdays(k).split(",")
			for d in days:
				times = dic[k].split(";")
				try:
					self.data_dic[d] = sorted(set(self.data_dic[d]+ [times]))
				except:
					self.data_dic[d] = sorted(set(times))


	def run(self):
		self.transformations()
		self.primitive_parser()
		self.extendliterals()
		print self.data_dic  # { day1 : times1 , day2 : times2 , day3 : times3 }
		return self.string