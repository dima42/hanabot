from collections import Counter
import itertools
import random



class GameState(object):

    class Card(object):
        """
        each card has a color, number, and how long the card has been clued
        the clue age is -1 if the clue has not been given,
        becomes 1 when the card is clued, and increments at end of own turn
        when the update_age() function is called on all cards
        """

        def __init__(self, color, number):
            self.color = color
            self.number = number
            self.turns_color_clued = -1
            self.turns_number_clued = -1
            self.turns_in_hand = 0

        @property
        def color_clued(self):
            return self.turns_color_clued != -1

        @property
        def number_clued(self):
            return self.turns_number_clued != -1

        def apply_clue(self, clue):
            if not self.color_clued and clue == self.color:
                self.turns_color_clued = 1
            if not self.number_clued and clue == self.number:
                self.turns_number_clued = 1

        def update_age(self):
            self.turns_color_clued += 1 if self.turns_color_clued != -1 else 0
            self.turns_number_clued += 1 if self.turns_number_clued != -1 else 0
            self.turns_in_hand += 1

    def __init__(self, debug):
        self.debug=debug
        self.done = False
        self.deal()
        self.clues = 8
        self.bombs = 0
        self.stacks = {c: 0 for c in 'bgrwy'}

    def deal(self):
        if self.debug:
            random.seed(10)
        card_generator = itertools.product('bgrwy', '1112233445')
        self.deck = [self.Card(j[0], int(j[1])) for j in card_generator]
        random.shuffle(self.deck)
        # hack for allowing each player a move after last card has been drawn
        self.deck.insert(0, self.Card('b', 10))
        self.deck.insert(0, self.Card('b', 11))
        self.player_cards = [[], []]
        for i in range(5):
            self.player_cards[0].append(self.deck.pop())
            self.player_cards[1].append(self.deck.pop())

    def draw(self, player_num, card_num):
        # shift over cards
        newer_cards = self.player_cards[player_num][card_num+1:]
        self.player_cards[player_num][card_num:] = newer_cards
        self.player_cards[player_num].append(self.deck.pop())

    def play_move(self, move, player_num):
        if self.debug:
            print move
            print [(c.color, c.number, c.turns_color_clued, c.turns_number_clued) for c in self.player_cards[player_num]]
            print [(c.color, c.number, c.turns_color_clued, c.turns_number_clued) for c in self.player_cards[(player_num+1)%2]]
            print self.stacks
            print
        if move[0] == 'play':
            self.put_down_card(self.player_cards[player_num][move[1]])
            self.draw(player_num, move[1])

        if move[0] == 'discard': 
            self.draw(player_num, move[1])
            self.clues = min(self.clues+1, 8) 

        if move[0] == 'clue':
            self.clues -= 1
            for card in self.player_cards[(player_num+1)%2]:
                card.apply_clue(move[1])

        # update age of clues
        for c_num in range(5):
            self.player_cards[player_num][c_num].update_age()

        self.done = self.bombs == 3 or len(self.deck) == 0

    def put_down_card(self, card):
        if self.stacks[card.color] == card.number-1:
            self.stacks[card.color] += 1
            if card.number == 5:
                self.clues = min(self.clues+1, 8)
        else:
            self.bombs += 1
