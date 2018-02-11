#!/usr/bin/python

from z3 import *

ctr = 1

def getInterestingConstants(numBits):
    result = set([-1, 1, numBits - 1])

    # for i in range(numBits):
        # result.add(i)
    # Maybe add some more interesting constants later.

    return result

def resetCtr():
    global ctr
    ctr = 1 

# ------------------------- Uniary Operators ---------------------------------

# Logical Operators

def BVUnaryNot(numBits, num):
    global ctr

    inputVar = BitVec("I{}".format(ctr), numBits)
    outputVar = BitVec("O{}".format(ctr), numBits)

    inputVarList = [inputVar]
    phiVar = (outputVar == Not(inputVar))

    ctr += 1
    return (inputVarList, outputVar, phiVar)

def BVUnaryAnd(numBits, num):
    global ctr

    inputVar = BitVec("I{}".format(ctr), numBits)
    outputVar = BitVec("O{}".format(ctr), numBits)

    inputVarList = [inputVar]
    phiVar = (outputVar == inputVar & num)

    ctr += 1
    return (inputVarList, outputVar, phiVar)

def BVUnaryOr(numBits, num):
    global ctr

    inputVar = BitVec("I{}".format(ctr), numBits)
    outputVar = BitVec("O{}".format(ctr), numBits)

    inputVarList = [inputVar]
    phiVar = (outputVar == inputVar | num)

    ctr += 1
    return (inputVarList, outputVar, phiVar)

def BVUnaryXor(numBits, num):
    global ctr

    inputVar = BitVec("I{}".format(ctr), numBits)
    outputVar = BitVec("O{}".format(ctr), numBits)

    inputVarList = [inputVar]
    phiVar = (outputVar == inputVar ^ num)

    ctr += 1
    return (inputVarList, outputVar, phiVar)
 
# Arithmetic Operators

def BVUnaryAdd(numBits, num):
    global ctr

    inputVar = BitVec("I{}".format(ctr), numBits)
    outputVar = BitVec("O{}".format(ctr), numBits)

    inputVarList = [inputVar]
    phiVar = (outputVar == inputVar + num)

    ctr += 1
    return (inputVarList, outputVar, phiVar)

def BVUnaryMultiply(numBits, num):
    global ctr

    inputVar = BitVec("I{}".format(ctr), numBits)
    outputVar = BitVec("O{}".format(ctr), numBits)

    inputVarList = [inputVar]
    phiVar = (outputVar == inputVar * num)

    ctr += 1
    return (inputVarList, outputVar, phiVar)

def BVUnaryLeftShift(numBits, num):
    global ctr

    inputVar = BitVec("I{}".format(ctr), numBits)
    outputVar = BitVec("O{}".format(ctr), numBits)

    inputVarList = [inputVar]
    phiVar = (outputVar == inputVar << num)

    ctr += 1
    return (inputVarList, outputVar, phiVar)

def BVUnaryRightShift(numBits, num):
    global ctr

    inputVar = BitVec("I{}".format(ctr), numBits)
    outputVar = BitVec("O{}".format(ctr), numBits)

    inputVarList = [inputVar]
    phiVar = (outputVar == inputVar >> num)

    ctr += 1
    return (inputVarList, outputVar, phiVar)

UnaryOperators = [BVUnaryAnd, BVUnaryOr, BVUnaryXor, BVUnaryAdd, BVUnaryMultiply, BVUnaryLeftShift, BVUnaryRightShift] 
UnaryOpsSet = set([str(x) for x in UnaryOperators])

# ----------------------------- Binary Operations -----------------------------------

# Logical Operators

def BVBitwiseAnd(numBits):
    global ctr

    inputVar1 = BitVec("I{}1".format(ctr), numBits)
    inputVar2 = BitVec("I{}2".format(ctr), numBits)
    outputVar = BitVec("O{}".format(ctr), numBits)

    inputVarList = [inputVar1, inputVar2]
    phiVar = (outputVar == inputVar1 & inputVar2)

    ctr += 1
    return (inputVarList, outputVar, phiVar)

def BVBitwiseOr(numBits):
    global ctr

    inputVar1 = BitVec("I{}1".format(ctr), numBits)
    inputVar2 = BitVec("I{}2".format(ctr), numBits)
    outputVar = BitVec("O{}".format(ctr), numBits)

    inputVarList = [inputVar1, inputVar2]
    phiVar = (outputVar == inputVar1 | inputVar2)

    ctr += 1
    return (inputVarList, outputVar, phiVar)

def BVBitwiseXor(numBits):
    global ctr

    inputVar1 = BitVec("I{}1".format(ctr), numBits)
    inputVar2 = BitVec("I{}2".format(ctr), numBits)
    outputVar = BitVec("O{}".format(ctr), numBits)

    inputVarList = [inputVar1, inputVar2]
    phiVar = (outputVar == inputVar1 ^ inputVar2)

    ctr += 1
    return (inputVarList, outputVar, phiVar)

# Arithmetic Operators

def BVBitwiseAdd(numBits):
    global ctr

    inputVar1 = BitVec("I{}1".format(ctr), numBits)
    inputVar2 = BitVec("I{}2".format(ctr), numBits)
    outputVar = BitVec("O{}".format(ctr), numBits)

    inputVarList = [inputVar1, inputVar2]
    phiVar = (outputVar == inputVar1 + inputVar2)

    ctr += 1
    return (inputVarList, outputVar, phiVar)

def BVBitwiseSub(numBits):
    global ctr

    inputVar1 = BitVec("I{}1".format(ctr), numBits)
    inputVar2 = BitVec("I{}2".format(ctr), numBits)
    outputVar = BitVec("O{}".format(ctr), numBits)

    inputVarList = [inputVar1, inputVar2]
    phiVar = (outputVar == inputVar1 - inputVar2)

    ctr += 1
    return (inputVarList, outputVar, phiVar)

def BVBitwiseMultiply(numBits):
    global ctr

    inputVar1 = BitVec("I{}1".format(ctr), numBits)
    inputVar2 = BitVec("I{}2".format(ctr), numBits)
    outputVar = BitVec("O{}".format(ctr), numBits)

    inputVarList = [inputVar1, inputVar2]
    phiVar = (outputVar == inputVar1 * inputVar2)

    ctr += 1
    return (inputVarList, outputVar, phiVar)

BinaryOperators = [BVBitwiseAnd, BVBitwiseOr, BVBitwiseXor, BVBitwiseAdd, BVBitwiseSub, BVBitwiseMultiply]
BinaryOpsSet = set([str(x) for x in BinaryOperators])
