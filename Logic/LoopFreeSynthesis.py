#!/usr/bin/python

from z3 import *
from ComponentsLibrary import *

from Queue import PriorityQueue
import sys

import Utility

def postProcessing(I, O, P, R, libConstraints, libParameterTable, libAssignments, RPermutation):
    """
    Performs post-processing on the satisfying assignments of the algorithm given
    the other constraints to display the program to the user in readable form.
    I, O, P, R, libConstraints are as in the synthesize function below
    libAssignments: key = name of variable
                    value = (location, the actual constraint)
    libParameterTable: key = name of the O variable
                       value = list of parameters used in that constraint 
    """
    result = []

    orderedOutputs = PriorityQueue()
    for tmpVar in R:
        locationVal, programLine = libAssignments[str(tmpVar)]
        orderedOutputs.put( (-locationVal, programLine, str(tmpVar)) )

    firstTime = True
    seenNames = set([])
    while not orderedOutputs.empty():
        currLocation, currProgramLine, OVarName = orderedOutputs.get()

        # This if case exists to get rid of useless lines of code
        if not firstTime and OVarName not in seenNames:
            continue

        for parameter in libParameterTable[OVarName]:
            varLoc, actualVar = libAssignments[str(parameter)]

            if varLoc == 0:
                currProgramLine = substitute(currProgramLine, (parameter, I))
            else:
                currProgramLine = substitute(currProgramLine, (parameter, RPermutation[varLoc]))
                seenNames.add(str(RPermutation[varLoc]))

        if firstTime:
            firstTime = False

            RIndex = -1
            for i in range(len(R)):
                if OVarName == str(R[i]):
                    RIndex = i
                    break
            currProgramLine = substitute(currProgramLine, (R[RIndex], O))
            # currProgramLine = simplify(currProgramLine)

        result.append(currProgramLine)

    return result[::-1]

def performSynthesis(I, O, P, R, libConstraints, libParameters, phiSpec):
    """ 
    Performs the algorithm described in "Synthesis of Loop-Free Programs" given 
    (non list valued) I, O
    P and R are as described in the paper.
    libConstraints contains the constraints followed by the functions.
    libParameters is a list of lists in bijection with R, where the values in each list
        represent parameters present in that corresponding value of R.
    phiSpec is a Z3 specification of the program to be synthesized.
    """
    L = P + R 
    M = len(libConstraints)

    # Edge cases 
    if len(P) == 0 or len(R) == 0 or len(libConstraints) == 0 or len(libParameters) == 0:
        return False

    # For locations, key = Z3 variable, value = location
    locations = {}
    for x in L:
        locations[x] = Int("Loc:{}".format(str(x)))

    # -------------------- Get phiLib -------------------------------------
    phiLib = True
    for constraint in libConstraints:
        phiLib = And(phiLib, constraint)

    # -------------------- Get phiCons ------------------------------------
    phiCons = True
    for i in range(len(R)):
        for j in range(i + 1, len(R)):
            x = R[i]
            y = R[j]
            phiCons = And(phiCons, (locations[x] != locations[y]))

    # -------------------- Get phiAcyclic ---------------------------------
    phiAcyc = True
    for i in range(len(R)):
        outputVar = R[i]
        for inputVar in libParameters[i]:
            phiAcyc = And(phiAcyc, locations[inputVar] < locations[outputVar])

    # -------------------- Get phiBound -----------------------------------
    phiBound = True
    for parameter in P:
        phiBound = And(phiBound, And(0 <= locations[parameter], locations[parameter] <= M))
    for returnVal in R:
        phiBound = And(phiBound, And(1 <= locations[returnVal], locations[returnVal] <= M))

    # -------------------- Get phiConn ------------------------------------
    phiConn = True
    for x in P:
        phiConn = And(phiConn, Implies(locations[x] == 0, x == I))

    for y in R:
        phiConn = And(phiConn, Implies(locations[y] == M, y == O))

    for x in P:
        for y in R:
            phiConn = And(phiConn, Implies(locations[x] == locations[y], x == y))

    # -------------------- Get phiWfp ------------------------------------- 
    phiWfp = And(phiBound, phiCons, phiAcyc)

    # -------------------- Get the final formula --------------------------
    finalFormula = ForAll(L + [I, O], And(phiWfp, Implies(And(phiLib, phiConn), phiSpec)))

    # -------------------- Solve ------------------------------------------
    s = Solver()
    s.add(finalFormula)

    if s.check() == sat:
        print ""
        m = s.model()
        for d in m.decls():
            print "{} = {}".format(d.name(), m[d])
    else:
        # print "unsat"
        return False

    # ------------------- Prepare for postprocessing ----------------------
    
    # See the specification for postProcessing() for information about the tables being made below
    PNameTable = {}
    for PVar in P:
        PNameTable[str(PVar)] = PVar

    libAssignments = {}
    RPermutation = {}
    for d in m.decls():
        name = d.name().split(":")[1]
        currLoc = m[d].as_long() 
        if name in PNameTable:
            libAssignments[name] = (currLoc, PNameTable[name])
        else:
            RIndex = -1
            for i in range(len(R)):
                RVar = R[i]
                if name == str(RVar):
                    RIndex = i

            libAssignments[name] = (currLoc, libConstraints[RIndex])
            RPermutation[currLoc] = R[RIndex]

    # print libAssignments

    libParameterTable = {}
    for i in range(len(R)):
        libParameterTable[str(R[i])] = libParameters[i]

    print "The synthesized program is: {}".format(postProcessing(I, O, P, R, libConstraints, libParameterTable, libAssignments, RPermutation))
    return True

