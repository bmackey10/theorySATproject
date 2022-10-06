import sys
import csv

f = open('./CSV/2SAT.csv', 'w')
writer = csv.writer(f)

def solver(wff, values):


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

    # call function verify on each assignment with the above wff
    satisfiable, values = None, None
    startTime = time.time() * (10**6)

    values = {1:0}
    satisfiable = False

    while !satisfiable:
        values = solver(wff, values)
        if len(values.keys()) == numVars:
            satisfiable = True

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
