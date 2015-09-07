def known_legal(card, gamestate):
    # TODO need to implement discard check here
    legal = False
    return (card.number_clued and card.color_clued and
            gamestate.stacks[card.color] == (card.number - 1))

def known_illegal(card, gamestate):
    illegal = False
    if card.color_clued:
        # TODO need to implement discard check here
        # check if illegal based on color
        legal_nums = [card.number] if card.number_clued else [0,1,2,3,4]
        illegal &= gamestate.stacks[card.color] not in legal_nums
    if card.number_clued:
        # check if this number fits any color
        illegal &= (card.number - 1) not in gamestate.stacks.values()
    return illegal

def newest_just_clued(own_cards, gamestate):
    """
    if exists a card has just been clued and is not known to be illegal to play,
    returns the newest such card
    else returns False
    """
    for i in range(4, -1, -1):
        card = own_cards[i]
        if 1 in (card.turns_color_clued, card.turns_number_clued):
            if not known_illegal(card, gamestate):
                return i
    return False

def partner_playable_clue(partner_cards, gamestate, ordering='newest', full_knowledge=False):
    """
    if partner has a card that can be played, and clued such that it is 
    the newest card clued or it already has one clue:
        if ordering='newest' returns the clue for the newest such card.
        if ordering='oldest', returns clue for the oldest such card 
        (which is still the newest card being clued)
        if ordering='mode', returns a clue for such a card such that the most
        unknown cards get clued
    else returns false
    """
    playable_clues = get_all_playable_clues(
        partner_cards,
        gamestate,
        full_knowledge=full_knowledge
    )
    if not playable_clues:
        return False

    def newest_card_clued(clue):
        for i in range(4, -1, -1):
            card = partner_cards[i]
            #print clue, card.color, card.number, card.color_clued, card.number_clued
            if (clue == card.color and not card.color_clued or
                clue == card.number and not card.number_clued):
                return i
    def num_cards_clued(clue):
        count = 0
        for i in range(4, -1, -1):
            card = partner_cards[i]
            if (clue == card.color and not card.color_clued or
                clue == card.number and not card.number_clued):
                count += 1 
        return count

    if ordering == 'newest':
        # newest = 4, want so want -4 to be smallest num
        playable_clues.sort(key = lambda clue: -newest_card_clued(clue))
    if ordering == 'oldest':
        playable_clues.sort(key = lambda clue: newest_card_clued(clue))
    if ordering == 'mode':
        playable_clues.sort(key = lambda clue: -num_cards_clued(clue))

    return playable_clues[0]


def get_all_playable_clues(partner_cards, gamestate, full_knowledge=False):
    playable_clues = []
    for i in range(4, -1, -1):
        card = partner_cards[i]
        stack_level = gamestate.stacks[card.color]
        if card.number == stack_level + 1:
            # all info already known - don't clue this
            if card.number_clued and card.color_clued:
                continue

            # will this fully identify a card?
            if full_knowledge:
                if card.number_clued:
                    playable_clues.append(card.color)
                elif card.color_clued:
                    playable_clues.append(card.number)
            # will this clue interfere with something newer?
            else:
                color_used = False
                number_used = False
                for j in range(4, i, -1):
                    conflict_card = partner_cards[j]
                    color_used |= conflict_card.color == card.color
                    number_used |= conflict_card.number == card.number
                if not color_used and not card.color_clued:
                    playable_clues.append(card.color)
                if not number_used and not card.number_clued:
                    playable_clues.append(card.number)
    return playable_clues

def known_irrelevant(cards, gamestate):
    # TODO add discard and partner info
    irrelevant = []
    for i in range(4, -1, -1):
        card = cards[i]
        if card.color_clued:
            stack_level = gamestate.stacks[card.color]
            if (stack_level == 5 or
                card.number_clued and card.number <= stack_level):
                irrelevant.append(i)
                break
        if card.number_clued:
            if (card.number-1) <  min(gamestate.stacks.values()):
                irrelevant.append(i)
    return irrelevant

def get_discard(cards, gamestate, ordering='newest'):
    ki = known_irrelevant(cards, gamestate)
    if ki:
        return ki[0]
    it = range(4, -1, -1) if ordering == 'newest' else range(5)
    for i in it:
        if not (cards[i].color_clued or cards[i].number_clued):
            return i
    for i in it:
        if not (cards[i].color_clued and cards[i].number_clued):
            return i
    return 4
