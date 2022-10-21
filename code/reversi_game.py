import argparse
from rpi_ws281x import *
from Reversi.game import Game


class Reversi:

    def __init__(self):
        self.first_player_color = (0, 255, 0, 0)
        self.second_player_color = (0, 0, 255, 0)
        self.flag_exit = False

    def play(self, strip):
        """ Reversi game with human player vs AI player."""
        parser = argparse.ArgumentParser()
        parser.add_argument('--timeout', help="Number of seconds the brain is allowed to think before making its move.",
                            type=int, default=1)
        parser.add_argument('--display-moves', help="Whether legal moves should be displayed or not.",
                            action='store_true')
        parser.add_argument('--colour', help="Display the game in 256 colours.", action='store_true')
        parser.add_argument('--player', help="If you want to play against the ai", action='store_true')
        parser.add_argument('--ai', help="If you want the ais to play against each other", action='store_true')
        parser.add_argument('--verify', help="Verify AI using a random player", action='store_true')
        args = parser.parse_args()
        if args.timeout < 0:
            exit()
        players = []
        if args.player:
            players = ['player', 'ai']
        if args.ai:
            players = ['ai', 'ai']
        elif args.verify:
            players = ['ai', 'random']
        if not players:
            players = ['player', 'ai']
        game = Game(timeout=args.timeout,
                    display_moves=args.display_moves,
                    colour=args.colour,
                    players=players)
        game.run(strip, True)
