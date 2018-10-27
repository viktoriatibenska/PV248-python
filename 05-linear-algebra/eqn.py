import sys
import numpy as np
import re

def main(inputFile):
    f = open(inputFile, "r")
    A = []
    b = []
    variables = []
    rawValues = []

    # Parse input file
    for line in f:
        clean = line.split(" ")
        clean = map(str.strip, clean)
        clean = list(filter(None, clean))
        
        sign = 1
        equals = False
        row = {}
        for item in clean:
            if item == "=":
                equals = True
                sign = 1
            elif item == "-":
                sign = -1
            elif item == "+":
                sign = 1
            else:
                if not equals:
                    r = re.compile( r"([0-9]*)([a-z])" )
                    m = r.match(item)
                    if m is not None:
                        if m.group(2) not in variables:
                            variables.append(m.group(2))
                        if m.group(1) == '':
                            row[m.group(2)] = float(sign)
                        else:
                            row[m.group(2)] = sign * float(m.group(1))
                else:
                    b.append(sign * float(item))
        rawValues.append(row)

    variables.sort()
    for r in rawValues:
        a = []
        for v in variables:
            if v in r:
                a.append(r[v])
            else:
                a.append(0.0)
        A.append(a)

    # solve
    matrix = np.array(A)
    rightSide = np.array(b)
    augmentedMatrix = np.hstack((matrix, np.expand_dims(rightSide, axis=1)))
    matrixRank = np.linalg.matrix_rank(matrix)
    augmentedRank = np.linalg.matrix_rank(augmentedMatrix)
    if matrixRank != augmentedRank:
        print("no solution")
    elif matrixRank != len(variables):
        print("solution space dimension:", len(variables) - matrixRank)
    else:
        solution = np.linalg.solve(matrix, rightSide)
        output = ""
        for index, s in enumerate(solution):
            if index != 0:
                output += ", "
            output += variables[index] + " = " + str(s)
        print("solution: " + output)


if __name__ == "__main__":
    main(sys.argv[1])
