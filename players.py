from collections import Counter

import util

class Player(object):
    def __init__(self, num, debug=False):
        self.num = num
        self.debug = debug

    def get_move(self, game_state):
        pass
        # overload this

class HumanPlayer(Player):
    def get_move(self, gamestate):
        print gamestate.stacks
        print "partner hand: "
        print [(c.color, c.number, c.color_clued, c.number_clued)
                for c in gamestate.player_cards[(self.num+1)%2]]
        print "own hand: "
        print [(c.color_clued, c.number_clued)
                for c in gamestate.player_cards[(self.num+1)%2]]
        print "enter move: "
        move = raw_input().split(" ")
        move[1] = int(move[1]) if move[1] in '012345' else move[1]
        print move
        return move

class BasicPlayer(Player):
    # plays newest if just clued
    # else clues if partner has playable/cluable card
    # else discards

    def get_move(self, gamestate):
        move = None
        jc =  util.newest_just_clued(gamestate.player_cards[self.num], gamestate)
        if jc:
            move = ('play', jc)

        if gamestate.clues > 0:
            pc = util.partner_playable_clue(
                partner_cards=gamestate.player_cards[(self.num+1)%2],
                gamestate=gamestate,
                ordering='newest',
                full_knowledge=False,
            )
            if pc and not move:
                move = ('clue', pc)

        dis = util.get_discard(
            gamestate.player_cards[self.num],
            gamestate,
            ordering='newest'
        )
        if not move:
            move = ('discard', dis)

        if self.debug:
            print move
        return move

class CardStatePlayer(Player):
    # if a playable card is clued, marks card as known playable by identifying 
    # its other characteristic

    # does not play if partner is about to discard playable card that can be
    # identified, or if partner has 0 known but >=2 existing playable cards
    # picks a card as known playable based on
    # -whether it is a 5 and hints < 4
    # -whether it enables partner card or known own card to be played
    # as a tiebreaker, bigger cards get played first

    def set_known_playable(self, gamestate):
        full_knowledge_generated = False
        for c in gamestate.player_cards[self.num]:
            c.known_playable = util.known_legal(c, gamestate)
            if (c.known_playable and 
                (c.turns_color_clued == 1 or c.turns_number_clued == 1)):
                full_knowledge_generated=True
        jc =  util.newest_just_clued(gamestate.player_cards[self.num], gamestate)
        if jc is not False:
            # we assume this card is marked as playable unless it is known illegal
            card = gamestate.player_cards[self.num][jc]
            if not util.known_illegal(card, gamestate) and not full_knowledge_generated:
                card.known_playable = True
                assert gamestate.stacks[card.color] == (card.number - 1)
                card.turns_color_clued = 1
                card.turns_number_clued = 1
        
    def get_move(self, gamestate):
        move = None

        self.set_known_playable(gamestate)
        for i in range(4, -1, -1):
            card = gamestate.player_cards[self.num][i]
            if card.known_playable:
                move = ('play', i)
                break

        if gamestate.clues > 0:
            pc = util.partner_playable_clue(
                partner_cards=gamestate.player_cards[(self.num+1)%2],
                gamestate=gamestate,
                ordering='mode',
                full_knowledge=True,
            )
            if pc and not move:
                move = ('clue', pc)

        dis = util.get_discard(
            gamestate.player_cards[self.num],
            gamestate,
            ordering='oldest'
        )
        if not move:
            move = ('discard', dis)

        if self.debug:
            print move
        return move
