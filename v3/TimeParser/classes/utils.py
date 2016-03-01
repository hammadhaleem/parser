#!/usr/bin/env python
# -*- coding: utf-8 -*- 

DAY = "day"
TIME = "time"
conf_step = 10



class Utils(object):

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

	def __init__(self):
		super(Utils, self).__init__()

	def listToString(self, lis ,deli = ""):
		stri = ""
		for i in lis:
			stri = stri + deli + str(i) 
		return stri

	def sec_to_string(self, seconds):
		hr = int((seconds) / 3600)
		mini = (seconds - (hr*60*60))/60
		if hr < 10:
			hr = "0" +str(hr)
		if mini < 10:
			mini = "0" +str(mini)
		return str(hr) + str(mini)

	def timeSequence(self , number1 , number2 , step = conf_step):
		lis = list()
		number1 = self.timeToSeconds(number1)
		number2 = self.timeToSeconds(number2) +step
		while  number1 < number2:
			lis.append(number1)
			number1 = number1 + step
		return lis 

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
