#!/usr/bin/python3

"""
TODO:
    use the numbrDict, shapeDict, etc, to add a nice printCard method
    clean up the debugging shit...gawdz!
    call mom
"""

from random import shuffle
from itertools import product, combinations
from time import time, sleep
from collections import defaultdict
from math import log10

iters = 1000
debug = False

# Not used yet...want to produce pretty printing...change to class fields ^_^
numbrDict = { 0: "One",     1: "Two",      2: "Three" }
shapeDict = { 0: "Diamond", 1: "Squiggle", 2: "Oval"}
shadeDict = { 0: "Solid",   1: "Stripe",   2: "Open" }
colorDict = { 0: "Red",     1: "Green",    2: "Color-blind Blue" }

def debugPrint(args):
    if debug:
        print(args)
        sleep(0.025)

class Set:
    NUM_CATEGORIES = 4
    SET_SIZE = 3
    INIT_HAND_SIZE = NUM_CATEGORIES * SET_SIZE
    DRAW_THRESHOLD = INIT_HAND_SIZE
    MAX_PLAY_DURATION = 130 # max seconds / hand
    EXTRA_SHUFFLING = False

    def debugPrint(self, s):
        debugPrint(s)

    def debugPrintDetails(self, s = ""):
        s and self.debugPrint(s)
        debugPrint("  Hand size / Deck size: {0:>2d} / {1:2>d}".format(len(self.hand), len(self.deck)))
        debugPrint("  Current Hand(sorted): {}".format(sorted(self.hand)))

    def __init__(self):
        self.wholeDeck = list(product( *(range(self.SET_SIZE) for _ in range(self.NUM_CATEGORIES)) ))
        self.deck = None
        self.hand = None
        self.setFound = None

    def shuffleWholeDeck(self):
        # Shuffle the deck
        debugPrint("Shuffling the deck")
        shuffle(self.wholeDeck)

    def shuffleHand(self):
        # Shuffle the hand (to help ensure randomness in looking for sets)
        # Using this instead of set.pop() since I'm think(!) that's not necessarily as
        # random (though it is probably more efficient...)
        if self.EXTRA_SHUFFLING:
            debugPrint("Shuffling the hand")
            shuffle(self.hand)

    def resetGame(self):
        self.debugPrint("Resetting the whole game (deck, mainDeck, hand, setFound)")
        self.shuffleWholeDeck()
        self.deck = self.wholeDeck
        self.hand = list()
        self.setFound = None

    def dealCards(self, n):
        self.hand.extend(self.deck[0:n])
        self.deck = self.deck[n:]

    def dealFirstHand(self):
        self.dealCards(self.INIT_HAND_SIZE)
        self.shuffleHand()
        self.debugPrintDetails("First hand has been dealt:")

    def draw(self):
        self.dealCards(self.SET_SIZE)
        self.shuffleHand()
        self.debugPrintDetails("Dealt {} more cards to hand:".format(self.SET_SIZE))

    def startNewRound(self):
        self.debugPrint("Starting new round")
        self.resetGame()
        self.dealFirstHand()

    def removeSetFromHand(self):
        # meh, just grab the first set found
        self.debugPrint("Removing a set that was found: {}".format(self.setFound))
        for card in self.setFound:
            self.debugPrint(" Removing card '{}'".format(card))
            self.hand.remove(card)
        self.debugPrintDetails()

    def lookForASet(self):
        self.setFound = None
        for maybeSet in combinations(self.hand, self.SET_SIZE):
            if all(len({card[i] for card in maybeSet}) in [1, self.SET_SIZE] for i in range(self.NUM_CATEGORIES)):
                self.setFound = maybeSet
                break

        self.debugPrint("Looking for new set")
        self.debugPrint("  Found set: {}".format(self.setFound))
        self.debugPrintDetails()

        return self.setFound


    # Play a single round or Set, starting with a new shuffled deck.
    # Include a timer mechanism to kill the round if it's taking too  long.
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
                errorMsg = """The current round is taking too long - max runtime is {} seconds
Current state:
    Main deck size: {}
    Hand      size: {}""".format(self.MAX_PLAY_DURATION, len(self.deck), len(self.hand))

                self.hand = self.wholeDeck
                print(errorMsg)
                break

                #raise RuntimeError(errorMsg)
            if self.setFound:
                self.debugPrint("{} sets found, proceed to remove one...".format(len(self.setFound)))
                self.removeSetFromHand()
            else:
                self.debugPrint("NO sets found...")
                if len(self.deck) == 0:
                    self.debugPrint("we are done")
                    # No sets and no more cards to deal. This round is done.
                    break
            if (not self.setFound) or (len(self.hand) < self.DRAW_THRESHOLD ):
                self.draw()
        self.debugPrint(self.hand)
        return self.hand

freqDigits = int(log10(iters))
freqDict = defaultdict(int)
game = Set()
print("Running {0:,} trials...".format(iters))
print("  {} cards".format(len(game.wholeDeck)))
print("  {} categories".format(game.NUM_CATEGORIES))
print("  {} set-size".format(game.SET_SIZE))
print("")
print("Shuffle hand after draw: {}".format(game.EXTRA_SHUFFLING))
print("")

print("Timing:")
print("  {}s max play duration / round".format(game.MAX_PLAY_DURATION))
start = time()
for i in range(iters):
    debugPrint("beginning iteration {0:>{1}d}".format(i, freqDigits))
    game.playOneRound()
    freqDict[len(game.hand)] += 1
end = time()
avgTimePerRound = (end - start) / iters
print("  {0:6.3f} seconds per game (avg)".format(avgTimePerRound))
print("")

for (size, freq) in sorted(freqDict.items()):
    percent = freq / iters * 100
    print("Remaining Cards: {0:>2d}    Freq: {1:>{2}d}    Percent: {3:>6.2f}".format(size, freq, freqDigits, percent))

