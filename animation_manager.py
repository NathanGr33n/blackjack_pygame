# animation_manager.py
# NathanGr33n 
# September 3, 2025

"""
Animation manager for integrating card animations with the Blackjack game.

This module provides a high-level interface for managing card animations
within the context of the blackjack game, including deck position management,
hand animations, and game state coordination.
"""

from __future__ import annotations
import pygame
from typing import List, Dict, Tuple, Optional, Callable, Any
from dataclasses import dataclass

from animations import AnimationSystem, AnimationConfig, EaseType
from card_animations import (
    AnimatedCard, CardRenderState, ComboAnimation,
    create_deal_animation, create_hit_animation, create_flip_reveal_animation,
    create_collect_animation, create_bounce_highlight_animation
)
from deck import Card
from layout import LayoutManager


@dataclass
class GameAnimationConfig:
    """Configuration for game-specific animations."""
    # Timing configurations
    deal_duration: float = 0.6
    deal_delay_between_cards: float = 0.2
    hit_duration: float = 0.4
    flip_duration: float = 0.5
    collect_duration: float = 0.8
    
    # Visual effect configurations
    deal_scale_start: float = 0.7
    hit_scale_start: float = 0.8
    bounce_height: float = 15
    
    # Easing preferences
    deal_ease: EaseType = EaseType.EASE_OUT
    hit_ease: EaseType = EaseType.EASE_OUT
    flip_ease: EaseType = EaseType.EASE_IN_OUT
    collect_ease: EaseType = EaseType.EASE_IN


