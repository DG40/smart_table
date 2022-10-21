from rpi_ws281x import *
import random
import time
import useful_box

PALETTE_1 = {
    'background': (0, 30, 0, 20),
    'cells_my': (255, 0, 0, 0),
    'cells_computer': (0, 0, 255, 0)
}

PALETTE_2 = {
    'background': (0, 0, 30, 20),
    'cells_my': (255, 255, 0, 0),
    'cells_computer': (255, 0, 255, 0)
}

PALETTES = (PALETTE_1, PALETTE_2)


class TikTakToe:

    def __init__(self):
        rand_numb = random.randrange(len(PALETTES))
        palette = PALETTES[rand_numb]
        self.background_color = palette['background']  # background
        self.first_player_color = palette['cells_my']
        self.second_player_color = palette['cells_computer']
        self.board = list(range(1, 10))
        self.flag_exit = False
        self.tmp = False
        self.win_coord = (0, 0, 0)

    def draw_board(self, strip):
        print("-" * 13)
        for i in range(3):
            print("|", self.board[0 + i * 3], "|", self.board[1 + i * 3], "|", self.board[2 + i * 3], "|")
            print("-" * 13)
        r, g, b, w = (0, 0, 0, 0)
        for i in range(16):  # PLAYING FIELD BORDER
            for j in (0, 1, 14, 15):
                strip.setPixelColor(useful_box.LEDS_ORDER[i][j], Color(r, g, b, w))
                strip.setPixelColor(useful_box.LEDS_ORDER[j][i], Color(r, g, b, w))
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
                            strip.setPixelColor(useful_box.LEDS_ORDER[k][m], Color(r, g, b, w))
                else:
                    w += 30
                    for k in range(i * 4 + 2, i * 4 + 6):
                        for m in range(j * 4 + 2, j * 4 + 6):
                            strip.setPixelColor(useful_box.LEDS_ORDER[k][m], Color(r, g, b, w))
        for i in range(3):  # X or O
            for j in range(3):
                if self.board[j + i * 3] == 'X':
                    r = self.first_player_color[0]
                    g = self.first_player_color[1]
                    b = self.first_player_color[2]
                    w = self.first_player_color[3]
                    for k in range(i * 4 + 2, i * 4 + 6):
                        for m in range(j * 4 + 2, j * 4 + 6):
                            strip.setPixelColor(useful_box.LEDS_ORDER[k][m], Color(r, g, b, w))
                elif self.board[j + i * 3] == 'O':
                    r = self.second_player_color[0]
                    g = self.second_player_color[1]
                    b = self.second_player_color[2]
                    w = self.second_player_color[3]
                    for k in range(i * 4 + 2, i * 4 + 6):
                        for m in range(j * 4 + 2, j * 4 + 6):
                            strip.setPixelColor(useful_box.LEDS_ORDER[k][m], Color(r, g, b, w))
        strip.show()

    def draw_endgame(self, strip):
        for i in range(16):
            for j in range(16):
                if self.tmp == 'X':
                    r = self.first_player_color[0]
                    g = self.first_player_color[1]
                    b = self.first_player_color[2]
                    w = self.first_player_color[3]
                elif self.tmp == 'O':
                    r = self.second_player_color[0]
                    g = self.second_player_color[1]
                    b = self.second_player_color[2]
                    w = self.second_player_color[3]
                else:
                    r = self.background_color[0]
                    g = self.background_color[1]
                    b = self.background_color[2]
                    w = self.background_color[3] + 30
                strip.setPixelColor(useful_box.LEDS_ORDER[i][j], Color(r, g, b, w))
            time.sleep(0.05)
            strip.show()
        time.sleep(1)

    def draw_win(self, strip):
        if self.tmp == 'X':
            r = self.first_player_color[0]
            g = self.first_player_color[1]
            b = self.first_player_color[2]
            w = self.first_player_color[3]
        else:
            r = self.second_player_color[0]
            g = self.second_player_color[1]
            b = self.second_player_color[2]
            w = self.second_player_color[3]
        r0, g0, b0, w0 = (0, 0, 0, 0)
        for t in range(6):
            for c in self.win_coord:
                i = c // 3
                j = c % 3
                for k in range(i * 4 + 2, i * 4 + 6):
                    for m in range(j * 4 + 2, j * 4 + 6):
                        if t % 2 == 0:
                            if k == i * 4 + 2 or k == i * 4 + 6 - 1 or m == j * 4 + 2 or m == j * 4 + 6 - 1:
                                strip.setPixelColor(useful_box.LEDS_ORDER[k][m], Color(r0, g0, b0, w0))
                            else:
                                strip.setPixelColor(useful_box.LEDS_ORDER[k][m], Color(r, g, b, w))
                        else:
                            strip.setPixelColor(useful_box.LEDS_ORDER[k][m], Color(r, g, b, w))
            strip.show()
            time.sleep(0.25)

    def take_input(self, player_token):
        print("Where to put " + player_token + "? ")
        while True:
            player_answer = 0
            active_cells = 0
            useful_box.data_processing(useful_box.BUF_TIK_TAK_TOE)
            for i in range(8):
                for j in range(8):
                    if useful_box.cells[i][j] == 1:
                        active_cells += 1
            if active_cells >= useful_box.EXIT_COUNT:
                self.flag_exit = True
                break
            else:
                for i in range(len(useful_box.CELLS_TIK_TAK)):
                    dry_cells = 0
                    for sens in useful_box.CELLS_TIK_TAK[i]:
                        if useful_box.dry_data[sens[0]][sens[1]] == 1:
                            dry_cells += 1
                    if dry_cells >= 3:
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
            useful_box.soft_up_brightness(strip)
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
                        self.draw_win(strip)
                        print(useful_box.ANSI_YELLOW + self.tmp + " WINS!" + useful_box.ANSI_RESET)
                        break
                    if counter == 9:
                        print(useful_box.ANSI_YELLOW + "TALL!" + useful_box.ANSI_RESET)
                        break
            time.sleep(0.25)
            if self.flag_exit:
                print(useful_box.ANSI_GREEN + 'QUIT GAME!' + useful_box.ANSI_RESET)
                self.tmp = ''
            self.draw_endgame(strip)
            useful_box.soft_down_brightness(strip)
            self.board = list(range(1, 10))
