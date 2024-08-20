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

    def spl(self):
        # this right here basically creates a new hand for that player
        card1 = self.cards[0]
        card2 = self.cards[1]
        self.cards.pop(1)
        print(self)
        time.sleep(0.5)
        self.addCard()
        time.sleep(0.5)
        print(self)
        new = Hand()
        new.cards.append(card2)
        time.sleep(0.5)
        print(new)
        new.addCard()
        time.sleep(0.5)
        print(new)
        return new


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
    
    def split(self, h): #splitting works BUT only allows to do it once
        new = self.hands[h].spl()
        self.addHand(new)
        self.cash -= self.bet
        self.bet * 2
        
        #this adds the new hand to the players hands which works beautifully
        # now the tricky part begins
        # how to make it loop ??
        # i found out that some casinos only allow 1 split so i will be that type of casino lol
        # if i want to add infinite splits i can tbh

        for i in range(len(self.hands)):
            print(f'hand {i + 1} {self.hands[i]}')
        for i in range(len(self.hands)):
            hand = self.hands[i]
            choice = input(f'${self.cash} | {self.name}, hand {i + 1} -- {self.hands[i]} -- choose to (s)tand, (d)ouble, or (h)it: ')
            valid = False
            while not valid:
                if choice.lower() == "s":
                    valid = True
                    continue
                elif choice.lower == "d":
                    valid = True
                    double = self.double(i)
                    if double == 1:
                        valid = False
                    else:
                        continue
                elif choice.lower() == "h":
                    valid = True
                    self.hit(i)
                    while self.hands[i].score < 21 and choice == "h" and self.hands[i].score > 0:
                        choice = input("(h)it or (s)tand: ")
                        if choice == "h":
                            self.hit(i)
                        elif choice == "s":
                            continue
                        else:
                            print("Invalid Choice")
                            choice = "h"
                        continue
                else:
                    print("-INVALID CHOICE-")
                    valid = False
                    choice = input(f'{self} Choose to (s)tand, (d)ouble, or (h)it: ')

                    

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


class Game:

    def __init__(self):
        self.players = {}
        self.dealer = Dealer()

    def addPlayer(self, other):
        self.players[other.name] = other

    def dealCards(self):
        for name, player in self.players.items():
            hand = Hand()
            player.addHand(hand)
        dHand = Hand()
        self.dealer.addHand(dHand)
        for i in range(2):
            for name, player in self.players.items():
                curr = player.hands[0]
                curr.addCard()
                if i == 2 and curr.score == 21:
                    player.blackjack = True
                time.sleep(1)
                print(player)

            self.dealer.dHand.addCard()
        self.action()

    def bets(self):
        for name, player in self.players.items():
            bet = int(input(f'${player.cash} | {name} please enter your bet: '))
            while bet > player.cash:
                bet = int(input("-Insufficient Funds-\n{name} please enter your bet: "))
            player.bet = bet
            player.cash -= player.bet

    def action(self):
        time.sleep(1)
        print(f'{self.dealer.name} : {"".join(self.dealer.dHand.cards[0])}, ?? : {self.dealer.dHand.score - values[self.dealer.dHand.cards[1][0]]}')
        time.sleep(1)
        for name, player in self.players.items():
            for i in range(len(player.hands)):
                if values[player.hands[i].cards[0][0]] == values[player.hands[i].cards[1][0]] and player.cash >= player.bet:
                    choice = input(f'{name}, hand {i + 1} -- {player.hands[i]} -- Choose to (s)tand, (d)ouble, (h)it, or (sp)lit: ')
                    time.sleep(1)
                else:
                    choice = input(f'{name}, hand {i + 1} -- {player.hands[i]} -- Choose to (s)tand, (d)ouble, or (h)it: ')
                    time.sleep(1)
                valid = False
                while not valid:
                    if choice.lower() == "s":
                        valid = True
                        continue
                    elif choice.lower() == "d":
                        valid = True
                        double = player.double(i)
                        if double == 1:
                            valid = False
                        else:
                            continue
                    elif choice.lower() == "h":
                        valid = True
                        player.hit(i)
                        while player.hands[i].score < 21 and choice == "h" and player.hands[i].score > 0:
                            choice = input("(h)it or (s)tand: ")
                            if choice == "h":
                                player.hit(i)
                            elif choice == "s":
                                continue
                            else:
                                print("Invalid Choice")
                                choice = "h"

                        continue
                    elif choice.lower() == "sp" and values[player.hands[i].cards[0][0]] == values[player.hands[i].cards[0][0]]:
                        valid = True
                        player.split(i)
                        print(player)
                        continue
                    else:
                        print("-INVALID CHOICE-")
                        valid = False
                    choice = input(f'{name} Choose to (s)tand, (d)ouble, or (h)it: ')

        self.dealer.play()
        self.winners()


    def winners(self):
        dealerScore = self.dealer.dHand.score
        for name, player in self.players.items():
            for i in range(len(player.hands)):
                playerScore = player.hands[i].score
                print(f'{name}, hand {i + 1}')
                time.sleep(1)
                if playerScore > dealerScore and playerScore == 21 and len(player.hands[i].cards) == 2:
                    print(f"BLACKJACK FOR {name}, hand {i + 1} !!!")
                    time.sleep(1)
                    player.blackjack()
                elif playerScore > dealerScore:
                    print(f'{name} beats Dealer, hand {i + 1}')
                    time.sleep(1)
                    player.win()
                elif playerScore < dealerScore:
                    print(f'Dealer beats {name}, hand {i + 1}')
                    time.sleep(1)
                    player.lose()
                else:
                    print(f'Push!')
                    time.sleep(1)
                    player.push()
        self.clearHands()





    def clearHands(self):

        for name, player in self.players.items():
            player.rmCards()

p1 = Player("player1", 300)
p2 = Player("player2", 400)
p3 = Player("player3", 400)

game = Game()
game.addPlayer(p1)
game.addPlayer(p2)
game.addPlayer(p3)


while True:
    game.bets()
    game.dealCards()