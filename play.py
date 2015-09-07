from collections import Counter
import argparse

import numpy as np

import gamestate
import players

def play(player1, player2):
    gs = gamestate.GameState(debug=False)
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
results = []
for i in range(10000):
    results.append(play(players.BasicPlayer(0), players.BasicPlayer(1)))


print np.average(results), "+-/", np.std(results), Counter(results)[24], Counter(results)[25]
