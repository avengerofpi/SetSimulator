#!/usr/bin/python3

"""
TODO:
    use the numbrDict, etc's for nice printing (maybe just in debug prints???)
    Better OOP...globals, sometimes functions return, sometimes not...
"""

from random import shuffle
from itertools import product
from time import time, sleep
from collections import defaultdict
from math import log10

debug = True

numbrDict = { 0: "One",     1: "Two",      2: "Three" }
shapeDict = { 0: "Diamond", 1: "Squiggle", 2: "Oval"}
shadeDict = { 0: "Solid",   1: "Stripe",   2: "Open" }
colorDict = { 0: "Red",     1: "Green",    2: "Color-blind Blue" }

dealSize_init = 12
dealSize_add = 3
dealMoreCardsThreshold = dealSize_init

def debugPrint(args):
    if debug:
        print(args)
        sleep(0.01)

def newShuffledDeck():
    debugPrint("shuffing a new deck")
    deck = [card for card in product(range(3), range(3), range(3), range(3))]
    shuffle(deck)
    return deck

# The return of the function is for loop control later on. The global variable is used directly.
setsFound = None
def updateSetsFound(hand):
    setsFound = list()
    setsFound = (hand[:3])

    debugPrint("looking for new sets")
    debugPrint("  found sets: {}".format(setsFound))

    return setsFound

def removeRandomSetFromHand(hand):
    # 'hand' is updated in-place, no return necessary
    # meh, just grab the first set found
    set = setsFound[0]
    debugPrint("removing a set that was found: {}".format(set))
    for card in set:
        hand.remove(card)

# Give the player another batch of cards.
def dealMoreCards(hand, deck):
    newCards = deck[0:dealSize_add]
    hand.append(newCards)
    deck = deck[dealSize_add:]
    debugPrint("dealing more cards: {}".format(newCards))
    return hand, deck

# Play a single round or Set, starting with a new shuffled deck.
# Include a timer mechanism to kill the round if it's taking too  long.
maxPlayDuration = 10 # seconds
def playOneRound():
    debugPrint("playing a new round")
    # Return number of cards left in play at the end
    deck = newShuffledDeck()
    hand = deck[0:dealSize_init]
    deck = deck[dealSize_init:]

    debugPrint("new hand: {}".format(hand))

    # Play until no more deck and no more sets can be found
    # Perform the updateSetsFound() function first to ensure it is always run (beware shortcircuiting!)
    startTime = time()
    maxEndTime = startTime + (maxPlayDuration * 1000)
    while updateSetsFound(hand) or (len(deck) == 0):
        if time() > maxEndTime:
            raise RuntimeError("The current round is taking too long - max runtime is {} seconds".format(maxPlayDuration))
        if setsFound:
            debugPrint("{} sets found, proceed to remove one...".format(len(setsFound)))
            removeRandomSetFromHand(hand)
        else:
            debugPrint("NO sets found...")
            if len(deck) == 0:
                debugPrint("we are done")
                # No sets and no more cards to deal. This round is done.
                break
        if (not setsFound) or (len(hand) < dealMoreCardsThreshold):
            hand, deck = dealMoreCards(hand, deck)
    debugPrint(hand)
    return len(hand)


iters = 1
freqDigits = int(log10(iters))
freqDict = defaultdict(int)
for i in range(iters):
    debugPrint("beginning iteration {0:>{1}d}".format(i, freqDigits))
    freqDict[playOneRound()] += 1

for (size, freq) in sorted(freqDict.items()):
    debugPrint("Size: {0:>2d}  Freq: {1:>{2}d}".format(size, freq, freqDigits))

