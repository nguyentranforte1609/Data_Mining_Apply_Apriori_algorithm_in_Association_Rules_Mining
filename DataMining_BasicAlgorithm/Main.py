from itertools import combinations


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


def saveItemSet(resItemSets, minSupp, itemDict, numOfTrans):
    for key in itemDict:
        if float(itemDict[key]/numOfTrans) >= minSupp:
            resItemSets.append(set(list(key)))
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

def applyApriori(numOfTrans, minSupp, tableOfTrans, resItemSets):
    level = 1
    baseItemDict = {}
    while(True):
        if (level == 1):
            baseItemDict = generateInitalItemDict(baseItemDict, tableOfTrans)
            countItemFrequency(baseItemDict, tableOfTrans, numOfTrans)
            saveItemSet(resItemSets, minSupp, baseItemDict, numOfTrans)
            # print(baseItemDict) DEBUG
        if (level > 1):
            crrItemDict = {}
            baseItemDict = regenerateItemDict(baseItemDict, level)
            countItemFrequency(baseItemDict, tableOfTrans, numOfTrans)
            saveItemSet(resItemSets, minSupp, baseItemDict, numOfTrans)
            # print(baseItemDict) DEBUG
        level += 1
        # Loop condition
        # There is no more itemset can be generated
        if (len(baseItemDict) <= 1): break #Temporary condition used for debugging

#
#   Main Operations
#
def Main():
    # Init
    numOfTrans = 0
    minSupp = 0.5
    minConf = 0.5
    tableOfTrans = []   # List of set
    resItemSets = []    # List of sets

    # Get input
    #getInput(numOfTrans, tableOfTrans)
    numOfTrans = 4
    tableOfTrans = [
        {"A","B","C","D"},
        {"B", "B", "A", "C"},
        {"D", "E", "C", "D"},
        {"A", "C", "D", "C"},
    ]
    applyApriori(numOfTrans, minSupp, tableOfTrans, resItemSets)
    print(resItemSets)
Main()