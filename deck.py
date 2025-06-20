# deck.py
# NathanGr33n
# June 20, 2025

#-------------Import Libraries-------------
import random  # Used to shuffle the deck
import os      # Used for file path construction


#------------Define Suits and Ranks--------------
SUITS = ['hearts', 'diamonds', 'clubs', 'spades']
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king', 'ace']

# Card class to represent a single card
class Card:
    def __init__(self, suit, rank):
        self.suit = suit                     # e.g., "hearts"
        self.rank = rank                     # e.g., "queen"
        # Build image path for this card using PNGs
        self.image_path = os.path.join("assets", "cards", "png", f"{rank}_of_{suit}.png")

    # Determine the blackjack values of Cards
    def value(self):
        if self.rank in ['jack', 'queen', 'king']:
            return 10     # Face cards are worth 10
        elif self.rank == 'ace':
            return 11     # Aces start as 11 (can convert to 1)
        else:
            return int(self.rank)  # Number cards have face value

# Deck class to represent a shuffled deck of 52 cards
class Deck:
    def __init__(self):
        # Create all 52 cards (4 suits × 13 ranks)
        self.cards = [Card(suit, rank) for suit in SUITS for rank in RANKS]
        random.shuffle(self.cards)  # Shuffle the deck

    def deal(self):
        # Remove and return the top card, if any remain
        return self.cards.pop() if self.cards else None
