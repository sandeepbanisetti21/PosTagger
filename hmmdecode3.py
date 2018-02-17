import json
from pprint import pprint
import sys

trans_probability = {}
emission_probability = {}
tag_count = {}
inputlines = []

def transformData(data):
    global trans_probability
    global emission_probability
    global tag_count
    trans_probability = data['trans_probability']
    emission_probability = data['emission_probability']
    tag_count = data['tag_count']

def printData():
    #pprint(trans_probability)
    #pprint(emission_probability)
    #pprint(tag_count)
    for x in inputlines:
        print(x)

def readInput():
     global inputlines
     filename = sys.argv[1]
     with open(filename) as f:
        inputlines = f.readlines() 

def main():   
    data = json.load(open('hmmmodel.txt'))
    transformData(data)
    readInput()
    printData()
    
    
if __name__ == '__main__':
    main()
    