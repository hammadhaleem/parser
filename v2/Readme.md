####Natural Language Hours Parsing
Creating a parser that can read store opening hours written by a human and produce a machine-readable structured representation.


######Procedure

1.  Apply test tranformations , conversion from chinese to english / toLower.

2.  Tokenize the string with help of regex, read through the string and generate literals.

3.  Find out all the days and corresponding times.
  >>      { '0' : '11:00-21:00' , '1' : : '11:00-21:00' ....
  
4.  Complete the time for individual days, find overlapping durations and convert to millirary time.

5.  Create a reverse associtive list for the time : dates.

6.  merge and create string for output.

Please find a sequencial debug output for one of the cases.

    0. Input string : 'Mon.-Fri.: 12:00-14:30； 18:00-22:30\nSat.-Sun.&Public Holidays: 11:30-15:00; 18:00-22:30'
   
    1. Transformed string : mon-fri:12:00-14:30； 18:00-22:30;sat-sun and public holidays:11:30-15:00; 18:00-22:30
    
    2. Expected String : S1-5:1200-1430,1800-2230;6-0:1130-1500,1800-2230
    
    3. Parsed string : ['Xmon', 'Xfri', '1200-1430', '1800-2230', 'Xsat', 'Xsun', 'Xand', '1130-1500', '1800-2230']
    
    4. Constructed by day table : {'1': '1200-1430,1800-2230', '0': '1130-1500,1800-2230', '3': '1200-1430,1800-2230', '2': '1200-1430,1800-2230', '5': '1200-1430,1800-2230', '4': '1200-1430,1800-2230', '6': '1130-1500,1800-2230'}
    
    5. Constructed Map by time :{'1800-2230': '6,5,4,3,2,1,0', '1200-1430': '5,4,3,2,1', '1130-1500': '6,0'}
    
    6. Ordered final map by time and ordered pairs : OrderedDict([('0,6', '1130-1500,1800-2230'), ('1,2,3,4,5', '1200-1430,1800-2230')])
    
    7. Final output : S1-5:1200-1430,1800-2230;6-0:1130-1500,1800-2230
