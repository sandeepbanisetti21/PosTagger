import sys
from pprint import pprint
from collections import defaultdict
inputlines = []

def readFileToString():
    global inputlines
    filename = sys.argv[1]
    with open(filename) as f:
        inputlines = f.readlines()

def outputInput():
    i = 0
    for x in inputlines:
        print("{} {}".format(i,x))
        i = i+1

def captureCount():
    for x in inputlines:
        parse(x)

def parse(string):
   words = string.split()
   words_tags = []
   count = 0  
   for x in words:
      tags = x.split("/")
      if(count==0):
          startTuple = ('START',tags[1])
          transisitionCount[startTuple] += 1
          emissionCount[(tags[0],tags[1])] += 1 
          count +=1
      else:
          countEmissionAndTransistion(words_tags[len(words_tags)-1],tags)
          count +=1
      words_tags.append(tags)     

def countEmissionAndTransistion(prev_tags,tags):
    transisitionCount[(prev_tags[1],tags[1])] += 1 
    emissionCount[(tags[0],tags[1])] +=1

def outputCOunts():
    pprint(transisitionCount)
    pprint(emissionCount)

def main():
    readFileToString()
    #outputInput()
    captureCount()
    outputCOunts()

transisitionCount = defaultdict(int)
emissionCount = defaultdict(int)

global inputLines   
if __name__ == '__main__':
    main()
    