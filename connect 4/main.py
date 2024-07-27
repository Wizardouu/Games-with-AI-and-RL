import pygame as py
import numpy as np
import math
import random
import numpy as np
import sys

BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
num_col = 7
num_row = 6
# yellow_piece is the computer player
# red_piece is human player
red_piece = 1
yellow_piece = 2


class State:
    def __init__(self, board):  # pass board
        self.turn = None
        self.board = board
        self.children = []
        self.parent = None  # parent should alos be a class state
        self.state_depth = 0
        self.max_utility = None
        self.max_child = None
        self.min_utility = None
        self.min_child = None

    def set_parent(self, parent):
        self.parent = parent
        self.parent.children.append(self)
        self.state_depth = self.parent.state_depth + 1


class TreeNode:
    def __init__(self, *data):
        self.data = list(data)
        self.children = []

    def print_tree(self):
        print(self.data)
        if self.children:
            for child in self.children:
                self.print_tree()


def available_moves(board):
    arr = []
    transpose = np.transpose(board)
    for i in range(len(transpose)):
        if (np.any(transpose[i] == 0)):
            arr.append(i)
    print(arr)
    return arr


def simulate_move(board, col, player):
    new_board = np.copy(board)  # Create a copy of the original board
    for row in range(len(new_board) - 1, -1, -1):
        if new_board[row][col] == 0:
            new_board[row][col] = player
            break
    return new_board


def evaluate_move(board, col, player, sequence_length):
    new_board = simulate_move(board, col, player)
    red_score = 0
    yellow_score = 0

    rows, cols = len(new_board), len(new_board[0])

    # Check rows
    for i in range(rows):
        row = new_board[i]
        for j in range(cols - sequence_length + 1):
            if row[j] == player and all(row[j + k] == player for k in range(1, sequence_length)):
                if player == red_piece:
                    red_score += 1
                elif player == yellow_piece:
                    yellow_score += 1

    # Check columns
    for j in range(cols):
        col = new_board[:, j]
        for i in range(rows - sequence_length + 1):
            if col[i] == player and all(col[i + k] == player for k in range(1, sequence_length)):
                if player == red_piece:
                    red_score += 1
                elif player == yellow_piece:
                    yellow_score += 1

    # Check diagonals (top-left to bottom-right)
    for i in range(rows - sequence_length + 1):
        for j in range(cols - sequence_length + 1):
            diagonal = [new_board[i + k][j + k] for k in range(sequence_length)]
            if diagonal[0] == player and all(diagonal[k] == player for k in range(1, sequence_length)):
                if player == red_piece:
                    red_score += 1
                elif player == yellow_piece:
                    yellow_score += 1

    # Check diagonals (top-right to bottom-left)
    for i in range(rows - sequence_length + 1):
        for j in range(sequence_length - 1, cols):
            diagonal = [new_board[i + k][j - k] for k in range(sequence_length)]
            if diagonal[0] == player and all(diagonal[k] == player for k in range(1, sequence_length)):
                if player == red_piece:
                    red_score += 1
                elif player == yellow_piece:
                    yellow_score += 1

    return red_score if player == red_piece else yellow_score

def best_move(board, sequence_length, player):
    moves = available_moves(board)
    scores = [evaluate_move(board, col, player, sequence_length) for col in moves]
    #print(scores)
    if(len(scores)==0):
        for k in range(num_col):
            if(avaible_col(board,k)==1):
                return k
    best_score = max(scores)
    best_moves = [moves[i] for i in range(len(moves)) if scores[i] == best_score]
    return best_moves[0]


def heuristic(board, player):
    if (player == 1):
        return best_move(board, 2, 1)
    else:
        for col in available_moves(board):
            if evaluate_move(board, col, 1, 4) > 0:
                return col
        return best_move(board, 2, 2)


def generate_children(state, player):
    for i in range(num_col):
        print("i", i)
        cols = available_moves(state.board)
        for col in cols:
            new_board = simulate_move(board, col, player)
            child = State(np.copy(new_board))
            child.turn = player
            child.set_parent(state)




import numpy as np

