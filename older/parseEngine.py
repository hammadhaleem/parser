#!/usr/bin/env python
# -*- coding: utf-8 -*- 
from nltk.tokenize import TweetTokenizer
import re

class Engine(object):

	string = "" 
	dayStack = []
	timeStack = []
	check_day_tree = {
		"sun" : 0,
		"mon" : 1,
		"tue" : 2,
		"wed" : 3,
		"thu" : 4,
		"fri" : 5, 
		"sat" : 6
	}

	single = ["1","2","3","6","7","8","9","0"]
	seprators = ['to']
	other = [":"]


	def __init__(self, arg = None):
		super(Engine, self).__init__()
		self.arg = arg

	def splInt(self, number):
		if number < 10:
			return "0"+str(number)
		return str(number)

	def toMilitaryTime(self , time ):
		time = time.split(":")
		try:
			t1 = self.splInt(int(time[0]))
			t2 = self.splInt(int(time[1]))
			return t1 + t2
		except Exception as e:
			return ""

	def timeSub(self, stri):
		lis =  re.findall("[0-9a-z\W][0-9]:[0-9][0-9a-z\W]" , stri)
		for i in lis :
			stri = stri.replace(i , " " +self.toMilitaryTime(i))
		return stri

	def generate_lists(self):
		string = self.string
		parsed = []
		ptr = 0 
		curr_ptr = 0
		parsed = TweetTokenizer().tokenize(string)
		tmp = []
		for elem in parsed : 
			if len(elem) >= 3 :
				try: 
					ty = int(elem)
					tmp.append(elem)
				except:
					tmp.append(elem[:3])
			else:
				tmp.append(elem)
		parsed = tmp
		return parsed

	def pair_elements(self, lis):
		# identify pairs 
		st1 = []
		st2 = []
		occ = 0 
		add = False

		for elem in lis:
			if elem in self.check_day_tree.keys():
				occ  = occ + 1
		
		if (occ % 2 != 0):
			add = True

		for ct in range(0, len(lis) ):
			if lis[ct] in self.seprators:
				try:
					e1 = lis[ct-1]
				except :
					e1 = None
				try:
					e2 = lis[ct+1]
				except :
					e2 = None
				st1.append((e1, e2))
				st2.append(e1)
				st2.append(e2)

		none_list = []
		ret_lis = []
		ct = 0
		while ct <  len(lis) : 
			elem = lis[ct]
			if (elem not in st2) and (elem in self.check_day_tree.keys()):
				for item in st1:
					tmp = ct -1 
					if ct is 0:
						tmp = 0
					try:
						if lis[tmp:].index(item[0]) > lis[tmp:].index(elem):
							# print "\t" , item , tmp , ret_lis , st1
							ret_lis.append((elem, None))
							ret_lis.append(item)
							st2.append(elem)
						# else:
							# ret_lis.append(item)
					except Exception as e :
						# print "\t\t",e, lis[tmp:] , item[0] , elem  , tmp , lis
						ret_lis.append(item)
						pass
				st1 = ret_lis
			ct = ct + 1
		
		ct  = 0 
		ret_lis = []
		try:
			while ct < len(st1):
				if(st1[ct][0] in self.check_day_tree.keys() and st1[ct+1][0] in self.check_day_tree.keys() ):
					ret_lis.append(st1[ct])
					ct = ct + 2
				else:
					ret_lis.append(st1[ct])
					ct = ct + 1
		except : 
			print st1  , self.string ,TweetTokenizer().tokenize(self.string)
		return ret_lis

	def parse(self, string ):
		ori = string
		string = string.lower().replace(".","").replace("–","-").replace("-"," to ")
		string = self.timeSub(string)
		for el in re.findall('[^A-Za-z0-9]+', string):
			string = string.replace(el , " " + el + " ")
		self.string = string
		lis = self.generate_lists()
		lis = self.pair_elements(lis)
		return lis 

	def reset(self):
		self.dayStack = []
		self.timeStack = []
		self.string = ""
		return None