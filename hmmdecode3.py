import json
from pprint import pprint
import sys
from collections import defaultdict
import codecs

trans_probability = {}
emission_probability = {}
tagList = []
tagProbability = {}
inputlines = []


def transformData(data):
    global trans_probability
    global emission_probability
    global tagList
    global tagProbability
    trans_probability = data['trans_probability']
    emission_probability = data['emission_probability']
    tagList = list(data['tag_count'].keys())
    tagProbability = data['tag_probabilities']


def printData():
    # pprint(trans_probability)
    # pprint(emission_probability)
    # pprint(tag_count)
    # for x in inputlines:
     #   print(x)
    print(tagList)


def readInput():
    global inputlines
    filename = sys.argv[1]
    with open(filename,encoding="utf8") as f:
        inputlines = f.readlines()


def processLines():
    outputlines = []
    lengthOfTags = len(tagList)
    for line in inputlines:
        x = hmm(line, lengthOfTags)
        outputlines.append(x)
    return outputlines


def hmm(line, lengthOfTags):
    words = line.split()
    lengthOfwords = len(words)
    backPointer = defaultdict(str)
    hmmProbs = [[0 for x in range(lengthOfwords)] for y in range(lengthOfTags)]
    hmmProbs, backPointer = handleStartState(
        lengthOfTags, words[0], hmmProbs, backPointer)

    for wordCounter in range(1, lengthOfwords):
        for tagCounter in range(0, lengthOfTags):
            nodeToNodeTranProbability = float('-inf')
            backPointerValue = None
            for prevTagCounter in range(0, lengthOfTags):
                nodeProb = getTransmissionProbability(
                    tagList[prevTagCounter], tagList[tagCounter]) + hmmProbs[prevTagCounter][wordCounter-1]
                if(nodeProb > nodeToNodeTranProbability):
                    nodeToNodeTranProbability = nodeProb
                    backPointerValue = prevTagCounter
            #print("Emission Probabiity: {} nodeToNode probability {}".format(getEmissionProbability(
             #   tagList[tagCounter], words[wordCounter]), nodeToNodeTranProbability))
            
            viterbi_probs = getEmissionProbability(
                tagList[tagCounter], words[wordCounter]) + nodeToNodeTranProbability
            
            hmmProbs[tagCounter][wordCounter] = viterbi_probs
            # print(backPointerValue)
            backPointer[(tagList[tagCounter], wordCounter)
                        ] = tagList[backPointerValue]

    lastBackPointer = handleEndState(lengthOfTags, lengthOfwords-1, hmmProbs, backPointer)
    #print(lastBackPointer)
    taggedPos = decode(lastBackPointer, backPointer, words)
    string = ''
    for i in range(0,lengthOfwords):
        string = string + words[i]+'/'+taggedPos[i]+' '
    #print(string.strip())
    return string.strip()    
    


def decode(lastBackPointer, backPointer, words):
    #print(lastBackPointer)
    lengthofWords = len(words)
    tagResult = []
    tagResult.insert(0, lastBackPointer)
    for index in range(lengthofWords-1, 0, -1):
        pointer = backPointer[(lastBackPointer, index)]
        tagResult.insert(0, pointer)
        lastBackPointer = pointer
    return tagResult


def getTransmissionProbability(prevtag, tag):
    return trans_probability[prevtag][tag]


def getEmissionProbability(tag, word):
    if word in emission_probability.keys():
        if tag in emission_probability[word].keys():
            return emission_probability[word][tag]
        else:
            return float('-inf')
    else:
        return tagProbability[tag]


def handleStartState(lengthOfTags, word, hmmProbs, backPointer):
    for tagCounter in range(0, lengthOfTags):
        em_prob = getEmissionProbability(tagList[tagCounter], word)
        tran_prob = getTransmissionProbability('START', tagList[tagCounter])
        hmmProbs[tagCounter][0] = em_prob + tran_prob
        backPointer[(tagList[tagCounter], 0)] = 'START'
    return hmmProbs, backPointer


def handleEndState(lengthOfTags, wordCounter, hmmProbs, backPointer):
    nodeToNodeProbability = float('-inf')
    backPointerValue = None
    for tagCounter in range(0, lengthOfTags):
        nodeProb = getTransmissionProbability(
            tagList[tagCounter], 'END') + hmmProbs[tagCounter][wordCounter]
        if(nodeProb > nodeToNodeProbability):
            nodeToNodeProbability = nodeProb
            backPointerValue = tagCounter
    return tagList[backPointerValue]


def main():
    data = json.load(open('hmmmodel.txt',encoding='utf-8'))
    transformData(data)
    readInput()
    # printData()
    result = processLines()
    thefile = open('hmmoutput.txt', 'w', encoding='utf-8')
    for item in result:
      thefile.write("%s\n" % item)


if __name__ == '__main__':
    main()