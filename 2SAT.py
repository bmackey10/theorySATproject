import sys
import csv

f = open('./CSV/2SAT.csv', 'w')
writer = csv.writer(f)

def solver(wff, numVars, values, currValue, assignment):

    print(currValue)

    if currValue not in values:
        values[currValue] = assignment
    else:
        return values

    print("OUTSIDE BEFORE: ",currValue)
    print("OUTSIDE BEFORE: ", values)

    for clause in wff:
        print("INSIDE BEFORE: ", currValue, clause)
        print("INSIDE BEFORE: ", values, clause)
        indexOther = -1
        if values[currValue] == 0 and currValue in clause:
            indexOther = int(not(clause.index(currValue)))
        elif values[currValue] == 1 and -currValue in clause:
            indexOther = int(not(clause.index(-currValue)))

        if indexOther != -1:
            if clause[indexOther] < 0:
                if -clause[indexOther] in values and values[-clause[indexOther]] != 0:
                    values = {}
                else:
                    values[-clause[indexOther]] = 0
            elif clause[indexOther] > 0:
                if clause[indexOther] in values and values[clause[indexOther]] != 1:
                    values = {}
                else:
                    values[clause[indexOther]] = 1

        print("INSIDE AFTER: ", currValue, clause)
        print("INSIDE AFTER: ", values, clause)
        if values == {}:
            values = solver(wff, numVars, values, currValue, int(not(assignment)))
            if values == {}:
                return {}
            else:
                break


    print("OUTSIDE AFTER: ", currValue)
    print("OUTSIDE AFTER: ", values)

    while(currValue < int(numVars)):
        values = solver(wff, numVars, values, currValue, 0)
        currValue += 1

    if len(values) > 0:
        print("checking")
        input = concatBools(values, numVars)
        return verify(input, wff)
    else:
        return values

def concatBools(values, numVars):

    input = []

    for i in range(int(numVars)):
        input.append(values[i + 1])

    return int("".join(input))

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

    values = {}

    values = solver(wff, numVars, values, 1, 0)
    print(values)

    return ' '.join(line)

def readFile(fileName):
    file = open(fileName, 'r')
    line = file.readline()

    i = 0

    while line and i < 1:
        if line.split()[0] == "c":
            line = readWFF(line, file)
        i += 1

    file.close()
    f.close()

def main():
    readFile(sys.argv[1])

if __name__ == "__main__":
    main()
