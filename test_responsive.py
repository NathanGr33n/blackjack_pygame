# test_responsive.py
# Quick test to verify responsive layout functionality

"""Simple test script to verify the responsive layout implementation."""

import pygame
import sys
from layout import LayoutManager

def test_layout_manager():
    """Test the LayoutManager at different resolutions."""
    pygame.init()
    
    # Test different resolutions
    test_resolutions = [
        (640, 480),   # Small
        (800, 600),   # Reference
        (1024, 768),  # Medium
        (1280, 720),  # HD
        (1920, 1080), # Full HD
    ]
    
    print("🧪 Testing LayoutManager at different resolutions:")
    print("=" * 60)
    
    for width, height in test_resolutions:
        layout = LayoutManager(width, height)
        
        print(f"\n📐 Resolution: {width}x{height}")
        print(f"   Scale Factor: {layout.dimensions.scale_factor:.3f}")
        print(f"   Aspect Ratio: {layout.dimensions.aspect_ratio:.3f}")
        print(f"   Mobile Layout: {'Yes' if layout.is_mobile_layout() else 'No'}")
        
        # Test some key positions
        buttons = layout.get_button_layout()
        text_pos = layout.get_text_positions()
        
        print(f"   Hit Button: {buttons['hit']}")
        print(f"   Chips Text: {text_pos['chips']}")
        print(f"   Card Size: {layout.get_card_size()}")
        print(f"   Font Size: {layout.get_font_size(24)}")

def test_interactive():
    """Interactive test - open window for manual testing."""
    pygame.init()
    
    width, height = 800, 600
    screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    pygame.display.set_caption("Responsive Layout Test - Resize the window!")
    
    layout = LayoutManager(width, height)
    font = pygame.font.SysFont("Arial", layout.get_font_size(24))
    clock = pygame.time.Clock()
    
    print("\n🖥️  Interactive test launched!")
    print("   Try resizing the window to see responsive behavior")
    print("   Press ESC to exit")
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.VIDEORESIZE:
                width, height = event.w, event.h
                screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
                layout.update_dimensions(width, height)
                font_size = layout.get_font_size(24)
                font = pygame.font.SysFont("Arial", font_size)
        
        # Clear screen
        screen.fill((0, 128, 0))
        
        # Get responsive positions
        buttons = layout.get_button_layout()
        text_positions = layout.get_text_positions()
        
        # Draw test elements
        # Buttons
        pygame.draw.rect(screen, (200, 200, 200), buttons['hit'])
        pygame.draw.rect(screen, (200, 200, 200), buttons['stand'])
        pygame.draw.rect(screen, (150, 200, 255), buttons['hint'])
        pygame.draw.rect(screen, (100, 255, 100), buttons['restart'])
        
        # Text labels
        text_surface = font.render("Hit", True, (0, 0, 0))
        screen.blit(text_surface, (buttons['hit'].x + 10, buttons['hit'].y + 10))
        
        text_surface = font.render("Stand", True, (0, 0, 0))
        screen.blit(text_surface, (buttons['stand'].x + 10, buttons['stand'].y + 10))
        
        # Display info
        info_lines = [
            f"Resolution: {width}x{height}",
            f"Scale: {layout.dimensions.scale_factor:.3f}",
            f"Mobile: {'Yes' if layout.is_mobile_layout() else 'No'}",
            "Resize window to test responsiveness!",
        ]
        
        for i, line in enumerate(info_lines):
            text_surface = font.render(line, True, (255, 255, 255))
            screen.blit(text_surface, (10, 10 + i * 25))
        
        # Stats panel preview
        stats_pos = layout.get_stats_panel_position()
        stats_size = layout.get_stats_panel_size()
        stats_panel = pygame.Rect(stats_pos[0], stats_pos[1], stats_size[0], stats_size[1])
        pygame.draw.rect(screen, (0, 100, 0), stats_panel)
        pygame.draw.rect(screen, (255, 255, 255), stats_panel, 2)
        
        text_surface = font.render("Stats Panel", True, (255, 255, 255))
        screen.blit(text_surface, (stats_pos[0] + 10, stats_pos[1] + 10))
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    print("🃏 Blackjack PyGame - Responsive Layout Test")
    print("=" * 50)
    
    # Run automated tests
    test_layout_manager()
    
    # Ask for interactive test
    print("\n" + "=" * 60)
    choice = input("Run interactive test? (y/n): ").lower().strip()
    if choice in ['y', 'yes']:
        test_interactive()
    else:
        print("✅ Tests complete!")
