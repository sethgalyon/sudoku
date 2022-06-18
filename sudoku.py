from random import shuffle
import re


def valid_num(board, row, col, num):
    if num in board[row]:
        return False

    for i in range(9):
        if board[i][col] == num:
            return False

    box_row = (row // 3) * 3
    box_col = (col // 3) * 3
    for i in range(box_row, (box_row + 3)): 
        for j in range(box_col, (box_col + 3)): 
            if board[i][j] == num: 
                return False

    return True


def empty_cell_exists(board):
    for row in board:
        if 0 in row:
            return True

    return False


def generate_board(board):
    nums = [1,2,3,4,5,6,7,8,9]
    for i in range(0, 81):
        row = i // 9
        col = i % 9
        if board[row][col] == 0:
            shuffle(nums)
            for num in nums:
                if valid_num(board, row, col, num):
                    board[row][col] = num
                    if not empty_cell_exists(board):
                        return True
                    elif generate_board(board):
                        return True
            break

    board[row][col] = 0
    return False


def remove_cells(board, writeable_cells, difficulty):
    row = 0
    nums = [0,1,2,3,4,5,6,7,8]
    while row < 9:
        shuffle(nums)
        for i in range(difficulty):
            col = nums[i]
            board[row][col] = ' '
            writeable_cells[row][col] = 1

        row += 1


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

    valid_input = re.match(r'([A-I])([1-9])\s+([1-9])\s*$', input.upper())

    if valid_input:
        cell = (int(valid_input[2]) - 1, ord(valid_input[1]) - 65)
        num = int(valid_input[3])

    return {'cell': cell, 'num': num}


def confirm_board(board):
    rows = {i: [] for i in range(len(board))}
    columns = {i: [] for i in range(len(board))}
    boxes = {i: [] for i in range(len(board))}
    for row in range(len(board)):
        for col in range(len(board)):
            if board[row][col] == '.':
                continue
            elif board[row][col] in rows[row] or \
                board[row][col] in columns[col] or \
                board[row][col] in boxes[row // 3 + (col // 3) * 3]:
                return False
            else:
                rows[row].append(board[row][col])
                columns[col].append(board[row][col])
                boxes[row // 3 + (col // 3) * 3].append(board[row][col])

    return True


def play_sudoku():
    board = [[0 for _ in range(9)] for _ in range(9)]
    writeable_cells = [[0 for _ in range(9)] for _ in range(9)]

    difficulty = input('\nPlease choose a difficulty (easy, medium, hard):')
    if difficulty == 'easy' or difficulty == 'e':
        difficulty = 5
    elif difficulty == 'medium' or difficulty == 'm':
        difficulty = 6
    elif difficulty == 'hard' or difficulty == 'h':
        difficulty = 7
    elif difficulty == 'quit' or difficulty == 'q':
        print('\nThanks for Playing!\n')
        return
    else:
        print("\nInvalid difficulty. Please re-enter difficulty or type 'quit' to quit.")
        play_sudoku()
        return

    generate_board(board)

    remove_cells(board, writeable_cells, difficulty)

    print_screen(board)

    helpmessage = "Type 'done'  to calculate board.\nType 'reset' to reset.\nType "\
                  "'quit'  to quit the game.\nType 'help'  to show this message again.\n"
    print('Type the column, row, and a space followed by the number desired. '\
          '(ex. A2 9)\n' + helpmessage)
    
    while True:
        prompt = input('Input cell index and number desired (ex. A2 9):')
        if prompt == 'quit' or prompt == 'q':
            print('\nThanks for playing!\n')
            break
        elif prompt == 'help' or prompt == 'h':
            print_screen(board)
            print(helpmessage)
            continue
        elif prompt == 'reset' or prompt == 'r':
            play_sudoku()
            break
        elif prompt == 'done' or prompt == 'd':
           if not confirm_board(board):
                print('\nPuzzle Not Correct! Try Again.')
                print_screen(board)
                continue
           else:
                print('\nCongratulations! The Puzzle is Correct!\n')
                prompt = input("Play Again? ('yes' to play again):")
                if prompt == 'yes' or prompt == 'y':
                    play_sudoku()
                    break
                print('\nThanks for Playing!\n')
                break
        
        result = parse_input(prompt)
        cell = result['cell']
        num = result['num']
        if cell and num:
            row, col = cell
            if writeable_cells[row][col] != 1:
                print("\nCan't change initial number. Try Again.")
            else:
                board[row][col] = num
            print_screen(board)
        else:
            print_screen(board)
            print('Invalid input. Type the column, row, and a space followed by '\
                  'the number desired. (ex. A2 9) \n')


if __name__ == '__main__':
    play_sudoku()