def avaible_col(board, col):
    # Check if there is a zero in the entire column
    if np.any(board[:, col] == 0):
        return 1
    else:
        return -1



def add_piece(board, col, piece):
    indices = np.where(board[col] == 0)
    if len(indices[0]) > 0:
        row = indices[0]
    else:
        return
    board[row][col] = piece


def maximize(board, depth, player):
    # either the board is full or the level == k
    if check_full(board):
        hn = heuristic(board, player)
        return board, hn
    elif depth == 0:
        winner, red, yellow = check_wining(board)
        return board, yellow - red

    max_child = None
    max_utility = -sys.maxsize

    children = available_moves(board)

    for child_col in children:
        child = simulate_move(board, child_col, player)
        _, utility = minimize(child, depth - 1, red_piece)
        if utility > max_utility:
            max_child = child
            max_utility = utility

    return max_child, max_utility


def minimize(board, depth, player):
    if check_full(board):
        hn = heuristic(board, player)
        return board, hn
    elif depth == 0:
        winner, red, yellow = check_wining(board)
        return board, yellow - red

    min_child = None
    min_utility = sys.maxsize
    children = available_moves(board)

    for child_col in children:
        child = simulate_move(board, child_col, player)
        _, utility = maximize(child, depth - 1, yellow_piece)
        if utility < min_utility:
            min_child = child
            min_utility = utility
    return min_child, min_utility


def maximize_pruning(board, alpha, beta, depth, player):
    if check_full(board):
        hn = heuristic(board, player)
        return board, hn
    elif depth == 0:
        winner, red, yellow = check_wining(board)
        return board, yellow - red

    max_child = None
    max_utility = -sys.maxsize

    children = available_moves(board)

    for child_col in children:
        child = simulate_move(board, child_col, player)
        _, utility = minimize_pruning(child, alpha, beta, depth - 1, red_piece)
        if utility > max_utility:
            max_child = child
            max_utility = utility
        alpha = max(alpha, max_utility)
        if alpha >= beta:
            break  # Beta cut-off# TODO TREE PRUNE
    return max_child, max_utility


def minimize_pruning(board, alpha, beta, depth, player):
    if check_full(board):
        hn = heuristic(board, player)
        return board, hn
    elif depth == 0:
        winner, red, yellow = check_wining(board)
        return board, yellow - red

    min_child = None
    min_utility = sys.maxsize
    children = available_moves(board)

    for child_col in children:
        child = simulate_move(board, child_col, player)
        _, utility = maximize_pruning(child, alpha, beta, depth - 1, yellow_piece)
        if utility < min_utility:
            min_child = child
            min_utility = utility
        beta = min(beta, min_utility)
        if beta <= alpha:
            break  # Alpha cut-off TODO TREE PRUNE
    return min_child, min_utility


import math

def expecti_maximize(board, depth, player):
    if check_full(board):
        hn = heuristic(board, yellow_piece)
        return board, hn
    elif depth == 0:
        winner, red, yellow = check_wining(board)
        return board, yellow - red

    max_child = None
    max_chance = -math.inf

    children = available_moves(board)

    for i in children:
        child_state = simulate_move(board, i, player)
        chance = 0

        if i == 0:
            _, c0 = expecti_minimize(child_state, depth - 1, player)
            if avaible_col(board, i + 1) != -1:
                next_child = simulate_move(board, i + 1, player)
                _, c1 = expecti_minimize(next_child, depth - 1, player)
                chance = 0.4 * c1 + 0.6 * c0
            else:
                chance = c0

        elif i == 6:
            _, c6 = expecti_minimize(child_state, depth - 1, player)
            if avaible_col(board, i - 1) != -1:
                prev_child = simulate_move(board, i - 1, player)
                _, c5 = expecti_minimize(prev_child, depth - 1, player)
                chance = 0.4 * c5 + 0.6 * c6
            else:
                chance = c6

        elif i in [1, 2, 3, 4, 5]:
            _, c = expecti_minimize(child_state, depth - 1, player)
            c1, c2 = None, None
            if avaible_col(board, i + 1) != -1:
                next_child = simulate_move(board, i + 1, player)
                _, c1 = expecti_minimize(next_child, depth - 1, player)
            if avaible_col(board, i - 1) != -1:
                prev_child = simulate_move(board, i - 1, player)
                _, c2 = expecti_minimize(prev_child, depth - 1, player)

            if c1 and c2:
                chance = 0.2 * c1 + 0.6 * c + 0.2 * c2
            elif c1:
                chance = 0.4 * c1 + 0.6 * c
            elif c2:
                chance = 0.4 * c2 + 0.6 * c
            else:
                chance = c

        if chance > max_chance:
            max_child = child_state
            max_chance = chance

    return max_child, max_chance


