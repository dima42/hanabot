from collections import Counter

import util

class Player(object):
    def __init__(self, num):
        self.num = num

    def get_move(self, game_state):
        pass
        # overload this

class BasicPlayer(Player):
    # plays newest if just clued
    # else clues if partner has playable/cluable card
    # else discards

    def get_move(self, gamestate):
        jc =  util.newest_just_clued(gamestate.player_cards[self.num], gamestate)
        if jc:
            return ('play', jc)

        if gamestate.clues > 0:
            pc = util.partner_playable_clue(
                partner_cards=gamestate.player_cards[(self.num+1)%2],
                gamestate=gamestate,
                ordering='newest',
                full_knowledge=False,
            )
            if pc:
                return ('clue', pc)

        dis = util.get_discard(
            gamestate.player_cards[self.num],
            gamestate,
            ordering='oldest'
        )
        return ('discard', dis)
