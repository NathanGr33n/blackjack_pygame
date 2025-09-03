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
from layout import LayoutManager  # Responsive layout system
from animation_manager import CardAnimationManager  # Animation system
from animation_config import AnimationConfigManager  # Animation configuration


class Game:
    """Encapsulates all Blackjack game logic and UI rendering."""

    def __init__(self) -> None:
        # --------- Game Window Setup ---------
        pygame.init()
        self.WIDTH, self.HEIGHT = 800, 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("Blackjack - Responsive")
        
        # --------- Initialize Layout Manager ---------
        self.layout = LayoutManager(self.WIDTH, self.HEIGHT)
        
        # --------- Initialize Animation System ---------
        self.animation_config = AnimationConfigManager()
        self.card_animator = CardAnimationManager(self.layout, self.animation_config.get_current_config())
        self.card_animator.initialize_positions()
        self.animations_enabled = True
        
        # --------- Initialize Font (will be scaled by layout) ---------
        base_font_size = 24
        font_size = self.layout.get_font_size(base_font_size)
        self.font = pygame.font.SysFont("Arial", font_size)

        # --------- Load and Scale Images ---------
        self._load_images()

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
            "double_downs": 0,
            "splits": 0,
        }

        # --------- Game State Flags ---------
        self.game_over = False         # Whether the round has ended
        self.player_turn = False       # Whether it's the player's turn
        self.winner = ""               # Result message (if any)
        self.round_started = False     # Whether a round is currently in play
        
        # --------- Double Down & Split State ---------
        self.double_down_used = False  # Whether double down has been used this round
        self.is_split = False          # Whether player has split their hand
        self.split_hands = []          # List of split hands when split is active
        self.split_bets = []           # Bets for each split hand
        self.active_split_hand = 0     # Which split hand is currently active
        self.split_hands_complete = [] # Track which split hands are finished

        # Deck and hands will be created when a round starts
        self.deck: Deck | None = None
        self.player_hand = []
        self.dealer_hand = []

        # --------- Initialize Responsive Button Layout ---------
        self._update_layout()

        self.running = True
        self.hints_enabled = False
    
    def _load_images(self) -> None:
        """Load and scale images based on current layout."""
        # Load original images
        chip_path = os.path.join("assets", "chips", "chip_25.png")
        self.chip_image_original = pygame.image.load(chip_path).convert_alpha()
        
        back_path = os.path.join("assets", "cards", "png", "back.png")
        self.card_back_original = pygame.image.load(back_path).convert_alpha()
        
        # Scale images based on layout
        chip_size = self.layout.get_chip_size()
        self.chip_image = pygame.transform.scale(self.chip_image_original, chip_size)
        
        card_size = self.layout.get_card_size()
        self.card_back = pygame.transform.scale(self.card_back_original, card_size)
    
    def _update_layout(self) -> None:
        """Update layout-dependent elements when screen size changes."""
        # Update button positions using layout manager
        buttons = self.layout.get_button_layout()
        self.hit_button = buttons['hit']
        self.stand_button = buttons['stand']
        self.double_button = buttons['double']
        self.split_button = buttons['split']
        self.hint_button = buttons['hint']
        self.restart_button = buttons['restart']
        self.bet_plus_button = buttons['bet_plus']
        self.bet_minus_button = buttons['bet_minus']
        
        # Update font size
        base_font_size = 24
        font_size = self.layout.get_font_size(base_font_size)
        self.font = pygame.font.SysFont("Arial", font_size)
        
        # Rescale images if needed
        if hasattr(self, 'chip_image_original'):
            chip_size = self.layout.get_chip_size()
            self.chip_image = pygame.transform.scale(self.chip_image_original, chip_size)
            
            card_size = self.layout.get_card_size()
            self.card_back = pygame.transform.scale(self.card_back_original, card_size)
        
        # Update animation manager with new layout
        if hasattr(self, 'card_animator'):
            self.card_animator.update_layout(self.layout)

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
    def draw_responsive_hand(self, hand, hand_name: str, hide_first: bool = False) -> None:
        """Draw a hand of cards using responsive positioning."""
        hand_positions = self.layout.get_hand_positions()
        start_x, start_y = hand_positions[hand_name]
        card_offset = self.layout.get_card_hand_offset()
        card_size = self.layout.get_card_size()
        
        for i, card in enumerate(hand):
            x = start_x + i * card_offset
            if hide_first and i == 0:
                self.draw_card_with_border(self.card_back, x, start_y, card_size)
            else:
                card_surface = self.load_png_card(card.image_path, card_size)
                self.draw_card_with_border(card_surface, x, start_y, card_size)

    # --------- Draw Chip Stack ---------
    def draw_chip_stack(self, x, y, bet_amount, tick):
        """Draws a stack of chips representing the current bet."""
        chips = bet_amount // 25  # One chip per $25 bet
        for i in range(chips):
            offset = int(5 * math.sin((tick / 200) + (i * 0.5)))
            self.screen.blit(self.chip_image, (x, y - i * 12 + offset))
    
    def draw_responsive_chip_stack(self, x, y, bet_amount, tick):
        """Draws a stack of chips using responsive scaling."""
        chips = bet_amount // 25  # One chip per $25 bet
        stack_spacing = int(12 * self.layout.dimensions.scale_factor)
        
        for i in range(chips):
            offset = int(5 * math.sin((tick / 200) + (i * 0.5)))
            self.screen.blit(self.chip_image, (x, y - i * stack_spacing + offset))

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
    
    # --------- Check Double Down Availability ---------
    def can_double_down(self) -> bool:
        """Check if double down is available."""
        return (
            not self.double_down_used and  # Haven't already doubled down
            len(self.player_hand) == 2 and  # First two cards only
            self.player_chips >= self.player_bet and  # Can afford to double bet
            not self.is_split  # No double down after split (house rule)
        )
    
    # --------- Check Split Availability ---------
    def can_split(self) -> bool:
        """Check if split is available."""
        return (
            not self.is_split and  # Haven't already split
            len(self.player_hand) == 2 and  # First two cards only
            self.player_hand[0].rank == self.player_hand[1].rank and  # Must be a pair
            self.player_chips >= self.player_bet  # Can afford second bet
        )
    
    # --------- Execute Double Down ---------
    def double_down(self) -> None:
        """Execute double down: double bet, deal one card, end turn."""
        if not self.can_double_down():
            return
        
        # Double the bet
        self.player_chips -= self.player_bet
        self.player_bet *= 2
        self.double_down_used = True
        self.stats["double_downs"] += 1
        
        # Deal exactly one more card
        self.player_hand.append(self.deck.deal())
        
        # Check for bust
        if self.calculate_hand_value(self.player_hand) > 21:
            self.winner = "Bust! Dealer Wins."
            self.player_chips -= self.player_bet  # Player already lost the doubled bet
            self.stats["busts"] += 1
            self.stats["losses"] += 1
            self.stats["chips_lost"] += self.player_bet
            self.game_over = True
            self.player_turn = False
        else:
            # End player's turn (no more actions allowed after double down)
            self.player_turn = False
            
            # Play dealer's hand
            while self.calculate_hand_value(self.dealer_hand) < 17:
                self.dealer_hand.append(self.deck.deal())
            
            # Determine winner
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
                # Player already lost the doubled bet above
                self.stats["losses"] += 1
                self.stats["chips_lost"] += self.player_bet
            
            self.game_over = True
    
    # --------- Execute Split ---------
    def split_hand(self) -> None:
        """Execute split: create two hands from pair, deal new cards."""
        if not self.can_split():
            return
        
        # Deduct bet for second hand
        self.player_chips -= self.player_bet
        self.is_split = True
        self.stats["splits"] += 1
        
        # Create two hands from the pair
        card1, card2 = self.player_hand[0], self.player_hand[1]
        self.split_hands = [[card1], [card2]]
        self.split_bets = [self.player_bet, self.player_bet]
        self.split_hands_complete = [False, False]
        self.active_split_hand = 0
        
        # Deal second card to each hand
        self.split_hands[0].append(self.deck.deal())
        self.split_hands[1].append(self.deck.deal())
        
        # Set current hand to first split hand
        self.player_hand = self.split_hands[0]
        self.player_bet = self.split_bets[0]
    
    # --------- Handle Split Hand Completion ---------
    def complete_split_hand(self) -> None:
        """Complete current split hand and move to next or finish round."""
        if not self.is_split:
            return
        
        # Mark current hand as complete
        self.split_hands_complete[self.active_split_hand] = True
        
        # Check if this hand busted
        if self.calculate_hand_value(self.split_hands[self.active_split_hand]) > 21:
            self.stats["busts"] += 1
            self.stats["losses"] += 1
            self.stats["chips_lost"] += self.split_bets[self.active_split_hand]
        
        # Move to next hand if available
        if self.active_split_hand == 0:
            self.active_split_hand = 1
            self.player_hand = self.split_hands[1]
            self.player_bet = self.split_bets[1]
        else:
            # Both hands complete - play dealer and determine winners
            self.player_turn = False
            while self.calculate_hand_value(self.dealer_hand) < 17:
                self.dealer_hand.append(self.deck.deal())
            
            self._resolve_split_hands()
            self.game_over = True
    
    # --------- Resolve Split Hand Results ---------
    def _resolve_split_hands(self) -> None:
        """Determine winners for each split hand."""
        dealer_value = self.calculate_hand_value(self.dealer_hand)
        results = []
        
        for i, hand in enumerate(self.split_hands):
            hand_value = self.calculate_hand_value(hand)
            bet_amount = self.split_bets[i]
            
            if hand_value > 21:
                # Already handled in complete_split_hand
                results.append("Bust")
            elif dealer_value > 21 or hand_value > dealer_value:
                results.append("Win")
                self.player_chips += bet_amount
                self.stats["wins"] += 1
                self.stats["chips_won"] += bet_amount
            elif hand_value == dealer_value:
                results.append("Push")
                self.stats["pushes"] += 1
            else:
                results.append("Loss")
                self.stats["losses"] += 1
                self.stats["chips_lost"] += bet_amount
        
        # Set winner message
        if results[0] == results[1]:
            if results[0] == "Win":
                self.winner = "Both hands win!"
            elif results[0] == "Loss":
                self.winner = "Both hands lose."
            elif results[0] == "Push":
                self.winner = "Both hands push."
            else:  # Both bust
                self.winner = "Both hands bust!"
        else:
            self.winner = f"Hand 1: {results[0]}, Hand 2: {results[1]}"

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
    
    def draw_responsive_stats_panel(self, x, y):
        """Draw statistics panel with responsive sizing."""
        panel_size = self.layout.get_stats_panel_size()
        panel_width = panel_size[0]
        panel_height = int(panel_size[1] * 1.4)  # Make panel taller for new stats
        panel = pygame.Rect(x, y, panel_width, panel_height)
        pygame.draw.rect(self.screen, (0, 100, 0), panel)
        pygame.draw.rect(self.screen, (255, 255, 255), panel, 2)
        
        # Scale text spacing based on layout
        padding = int(10 * self.layout.dimensions.scale_factor)
        line_height = int(18 * self.layout.dimensions.scale_factor)  # Slightly smaller for more lines
        
        self.draw_text(f"Wins: {self.stats['wins']}", x + padding, y + padding)
        self.draw_text(f"Losses: {self.stats['losses']}", x + padding, y + padding + line_height)
        self.draw_text(f"Pushes: {self.stats['pushes']}", x + padding, y + padding + line_height * 2)
        self.draw_text(f"Busts: {self.stats['busts']}", x + padding, y + padding + line_height * 3)
        self.draw_text(f"Chips Won: {self.stats['chips_won']}", x + padding, y + padding + line_height * 4)
        self.draw_text(f"Chips Lost: {self.stats['chips_lost']}", x + padding, y + padding + line_height * 5)
        self.draw_text(f"Doubles: {self.stats['double_downs']}", x + padding, y + padding + line_height * 6)
        self.draw_text(f"Splits: {self.stats['splits']}", x + padding, y + padding + line_height * 7)

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
        # Clear previous animations
        self.card_animator.clear_all_animations()
        
        # Create new deck and deal cards
        self.deck = Deck()
        self.player_hand = [self.deck.deal(), self.deck.deal()]
        self.dealer_hand = [self.deck.deal(), self.deck.deal()]
        
        # Reset game state
        self.player_turn = True
        self.game_over = False
        self.winner = ""
        self.round_started = True  # Round has officially started
        
        # Reset Double Down and Split state
        self.double_down_used = False
        self.is_split = False
        self.split_hands = []
        self.split_bets = []
        self.active_split_hand = 0
        self.split_hands_complete = []
        
        # Start dealing animation if animations are enabled
        if self.animations_enabled:
            def on_deal_complete():
                """Called when initial dealing animation completes."""
                # Cards have been dealt, player can now act
                pass
            
            self.card_animator.deal_initial_cards(
                self.player_hand, 
                self.dealer_hand, 
                callback=on_deal_complete
            )

    # --------- Handle a Single Event ---------
    def handle_event(self, event) -> None:
        if event.type == pygame.QUIT:
            self.running = False
        elif event.type == pygame.VIDEORESIZE:
            # Handle window resize
            self.WIDTH, self.HEIGHT = event.w, event.h
            self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT), pygame.RESIZABLE)
            self.layout.update_dimensions(self.WIDTH, self.HEIGHT)
            self._update_layout()
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
                    if self.is_split:
                        # Update the active split hand
                        self.split_hands[self.active_split_hand] = self.player_hand
                    
                    if self.calculate_hand_value(self.player_hand) > 21:
                        if self.is_split:
                            self.complete_split_hand()
                        else:
                            self.winner = "Bust! Dealer Wins."
                            self.player_chips -= self.player_bet
                            self.stats["busts"] += 1
                            self.stats["losses"] += 1
                            self.stats["chips_lost"] += self.player_bet
                            self.game_over = True
                            self.player_turn = False
                elif self.stand_button.collidepoint(event.pos):
                    if self.is_split:
                        self.complete_split_hand()
                    else:
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
                elif self.double_button.collidepoint(event.pos) and self.can_double_down():
                    self.double_down()
                elif self.split_button.collidepoint(event.pos) and self.can_split():
                    self.split_hand()
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
        
        # Update animation system
        if self.animations_enabled:
            self.card_animator.update()
        
        # Get responsive text positions
        text_positions = self.layout.get_text_positions()

        # Draw animated cards if animations are enabled, otherwise fall back to static drawing
        if self.animations_enabled and self.card_animator.has_animations():
            # Render animated cards
            card_size = self.layout.get_card_size()
            self.card_animator.render_animated_cards(self.screen, card_size)
        elif self.round_started:
            # Fallback to static drawing when no animations are active
            if self.is_split:
                # Draw both split hands
                self.draw_responsive_hand(self.split_hands[0], 'player_split_1', hide_first=False)
                self.draw_responsive_hand(self.split_hands[1], 'player_split_2', hide_first=False)
                
                # Highlight active hand with border
                if not self.game_over:
                    hand_positions = self.layout.get_hand_positions()
                    if self.active_split_hand == 0:
                        pos = hand_positions['player_split_1']
                    else:
                        pos = hand_positions['player_split_2']
                    
                    # Draw active hand indicator
                    card_size = self.layout.get_card_size()
                    border_rect = pygame.Rect(pos[0] - 5, pos[1] - 5, card_size[0] + 10, card_size[1] + 10)
                    pygame.draw.rect(self.screen, (255, 255, 0), border_rect, 3)
            else:
                self.draw_responsive_hand(self.player_hand, 'player', hide_first=False)
            
            self.draw_responsive_hand(self.dealer_hand, 'dealer', hide_first=(self.player_turn and not self.game_over))

        # Draw hand values using responsive positioning
        if self.round_started:
            if self.is_split:
                # Draw values for both split hands
                hand1_value = self.calculate_hand_value(self.split_hands[0])
                hand2_value = self.calculate_hand_value(self.split_hands[1])
                
                player_pos = text_positions['player_score']
                self.draw_text(f"Hand 1: {hand1_value}", player_pos[0], player_pos[1])
                self.draw_text(f"Hand 2: {hand2_value}", player_pos[0] + 150, player_pos[1])
                
                if not self.game_over:
                    # Show which hand is active
                    active_text = f"Playing Hand {self.active_split_hand + 1}"
                    self.draw_text(active_text, player_pos[0], player_pos[1] - 25, (255, 255, 0))
            else:
                player_value = self.calculate_hand_value(self.player_hand)
                player_pos = text_positions['player_score']
                self.draw_text(f"Player: {player_value}", player_pos[0], player_pos[1])
            
            if not self.player_turn or self.game_over:
                dealer_value = self.calculate_hand_value(self.dealer_hand)
                dealer_pos = text_positions['dealer_score']
                self.draw_text(f"Dealer: {dealer_value}", dealer_pos[0], dealer_pos[1])

        # Draw chips and bet info using responsive positioning
        chips_pos = text_positions['chips']
        bet_pos = text_positions['bet']
        self.draw_text(f"Chips: ${self.player_chips}", chips_pos[0], chips_pos[1])
        self.draw_text(f"Bet: ${self.player_bet}", bet_pos[0], bet_pos[1])
        
        # Draw chip stack using responsive positioning
        chip_stack_pos = self.layout.get_chip_stack_position()
        self.draw_responsive_chip_stack(chip_stack_pos[0], chip_stack_pos[1], self.player_bet, self.tick)
        
        # Draw stats panel using responsive positioning
        stats_pos = self.layout.get_stats_panel_position()
        self.draw_responsive_stats_panel(stats_pos[0], stats_pos[1])

        # Draw betting buttons when not in a round
        if not self.round_started:
            self.draw_button("+", self.bet_plus_button, (150, 200, 255))
            self.draw_button("-", self.bet_minus_button, (150, 200, 255))

        # Handle strategy hints
        suggestion = None
        if self.hints_enabled and self.round_started and not self.game_over and self.player_turn:
            suggestion = suggest_move(self.player_hand, self.dealer_hand[1])

        # Draw action buttons during gameplay
        if self.round_started and not self.game_over:
            hit_outline = suggestion == "Hit"
            stand_outline = suggestion == "Stand"
            self.draw_button("Hit", self.hit_button, (200, 200, 200), outline=hit_outline)
            self.draw_button("Stand", self.stand_button, (200, 200, 200), outline=stand_outline)
            
            # Draw Double Down button if available
            if self.can_double_down():
                double_outline = suggestion == "Double"
                self.draw_button("Double", self.double_button, (255, 200, 100), outline=double_outline)
            
            # Draw Split button if available
            if self.can_split():
                split_outline = suggestion == "Split"
                self.draw_button("Split", self.split_button, (100, 255, 200), outline=split_outline)
            
            # Draw hint text using responsive positioning
            if suggestion:
                hint_pos = text_positions['hint_text']
                self.draw_text(f"Hint: {suggestion}", hint_pos[0], hint_pos[1], (255, 255, 0))

        # Draw hint toggle button
        hint_color = (150, 200, 255) if not self.hints_enabled else (255, 215, 0)
        self.draw_button("Hint", self.hint_button, hint_color)

        # Draw game over/restart UI
        if self.game_over:
            winner_pos = text_positions['winner']
            self.draw_text(self.winner, winner_pos[0], winner_pos[1], (255, 215, 0))
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

