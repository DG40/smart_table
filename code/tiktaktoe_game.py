from rpi_ws281x import *
import random
import time
from variables import *

# 1:
Pallete_1 = [
    [0, 30, 0, 20],  # background
    [255, 0, 0, 0],  # checkers_my
    [0, 0, 255, 0],  # checkers_computer
]

# 2:
Pallete_2 = [
    [0, 0, 30, 20],  # background
    [255, 255, 0, 0],  # checkers_my
    [255, 0, 255, 0],  # checkers_computer
]


class TikTakToe:
    print("*" * 10, " Tic-tac-toe game for two players ", "*" * 10)

    def __init__(self):
        rand_numb = random.randint(1, 2)
        if rand_numb == 1:
            Pallete = Pallete_1
        elif rand_numb == 2:
            Pallete = Pallete_2

        self.background_color = Pallete[0]  # background
        self.tiktak_first_player_color = Pallete[1]  # checkers_my
        self.tiktak_second_player_color = Pallete[2]  # checkers_computer
        self.board = list(range(1, 10))
        self.flag_exit = False
        self.tmp = False
        self.win_coord = (0, 0, 0)

    def draw_board(self, strip):
        print("-" * 13)
        for i in range(3):
            print("|", self.board[0 + i * 3], "|", self.board[1 + i * 3], "|", self.board[2 + i * 3], "|")
            print("-" * 13)

        r, g, b, w = 0, 0, 0, 0
        for i in range(16):  # FRAME
            strip.setPixelColor(order[0][i], Color(r, g, b, w))
            strip.setPixelColor(order[1][i], Color(r, g, b, w))
            strip.setPixelColor(order[14][i], Color(r, g, b, w))
            strip.setPixelColor(order[15][i], Color(r, g, b, w))
            strip.setPixelColor(order[i][0], Color(r, g, b, w))
            strip.setPixelColor(order[i][1], Color(r, g, b, w))
            strip.setPixelColor(order[i][14], Color(r, g, b, w))
            strip.setPixelColor(order[i][15], Color(r, g, b, w))

        r = self.background_color[0]
        g = self.background_color[1]
        b = self.background_color[2]
        w = self.background_color[3]

        for i in range(3):  # SHARPS
            for j in range(3):
                if (i * 3 + j) % 2 == 0:
                    r = self.background_color[0]
                    g = self.background_color[1]
                    b = self.background_color[2]
                    w = self.background_color[3]
                    for k in range(i * 4 + 2, i * 4 + 6):
                        for m in range(j * 4 + 2, j * 4 + 6):
                            strip.setPixelColor(order[k][m], Color(r, g, b, w))
                else:
                    w += 30
                    for k in range(i * 4 + 2, i * 4 + 6):
                        for m in range(j * 4 + 2, j * 4 + 6):
                            strip.setPixelColor(order[k][m], Color(r, g, b, w))

        for i in range(3):  # XO
            for j in range(3):
                if self.board[j + i * 3] == 'X':
                    r = self.tiktak_first_playrer_color[0]
                    g = self.tiktak_first_playrer_color[1]
                    b = self.tiktak_first_playrer_color[2]
                    w = self.tiktak_first_playrer_color[3]
                    for k in range(i * 4 + 2, i * 4 + 6):
                        for m in range(j * 4 + 2, j * 4 + 6):
                            strip.setPixelColor(order[k][m], Color(r, g, b, w))
                elif self.board[j + i * 3] == 'O':
                    r = self.tiktak_second_player_color[0]
                    g = self.tiktak_second_player_color[1]
                    b = self.tiktak_second_player_color[2]
                    w = self.tiktak_second_player_color[3]
                    for k in range(i * 4 + 2, i * 4 + 6):
                        for m in range(j * 4 + 2, j * 4 + 6):
                            strip.setPixelColor(order[k][m], Color(r, g, b, w))
        strip.show()

    def draw_endgame(self, strip):
        for i in range(16):  # BACKGROUND
            for j in range(16):
                if self.tmp == 'X':  # X won!
                    r = self.tiktak_first_playrer_color[0]
                    g = self.tiktak_first_playrer_color[1]
                    b = self.tiktak_first_playrer_color[2]
                    w = self.tiktak_first_playrer_color[3]
                elif self.tmp == 'O':  # 0 won!
                    r = self.tiktak_second_player_color[0]
                    g = self.tiktak_second_player_color[1]
                    b = self.tiktak_second_player_color[2]
                    w = self.tiktak_second_player_color[3]
                else:  # Ничья!
                    r = self.background_color[0]
                    g = self.background_color[1]
                    b = self.background_color[2]
                    w = self.background_color[3] + 30
                strip.setPixelColor(order[i][j], Color(r, g, b, w))
            time.sleep(0.05)
            strip.show()
        time.sleep(1)

    def blink_win(self, strip):

        if self.tmp == 'X':  # X won!
            r = self.tiktak_first_playrer_color[0]
            g = self.tiktak_first_playrer_color[1]
            b = self.tiktak_first_playrer_color[2]
            w = self.tiktak_first_playrer_color[3]
        else:  # 0 won!
            r = self.tiktak_second_player_color[0]
            g = self.tiktak_second_player_color[1]
            b = self.tiktak_second_player_color[2]
            w = self.tiktak_second_player_color[3]

        r0, g0, b0, w0 = 0, 0, 0, 0

        for t in range(6):
            for c in self.win_coord:
                i = c // 3
                j = c % 3
                for k in range(i * 4 + 2, i * 4 + 6):
                    for m in range(j * 4 + 2, j * 4 + 6):
                        if t % 2 == 0:
                            if k == i * 4 + 2 or k == i * 4 + 6 - 1 or m == j * 4 + 2 or m == j * 4 + 6 - 1:
                                strip.setPixelColor(order[k][m], Color(r0, g0, b0, w0))
                            else:
                                strip.setPixelColor(order[k][m], Color(r, g, b, w))
                        else:
                            strip.setPixelColor(order[k][m], Color(r, g, b, w))
            strip.show()
            time.sleep(0.25)

    def take_input(self, player_token):

        print("Where will we put " + player_token + "? ")
        while True:
            player_answer = 0
            total = 0

            DataProcessing(buf_tiktaktoe)
            time.sleep(0.01)

            for i in range(8):
                for j in range(8):
                    if Cells[i][j] == 1:
                        total += 1
            if total >= switch_count:
                self.flag_exit = True
                break

            else:
                for i in range(len(cells_TikTak)):
                    totalDry = 0
                    for sens in cells_TikTak[i]:
                        if DryData[sens[0]][sens[1]] == 1:
                            totalDry += 1
                    if totalDry >= 3:
                        player_answer = i + 1
                        print(player_answer)
                        break

                if str(self.board[player_answer - 1]) not in "XO" and player_answer != 0:
                    self.board[player_answer - 1] = player_token
                    break
                elif player_answer != 0:
                    print("This cell is already taken!")

    def check_win(self):
        win_coord = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6))
        for each in win_coord:
            if self.board[each[0]] == self.board[each[1]] == self.board[each[2]]:
                self.win_coord = each
                return self.board[each[0]]
        return False

    def play(self, strip):

        while not self.flag_exit:

            counter = 0
            win = False

            self.draw_board(strip)
            Soft_up_brightness(strip)
            time.sleep(1)

            while not win:
                if counter % 2 == 0:
                    self.take_input("X")
                else:
                    self.take_input("O")
                if self.flag_exit:
                    break
                counter += 1
                self.draw_board(strip)
                if counter > 4:
                    self.tmp = self.check_win()
                    if self.tmp:
                        self.blink_win(strip)

                        print(self.tmp, "won!")
                        win = True
                        break
                    if counter == 9:
                        print("Tie!")
                        break

            time.sleep(0.25)
            if self.flag_exit:
                print(ansi_green + 'Quit game!' + ansi_reset)
                self.tmp = ''
            self.draw_endgame(strip)
            Soft_down_brightness(strip)
            self.board = list(range(1, 10))
