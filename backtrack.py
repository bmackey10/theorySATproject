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
        #print(clause, nextVal)
        clauseTruth = "false"
        for num in clause:
            if nextVal > abs(num):
                if num < 0:
                    if not ((i >> (abs(num) - 1)) & 1):
                        clauseTruth = "true"
                        break
                if num > 0:
                    if ((i >> (abs(num) - 1)) & 1):
                        clauseTruth = "true"
                        break
            else:
                clauseTruth = "unknown"
        #print(f"{clauseTruth}\n")
        if clauseTruth != "true":
            return clauseTruth
    return "true"

def tryAssignments(assignment, nextVal, wff):
    global count
    count += 1
    #if count == 1 or count == 10 or not count % 100:
    #    print(f"tryAssignments({assignment}, {nextVal}, {numVars}, {wff}) #{count}")
    if verify(assignment, wff, nextVal) == "false":
        return [None, None]
    if verify(assignment, wff, nextVal) == "true":
        return [assignment, nextVal]
    answer, val_len = tryAssignments(assignment, nextVal + 1, wff)
    if answer:
        return [answer, val_len]
    answer, val_len = tryAssignments(assignment | 1 << (nextVal - 1), nextVal + 1, wff)
    if answer:
        return [answer, val_len]

    return [None, None]


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
    #print(wff)
    startTime = time.time() * (10**6)
    values, vals_used = tryAssignments(0, 1, wff)
    if values:
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

    if values:
        values = str(bin(values))[::-1]
        values = [x for x in values][:-2]
        for i in range(vals_used, len(values)):
            values[i] = -1
        ','.join(values)
    # output
    execTime = endTime - startTime
    outputarr = [problemNum, maxLiterals, totalLiterals, satisfiable, rightAns, execTime]
    if values:
        outputarr.extend(values)
    output([x for x in outputarr])

    # returning the next 'c' line back to readFile
    return ' '.join(line)

def readFile(fileName):
    file = open(fileName, 'r')
    line = file.readline()
    i = 0
    while line and i < 40:
        if line[0] == 'c':
            line = readWFF(line, file)
        i += 1

    file.close()
    f.close()


def main():
    readFile(sys.argv[1])

if __name__ == "__main__":
    main()
