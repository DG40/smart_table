import time
import math
import random
from copy import deepcopy
from rpi_ws281x import *

import useful_box
from useful_box import battlefield as battlefield

PALETTE_1 = {
    'background': (0, 0, 0, 0),
    'checkers_my': (255, 0, 0, 0),
    'checkers_computer': (0, 0, 255, 0),
    'queens_my': (255, 0, 0, 50),
    'queens_computer': (0, 0, 255, 50)
}

PALETTE_2 = {
    'background': (0, 0, 0, 0),
    'checkers_my': (200, 200, 0, 0),
    'checkers_computer': (200, 0, 200, 0),
    'queens_my': (255, 255, 0, 50),
    'queens_computer': (255, 0, 255, 50)
}

PALETTES = (PALETTE_1, PALETTE_2)


class Node:
    def __init__(self, board, move=None, parent=None, value=None):
        self.board = board
        self.value = value
        self.move = move
        self.parent = parent

    def get_children(self, strip, minimizing_player, mandatory_jumping):
        current_state = deepcopy(self.board)
        children_states = []
        if minimizing_player is True:
            available_moves = Checkers.find_available_moves(strip, current_state, mandatory_jumping)
            big_letter = "C"
            queen_row = 7
        else:
            available_moves = Checkers.find_player_available_moves(current_state, mandatory_jumping)
            big_letter = "B"
            queen_row = 0
        if useful_box.FLAG_EXIT:
            return children_states
        for i in range(len(available_moves)):
            old_i = available_moves[i][0]
            old_j = available_moves[i][1]
            new_i = available_moves[i][2]
            new_j = available_moves[i][3]
            state = deepcopy(current_state)
            Checkers.make_a_move(state, old_i, old_j, new_i, new_j, big_letter, queen_row)
            children_states.append(Node(state, [old_i, old_j, new_i, new_j]))
        return children_states

    def set_value(self, value):
        self.value = value

    def get_value(self):
        return self.value

    def get_board(self):
        return self.board

    def get_parent(self):
        return self.parent

    def set_parent(self, parent):
        self.parent = parent


