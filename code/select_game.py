import useful_box


class SelectedGame:
    def __init__(self):
        self.selected_game = 0
        self.players = False

    def choice_the_game(self, value, players=False):
        self.selected_game = value
        self.players = players

    def start_the_game(self, strip):
        if self.selected_game == 1:
            print(useful_box.ANSI_CYAN + 'YOU SELECTED THE FIRST GAME - CHECKERS' + useful_box.ANSI_RESET)
            useful_box.soft_down_brightness(strip)
            from checkers_game import Checkers
            checkers = Checkers()
            checkers.play(strip)
        elif self.selected_game == 2:
            print(useful_box.ANSI_CYAN + 'YOU SELECTED THE SECOND GAME - TIK TAK TOE' + useful_box.ANSI_RESET)
            useful_box.soft_down_brightness(strip)
            from tiktaktoe_game import TikTakToe
            tik_tak_toe = TikTakToe()
            tik_tak_toe.play(strip)
        elif self.selected_game == 3:
            print(useful_box.ANSI_CYAN + 'YOU SELECTED THE THIRD GAME - REVERSI' + useful_box.ANSI_RESET)
            useful_box.soft_down_brightness(strip)
            from reversi_game import Reversi
            reversi = Reversi()
            reversi.play(strip)

        elif self.selected_game == 0:
            print(useful_box.ANSI_CYAN + '____SERVICE MODE____' + useful_box.ANSI_RESET)
            useful_box.soft_down_brightness(strip)
            from service_mode import ServiceMode
            service = ServiceMode()
            service.play_raw(strip)
        else:
            useful_box.color_leds_error(strip)
            print(useful_box.ANSI_RED + 'Incorrect input. Repeat please' + useful_box.ANSI_RESET)
