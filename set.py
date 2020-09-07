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
        debugPrint("  Hand size / Deck size: {0:>2d} / {1:2>d}".format(len(self.hand), len(self.mainDeck)))
        debugPrint("  Current Hand: {}".format(self.hand))

    def __init__(self):
        self.deck = [card for card in product(range(3), range(3), range(3), range(3))]
        self.mainDeck = None
        self.hand = None
        self.setsFound = None

    def shuffle(self):
        # Shuffle the deck
        debugPrint("Shuffing the deck")
        shuffle(self.deck)

    def resetGame(self):
        self.debugPrint("Resetting the whole game (deck, mainDeck, hand, setsFound)")
        self.shuffle()
        self.mainDeck = None
        self.hand = None
        self.setsFound = None

    def dealFirstHand(self):
        self.hand = self.mainDeck[0:self.DEAL_SIZE_INIT]
        self.mainDeck = self.mainDeck[self.DEAL_SIZE_INIT:]
        self.debugPrintDetails("First hand has been dealt:")

    def dealMore(self):
        self.hand.extend(self.mainDeck[0:self.DEAL_SIZE_ADD])
        self.mainDeck = self.mainDeck[self.DEAL_SIZE_ADD:]
        self.debugPrintDetails("Dealt {} more cards to hand:".format(self.DEAL_SIZE_ADD))

    def startNewRound(self):
        self.debugPrint("Starting new round")
        self.resetGame()
        self.mainDeck = self.deck
        self.dealFirstHand()

    def removeRandomSetFromHand(self):
        # meh, just grab the first set found
        setToRemove = self.setsFound[0]
        self.debugPrint("Removing a set that was found: {}".format(setToRemove))
        for card in setToRemove:
            self.debugPrint(" Removing card '{}'".format(card))
            self.hand.remove(card)
        self.debugPrintDetails()

    def updateSetsFound(self):
        self.setsFound = list()

        # !!!!! FAKE SET FINDING CODE - FILL IN REAL LOGIC LATER !!!!!
        self.setsFound = (self.hand[:3],)

        self.debugPrint("Looking for new sets")
        self.debugPrint("  Found sets: {}".format(self.setsFound))
        self.debugPrintDetails()

        return self.setsFound


    # Play a single round or Set, starting with a new shuffled deck.
    # Include a timer mechanism to kill the round if it's taking too  long.
    MAX_PLAY_DURATION = 20 # seconds
    def playOneRound(self):
        self.debugPrint("Playing a new round")
        self.startNewRound()

        # Play until no more deck and no more sets can be found
        # Perform the updateSetsFound() function first to ensure it is always run (beware shortcircuiting!)
        startTime = time()
        maxEndTime = startTime + self.MAX_PLAY_DURATION
        self.debugPrint("\n\nstartTime: {}\nendTime:   {}\n\n".format(startTime, maxEndTime))
        while (len(self.hand) and self.updateSetsFound()) or (len(self.mainDeck) > 0):
            currentTime = time()
            secondsLeft = maxEndTime - currentTime
            self.debugPrint("\n\ncurrentTime: {}\nendTime:     {}\nsecondsLeft: {}\n\n".format(currentTime, maxEndTime, secondsLeft))
            if time() > maxEndTime:
                raise RuntimeError("The current round is taking too long - max runtime is {} seconds".format(self.MAX_PLAY_DURATION))
            if self.setsFound:
                self.debugPrint("{} sets found, proceed to remove one...".format(len(self.setsFound)))
                self.removeRandomSetFromHand()
            else:
                self.debugPrint("NO sets found...")
                if len(self.mainDeck) == 0:
                    self.debugPrint("we are done")
                    # No sets and no more cards to deal. This round is done.
                    break
            if (not self.setsFound) or (len(self.hand) < self.DEAL_MORE_CARDS_THRESHOLD ):
                self.dealMore()
        self.debugPrint(self.hand)
        return self.hand

iters = 10
freqDigits = int(log10(iters))
freqDict = defaultdict(int)
set = Set()
for i in range(iters):
    debugPrint("beginning iteration {0:>{1}d}".format(i, freqDigits))
    set.playOneRound()
    freqDict[len(set.hand)] += 1

for (size, freq) in sorted(freqDict.items()):
    print("Size: {0:>2d}  Freq: {1:>{2}d}".format(size, freq, freqDigits))

