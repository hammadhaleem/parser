#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from utils import *


class  OpenTimesByDay(object):
	"""Process the day. """

	
	def __init__(self, day, lis):
		self.day = day 
		self.times = lis
		self.day_vector = [day]

	def __str__(self):
		return self.day	

	def __repr__(self):
		return "<"+Utils().listToString(self.day_vector,",")[1:] + ":" + Utils().listToString(self.times,",")[1:] +">"

	def sorted_times(self):
		return sorted(self.times)

	def add_day(self, day):
		self.day_vector.append(day)
		self.day_vector = sorted(self.day_vector)

	def __eq__(self, other):
		return sorted(self.times) == other.sorted_times()
		
	def __lt__(self, other):
		return int(self.day) < int(other.day)

	def __gt__(self, other):
		return int(self.day) > int(other.day)

	def generate_day_sequence(self):
		days = self.day_vector
		day_set = []
		for day in self.day_vector:
			day_set.append(int(day))
			day_set.append(7+ int(day))
		day_set =  list(set(day_set))

		interval = []
		old = day_set[0]
		prev = None
		for item in day_set:
			if prev is not None and item - prev != 1 :
				interval.append(range(old ,prev+1))
				old = item
				prev = item
			prev = item
		interval.append( range(old ,day_set.pop()+1))
		day_set = []
		for elem in interval:
			day_set.append((len(elem), elem))
		return sorted(day_set, reverse = True)

	def minus_7(self, lis):
		ret =[]
		for i in lis:
			if i - 7 >= 0 :
				ret.append(i-7)
			else:
				ret.append(i)
		return ret 

	def get_unique_days(self):
		day_set = self.generate_day_sequence()
		done = []
		sets = []
		for elem in day_set:
			set_1 = set(done)
			set_2 = set(self.minus_7(elem[1]))
			if set_1.intersection(set_2): 
				pass
			else:
				done = done + self.minus_7(elem[1])
				sets.append(self.minus_7(elem[1]))
		return (sets , self.times)

class  OpenTimes(object):
	def __init__(self, time, days):
		self.time = time
		self.days = days
		
	def __str__(self):
		return self.time	

	def __repr__(self):
		return "<" + self.time + + ":" + Utils().listToString(self.days,",")[1:] +">"
