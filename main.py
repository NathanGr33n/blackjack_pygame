# main.py
# NathanGr33n
# June 20, 2025

"""Main entry point for the Blackjack game.

The module defines a :class:`Game` class encapsulating all game state
and behaviour.  Running this file will instantiate the class and start
the main loop.
"""

# --------- Library Imports ---------
import json                   # For exporting statistics
import math                   # For sine animation
import os                     # File system operations
import sys                    # System functions

import pygame                 # Game engine

from deck import Deck         # Custom Deck and Card classes
from basic_strategy import suggest_move


class Game:
    """Encapsulates all Blackjack game logic and UI rendering."""

    def __init__(self) -> None:
        # --------- Game Window Setup ---------
        pygame.init()
        self.WIDTH, self.HEIGHT = 800, 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Blackjack")
        self.font = pygame.font.SysFont("Arial", 24)

        # --------- Load Chip Image ---------
        chip_path = os.path.join("assets", "chips", "chip_25.png")
        self.chip_image = pygame.image.load(chip_path).convert_alpha()
        self.chip_image = pygame.transform.scale(self.chip_image, (40, 40))

        # --------- Load Card Back Image ---------
        back_path = os.path.join("assets", "cards", "png", "back.png")
        self.card_back = pygame.image.load(back_path).convert_alpha()
        self.card_back = pygame.transform.scale(self.card_back, (80, 120))

        # --------- Initial Animation Setup ---------
        self.tick = 0  # For animation timing

        # --------- Initial Chip Setup ---------
        self.player_chips = 500        # Starting chips
        self.player_bet = 25           # Initial bet

        # --------- Statistics Tracking ---------
        self.stats = {
            "wins": 0,
            "losses": 0,
            "pushes": 0,
            "busts": 0,
            "chips_won": 0,
            "chips_lost": 0,
        }

        # --------- Game State Flags ---------
        self.game_over = False         # Whether the round has ended
        self.player_turn = False       # Whether it's the player's turn
        self.winner = ""               # Result message (if any)
        self.round_started = False     # Whether a round is currently in play

        # Deck and hands will be created when a round starts
        self.deck: Deck | None = None
        self.player_hand = []
        self.dealer_hand = []

        # --------- Define Button Rectangles ---------
        self.hit_button = pygame.Rect(100, 530, 100, 40)
        self.stand_button = pygame.Rect(250, 530, 100, 40)
        self.restart_button = pygame.Rect(500, 530, 120, 40)
        self.bet_plus_button = pygame.Rect(630, 90, 40, 30)
        self.bet_minus_button = pygame.Rect(570, 90, 40, 30)
        self.hint_button = pygame.Rect(380, 530, 100, 40)

        self.running = True
        self.hints_enabled = False

    # --------- Load and Scale Card Image ---------
    def load_png_card(self, path: str, size: tuple[int, int] = (80, 120)):
        try:
            image = pygame.image.load(path).convert_alpha()
            return pygame.transform.scale(image, size)
        except Exception as e:  # pragma: no cover - unlikely during normal run
            print(f"Error loading PNG '{path}': {e}")
            return None

    # --------- Draw Card with Border and Shadow ---------
    def draw_card_with_border(
        self,
        card_surface: pygame.Surface | None,
        x: int,
        y: int,
        card_size: tuple[int, int] = (80, 120),
        border_thickness: int = 6,
    ) -> None:
        if card_surface is None:
            return
        width = card_size[0] + 2 * border_thickness
        height = card_size[1] + 2 * border_thickness
        shadow = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.rect(shadow, (0, 0, 0, 100), shadow.get_rect(), border_radius=10)
        self.screen.blit(shadow, (x + 3, y + 3))
        frame = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.rect(frame, (255, 255, 255), frame.get_rect(), border_radius=10)
        self.screen.blit(frame, (x, y))
        self.screen.blit(card_surface, (x + border_thickness, y + border_thickness))

    # --------- Draw a Hand of Cards ---------
    def draw_hand(self, hand, y, hide_first: bool = False) -> None:
        for i, card in enumerate(hand):
            x = 100 + i * 100
            if hide_first and i == 0:
                self.draw_card_with_border(self.card_back, x, y)
            else:
                card_surface = self.load_png_card(card.image_path)
                self.draw_card_with_border(card_surface, x, y)

    # --------- Draw Chip Stack ---------
    def draw_chip_stack(self, x, y, bet_amount, tick):
        """Draws a stack of chips representing the current bet."""
        chips = bet_amount // 25  # One chip per $25 bet
        for i in range(chips):
            offset = int(5 * math.sin((tick / 200) + (i * 0.5)))
            self.screen.blit(self.chip_image, (x, y - i * 12 + offset))

    # --------- Calculate Blackjack Hand Value ---------
    def calculate_hand_value(self, hand) -> int:
        value = 0
        aces = 0
        for card in hand:
            val = card.value()
            value += val
            if card.rank == "ace":
                aces += 1
        while value > 21 and aces > 0:
            value -= 10
            aces -= 1
        return value

    # --------- Display Text ---------
    def draw_text(self, text, x, y, color=(255, 255, 255)):
        surface = self.font.render(text, True, color)
        self.screen.blit(surface, (x, y))

    # --------- Display Button ---------
    def draw_button(self, text, rect, color, text_color=(0, 0, 0), outline=False):
        pygame.draw.rect(self.screen, color, rect)
        if outline:
            pygame.draw.rect(self.screen, (255, 215, 0), rect, 3)
        self.draw_text(text, rect[0] + 10, rect[1] + 10, text_color)

    # --------- Draw Statistics Panel ---------
    def draw_stats_panel(self, x, y):
        panel = pygame.Rect(x, y, 200, 140)
        pygame.draw.rect(self.screen, (0, 100, 0), panel)
        pygame.draw.rect(self.screen, (255, 255, 255), panel, 2)
        self.draw_text(f"Wins: {self.stats['wins']}", x + 10, y + 10)
        self.draw_text(f"Losses: {self.stats['losses']}", x + 10, y + 30)
        self.draw_text(f"Pushes: {self.stats['pushes']}", x + 10, y + 50)
        self.draw_text(f"Busts: {self.stats['busts']}", x + 10, y + 70)
        self.draw_text(f"Chips Won: {self.stats['chips_won']}", x + 10, y + 90)
        self.draw_text(f"Chips Lost: {self.stats['chips_lost']}", x + 10, y + 110)

    # --------- Export Statistics ---------
    def export_stats(self):
        with open("stats.json", "w") as jf:
            json.dump(self.stats, jf, indent=4)
        with open("stats.txt", "w") as tf:
            for key, value in self.stats.items():
                tf.write(f"{key}: {value}\n")

    # --------- Reset Game State ---------
    def reset_game(self) -> None:
        """Prepares the next round, keeping chips and bet."""
        self.deck = Deck()
        self.player_hand = [self.deck.deal(), self.deck.deal()]
        self.dealer_hand = [self.deck.deal(), self.deck.deal()]
        self.player_turn = True
        self.game_over = False
        self.winner = ""
        self.round_started = True  # Round has officially started

    # --------- Handle a Single Event ---------
    def handle_event(self, event) -> None:
        if event.type == pygame.QUIT:
            self.running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                self.export_stats()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.hint_button.collidepoint(event.pos):
                self.hints_enabled = not self.hints_enabled
            elif not self.round_started:
                if self.bet_plus_button.collidepoint(event.pos) and self.player_bet + 25 <= self.player_chips:
                    self.player_bet += 25
                elif self.bet_minus_button.collidepoint(event.pos) and self.player_bet - 25 >= 25:
                    self.player_bet -= 25
                elif self.restart_button.collidepoint(event.pos):
                    self.reset_game()  # Start round
            elif self.round_started and not self.game_over:
                if self.hit_button.collidepoint(event.pos):
                    self.player_hand.append(self.deck.deal())
                    if self.calculate_hand_value(self.player_hand) > 21:
                        self.winner = "Bust! Dealer Wins."
                        self.player_chips -= self.player_bet
                        self.stats["busts"] += 1
                        self.stats["losses"] += 1
                        self.stats["chips_lost"] += self.player_bet
                        self.game_over = True
                        self.player_turn = False
                elif self.stand_button.collidepoint(event.pos):
                    self.player_turn = False
                    while self.calculate_hand_value(self.dealer_hand) < 17:
                        self.dealer_hand.append(self.deck.deal())
                    player_value = self.calculate_hand_value(self.player_hand)
                    dealer_value = self.calculate_hand_value(self.dealer_hand)
                    if dealer_value > 21 or player_value > dealer_value:
                        self.winner = "Player Wins!"
                        self.player_chips += self.player_bet
                        self.stats["wins"] += 1
                        self.stats["chips_won"] += self.player_bet
                    elif player_value == dealer_value:
                        self.winner = "Push! It's a tie."
                        self.stats["pushes"] += 1
                    else:
                        self.winner = "Dealer Wins."
                        self.player_chips -= self.player_bet
                        self.stats["losses"] += 1
                        self.stats["chips_lost"] += self.player_bet
                    self.game_over = True
            elif self.game_over and self.restart_button.collidepoint(event.pos):
                if self.player_chips >= 25:
                    self.round_started = False
                    self.winner = ""
                else:
                    self.winner = "You're out of chips!"

    # --------- Draw the Current Frame ---------
    def draw(self) -> None:
        self.screen.fill((0, 128, 0))  # Green felt background
        self.tick += 1

        if self.round_started:
            self.draw_hand(self.player_hand, 400)
            self.draw_hand(self.dealer_hand, 100, hide_first=(self.player_turn and not self.game_over))

        if self.round_started:
            player_value = self.calculate_hand_value(self.player_hand)
            dealer_value = self.calculate_hand_value(self.dealer_hand if not self.player_turn else self.dealer_hand[1:])
            self.draw_text(f"Player: {player_value}", 100, 370)
            if not self.player_turn or self.game_over:
                self.draw_text(f"Dealer: {self.calculate_hand_value(self.dealer_hand)}", 100, 230)

        self.draw_text(f"Chips: ${self.player_chips}", 570, 20)
        self.draw_text(f"Bet: ${self.player_bet}", 570, 60)
        self.draw_chip_stack(600, 250, self.player_bet, self.tick)
        self.draw_stats_panel(10, 20)

        if not self.round_started:
            self.draw_button("+", self.bet_plus_button, (150, 200, 255))
            self.draw_button("-", self.bet_minus_button, (150, 200, 255))

        suggestion = None
        if self.hints_enabled and self.round_started and not self.game_over and self.player_turn:
            suggestion = suggest_move(self.player_hand, self.dealer_hand[1])

        if self.round_started and not self.game_over:
            hit_outline = suggestion == "Hit"
            stand_outline = suggestion == "Stand"
            self.draw_button("Hit", self.hit_button, (200, 200, 200), outline=hit_outline)
            self.draw_button("Stand", self.stand_button, (200, 200, 200), outline=stand_outline)
            if suggestion:
                self.draw_text(f"Hint: {suggestion}", 360, 490, (255, 255, 0))

        hint_color = (150, 200, 255) if not self.hints_enabled else (255, 215, 0)
        self.draw_button("Hint", self.hint_button, hint_color)

        if self.game_over:
            self.draw_text(self.winner, 500, 370, (255, 215, 0))
            self.draw_button("Restart", self.restart_button, (150, 255, 150))
        elif not self.round_started:
            self.draw_button("Start", self.restart_button, (100, 255, 100))

    # --------- Main Game Loop ---------
    def run(self) -> None:
        clock = pygame.time.Clock()
        while self.running:
            for event in pygame.event.get():
                self.handle_event(event)
            self.draw()
            pygame.display.flip()
            clock.tick(60)
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    Game().run()

