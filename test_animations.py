#!/usr/bin/env python3

"""Quick test to verify animation system is working correctly."""

import pygame
from layout import LayoutManager
from animation_manager import CardAnimationManager
from animation_config import AnimationConfigManager
from deck import Deck

def test_animation_system():
    """Test that the animation system initializes without errors."""
    pygame.init()
    
    # Test layout manager
    layout = LayoutManager(800, 600)
    print("✓ Layout manager created successfully")
    
    # Test animation config
    animation_config = AnimationConfigManager()
    print("✓ Animation config manager created successfully")
    
    # Test animation manager
    card_animator = CardAnimationManager(layout, animation_config.get_current_config())
    card_animator.initialize_positions()
    print("✓ Card animation manager created successfully")
    
    # Test deck
    deck = Deck()
    player_hand = [deck.deal(), deck.deal()]
    dealer_hand = [deck.deal(), deck.deal()]
    print("✓ Deck and cards created successfully")
    
    # Test animation methods exist
    assert hasattr(card_animator, 'has_animations'), "has_animations method missing"
    assert hasattr(card_animator, 'is_animating'), "is_animating method missing"
    assert hasattr(card_animator, 'deal_initial_cards'), "deal_initial_cards method missing"
    print("✓ Required animation methods exist")
    
    # Test animation state
    assert not card_animator.has_animations(), "Should start with no animations"
    assert not card_animator.is_animating(), "Should start with no animations"
    print("✓ Animation state checks working")
    
    print("\nAll tests passed! ✅")
    print("The animation system should work correctly in your game.")
    
    pygame.quit()

if __name__ == "__main__":
    test_animation_system()
