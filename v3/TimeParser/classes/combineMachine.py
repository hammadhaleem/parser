#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from utils import *

class Machine(object):

	def __init__(self, day_time_vector):
		self.day_time_vector = day_time_vector

	def group_by_time(self):
		done = []
		while self.day_time_vector :
			elem = self.day_time_vector.pop()
			flag = True 
			for item in done:
				if item == elem:
					flag = False
					item.add_day(elem.day)
			if flag is True :
				done.append(elem)

		self.grouped_by_time = done
		return done

	def generate_day_sequences(self, output_vector):
		data = []
		for elem in output_vector:
				data.append(elem.get_unique_days())
		return data

	def repartition_time(self, list_of_times):
		time_intervals = []
		for time in list_of_times :
			time = time.split("-")
			time_intervals =list(set(sorted(time_intervals + Utils().timeSequence(time[0], time[1]))))
		time_intervals = sorted(list(set(time_intervals)))
		return sorted(Utils().getDistinctIntervals(time_intervals))



	def generate_string(self, day_sequences):
		string = []
		for elem in day_sequences:
			dy = []
			for days in elem[0]:
				d1 = str(days[0])
				d2 = str(days.pop())
				if d1 == d2 :
					dy.append(d1)
				else:
					dy.append(d1 +"-" + d2)
			time_intervals = self.repartition_time(sorted(elem[1]))
			tmp = Utils().listToString(sorted(dy),",")[1:] +":"+ Utils().listToString(time_intervals,",")[1:]
			string.append( tmp )
		return "S"+Utils().listToString(sorted(string),";")[1:]
		