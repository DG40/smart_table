import time
import math
import random
from rpi_ws281x import *
from copy import deepcopy

from table import Table
from variables import *

# 1:
Pallete_1 = [
    [0, 0, 0, 0],  # background
    [255, 0, 0, 0],  # checkers_my
    [0, 0, 255, 0],  # checkers_computer
    [255, 0, 0, 50],  # queens_my
    [0, 0, 255, 50]  # queens_computer
]

# 2:
Pallete_2 = [
    [0, 0, 0, 0],  # background
    [200, 200, 0, 0],  # checkers_my
    [200, 0, 200, 0],  # checkers_computer
    [255, 255, 0, 50],  # queens_my
    [255, 0, 255, 50]  # queens_computer
]


class Node:
    def __init__(self, board, move=None, parent=None, value=None):
        self.board = board
        self.value = value
        self.move = move
        self.parent = parent

    def get_children(self, minimizing_player, mandatory_jumping):
        current_state = deepcopy(self.board)
        children_states = []
        if minimizing_player is True:
            available_moves = Checkers.find_available_moves(current_state, mandatory_jumping)
            big_letter = "C"  # - my checkers
            queen_row = 7  # line of my queens
        else:
            available_moves = Checkers.find_player_available_moves(current_state, mandatory_jumping)
            big_letter = "B"  # - opponent's checkers
            queen_row = 0  # line of opponent's queens
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

        rand_numb = random.randint(1, 2)
        if rand_numb == 1:
            Pallete = Pallete_1
        elif rand_numb == 2:
            Pallete = Pallete_2

        self.background_color = Pallete[0]  # background
        self.checkers_my_color = Pallete[1]  # checkers_my
        self.checkers_computer_color = Pallete[2]  # checkers_computer
        self.queens_my_color = Pallete[3]  # queens_my
        self.queens_computer_color = Pallete[4]  # queens_computer

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
        for i in range(5, 8):
            for j in range(8):
                if (i + j) % 2 == 1:
                    self.matrix[i][j] = ("b" + str(i) + str(j))

    def print_matrix(self, strip):
        i = 0  # - checkerboard line
        print()
        for row in self.matrix:
            print(i, end="  |")
            i += 1
            for elem in row:
                if elem[0] == 'c':
                    print(ansi_cyan + elem + ansi_reset, end=" ")
                elif elem[0] == 'b':
                    print(ansi_yellow + elem + ansi_reset, end=" ")
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
                battlefield[i][j] = 0

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

        # Print LEDs
        for i in range(8):
            for j in range(8):
                if battlefield[i][j] == 0:
                    # Background:
                    r = self.background_color[0]
                    g = self.background_color[1]
                    b = self.background_color[2]
                    w = self.background_color[3]
                elif battlefield[i][j] == 1:
                    # My checkers:
                    r = self.checkers_my_color[0]
                    g = self.checkers_my_color[1]
                    b = self.checkers_my_color[2]
                    w = self.checkers_my_color[3]
                elif battlefield[i][j] == 2:
                    # Computer checkers:
                    r = self.checkers_computer_color[0]
                    g = self.checkers_computer_color[1]
                    b = self.checkers_computer_color[2]
                    w = self.checkers_computer_color[3]
                elif battlefield[i][j] == 3:
                    # My Queens:
                    r = self.queens_my_color[0]
                    g = self.queens_my_color[1]
                    b = self.queens_my_color[2]
                    w = self.queens_my_color[3]
                elif battlefield[i][j] == 4:
                    # Computer Queens:
                    r = self.queens_computer_color[0]
                    g = self.queens_computer_color[1]
                    b = self.queens_computer_color[2]
                    w = self.queens_computer_color[3]
                strip.setPixelColor(order[i * 2][j * 2], Color(r, g, b, w))
                strip.setPixelColor(order[i * 2 + 1][j * 2], Color(r, g, b, w))
                strip.setPixelColor(order[i * 2][j * 2 + 1], Color(r, g, b, w))
                strip.setPixelColor(order[i * 2 + 1][j * 2 + 1], Color(r, g, b, w))

        strip.show()
        ReadCells(buf_checkers)
        PrintData()

    def get_player_input(self, strip):
        exit_game = False

        available_moves = Checkers.find_player_available_moves(self.matrix, self.mandatory_jumping)
        if len(available_moves) == 0:
            if self.computer_pieces > self.player_pieces:
                print(
                    ansi_red + "You have no moves left, and you have fewer pieces than the computer. YOU LOSE!" + ansi_reset)
                self.draw_lose(strip)
                exit_game = True
                return exit_game

            else:
                print(ansi_yellow + "You have no available moves.\nGAME ENDED!" + ansi_reset)
                self.draw_endgame(strip)
                exit_game = True
                return exit_game

        self.player_pieces = 0
        self.computer_pieces = 0

        while True:
            # coord1 = input("Which piece[i,j]: ")
            coord1 = '#'
            while coord1 == '#':
                DataProcessing(buf_checkers)
                time.sleep(0.01)
                active_cells = 0
                for i in range(8):
                    for j in range(8):
                        if Cells[i][j] == 1:
                            active_cells += 1
                        if DryData[i][j] == 1:
                            coord1 = str(i) + ',' + str(j)
                if active_cells >= switch_count:
                    coord1 = ""

            if coord1 == "":
                print(ansi_cyan + "Game ended!" + ansi_reset)
                exit_game = True
                return exit_game

            elif coord1 == "s":
                print(ansi_cyan + "You surrendered.\nCoward." + ansi_reset)
                exit_game = True
                return exit_game

            else:  # This is correct input?
                old = coord1.split(",")
                if len(old) != 2:
                    print(ansi_red + "Illegal input" + ansi_reset)
                    continue
                else:
                    old_i = old[0]
                    old_j = old[1]
                    if not old_i.isdigit() or not old_j.isdigit():
                        print(ansi_red + "Illegal input" + ansi_reset)
                        continue
                    elif int(old_i) < 0 or int(old_i) > 7 or int(old_j) < 0 or int(old_j) > 7:
                        print(ansi_red + "Illegal input" + ansi_reset)
                        continue
                    else:
                        symb = self.matrix[int(old_i)][int(old_j)][0]
                        if symb == 'b' or symb == 'B':  # COOL! This is my checker. Let's continue!

                            # Select cell with using white color:
                            r, g, b, w = (0, 0, 0, 200)  # - color of selected cell
                            strip.setPixelColor(order[int(old_i) * 2][int(old_j) * 2], Color(r, g, b, w))
                            strip.setPixelColor(order[int(old_i) * 2 + 1][int(old_j) * 2], Color(r, g, b, w))
                            strip.setPixelColor(order[int(old_i) * 2][int(old_j) * 2 + 1], Color(r, g, b, w))
                            strip.setPixelColor(order[int(old_i) * 2 + 1][int(old_j) * 2 + 1], Color(r, g, b, w))
                            strip.show()
                        else:
                            continue

                        while True:
                            # coord2 = input("Where to[i,j]:")
                            coord2 = '#'
                            while coord2 == '#':
                                DataProcessing(buf_checkers)
                                time.sleep(0.01)
                                active_cells = 0
                                for i in range(8):
                                    for j in range(8):
                                        if Cells[i][j] == 1:
                                            active_cells += 1
                                        if DryData[i][j] == 1:
                                            coord2 = str(i) + ',' + str(j)
                                if active_cells >= switch_count:
                                    coord2 = ""
                            if coord2 == "":
                                print(ansi_cyan + "Game ended!" + ansi_reset)
                                exit_game = True
                                return exit_game

                            elif coord2 == "s":
                                print(ansi_cyan + "You surrendered.\nCoward." + ansi_reset)
                                exit_game = True
                                return exit_game

                            else:  # This is correct input?
                                new = coord2.split(",")
                                if len(new) != 2:
                                    print(ansi_red + "Illegal input" + ansi_reset)
                                    continue
                                else:
                                    new_i = new[0]
                                    new_j = new[1]
                                    if new_i == old_i and new_j == old_j:
                                        continue
                                    if not new_i.isdigit() or not new_j.isdigit():
                                        print(ansi_red + "Illegal input" + ansi_reset)
                                        continue
                                    elif int(new_i) < 0 or int(new_i) > 7 or int(new_j) < 0 or int(new_j) > 7:
                                        print(ansi_red + "Illegal input" + ansi_reset)
                                        continue
                                    else:
                                        symb = self.matrix[int(new_i)][int(new_j)][0]
                                        if symb == 'b' or symb == 'B':  # This is my checker again. Let's continue!
                                            self.print_matrix(strip)  # Redrawing #
                                            old_i = new_i
                                            old_j = new_j
                                            print(ansi_cyan + "You chose your checker again" + ansi_reset)

                                            # Select cell with using white color:
                                            r, g, b, w = (0, 0, 0, 200)
                                            strip.setPixelColor(order[int(old_i) * 2][int(old_j) * 2],
                                                                Color(r, g, b, w))
                                            strip.setPixelColor(order[int(old_i) * 2 + 1][int(old_j) * 2],
                                                                Color(r, g, b, w))
                                            strip.setPixelColor(order[int(old_i) * 2][int(old_j) * 2 + 1],
                                                                Color(r, g, b, w))
                                            strip.setPixelColor(order[int(old_i) * 2 + 1][int(old_j) * 2 + 1],
                                                                Color(r, g, b, w))
                                            strip.show()

                                            continue
                                        else:
                                            move = [int(old_i), int(old_j), int(new_i), int(new_j)]
                                            if move not in available_moves:
                                                print(ansi_red + "Illegal move!" + ansi_reset)
                                                continue
                                            else:
                                                break_flag = True
                                                print(int(old_i), int(old_j), int(new_i), int(new_j))
                                                Checkers.make_a_move(self.matrix, int(old_i), int(old_j), int(new_i),
                                                                     int(new_j), "B", 0)
                                                for m in range(8):
                                                    for n in range(8):
                                                        if self.matrix[m][n][0] == "c" or self.matrix[m][n][0] == "C":
                                                            self.computer_pieces += 1
                                                        elif self.matrix[m][n][0] == "b" or self.matrix[m][n][0] == "B":
                                                            self.player_pieces += 1
                                                break
                        return exit_game

    @staticmethod
    def find_available_moves(board, mandatory_jumping):
        available_moves = []
        available_jumps = []
        for m in range(8):
            for n in range(8):
                if board[m][n][0] == "c":
                    if Checkers.check_moves(board, m, n, m + 1, n + 1):
                        available_moves.append([m, n, m + 1, n + 1])
                    if Checkers.check_moves(board, m, n, m + 1, n - 1):
                        available_moves.append([m, n, m + 1, n - 1])
                    if Checkers.check_jumps(board, m, n, m + 1, n - 1, m + 2, n - 2):
                        available_jumps.append([m, n, m + 2, n - 2])
                    if Checkers.check_jumps(board, m, n, m + 1, n + 1, m + 2, n + 2):
                        available_jumps.append([m, n, m + 2, n + 2])
                elif board[m][n][0] == "C":
                    if Checkers.check_moves(board, m, n, m + 1, n + 1):
                        available_moves.append([m, n, m + 1, n + 1])
                    if Checkers.check_moves(board, m, n, m + 1, n - 1):
                        available_moves.append([m, n, m + 1, n - 1])
                    if Checkers.check_moves(board, m, n, m - 1, n - 1):
                        available_moves.append([m, n, m - 1, n - 1])
                    if Checkers.check_moves(board, m, n, m - 1, n + 1):
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
    def check_moves(board, old_i, old_j, new_i, new_j):

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
                    if (board[i + 1][j - 1][0] == "b" or board[i + 1][j - 1][0] == "B") and board[i - 1][
                        j + 1] == "---":
                        result -= 3
                    if (board[i + 1][j + 1][0] == "b" or board[i + 1][j + 1] == "B") and board[i - 1][j - 1] == "---":
                        result -= 3
                    if board[i - 1][j - 1][0] == "B" and board[i + 1][j + 1] == "---":
                        result -= 3

                    if board[i - 1][j + 1][0] == "B" and board[i + 1][j - 1] == "---":
                        result -= 3
                    if i + 2 > 7 or i - 2 < 0:
                        continue
                    if (board[i + 1][j - 1][0] == "B" or board[i + 1][j - 1][0] == "b") and board[i + 2][
                        j - 2] == "---":
                        result += 6
                    if i + 2 > 7 or j + 2 > 7:
                        continue
                    if (board[i + 1][j + 1][0] == "B" or board[i + 1][j + 1][0] == "b") and board[i + 2][
                        j + 2] == "---":
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

    def evaluate_states(self):
        t1 = time.time()
        current_state = Node(deepcopy(self.matrix))

        first_computer_moves = current_state.get_children(True, self.mandatory_jumping)
        if len(first_computer_moves) == 0:
            if self.player_pieces > self.computer_pieces:
                print(
                    ansi_yellow + "Computer has no available moves left, and you have more pieces left.\nYOU WIN!" + ansi_reset)
                exit()
            else:
                print(ansi_yellow + "Computer has no available moves left.\nGAME ENDED!" + ansi_reset)
                exit()
        dict = {}
        for i in range(len(first_computer_moves)):
            child = first_computer_moves[i]
            value = Checkers.minimax(child.get_board(), 4, -math.inf, math.inf, False, self.mandatory_jumping)
            dict[value] = child
        if len(dict.keys()) == 0:
            print(ansi_green + "Computer has cornered itself.\nYOU WIN!" + ansi_reset)
            exit()
        new_board = dict[max(dict)].get_board()
        move = dict[max(dict)].move
        self.matrix = new_board
        t2 = time.time()
        diff = t2 - t1
        print("Computer has moved (" + str(move[0]) + "," + str(move[1]) + ") to (" + str(move[2]) + "," + str(
            move[3]) + ").")
        print("It took him " + str(diff) + " seconds.")

    @staticmethod
    def minimax(board, depth, alpha, beta, maximizing_player, mandatory_jumping):
        if depth == 0:
            return Checkers.calculate_heuristics(board)
        current_state = Node(deepcopy(board))
        if maximizing_player is True:
            max_eval = -math.inf
            for child in current_state.get_children(True, mandatory_jumping):
                ev = Checkers.minimax(child.get_board(), depth - 1, alpha, beta, False, mandatory_jumping)
                max_eval = max(max_eval, ev)
                alpha = max(alpha, ev)
                if beta <= alpha:
                    break
            current_state.set_value(max_eval)
            return max_eval
        else:
            min_eval = math.inf
            for child in current_state.get_children(False, mandatory_jumping):
                ev = Checkers.minimax(child.get_board(), depth - 1, alpha, beta, True, mandatory_jumping)
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

    def draw_endgame(self, strip):
        r = self.background_color[0]
        g = self.background_color[1]
        b = self.background_color[2]
        w = self.background_color[3]
        for i in range(16):
            for j in range(16):
                strip.setPixelColor(order[15 - i][j], Color(r, g, b, w))
            time.sleep(0.05)
            strip.show()
        # time.sleep(1)
        Soft_down_brightness(strip)

    def draw_win(self, strip):
        r = self.checkers_my_color[0]
        g = self.checkers_my_color[1]
        b = self.checkers_my_color[2]
        w = self.checkers_my_color[3]
        for i in range(16):
            for j in range(16):
                strip.setPixelColor(order[15 - i][j], Color(r, g, b, w))
            time.sleep(0.05)
            strip.show()
        time.sleep(1)
        Soft_down_brightness(strip)

    def draw_lose(self, strip):
        r = self.checkers_computer_color[0]
        g = self.checkers_computer_color[1]
        b = self.checkers_computer_color[2]
        w = self.checkers_computer_color[3]
        for i in range(16):
            for j in range(16):
                strip.setPixelColor(order[i][j], Color(r, g, b, w))
            time.sleep(0.05)
            strip.show()
        time.sleep(1)
        Soft_down_brightness(strip)

    def play(self, strip):

        exit_game = False

        r0 = self.background_color[0]
        g0 = self.background_color[1]
        b0 = self.background_color[2]
        w0 = self.background_color[3]

        Table.ColoringTable_JustColor(strip, r0, g0, b0, w0)  # Coloring background
        self.print_matrix(strip)
        Soft_up_brightness(strip)
        time.sleep(1)

        print(ansi_cyan + "##### WELCOME TO CHECKERS ####" + ansi_reset)
        print("\nSome basic rules:")
        print("1.You enter the coordinates in the form i,j.")
        print("2.You can quit the game at any time by pressing enter.")
        print("3.You can surrender at any time by pressing 's'.")
        print("Now that you've familiarized yourself with the rules, enjoy!")
        while True:
            # answer = input("\nFirst, we need to know, is jumping mandatory?[Y/n]: ")
            answer = "N"  # (crutch, needs code-review)
            if answer == "Y" or answer == "y":
                self.mandatory_jumping = True
                break
            elif answer == "N" or answer == "n":
                self.mandatory_jumping = False
                break
            elif answer == "":
                print(ansi_cyan + "Game ended!" + ansi_reset)
                exit_game = True
                break
            elif answer == "s":
                print(ansi_cyan + "You've surrendered before the game even started.\nPathetic." + ansi_reset)
                exit_game = True
                break
            else:
                print(ansi_red + "Illegal input!" + ansi_reset)

        while True:
            if not exit_game:
                self.print_matrix(strip)
                if self.player_turn is True:
                    print(ansi_cyan + "\nPlayer's turn." + ansi_reset)
                    exit_game = self.get_player_input(strip)
                    if exit_game:
                        self.draw_endgame(strip)
                        break
                else:
                    print(ansi_cyan + "Computer's turn." + ansi_reset)
                    print("Thinking...")
                    self.evaluate_states()

                if self.player_pieces == 0:
                    print(ansi_red + "You have no pieces left.\nYOU LOSE!" + ansi_reset)
                    self.print_matrix(strip)
                    self.draw_lose(strip)
                    break
                elif self.computer_pieces == 0:
                    print(ansi_green + "Computer has no pieces left.\nYOU WIN!" + ansi_reset)
                    self.print_matrix(strip)
                    self.draw_win(strip)
                    break
                self.player_turn = not self.player_turn
            else:
                break
