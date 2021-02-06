def sudoku(sudoku_values):

    def af(g):
        for n, l in enumerate(g):
            for m, c in enumerate(l):
                print(str(c).replace("0", "."), end="")   # Replacing 0 with .
                if m in {2, 5}:
                    print("+", end="")
            print()
            if n in {2, 5}:
                print("+" * 11)

    def cp(q, s):
        l = set(s[q[0]])
        l |= {s[i][q[1]] for i in range(9)}
        k = q[0] // 3, q[1] // 3
        for i in range(3):
            l |= set(s[k[0] * 3 + i][k[1] * 3:(k[1] + 1) * 3])
        return set(range(1, 10)) - l

    def ec(l):
        q = set(l) - {0}
        for c in q:
            if l.count(c) != 1:
                return True
        return False

    af(sudoku_values)

    s = []
    t = []
    for nl, l in enumerate(sudoku_values):
        try:
            n = list(map(int, l))
        except:
            print("Line " + str(nl + 1) + " contains something other than a number.")
            return
        if len(n) != 9:
            print("The line " + str(nl + 1) + " does not contain 9 digits.")
            return
        t += [[nl, i] for i in range(9) if n[i] == 0]
        s.append(n)
    if nl != 8:
        print("The board has " + str(nl + 1) + " instead of 9")
        return

    for l in range(9):
        if ec(s[l]):
            print("Line " + str(l + 1) + " contradicts.")
            return
    for c in range(9):
        k = [s[l][c] for l in range(9)]
        if ec(k):
            print("The Column " + str(c + 1) + " contradicts.")
            return
    for l in range(3):
        for c in range(3):
            q = []
            for i in range(3):
                q += s[l * 3 + i][c * 3:(c + 1) * 3]
            if ec(q):
                print("The Cell (" + str(l + 1) + ";" +
                  str(c + 1) + ") contradicts.")
                return

    p = [[] for i in t]
    cr = 0

    while cr < len(t):
        p[cr] = cp(t[cr], s)
        try:
            while not p[cr]:
                s[t[cr][0]][t[cr][1]] = 0
                cr -= 1
        except:
            print("Sudoku has no solution")
            return
        s[t[cr][0]][t[cr][1]] = p[cr].pop()
        cr += 1

    af(s)
    return(s)
