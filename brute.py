from re import L
import sys
import csv
import time

f = open('./CSV/brute.csv', 'w')
writer = csv.writer(f)

def output(args):
    # args = list(args)
    writer.writerow(args)

# def nextAssignment(numVars):
#     assignment = {}
#     for i in range(1, numVars+1):
#         assignment

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
    problemNum, maxLiterals, satisfiableAns = line[1], line[2], None

    if len(line) == 4:
        satisfiableAns = line[3]

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
        line = file.readline().split(',')

    # call function verify on each assignment with the above wff
    satisfiable, values = None, None
    startTime = time.time() * (10**6)
    for i in range(1<<int(numVars)):
        if verify(i, wff):
            satisfiable = 'S'
            values = i
    if not satisfiable:
        satisfiable = 'U'
    endTime = time.time() * (10**6)

    # setting
    if not satisfiableAns:
        rightAns = 0
    else:
        if satisfiableAns == satisfiable:
            rightAns = 1
        else:
            rightAns = -1

    if values:
        values = str(bin(values))[::-1]
        values = [x for x in values][:-2]
        ','.join(values)

    if values and len(values) < int(numVars):
        numZeros = (int(numVars) - len(values)) * [0]
        values = numZeros + values

    print(problemNum)
    # output
    execTime = endTime-startTime # dummy values for now
    outputarr = [problemNum, numVars, numClauses, maxLiterals, totalLiterals, satisfiable, rightAns, execTime]
    if values:
     outputarr.extend(values)
    output([x for x in outputarr])

    # returning the next 'c' line back to readFile
    return ' '.join(line)

def readFile(fileName):
    file = open(fileName, 'r')
    line = file.readline()

    while line:
        if line.split()[0] == 'c':
            line = readWFF(line, file)
            
            
    file.close()
    f.close()


def main():
    readFile(sys.argv[1])

if __name__ == "__main__":
    main()
