# main.py
# NathanGr33n
# June 20, 2025

# --------- Library Imports ---------
import pygame                 # Game engine
import sys                    # System functions
import os                     # File system operations
import math  			   # For sine animation
import json                   # For exporting statistics
from deck import Deck         # Custom Deck and Card classes


# --------- Animated Card Sprite ---------
class CardSprite:
    """Simple sprite to move a card surface from a start to end position."""

    def __init__(self, card, surface, start_pos, end_pos, target_hand, speed=15):
        self.card = card
        self.surface = surface
        self.x, self.y = start_pos
        self.end_x, self.end_y = end_pos
        self.target_hand = target_hand
        self.speed = speed

    def update(self):
        dx = self.end_x - self.x
        dy = self.end_y - self.y
        dist = math.hypot(dx, dy)
        if dist <= self.speed or dist == 0:
            self.x, self.y = self.end_x, self.end_y
            draw_card_with_border(self.surface, int(self.x), int(self.y))
            return True
        self.x += self.speed * dx / dist
        self.y += self.speed * dy / dist
        draw_card_with_border(self.surface, int(self.x), int(self.y))
        return False



# --------- Game Window Setup ---------
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Blackjack")
font = pygame.font.SysFont("Arial", 24)

# --------- Load Chip Image ---------
chip_image = pygame.image.load(os.path.join("assets", "chips", "chip_25.png")).convert_alpha()
chip_image = pygame.transform.scale(chip_image, (40, 40))

# --------- Load Card Back Image ---------
card_back = pygame.image.load(os.path.join("assets", "cards", "png", "back.png")).convert_alpha()
card_back = pygame.transform.scale(card_back, (80, 120))

# --------- Load and Scale Card Image ---------
def load_png_card(path, size=(80, 120)):
    try:
        image = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(image, size)
    except Exception as e:
        print(f"Error loading PNG '{path}': {e}")
        return None

# --------- Draw Card with Border and Shadow ---------
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

# --------- Draw a Hand of Cards ---------
def draw_hand(hand, y, hide_first=False):
    for i, card in enumerate(hand):
        x = 100 + i * 100
        if hide_first and i == 0:
            draw_card_with_border(card_back, x, y)
        else:
            card_surface = load_png_card(card.image_path)
            draw_card_with_border(card_surface, x, y)
            
# --------- Draw Chip Stack ---------
def draw_chip_stack(x, y, bet_amount, tick):
    """
    Draws a stack of chips representing the current bet.
    A subtle bounce animation is added for visual effect.
    """
    chips = bet_amount // 25  # One chip per $25 bet
    for i in range(chips):
        # Simple bounce animation: chips rise and fall
        offset = int(5 * math.sin((tick / 200) + (i * 0.5)))
        screen.blit(chip_image, (x, y - i * 12 + offset))


# --------- Calculate Blackjack Hand Value ---------
def calculate_hand_value(hand):
    value = 0
    aces = 0
    for card in hand:
        val = card.value()
        value += val
        if card.rank == 'ace':
            aces += 1
    while value > 21 and aces > 0:
        value -= 10
        aces -= 1
    return value

# --------- Display Text ---------
def draw_text(text, x, y, color=(255, 255, 255)):
    surface = font.render(text, True, color)
    screen.blit(surface, (x, y))

# --------- Display Button ---------
def draw_button(text, rect, color, text_color=(0, 0, 0)):
    pygame.draw.rect(screen, color, rect)
    draw_text(text, rect[0] + 10, rect[1] + 10, text_color)

# --------- Draw Statistics Panel ---------
def draw_stats_panel(x, y):
    panel = pygame.Rect(x, y, 200, 140)
    pygame.draw.rect(screen, (0, 100, 0), panel)
    pygame.draw.rect(screen, (255, 255, 255), panel, 2)
    draw_text(f"Wins: {stats['wins']}", x + 10, y + 10)
    draw_text(f"Losses: {stats['losses']}", x + 10, y + 30)
    draw_text(f"Pushes: {stats['pushes']}", x + 10, y + 50)
    draw_text(f"Busts: {stats['busts']}", x + 10, y + 70)
    draw_text(f"Chips Won: {stats['chips_won']}", x + 10, y + 90)
    draw_text(f"Chips Lost: {stats['chips_lost']}", x + 10, y + 110)

# --------- Export Statistics ---------
def export_stats():
    with open("stats.json", "w") as jf:
        json.dump(stats, jf, indent=4)
    with open("stats.txt", "w") as tf:
        for key, value in stats.items():
            tf.write(f"{key}: {value}\n")

# --------- Reset Game State ---------
def reset_game():
    """Prepares the next round, keeping chips and bet"""
    global deck, player_hand, dealer_hand, player_turn, game_over, winner, round_started, deal_queue, dealer_playing
    deck = Deck()
    player_hand = []
    dealer_hand = []
    player_turn = True
    game_over = False
    winner = ""
    round_started = True  # Round has officially started
    dealer_playing = False
    deal_queue = ["player", "dealer", "player", "dealer"]
    start_next_deal()
    
# --------- Initial Animation Setup ---------
tick = 0  # For animation timing


# --------- Initial Chip Setup ---------
player_chips = 500        # Starting chips
player_bet = 25           # Initial bet
round_started = False     # Round begins after betting

# --------- Statistics Tracking ---------
stats = {
    "wins": 0,
    "losses": 0,
    "pushes": 0,
    "busts": 0,
    "chips_won": 0,
    "chips_lost": 0,
}

# --------- Animation Helpers ---------
animating_cards = []  # Active CardSprite objects
deal_queue = []       # Pending deals ('player' or 'dealer')
dealer_playing = False


