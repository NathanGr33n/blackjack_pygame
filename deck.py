# deck.py
# NathanGr33n
# June 20, 2025

import random #for shuffle

SUITS = ['hearts', 'diamonds', 'clubs', 'spades'] #card suits
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king', 'ace'] #card ranks

#card class
class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.image_path = f"assets/cards/{rank}_of_{suit}.png" #set image for card
	
    #Sets value for j,q,k,a
    def value(self):
        if self.rank in ['jack', 'queen', 'king']:
            return 10
        elif self.rank == 'ace':
            return 11
        else:
            return int(self.rank)

#deck class
class Deck:
    def __init__(self):
        self.cards = [Card(suit, rank) for suit in SUITS for rank in RANKS] #initializes deck of cards
        random.shuffle(self.cards)

    def deal(self):
        return self.cards.pop() if self.cards else None
