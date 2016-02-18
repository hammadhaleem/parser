#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import re
import collections
import itertools

conf_step = 10
class RegexParser(object):

	
	day_seq = ["sun","mon","tue","wed","thu","fri","sat","sun","mon","tue","wed","thu","fri","sat"]
	number = "01234560123"
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
		("露台咖啡廳",""),
		("Verandah Café", ""),
		("糕點及三文治於","cakes and sandwiches only available from "),
		("供應"," daily"),
		("至五", "fri "),
		("\n", ";"),
		("一", " - "),
		("Breakfast (Weekday)","mon to fri"),
		("–"," - "),
		("and Public Holiday" ," ")
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
		self.data_dic = {}
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


	# takes two numbers in strings
	def timeSequence(self , number1 , number2 , step = conf_step):

		lis = list()
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
			times = dic[k].split(";")
			time_intervals = []
			for time in times :
				time = time.split("-")
				time_intervals = time_intervals + self.timeSequence(time[0], time[1])
			for d in days:
				try:
					self.data_dic[d] = sorted(list(set(self.data_dic[d]+ [time_intervals])))
				except:
					self.data_dic[d] = sorted(list(set(time_intervals)))
		# print self.data_dic
		new_dic = {}
		for k in self.data_dic.keys():
			if k != '':
				new_dic[k] = self.getDistinctIntervals(self.data_dic[k])
		
		self.data_dic = new_dic

	def groupByTime(self):
		tmp = {}
		for k in self.data_dic.keys():
			for time in self.data_dic[k]:
				try:
					tmp[time].append(k)
				except:
					tmp[time] =[]
					tmp[time].append(k)
		for k in tmp.keys():
			tmp[k] = self.listToString(sorted(tmp[k], reverse = True) , ",")[1:]
		self.date_dic = tmp

		for k in self.data_dic.keys():
			self.data_dic[k] = self.listToString(self.data_dic[k], ",")[1:]

	def findKeyValueSets(self):
		new_dic = {}
		for day in self.data_dic.keys():
			for time in self.date_dic.keys():
				for dy in self.date_dic[time]:
					days = dy
					if day in days:
						try:
							new_dic[day] = list(set(sorted(new_dic[day] + [time])))
						except : 
							new_dic[day] = []
							new_dic[day].append(time)
		for k in new_dic:
			new_dic[k] =self.listToString(sorted(new_dic[k]) , ",")[1:]
		self.final_dic = new_dic

	def get_seq(self ,stri):
		if len(stri) > 1:
			# try:
			# 	try:
			# 		index = self.number.index(stri)
			# 		return self.number[index] +"-"+self.number[index+len(stri)-1]
			# 	except Exception as e:
			# 		stri = self.listToString(sorted(stri.split(","), reverse =True),",")[1:]
			# 		index = self.number.index(stri)
			# 		return self.number[index] +"-"+self.number[index+len(stri)-1]
			# except Exception as e:
			# 	t = stri.split(",")
			# 	for i in itertools.permutations(t, len(t)):
			# 		i = self.listToString(i,",")[1:]
			# 		try:
			# 			index = self.number.index(i)
			# 			return self.number[index] +"-"+self.number[index+len(stri)-1]
			# 		except:				
			# 			pass

				t = stri.split(",")
				lis = []

				for i in range(len(t)):
					lis.append(self.number.index(t[i]))
				lis = sorted(lis)
				interval = []
				old = lis[0]
				prev = None
				for item in lis:
					if prev is not None and item - prev != 1 :
						interval.append((old ,prev))
						old = item
						prev = item
					prev = item
				interval.append( (old ,lis.pop()))
				interval= sorted(interval) 
				ret = ""
				for i in interval:
					if(i[0] != i[1]):
						ret = ret + "," + self.number[i[0]] +"-"+self.number[i[1]]
					else:
						ret = ret + "," + self.number[i[0]] 
				
				stri = ret[1:]
		return stri

	def generate_string(self):
		group_by_value = {}
		tmp = self.final_dic
		for k in tmp.keys():
			try:
				group_by_value[tmp[k]]  = sorted(group_by_value[tmp[k]] + [k])
			except :
				group_by_value[tmp[k]]  = [] + [k]

		for k in group_by_value.keys():
			group_by_value[k] = self.listToString(sorted(group_by_value[k]) , ",")[1:]

		group_by_value = {v: k for k, v in group_by_value.items()}
		group_by_value = collections.OrderedDict(sorted(group_by_value.items()))
		self.group_by_value =group_by_value
		stri = "S"
		lis = []
		for k in group_by_value.keys():
			lis.append (self.get_seq(k) + ":" + group_by_value[k] )
		stri = "S"+self.listToString(sorted(lis), ";")[1:]
		self.string = stri

	def run(self):
		self.transformations()
		try:
			self.primitive_parser()
			self.extendliterals()
			self.groupByTime()
			self.findKeyValueSets()
			self.generate_string()
			# print self.string
			# print self.date_dic
			# print self.final_dic 
			# print self.group_by_value
		except Exception as e:
			print e
			print self.string
			print self.date_dic
			print self.final_dic 
			print self.group_by_value
		return self.string