import sys

def expecti_minimize(board, depth, player):
    if check_full(board):
        winner, red, yellow = check_wining(board)
        return board, yellow - red
    elif depth == 0:
        hn = heuristic(board, yellow_piece)
        return board, hn

    min_child = None
    min_chance = sys.maxsize

    children = available_moves(board)

    for i in children:
        child_state = simulate_move(board, i, player)
        chance = 0

        if i == 0:
            _, c0 = expecti_maximize(child_state, depth - 1, player)
            if avaible_col(board, i + 1) != -1:
                next_child = simulate_move(board, i + 1, player)
                _, c1 = expecti_maximize(next_child, depth - 1, player)
                chance = 0.4 * c1 + 0.6 * c0
            else:
                chance = c0

        elif i == 6:
            _, c6 = expecti_maximize(child_state, depth - 1, player)
            if avaible_col(board, i - 1) != -1:
                prev_child = simulate_move(board, i - 1, player)
                _, c5 = expecti_maximize(prev_child, depth - 1, player)
                chance = 0.4 * c5 + 0.6 * c6
            else:
                chance = c6

        elif i in [1, 2, 3, 4, 5]:
            _, c = expecti_maximize(child_state, depth - 1, player)
            c1, c2 = None, None
            if avaible_col(board, i + 1) != -1:
                next_child = simulate_move(board, i + 1, player)
                _, c1 = expecti_maximize(next_child, depth - 1, player)
            if avaible_col(board, i - 1) != -1:
                prev_child = simulate_move(board, i - 1, player)
                _, c2 = expecti_maximize(prev_child, depth - 1, player)

            if c1 and c2:
                chance = 0.2 * c1 + 0.6 * c + 0.2 * c2
            elif c1:
                chance = 0.4 * c1 + 0.6 * c
            elif c2:
                chance = 0.4 * c2 + 0.6 * c
            else:
                chance = c

        if chance < min_chance:
            min_child = child_state
            min_chance = chance

    return min_child, min_chance


def create_board():
    board = np.zeros((6, 7))
    return board


def print_board(board):
    for i in range(6):
        print(board[i])
    print("******************************")


def draw_board(board):
    for c in range(7):
        for r in range(6):
            py.draw.rect(screen, BLUE, (c * 100, r * 100 + 100, 100, 100))
            py.draw.circle(screen, WHITE, (int(c * 100 + 50), int(r * 100 + 150)), 45)


