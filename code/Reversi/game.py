import os
from collections import deque
from Reversi.board import Board
from Reversi.controllers import PlayerController, AiController
from Reversi.random_controller import RandomController
from Reversi.settings import *

import useful_box
import time

class Game(object):
    """Game ties everything together. It has a board,
    two controllers, and can draw to the screen."""

    def __init__(self, timeout=1,
                 display_moves=True,
                 players=['ai', 'ai'],
                 colour=False):

        self.board = Board(colour)
        self.flag_exit = False
        self.timeout = timeout
        self.ai_counter = 0
        self.list_of_colours = [BLACK, WHITE]
        self.players = players
        self.display_moves = display_moves
        self.controllers = deque([self._make_controller(c, p) for c, p in zip(self.list_of_colours, self.players)])
        self.player = self.controllers[0].get_colour()
        self.board.set_black(4, 3)
        self.board.set_black(3, 4)
        self.board.set_white(4, 4)
        self.board.set_white(3, 3)
        self.board.mark_moves(self.player)
        self.previous_move = None
        self.previous_round_passed = False

    def _make_controller(self, colour, controller_type):
        """ Returns a controller with the specified colour.
            'player' == PlayerController,
            'ai' == AiController.
        """
        if controller_type == 'player':
            return PlayerController(colour)
        elif controller_type == 'random':
            return RandomController(colour)
        else:
            self.ai_counter += 1
            return AiController(self.ai_counter, colour, self.timeout)

    def show_info(self):
        """ Prints game information to stdout.
        """
        self.player = self.controllers[0].get_colour()
        print("Playing as:       " + self.player)
        print("Displaying moves: " + str(self.display_moves))
        print("Current turn:     " + str(self.controllers[0]))
        print("Number of Black:  " + str(
            len([p for p in self.board.pieces if p.get_state() == BLACK])))
        print("Number of White:  " + str(
            len([p for p in self.board.pieces if p.get_state() == WHITE])))

    def show_board(self, strip, flag_SetUpBrightness):
        """ Prints the current state of the board to stdout.
        """
        self.board.mark_moves(self.player)
        print(self.board.draw(strip, flag_SetUpBrightness))
        
        

    def show_commands(self):
        """ Prints the possible moves to stdout.
        """
        moves = [self.to_board_coordinates(piece.get_position()) for piece in self.board.get_move_pieces(self.player)]

        if not moves:
            raise NoMovesError

        print("Possible moves are: ", moves)
        self.board.clear_moves()

    def run(self, strip, flag_SetUpBrightness):
        """ The game loop will print game information, the board, the possible moves, and then wait for the
            current player to make its decision before it processes it and then goes on repeating itself.
        """
        while True:
            #os.system('clear')
            self.show_info()
            self.show_board(strip, flag_SetUpBrightness)
            if flag_SetUpBrightness:
                flag_SetUpBrightness = False
            try:
                self.show_commands()
                next_move = self.controllers[0].next_move(self.board)
                if next_move == 'exit':
                    useful_box.slide_leds(strip, (0, 0, 0, 100))
                    time.sleep(1)
                    useful_box.soft_down_brightness(strip)
                    break
                self.board.make_move(next_move, self.controllers[0].get_colour())
                self.previous_round_passed = False
            except NoMovesError:
                if self.previous_round_passed:
                    print("Game Over")
                    blacks = len([p for p in self.board.pieces if p.get_state() == BLACK])
                    whites = len([p for p in self.board.pieces if p.get_state() == WHITE])

                    if blacks > whites:
                        print("Black won this game.")
                        time.sleep(1)
                        useful_box.soft_down_brightness(strip)
                        
                        useful_box.soft_up_brightness(strip)
                        time.sleep(5)
                        useful_box.soft_down_brightness(strip)
                        break
                    elif blacks == whites:
                        print("This game was a tie.")
                        time.sleep(1)
                        useful_box.soft_down_brightness(strip)
                        useful_box.slide_leds(strip, (0, 0, 0, 255))
                        useful_box.soft_up_brightness(strip)
                        time.sleep(5)
                        useful_box.soft_down_brightness(strip)
                        break
                    else:
                        print("White won this game.")
                        time.sleep(1)
                        useful_box.soft_down_brightness(strip)
                        useful_box.slide_leds(strip, (255, 0, 0, 0))
                        useful_box.soft_up_brightness(strip)
                        time.sleep(5)
                        useful_box.soft_down_brightness(strip)
                        break
                else:
                    self.previous_round_passed = True

            self.controllers.rotate()

            print("Current move is: ", self.to_board_coordinates(next_move))

            self.previous_move = next_move

    def to_board_coordinates(self, coordinate):
        """ Transforms an (x, y) tuple into (a-h, 1-8) tuple.
        """
        x, y = coordinate
        return '{0}{1}'.format(chr(ord('a') + x), y + 1)
