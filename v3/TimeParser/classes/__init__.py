from stringCleaning import *
from Tokenize import *
from combineMachine import *
from dayAndTime import *
from utils import *



class Runner(object):
  def __init__(self):
    super(Runner, self).__init__()
    
  def run(self,inp):
    line   = stringCleaning(inp)
    line.clean()
    line   = line.get_string().strip(" ")
    

    tokens = stringToToken(line)
    tokens.parse()
    tokens.extendliterals()
    tokens.to_dateTimeVector()


    date_time_vectors = tokens.get_dateTimeVector()

    mach = Machine(date_time_vectors)

    vectored_seq = mach.group_by_time()
    
    output = mach.generate_day_sequences(vectored_seq)
    output = mach.generate_string(output)
    
    return output