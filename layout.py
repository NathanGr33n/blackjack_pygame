# layout.py
# NathanGr33n
# September 1, 2025

"""Responsive layout manager for dynamic UI positioning and scaling.

This module provides a layout system that adapts UI elements to different
screen sizes and aspect ratios, ensuring optimal user experience across
various display configurations.
"""

from __future__ import annotations

import pygame
from typing import NamedTuple, Tuple, Dict, Any
from enum import Enum


class Anchor(Enum):
    """Anchor points for positioning elements relative to screen edges."""
    TOP_LEFT = "top_left"
    TOP_CENTER = "top_center" 
    TOP_RIGHT = "top_right"
    CENTER_LEFT = "center_left"
    CENTER = "center"
    CENTER_RIGHT = "center_right"
    BOTTOM_LEFT = "bottom_left"
    BOTTOM_CENTER = "bottom_center"
    BOTTOM_RIGHT = "bottom_right"


class Dimensions(NamedTuple):
    """Screen dimensions with calculated properties."""
    width: int
    height: int
    aspect_ratio: float
    scale_factor: float


class LayoutManager:
    """Manages responsive layout for game UI elements."""
    
    # Standard reference resolution (what the game was originally designed for)
    REFERENCE_WIDTH = 800
    REFERENCE_HEIGHT = 600
    MIN_WIDTH = 640
    MIN_HEIGHT = 480
    
    def __init__(self, initial_width: int = REFERENCE_WIDTH, 
                 initial_height: int = REFERENCE_HEIGHT):
        """Initialize layout manager with screen dimensions."""
        self.dimensions = self._calculate_dimensions(initial_width, initial_height)
        self._layout_cache: Dict[str, Any] = {}
    
    def _calculate_dimensions(self, width: int, height: int) -> Dimensions:
        """Calculate screen dimensions and scaling factors."""
        # Ensure minimum dimensions
        width = max(width, self.MIN_WIDTH)
        height = max(height, self.MIN_HEIGHT)
        
        aspect_ratio = width / height
        
        # Calculate scale factor based on the smaller dimension to maintain proportions
        scale_x = width / self.REFERENCE_WIDTH
        scale_y = height / self.REFERENCE_HEIGHT
        scale_factor = min(scale_x, scale_y)  # Use smaller scale to prevent overflow
        
        return Dimensions(width, height, aspect_ratio, scale_factor)
    
    def update_dimensions(self, width: int, height: int) -> None:
        """Update layout dimensions and clear cache."""
        self.dimensions = self._calculate_dimensions(width, height)
        self._layout_cache.clear()
    
    def get_scaled_size(self, original_width: int, original_height: int) -> Tuple[int, int]:
        """Scale dimensions based on current screen size."""
        return (
            int(original_width * self.dimensions.scale_factor),
            int(original_height * self.dimensions.scale_factor)
        )
    
    def get_position(self, x_percent: float, y_percent: float, 
                    anchor: Anchor = Anchor.TOP_LEFT) -> Tuple[int, int]:
        """Get absolute position from percentage coordinates.
        
        Args:
            x_percent: X position as percentage (0.0 to 1.0)
            y_percent: Y position as percentage (0.0 to 1.0)
            anchor: Anchor point for positioning
            
        Returns:
            Tuple of (x, y) absolute coordinates
        """
        base_x = int(x_percent * self.dimensions.width)
        base_y = int(y_percent * self.dimensions.height)
        
        return self._apply_anchor(base_x, base_y, anchor)
    
    def _apply_anchor(self, x: int, y: int, anchor: Anchor) -> Tuple[int, int]:
        """Apply anchor offset to coordinates."""
        # For now, return base coordinates (can be extended for complex anchoring)
        return (x, y)
    
    def get_rect(self, x_percent: float, y_percent: float, 
                width: int, height: int, anchor: Anchor = Anchor.TOP_LEFT) -> pygame.Rect:
        """Create a pygame.Rect with responsive positioning.
        
        Args:
            x_percent: X position as percentage (0.0 to 1.0)
            y_percent: Y position as percentage (0.0 to 1.0)
            width: Original width (will be scaled)
            height: Original height (will be scaled)
            anchor: Anchor point for positioning
            
        Returns:
            pygame.Rect with scaled dimensions and positioned coordinates
        """
        pos_x, pos_y = self.get_position(x_percent, y_percent, anchor)
        scaled_width, scaled_height = self.get_scaled_size(width, height)
        
        return pygame.Rect(pos_x, pos_y, scaled_width, scaled_height)
    
    def get_font_size(self, base_size: int) -> int:
        """Get scaled font size based on screen resolution."""
        return max(int(base_size * self.dimensions.scale_factor), 8)  # Minimum 8pt font
    
    def get_card_size(self) -> Tuple[int, int]:
        """Get appropriately scaled card dimensions."""
        base_width, base_height = 80, 120
        return self.get_scaled_size(base_width, base_height)
    
    def get_chip_size(self) -> Tuple[int, int]:
        """Get appropriately scaled chip dimensions."""
        base_size = 40
        scaled_size = int(base_size * self.dimensions.scale_factor)
        return (scaled_size, scaled_size)
    
    def get_button_layout(self) -> Dict[str, pygame.Rect]:
        """Get all button positions using responsive layout."""
        cache_key = f"buttons_{self.dimensions.width}x{self.dimensions.height}"
        
        if cache_key in self._layout_cache:
            return self._layout_cache[cache_key]
        
        # Button dimensions (will be scaled)
        button_width, button_height = 100, 40
        small_button_width, small_button_height = 40, 30
        
        # Calculate button positions as percentages of screen
        buttons = {
            'hit': self.get_rect(0.125, 0.883, button_width, button_height),      # ~100, 530
            'stand': self.get_rect(0.3125, 0.883, button_width, button_height),   # ~250, 530
            'hint': self.get_rect(0.475, 0.883, button_width, button_height),     # ~380, 530
            'restart': self.get_rect(0.625, 0.883, 120, button_height),           # ~500, 530
            'bet_plus': self.get_rect(0.7875, 0.15, small_button_width, small_button_height),  # ~630, 90
            'bet_minus': self.get_rect(0.7125, 0.15, small_button_width, small_button_height), # ~570, 90
        }
        
        self._layout_cache[cache_key] = buttons
        return buttons
    
    def get_text_positions(self) -> Dict[str, Tuple[int, int]]:
        """Get text positions using responsive layout."""
        return {
            'player_score': self.get_position(0.125, 0.617),      # ~100, 370
            'dealer_score': self.get_position(0.125, 0.383),      # ~100, 230
            'chips': self.get_position(0.7125, 0.033),            # ~570, 20
            'bet': self.get_position(0.7125, 0.1),                # ~570, 60
            'winner': self.get_position(0.625, 0.617),            # ~500, 370
            'hint_text': self.get_position(0.45, 0.817),          # ~360, 490
        }
    
    def get_hand_positions(self) -> Dict[str, Tuple[int, int]]:
        """Get card hand positions using responsive layout."""
        return {
            'player': self.get_position(0.125, 0.667),            # ~100, 400
            'dealer': self.get_position(0.125, 0.167),            # ~100, 100
        }
    
    def get_chip_stack_position(self) -> Tuple[int, int]:
        """Get chip stack position using responsive layout."""
        return self.get_position(0.75, 0.417)                    # ~600, 250
    
    def get_stats_panel_position(self) -> Tuple[int, int]:
        """Get statistics panel position using responsive layout."""
        return self.get_position(0.0125, 0.033)                  # ~10, 20
    
    def get_stats_panel_size(self) -> Tuple[int, int]:
        """Get scaled statistics panel size."""
        return self.get_scaled_size(200, 140)
    
    def get_card_hand_offset(self) -> int:
        """Get spacing between cards in a hand."""
        return int(100 * self.dimensions.scale_factor)
    
    def is_mobile_layout(self) -> bool:
        """Determine if mobile layout adjustments should be applied."""
        return (self.dimensions.width < 800 or 
                self.dimensions.height < 600 or 
                self.dimensions.aspect_ratio < 1.2)
    
    def get_debug_info(self) -> Dict[str, Any]:
        """Get layout debug information."""
        return {
            'dimensions': self.dimensions._asdict(),
            'is_mobile': self.is_mobile_layout(),
            'cache_size': len(self._layout_cache),
        }