class CardAnimationManager:
    """High-level manager for card animations in the blackjack game."""
    
    def __init__(self, layout_manager: LayoutManager, 
                 animation_config: Optional[GameAnimationConfig] = None):
        self.layout = layout_manager
        self.animation_system = AnimationSystem()
        self.config = animation_config or GameAnimationConfig()
        
        # Card tracking
        self.animated_cards: Dict[Card, AnimatedCard] = {}
        self.deck_position = (0, 0)
        self.discard_position = (0, 0)
        
        # Cached surfaces for rendering
        self._card_surfaces: Dict[str, pygame.Surface] = {}
        self._card_back_surface: Optional[pygame.Surface] = None
        
        # Animation state
        self.animations_enabled = True
        self.current_dealing = False
        self.dealing_queue: List[Callable] = []
        
        # Callbacks for game events
        self.on_deal_complete: Optional[Callable] = None
        self.on_animation_complete: Optional[Callable] = None
    
    def initialize_positions(self) -> None:
        """Initialize deck and discard pile positions based on layout."""
        # Deck position (top-right area)
        self.deck_position = self.layout.get_position(0.85, 0.1)
        
        # Discard position (near deck)
        self.discard_position = self.layout.get_position(0.85, 0.3)
    
    def update(self, delta_time: Optional[float] = None) -> None:
        """Update all active animations."""
        self.animation_system.update(delta_time)
        
        # Process dealing queue if not currently dealing
        if not self.current_dealing and self.dealing_queue:
            next_deal = self.dealing_queue.pop(0)
            next_deal()
    
    def create_animated_card(self, card: Card, initial_position: Optional[Tuple[float, float]] = None) -> AnimatedCard:
        """Create an animated card wrapper for a game card."""
        if initial_position is None:
            initial_position = self.deck_position
        
        animated_card = AnimatedCard(card, initial_position)
        self.animated_cards[card] = animated_card
        return animated_card
    
    def get_animated_card(self, card: Card) -> Optional[AnimatedCard]:
        """Get the animated card wrapper for a game card."""
        return self.animated_cards.get(card)
    
    def remove_animated_card(self, card: Card) -> None:
        """Remove an animated card from tracking."""
        if card in self.animated_cards:
            del self.animated_cards[card]
    
    def deal_initial_cards(self, player_hand: List[Card], dealer_hand: List[Card], 
                          callback: Optional[Callable] = None) -> None:
        """Animate dealing initial cards to player and dealer."""
        if not self.animations_enabled:
            if callback:
                callback()
            return
        
        hand_positions = self.layout.get_hand_positions()
        card_offset = self.layout.get_card_hand_offset()
        
        deal_sequence = []
        delay = 0.0
        
        # Deal alternating between player and dealer
        max_cards = max(len(player_hand), len(dealer_hand))
        
        for i in range(max_cards):
            # Deal to player first
            if i < len(player_hand):
                card = player_hand[i]
                animated_card = self.create_animated_card(card)
                
                target_pos = (
                    hand_positions['player'][0] + i * card_offset,
                    hand_positions['player'][1]
                )
                
                deal_sequence.append({
                    'card': animated_card,
                    'target': target_pos,
                    'delay': delay,
                    'face_up': True
                })
                delay += self.config.deal.delay_between_cards
            
            # Then deal to dealer
            if i < len(dealer_hand):
                card = dealer_hand[i]
                animated_card = self.create_animated_card(card)
                
                target_pos = (
                    hand_positions['dealer'][0] + i * card_offset,
                    hand_positions['dealer'][1]
                )
                
                # First dealer card is face down
                face_up = i != 0
                
                deal_sequence.append({
                    'card': animated_card,
                    'target': target_pos,
                    'delay': delay,
                    'face_up': face_up
                })
                delay += self.config.deal.delay_between_cards
        
        # Execute the dealing sequence
        self.current_dealing = True
        animations_remaining = len(deal_sequence)
        
        def on_deal_animation_complete():
            nonlocal animations_remaining
            animations_remaining -= 1
            if animations_remaining <= 0:
                self.current_dealing = False
                if callback:
                    callback()
        
        for deal in deal_sequence:
            animated_card = deal['card']
            animated_card.is_face_up = deal['face_up']
            
            animation = create_deal_animation(
                animated_card, 
                self.deck_position, 
                deal['target'], 
                deal['delay']
            )
            
            animation.on_complete(on_deal_animation_complete)
            self.animation_system.add_animation(animation)
    
    def animate_hit_card(self, card: Card, hand_position: str, hand_index: int, 
                        callback: Optional[Callable] = None) -> None:
        """Animate adding a card to a hand (hit)."""
        if not self.animations_enabled:
            if callback:
                callback()
            return
        
        animated_card = self.create_animated_card(card)
        hand_positions = self.layout.get_hand_positions()
        card_offset = self.layout.get_card_hand_offset()
        
        target_pos = (
            hand_positions[hand_position][0] + hand_index * card_offset,
            hand_positions[hand_position][1]
        )
        
        animation = create_hit_animation(animated_card, self.deck_position, target_pos)
        
        if callback:
            animation.on_complete(callback)
        
        self.animation_system.add_animation(animation)
    
    def animate_dealer_reveal(self, dealer_card: Card, callback: Optional[Callable] = None) -> None:
        """Animate revealing the dealer's face-down card."""
        if not self.animations_enabled:
            if callback:
                callback()
            return
        
        animated_card = self.get_animated_card(dealer_card)
        if animated_card:
            animation = create_flip_reveal_animation(animated_card)
            
            if callback:
                animation.on_complete(callback)
            
            self.animation_system.add_animation(animation)
    
    def animate_card_highlight(self, card: Card) -> None:
        """Animate highlighting a card (subtle bounce)."""
        if not self.animations_enabled:
            return
        
        animated_card = self.get_animated_card(card)
        if animated_card:
            animation = create_bounce_highlight_animation(animated_card)
            self.animation_system.add_animation(animation)
    
    def collect_all_cards(self, all_cards: List[Card], callback: Optional[Callable] = None) -> None:
        """Animate collecting all cards to the discard pile."""
        if not self.animations_enabled or not all_cards:
            if callback:
                callback()
            return
        
        animations_remaining = len(all_cards)
        
        def on_collect_complete():
            nonlocal animations_remaining
            animations_remaining -= 1
            if animations_remaining <= 0:
                # Clear all animated cards after collection
                self.animated_cards.clear()
                if callback:
                    callback()
        
        delay = 0.0
        for card in all_cards:
            animated_card = self.get_animated_card(card)
            if animated_card:
                animation = create_collect_animation(animated_card, self.discard_position)
                animation.config.delay = delay
                animation.on_complete(on_collect_complete)
                self.animation_system.add_animation(animation)
                delay += 0.1
    
    def render_animated_cards(self, surface: pygame.Surface, card_size: Tuple[int, int]) -> None:
        """Render all animated cards to the screen."""
        if not self.animated_cards:
            return
        
        # Sort cards by z-order (cards with higher z_offset render last)
        sorted_cards = sorted(
            self.animated_cards.values(),
            key=lambda ac: ac.render_state.z_offset
        )
        
        for animated_card in sorted_cards:
            if animated_card.visible:
                # Load card surfaces if not cached
                card_front = self._get_card_surface(animated_card.card, card_size)
                card_back = self._get_card_back_surface(card_size)
                
                animated_card.render(surface, card_front, card_back, card_size)
    
    def _get_card_surface(self, card: Card, card_size: Tuple[int, int]) -> pygame.Surface:
        """Get or create a cached card surface."""
        cache_key = f"{card.suit}_{card.rank}_{card_size[0]}x{card_size[1]}"
        
        if cache_key not in self._card_surfaces:
            try:
                surface = pygame.image.load(card.image_path).convert_alpha()
                surface = pygame.transform.scale(surface, card_size)
                self._card_surfaces[cache_key] = surface
            except Exception as e:
                # Fallback to a simple colored rectangle if image loading fails
                surface = pygame.Surface(card_size)
                surface.fill((255, 255, 255))
                pygame.draw.rect(surface, (0, 0, 0), surface.get_rect(), 2)
                self._card_surfaces[cache_key] = surface
        
        return self._card_surfaces[cache_key]
    
    def _get_card_back_surface(self, card_size: Tuple[int, int]) -> pygame.Surface:
        """Get or create a cached card back surface."""
        cache_key = f"back_{card_size[0]}x{card_size[1]}"
        
        if cache_key not in self._card_surfaces:
            try:
                back_path = "assets/cards/png/back.png"
                surface = pygame.image.load(back_path).convert_alpha()
                surface = pygame.transform.scale(surface, card_size)
                self._card_surfaces[cache_key] = surface
            except Exception as e:
                # Fallback to a simple blue back
                surface = pygame.Surface(card_size)
                surface.fill((0, 0, 150))
                pygame.draw.rect(surface, (255, 255, 255), surface.get_rect(), 2)
                self._card_surfaces[cache_key] = surface
        
        return self._card_surfaces[cache_key]
    
    def pause_animations(self) -> None:
        """Pause all animations."""
        self.animation_system.pause()
    
    def resume_animations(self) -> None:
        """Resume all animations."""
        self.animation_system.resume()
    
    def clear_all_animations(self) -> None:
        """Clear all active animations and reset state."""
        self.animation_system.clear_all()
        self.animated_cards.clear()
        self.current_dealing = False
        self.dealing_queue.clear()
    
    def enable_animations(self, enabled: bool = True) -> None:
        """Enable or disable animations."""
        self.animations_enabled = enabled
        if not enabled:
            self.clear_all_animations()
    
    def is_animating(self) -> bool:
        """Check if any animations are currently active."""
        return self.animation_system.has_animations() or self.current_dealing
    
    def has_animations(self) -> bool:
        """Check if there are any active animations (alias for is_animating)."""
        return self.is_animating()
    
    def wait_for_animations(self, callback: Callable) -> None:
        """Execute callback when all animations complete."""
        if not self.is_animating():
            callback()
        else:
            # Check periodically until animations finish
            def check_complete():
                if not self.is_animating():
                    callback()
                else:
                    # Schedule next check (this would need to be implemented based on your game loop)
                    pass
            
            self.on_animation_complete = check_complete
    
    def get_card_position(self, card: Card) -> Optional[Tuple[float, float]]:
        """Get the current animated position of a card."""
        animated_card = self.get_animated_card(card)
        return animated_card.get_position() if animated_card else None
    
    def update_layout(self, new_layout: LayoutManager) -> None:
        """Update layout manager and recalculate positions."""
        self.layout = new_layout
        self.initialize_positions()
        
        # Update any existing card positions based on new layout
        # This would require more complex logic to maintain relative positions
        # For now, we'll just update the reference positions
    
    def get_debug_info(self) -> Dict[str, Any]:
        """Get debug information about current animation state."""
        return {
            'active_animations': self.animation_system.get_active_count(),
            'animated_cards': len(self.animated_cards),
            'is_dealing': self.current_dealing,
            'dealing_queue_size': len(self.dealing_queue),
            'animations_enabled': self.animations_enabled,
            'cached_surfaces': len(self._card_surfaces)
        }
