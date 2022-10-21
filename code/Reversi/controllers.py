import datetime
import os
import queue
import threading
import sys
from Reversi.ai import AlphaBetaPruner
from Reversi.brain import Brain
from Reversi.settings import *

import useful_box

__author__ = 'bengt'


class Controller(object):
    """ Interface for different types of controllers of the board
    """

    def next_move(self, pieces):
        """ Will return a single valid move as an (x, y) tuple.
        """
        pass

    def get_colour(self):
        """ Returns the colour of the controller.
        """
        pass


class PlayerController(Controller):
    """ Controller for a real, alive and kicking player.
    """

    def __init__(self, colour):
        self.colour = colour

    def next_move(self, board):
        """ Will return a single valid move as an (x, y) tuple.

            Processes input from the user, parses it, and then returns the
            chosen move if it is valid, otherwise the user can retry sending
            new input until successful.
        """
        coord = None
        while True:
            useful_box.data_processing(useful_box.BUF_REVERSI)
            # time.sleep(0.01)
            
            active_cells = 0
            for i in range(8):
                for j in range(8):
                    if useful_box.cells[i][j] == 1:
                        active_cells += 1                          
                    if useful_box.dry_data[i][j] == 1:
                        coord = [i, j]
                        
            if active_cells >= useful_box.EXIT_COUNT:
                coord = ""
                return 'exit'
                active_cells = 0
            
            elif coord == "":
                print(useful_box.ANSI_CYAN + "Game ended!" + useful_box.ANSI_RESET)
                exit_game = True
                return exit_game
                break
                
            elif coord is not None: 
                if useful_box.battlefield[coord[0]][coord[1]] == 'MM':
                    print(useful_box.battlefield[coord[0]][coord[1]])
                    return tuple(coord)
            coord = None
            
            

    def get_colour(self):
        """ Returns the colour of the controller.
        """
        return self.colour

    def __str__(self):
        return "Player"

    def __repr__(self):
        return "PlayerController"

    @staticmethod
    def _parse_coordinates(x, y):
        """ Parses board coordinates into (x, y) coordinates.
        """
        print(ord(x) - ord('a'), ord(y) - ord('0') - 1)
        return ord(x) - ord('a'), ord(y) - ord('0') - 1


stdoutmutex = threading.Lock()
workQueue = queue.Queue(1)
threads = []


class AiController(Controller):
    """ Artificial Intelligence Controller.
    """

    def __init__(self, id, colour, duration):
        self.id = id
        self.colour = colour
        self.duration = duration

    def next_move(self, board):
        """ Will return a single valid move as an (x, y) tuple.

            Will create a new Brain to start a Minimax calculation with
            the Alpha-Beta Pruning optimization to find optimal moves based
            on an evaluation function, in another thread.

            Meanwhile the AiController will output to stdout to show
            that it hasn't crashed.
        """


        brain = Brain(self.duration, stdoutmutex, workQueue, board.pieces, self.colour,
                      BLACK if self.colour is WHITE else WHITE)
        brain.start()

        threads.append(brain)

        print('Brain is thinking ', end='')
        update_step_duration = datetime.timedelta(microseconds=10000)
        goal_time = datetime.datetime.now() + update_step_duration
        accumulated_time = datetime.datetime.now()

        while workQueue.empty():
            if accumulated_time >= goal_time:
                print('.', end='')
                goal_time = datetime.datetime.now() + update_step_duration
                sys.stdout.flush()

            accumulated_time = datetime.datetime.now()

        print()

        for thread in threads:
            thread.join()

        return workQueue.get()

    def get_colour(self):
        """ Returns the colour of the controller.
        """
        return self.colour

    def __str__(self):
        return "Ai"

    def __repr__(self):
        return "AiController[" + self.id + "]"