def update(col, board, top_position, turn):
    if (top_position[col] == 50):
        return turn, board
    row = top_position[col] // 100 - 1
    if (turn % 2 == 0):
        py.draw.circle(screen, RED, (int(col * 100 + 50), top_position[col]), 45)
        board[row][col] = 1
    else:
        print("row", int(col * 100 + 50) // 700)
        print("column", col)
        py.draw.circle(screen, YELLOW, (int(col * 100 + 50), top_position[col]), 45)
        board[row][col] = 2
    top_position[col] = top_position[col] - 100
    turn = turn + 1
    return turn, board


def check_full(board):
    if (np.any(board == 0)):
        return
    else:
        check_wining(board)

def draw_buttons():
    button_font = py.font.Font('freesansbold.ttf', 24)
    button_spacing = 30
    button_width = 250
    button_height = 50
    buttons = ["MinMax", "MinMax Pruning", "Expected Minimax"]
    for i, button_text in enumerate(buttons):
        button_x = screen.get_width() - button_width - 20
        button_y = i * (button_height + button_spacing) + 20
        button_rect = py.Rect(button_x, button_y, button_width, button_height)
        py.draw.rect(screen, BLACK, button_rect)
        text = button_font.render(button_text, True, WHITE)
        text_rect = text.get_rect(center=button_rect.center)
        screen.blit(text, text_rect)
        # Store button rectangle and text for event handling
        buttons[i] = (button_rect, button_text)
    return buttons

def check_wining(board):
    red = 0
    yellow = 0
    for i in range(len(board)):
        row = board[i]
        for k in range(4):
            if (row[k] == row[k + 1] == row[k + 2] == row[k + 3]):
                if (row[k] == 1):
                    red = red + 1
                elif (row[k] == 2):
                    yellow = yellow + 1
    transpose = np.transpose(board)
    for i in range(len(transpose)):
        column = transpose[i]
        for k in range(3):
            if (column[k] == column[k + 1] == column[k + 2] == column[k + 3]):
                if (column[k] == 1):
                    red = red + 1
                elif (column[k] == 2):
                    yellow = yellow + 1
    for i in range(3):
        for j in range(4):
            if (board[i][j] == board[i + 1][j + 1] == board[i + 2][j + 2] == board[i + 3][j + 3]):
                if (board[i][j] == 1):
                    red = red + 1
                elif (board[i][j] == 2):
                    yellow = yellow + 1
    for i in range(3, 6):
        for j in range(4):
            if (board[i][j] == board[i - 1][j + 1] == board[i - 2][j + 2] == board[i - 3][j + 3]):
                if (board[i][j] == 1):
                    red = red + 1
                elif (board[i][j] == 2):
                    yellow = yellow + 1
    print("win red", red)
    print("win yellow", yellow)
    if (red > yellow):
        return "R", red, yellow
    else:
        return "Y", red, yellow


def get_change(board1, board2):
    diff_elements = board1 != board2
    if np.sum(diff_elements) == 1:
        indices = np.argwhere(diff_elements)
        return indices[0][1]
    else:
        return None


board = create_board()
game_over = False
turn = 0
py.init()
screen = py.display.set_mode((1000, 700))
screen.fill(WHITE)
draw_board(board)
buttons = draw_buttons()
py.display.set_caption("Connect Four")
running = True
top_position = [650] * 7
font = py.font.Font('freesansbold.ttf', 32)
text1 = font.render('Red Turn', True, RED, WHITE)
text1_rect = text1.get_rect(center=(700 // 2, 25))
text2 = font.render('Yellow Turn', True, YELLOW, WHITE)
text2_rect = text2.get_rect(center=(700 // 2, 25))
text1_rect.center = (700 // 2, 25)
text2_rect.center = (700 // 2, 25)
screen.blit(text1, text1_rect)
visited = []
visited_nodes = []
while running:
    for event in py.event.get():
        if event.type == py.QUIT:
            running = False
        if event.type == py.MOUSEBUTTONDOWN:
            posx, posy = py.mouse.get_pos()
            posx = event.pos[0]
            if (turn % 2 == 0):
                col = posx // 100
            else:
                for button_rect, button_text in buttons:
                    if button_rect.collidepoint(posx, posy):
                        print(f"Clicked on {button_text} button")
                        # Handle button click events here
                        if button_text == "MinMax":
                            new_board, max_utility = maximize(board, 5, 2)
                        elif button_text == "MinMax Pruning":
                            new_board, max_utility = maximize_pruning(board, -math.inf, math.inf, 7, 2)
                        elif button_text == "Expected Minimax":
                            new_board, max_utility = expecti_maximize(board, 3, 2)
                col = get_change(board, new_board)
                if(turn == 1):
                    col = random.randint(0,6)
            turn, board = update(col, board, top_position, turn)
            #print_board(board)
            if (turn % 2 == 0):
                py.draw.rect(screen, WHITE, text2_rect)
                screen.blit(text1, text1_rect)
            else:
                screen.blit(text2, text2_rect)
            check_full(board)
    py.display.update()
