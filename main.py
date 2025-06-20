# main.py
# NathanGr33n
# June 20, 2025

# --------- Library Imports ---------
import pygame                     # Game engine
import sys                        # System functions
import os                         # File path handling
from deck import Deck             # Import the Deck class from deck.py

# --------- Game Setup ---------
pygame.init()                     # Initialize Pygame
WIDTH, HEIGHT = 800, 600          # Window dimensions
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Create the game window
pygame.display.set_caption("Blackjack")            # Set the window title
font = pygame.font.SysFont("Arial", 24)            # Define font for text

# --------- Load Card Back Image ---------
card_back = pygame.image.load(os.path.join("assets", "cards", "png", "back.png")).convert_alpha()  # Load back of card
card_back = pygame.transform.scale(card_back, (80, 120))  # Scale card back to desired size

# --------- Load a PNG Card ---------
def load_png_card(path, size=(80, 120)):
    try:
        image = pygame.image.load(path).convert_alpha()  # Load and convert image with alpha transparency
        return pygame.transform.scale(image, size)       # Scale to standard card size
    except Exception as e:
        print(f"Error loading PNG '{path}': {e}")         # Print error if loading fails
        return None

# --------- Draw a Card with Border and Shadow ---------
def draw_card_with_border(card_surface, x, y, card_size=(80, 120), border_thickness=6):
    if card_surface is None:
        return
    width = card_size[0] + 2 * border_thickness      # Full card width with border
    height = card_size[1] + 2 * border_thickness     # Full card height with border
    shadow = pygame.Surface((width, height), pygame.SRCALPHA)  # Create transparent surface for shadow
    pygame.draw.rect(shadow, (0, 0, 0, 100), shadow.get_rect(), border_radius=10)  # Draw translucent shadow
    screen.blit(shadow, (x + 3, y + 3))               # Offset to simulate drop shadow
    frame = pygame.Surface((width, height), pygame.SRCALPHA)   # Create frame surface
    pygame.draw.rect(frame, (255, 255, 255), frame.get_rect(), border_radius=10)  # Draw white rounded rectangle
    screen.blit(frame, (x, y))                        # Draw frame behind card
    screen.blit(card_surface, (x + border_thickness, y + border_thickness))  # Draw actual card

# --------- Draw a Hand of Cards ---------
def draw_hand(hand, y, hide_first=False):
    for i, card in enumerate(hand):
        x = 100 + i * 100  # Set card X position with spacing
        if hide_first and i == 0:
            draw_card_with_border(card_back, x, y)  # Use card back for first card
        else:
            card_surface = load_png_card(card.image_path)  # Load card face
            draw_card_with_border(card_surface, x, y)       # Draw it

# --------- Calculate Hand Value ---------
def calculate_hand_value(hand):
    value = 0
    aces = 0
    for card in hand:
        val = card.value()     # Get card value
        value += val
        if card.rank == 'ace':
            aces += 1          # Count aces
    while value > 21 and aces > 0:
        value -= 10            # Convert ace from 11 to 1 if needed
        aces -= 1
    return value

# --------- Draw Text on Screen ---------
def draw_text(text, x, y, color=(255, 255, 255)):
    surface = font.render(text, True, color)  # Render text surface
    screen.blit(surface, (x, y))              # Blit to screen

# --------- Draw a Button ---------
def draw_button(text, rect, color, text_color=(0, 0, 0)):
    pygame.draw.rect(screen, color, rect)                    # Draw button rectangle
    draw_text(text, rect[0] + 10, rect[1] + 10, text_color)   # Draw label text

# --------- Reset Game State ---------
def reset_game():
    global deck, player_hand, dealer_hand, player_turn, game_over, winner
    deck = Deck()                               # Create a new shuffled deck
    player_hand = [deck.deal(), deck.deal()]    # Deal two cards to player
    dealer_hand = [deck.deal(), deck.deal()]    # Deal two cards to dealer
    player_turn = True                          # Start with player's turn
    game_over = False                           # Not over yet
    winner = ""                                 # No winner yet

# --------- Initialize First Game ---------
reset_game()

# --------- Define Button Rectangles ---------
hit_button = pygame.Rect(100, 530, 100, 40)
stand_button = pygame.Rect(250, 530, 100, 40)
restart_button = pygame.Rect(500, 530, 120, 40)

# --------- Game Loop ---------
running = True
while running:
    screen.fill((0, 128, 0))  # Fill screen with green (felt table color)

    draw_hand(player_hand, 400)                         # Draw player hand
    draw_hand(dealer_hand, 100, hide_first=(player_turn and not game_over))  # Hide dealer's first card during player turn

    player_value = calculate_hand_value(player_hand)    # Calculate player's total
    dealer_value = calculate_hand_value(dealer_hand if not player_turn else dealer_hand[1:])  # Dealer value (hides one card)

    draw_text(f"Player: {player_value}", 100, 370)      # Show player score
    if not player_turn or game_over:
        draw_text(f"Dealer: {calculate_hand_value(dealer_hand)}", 100, 230)  # Show full dealer score

    if game_over:
        draw_text(winner, 500, 370, (255, 215, 0))       # Display result
        draw_button("Restart", restart_button, (150, 255, 150))  # Show restart button

    if player_turn and not game_over:
        draw_button("Hit", hit_button, (200, 200, 200))    # Hit button
        draw_button("Stand", stand_button, (200, 200, 200))  # Stand button

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False  # Exit the game
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Player clicks during active round
            if player_turn and not game_over:
                if hit_button.collidepoint(event.pos):
                    player_hand.append(deck.deal())        # Deal new card
                    player_value = calculate_hand_value(player_hand)
                    if player_value > 21: # Player Busts (Player's hand value is greater than 21)
                        game_over = True
                        player_turn = False
                        winner = "Bust! Dealer Wins."
                elif stand_button.collidepoint(event.pos):
                    player_turn = False
                    while calculate_hand_value(dealer_hand) < 17:
                        dealer_hand.append(deck.deal())    # Dealer draws
                    dealer_value = calculate_hand_value(dealer_hand)
                    player_value = calculate_hand_value(player_hand)
                    game_over = True
                    if dealer_value > 21 or player_value > dealer_value: #Player Wins (Dealer Busts or Player's hand > Dealers hand)
                        winner = "Player Wins!"
                    elif player_value == dealer_value: #Tie Conditions
                        winner = "Push! It's a tie."
                    else: #Dealer's hand > Players hand
                        winner = "Dealer Wins."
            elif game_over and restart_button.collidepoint(event.pos):
                reset_game()  # Restart game if clicked

    pygame.display.flip()  # Refresh screen

# --------- Cleanup on Exit ---------
pygame.quit()
sys.exit()
