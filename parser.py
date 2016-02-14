#!/usr/bin/env python
# -*- coding: utf-8 -*- 
from parseRegex import * 


cases = {
    'Sunday: 7:00 to 11:00': 'S0:0700-1100'
  , 'Sunday: 15:00 to 1:00': 'S0:1500-2500'
  , 'Sun: 07:00-00:00': 'S0:0700-2400'
  , 'Mon-Sun: 12:30-01:00': 'S0-6:1230-2500'
  , 'Mon to Sun: 06:30 - 22:30': 'S0-6:0630-2230'
  , 'Fri to Tue: 06:30 - 22:30': 'S5-2:0630-2230'
  , 'Mon - Wed: 07:00-01:00': 'S1-3:0700-2500'
  , 'Mon-Thu & Sun: 09:30-22:30': 'S0-4:0930-2230'
  , 'Fri-Sat & PH: 09:30-23:00': 'S5-6:0930-2300'
  , 'Mon-Fri: 11:45-16:30; 17:45-23:30': 'S1-5:1145-1630,1745-2330'
  , 'Monday to Sunday: 12:00-15:00, 18:00-22:00': 'S0-6:1200-1500,1800-2200'
  , 'Mon：18:00-00:00': 'S1:1800-2400'  # :
  , 'Sat & Sun: 12:00-14:30；18:00-23:00': 'S6-0:1200-1430,1800-2300'  # ;
  , 'Mon to Fri: 6:30 – 20:30': 'S1-5:0630-2030'  # -
  , 'Mon.-Sat.: 11:30-22:30; Sun.: 10:30-22:30': 'S0:1030-2230;1-6:1130-2230'
  , 'Sun.-Thur. 11:00-23:00, Fri.-Sat. 11:00-00:00': 'S0-4:1100-2300;5-6:1100-2400'
  # , 'Mon-Sun\nBreakfast 07:00-11:00\nLunch 11:30-14:30\nTea 14:00-18:00\nSun-Thu Dinner 18:30-22:30\nFri & Sat Dinner 18:30-23:30': 'S0-4:0700-1100,1130-1800,1830-2230;5-6:0700-1100,1130-1800,1830-2330'
  , 'Mon-Sun: 06:00-23:00\n(Tea: 06:00-16:00)': 'S0-6:0600-2300'
  , 'Mon-Sat: 11:00-21:00 until 300 quotas soldout': 'S1-6:1100-2100'
  , 'Monday to Sunday & Public Holiday:\n12:00-15:00, 18:00-00:00': 'S0-6:1200-1500,1800-2400'
  , 'Restaurant Mon-Sun: 06:30-23:00\nBar Mon-Sun: 15:00-00:00\nBe on Canton Mon-Sun: 12:00-00:00': 'S0-6:0630-2400'
  , 'Mon-Sat: 2300-2500,0600-0800': 'S1-6:0600-0800,2300-2500'
  , 'Mon-Sat: 0000-2300,2301-2800': 'S1-6:0000-2300,2301-2800'
  , 'Fri-Sat: 0000-2300, Mon: 0000-2300': 'S1,5-6:0000-2300'
  , 'Fri-Sat: 0000-2300, Mon: 0000-2301': 'S1:0000-2301;5-6:0000-2300'
  }


count = 0
for k  in cases.keys():
  pr = RegexParser()
  line  ,dic, revDic= pr.run(k)
  line = line.strip(" ")
  if line != cases[k].strip(" "):
    print  count, "\t" , line,"\t",cases[k]  ,"\n\t\t" , dic ,"\n\t\t" ,revDic

    count = count +1
  else:
    print count , True , line


