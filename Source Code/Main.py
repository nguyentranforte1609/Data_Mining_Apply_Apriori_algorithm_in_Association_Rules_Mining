from itertools import combinations
from itertools import permutations

def getInput(numOfTrans, tableOfTrans):
    # Get number of transactions
    try:
        numOfTrans = int(input("Input number of transactions: "))
    except IOError as e:
        raise (e)
    # Get detail of each transaction
    for i in range(numOfTrans):
        tempInput = input("Transaction T" + str(i) + ": ")
        tableOfTrans.append(set(tempInput.split(" ")))
    return  numOfTrans, tableOfTrans

def generateInitalItemDict(itemDict, tableOfTrans):
    for trans in tableOfTrans:
        for item in trans:
            if item not in itemDict:
                itemDict[item] = 0
    return  itemDict

def countItemFrequency(itemDict, tableOfTrans, numOfTrans):
    for key in itemDict:
        for trans in tableOfTrans:
            if set(key).issubset(trans):
                itemDict[key] += 1

def saveItemSet(resItemSets, minSupp, itemDict, numOfTrans, resDict):
    for key in itemDict:
        if float(itemDict[key]/numOfTrans) >= minSupp:
            resItemSets.append(set(list(key)))
            resDict[key] = itemDict[key]
        else:
            itemDict[key] = -1

def generateCombinations(baseItemDict):
    listItemSets = []  # Contains itemsets that satisfy minsupp on previous level
    for key in baseItemDict:
        if (baseItemDict[key] > -1):
            listItemSets.append(frozenset(list(key)))
    combinationSets = combinations(listItemSets, 2)
    return  combinationSets

def generateSets(combinationSets):
    sets = set()
    for t in combinationSets:
        tempSet = t[0].union(t[1])
        sets.add(tempSet)
    return  sets

def pruneItemsets(listItemSets, baseItemDict):
    tempSet = set()
    for baseKey in baseItemDict:
        if baseItemDict[baseKey] == -1:
            for subset in listItemSets:
                if set(list(baseKey)).issubset(subset):
                    tempSet.add(subset)
    for subset in tempSet:
        listItemSets.remove(subset)

def regenerateItemDict(baseItemDict, level):
    newItemDict = {}
    combinationSets = generateCombinations(baseItemDict)
    listItemSets = generateSets(combinationSets)
    pruneItemsets(listItemSets, baseItemDict)
    for subset in listItemSets:
        tempKey = "".join(subset)
        newItemDict[tempKey] = 0
    return newItemDict

def applyApriori(numOfTrans, minSupp, tableOfTrans, resItemSets, resDict):
    level = 1
    baseItemDict = {}
    while(True):
        if (level == 1):
            baseItemDict = generateInitalItemDict(baseItemDict, tableOfTrans)
            countItemFrequency(baseItemDict, tableOfTrans, numOfTrans)
            saveItemSet(resItemSets, minSupp, baseItemDict, numOfTrans, resDict)
            # print(baseItemDict) DEBUG
        if (level > 1):
            crrItemDict = {}
            baseItemDict = regenerateItemDict(baseItemDict, level)
            countItemFrequency(baseItemDict, tableOfTrans, numOfTrans)
            saveItemSet(resItemSets, minSupp, baseItemDict, numOfTrans, resDict)
            # print(baseItemDict) DEBUG
        level += 1
        # Loop condition
        # There is no more itemset can be generated
        if (len(baseItemDict) <= 1): break #Temporary condition used for debugging


def findSupportValue(valueSet, resDict, isTuple = False):
    if isTuple == False:
        targetKey = "".join(valueSet)
        for key in resDict:
            if targetKey == key:
                return resDict[key]
    else:
        targetKey01 = "".join(valueSet[0]) + "".join(valueSet[1])
        targetKey02 = "".join(valueSet[1]) + "".join(valueSet[0])
        for key in resDict:
            if targetKey01 == key:
                return resDict[key]
            if targetKey02 == key:
                return  resDict[key]
    return 0



def applyAssociationRules(resItemSets, resDict, minConf, numOfTrans, resConf):
    tempCombinationSets = permutations(resItemSets,2)
    for t in tempCombinationSets: # t is a tuple
        supp01 = float(findSupportValue(t[0], resDict)/numOfTrans)
        supp02 = float(findSupportValue(t, resDict, True)/numOfTrans)
        try:
            if float(supp01/supp02) >= minConf and t not in resConf:
                resConf.append(t)
        except:
            continue

#
#   Main Operations
#
def displayResult(resItemSets, resConf):
    print("=============================")
    print("List of itemsets: ")
    for item in resItemSets:
        print(item)
    print("=============================")
    print("List of strong association: {X} => {Y}")
    for item in resConf:
        print(item)


def Main():
    # Init
    numOfTrans = 0
    minSupp = 0.5
    minConf = 0.5
    tableOfTrans = []   # List of set
    resItemSets = []    # List of sets
    resDict = {}
    resConf = []


    numOfTrans, tableOfTrans = getInput(numOfTrans, tableOfTrans)
    applyApriori(numOfTrans, minSupp, tableOfTrans, resItemSets, resDict)
    applyAssociationRules(resItemSets,resDict, minConf, numOfTrans, resConf)
    displayResult(resItemSets, resConf)

# Start
Main()

""" 
[SAMPLE_01]
Input number of transactions: 4
Transaction T0: A B C
Transaction T1: A C
Transaction T2: A D
Transaction T3: B E F
=============================
List of itemsets: 
{'A'}
{'C'}
{'B'}
{'A', 'C'}
=============================
List of strong association: {X} => {Y}
({'A'}, {'C'})
({'C'}, {'A'})


[SAMPLE_02]
Input number of transactions: 4
Transaction T0: A B C D
Transaction T1: A A D E
Transaction T2: B E F G
Transaction T3: C A E F
=============================
List of itemsets: 
{'B'}
{'D'}
{'C'}
{'A'}
{'E'}
{'F'}
{'E', 'A'}
{'C', 'A'}
{'E', 'F'}
{'D', 'A'}
=============================
List of strong association: {X} => {Y}
({'D'}, {'A'})
({'C'}, {'A'})
({'A'}, {'D'})
({'A'}, {'C'})
({'A'}, {'E'})
({'E'}, {'A'})
({'E'}, {'F'})
({'F'}, {'E'})
"""