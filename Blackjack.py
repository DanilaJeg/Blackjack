#!/usr/bin/env python3

import random
import time

def initialize():
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

    return shoe, values
shoe, values = initialize()

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


class Player:
    def __init__(self, name: str, cash: int):
        self.name = name
        self.cash = cash
        self.hands = []

    def addHand(self, other): #adds a hand object to self.hands
        self.hands.append(other)

    def rmCards(self): # resets the hands
        self.hands = []

    def hit(self, i=0): #adds card to a hand (i assume its possible to have more than one hand)
        self.hands[i].addCard()
        print(self)
        if self.hands[i].score > 21:
            print(f"{self.name}, BUST!!")
            self.hands[i].score = -1
    
    def double(self, i): #adds card to hand and doubles the amount bet if possible
        if self.cash < self.bet:
            print("Insufficient Funds.")
            return 1
        self.cash -= self.bet
        self.bet *= 2
        self.hit(i)
        return 0
    
    #TODO add a split method that actually works. 
    
    def blackjack(self): # checking for a blackjack
        winnings = 0
        winnings += self.bet * 2.5
        self.cash += winnings
        print(f'{self.name} wins {winnings}')

    def win(self): #what to do if you won
        winnings = 0
        winnings += self.bet * 2
        self.cash += winnings
        print(f'{self.name} wins {winnings}')


    def lose(self): #what to do if loses
        print(f'{self.name} loses {self.bet}')

    def push(self): #if the game ends in a draw
        self.cash += self.bet

    def __str__(self):
        out = []
        for hand in self.hands:
            out.append(str(hand))

        return f'${self.cash} | {self.name} {"  |||  ".join(out)}'

# inherit from player class
class Dealer(Player):

    def __init__(self): # add a few new attributes
        self.name = "Dealer"
        self.dHand = Hand()

    def play(self): #once everyone put their bets and and their choices the dealer will "reveal" his card and play stopping at 17 or more
        print(self)
        while self.dHand.score < 17 and self.dHand.score > 0:
            self.dHand.addCard()
            self.score = self.dHand.calcScore()
            print(self)
        if self.dHand.score > 21: # if it goes over the score of 21 its a bust meaning score of 0 appointed
            self.dHand.score = 0

    def addHand(self, other):
        self.dHand = other

    def rmCards(self):
        self.dHand = None

    def __str__(self):
        return f'Dealer {self.dHand}'