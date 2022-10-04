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
        print(clause)
        clauseTruth = False
        for num in clause:
            print(num)
            print((i >> (abs(num)-1)))
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
    i = 0
    totalLiterals = 0
    while line and line[0][0] != 'c' and i < 20:
        # each wff will be stored like [[1, 2], [2, -3]]
        line.pop()
        for num in line:
            totalLiterals += 1
        line = list(map(int, line))
        wff.append(line)
        line = file.readline().split(',')
        i += 1

    # call function verify on each assignment with the above wff
    satisfiable = None
    for i in range(1<<int(numVars)):
        print("i: ", i)
        if verify(i, wff):
            satisfiable = 'S'
    if not satisfiable:
        satisfiable = 'U' 

    # setting 
    if not satisfiableAns:
        rightAns = 0
    else:
        if satisfiableAns == satisfiable:
            rightAns = 1
        else:
            rightAns = -1

    # output
    execTime, values = None, None # dummy values for now 
    output(problemNum, numVars, numClauses, maxLiterals, totalLiterals, satisfiable, rightAns, execTime, values)
    
    # returning the next 'c' line back to readFile
    return ' '.join(line)

def readFile(fileName):
    file = open(fileName, 'r')
    line = file.readline()
    i = 0
    while line and i < 10:
        if line[0] == 'c':
            line = readWFF(line, file)
        i += 1
    
    file.close()
    f.close()


def main():
    readFile(sys.argv[1])

if __name__ == "__main__":
    main()