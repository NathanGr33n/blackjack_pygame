# animation_config.py
# NathanGr33n
# September 3, 2025

"""
Configuration system for card animations in the Blackjack game.

This module provides a comprehensive configuration system that allows easy
customization of animation timing, easing, visual effects, and behavior
through JSON files and runtime settings.
"""

from __future__ import annotations
import json
import os
from dataclasses import dataclass, asdict, field
from typing import Dict, Any, Optional, List
from enum import Enum

from animations import EaseType


class AnimationSpeed(Enum):
    """Preset animation speed configurations."""
    VERY_SLOW = "very_slow"
    SLOW = "slow" 
    NORMAL = "normal"
    FAST = "fast"
    VERY_FAST = "very_fast"
    INSTANT = "instant"


class AnimationQuality(Enum):
    """Animation quality presets affecting performance vs visual fidelity."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    ULTRA = "ultra"


@dataclass
class DealAnimationSettings:
    """Configuration for card dealing animations."""
    duration: float = 0.6
    delay_between_cards: float = 0.2
    start_scale: float = 0.7
    end_scale: float = 1.0
    rotation_start: float = -5.0
    rotation_end: float = 0.0
    ease_type: EaseType = EaseType.EASE_OUT
    
    # Visual effects
    show_card_trail: bool = False
    trail_length: int = 3
    highlight_destination: bool = True


@dataclass
class HitAnimationSettings:
    """Configuration for hit card animations."""
    duration: float = 0.4
    start_scale: float = 0.8
    end_scale: float = 1.0
    bounce_height: float = 10.0
    ease_type: EaseType = EaseType.EASE_OUT
    
    # Visual effects
    add_spin: bool = False
    spin_degrees: float = 180.0


@dataclass
class FlipAnimationSettings:
    """Configuration for card flip animations."""
    duration: float = 0.5
    ease_type: EaseType = EaseType.EASE_IN_OUT
    flip_axis: str = "horizontal"  # "horizontal" or "vertical"
    
    # Visual effects
    add_glow: bool = False
    glow_color: tuple = (255, 255, 0)  # RGB
    pause_at_edge: float = 0.1  # Pause time when card is edge-on


@dataclass
class CollectAnimationSettings:
    """Configuration for card collection animations."""
    duration: float = 0.8
    delay_between_cards: float = 0.1
    end_scale: float = 0.3
    ease_type: EaseType = EaseType.EASE_IN
    
    # Visual effects
    fade_out: bool = True
    spiral_motion: bool = False
    spiral_tightness: float = 2.0


@dataclass
class BounceAnimationSettings:
    """Configuration for bounce/highlight animations."""
    duration: float = 0.4
    bounce_height: float = 15.0
    bounces: int = 1
    ease_type: EaseType = EaseType.BOUNCE_OUT
    
    # Visual effects
    scale_bounce: bool = True
    scale_amount: float = 0.1  # How much to scale (±)


@dataclass
class VisualEffectsSettings:
    """Configuration for visual effects and rendering."""
    enable_shadows: bool = True
    shadow_offset: tuple = (3, 3)
    shadow_color: tuple = (0, 0, 0, 100)  # RGBA
    
    enable_glow: bool = False
    glow_intensity: float = 0.3
    
    enable_particle_effects: bool = False
    particle_count: int = 10
    
    enable_sound_effects: bool = False
    card_deal_sound: str = "card_deal.wav"
    card_flip_sound: str = "card_flip.wav"
    card_collect_sound: str = "card_collect.wav"


@dataclass
class PerformanceSettings:
    """Configuration for performance optimization."""
    max_concurrent_animations: int = 50
    use_animation_pooling: bool = True
    cache_card_surfaces: bool = True
    max_cached_surfaces: int = 100
    
    # Quality vs performance trade-offs
    interpolation_steps: int = 60  # Steps per second for smooth animation
    use_sub_pixel_positioning: bool = True
    anti_aliased_rotation: bool = True


@dataclass
class GameplaySettings:
    """Configuration for gameplay-related animation behavior."""
    wait_for_deal_complete: bool = True
    allow_skip_animations: bool = True
    skip_key: str = "space"
    
    auto_reveal_dealer: bool = True
    dealer_reveal_delay: float = 0.5
    
    animate_hand_values: bool = True
    animate_button_highlights: bool = True
    
    # Accessibility
    reduce_motion: bool = False
    high_contrast_mode: bool = False
    animation_descriptions: bool = False  # For screen readers


@dataclass
class AnimationPreset:
    """Complete animation preset configuration."""
    name: str
    description: str
    deal: DealAnimationSettings = field(default_factory=DealAnimationSettings)
    hit: HitAnimationSettings = field(default_factory=HitAnimationSettings)
    flip: FlipAnimationSettings = field(default_factory=FlipAnimationSettings)
    collect: CollectAnimationSettings = field(default_factory=CollectAnimationSettings)
    bounce: BounceAnimationSettings = field(default_factory=BounceAnimationSettings)
    visual_effects: VisualEffectsSettings = field(default_factory=VisualEffectsSettings)
    performance: PerformanceSettings = field(default_factory=PerformanceSettings)
    gameplay: GameplaySettings = field(default_factory=GameplaySettings)


class AnimationConfigManager:
    """Manager for animation configuration with preset support."""
    
    def __init__(self, config_file: str = "animation_config.json"):
        self.config_file = config_file
        self.current_preset = self._create_default_preset()
        self.presets: Dict[str, AnimationPreset] = {}
        
        # Create built-in presets
        self._create_builtin_presets()
        
        # Load from file if it exists
        self.load_config()
    
    def _create_default_preset(self) -> AnimationPreset:
        """Create the default animation preset."""
        return AnimationPreset(
            name="Default",
            description="Balanced animations for good visual appeal and performance"
        )
    
    def _create_builtin_presets(self) -> None:
        """Create built-in animation presets."""
        
        # Performance preset - minimal animations
        performance_preset = AnimationPreset(
            name="Performance",
            description="Minimal animations optimized for performance",
            deal=DealAnimationSettings(duration=0.3, delay_between_cards=0.1),
            hit=HitAnimationSettings(duration=0.2),
            flip=FlipAnimationSettings(duration=0.3),
            collect=CollectAnimationSettings(duration=0.4, delay_between_cards=0.05),
            bounce=BounceAnimationSettings(duration=0.2),
            performance=PerformanceSettings(
                max_concurrent_animations=20,
                interpolation_steps=30,
                anti_aliased_rotation=False
            )
        )
        
        # Cinematic preset - elaborate animations
        cinematic_preset = AnimationPreset(
            name="Cinematic",
            description="Rich, elaborate animations for maximum visual impact",
            deal=DealAnimationSettings(
                duration=1.0,
                delay_between_cards=0.3,
                show_card_trail=True,
                trail_length=5,
                highlight_destination=True
            ),
            hit=HitAnimationSettings(
                duration=0.8,
                bounce_height=20.0,
                add_spin=True,
                spin_degrees=360.0
            ),
            flip=FlipAnimationSettings(
                duration=0.8,
                add_glow=True,
                pause_at_edge=0.2
            ),
            collect=CollectAnimationSettings(
                duration=1.2,
                delay_between_cards=0.15,
                spiral_motion=True,
                spiral_tightness=3.0
            ),
            bounce=BounceAnimationSettings(
                duration=0.6,
                bounces=2,
                scale_bounce=True
            ),
            visual_effects=VisualEffectsSettings(
                enable_shadows=True,
                enable_glow=True,
                enable_particle_effects=True,
                particle_count=20
            ),
            performance=PerformanceSettings(
                interpolation_steps=120,
                anti_aliased_rotation=True
            )
        )
        
        # Accessibility preset - reduced motion
        accessibility_preset = AnimationPreset(
            name="Accessibility",
            description="Reduced motion animations for accessibility",
            deal=DealAnimationSettings(duration=0.2, delay_between_cards=0.05),
            hit=HitAnimationSettings(duration=0.1, bounce_height=5.0),
            flip=FlipAnimationSettings(duration=0.2),
            collect=CollectAnimationSettings(duration=0.3, fade_out=False),
            bounce=BounceAnimationSettings(duration=0.1, bounce_height=5.0),
            visual_effects=VisualEffectsSettings(
                enable_shadows=False,
                enable_glow=False,
                enable_particle_effects=False
            ),
            gameplay=GameplaySettings(
                reduce_motion=True,
                high_contrast_mode=True,
                animation_descriptions=True
            )
        )
        
        self.presets = {
            "default": self._create_default_preset(),
            "performance": performance_preset,
            "cinematic": cinematic_preset,
            "accessibility": accessibility_preset
        }
    
    def apply_speed_preset(self, speed: AnimationSpeed) -> None:
        """Apply a speed preset to current configuration."""
        speed_multipliers = {
            AnimationSpeed.VERY_SLOW: 2.0,
            AnimationSpeed.SLOW: 1.5,
            AnimationSpeed.NORMAL: 1.0,
            AnimationSpeed.FAST: 0.7,
            AnimationSpeed.VERY_FAST: 0.4,
            AnimationSpeed.INSTANT: 0.1
        }
        
        multiplier = speed_multipliers.get(speed, 1.0)
        
        # Apply multiplier to all duration settings
        self.current_preset.deal.duration *= multiplier
        self.current_preset.deal.delay_between_cards *= multiplier
        self.current_preset.hit.duration *= multiplier
        self.current_preset.flip.duration *= multiplier
        self.current_preset.collect.duration *= multiplier
        self.current_preset.collect.delay_between_cards *= multiplier
        self.current_preset.bounce.duration *= multiplier
        
        if speed == AnimationSpeed.INSTANT:
            # Disable most visual effects for instant mode
            self.current_preset.visual_effects.enable_shadows = False
            self.current_preset.visual_effects.enable_glow = False
            self.current_preset.visual_effects.enable_particle_effects = False
    
    def apply_quality_preset(self, quality: AnimationQuality) -> None:
        """Apply a quality preset to current configuration."""
        quality_settings = {
            AnimationQuality.LOW: {
                'interpolation_steps': 30,
                'anti_aliased_rotation': False,
                'enable_shadows': False,
                'enable_glow': False,
                'enable_particle_effects': False,
                'max_concurrent_animations': 10
            },
            AnimationQuality.MEDIUM: {
                'interpolation_steps': 45,
                'anti_aliased_rotation': True,
                'enable_shadows': True,
                'enable_glow': False,
                'enable_particle_effects': False,
                'max_concurrent_animations': 25
            },
            AnimationQuality.HIGH: {
                'interpolation_steps': 60,
                'anti_aliased_rotation': True,
                'enable_shadows': True,
                'enable_glow': True,
                'enable_particle_effects': False,
                'max_concurrent_animations': 50
            },
            AnimationQuality.ULTRA: {
                'interpolation_steps': 120,
                'anti_aliased_rotation': True,
                'enable_shadows': True,
                'enable_glow': True,
                'enable_particle_effects': True,
                'max_concurrent_animations': 100
            }
        }
        
        settings = quality_settings.get(quality, quality_settings[AnimationQuality.MEDIUM])
        
        # Apply settings
        self.current_preset.performance.interpolation_steps = settings['interpolation_steps']
        self.current_preset.performance.anti_aliased_rotation = settings['anti_aliased_rotation']
        self.current_preset.performance.max_concurrent_animations = settings['max_concurrent_animations']
        
        self.current_preset.visual_effects.enable_shadows = settings['enable_shadows']
        self.current_preset.visual_effects.enable_glow = settings['enable_glow']
        self.current_preset.visual_effects.enable_particle_effects = settings['enable_particle_effects']
    
    def load_preset(self, preset_name: str) -> bool:
        """Load a specific animation preset."""
        if preset_name in self.presets:
            self.current_preset = self.presets[preset_name]
            return True
        return False
    
    def save_custom_preset(self, name: str, description: str = "") -> None:
        """Save current configuration as a custom preset."""
        custom_preset = AnimationPreset(
            name=name,
            description=description,
            deal=self.current_preset.deal,
            hit=self.current_preset.hit,
            flip=self.current_preset.flip,
            collect=self.current_preset.collect,
            bounce=self.current_preset.bounce,
            visual_effects=self.current_preset.visual_effects,
            performance=self.current_preset.performance,
            gameplay=self.current_preset.gameplay
        )
        self.presets[name] = custom_preset
    
    def get_preset_names(self) -> List[str]:
        """Get list of available preset names."""
        return list(self.presets.keys())
    
    def load_config(self) -> bool:
        """Load configuration from JSON file."""
        if not os.path.exists(self.config_file):
            return False
        
        try:
            with open(self.config_file, 'r') as f:
                data = json.load(f)
            
            # Load current preset
            if 'current_preset' in data:
                preset_data = data['current_preset']
                self.current_preset = AnimationPreset(**preset_data)
            
            # Load custom presets
            if 'custom_presets' in data:
                for name, preset_data in data['custom_presets'].items():
                    self.presets[name] = AnimationPreset(**preset_data)
            
            return True
        except Exception as e:
            print(f"Error loading animation config: {e}")
            return False
    
    def save_config(self) -> bool:
        """Save configuration to JSON file."""
        try:
            # Prepare data for serialization
            data = {
                'current_preset': asdict(self.current_preset),
                'custom_presets': {}
            }
            
            # Save only custom presets (not built-in ones)
            builtin_names = {'default', 'performance', 'cinematic', 'accessibility'}
            for name, preset in self.presets.items():
                if name not in builtin_names:
                    data['custom_presets'][name] = asdict(preset)
            
            with open(self.config_file, 'w') as f:
                json.dump(data, f, indent=2, default=str)
            
            return True
        except Exception as e:
            print(f"Error saving animation config: {e}")
            return False
    
    def get_current_config(self) -> AnimationPreset:
        """Get the current animation configuration."""
        return self.current_preset
    
    def reset_to_default(self) -> None:
        """Reset configuration to default preset."""
        self.current_preset = self._create_default_preset()
    
    def create_config_ui_data(self) -> Dict[str, Any]:
        """Create data structure for configuration UI."""
        return {
            'current_preset_name': self.current_preset.name,
            'available_presets': [(name, preset.description) 
                                 for name, preset in self.presets.items()],
            'speed_options': [speed.value for speed in AnimationSpeed],
            'quality_options': [quality.value for quality in AnimationQuality],
            'ease_types': [ease.value for ease in EaseType],
            'current_settings': {
                'deal_duration': self.current_preset.deal.duration,
                'hit_duration': self.current_preset.hit.duration,
                'flip_duration': self.current_preset.flip.duration,
                'visual_effects_enabled': any([
                    self.current_preset.visual_effects.enable_shadows,
                    self.current_preset.visual_effects.enable_glow,
                    self.current_preset.visual_effects.enable_particle_effects
                ]),
                'reduce_motion': self.current_preset.gameplay.reduce_motion
            }
        }
