import sys
import csv

f = open('./CSV/2SAT.csv', 'w')
writer = csv.writer(f)

def solver(wff, values, currValue):

    nextValue = None
    print(currValue)

    for clause in wff:
        print(values)
        indexOther = -1
        if values[currValue] == 0 and currValue in clause:
            indexOther = int(not(clause.index(currValue)))
        elif values[currValue] == 1 and -currValue in clause:
            indexOther = int(not(clause.index(-currValue)))

        if indexOther != -1:
            if clause[indexOther] < 0:
                if -clause[indexOther] in values and values[-clause[indexOther]] != 0:
                    return "error"
                else:
                    values[-clause[indexOther]] = 0
                    if not nextValue: -clause[indexOther]
            elif clause[indexOther] > 0:
                if clause[indexOther] in values and values[clause[indexOther]] != 1:
                    return "error"
                else:
                    values[clause[indexOther]] = 1
                    if not nextValue: clause[indexOther]

    if nextValue:
        values = solver(wff, values, nextValue)

    return values

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

    variable = 1
    assignment = 0
    oppositeChecked = False
    i = 0
    values = {variable : assignment}

    while len(values) < int(numVars) and i < 10:

        values = solver(wff, values, variable)

        if values == "error" and oppositeChecked == False:
            oppositeChecked = True
            values = {variable: int(not(assignment))}
        if len(values) < int(numVars) and values != "error":
            oppositeChecked = False
            variable += 1
            values[variable] = 0
        if values == "error" and oppositeChecked == True:
            return "unsatisfiable"

        print(values)

        i += 1


    return ' '.join(line)

def readFile(fileName):
    file = open(fileName, 'r')
    line = file.readline()

    i = 0

    while line and i < 2:
        if line.split()[0] == "c":
            line = readWFF(line, file)
            print(line)
        i += 1

    file.close()
    f.close()

def main():
    readFile(sys.argv[1])

if __name__ == "__main__":
    main()
