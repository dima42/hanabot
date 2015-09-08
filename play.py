from collections import Counter
import argparse

import numpy as np

import gamestate
import players

def play(player1, player2, debug=False):
    gs = gamestate.GameState(debug=debug)
    current_player = player1
    while not gs.done:
        move = current_player.get_move(gs)
        gs.play_move(move, 0 if current_player == player1 else 1)
        current_player = player2 if current_player == player1 else player1
    return sum(gs.stacks.values())

"""
# todo: argparse for human play option 
play(players.HumanPlayer(0), players.BasicPlayer(1, debug=True))
"""

parser = argparse.ArgumentParser(description = "Play some Hanabi")
parser.add_argument(
    'player1',
    type=int,
    default=2,
    help='0 for human, 1 for BasicPlayer, 2 for CardStatePlayer'
)
parser.add_argument(
    'player2',
    type=int,
    default=2,
    help='0 for human, 1 for BasicPlayer, 2 for CardStatePlayer'
)
parser.add_argument(
    'numgames',
    type=int,
    default=10000,
)
parser.add_argument(
    '--debug',
    action='store_true'
)

args = parser.parse_args()
results = []
if args.player1 == 0:
    p1 = players.HumanPlayer(0)
elif args.player1 == 1:
    p1 = players.BasicPlayer(0)
elif args.player1 == 2:
    p1 = players.CardStatePlayer(0)
if args.player2 == 0:
    p2 = players.HumanPlayer(1)
elif args.player2 == 1:
    p2 = players.BasicPlayer(1)
elif args.player2 == 2:
    p2 = players.CardStatePlayer(1)

for i in range(args.numgames):
    results.append(play(p1, p2, args.debug))


print np.average(results), "+-/", np.std(results), Counter(results)[24], Counter(results)[25]
