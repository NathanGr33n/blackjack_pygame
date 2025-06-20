# deck.py
# NathanGr33n
# June 20, 2025

import random
import os

SUITS = ['hearts', 'diamonds', 'clubs', 'spades']
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king', 'ace']

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        # Use PNG image path
        self.image_path = os.path.join("assets", "cards", "png", f"{rank}_of_{suit}.png")

    def value(self):
        if self.rank in ['jack', 'queen', 'king']:
            return 10
        elif self.rank == 'ace':
            return 11
        else:
            return int(self.rank)

class Deck:
    def __init__(self):
        self.cards = [Card(suit, rank) for suit in SUITS for rank in RANKS]
        random.shuffle(self.cards)

    def deal(self):
        return self.cards.pop() if self.cards else None
