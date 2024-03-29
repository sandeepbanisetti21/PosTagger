import sys
from pprint import pprint
from collections import defaultdict
from decimal import Decimal
import json
import math
import re
inputlines = []

def superSplit(word):
    pair = []
    tags = re.split('(/)',word)
    tagsLength = len(tags)
    x = tags[tagsLength-1]
    word = "".join(tags[0:tagsLength-2])
    pair.append(word)
    pair.append(x)
    return pair  

def readFileToString():
    global inputlines
    filename = sys.argv[1]
    with open(filename,encoding="utf8") as f:
        inputlines = f.readlines()

def captureCount():
    for x in inputlines:
        parse(x)
    for t in listOfTags:
        myset.add(t)
    myset.add('START')
    myset.add('END')
   # pprint(tagCount)

def parse(string):
   words = string.split()
   words_tags = []
   count = 0  
   for x in words:
      tags = superSplit(x)
      listOfTags.append(tags[1])
      if(count==0):
          startTuple = ('START',tags[1])
          transisitionCount[startTuple] += 1
          emissionCount[(tags[0],tags[1])] += 1 
          count +=1
          tagCount['START'] += 1
      else:
          countEmissionAndTransistion(words_tags[len(words_tags)-1],tags)
          count +=1    
      words_tags.append(tags)

   lastTag = words_tags[len(words_tags)-1]
   endTuple = (lastTag[1],'END')
   transisitionCount[endTuple]+=1
   tagCount[lastTag[1]] += 1

#tags[0] = word
#tags[1] = tag
def countEmissionAndTransistion(prev_tags,tags):
    transisitionCount[(prev_tags[1],tags[1])] += 1
    tagCount[prev_tags[1]] += 1  
    emissionCount[(tags[0],tags[1])] +=1

def calculateProbs():
    for key, value in emissionCount.items():
        #print("key is {} value is {}".format(key,value))
        emission_probability[key[0]][key[1]] = math.log10(value/(tagCount[key[1]]))

    for key,value in transisitionCount.items():
        trans_probability[key[0]][key[1]] = math.log10(value/(len(myset)+ tagCount[key[0]]))    

def outputProbs():
    pprint(trans_probability)
    pprint(emission_probability)    

def performsmoothing():
    for key in myset:
        for key_tag in myset:
            transisitionCount[(key,key_tag)] += 1

def convertToJson(map):
    return [{'key':k, 'value': v} for k, v in map.items()]

def getTagProbabilities():
    probs = {}
    totalCountOfValues = 0
    for key,value in tagCount.items():
        totalCountOfValues = totalCountOfValues+value
    #print(totalCountOfValues)    
    for (key,value) in tagCount.items():
        #print("value {} totalCountOfValues {}".format(value,totalCountOfValues))
        probs[key] = math.log10(value/totalCountOfValues)
    return probs

def writeProbs():    
    del tagCount['START']
    del tagCount['END']
    tagProbabilities = getTagProbabilities()
    data = {}
    data['trans_probability'] = trans_probability
    data['emission_probability'] = emission_probability
    data['tag_count'] = tagCount
    data['tag_probabilities'] = tagProbabilities
    x = json.dumps(data,ensure_ascii=False)    
    with open('hmmmodel.txt','w',encoding='utf-8') as file:
        file.write(x)


myset = set()
transisitionCount = defaultdict(int)
emissionCount = defaultdict(int)
trans_probability = defaultdict(lambda: defaultdict(float))
emission_probability = defaultdict(lambda: defaultdict(lambda: float('-inf')))
tagCount = defaultdict(int)


global inputLines   
listOfTags = []
    
def main():
    readFileToString()
    captureCount()
    performsmoothing()
    calculateProbs()
    #outputProbs()
    writeProbs()
    #pprint(emissionCount)

if __name__ == '__main__':
    main()
        