class Checkers:

    def __init__(self):
        rand_numb = random.randrange(len(PALETTES))
        palette = PALETTES[rand_numb]
        self.background_color = palette['background']
        self.checkers_my_color = palette['checkers_my']
        self.checkers_computer_color = palette['checkers_computer']
        self.queens_my_color = palette['queens_my']
        self.queens_computer_color = palette['queens_computer']
        self.matrix = [[], [], [], [], [], [], [], []]
        self.player_turn = True
        self.computer_pieces = 12
        self.player_pieces = 12
        self.available_moves = []
        self.mandatory_jumping = False
        for row in self.matrix:
            for i in range(8):
                row.append("---")
        self.position_computer()
        self.position_player()

    def position_computer(self):
        for i in range(3):
            for j in range(8):
                if (i + j) % 2 == 1:
                    self.matrix[i][j] = ("c" + str(i) + str(j))

    def position_player(self):
        for i in range(5, 8, 1):
            for j in range(8):
                if (i + j) % 2 == 1:
                    self.matrix[i][j] = ("b" + str(i) + str(j))

    def print_matrix(self, strip):
        i = 0
        print()
        for row in self.matrix:
            print(i, end="  |")
            i += 1
            for elem in row:
                if elem[0] == 'c':
                    print(useful_box.ANSI_CYAN + elem + useful_box.ANSI_RESET, end=" ")
                elif elem[0] == 'b':
                    print(useful_box.ANSI_YELLOW + elem + useful_box.ANSI_RESET, end=" ")
                else:
                    print(elem, end=" ")
            print()
        print()
        for j in range(8):
            if j == 0:
                j = "     0"
            print(j, end="   ")
        print("\n")
        for i in range(8):
            for j in range(8):
                if self.matrix[i][j][0] == 'b':
                    battlefield[i][j] = 1
                elif self.matrix[i][j][0] == 'c':
                    battlefield[i][j] = 2
                elif self.matrix[i][j][0] == 'B':
                    battlefield[i][j] = 3
                elif self.matrix[i][j][0] == 'C':
                    battlefield[i][j] = 4
                else:
                    battlefield[i][j] = 0
        for i in range(8):
            for j in range(8):
                if battlefield[i][j] == 0:  # background
                    r = self.background_color[0]
                    g = self.background_color[1]
                    b = self.background_color[2]
                    w = self.background_color[3]
                elif battlefield[i][j] == 1:  # my checkers
                    r = self.checkers_my_color[0]
                    g = self.checkers_my_color[1]
                    b = self.checkers_my_color[2]
                    w = self.checkers_my_color[3]
                elif battlefield[i][j] == 2:  # computer checkers
                    r = self.checkers_computer_color[0]
                    g = self.checkers_computer_color[1]
                    b = self.checkers_computer_color[2]
                    w = self.checkers_computer_color[3]
                elif battlefield[i][j] == 3:  # my queens
                    r = self.queens_my_color[0]
                    g = self.queens_my_color[1]
                    b = self.queens_my_color[2]
                    w = self.queens_my_color[3]
                elif battlefield[i][j] == 4:  # computer queens
                    r = self.queens_computer_color[0]
                    g = self.queens_computer_color[1]
                    b = self.queens_computer_color[2]
                    w = self.queens_computer_color[3]
                else:
                    r, g, b, w = 0, 0, 0, 0
                useful_box.color_cell(strip, i, j, (r, g, b, w))
        strip.show()
        useful_box.read_cells(useful_box.BUF_CHECKERS)

    def get_player_input(self, strip):
        useful_box.FLAG_EXIT = False
        available_moves = Checkers.find_player_available_moves(self.matrix, self.mandatory_jumping)
        if len(available_moves) == 0:
            if self.computer_pieces > self.player_pieces:
                print(
                    useful_box.ANSI_RED + "You have no moves left, and you have fewer pieces than the computer. YOU LOSE!" + useful_box.ANSI_RESET)
                self.draw_lose(strip)
            else:
                print(useful_box.ANSI_YELLOW + "You have no available moves.\nGAME ENDED!" + useful_box.ANSI_RESET)
            return True  # exit_game
        self.player_pieces = 0
        self.computer_pieces = 0
        while True:
            coord_1 = '#'
            while coord_1 == '#':
                useful_box.data_processing(useful_box.BUF_CHECKERS)
                time.sleep(0.01)
                active_cells = 0
                for i in range(8):
                    for j in range(8):
                        if useful_box.cells[i][j] == 1:
                            active_cells += 1
                        if useful_box.dry_data[i][j] == 1:
                            coord_1 = str(i) + ',' + str(j)
                if active_cells >= useful_box.EXIT_COUNT:
                    coord_1 = ""
            if coord_1 == "":
                print(useful_box.ANSI_CYAN + "Game ended!" + useful_box.ANSI_RESET)
                useful_box.FLAG_EXIT = True
                return
            elif coord_1 == "s":
                print(useful_box.ANSI_CYAN + "You surrendered.\nCoward." + useful_box.ANSI_RESET)
                useful_box.FLAG_EXIT = True
                return
            else:  # This is correct input?
                old = coord_1.split(",")
                if len(old) != 2:
                    print(useful_box.ANSI_RED + "Illegal input" + useful_box.ANSI_RESET)
                    continue
                else:
                    old_i = old[0]
                    old_j = old[1]
                    if not old_i.isdigit() or not old_j.isdigit():
                        print(useful_box.ANSI_RED + "Illegal input" + useful_box.ANSI_RESET)
                        continue
                    elif int(old_i) < 0 or int(old_i) > 7 or int(old_j) < 0 or int(old_j) > 7:
                        print(useful_box.ANSI_RED + "Illegal input" + useful_box.ANSI_RESET)
                        continue
                    else:
                        symbol = self.matrix[int(old_i)][int(old_j)][0]
                        if symbol == 'b' or symbol == 'B':  # - this is my checker
                            useful_box.color_cell(strip, int(old_i), int(old_j),
                                                  (0, 0, 0, 200))  # - highlight cell with using white color:
                            strip.show()
                        else:
                            continue
                        while True:
                            coord_2 = '#'
                            while coord_2 == '#':
                                useful_box.data_processing(useful_box.BUF_CHECKERS)
                                time.sleep(0.01)
                                active_cells = 0
                                for i in range(8):
                                    for j in range(8):
                                        if useful_box.cells[i][j] == 1:
                                            active_cells += 1
                                        if useful_box.dry_data[i][j] == 1:
                                            coord_2 = str(i) + ',' + str(j)
                                if active_cells >= useful_box.EXIT_COUNT:
                                    useful_box.FLAG_EXIT = True
                                    return
                            if coord_2 == "":
                                print(useful_box.ANSI_CYAN + "Game ended!" + useful_box.ANSI_RESET)
                                useful_box.FLAG_EXIT = True
                                return
                            elif coord_2 == "s":
                                print(useful_box.ANSI_CYAN + "You surrendered.\nCoward." + useful_box.ANSI_RESET)
                                useful_box.FLAG_EXIT = True
                                return
                            else:  # - here we'll check "Input is correct"
                                new = coord_2.split(",")
                                if len(new) != 2:
                                    print(useful_box.ANSI_RED + "Illegal input" + useful_box.ANSI_RESET)
                                    continue
                                else:
                                    new_i = new[0]
                                    new_j = new[1]
                                    if new_i == old_i and new_j == old_j:
                                        continue
                                    if not new_i.isdigit() or not new_j.isdigit():
                                        print(useful_box.ANSI_RED + "Illegal input" + useful_box.ANSI_RESET)
                                        continue
                                    elif int(new_i) < 0 or int(new_i) > 7 or int(new_j) < 0 or int(new_j) > 7:
                                        print(useful_box.ANSI_RED + "Illegal input" + useful_box.ANSI_RESET)
                                        continue
                                    else:
                                        symbol = self.matrix[int(new_i)][int(new_j)][0]
                                        if symbol == 'b' or symbol == 'B':  # This is my checker again. Let's continue!
                                            self.print_matrix(strip)
                                            old_i = new_i
                                            old_j = new_j
                                            print(
                                                useful_box.ANSI_CYAN + "You chose your checker again" + useful_box.ANSI_RESET)
                                            useful_box.color_cell(strip, int(old_i), int(old_j), (0, 0, 0, 200))
                                            continue
                                        else:
                                            move = [int(old_i), int(old_j), int(new_i), int(new_j)]
                                            if move not in available_moves:
                                                print(useful_box.ANSI_RED + "Illegal move!" + useful_box.ANSI_RESET)
                                                continue
                                            else:
                                                print(old_i, old_j, new_i, new_j) # ###############################
                                                Checkers.make_a_move(self.matrix, int(old_i), int(old_j), int(new_i),
                                                                     int(new_j), "B", 0)
                                                for m in range(8):
                                                    for n in range(8):
                                                        if self.matrix[m][n][0] == "c" or self.matrix[m][n][0] == "C":
                                                            self.computer_pieces += 1
                                                        elif self.matrix[m][n][0] == "b" or self.matrix[m][n][0] == "B":
                                                            self.player_pieces += 1
                                                break
                        break

    @staticmethod
    def find_available_moves(strip, board, mandatory_jumping):
        available_moves = []
        available_jumps = []
        for m in range(8):
            for n in range(8):
                if useful_box.FLAG_EXIT:
                    return available_moves
                if board[m][n][0] == "c":
                    if Checkers.check_moves(strip, board, m, n, m + 1, n + 1):
                        available_moves.append([m, n, m + 1, n + 1])
                    if Checkers.check_moves(strip, board, m, n, m + 1, n - 1):
                        available_moves.append([m, n, m + 1, n - 1])
                    if Checkers.check_jumps(board, m, n, m + 1, n - 1, m + 2, n - 2):
                        available_jumps.append([m, n, m + 2, n - 2])
                    if Checkers.check_jumps(board, m, n, m + 1, n + 1, m + 2, n + 2):
                        available_jumps.append([m, n, m + 2, n + 2])
                elif board[m][n][0] == "C":
                    if Checkers.check_moves(strip, board, m, n, m + 1, n + 1):
                        available_moves.append([m, n, m + 1, n + 1])
                    if Checkers.check_moves(strip, board, m, n, m + 1, n - 1):
                        available_moves.append([m, n, m + 1, n - 1])
                    if Checkers.check_moves(strip, board, m, n, m - 1, n - 1):
                        available_moves.append([m, n, m - 1, n - 1])
                    if Checkers.check_moves(strip, board, m, n, m - 1, n + 1):
                        available_moves.append([m, n, m - 1, n + 1])
                    if Checkers.check_jumps(board, m, n, m + 1, n - 1, m + 2, n - 2):
                        available_jumps.append([m, n, m + 2, n - 2])
                    if Checkers.check_jumps(board, m, n, m - 1, n - 1, m - 2, n - 2):
                        available_jumps.append([m, n, m - 2, n - 2])
                    if Checkers.check_jumps(board, m, n, m - 1, n + 1, m - 2, n + 2):
                        available_jumps.append([m, n, m - 2, n + 2])
                    if Checkers.check_jumps(board, m, n, m + 1, n + 1, m + 2, n + 2):
                        available_jumps.append([m, n, m + 2, n + 2])
        if mandatory_jumping is False:
            available_jumps.extend(available_moves)
            return available_jumps
        elif mandatory_jumping is True:
            if len(available_jumps) == 0:
                return available_moves
            else:
                return available_jumps

    @staticmethod
    def check_jumps(board, old_i, old_j, via_i, via_j, new_i, new_j):
        if new_i > 7 or new_i < 0:
            return False
        if new_j > 7 or new_j < 0:
            return False
        if board[via_i][via_j] == "---":
            return False
        if board[via_i][via_j][0] == "C" or board[via_i][via_j][0] == "c":
            return False
        if board[new_i][new_j] != "---":
            return False
        if board[old_i][old_j] == "---":
            return False
        if board[old_i][old_j][0] == "b" or board[old_i][old_j][0] == "B":
            return False
        return True

    @staticmethod
    def check_moves(strip, board, old_i, old_j, new_i, new_j):
        useful_box.data_processing(useful_box.BUF_CHECKERS)
        active_cells = 0
        for i in range(8):
            for j in range(8):
                if useful_box.cells[i][j] == 1:
                    active_cells += 1
        if active_cells >= useful_box.EXIT_COUNT:
            useful_box.FLAG_EXIT = True
        if new_i > 7 or new_i < 0:
            return False
        if new_j > 7 or new_j < 0:
            return False
        if board[old_i][old_j] == "---":
            return False
        if board[new_i][new_j] != "---":
            return False
        if board[old_i][old_j][0] == "b" or board[old_i][old_j][0] == "B":
            return False
        if board[new_i][new_j] == "---":
            return True

    @staticmethod
    def calculate_heuristics(board):
        result = 0
        mine = 0
        opp = 0
        for i in range(8):
            for j in range(8):
                if board[i][j][0] == "c" or board[i][j][0] == "C":
                    mine += 1

                    if board[i][j][0] == "c":
                        result += 5
                    if board[i][j][0] == "C":
                        result += 10
                    if i == 0 or j == 0 or i == 7 or j == 7:
                        result += 7
                    if i + 1 > 7 or j - 1 < 0 or i - 1 < 0 or j + 1 > 7:
                        continue
                    if (board[i + 1][j - 1][0] == "b" or board[i + 1][j - 1][0] == "B") \
                            and board[i - 1][j + 1] == "---":
                        result -= 3
                    if (board[i + 1][j + 1][0] == "b" or board[i + 1][j + 1] == "B") and board[i - 1][j - 1] == "---":
                        result -= 3
                    if board[i - 1][j - 1][0] == "B" and board[i + 1][j + 1] == "---":
                        result -= 3

                    if board[i - 1][j + 1][0] == "B" and board[i + 1][j - 1] == "---":
                        result -= 3
                    if i + 2 > 7 or i - 2 < 0:
                        continue
                    if (board[i + 1][j - 1][0] == "B" or board[i + 1][j - 1][0] == "b") \
                            and board[i + 2][j - 2] == "---":
                        result += 6
                    if i + 2 > 7 or j + 2 > 7:
                        continue
                    if (board[i + 1][j + 1][0] == "B" or board[i + 1][j + 1][0] == "b") \
                            and board[i + 2][j + 2] == "---":
                        result += 6

                elif board[i][j][0] == "b" or board[i][j][0] == "B":
                    opp += 1
        return result + (mine - opp) * 1000

    @staticmethod
    def find_player_available_moves(board, mandatory_jumping):
        available_moves = []
        available_jumps = []
        for m in range(8):
            for n in range(8):
                if board[m][n][0] == "b":
                    if Checkers.check_player_moves(board, m, n, m - 1, n - 1):
                        available_moves.append([m, n, m - 1, n - 1])
                    if Checkers.check_player_moves(board, m, n, m - 1, n + 1):
                        available_moves.append([m, n, m - 1, n + 1])
                    if Checkers.check_player_jumps(board, m, n, m - 1, n - 1, m - 2, n - 2):
                        available_jumps.append([m, n, m - 2, n - 2])
                    if Checkers.check_player_jumps(board, m, n, m - 1, n + 1, m - 2, n + 2):
                        available_jumps.append([m, n, m - 2, n + 2])
                elif board[m][n][0] == "B":
                    if Checkers.check_player_moves(board, m, n, m - 1, n - 1):
                        available_moves.append([m, n, m - 1, n - 1])
                    if Checkers.check_player_moves(board, m, n, m - 1, n + 1):
                        available_moves.append([m, n, m - 1, n + 1])
                    if Checkers.check_player_jumps(board, m, n, m - 1, n - 1, m - 2, n - 2):
                        available_jumps.append([m, n, m - 2, n - 2])
                    if Checkers.check_player_jumps(board, m, n, m - 1, n + 1, m - 2, n + 2):
                        available_jumps.append([m, n, m - 2, n + 2])
                    if Checkers.check_player_moves(board, m, n, m + 1, n - 1):
                        available_moves.append([m, n, m + 1, n - 1])
                    if Checkers.check_player_jumps(board, m, n, m + 1, n - 1, m + 2, n - 2):
                        available_jumps.append([m, n, m + 2, n - 2])
                    if Checkers.check_player_moves(board, m, n, m + 1, n + 1):
                        available_moves.append([m, n, m + 1, n + 1])
                    if Checkers.check_player_jumps(board, m, n, m + 1, n + 1, m + 2, n + 2):
                        available_jumps.append([m, n, m + 2, n + 2])
        if mandatory_jumping is False:
            available_jumps.extend(available_moves)
            return available_jumps
        elif mandatory_jumping is True:
            if len(available_jumps) == 0:
                return available_moves
            else:
                return available_jumps

    @staticmethod
    def check_player_moves(board, old_i, old_j, new_i, new_j):
        if new_i > 7 or new_i < 0:
            return False
        if new_j > 7 or new_j < 0:
            return False
        if board[old_i][old_j] == "---":
            return False
        if board[new_i][new_j] != "---":
            return False
        if board[old_i][old_j][0] == "c" or board[old_i][old_j][0] == "C":
            return False
        if board[new_i][new_j] == "---":
            return True

    @staticmethod
    def check_player_jumps(board, old_i, old_j, via_i, via_j, new_i, new_j):
        if new_i > 7 or new_i < 0:
            return False
        if new_j > 7 or new_j < 0:
            return False
        if board[via_i][via_j] == "---":
            return False
        if board[via_i][via_j][0] == "B" or board[via_i][via_j][0] == "b":
            return False
        if board[new_i][new_j] != "---":
            return False
        if board[old_i][old_j] == "---":
            return False
        if board[old_i][old_j][0] == "c" or board[old_i][old_j][0] == "C":
            return False
        return True

    def evaluate_states(self, strip):
        t1 = time.time()
        current_state = Node(deepcopy(self.matrix))
        first_computer_moves = current_state.get_children(strip, True, self.mandatory_jumping)
        if first_computer_moves is None:
            return
        if len(first_computer_moves) == 0:
            if self.player_pieces > self.computer_pieces:
                print(useful_box.ANSI_YELLOW + "Computer has no available moves left, and you have more pieces left.\nYOU WIN!" + useful_box.ANSI_RESET)
                useful_box.FLAG_EXIT = True
                return
            else:
                print(useful_box.ANSI_YELLOW + "Computer has no available moves left.\nGAME ENDED!" + useful_box.ANSI_RESET)
                useful_box.FLAG_EXIT = True
                return
        board_dict = {}
        for i in range(len(first_computer_moves)):
            child = first_computer_moves[i]
            value = Checkers.minimax(strip, child.get_board(), 4, -math.inf, math.inf, False, self.mandatory_jumping)
            board_dict[value] = child
        if len(board_dict.keys()) == 0:
            print(useful_box.ANSI_GREEN + "Computer has cornered itself.\nYOU WIN!" + useful_box.ANSI_RESET)
            return
        new_board = board_dict[max(board_dict)].get_board()
        move = board_dict[max(board_dict)].move
        self.matrix = new_board
        t2 = time.time()
        diff = t2 - t1
        print("Computer has moved (" + str(move[0]) + "," + str(move[1]) + ") to (" + str(move[2]) + "," + str(
            move[3]) + ").")
        print("It took him " + str(diff) + " seconds.")
        return move

    @staticmethod
    def minimax(strip, board, depth, alpha, beta, maximizing_player, mandatory_jumping):
        if depth == 0:
            return Checkers.calculate_heuristics(board)
        current_state = Node(deepcopy(board))
        if maximizing_player is True:
            max_eval = -math.inf
            childrens = current_state.get_children(strip, True, mandatory_jumping)
            if childrens is None:
                return
            for child in childrens:
                ev = Checkers.minimax(strip, child.get_board(), depth - 1, alpha, beta, False, mandatory_jumping)
                max_eval = max(max_eval, ev)
                alpha = max(alpha, ev)
                if beta <= alpha:
                    break
            current_state.set_value(max_eval)
            return max_eval
        else:
            min_eval = math.inf
            childrens = current_state.get_children(strip, False, mandatory_jumping)
            if childrens is None:
                return
            for child in childrens:
                ev = Checkers.minimax(strip, child.get_board(), depth - 1, alpha, beta, True, mandatory_jumping)
                min_eval = min(min_eval, ev)
                beta = min(beta, ev)
                if beta <= alpha:
                    break
            current_state.set_value(min_eval)
            return min_eval

    @staticmethod
    def make_a_move(board, old_i, old_j, new_i, new_j, big_letter, queen_row):
        letter = board[old_i][old_j][0]
        i_difference = old_i - new_i
        j_difference = old_j - new_j
        if i_difference == -2 and j_difference == 2:
            board[old_i + 1][old_j - 1] = "---"

        elif i_difference == 2 and j_difference == 2:
            board[old_i - 1][old_j - 1] = "---"

        elif i_difference == 2 and j_difference == -2:
            board[old_i - 1][old_j + 1] = "---"

        elif i_difference == -2 and j_difference == -2:
            board[old_i + 1][old_j + 1] = "---"

        if new_i == queen_row:
            letter = big_letter
        board[old_i][old_j] = "---"
        board[new_i][new_j] = letter + str(new_i) + str(new_j)

    def draw_win(self, strip):
        r = self.checkers_my_color[0]
        g = self.checkers_my_color[1]
        b = self.checkers_my_color[2]
        w = self.checkers_my_color[3]
        for i in range(16):
            for j in range(16):
                strip.setPixelColor(useful_box.LEDS_ORDER[15 - i][j], Color(r, g, b, w))
            time.sleep(0.05)
            strip.show()
        time.sleep(1)
        useful_box.soft_down_brightness(strip)

    def draw_lose(self, strip):
        r = self.checkers_computer_color[0]
        g = self.checkers_computer_color[1]
        b = self.checkers_computer_color[2]
        w = self.checkers_computer_color[3]
        for i in range(16):
            for j in range(16):
                strip.setPixelColor(useful_box.LEDS_ORDER[i][j], Color(r, g, b, w))
            time.sleep(0.05)
            strip.show()
        time.sleep(1)
        useful_box.soft_down_brightness(strip)

    def play(self, strip):

        useful_box.FLAG_EXIT = False

        r0 = self.background_color[0]
        g0 = self.background_color[1]
        b0 = self.background_color[2]
        w0 = self.background_color[3]

        useful_box.color_leds(strip, (r0, g0, b0, w0))  # coloring table in background color
        self.print_matrix(strip)
        useful_box.soft_up_brightness(strip)
        time.sleep(1)

        print(useful_box.ANSI_CYAN + "##### WELCOME TO CHECKERS ####" + useful_box.ANSI_RESET)
        print("\nSome basic rules:")
        print("1.You enter the coordinates in the form i,j.")
        print("2.You can quit the game at any time by pressing enter.")
        print("3.You can surrender at any time by pressing 's'.")
        print("Now that you've familiarized yourself with the rules, enjoy!")
        while True:
            answer = "N"  # Костыль - сразу выбираю игру без поддавков. Блок ниже - обработчик выбора режима игры
            if answer == "Y" or answer == "y":
                self.mandatory_jumping = True
                break
            elif answer == "N" or answer == "n":
                self.mandatory_jumping = False
                break

            elif answer == "":
                print(useful_box.ANSI_CYAN + "Game ended!" + useful_box.ANSI_RESET)
                useful_box.FLAG_EXIT = True
                break

            elif answer == "s":
                print(useful_box.ANSI_CYAN + "You've surrendered before the game even started.\nPathetic." + useful_box.ANSI_RESET)
                useful_box.FLAG_EXIT = True
                break

            else:
                print(useful_box.ANSI_RED + "Illegal input! Repeat input please" + useful_box.ANSI_RESET)

        while not useful_box.FLAG_EXIT:
            self.print_matrix(strip)
            if self.player_turn is True:
                print(useful_box.ANSI_CYAN + "\nPlayer's turn." + useful_box.ANSI_RESET)
                self.get_player_input(strip)
            else:
                print(useful_box.ANSI_CYAN + "Computer's turn." + useful_box.ANSI_RESET)
                print("Thinking...")
                move = self.evaluate_states(strip)
                print(move)
            if useful_box.FLAG_EXIT:
                useful_box.draw_endgame(strip)
                useful_box.soft_down_brightness(strip)
                break
            if self.player_pieces == 0:
                print(useful_box.ANSI_RED + "You have no pieces left.\nYOU LOSE!" + useful_box.ANSI_RESET)
                self.print_matrix(strip)
                self.draw_lose(strip)
                break
            elif self.computer_pieces == 0:
                print(useful_box.ANSI_GREEN + "Computer has no pieces left.\nYOU WIN!" + useful_box.ANSI_RESET)
                self.print_matrix(strip)
                self.draw_win(strip)
                break
            self.player_turn = not self.player_turn
