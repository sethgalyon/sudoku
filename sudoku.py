import random
import re

def shift(x,n):
    return x[n:] + x[:n]

def randomize_screen(difficulty, working_board, solved_board, writeable_cells):
    for p in range(len(working_board)):
        for o in range(len(working_board)):
            working_board[o][p] = ' '
            writeable_cells[o][p] = ' '
    
    b = [1,2,3,4,5,6,7,8,9]
    random.shuffle(b)
    for y in range(len(working_board)):
        working_board[0][y] = b[y]
        
    p = 1
    c = shift(b,3)
    while True:
        for y in range(len(working_board)):
            working_board[p][y] = c[y]
        p = p + 1
        if p == 9:
            break
        elif p == 3 or p == 6:
            c = shift(c,1)
        else:
            c = shift(c,3)
    
    if random.getrandbits(1) == 1:
        for y in range(len(working_board)):
            c[y] = working_board[y][0]
                
        p = 1
        c = shift(c,3)
        while True:
            for y in range(len(working_board)):
                working_board[y][p] = c[y]
            p = p + 1
            if p == 9:
                break
            elif p == 3 or p == 6:
                c = shift(c,1)
            else:
                c = shift(c,3)
    else:
        for y in range(len(working_board)):
            c[y] = working_board[0][y]
            
        p = 1
        c = shift(c,3)
        while True:
            for y in range(len(working_board)):
                working_board[p][y] = c[y]
            p = p + 1
            if p == 9:
                break
            elif p == 3 or p == 6:
                c = shift(c,1)
            else:
                c = shift(c,3)
    
    for solved_boardcol in range(9):
        for solved_boardrow in range(9):
            solved_board[solved_boardrow][solved_boardcol] = \
                working_board[solved_boardrow][solved_boardcol]
    
    p = 0
    while True:
        if p == 9:
            break
        random.shuffle(b)
        for i in range(difficulty):
            index = b[i] - 1
            working_board[p][index] = ' '
            writeable_cells[p][index] = 1
        p = p + 1

def print_screen(board):
    print('\n    A   B   C   D   E   F   G   H   I\n')
    for i, row in enumerate(board):
        print(f'{i+1}   {row[0]}   {row[1]}   {row[2]} | '\
                      f'{row[3]}   {row[4]}   {row[5]} | '\
                      f'{row[6]}   {row[7]}   {row[8]}')
        if i == 2 or i == 5:
            print('   --- --- --- --- --- --- --- --- ---')
    print()

def parse_input(input):
    cell = ()
    num = None
    message = 'Invalid input. Type the column, row, and a space followed by '\
              'the number desired. (ex. A2 9) \n'

    valid_input = re.match(r'([A-I])([1-9])\s+([1-9])\s*$', input.upper())

    if valid_input:
        cell = (int(valid_input[2]) - 1, ord(valid_input[1]) - 65)
        num = int(valid_input[3])
        message = ''

    return {'cell': cell, 'number': num, 'message': message}

def confirm_board(board):
    rows = {i: [] for i in range(len(board))}
    columns = {i: [] for i in range(len(board))}
    boxes = {i: [] for i in range(len(board))}
    
    for row in range(len(board)):
        for column in range(len(board)):
            if board[row][column] == '.':
                continue
            elif board[row][column] in rows[row] or \
                board[row][column] in columns[column] or \
                board[row][column] in boxes[row // 3 + (column // 3) * 3]:
                return False
            else:
                rows[row].append(board[row][column])
                columns[column].append(board[row][column])
                boxes[row // 3 + (column // 3) * 3].append(board[row][column])
    
    return True

def play_sudoku():
    working_board   = [[' ' for _ in range(9)] for _ in range(9)]
    solved_board    = [[' ' for _ in range(9)] for _ in range(9)]
    writeable_cells = [[' ' for _ in range(9)] for _ in range(9)]

    difficulty = input('\nPlease choose a difficulty (easy, medium, hard):')
    if difficulty == 'easy' or difficulty == 'e':
        difficulty = 5
    elif difficulty == 'medium' or difficulty == 'm':
        difficulty = 6
    elif difficulty == 'hard' or difficulty == 'h':
        difficulty = 7
    elif difficulty == 'quit' or difficulty == 'q':
        print('\nThanks for Playing!')
        return
    else:
        print("\nInvalid difficulty. Please re-enter difficulty (type 'quit' to quit).")
        play_sudoku()
        return

    randomize_screen(difficulty, working_board, solved_board, writeable_cells)
    
    print_screen(working_board)

    helpmessage = "Type 'done'  to calculate board.\nType 'reset' to reset.\nType "\
                  "'quit'  to quit the game.\nType 'help'  to show this message again.\n"
    print('Type the column, row, and a space followed by the number desired. '\
          '(ex. A2 9)\n' + helpmessage)
    
    while True:
        prompt = input('Input cell index and number desired (ex. A2 9):')
        if prompt == 'quit' or prompt == 'q':
            print('\nThanks for playing!')
            break
        elif prompt == 'help' or prompt == 'h':
            print_screen(working_board)
            print(helpmessage)
            continue
        elif prompt == 'backdoor':
            print_screen(solved_board)
            print('Solution displayed.')
            print_screen(working_board)
            continue
        elif prompt == 'reset' or prompt == 'r':
            play_sudoku()
            break
        elif prompt == 'done' or prompt == 'd':
           if not confirm_board(working_board):
                print('\nPuzzle Not Correct! Try Again.')
                print_screen(working_board)
                continue
           else:
               print('\nCongratulations! The Puzzle is Correct!\n')
               again = input("Play Again? ('yes' to play again):")
               if again == 'yes' or again == 'y':
                   play_sudoku()
                   break
               print('\nThanks for Playing!')
               break
        
        result = parse_input(prompt)
        cell = result['cell']
        number = result['number']
        message = result['message']
        if cell and number:
            rowno, colno = cell
            if writeable_cells[rowno][colno] != 1:
                print("\nCan't change initial number. Try Again.")
                print_screen(working_board)
                continue
            
            working_board[rowno][colno] = number
        
        print_screen(working_board)
        
        if message != '':
            print(message)

if __name__ == '__main__':
    play_sudoku()