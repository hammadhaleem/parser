#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import re

class stringCleaning(object):
	"""docstring for stringCleaning"""
	string = ""
	
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

	def __init__(self, string):
		super(stringCleaning, self).__init__()
		self.string = string

	def clean(self):
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


	def get_string(self):
		return self.string
	
	def set_string(self,string):
		self.string = string 



		