def synthesizeBitvectorProgram(programSpec, numBits, maxDepth):

    # Form Input/Output
    I = BitVec('I', numBits)
    O = BitVec('O', numBits)

    interestingConstants = getInterestingConstants(numBits) 

    generatingSet = []
    # Generate all possible paths in increasing order of length
    for uniOp in UnaryOperators:
        for constant in interestingConstants:
            generatingSet.append( (uniOp, (numBits, constant)) )
    for binOp in BinaryOperators:
        generatingSet.append( (binOp, numBits) )

    operatorSets = Utility.generateAllSubsets(generatingSet, maxDepth)

    totalNumPrograms = len(operatorSets)
    currChecked = 0
    
    phiSpec = programSpec(I, O, numBits)

    for operatorSet in operatorSets:
        libParameters = []
        R = []
        libConstraints = []
        for op, args in operatorSet:
            hashVal = str(op)

            if hashVal in UnaryOpsSet:
                arg0, arg1 = args
                currIList, currO, currPhi = op(arg0, arg1)

            else:
                currIList, currO, currPhi = op(args)

            libParameters.append(currIList)
            R.append(currO)
            libConstraints.append(currPhi)

        # Form P
        P = [x for Ix in libParameters for x in Ix]

        if performSynthesis(I, O, P, R, libConstraints, libParameters, phiSpec):
            return 

        currChecked += 1
        sys.stdout.write("\rEvaluated {} / {} programs".format(currChecked, totalNumPrograms))
        sys.stdout.flush()

        resetCtr() 

def synthesizeStrToStrProgram():
    I = StringSort()
    O = StringSort()

    pass

def synthesizeStrToIntProgram():
    I = StringSort() 
    O = IntSort()

    X = I + I



# ---------------------------------- User specified program specifications ------------------------------

def turnOffLSBSpec(I, O, numBits):
    """
    I = input bitvector
    O = output bitvector
    numBits = integer describing the number of bits
    """
    result = (I == I) 
    for t in range(numBits):
        innerSpecLHS = (Extract(t, t, I) == 1)
        for boolVal in [Extract(j, j, I) == 0 for j in range(t)]:
            innerSpecLHS = And(innerSpecLHS, boolVal)

        innerSpecRHS = (Extract(t, t, O) == 0)
        for boolVal in [Extract(j, j, I) == Extract(j, j, O) for j in range(numBits) if j != t]:
            innerSpecRHS = And(innerSpecRHS, boolVal)

        result = And(result, Implies(innerSpecLHS, innerSpecRHS))

    return result

def turnOnLeastSigZeroSpec(I, O, numBits):
    result = True
    for t in range(numBits):
        LHS = (Extract(t, t, I) == 1)
        for boolVal in [Extract(tp, tp, I) == 0 for tp in range(t)]:
            LHS = And(LHS, boolVal)

        RHS = (Extract(t, t, O) == 1)
        for boolVal in [Extract(tp, tp, O) == 0 for tp in range(numBits) if tp != t]:
            RHS = And(RHS, boolVal)

        result = And(result, Implies(LHS, RHS))

    return result

def turnOffOneStreamSpec(I, O, numBits):
    result = True

    for t in range(numBits):
        innerSpecLHS = Extract(t, t, I) == 0
        for j in range(t):
            innerSpecLHS = And(innerSpecLHS, Extract(j, j, I) == 1)

        innerSpecRHS = True
        for j in range(t):
            innerSpecRHS = And(innerSpecRHS, Extract(j, j, O) == 0)

        for j in range(t, numBits):
            innerSpecRHS = And(innerSpecRHS, Extract(j, j, O) == Extract(j, j, I))

        result = And(result, Implies(innerSpecLHS, innerSpecRHS))

    return result

def addSpec(I, O, numBits):
    return O == I + 1

def absolutePowerSpec(I, O, numBits):
    return (O == If(I >= 0, I, -I))

def signumSpec(I, O, numBits):
    # sgnSpec = And(Implies(I < 0, O == -1), Implies(I == 0, O == 0), Implies(I > 0, O == 1))
    sgnSpec = If(I < 0, O == -1, O == 1)
    return sgnSpec

def main():
    numBits = 8 
    maxDepth = 3

    # synthesizeStrToIntProgram()
    synthesizeBitvectorProgram(turnOffLSBSpec, numBits, maxDepth)
    synthesizeBitvectorProgram(turnOnLeastSigZeroSpec, numBits, maxDepth)
    synthesizeBitvectorProgram(turnOffOneStreamSpec, numBits, maxDepth)
    synthesizeBitvectorProgram(addSpec, numBits, maxDepth)
    synthesizeBitvectorProgram(absolutePowerSpec, numBits, maxDepth)
    synthesizeBitvectorProgram(signumSpec, numBits, maxDepth)

if __name__ == "__main__":
    main()
