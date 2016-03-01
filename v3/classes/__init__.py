from stringCleaning import *
from Tokenize import *

def run(inp):
  line   = stringCleaning(inp)
  line.clean()
  line   = line.get_string()
  line   = line.strip(" ")
  tokens = stringToToken(line)
  tokens.parse()
  tokens.extendliterals()
  tokens.to_dateTimeVector()
  output = tokens.get_dateTimeVector()


  return sorted(output)