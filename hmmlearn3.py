import sys
from pprint import pprint
from collections import defaultdict
from decimal import Decimal
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
        emission_probability[key[1]][key[0]] = value            

    for key,value in emission_probability.items():
        keyCount = 0
        for innerkey, innervalue in value.items():
            keyCount = keyCount + innervalue

        for innerkey,innervalue in value.items():
            emission_probability[key][innerkey] = Decimal.log10(Decimal(innervalue)/(Decimal(keyCount)))

def countEmissionAndTransistion(prev_tags,tags):
    transisitionCount[(prev_tags[1],tags[1])] += 1 
    emissionCount[(tags[0],tags[1])] +=1

def outputCounts():
    pprint(transisitionCount)
    pprint(emissionCount)
    pprint(listOfTags)

def outputProbs():
    pprint(trans_probability)
    pprint(emission_probability)    

def performsmoothing():
    for key,value in trans_probability.items():
        keyCount = 0
        for innerkey, innervalue in value.items():
            keyCount = keyCount + innervalue
        smoothedvalue = keyCount + len(myset)
        for innerkey,innervalue in value.items():
            if(innerkey!='START'):
                trans_probability[key][innerkey] = Decimal.log10(Decimal(trans_probability[key][innerkey] + 1)/Decimal(smoothedvalue))
              

myset = set()
transisitionCount = defaultdict(int)
emissionCount = defaultdict(int)
trans_probability = defaultdict(lambda: defaultdict(float))
emission_probability = defaultdict(lambda: defaultdict(float))

global inputLines   
listOfTags = []
    
def main():
    readFileToString()
    #outputInput()
    captureCount()
    #outputCounts()
    performsmoothing()
    outputProbs()

if __name__ == '__main__':
    main()
        