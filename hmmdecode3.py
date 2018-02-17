import json
from pprint import pprint
import sys
from collections import defaultdict

trans_probability = {}
emission_probability = {}
tagList = []
inputlines = []


def transformData(data):
    global trans_probability
    global emission_probability
    global tagList
    trans_probability = data['trans_probability']
    emission_probability = data['emission_probability']
    tagList = list(data['tag_count'].keys())


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
    with open(filename) as f:
        inputlines = f.readlines()


def processLines():
    outputlines = []
    lengthOfTags = len(tagList)
    for line in inputlines:
        outputlines.append(hmm(line, lengthOfTags))
    return outputlines


def hmm(line, lengthOfTags):
    words = line.split()
    lengthOfwords = len(words)

    backPointer = defaultdict(str)
    hmmProbs = [[0 for x in range(lengthOfwords)] for y in range(lengthOfTags)]
    

    hmmProbs,backPointer = handleStartState(lengthOfTags,words[0],hmmProbs,backPointer)
    print(hmmProbs)

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
            viterbi_probs = getEmissionProbability(tagList[tagCounter],words[wordCounter]) + nodeToNodeTranProbability
            hmmProbs[tagCounter][wordCounter] = viterbi_probs
            #print(backPointerValue)
            backPointer[(tagList[tagCounter],wordCounter)] = tagList[backPointerValue]

    lastBackPointer = handleEndState(lengthOfTags,lengthOfwords-1,hmmProbs,backPointer)
    taggedPos = decode(lastBackPointer,backPointer,words)
    print(taggedPos)
    
                    
def decode(lastBackPointer,backPointer, words):
    lengthofWords = len(words)
    tagResult = []
    tagResult.insert(0,lastBackPointer)
    for index in range (lengthofWords-1,0,-1):
        pointer = backPointer[(lastBackPointer,index)]
        tagResult.insert(pointer,0)
        lastBackPointer = pointer
    return tagResult


def getTransmissionProbability(prevtag, tag):
    return trans_probability[prevtag][tag]


def getEmissionProbability(tag, word):
    if word in emission_probability[tag]:
        return emission_probability[tag][word]
    else:
        return float('-inf')    

def handleStartState(lengthOfTags,word,hmmProbs,backPointer):
     for tagCounter in range(0, lengthOfTags):
        em_prob = getEmissionProbability(tagList[tagCounter], word)
        tran_prob = getTransmissionProbability('START', tagList[tagCounter])
        hmmProbs[tagCounter][0] = em_prob + tran_prob
        backPointer[(tagList[tagCounter],0)] = 'START'
     return hmmProbs,backPointer

def handleEndState(lengthOfTags,wordCounter,hmmProbs,backPointer):
    nodeToNodeProbability = float('-inf')
    for tagCounter in range (0,lengthOfTags):
        nodeProb = getTransmissionProbability(
                    tagList[tagCounter], 'END') + hmmProbs[tagCounter][wordCounter-1]
        if(nodeProb > nodeToNodeProbability):
            nodeToNodeProbability = nodeProb
            backPointerValue = tagCounter
    return tagList[backPointerValue]



def main():
    data = json.load(open('hmmmodel.txt'))
    transformData(data)
    readInput()
    # printData()
    result = processLines()


if __name__ == '__main__':
    main()