def start_next_deal():
    """Begin the next card animation if queued."""
    if deal_queue and not animating_cards:
        target = deal_queue.pop(0)
        card = deck.deal()
        if not card:
            return
        start_pos = (WIDTH // 2 - 40, HEIGHT // 2 - 60)
        if target == "player":
            index = len(player_hand) + sum(1 for s in animating_cards if s.target_hand == "player")
            end_pos = (100 + index * 100, 400)
            surface = load_png_card(card.image_path)
        else:
            index = len(dealer_hand) + sum(1 for s in animating_cards if s.target_hand == "dealer")
            end_pos = (100 + index * 100, 100)
            surface = card_back if index == 0 and player_turn else load_png_card(card.image_path)
        animating_cards.append(CardSprite(card, surface, start_pos, end_pos, target))


def determine_winner():
    """Evaluate final hands and update statistics."""
    global winner, player_chips, game_over, stats
    player_value = calculate_hand_value(player_hand)
    dealer_value = calculate_hand_value(dealer_hand)
    if dealer_value > 21 or player_value > dealer_value:
        winner = "Player Wins!"
        player_chips += player_bet
        stats["wins"] += 1
        stats["chips_won"] += player_bet
    elif player_value == dealer_value:
        winner = "Push! It's a tie."
        stats["pushes"] += 1
    else:
        winner = "Dealer Wins."
        player_chips -= player_bet
        stats["losses"] += 1
        stats["chips_lost"] += player_bet
    game_over = True

# --------- Game State Flags ---------
game_over = False         # Whether the round has ended
player_turn = False       # Whether it's the player's turn
winner = ""               # Result message (if any)
round_started = False     # Whether a round is currently in play


# --------- Define Button Rectangles ---------
hit_button = pygame.Rect(100, 530, 100, 40)
stand_button = pygame.Rect(250, 530, 100, 40)
restart_button = pygame.Rect(500, 530, 120, 40)
bet_plus_button = pygame.Rect(630, 90, 40, 30)
bet_minus_button = pygame.Rect(570, 90, 40, 30)

# --------- Main Game Logic ---------
running = True
while running:
    screen.fill((0, 128, 0))  # Green felt background
    tick += 1 #Increment Animation tick

    # Draw hands and update animations if the round has started
    if round_started:
        draw_hand(player_hand, 400)
        draw_hand(dealer_hand, 100, hide_first=(player_turn and not game_over))
        for sprite in animating_cards[:]:
            finished = sprite.update()
            if finished:
                if sprite.target_hand == "player":
                    player_hand.append(sprite.card)
                    if calculate_hand_value(player_hand) > 21:
                        winner = "Bust! Dealer Wins."
                        player_chips -= player_bet
                        stats["busts"] += 1
                        stats["losses"] += 1
                        stats["chips_lost"] += player_bet
                        game_over = True
                        player_turn = False
                else:
                    dealer_hand.append(sprite.card)
                    if dealer_playing and calculate_hand_value(dealer_hand) < 17:
                        deal_queue.append("dealer")
                    elif dealer_playing and calculate_hand_value(dealer_hand) >= 17:
                        dealer_playing = False
                        determine_winner()
                animating_cards.remove(sprite)
                start_next_deal()

    # Calculate and display scores
    if round_started:
        player_value = calculate_hand_value(player_hand)
        dealer_value = calculate_hand_value(dealer_hand if not player_turn else dealer_hand[1:])
        draw_text(f"Player: {player_value}", 100, 370)
        if not player_turn or game_over:
            draw_text(f"Dealer: {calculate_hand_value(dealer_hand)}", 100, 230)

    # Display chip and bet info
    draw_text(f"Chips: ${player_chips}", 570, 20)
    draw_text(f"Bet: ${player_bet}", 570, 60)
    draw_chip_stack(600, 250, player_bet, tick)
    draw_stats_panel(10, 20)
    
    # Bet adjustment buttons (only if round hasn’t started)
    if not round_started:
        draw_button("+", bet_plus_button, (150, 200, 255))
        draw_button("-", bet_minus_button, (150, 200, 255))

    # Draw control buttons
    if round_started and not game_over:
        draw_button("Hit", hit_button, (200, 200, 200))
        draw_button("Stand", stand_button, (200, 200, 200))

    if game_over:
        draw_text(winner, 500, 370, (255, 215, 0))
        draw_button("Restart", restart_button, (150, 255, 150))
    elif not round_started:
        draw_button("Start", restart_button, (100, 255, 100))  # Deal cards after betting

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False  # Exit game
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                export_stats()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Bet adjustment (only before round starts)
            if not round_started:
                if bet_plus_button.collidepoint(event.pos) and player_bet + 25 <= player_chips:
                    player_bet += 25
                elif bet_minus_button.collidepoint(event.pos) and player_bet - 25 >= 25:
                    player_bet -= 25
                elif restart_button.collidepoint(event.pos):
                    reset_game()  # Start round

            # During active round
            elif round_started and not game_over:
                if hit_button.collidepoint(event.pos) and player_turn and not animating_cards and not deal_queue:
                    deal_queue.append("player")
                    start_next_deal()

                elif stand_button.collidepoint(event.pos) and player_turn and not animating_cards and not deal_queue:
                    player_turn = False
                    if calculate_hand_value(dealer_hand) < 17:
                        dealer_playing = True
                        deal_queue.append("dealer")
                        start_next_deal()
                    else:
                        determine_winner()

            # Restart after game over
            elif game_over and restart_button.collidepoint(event.pos):
                if player_chips >= 25:
                    round_started = False  # Return to bet adjustment
                    winner = ""
                else:
                    winner = "You're out of chips!"

    pygame.display.flip()  # Update the display

# Exit cleanly
pygame.quit()
sys.exit()
