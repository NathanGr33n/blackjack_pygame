# animations.py
# NathanGr33n
# September 3, 2025

"""
Comprehensive card animation system for Blackjack game.

This module provides a complete animation framework for card movements,
including sliding, flipping, bouncing, and other effects. The system
integrates seamlessly with the existing pygame-based game architecture.
"""

from __future__ import annotations
import math
import pygame
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Callable, Dict, List, Optional, Tuple, Union, Any


class EaseType(Enum):
    """Enumeration of available easing functions for animations."""
    LINEAR = "linear"
    EASE_IN = "ease_in"
    EASE_OUT = "ease_out"
    EASE_IN_OUT = "ease_in_out"
    BOUNCE_OUT = "bounce_out"
    BOUNCE_IN = "bounce_in"
    ELASTIC_OUT = "elastic_out"
    BACK_OUT = "back_out"


class AnimationState(Enum):
    """Current state of an animation."""
    PENDING = "pending"
    RUNNING = "running" 
    COMPLETED = "completed"
    CANCELLED = "cancelled"


@dataclass
class AnimationConfig:
    deal_delay_between_cards: float = 0.2
    """Configuration for animation behavior and appearance."""
    duration: float = 1.0  # Duration in seconds
    delay: float = 0.0     # Delay before starting in seconds
    ease: EaseType = EaseType.EASE_OUT
    loop: bool = False
    reverse: bool = False
    auto_remove: bool = True  # Remove animation when completed


class EasingFunctions:
    """Collection of easing functions for smooth animations."""
    
    @staticmethod
    def linear(t: float) -> float:
        """Linear interpolation (no easing)."""
        return t
    
    @staticmethod
    def ease_in(t: float) -> float:
        """Accelerating from zero velocity."""
        return t * t
    
    @staticmethod
    def ease_out(t: float) -> float:
        """Decelerating to zero velocity."""
        return 1 - (1 - t) * (1 - t)
    
    @staticmethod
    def ease_in_out(t: float) -> float:
        """Acceleration until halfway, then deceleration."""
        return 3 * t * t - 2 * t * t * t
    
    @staticmethod
    def bounce_out(t: float) -> float:
        """Bouncing effect at the end."""
        if t < 1/2.75:
            return 7.5625 * t * t
        elif t < 2/2.75:
            t -= 1.5/2.75
            return 7.5625 * t * t + 0.75
        elif t < 2.5/2.75:
            t -= 2.25/2.75
            return 7.5625 * t * t + 0.9375
        else:
            t -= 2.625/2.75
            return 7.5625 * t * t + 0.984375
    
    @staticmethod
    def bounce_in(t: float) -> float:
        """Bouncing effect at the beginning."""
        return 1 - EasingFunctions.bounce_out(1 - t)
    
    @staticmethod
    def elastic_out(t: float) -> float:
        """Elastic snap at the end."""
        if t == 0 or t == 1:
            return t
        return 2**(-10*t) * math.sin((t - 0.1) * 2 * math.pi / 0.4) + 1
    
    @staticmethod
    def back_out(t: float) -> float:
        """Overshoot then settle."""
        c1 = 1.70158
        c3 = c1 + 1
        return 1 + c3 * (t - 1)**3 + c1 * (t - 1)**2
    
    @staticmethod
    def get_function(ease_type: EaseType) -> Callable[[float], float]:
        """Get easing function by type."""
        mapping = {
            EaseType.LINEAR: EasingFunctions.linear,
            EaseType.EASE_IN: EasingFunctions.ease_in,
            EaseType.EASE_OUT: EasingFunctions.ease_out,
            EaseType.EASE_IN_OUT: EasingFunctions.ease_in_out,
            EaseType.BOUNCE_OUT: EasingFunctions.bounce_out,
            EaseType.BOUNCE_IN: EasingFunctions.bounce_in,
            EaseType.ELASTIC_OUT: EasingFunctions.elastic_out,
            EaseType.BACK_OUT: EasingFunctions.back_out,
        }
        return mapping.get(ease_type, EasingFunctions.linear)


