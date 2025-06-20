# deck.py
# NathanGr33n
# June 20, 2025

import random  # Used to shuffle the deck
import os      # Used for file path operations

# Suits and ranks used in a standard deck
SUITS = ['hearts', 'diamonds', 'clubs', 'spades']
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king', 'ace']

# Represents a single playing card
class Card:
    def __init__(self, suit, rank):
        self.suit = suit  # e.g., "hearts"
        self.rank = rank  # e.g., "queen"
        # Create the path to the image file for this card
        self.image_path = os.path.join("assets", "cards", "png", f"{rank}_of_{suit}.png")

    def value(self):
        """Returns the blackjack value of the card"""
        if self.rank in ['jack', 'queen', 'king']:
            return 10
        elif self.rank == 'ace':
            return 11
        else:
            return int(self.rank)

# Represents a full 52-card deck
class Deck:
    def __init__(self):
        # Build the deck as a list of Card objects (one for each combination)
        self.cards = [Card(suit, rank) for suit in SUITS for rank in RANKS]
        random.shuffle(self.cards)  # Shuffle the deck randomly

    def deal(self):
        """Deals (removes and returns) the top card from the deck"""
        return self.cards.pop() if self.cards else None
