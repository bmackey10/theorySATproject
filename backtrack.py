#!/usr/bin/env python3

import sys
import csv
import time

count = 0

f = open('./CSV/backtrack.csv', 'w')
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
                if not ((i >> (abs(num) - 1)) & 1):
                    clauseTruth = True
                    break
            if num > 0:
                if ((i >> (abs(num) - 1)) & 1):
                    clauseTruth = True
                    break
        if not clauseTruth:
            return False
    return True

def tryAssignments(assignment, nextVal, numVars, wff):
    global count
    count += 1
    #if count == 1 or count == 10 or not count % 100:
    #    print(f"tryAssignments({assignment}, {nextVal}, {numVars}, {wff}) #{count}")
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
    problemNum, maxLiterals, satisfiableAns = line[1], line[2], None

    if len(line) == 4:
        satisfiableAns = line[3]

    # p line
    line = file.readline().split()
    numVars, numClauses = line[2], line[3]

    # TODO: brute force
    line = file.readline().split(",")
    wff = []
    totalLiterals = 0
    while line and line[0][0] != 'c':
        # UNSURE?: each wff will be stored like [[1, 2, 0], [2, -3, 0]]
        line.pop()
        for num in line:
            totalLiterals += 1
        line = list(map(int, line))
        wff.append(line)
        line = file.readline().split(",")

    # call function verify on each assignment with the above wff
    startTime = time.time() * (10**6)
    if tryAssignments(0, 1, int(numVars), wff):
        satisfiable = 'S'
    else:
        satisfiable = 'U'
    endTime = time.time() * (10**6)

    # get total # of literals

    # setting
    if not satisfiableAns:
        rightAns = 0
    else:
        if satisfiableAns == satisfiable:
            rightAns = 1
        else:
            rightAns = -1

    values = 0
    # output
    execTime = endTime - startTime
    outputarr = [problemNum, maxLiterals, totalLiterals, satisfiable, rightAns, execTime, values]
    if values:
        outputarr.extend(values)
    output([x for x in outputarr])

    # returning the next 'c' line back to readFile
    return ' '.join(line)

def readFile(fileName):
    file = open(fileName, 'r')
    line = file.readline()
    i = 0
    while line and i < 2:
        if line[0] == 'c':
            line = readWFF(line, file)
        i += 1

    file.close()
    f.close()


def main():
    readFile(sys.argv[1])

if __name__ == "__main__":
    main()
