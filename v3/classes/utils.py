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

	def sec_to_string(self, seconds):
		hr = int((seconds) / 3600)
		mini = (seconds - (hr*60*60))/60
		if hr < 10:
			hr = "0" +str(hr)
		if mini < 10:
			mini = "0" +str(mini)
		return str(hr) + str(mini)

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