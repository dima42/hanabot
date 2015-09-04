class Player(object):
    def __init__(self, num):
        self.num = num

    def get_move(self, game_state):
        pass
        # overload this

class Daredevil(Player):
    # always plays oldest card
    def get_move(self, game_state):
        return ("play", 0)

class BasicPlayer(Player):
    # plays newest if just clued
    # else clues if partner has playable/cluable card
    # else discards

    def get_move(self, game_state):
        # is there a card that was just clued?
        for i in range(4, 0, -1):
            card = game_state.player_cards[self.num][i]
            if card[1][0] == 1 or card[1][1] == 1:
                return ("play",  i)

        # is there a playable+cluable card?
        if game_state.clues > 0:
            for i in range(4, 0, -1):
                partner_card = game_state.player_cards[(self.num+1)%2][i]
                stack_level = game_state.stacks[partner_card[0][0]]
                if int(partner_card[0][1]) == stack_level+1:
                    # will this clue interfere with something earlier?
                    color_used = False
                    number_used = False
                    for j in range(4, i, -1):
                        conflict_card = game_state.player_cards[(self.num+1)%2][j]
                        same_color = conflict_card[0][0] == partner_card[0][0]
                        color_used = same_color or color_used
                        same_number = conflict_card[0][1] == partner_card[0][1]
                        number_used = same_number or number_used
                    if not color_used:
                        return ("clue", partner_card[0][0])
                    if not number_used:
                        return ("clue", partner_card[0][1])

        # discard
        return ("discard", 4)

