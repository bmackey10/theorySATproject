#!/usr/bin/env python3

import sys
import csv
import time

count = 0

f = open('./CSV/backtrack_heuristic.csv', 'w')
writer = csv.writer(f)

def output(*args):
    #args = list(args)
    #print(args)
    writer.writerow(args)


def verify(i, wff, vals_used):
    unknown = False
    for clause in wff:
        #print(clause, bin(i), vals_used)
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
            #print(f"{clauseTruth}\n")
            return clauseTruth
    #print(f"{clauseTruth}\n")
    return clauseTruth

def tryAssignments(assignment, wff, check_other, cur_val, vals_used, counts):
    #if count == 1 or count == 10 or not count % 100:
    #    print(f"tryAssignments({assignment}, {nextVal}, {numVars}, {wff}) #{count}")
    #print(f"Verifying {bin(assignment)} {bin(vals_used)}")
    verified = verify(assignment, wff, vals_used)
    if verified == "true":
        return [assignment, vals_used]
    elif verified == "unknown":
        max_index = 0
        max_val = 0
        for i in range(len(counts)):
            if ((vals_used >> i) ^ 1) & 1:
                #print(i)
                if counts[i] > max_val:
                    max_index = i + 1
                    #print(f"max_index = {max_index}")
                    max_val = counts[i]
        #print(vals_used)
        vals_used_now = vals_used | (1 << (max_index - 1))
        #print(vals_used)
        #print(f"Trying assignment {bin(assignment)} with vals_used {bin(vals_used)} and cur_val {cur_val} and max_index {max_index}")
        #if cur_val == 3:
        #    print(f"Line 66: {bin(assignment)}, {max_index}, {bin(vals_used)}, {check_other}")
        answer, answers_used = tryAssignments(assignment, wff, True, max_index, vals_used_now, counts)
        if answer:
            return [answer, answers_used]
        #if cur_val == 3:
        #    print(f"Line 71: {bin(assignment)}, {max_index} {bin(vals_used)}, {check_other}")
    if check_other:
        #print(f"Trying assignment {bin(assignment | 1 << (cur_val - 1))} with vals_used {bin(vals_used)} and cur_val {cur_val}")
        answer, answers_used = tryAssignments(assignment | (1 << (cur_val - 1)), wff, False, cur_val, vals_used, counts)
        #return [None, None]
        if answer:
            return [answer, answers_used]
    return [None, None]
    #answer, val_len = tryAssignments(assignment | 1 << (nextVal - 1), nextVal + 1, wff)
    #if answer:
    #    return [answer, val_len]


def readWFF(line, file):
    # c line
    line = line.split()
    #print(line)
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
    counts = [0] * int(numVars)
    for clause in wff:
        for num in clause:
            counts[abs(num) - 1] += 1
    #print(counts)
    cur_val = counts.index(max(counts)) + 1
    vals_used = 0 | 1 << (cur_val - 1)
    #print(bin(vals_used))
    #print(wff)
    values, vals_known = tryAssignments(0, wff, True, cur_val, vals_used, counts)
    #print(f"\nValue: {values}\n")
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
        values = [int(x) for x in values[:-2]]
        for i in range(len(values)):
            if not (vals_known >> i) & 1:
                values[i] = -1
        #','.join(values)
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
    while line and i < 30:
        if line[0] == 'c':
            line = readWFF(line, file)
        i += 1

    file.close()
    f.close()


def main():
    readFile(sys.argv[1])

if __name__ == "__main__":
    main()
