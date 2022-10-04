import sys
import csv

f = open('./CSV/brute.csv', 'w')
writer = csv.writer(f)

def output(*args):
    args = list(args)
    writer.writerow(args)


def verify(i, wff, nextVal):
    for clause in wff:
        clauseTruth = False
        for num in clause:
            if abs(nextVal) < num:
                clauseTruth = True
                break
            if num < 0:
                if not ((i >> (abs(clause) - 1)) & 1):
                    clauseTruth = True
                    break
            if num > 0:
                if ((i >> (abs(clause) - 1)) & 1):
                    clauseTruth = True
                    break
        if not clauseTruth:
            return False
    return True

def tryAssignments(assignment, nextVal, numVars, wff):
    if not verify(assignment, wff, nextVal):
        return False
    if nextVal > numVars:
        return verify(assignment, wff, nextVal)
    if tryAssignments(assignment, nextVal + 1, numVars, wff):
        return True
    if tryAssignments(assignment | 1 << (nextVal - 1), nextVal + 1, numVars, wff):
        return True
    return False


def readWFF(line, file):
    # c line
    line = line.split()
    problemNum, maxLiterals, satisfiable = line[1], line[2], None

    if len(line) == 4:
        satisfiable = line[3]

    # p line
    line = file.readline().split()
    numVars, numClauses = line[2], line[3]

    # TODO: brute force
    line = file.readline().split(",")
    wff = []
    while line and line[0] != 'c':
        # UNSURE?: each wff will be stored like [[1, 2, 0], [2, -3, 0]]
        line.pop()
        wff.append(line)
        line = file.readline().split(",")


    tryAssignments(0, 1, numVars, wff)

    # output
    totalLiterals, rightAns, execTime, values = None, None, None, None # dummy values for now
    output(problemNum, maxLiterals, totalLiterals, satisfiable, rightAns, execTime, values)

    # returning the next 'c' line back to readFile
    return ' '.join(line)

def readFile(fileName):
    file = open(fileName, 'r')
    line = file.readline()
    while line:
        if line[0] == 'c':
            line = readWFF(line, file)

    file.close()
    f.close()


def main():
    readFile(sys.argv[1])

if __name__ == "__main__":
    main()