class BaseAnimation(ABC):
    """Abstract base class for all animations."""
    
    def __init__(self, target: Any, config: AnimationConfig):
        self.target = target
        self.config = config
        self.state = AnimationState.PENDING
        self.start_time = 0.0
        self.current_time = 0.0
        self.progress = 0.0
        self.easing_func = EasingFunctions.get_function(config.ease)
        self._on_complete_callbacks: List[Callable] = []
        self._on_update_callbacks: List[Callable[[float], None]] = []
    
    def start(self) -> None:
        """Start the animation."""
        self.start_time = time.time() + self.config.delay
        self.state = AnimationState.RUNNING
    
    def update(self, delta_time: float) -> bool:
        """
        Update animation state.
        
        Args:
            delta_time: Time elapsed since last update
            
        Returns:
            True if animation is still running, False if completed
        """
        if self.state != AnimationState.RUNNING:
            return self.state == AnimationState.RUNNING
        
        self.current_time = time.time()
        
        # Check if animation hasn't started due to delay
        if self.current_time < self.start_time:
            return True
        
        # Calculate progress (0.0 to 1.0)
        elapsed = self.current_time - self.start_time
        if self.config.duration <= 0:
            self.progress = 1.0
        else:
            self.progress = min(elapsed / self.config.duration, 1.0)
        
        # Apply easing function
        eased_progress = self.easing_func(self.progress)
        
        # Apply animation-specific updates
        self._apply_animation(eased_progress)
        
        # Call update callbacks
        for callback in self._on_update_callbacks:
            callback(eased_progress)
        
        # Check if animation is complete
        if self.progress >= 1.0:
            self.state = AnimationState.COMPLETED
            self._on_complete()
            return not self.config.auto_remove
        
        return True
    
    def cancel(self) -> None:
        """Cancel the animation."""
        self.state = AnimationState.CANCELLED
    
    def on_complete(self, callback: Callable) -> BaseAnimation:
        """Add callback for when animation completes."""
        self._on_complete_callbacks.append(callback)
        return self
    
    def on_update(self, callback: Callable[[float], None]) -> BaseAnimation:
        """Add callback for animation updates."""
        self._on_update_callbacks.append(callback)
        return self
    
    def _on_complete(self) -> None:
        """Internal completion handler."""
        for callback in self._on_complete_callbacks:
            callback()
    
    @abstractmethod
    def _apply_animation(self, progress: float) -> None:
        """Apply animation-specific transformations."""
        pass


class AnimationSystem:
    """Central manager for all animations in the game."""
    
    def __init__(self):
        self.animations: List[BaseAnimation] = []
        self.paused = False
        self.last_update_time = time.time()
    
    def add_animation(self, animation: BaseAnimation) -> BaseAnimation:
        """Add an animation to the system."""
        self.animations.append(animation)
        animation.start()
        return animation
    
    def remove_animation(self, animation: BaseAnimation) -> None:
        """Remove an animation from the system."""
        if animation in self.animations:
            self.animations.remove(animation)
    
    def update(self, delta_time: Optional[float] = None) -> None:
        """Update all active animations."""
        if self.paused:
            return
        
        if delta_time is None:
            current_time = time.time()
            delta_time = current_time - self.last_update_time
            self.last_update_time = current_time
        
        # Update animations and remove completed ones
        active_animations = []
        for animation in self.animations:
            if animation.update(delta_time):
                active_animations.append(animation)
        
        self.animations = active_animations
    
    def pause(self) -> None:
        """Pause all animations."""
        self.paused = True
    
    def resume(self) -> None:
        """Resume all animations."""
        self.paused = False
        self.last_update_time = time.time()
    
    def clear_all(self) -> None:
        """Clear all animations."""
        for animation in self.animations:
            animation.cancel()
        self.animations.clear()
    
    def get_active_count(self) -> int:
        """Get count of active animations."""
        return len([a for a in self.animations if a.state == AnimationState.RUNNING])
    
    def has_animations(self) -> bool:
        """Check if there are any active animations."""
        return len(self.animations) > 0


# Utility functions for common animation operations
def interpolate(start: float, end: float, progress: float) -> float:
    """Linear interpolation between two values."""
    return start + (end - start) * progress


def interpolate_point(start: Tuple[float, float], end: Tuple[float, float], 
                     progress: float) -> Tuple[float, float]:
    """Linear interpolation between two points."""
    return (
        interpolate(start[0], end[0], progress),
        interpolate(start[1], end[1], progress)
    )


def interpolate_color(start: Tuple[int, int, int], end: Tuple[int, int, int], 
                     progress: float) -> Tuple[int, int, int]:
    """Linear interpolation between two RGB colors."""
    return (
        int(interpolate(start[0], end[0], progress)),
        int(interpolate(start[1], end[1], progress)),
        int(interpolate(start[2], end[2], progress))
    )
