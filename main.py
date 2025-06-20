# main.py
# NathanGr33n
# June 20, 2025

import pygame
import sys
import os
from deck import Deck

# Setup
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Blackjack")

# Load card back image once
card_back = pygame.image.load(os.path.join("assets", "cards", "png", "back.png")).convert_alpha()
card_back = pygame.transform.scale(card_back, (80, 120))

# Load and scale PNG cards
def load_png_card(path, size=(80, 120)):
    try:
        image = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(image, size)
    except Exception as e:
        print(f"Error loading PNG '{path}': {e}")
        return None

# Draw card with a white frame and drop shadow
def draw_card_with_border(card_surface, x, y, card_size=(80, 120), border_thickness=6):
    if card_surface is None:
        return

    width = card_size[0] + 2 * border_thickness
    height = card_size[1] + 2 * border_thickness

    shadow = pygame.Surface((width, height), pygame.SRCALPHA)
    pygame.draw.rect(shadow, (0, 0, 0, 100), shadow.get_rect(), border_radius=10)
    screen.blit(shadow, (x + 3, y + 3))

    frame = pygame.Surface((width, height), pygame.SRCALPHA)
    pygame.draw.rect(frame, (255, 255, 255), frame.get_rect(), border_radius=10)
    screen.blit(frame, (x, y))

    screen.blit(card_surface, (x + border_thickness, y + border_thickness))

# Draw a hand; optionally hide the first card
def draw_hand(hand, y, hide_first=False):
    for i, card in enumerate(hand):
        x = 100 + i * 100
        if hide_first and i == 0:
            draw_card_with_border(card_back, x, y)
        else:
            card_surface = load_png_card(card.image_path)
            draw_card_with_border(card_surface, x, y)

# Deal initial cards
deck = Deck()
player_hand = [deck.deal(), deck.deal()]
dealer_hand = [deck.deal(), deck.deal()]

# Game loop
running = True
while running:
    screen.fill((0, 128, 0))  # Green felt background

    draw_hand(player_hand, 400)                  # Player's full hand
    draw_hand(dealer_hand, 100, hide_first=True) # Dealer's hand (first card hidden)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()

pygame.quit()
sys.exit()
