#!/usr/bin/env python3

import sys
import csv
import time
import datetime

count = 0

f = open('./CSV/backtrack_heuristic_kSATu.csv', 'w')
writer = csv.writer(f)

def output(args):
    writer.writerow(args)


def verify(i, wff, vals_used):
    unknown = False
    for clause in wff:
        clauseTruth = "false"
        for num in clause:
            if (vals_used >> (abs(num) - 1)) & 1:
                if num < 0:
                    if not ((i >> (abs(num) - 1)) & 1):
                        if not unknown:
                            clauseTruth = "true"
                            break
                        else:
                            clauseTruth = "unknown"
                if num > 0:
                    if ((i >> (abs(num) - 1)) & 1):
                        if not unknown:
                            clauseTruth = "true"
                            break
                        else:
                            clauseTruth = "unknown"
            else:
                clauseTruth = "unknown"
                unknown = True
        if clauseTruth == "false":
            return clauseTruth
    return clauseTruth

def tryAssignments(assignment, wff, check_other, cur_val, vals_used, counts):

    verified = verify(assignment, wff, vals_used)
    if verified == "true":
        return [assignment, vals_used]
    elif verified == "unknown":
        max_index = 0
        max_val = 0
        for i in range(len(counts)):
            if ((vals_used >> i) ^ 1) & 1:
                if counts[i] > max_val:
                    max_index = i + 1
                    max_val = counts[i]
        vals_used_now = vals_used | (1 << (max_index - 1))
        answer, answers_used = tryAssignments(assignment, wff, True, max_index, vals_used_now, counts)
        if answer:
            return [answer, answers_used]
    if check_other:
        answer, answers_used = tryAssignments(assignment | (1 << (cur_val - 1)), wff, False, cur_val, vals_used, counts)
        if answer:
            return [answer, answers_used]
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

    line = file.readline().split(",")
    wff = []
    totalLiterals = 0
    while line != [''] and line[0][0] != 'c':
        line.pop()
        for num in line:
            totalLiterals += 1
        line = list(map(int, line))
        wff.append(line)
        line = file.readline().split(",")

    startTime = time.time() * (10**6)
    counts = [0] * int(numVars)
    for clause in wff:
        for num in clause:
            counts[abs(num) - 1] += 1

    cur_val = counts.index(max(counts)) + 1
    vals_used = 0 | 1 << (cur_val - 1)

    values, vals_known = tryAssignments(0, wff, True, cur_val, vals_used, counts)

    if values:
        satisfiable = 'S'
    else:
        satisfiable = 'U'
    endTime = time.time() * (10**6)

    if satisfiableAns == "?":
        rightAns = 0
    else:
        if satisfiableAns == satisfiable:
            rightAns = 1
        else:
            rightAns = -1

    if values:
        values = str(bin(values))[::-1]
        values = [int(x) for x in values[:-2]]
        for i in range(len(values)):
            if not (vals_known >> i) & 1:
                values[i] = -1

    # output
    execTime = endTime - startTime
    outputarr = [problemNum, numVars, numClauses, maxLiterals, totalLiterals, satisfiable, rightAns, execTime]
    if values:
        outputarr.extend(values)
    output([x for x in outputarr])

    # returning the next 'c' line back to readFile
    return ' '.join(line)

def readFile(fileName):
    file = open(fileName, 'r')
    line = file.readline()
    i = 0
    while line:
        print(f"WFF #{i + 1}: {datetime.datetime.now()}")
        if line[0] == 'c':
            line = readWFF(line, file)
        i += 1

    file.close()
    f.close()


def main():
    readFile(sys.argv[1])

if __name__ == "__main__":
    main()
