#!/usr/bin/env python3

import random
import time
# creating deck of cards
faces = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
suits = ["H", "S", "D", "C"]

values = {
        "2": 2,
        "3": 3,
        "4": 4,
        "5": 5,
        "6": 6,
        "7": 7,
        "8": 8,
        "9": 9,
        "10": 10,
        "J": 10,
        "Q": 10,
        "K": 10,
        "A": 11,
        }

deck = []
#adds every possible card into a deck
for n in faces:
    for suit in suits:
        deck.append((n , suit))
#creates shoe containing 6 decks
shoe = deck * 6
random.shuffle(shoe)

class Hand:
    def __init__(self): # each hand will have cards and a score. SIMPLE
        self.cards = []
        self.score = self.calcScore()

    def calcScore(self): #This should account for all possible combination of aces so should work.
        score = 0
        num_aces = 0
        for card in self.cards:
            face_value = card[0]
            score += values[face_value]
            if face_value == "A":
                num_aces += 1

        while score > 21 and num_aces > 0:
            score -= 10
            num_aces -= 1

        self.score = score

        return score
    
    def addCard(self): #adds card to hand when necessary
        self.cards.append(shoe[0])
        shoe.pop(0)
        self.calcScore()


    def __str__(self):
        return f': {" ".join("".join(card) for card in self.cards)} : {self.score}'
