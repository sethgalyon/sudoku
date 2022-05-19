import random
import re
from string import ascii_uppercase
x = [[" "," "," "," "," "," "," "," "," "],[" "," "," "," "," "," "," "," "," "],[" "," "," "," "," "," "," "," "," "],[" "," "," "," "," "," "," "," "," "],[" "," "," "," "," "," "," "," "," "],[" "," "," "," "," "," "," "," "," "],[" "," "," "," "," "," "," "," "," "],[" "," "," "," "," "," "," "," "," "],[" "," "," "," "," "," "," "," "," "]]
xcopy = [[" "," "," "," "," "," "," "," "," "],[" "," "," "," "," "," "," "," "," "],[" "," "," "," "," "," "," "," "," "],[" "," "," "," "," "," "," "," "," "],[" "," "," "," "," "," "," "," "," "],[" "," "," "," "," "," "," "," "," "],[" "," "," "," "," "," "," "," "," "],[" "," "," "," "," "," "," "," "," "],[" "," "," "," "," "," "," "," "," "]]
indexing = [[" "," "," "," "," "," "," "," "," "],[" "," "," "," "," "," "," "," "," "],[" "," "," "," "," "," "," "," "," "],[" "," "," "," "," "," "," "," "," "],[" "," "," "," "," "," "," "," "," "],[" "," "," "," "," "," "," "," "," "],[" "," "," "," "," "," "," "," "," "],[" "," "," "," "," "," "," "," "," "],[" "," "," "," "," "," "," "," "," "]]

def shift(x,n):
    return x[n:] + x[:n]

def randomize_screen(diff):
    if diff == "easy" or diff == 'e':
        difficulty = 5
    elif diff == "medium" or diff == 'm':
        difficulty = 6
    elif diff == "hard" or diff == 'h':
        difficulty = 7
    elif diff == "quit" or diff == 'q':
        return 1
    else:
        return 0

    for p in range(0,len(x)):
        for o in range(0,len(x)):
            x[o][p] = " "
            indexing[o][p] = " "
    
    b = [1,2,3,4,5,6,7,8,9]
    random.shuffle(b)
    for y in range(0,len(x)):
        x[0][y] = b[y]
        
    p = 1
    c = shift(b,3)
    while True:
        for y in range(0,len(x)):
            x[p][y] = c[y]
        p = p + 1
        if p == 9:
            break
        elif p == 3 or p == 6:
            c = shift(c,1)
        else:
            c = shift(c,3)
    
    choice = random.getrandbits(1)
    if choice == 1:
        for y in range(0,len(x)):
            c[y] = x[y][0]
                
        p = 1
        c = shift(c,3)
        while True:
            for y in range(0,len(x)):
                x[y][p] = c[y]
            p = p + 1
            if p == 9:
                break
            elif p == 3 or p == 6:
                c = shift(c,1)
            else:
                c = shift(c,3)
    elif choice == 0:
        for y in range(0,len(x)):
            c[y] = x[0][y]
            
        p = 1
        c = shift(c,3)
        while True:
            for y in range(0,len(x)):
                x[p][y] = c[y]
            p = p + 1
            if p == 9:
                break
            elif p == 3 or p == 6:
                c = shift(c,1)
            else:
                c = shift(c,3)
    
    for xcopycol in range(0,9):
        for xcopyrow in range(0,9):
            xcopy[xcopyrow][xcopycol] = x[xcopyrow][xcopycol]
    
    p = 0
    while True:
        if p == 9:
            break
        random.shuffle(b)
        for i in range(0,difficulty):
            index = b[i] - 1
            x[p][index] = " "
            indexing[p][index] = 1
        p = p + 1
    
    return 2

def print_screen(y):
    print("\n    A   B   C   D   E   F   G   H   I")
    for i in range(1,10):
        print("%d   %s   %s   %s - %s   %s   %s - %s   %s   %s" % (i, y[i-1][0], y[i-1][1], y[i-1][2], y[i-1][3], y[i-1][4], y[i-1][5], y[i-1][6], y[i-1][7], y[i-1][8]))
        if i == 3 or i == 6:
            print("   --- --- --- --- --- --- --- --- ---")

def parseinput(inputstring, helpmessage):
    cell = ()
    number = 0
    message = "\nInvalid input. " + helpmessage

    pattern = r'([A-I])([0-9]+)( )([0-9]+)'
    validinput = re.match(pattern, inputstring)

    if validinput:
        rowno = int(validinput.group(2)) - 1
        colno = ascii_uppercase.index(validinput.group(1))
        number = int(validinput.group(4))
        message = ''

        if -1 < rowno < 9:
            cell = (rowno, colno)

    return {'cell': cell, 'number': number, 'message': message}

def confirm():
    try:
        wrong = 0
        answer = 0
        for rows in range(0,9):
            answer = 0
            for columns in range(0,9):
                answer = answer + x[rows][columns]
            if answer != 45:
                wrong = 1
                return wrong
            
        for columns in range(0,9):
            answer = 0
            for rows in range(0,9):
                answer = answer + x[rows][columns]
            if answer != 45:
                wrong = 1
                return wrong
            
        for boxes in (0,3,6):
            for boxes2 in (0,3,6):
                answer = 0
                for u in range(0,3):
                    for v in range(0,3):
                        answer = answer + x[boxes+u][boxes2+v]
                if answer != 45:
                    wrong = 1
                    return wrong
                
        return wrong
    except:
        wrong = 1
        return wrong

def play_sudoku():
    difficulty = input('\nPlease choose a difficulty (easy, medium, hard):')
    good = randomize_screen(difficulty)
    if good == 0:
        print("\nInvalid difficulty. Please re-enter difficulty (type quit to quit).")
        play_sudoku()
        return
    elif good == 1:
        print("\nThanks for Playing!")
        return
    
    helpmessage = "\nType 'done' to calculate board. Type 'reset' to reset and 'quit' to quit the game. Type 'help' to show this message again.\n"
    
    print_screen(x)
    
    print("Type the column, row, and a space followed by the number desired. (ex. A2 9)" + helpmessage)
    while True:
        prompt = input('Input cell index and number desired (ex. A2 9):')
        if prompt == "quit":
            print("\nThanks for playing!")
            break
        elif prompt == "help":
            print_screen(x)
            print(helpmessage)
            continue
        elif prompt == "backdoor":
            print_screen(xcopy)
            print("\nBackdoor solution verified")
            break
        elif prompt == "reset":
            play_sudoku()
            break
        elif prompt == "done":
           wrong = confirm()
           if wrong == 1:
               print("\nPuzzle Not Correct! Try Again.\n")
           elif wrong == 0:
               print("\nCongratulations! The Puzzle is Correct!\n")
               again = input("Play Again? ('yes' to play again):")
               if again == "yes":
                   play_sudoku()
                   break
               print("\nThanks for Playing!")
               break
           print_screen(x)
           continue
        
        result = parseinput(prompt, "Type the column, row, and a space followed by the number desired. (ex. A2 9) \n")
        cell = result['cell']
        number = result['number']
        message = result['message']
        if cell and number:
            rowno, colno = cell
            
            if indexing[rowno][colno] != 1:
                print("\nCan't change initial number. Try Again.")
                print_screen(x)
                continue
            
            print('\n\n')
            x[rowno][colno] = number
        
        print_screen(x)
        if message != "":
            print(message)
        
play_sudoku()