# card_animations.py
# NathanGr33n
# September 3, 2025

"""
Specialized card animations for the Blackjack game.

This module contains card-specific animation classes that extend the base
animation system to provide realistic card movements and effects.
"""

from __future__ import annotations
import math
import pygame
from typing import Tuple, Optional, Dict, Any
from dataclasses import dataclass

from animations import BaseAnimation, AnimationConfig, EaseType, interpolate, interpolate_point
from deck import Card


@dataclass
class CardRenderState:
    """Represents the visual state of a card during animation."""
    position: Tuple[float, float] = (0, 0)
    rotation: float = 0.0  # Degrees
    scale: float = 1.0
    alpha: int = 255  # 0-255 opacity
    flip_progress: float = 0.0  # 0=face up, 0.5=edge, 1.0=back
    z_offset: int = 0  # For layering during animations
    
    def copy(self) -> CardRenderState:
        """Create a copy of this render state."""
        return CardRenderState(
            position=self.position,
            rotation=self.rotation,
            scale=self.scale,
            alpha=self.alpha,
            flip_progress=self.flip_progress,
            z_offset=self.z_offset
        )


class AnimatedCard:
    """Wrapper for a card with animation state and rendering capabilities."""
    
    def __init__(self, card: Card, initial_position: Tuple[float, float] = (0, 0)):
        self.card = card
        self.render_state = CardRenderState(position=initial_position)
        self.target_state = CardRenderState(position=initial_position)
        self.is_face_up = True
        self.visible = True
        
        # Cached surfaces for performance
        self._cached_front: Optional[pygame.Surface] = None
        self._cached_back: Optional[pygame.Surface] = None
        self._cached_size: Tuple[int, int] = (0, 0)
    
    def set_position(self, position: Tuple[float, float]) -> None:
        """Set card position immediately."""
        self.render_state.position = position
        self.target_state.position = position
    
    def get_position(self) -> Tuple[float, float]:
        """Get current card position."""
        return self.render_state.position
    
    def get_rect(self, card_size: Tuple[int, int]) -> pygame.Rect:
        """Get the card's current rectangle for collision detection."""
        x, y = self.render_state.position
        w, h = card_size
        # Account for scaling
        scaled_w = int(w * self.render_state.scale)
        scaled_h = int(h * self.render_state.scale)
        # Center the rectangle on the position
        return pygame.Rect(x - scaled_w // 2, y - scaled_h // 2, scaled_w, scaled_h)
    
    def render(self, surface: pygame.Surface, card_front: pygame.Surface, 
               card_back: pygame.Surface, card_size: Tuple[int, int]) -> None:
        """Render the animated card to the surface."""
        if not self.visible or self.render_state.alpha <= 0:
            return
        
        # Choose which card surface to use based on flip progress
        if self.render_state.flip_progress < 0.5:
            # Show front
            card_surface = card_front if self.is_face_up else card_back
            flip_scale_x = 1.0 - (self.render_state.flip_progress * 2.0)
        else:
            # Show back
            card_surface = card_back if self.is_face_up else card_front
            flip_scale_x = (self.render_state.flip_progress - 0.5) * 2.0
        
        # Apply transformations
        scaled_surface = card_surface
        
        # Apply scaling (including flip scaling)
        scale_x = self.render_state.scale * flip_scale_x
        scale_y = self.render_state.scale
        
        if scale_x != 1.0 or scale_y != 1.0:
            new_width = max(1, int(card_size[0] * scale_x))
            new_height = max(1, int(card_size[1] * scale_y))
            scaled_surface = pygame.transform.scale(scaled_surface, (new_width, new_height))
        
        # Apply rotation
        if self.render_state.rotation != 0:
            scaled_surface = pygame.transform.rotate(scaled_surface, self.render_state.rotation)
        
        # Apply alpha
        if self.render_state.alpha < 255:
            scaled_surface = scaled_surface.copy()
            scaled_surface.set_alpha(self.render_state.alpha)
        
        # Calculate position (center the card)
        rect = scaled_surface.get_rect()
        rect.center = self.render_state.position
        
        surface.blit(scaled_surface, rect)


class SlideAnimation(BaseAnimation):
    """Animate a card sliding from one position to another."""
    
    def __init__(self, animated_card: AnimatedCard, start_pos: Tuple[float, float], 
                 end_pos: Tuple[float, float], config: AnimationConfig):
        super().__init__(animated_card, config)
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.animated_card = animated_card
        
        # Set initial position
        self.animated_card.render_state.position = start_pos
    
    def _apply_animation(self, progress: float) -> None:
        """Apply sliding animation."""
        current_pos = interpolate_point(self.start_pos, self.end_pos, progress)
        self.animated_card.render_state.position = current_pos


class FlipAnimation(BaseAnimation):
    """Animate a card flipping from front to back or vice versa."""
    
    def __init__(self, animated_card: AnimatedCard, flip_to_back: bool, config: AnimationConfig):
        super().__init__(animated_card, config)
        self.animated_card = animated_card
        self.flip_to_back = flip_to_back
        self.start_flip = 0.0 if not flip_to_back else 1.0
        self.end_flip = 1.0 if flip_to_back else 0.0
    
    def _apply_animation(self, progress: float) -> None:
        """Apply flipping animation."""
        flip_progress = interpolate(self.start_flip, self.end_flip, progress)
        self.animated_card.render_state.flip_progress = flip_progress
        
        # Update face state when flip completes
        if progress >= 1.0:
            self.animated_card.is_face_up = not self.flip_to_back


class BounceAnimation(BaseAnimation):
    """Animate a card with a bouncing effect."""
    
    def __init__(self, animated_card: AnimatedCard, bounce_height: float, config: AnimationConfig):
        super().__init__(animated_card, config)
        self.animated_card = animated_card
        self.base_position = animated_card.render_state.position
        self.bounce_height = bounce_height
    
    def _apply_animation(self, progress: float) -> None:
        """Apply bouncing animation."""
        # Use sine wave for smooth bounce
        bounce_offset = math.sin(progress * math.pi) * self.bounce_height
        x, y = self.base_position
        self.animated_card.render_state.position = (x, y - bounce_offset)


class ScaleAnimation(BaseAnimation):
    """Animate a card scaling up or down."""
    
    def __init__(self, animated_card: AnimatedCard, start_scale: float, 
                 end_scale: float, config: AnimationConfig):
        super().__init__(animated_card, config)
        self.animated_card = animated_card
        self.start_scale = start_scale
        self.end_scale = end_scale
        
        # Set initial scale
        self.animated_card.render_state.scale = start_scale
    
    def _apply_animation(self, progress: float) -> None:
        """Apply scaling animation."""
        current_scale = interpolate(self.start_scale, self.end_scale, progress)
        self.animated_card.render_state.scale = current_scale


class FadeAnimation(BaseAnimation):
    """Animate a card fading in or out."""
    
    def __init__(self, animated_card: AnimatedCard, start_alpha: int, 
                 end_alpha: int, config: AnimationConfig):
        super().__init__(animated_card, config)
        self.animated_card = animated_card
        self.start_alpha = start_alpha
        self.end_alpha = end_alpha
        
        # Set initial alpha
        self.animated_card.render_state.alpha = start_alpha
    
    def _apply_animation(self, progress: float) -> None:
        """Apply fading animation."""
        current_alpha = int(interpolate(self.start_alpha, self.end_alpha, progress))
        self.animated_card.render_state.alpha = current_alpha
        
        # Hide card completely when fully transparent
        self.animated_card.visible = current_alpha > 0


class RotationAnimation(BaseAnimation):
    """Animate a card rotating."""
    
    def __init__(self, animated_card: AnimatedCard, start_rotation: float, 
                 end_rotation: float, config: AnimationConfig):
        super().__init__(animated_card, config)
        self.animated_card = animated_card
        self.start_rotation = start_rotation
        self.end_rotation = end_rotation
        
        # Set initial rotation
        self.animated_card.render_state.rotation = start_rotation
    
    def _apply_animation(self, progress: float) -> None:
        """Apply rotation animation."""
        current_rotation = interpolate(self.start_rotation, self.end_rotation, progress)
        self.animated_card.render_state.rotation = current_rotation


class ComboAnimation(BaseAnimation):
    """Combine multiple animation effects on a single card."""
    
    def __init__(self, animated_card: AnimatedCard, config: AnimationConfig):
        super().__init__(animated_card, config)
        self.animated_card = animated_card
        self.effects: Dict[str, Dict[str, Any]] = {}
    
    def add_slide(self, start_pos: Tuple[float, float], end_pos: Tuple[float, float]) -> ComboAnimation:
        """Add sliding effect to the combo."""
        self.effects['slide'] = {'start': start_pos, 'end': end_pos}
        return self
    
    def add_scale(self, start_scale: float, end_scale: float) -> ComboAnimation:
        """Add scaling effect to the combo."""
        self.effects['scale'] = {'start': start_scale, 'end': end_scale}
        return self
    
    def add_rotation(self, start_rotation: float, end_rotation: float) -> ComboAnimation:
        """Add rotation effect to the combo."""
        self.effects['rotation'] = {'start': start_rotation, 'end': end_rotation}
        return self
    
    def add_fade(self, start_alpha: int, end_alpha: int) -> ComboAnimation:
        """Add fading effect to the combo."""
        self.effects['fade'] = {'start': start_alpha, 'end': end_alpha}
        return self
    
    def add_flip(self, flip_to_back: bool) -> ComboAnimation:
        """Add flipping effect to the combo."""
        start_flip = 0.0 if not flip_to_back else 1.0
        end_flip = 1.0 if flip_to_back else 0.0
        self.effects['flip'] = {'start': start_flip, 'end': end_flip, 'to_back': flip_to_back}
        return self
    
    def _apply_animation(self, progress: float) -> None:
        """Apply all combined effects."""
        # Apply slide effect
        if 'slide' in self.effects:
            effect = self.effects['slide']
            pos = interpolate_point(effect['start'], effect['end'], progress)
            self.animated_card.render_state.position = pos
        
        # Apply scale effect
        if 'scale' in self.effects:
            effect = self.effects['scale']
            scale = interpolate(effect['start'], effect['end'], progress)
            self.animated_card.render_state.scale = scale
        
        # Apply rotation effect
        if 'rotation' in self.effects:
            effect = self.effects['rotation']
            rotation = interpolate(effect['start'], effect['end'], progress)
            self.animated_card.render_state.rotation = rotation
        
        # Apply fade effect
        if 'fade' in self.effects:
            effect = self.effects['fade']
            alpha = int(interpolate(effect['start'], effect['end'], progress))
            self.animated_card.render_state.alpha = alpha
            self.animated_card.visible = alpha > 0
        
        # Apply flip effect
        if 'flip' in self.effects:
            effect = self.effects['flip']
            flip_progress = interpolate(effect['start'], effect['end'], progress)
            self.animated_card.render_state.flip_progress = flip_progress
            
            # Update face state when flip completes
            if progress >= 1.0:
                self.animated_card.is_face_up = not effect['to_back']


# Utility functions for creating common card animations
def create_deal_animation(animated_card: AnimatedCard, start_pos: Tuple[float, float], 
                         end_pos: Tuple[float, float], delay: float = 0.0) -> ComboAnimation:
    """Create a realistic card dealing animation."""
    config = AnimationConfig(
        duration=0.6,
        delay=delay,
        ease=EaseType.EASE_OUT
    )
    
    return (ComboAnimation(animated_card, config)
            .add_slide(start_pos, end_pos)
            .add_scale(0.7, 1.0)
            .add_rotation(-5, 0))


def create_hit_animation(animated_card: AnimatedCard, start_pos: Tuple[float, float], 
                        end_pos: Tuple[float, float]) -> ComboAnimation:
    """Create an animation for hitting (adding a card to hand)."""
    config = AnimationConfig(
        duration=0.4,
        ease=EaseType.EASE_OUT
    )
    
    return (ComboAnimation(animated_card, config)
            .add_slide(start_pos, end_pos)
            .add_scale(0.8, 1.0))


def create_flip_reveal_animation(animated_card: AnimatedCard) -> FlipAnimation:
    """Create an animation for revealing a face-down card."""
    config = AnimationConfig(
        duration=0.5,
        ease=EaseType.EASE_IN_OUT
    )
    
    return FlipAnimation(animated_card, False, config)


def create_collect_animation(animated_card: AnimatedCard, target_pos: Tuple[float, float]) -> ComboAnimation:
    """Create an animation for collecting cards at the end of a round."""
    config = AnimationConfig(
        duration=0.8,
        ease=EaseType.EASE_IN
    )
    
    return (ComboAnimation(animated_card, config)
            .add_slide(animated_card.get_position(), target_pos)
            .add_scale(1.0, 0.3)
            .add_fade(255, 0))


def create_bounce_highlight_animation(animated_card: AnimatedCard) -> BounceAnimation:
    """Create a subtle bounce animation to highlight a card."""
    config = AnimationConfig(
        duration=0.4,
        ease=EaseType.BOUNCE_OUT
    )
    
    return BounceAnimation(animated_card, 15, config)
