import sys
import csv

f = open('./CSV/2SAT.csv', 'w')
writer = csv.writer(f)

def solver(wff, numVars, values, currValue, assignment):

    tempValues = values.copy()

    if currValue not in tempValues:
        tempValues[currValue] = assignment
    else:
        return tempValues

    print(tempValues)

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
    currStackDict = {1:0}
    currStack = [1]
    currValue = 1

    while (currStack):
        print("Begin: ", currValue)
        print("Begin: ", values)
        print("--------------", currStackDict)
        print("--------------", currStack)
        newValues = {}

        if currStackDict[currValue] == 0:
            newValues = solver(wff, numVars, values, currValue, 0)
            currStackDict[currValue] = 1

        print("Middle: ", currValue)
        print("Middle: ", newValues)
        print("Middle: ", values)
        print("--------------", currStackDict)
        print("--------------", currStack)

        if newValues == {} and currStackDict[currValue] == 1:
            print("try two")
            newValues = solver(wff, numVars, values, currValue, 1)
            currStackDict[currValue] = 2

        print("Middle 2: ", currValue)
        print("Middle 2: ", newValues)
        print("Middle 2: ", values)
        print("--------------", currStackDict)
        print("--------------", currStack)

        if newValues == {}:
            discard = currStack.pop()
            del currStackDict[discard]
            if len(currStack) > 0:
                currValue = currStack[-1]
            else:
                return False
        else:
            values = newValues
            if currValue != int(numVars):
                currStackDict[currValue + 1] = 0
                currStack.append(currValue + 1)
                currValue = currValue + 1
            else:
                input = concatBools(values, numVars)
                return verify(input, wff)

        print("End: ", currValue)
        print("End: ", values)
        print("--------------", currStackDict)
        print("--------------", currStack)


    return False


def concatBools(values, numVars):

    input = []

    for i in range(int(numVars)):
        input.append(f"{values[int(numVars) - i]}")

    return int("".join(input),2)

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

    values = helper(wff, numVars)
    print("\n",values, "\n")

    return ' '.join(line)

def readFile(fileName):
    file = open(fileName, 'r')
    line = file.readline()

    i = 0

    while line and i < 10:
        if line.split()[0] == "c":
            line = readWFF(line, file)
        i += 1

    file.close()
    f.close()

def main():
    readFile(sys.argv[1])

if __name__ == "__main__":
    main()
