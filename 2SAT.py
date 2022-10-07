import sys
import csv
import time

f = open('./CSV/2SAT.csv', 'w')
writer = csv.writer(f)

def output(args):
    writer.writerow(args)


def solver(wff, numVars, values, currValue, assignment):

    tempValues = values.copy()

    if currValue not in tempValues:
        tempValues[currValue] = assignment
    else:
        return tempValues

    for clause in wff:
        indexOther = -1
        if tempValues[currValue] == 0 and currValue in clause:
            indexOther = int(not(clause.index(currValue)))
        elif tempValues[currValue] == 1 and -currValue in clause:
            indexOther = int(not(clause.index(-currValue)))

        if indexOther != -1:
            if clause[indexOther] < 0:
                if -clause[indexOther] in tempValues and tempValues[-clause[indexOther]] != 0:
                    return {}
                else:
                    tempValues[-clause[indexOther]] = 0
            elif clause[indexOther] > 0:
                if clause[indexOther] in tempValues and tempValues[clause[indexOther]] != 1:
                    return {}
                else:
                    tempValues[clause[indexOther]] = 1

    return tempValues


def helper(wff, numVars):

    values = {}
    currStackDict = {1:[0, {}]}
    options = [(x + 1) for x in range(int(numVars))]
    currStack = [1]
    currValue = 1

    while (currStack):
        newValues = {}
        origValues = values.copy()

        if currStackDict[currValue][0] == 0:
            newValues = solver(wff, numVars, values, currValue, 0)
            currStackDict[currValue][0] = 1

        if newValues == {} and currStackDict[currValue][0] == 1:
            newValues = solver(wff, numVars, values, currValue, 1)
            currStackDict[currValue][0] = 2

        if newValues == {}:
            while len(currStack) > 0 and currStackDict[currStack[-1]][0] == 2:
                discard = currStack.pop()
                del currStackDict[discard]
            if len(currStack) > 0:
                currValue = currStack[-1]
                values = currStackDict[currValue][1].copy()
            else:
                return False
        else:
            values = newValues
            if len(values) != int(numVars):
                currOptions = options.copy()
                for item in currStackDict:
                    currOptions.pop(currOptions.index(item))
                currStackDict[currOptions[0]] = [0, {}]
                currStack.append(currOptions[0])
                currStackDict[currValue][1] = origValues.copy()
                currValue = currOptions[0]
            else:
                [input, binaryVal] = concatBools(values, numVars)
                if verify(input, wff):
                    return binaryVal
    return False


def concatBools(values, numVars):

    input = []

    for i in range(int(numVars)):
        input.append(f"{values[int(numVars) - i]}")

    return [int("".join(input),2), "".join(input)[::-1]]


def verify(i, wff):
    for clause in wff:
        clauseTruth = False
        for num in clause:
            if num < 0:
                if not ((i >> (abs(num)-1)) & 1):
                    clauseTruth = True
                    break
            if num > 0:
                if ((i >> (abs(num)-1)) & 1):
                    clauseTruth = True
                    break
        if not clauseTruth:
            return False

    return True


def readWFF(line, file):
    # c line
    line = line.split()
    problemNum, maxLiterals, satisfiableAns = line[1], line[2], line[3]

    # p line
    line = file.readline().split()
    numVars, numClauses = line[2], line[3]

    # reading in wff
    line = file.readline().split(',')
    wff = []
    totalLiterals = 0

    while line != [''] and line[0][0] != 'c':
        # each wff will be stored like [[1, 2], [2, -3]]
        line.pop()
        for num in line:
            totalLiterals += 1
        line = list(map(int, line))
        wff.append(line)
        line = file.readline().split(",")

    startTime = time.time() * (10**6)
    values = helper(wff, numVars)
    endTime = time.time() * (10**6)

    if values:
        satisfiableAns = "S"
    else:
        satisfiableAns = "U"

    print(problemNum)
    # output
    execTime = endTime-startTime # dummy values for now
    outputarr = [problemNum, numVars, numClauses, maxLiterals, totalLiterals, satisfiableAns, -1, execTime]
    if values:
        outputarr.extend([x for x in values])
    output(outputarr)

    return ' '.join(line)

def readFile(fileName):
    file = open(fileName, 'r')
    line = file.readline()

    i = 0

    while line:
        if line.split()[0] == "c":
            line = readWFF(line, file)

        i += 1

    file.close()
    f.close()

def main():
    readFile(sys.argv[1])

if __name__ == "__main__":
    main()
