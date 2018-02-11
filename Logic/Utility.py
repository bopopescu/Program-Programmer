#!/usr/bin/python

def generateSubsetsHelper(inputList, index, k, currList, result):
    if index >= len(inputList):
        result.append(currList)
        return
    if len(currList) >= k:
        result.append(currList)
        return 

    generateSubsetsHelper(inputList, index + 1, k, currList, result)
    generateSubsetsHelper(inputList, index + 1, k, currList + [inputList[index]], result)

def generateAllSubsets(inputList, k):
    result = []
    generateSubsetsHelper(inputList, 0, k, [], result)
    result.sort(key = len)

    return result

def main():
    print generateAllSubsets([1, 2, 3, 4, 5, 6, 7, 8], 10)

if __name__ == "__main__":
    main()