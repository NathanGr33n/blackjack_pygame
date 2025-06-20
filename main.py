# main.py
# NathanGr33n
# June 20, 2025

# --------- Library Imports ---------
import pygame                 # Imports the Pygame library for game development
import sys                    # Imports system-specific parameters and functions
import os                     # Imports functions for interacting with the file system
from deck import Deck         # Imports the custom Deck class from deck.py

# --------- Game Window Setup ---------
pygame.init()                 # Initializes all imported Pygame modules
WIDTH, HEIGHT = 800, 600      # Sets the width and height of the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Creates the game window with specified size
pygame.display.set_caption("Blackjack")            # Sets the title of the window
font = pygame.font.SysFont("Arial", 24)            # Defines the font used for displaying text

# --------- Load Card Back Image ---------
card_back = pygame.image.load(os.path.join("assets", "cards", "png", "back.png")).convert_alpha()  # Loads the card back image
card_back = pygame.transform.scale(card_back, (80, 120))  # Resizes the card back image

# --------- Load and Scale Card Images ---------
def load_png_card(path, size=(80, 120)):
    """Loads a PNG card image and scales it to the specified size"""
    try:
        image = pygame.image.load(path).convert_alpha()  # Load image with transparency support
        return pygame.transform.scale(image, size)       # Resize the image
    except Exception as e:
        print(f"Error loading PNG '{path}': {e}")         # Print error if loading fails
        return None

# --------- Draw a Card with Border and Shadow ---------
def draw_card_with_border(card_surface, x, y, card_size=(80, 120), border_thickness=6):
    """Draws a card image with a white frame and shadow effect"""
    if card_surface is None:
        return
    width = card_size[0] + 2 * border_thickness
    height = card_size[1] + 2 * border_thickness

    # Draw shadow
    shadow = pygame.Surface((width, height), pygame.SRCALPHA)
    pygame.draw.rect(shadow, (0, 0, 0, 100), shadow.get_rect(), border_radius=10)
    screen.blit(shadow, (x + 3, y + 3))

    # Draw white border
    frame = pygame.Surface((width, height), pygame.SRCALPHA)
    pygame.draw.rect(frame, (255, 255, 255), frame.get_rect(), border_radius=10)
    screen.blit(frame, (x, y))

    # Draw actual card image
    screen.blit(card_surface, (x + border_thickness, y + border_thickness))

# --------- Draw a Hand of Cards ---------
def draw_hand(hand, y, hide_first=False):
    """Draws a player's or dealer's hand of cards"""
    for i, card in enumerate(hand):
        x = 100 + i * 100
        if hide_first and i == 0:
            draw_card_with_border(card_back, x, y)  # Draw card back for hidden dealer card
        else:
            card_surface = load_png_card(card.image_path)
            draw_card_with_border(card_surface, x, y)

# --------- Calculate Total Hand Value ---------
def calculate_hand_value(hand):
    """Calculates the value of a blackjack hand, adjusting for aces"""
    value = 0
    aces = 0
    for card in hand:
        val = card.value()
        value += val
        if card.rank == 'ace':
            aces += 1
    while value > 21 and aces > 0:
        value -= 10  # Convert ace from 11 to 1 if needed
        aces -= 1
    return value

# --------- Draw Text ---------
def draw_text(text, x, y, color=(255, 255, 255)):
    """Displays text on screen"""
    surface = font.render(text, True, color)
    screen.blit(surface, (x, y))

# --------- Draw a Button ---------
def draw_button(text, rect, color, text_color=(0, 0, 0)):
    """Draws a clickable button with label text"""
    pygame.draw.rect(screen, color, rect)
    draw_text(text, rect[0] + 10, rect[1] + 10, text_color)

# --------- Reset Game State ---------
def reset_game():
    """Starts a new round and deals fresh cards"""
    global deck, player_hand, dealer_hand, player_turn, game_over, winner, player_bet
    deck = Deck()
    player_hand = [deck.deal(), deck.deal()]
    dealer_hand = [deck.deal(), deck.deal()]
    player_turn = True
    game_over = False
    winner = ""
    player_bet = 25  # Set default bet

# --------- Chip Setup ---------
player_chips = 500  # Player's starting chip balance
player_bet = 25     # Default bet for each round

# --------- First Game Setup ---------
reset_game()

# --------- Define Button Areas ---------
hit_button = pygame.Rect(100, 530, 100, 40)
stand_button = pygame.Rect(250, 530, 100, 40)
restart_button = pygame.Rect(500, 530, 120, 40)

# --------- Main Game Loop ---------
running = True
while running:
    screen.fill((0, 128, 0))  # Green table background

    # Draw hands
    draw_hand(player_hand, 400)
    draw_hand(dealer_hand, 100, hide_first=(player_turn and not game_over))

    # Calculate and show scores
    player_value = calculate_hand_value(player_hand)
    dealer_value = calculate_hand_value(dealer_hand if not player_turn else dealer_hand[1:])
    draw_text(f"Player: {player_value}", 100, 370)
    if not player_turn or game_over:
        draw_text(f"Dealer: {calculate_hand_value(dealer_hand)}", 100, 230)

    # Draw chip info
    draw_text(f"Chips: ${player_chips}", 600, 20)
    draw_text(f"Bet: ${player_bet}", 600, 50)

    # Show winner message and restart button
    if game_over:
        draw_text(winner, 500, 370, (255, 215, 0))
        draw_button("Restart", restart_button, (150, 255, 150))

    # Show hit/stand buttons if game is still active
    if player_turn and not game_over:
        draw_button("Hit", hit_button, (200, 200, 200))
        draw_button("Stand", stand_button, (200, 200, 200))

    # Handle button clicks
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False  # Exit game

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if player_turn and not game_over:
                if hit_button.collidepoint(event.pos):
                    player_hand.append(deck.deal())  # Deal card to player
                    if calculate_hand_value(player_hand) > 21:
                        game_over = True
                        player_turn = False
                        winner = "Bust! Dealer Wins."
                        player_chips -= player_bet
                elif stand_button.collidepoint(event.pos):
                    player_turn = False
                    while calculate_hand_value(dealer_hand) < 17:
                        dealer_hand.append(deck.deal())  # Dealer hits until 17+
                    dealer_value = calculate_hand_value(dealer_hand)
                    player_value = calculate_hand_value(player_hand)
                    game_over = True
                    if dealer_value > 21 or player_value > dealer_value:
                        winner = "Player Wins!"
                        player_chips += player_bet
                    elif player_value == dealer_value:
                        winner = "Push! It's a tie."
                    else:
                        winner = "Dealer Wins."
                        player_chips -= player_bet
            elif game_over and restart_button.collidepoint(event.pos):
                if player_chips >= 25:
                    reset_game()
                else:
                    winner = "You're out of chips!"

    # Update screen
    pygame.display.flip()

# --------- Cleanup ---------
pygame.quit()
sys.exit()
