#!/usr/bin/python3

"""
TODO:
    use the numbrDict, etc's for nice printing (maybe just in debug prints???)
    Better OOP...globals, sometimes functions return, sometimes not...
"""

from random import shuffle
from itertools import product, combinations
from time import time, sleep
from collections import defaultdict
from math import log10

iters = 100

numbrDict = { 0: "One",     1: "Two",      2: "Three" }
shapeDict = { 0: "Diamond", 1: "Squiggle", 2: "Oval"}
shadeDict = { 0: "Solid",   1: "Stripe",   2: "Open" }
colorDict = { 0: "Red",     1: "Green",    2: "Color-blind Blue" }

debug = False
def debugPrint(args):
    if debug:
        print(args)
        sleep(0.025)

class Set:
    DEAL_SIZE_INIT = 12
    DEAL_SIZE_ADD = 3
    DEAL_MORE_CARDS_THRESHOLD = DEAL_SIZE_INIT

    def debugPrint(self, s):
        debugPrint(s)

    def debugPrintDetails(self, s = ""):
        s and self.debugPrint(s)
        debugPrint("  Hand size / Deck size: {0:>2d} / {1:2>d}".format(len(self.hand), len(self.deck)))
        debugPrint("  Current Hand(sorted): {}".format(sorted(self.hand)))

    def __init__(self):
        self.wholeDeck = [card for card in product(range(3), range(3), range(3), range(3))]
        self.deck = None
        self.hand = None
        self.setFound = None

    def shuffleDeck(self):
        # Shuffle the deck
        debugPrint("Shuffling the deck")
        shuffle(self.wholeDeck)

    def shuffleHand(self):
        # Shuffle the hand (to help ensure randomness in looking for sets)
        # Using this instead of set.pop() since I'm think(!) that's not necessarily as
        # random (though it is probably more efficient...)
        debugPrint("Shuffling the hand")
        shuffle(self.hand)

    def resetGame(self):
        self.debugPrint("Resetting the whole game (deck, mainDeck, hand, setFound)")
        self.shuffleDeck()
        self.deck = None
        self.hand = None
        self.setFound = None

    def dealFirstHand(self):
        self.hand = self.deck[0:self.DEAL_SIZE_INIT]
        self.deck = self.deck[self.DEAL_SIZE_INIT:]
        self.shuffleHand()
        self.debugPrintDetails("First hand has been dealt:")

    def dealMore(self):
        self.hand.extend(self.deck[0:self.DEAL_SIZE_ADD])
        self.shuffleHand()
        self.deck = self.deck[self.DEAL_SIZE_ADD:]
        self.debugPrintDetails("Dealt {} more cards to hand:".format(self.DEAL_SIZE_ADD))

    def startNewRound(self):
        self.debugPrint("Starting new round")
        self.resetGame()
        self.deck = self.wholeDeck
        self.dealFirstHand()

    def removeSetFromHand(self):
        # meh, just grab the first set found
        self.debugPrint("Removing a set that was found: {}".format(self.setFound))
        for card in self.setFound:
            self.debugPrint(" Removing card '{}'".format(card))
            self.hand.remove(card)
        self.debugPrintDetails()

    def lookForASet(self):
        self.setFound = list()

        # !!!!! FAKE SET FINDING CODE - FILL IN REAL LOGIC LATER !!!!!
        #self.setFound = self.hand[:3]

        for maybeSet in combinations(self.hand, 3):
            if all(len({card[i] for card in maybeSet}) != 2 for i in range(4)):
                self.setFound = maybeSet
                break

        self.debugPrint("Looking for new set")
        self.debugPrint("  Found set: {}".format(self.setFound))
        self.debugPrintDetails()

        return self.setFound


    # Play a single round or Set, starting with a new shuffled deck.
    # Include a timer mechanism to kill the round if it's taking too  long.
    MAX_PLAY_DURATION = 20 # seconds
    def playOneRound(self):
        self.debugPrint("Playing a new round")
        self.startNewRound()

        # Play until the deck is empty and no more sets can be found
        # Perform the '(len(self.hand) and self.lookForASet())' first to ensure it is always run (beware shortcircuiting!)
        startTime = time()
        maxEndTime = startTime + self.MAX_PLAY_DURATION
        self.debugPrint("\n\nstartTime: {}\nendTime:   {}\n\n".format(startTime, maxEndTime))
        while (len(self.hand) and self.lookForASet()) or (len(self.deck) > 0):
            currentTime = time()
            secondsLeft = maxEndTime - currentTime
            self.debugPrint("\n\ncurrentTime: {}\nendTime:     {}\nsecondsLeft: {}\n\n".format(currentTime, maxEndTime, secondsLeft))
            if time() > maxEndTime:
                raise RuntimeError("The current round is taking too long - max runtime is {} seconds".format(self.MAX_PLAY_DURATION))
            if self.setFound:
                self.debugPrint("{} sets found, proceed to remove one...".format(len(self.setFound)))
                self.removeSetFromHand()
            else:
                self.debugPrint("NO sets found...")
                if len(self.deck) == 0:
                    self.debugPrint("we are done")
                    # No sets and no more cards to deal. This round is done.
                    break
            if (not self.setFound) or (len(self.hand) < self.DEAL_MORE_CARDS_THRESHOLD ):
                self.dealMore()
        self.debugPrint(self.hand)
        return self.hand

freqDigits = int(log10(iters))
freqDict = defaultdict(int)
print("Running {} trials...".format(iters))
set = Set()
for i in range(iters):
    debugPrint("beginning iteration {0:>{1}d}".format(i, freqDigits))
    set.playOneRound()
    freqDict[len(set.hand)] += 1

for (size, freq) in sorted(freqDict.items()):
    print("Size: {0:>2d}  Freq: {1:>{2}d}".format(size, freq, freqDigits))

