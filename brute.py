from re import L
import sys
import csv

f = open('./CSV/brute.csv', 'w')
writer = csv.writer(f)

def output(*args):
    args = list(args)
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
                if not ((i >> (abs(clause)-1)) & 1):
                    clauseTruth = True
            if num > 0:
                if ((i >> (abs(clause)-1)) & 1):
                    clauseTruth = True
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
    print(line)
    wff = []
    while line and line[0] != 'c':
        # each wff will be stored like [[1, 2], [2, -3, 0]]
        line.pop()
        wff.append(line)
        line = file.readline().split(',')

    print(wff)
    # call function verify on each assignment with the above wff
    rightAns = None
    for i in range(1<<int(numVars)):
        if not verify(i, wff):
            satisfiable = 'U'
    if not rightAns:
        satisfiable = 'S' 

    # get total # of literals

    # setting 
    if not satisfiableAns:
        rightAns = 0
    else:
        if satisfiableAns == satisfiable:
            rightAns = 1
        else:
            rightAns = -1

    totalLiterals = None
    # output
    execTime, values = None, None # dummy values for now 
    output(problemNum, numVars, numClauses, maxLiterals, totalLiterals, satisfiable, rightAns, execTime, values)
    
    # returning the next 'c' line back to readFile
    return ' '.join(line)

def readFile(fileName):
    file = open(fileName, 'r')
    line = file.readline()
    while line:
        if line[0] == 'c':
            line = readWFF(line, file)
        break

    file.close()
    f.close()


def main():
    readFile(sys.argv[1])

if __name__ == "__main__":
    main()