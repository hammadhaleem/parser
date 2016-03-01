For running the parser on the inputs      

     python Runparser.py

For running various testes on the code. ( Not 100% percent test coverage is achived )

     python RunTest.py


####Natural Language Hours Parsing
Creating a parser that can read store opening hours written by a human and produce a machine-readable structured representation.


######Procedure

1.  Apply test tranformations , conversion from chinese to english / toLower.

2.  Tokenize the string with help of regex, read through the string and generate literals.

3.  Find out all the days and corresponding times.
  
4.  Complete the time for individual days, find overlapping durations and convert to millirary time.

6.  merge and create string for output.

Please find a sequencial debug output for one of the cases.

    0. Input string : 'Mon.-Fri.: 12:00-14:30； 18:00-22:30\nSat.-Sun.&Public Holidays: 11:30-15:00; 18:00-22:30'
   
    1. Transformed string : mon-fri:12:00-14:30； 18:00-22:30;sat-sun and public holidays:11:30-15:00; 18:00-22:30
    
    2. Expected String : S1-5:1200-1430,1800-2230;6-0:1130-1500,1800-2230
    
    3. Parsed string : ['mon', 'fri', '1200-1430', '1800-2230', 'sat', 'sun', 'and', '1130-1500', '1800-2230']

    [<1:630-2030>, <3:630-2030>, <2:630-2030>, <5:630-2030>, <4:630-2030>]  ## Overloaded __repr__

    [<1,2,3,4,5:630-2030>]  ## Overloaded __repr__  ( taking union )
    
    4. Final output : S1-5:0630-2030