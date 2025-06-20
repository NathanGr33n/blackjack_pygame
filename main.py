# main.py
# NathanGr33n
# June 20, 2025

import pygame #import game engine
import sys
from deck import Deck #import deck class from deck.py

# Setup
pygame.init()
WIDTH, HEIGHT = 800, 600 #window size variables
screen = pygame.display.set_mode((WIDTH, HEIGHT)) #setting window size
pygame.display.set_caption("Blackjack") #Set Display Caption

# Load card back
card_back = pygame.image.load("assets/cards/back.png")

# Deck setup
deck = Deck()
player_hand = [deck.deal(), deck.deal()]
dealer_hand = [deck.deal(), deck.deal()]

# draw hand method, displays image for cards on screen with y value for location
def draw_hand(hand, y):
    for i, card in enumerate(hand):
        card_image = pygame.image.load(card.image_path)
        screen.blit(card_image, (100 + i * 100, y))

# Game loop
running = True
while running:
    screen.fill((0, 128, 0))  # Green background

    draw_hand(player_hand, 400) #display player's cards
    draw_hand(dealer_hand, 100) #display dealer's cards

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()

#deactivating libraries
pygame.quit()
sys.exit()
