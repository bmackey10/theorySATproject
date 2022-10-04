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
    line = file.readline().split()
    wff = []
    while line and line[0] != 'c':
        # UNSURE?: each wff will be stored like [[1, 2, 0], [2, -3, 0]]
        wff.append(line)
        line = file.readline().split()

    # for i in range(1<<numVars):


    # nextAssignment(numVars)

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