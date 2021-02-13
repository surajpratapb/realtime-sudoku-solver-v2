def sudoku(f):

    # Step1 : setting up board with .'s in places of 0 +'s to show edges of subgrids
    def boardsetup(g):
        for n, row in enumerate(g):
            for m, column in enumerate(row):
                print(str(column).replace("0", "."), end="")  # replace 0 with . 
                if m in {2, 5}:
                    print("+", end="")  # +'s to make the grids
            print()
            if n in {2, 5}:
                print("+" * 11)

    # Step2 : Get values of all rows in the sudoku
    def isvalid(q, solved_sudoku):
        row = set(solved_sudoku[q[0]])
        row |= {solved_sudoku[i][q[1]] for i in range(9)}  # works same as a=a|b or a|=b
        # this can also be written as..
        '''
        x = q[1]
        for i in range(9):
             new_item = s[i][x]
             row.add(new_item)
        
        '''
    # Step3 : Check the number value in the subgrid
        subGridX, subGridY = q[0] // 3, q[1] // 3  # floored division to find top-right most part of the subgrid
        for i in range(3):
            row |= set(solved_sudoku[subGridX * 3 + i][subGridY * 3:(subGridY + 1) * 3])
        return set(range(1, 10)) - row

    def is_correct(row):
        q = set(row) - {0}
        for column in q:
            if row.count(column) != 1:
                return True
        return False

    boardsetup(f)

    solved_sudoku = []
    table = []

    # Accounting fot Exception & Edge Cases
    for no_ofrows , row in enumerate(f):
        try:
            n = list(map(int, row))
        except:
            print("The Row " + str(no_ofrows + 1) + " contains something other than a number")
            return
        if len(n) != 9:
            print("The Row " + str(no_ofrows + 1) + " does not contain 9 digits.")

            return
        table += [[no_ofrows, i] for i in range(9) if n[i] == 0]
        solved_sudoku.append(n)

    if no_ofrows != 8:
        print("The Sudoku contains" + str(no_ofrows + 1) + " rows instead of 9.")
        return

    for row in range(9):
        if is_correct(solved_sudoku[row]):
            print("The Row " + str(row + 1) + " contradicts")
            return

    for column in range(9):
        k = [solved_sudoku[row][column] for row in range(9)]
        if is_correct(k):
            print("The Column " + str(column + 1) + " contradicts")
            return

    for row in range(3):
        for column in range(3):
            q = []
            for i in range(3):
                q += solved_sudoku[row * 3 + i][column * 3:(column + 1) * 3]
            if is_correct(q):
                print("The Cell (" + str(row + 1) + ";" +
                  str(column + 1) + ") contradicts.")
                return

    board = [[] for i in table]
    cr = 0  # for traversing the new table

    # Step : Creating the final board
    while cr < len(table):
        board[cr] = isvalid(table[cr], solved_sudoku)
        try:
            while not board[cr]:
                solved_sudoku[table[cr][0]][table[cr][1]] = 0
                cr -= 1
        except:
            print("Sudoku has no solution")
            return
        solved_sudoku[table[cr][0]][table[cr][1]] = board[cr].pop()
        cr += 1

    boardsetup(solved_sudoku)
    return solved_sudoku
