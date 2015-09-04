import itertools
import random

import numpy as np

import players

class GameState:

    def __init__(self):
        self.done = False
        self.deal()
        self.clues = 8
        self.bombs = 0
        self.stacks = {c: 0 for c in 'bgrwy'}

    def deal(self):
        self.deck = list(itertools.product('bgrwy', '1112233445'))
        self.deck = ["".join(j) for j in self.deck]
        random.shuffle(self.deck)
        self.deck.insert(0, -1) # hack for not ending game until player 2 goes
        # a card is ('cn', (int, int)) where c = color, n=number
        # and the ints are either -1 for not clued or age of clue
        self.player_cards = [[], []]
        for i in range(5):
            self.player_cards[0].append((self.deck.pop(), [-1, -1]))
            self.player_cards[1].append((self.deck.pop() ,[-1, -1]))

    def print_state(self):
        print self.deck, self.player_cards, self.stacks, self.bombs, self.clues

    def draw(self, player_num, card_num):
        # shift over cards
        newer_cards = self.player_cards[player_num][card_num+1:]
        self.player_cards[player_num][card_num:] = newer_cards
        self.player_cards[player_num].append((self.deck.pop(), [-1, -1]))


    def play_move(self, move, player_num):
        if move[0] == 'play':
            self.put_down_card(self.player_cards[player_num][move[1]])
            self.draw(player_num, move[1])

        if move[0] == 'discard':
            self.draw(player_num, move[1])
            self.clues = min(self.clues+1, 8) 

        if move[0] == 'clue':
            self.clues -= 1
            for card in self.player_cards[(player_num+1)%2]:
                for i in (0, 1):
                    if card[0][i] == move[1]:
                        card[1][i] = 0

        # update age of clues
        for p_num in (0, 1):
            for c_num in range(5):
                for c_aspect in (0, 1):
                    if self.player_cards[p_num][c_num][1][c_aspect] > -1:
                        self.player_cards[p_num][c_num][1][c_aspect] += 1

        self.done = self.bombs == 3 or len(self.deck) == 0

    def put_down_card(self, card):
        color = card[0][0]
        number = int(card[0][1])
        if self.stacks[color] == number-1:
            self.stacks[color] += 1
            if number == '5':
                self.hints = min(self.hints+1, 8)
        else:
            self.bombs += 1

def play(player1, player2):
    gs = GameState()
    current_player = player1
    while not gs.done:
        move = current_player.get_move(gs)
        gs.play_move(move, 0 if current_player == player1 else 1)
        current_player = player2 if current_player == player1 else player1
    return sum(gs.stacks.values())    

results = []
for i in range(1000):
    results.append(play(players.BasicPlayer(0), players.BasicPlayer(1)))

print np.average(results), "+-/", np.std(results) 
