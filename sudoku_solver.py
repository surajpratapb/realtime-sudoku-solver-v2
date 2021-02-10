def sudoku(f):

    def boardSetup(g):
        for n, row in enumerate(g):
            for m, column in enumerate(row):
                print(str(column).replace("0", "."), end="")  # replace 0 with . 
                if m in {2, 5}:
                    print("+", end="")  # +'s to make the grids
            print()
            if n in {2, 5}:
                print("+" * 11)

    def isValid(q, s):
        row = set(s[q[0]])
        row |= {s[i][q[1]] for i in range(9)}
        # this can also be written as..
        '''
        x = q[1]
        for i in range(9):
             new_item = s[i][x]
             row.add(new_item)
        
        '''

        subGridX, subGridY = q[0] // 3, q[1] // 3  # floored division to find top-right most part of the subgrid
        for i in range(3):
            row |= set(s[subGridX * 3 + i][subGridY * 3:(subGridY + 1) * 3])
        return set(range(1, 10)) - row

    def ec(row):
        q = set(row) - {0}
        for column in q:
            if row.count(column) != 1:
                return True
        return False

    boardSetup(f)

    s = []
    table = []
    for no_ofRows, row in enumerate(f):
        try:
            n = list(map(int, row))
        except:
            print("The Row " + str(no_ofRows + 1) + " contains something other than a number")
            return
        if len(n) != 9:
            print("The Row " + str(no_ofRows + 1) + " does not contain 9 digits.")

            return
        table += [[no_ofRows, i] for i in range(9) if n[i] == 0]
        s.append(n)
    if no_ofRows != 8:
        print("The Sudoku contains" + str(no_ofRows + 1) + " rows instead of 9.")
        return

    for row in range(9):
        if ec(s[row]):
            print("The Row " + str(row + 1) + " contradicts")
            return
    for column in range(9):
        k = [s[row][column] for row in range(9)]
        if ec(k):
            print("The Column " + str(column + 1) + " contradicts")
            return
    for row in range(3):
        for column in range(3):
            q = []
            for i in range(3):
                q += s[row * 3 + i][column * 3:(column + 1) * 3]
            if ec(q):
                print("The Cell (" + str(row + 1) + ";" +
                  str(column + 1) + ") contradicts.")
                return

    board = [[] for i in table]
    cr = 0

    while cr < len(table):
        board[cr] = isValid(table[cr], s)
        try:
            while not board[cr]:
                s[table[cr][0]][table[cr][1]] = 0
                cr -= 1
        except:
            print("Sudoku has no solution")
            return
        s[table[cr][0]][table[cr][1]] = board[cr].pop()
        cr += 1

    boardSetup(s)
    return(s)
