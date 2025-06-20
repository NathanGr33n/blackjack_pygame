# main.py
# NathanGr33n
# June 20, 2025

#Library Imports
import pygame #Game Engine
import sys
import os
from deck import Deck #Imports deck class

#Game Engine and Window Setup
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Blackjack")
font = pygame.font.SysFont("Arial", 24)

# Load card back
card_back = pygame.image.load(os.path.join("assets", "cards", "png", "back.png")).convert_alpha()
card_back = pygame.transform.scale(card_back, (80, 120))

#loads png images for cards
def load_png_card(path, size=(80, 120)):
    try:
        image = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(image, size)
    except Exception as e:
        print(f"Error loading PNG '{path}': {e}")
        return None

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

#display cards
def draw_hand(hand, y, hide_first=False):
    for i, card in enumerate(hand):
        x = 100 + i * 100
        if hide_first and i == 0:
            draw_card_with_border(card_back, x, y)
        else:
            card_surface = load_png_card(card.image_path)
            draw_card_with_border(card_surface, x, y)

#calculate value of cards in hand
def calculate_hand_value(hand):
    value = 0
    aces = 0
    for card in hand:
        val = card.value()
        value += val
        if card.rank == 'ace':
            aces += 1
    # Convert Ace from 11 to 1 as needed
    while value > 21 and aces > 0:
        value -= 10
        aces -= 1
    return value

def draw_text(text, x, y, color=(255,255,255)):
    surface = font.render(text, True, color)
    screen.blit(surface, (x, y))

def draw_button(text, rect, color, text_color=(0,0,0)):
    pygame.draw.rect(screen, color, rect)
    draw_text(text, rect[0] + 10, rect[1] + 10, text_color)

# Game setup
deck = Deck()
player_hand = [deck.deal(), deck.deal()]
dealer_hand = [deck.deal(), deck.deal()]
player_turn = True
game_over = False
winner = ""

# Button areas
hit_button = pygame.Rect(100, 530, 100, 40)
stand_button = pygame.Rect(250, 530, 100, 40)

# Game loop
running = True
while running:
    screen.fill((0, 128, 0))  # Green felt background
    draw_hand(player_hand, 400)
    draw_hand(dealer_hand, 100, hide_first=(player_turn and not game_over))

    player_value = calculate_hand_value(player_hand) #player's hand value
    dealer_value = calculate_hand_value(dealer_hand if not player_turn else dealer_hand[1:]) #dealer's hand value

    draw_text(f"Player: {player_value}", 100, 370)
    if not player_turn:
        draw_text(f"Dealer: {calculate_hand_value(dealer_hand)}", 100, 230) #displays dealers score

    if game_over:
        draw_text(winner, 500, 370, (255, 215, 0)) #displays winner text

    if player_turn and not game_over:
        draw_button("Hit", hit_button, (200, 200, 200)) #displays hit button
        draw_button("Stand", stand_button, (200, 200, 200)) #display stand button

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and player_turn and not game_over:
            if hit_button.collidepoint(event.pos):
                player_hand.append(deck.deal())
                player_value = calculate_hand_value(player_hand)
                if player_value > 21: #if player's hand value is greater than 21 (bust)
                    game_over = True
                    player_turn = False
                    winner = "Bust! Dealer Wins."
            elif stand_button.collidepoint(event.pos):
                player_turn = False
                # Dealer's turn
                while calculate_hand_value(dealer_hand) < 17:
                    dealer_hand.append(deck.deal())
                dealer_value = calculate_hand_value(dealer_hand)
                player_value = calculate_hand_value(player_hand)
                game_over = True
                if dealer_value > 21 or player_value > dealer_value: #Win Conditions
                    winner = "Player Wins!"
                elif player_value == dealer_value: #Tie Conditions
                    winner = "Push! It's a tie."
                else:
                    winner = "Dealer Wins."

    pygame.display.flip()

#cleanup
pygame.quit()
sys.exit()
