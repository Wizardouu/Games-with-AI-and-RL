from game import *
from gui import *
import random


def generate_random_board():
    init_board = ZERO_BOARD
    board_2d = [[int(char) for char in row] for row in init_board]
    rand_num = random.randint(0, 8)
    rand_row = random.randint(0, 8)
    rand_col = random.randint(0, 8)
    board_2d[rand_row][rand_col] = rand_num

    rand_num2 = random.randint(0, 8)
    rand_col2 = random.randint(0, 8)

    while rand_num2 == rand_num:
        rand_num2 = random.randint(0, 8)
    while rand_col2 == rand_col:
        rand_col2 = random.randint(0, 8)
    board_2d[0][rand_col2] = rand_num2
    
    game = SudokuGame(board_2d,"arc_consistency_log.txt")
    game.start()
    game.solve()
    board = game.puzzle
    print(board)
    indices = [(i, j) for i in range(9) for j in range(9)]
    random.shuffle(indices)
    num_to_remove = random.randint(40, 60)
    for _ in range(num_to_remove):
        i, j = indices.pop()
        board[i][j] = 0
    return board

