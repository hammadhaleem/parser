#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import re



days = {
    "sunday": "sun",
    "monday": "mon",
    "tuesday": "tue",
    "wedneday": "wed",
    "thursday": "thu",
    "friday": "fri",
    "saturday": "sat"
}

mapp = {
    "sun": 0,
    "mon": 1,
    "tue": 2,
    "wed": 3,
    "thu": 4,
    "fri": 5,
    "sat": 6
}

class RegexParser(object):
    # pattern for finding the digits
    pattern = re.compile(r"\d*\d:?\d\d-\d*\d:?\d\d|\d-?\d?")
    day_loop =[0,1,2,3,4,5,6,0,1,2,3,4,5,6]
    temp = []

    def __init__(self):
        super(RegexParser, self).__init__()
        
    ### clean the string according to the constraints.
    def clean(self,string ):
            string  = string.replace("–","-").lower()

            for day in days:
                if day in string :
                    string  = string .replace(day, str(mapp[days[day]]))

            for day in mapp:
                if day in string :
                    string  = string .replace(day, str(mapp[day]))

            string  = re.sub(r' *to *', "-", string )
            string  = re.sub(r' *- *', "-", string )
            string  = re.sub(r' *: *', ":", string )
            string  = re.sub(r' *& *', "-", string )
            string  = string.replace(".", "")
            string  = string.replace("\\n", ";")
            string  = "S" + string 
            return string

    # find all the patterns in the input strings
    def paternize(self,string):
            temp = re.findall(self.pattern, string )
            return temp

    # utility for splitting the numbers
    def splInt(self, number):
        if number < 10:
            return "0"+str(number)
        return str(number)

    # convert to military time
    def toMilitaryTime(self , times ):
        time = times.split(":")
        try:
            t1 = self.splInt(int(time[0]))
            t2 = self.splInt(int(time[1]))
            return t1 + t2
        except Exception as e:
            return times

    #utility for adding bars 
    def _add_bar(self , lis , bar = "-"):
        stri = ""
        for i in lis :
            stri = stri + i + bar

        return stri[:len(stri)-1]

    # find time in the string 
    def findTime(self , lis):
        ret = []
        stri = self._add_bar(lis, " == ")
        li =  re.findall(r"[\d]*:[\d]*-[\d]*:[\d]*" , stri)+ re.findall(r"[\d][\d][\d][\d]-[\d][\d][\d][\d]" , stri)
        for elem in lis:
            if elem in li :
                tmp = []
                sub = elem.split("-")
                t1 = self.toMilitaryTime(sub[0])
                t2 = self.toMilitaryTime(sub[1])
                if ( int(t2) < int(t1)):
                    t2 = str(2400 + int(t2))
                ret.append(t1 +"-"+ t2 )
            else:
                ret.append("S"+elem)
        return ret

    # construct series in the day string. between two days find the correct order.
    def constructSeries(self , string):
        string  = string[1:]
        try:
            day1 , day2 = string.split("-")
        except :
            return "S"+string

        day1 = int(day1)
        day2 = int(day2)

        ct = 0 
        index = 0 
        index2  = 0 
        flag = False
        while ct < len(self.day_loop):
            if day1 == self.day_loop[ct] and flag is False:
                index = ct 
                flag = True
            if flag is True  and day2 == self.day_loop[ct] :
                index2 = ct +1
                break
            ct =ct + 1

        lis =self.day_loop

        lis = sorted(self.day_loop[index : index2])
        flag = True
        old = None
        for item in lis : 
            if old is None :
                old = item
            else:
                if item - old  > 1 : 
                    flag = False
                    break
                else:
                    old = item
        if flag is False : 
            lis = self.day_loop[index : index2]
        return "S"+str(lis[0]) + "-"+str(lis.pop())

    def competeDays(self , string):
        ret = []
        for elem in string : 
            if elem[0] is "S" :
                ret.append(self.constructSeries(elem))
            else:
                ret.append(elem)
        return ret 

    def combine(self, string ) :
        stri = ""
        for i in string : 
            if i[0] is "S":
                stri = stri + ";" + i + ":"
            else:
                stri = stri + i +","
        stri = stri[1:]
        tmp = stri[1:].replace("S", "")
        stri = "S"+tmp
        return stri[:len(stri)-1]

    # convert time to military time
    def timeToStr(self, time):
        if time < 10 : 
            return "000" +str(time)
        if time < 100 : 
            return "00" +str(time)
        if time < 1000 : 
            return "0" +str(time)
        if time < 10000 : 
            return "" +str(time)
        return str(time)

    def timeInSequence(self , list_time):
        # genrate overlapping time sequences and find out distinct intervals.
        list_time = sorted(list_time)
        big_list = []
        for el in list_time : 
            for item in el:
                for elem in item.split(","):
                    elem = elem.split("-")
                    if len(elem) >= 2 :
                        t1 , t2 = elem
                        big_list = big_list + list(range(int(t1), int(t2)+1 , 1))

        big_list = sorted(set(big_list))
        prev = None
        start = None
        interval = []
        flag = 0
        for number in big_list:
            if start is None :
                start = number
                prev = number
            elif number - prev > 1 :
                interval.append(self.timeToStr(start - flag)+"-"+self.timeToStr(prev))
                flag = 1
                start = None
            else:
                prev = number

        if(start is not None):
            interval.append(self.timeToStr(start - flag )+"-"+self.timeToStr(prev))
        return interval

    def toSeqDic(self , string):
        # generate dat aggregated sequence dictionary for computation.
        lis = string.split(";")
        dic = {}
        for elem in lis : 
            elem = elem.split(":")
            day = elem[0]
            time = elem[1:]
            if (day[0] == "S"):
                day = day[1:]
            try:
                dic[day].append(time)
            except:
                dic[day]  = [time]

        dici = {}
        for keys in dic.keys():
            ti = self.timeInSequence(dic[keys])
            if ti is not None:
                dici[keys] = ti
            else:
                dici[keys] = dic[keys]
        dic = dici

        revDic = {}
        for k in dic.keys():
                for item in dic[k]:
                    try:
                        revDic[item].append(k)
                    except:
                        revDic[item] = [k]
        flag = False
        for o in revDic.keys():
            if len(revDic[o]) > 1:
                flag = True
        return dic , revDic ,flag

    def mergeDays(self , lis):
        # merge sorted days in the list 
        stri = "S"
        for el in sorted(lis):
            stri = stri + el +","
        return stri[:len(stri) - 1] + ":"

    def dicToString(self , dic):
        # convert dictionary to string for rendering
        stri= "S"
        for key in dic.keys():
            if(len(dic[key]) >= 1):
                stri = stri + key + ":" 
                for time in dic[key]:
                    stri = stri  + time +","
                stri = stri[:len(stri)-1] + ";"
        stri = stri[:len(stri)-1]
        return stri

    def revDicToString(self , revDic):
        # convert time aggregated dictionary to string
        stri = ""
        for k in revDic.keys():
            stri = stri + self.mergeDays(revDic[k]) + k + ";"
        stri = stri[:len(stri)-1]
        return stri

    def run(self , string):
        string = self.paternize(self.clean(string))
        string = self.findTime(string)
        string = self.competeDays(string)
        string = self.combine(string)
        dic ,revDic , flag = self.toSeqDic(string)
        if flag is True:
            string = self.revDicToString(revDic)
        else:
            string = self.dicToString(dic)
        return string ,dic ,revDic
