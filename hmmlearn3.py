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
    for t in listOfTags:
        myset.add(t)
    # myset = set(listOfTags)
    myset.add('START')
    formatTransisition()
    formatEmission()

def parse(string):
   words = string.split()
   words_tags = []
   count = 0  
   for x in words:
      tags = x.split("/")
      listOfTags.append(tags[1])
      if(count==0):
          startTuple = ('START',tags[1])
          transisitionCount[startTuple] += 1
          emissionCount[(tags[0],tags[1])] += 1 
          count +=1
      else:
          countEmissionAndTransistion(words_tags[len(words_tags)-1],tags)
          count +=1
      words_tags.append(tags)

def formatTransisition():
    for x in myset:
        for y in myset:
            trans_probability[x][y] = transisitionCount[(x,y)]

def formatEmission():
    for key, value in emissionCount.items():
        emission_probability[key[0]][key[1]] = value            

def countEmissionAndTransistion(prev_tags,tags):
    transisitionCount[(prev_tags[1],tags[1])] += 1 
    emissionCount[(tags[0],tags[1])] +=1

def outputCounts():
    pprint(transisitionCount)
    pprint(emissionCount)
    pprint(listOfTags)

def outputProbs():
    #pprint(trans_probability)
    pprint(emission_probability)    


myset = set()
transisitionCount = defaultdict(int)
emissionCount = defaultdict(int)
trans_probability = defaultdict(lambda: defaultdict(int))
emission_probability = defaultdict(lambda: defaultdict(int))

global inputLines   
listOfTags = []
    
def main():
    readFileToString()
    #outputInput()
    captureCount()
    # outputCounts()
    outputProbs()
        
if __name__ == '__main__':
    main()
        