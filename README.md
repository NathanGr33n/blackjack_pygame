# 🃏 Blackjack PyGame

A fully-featured **Blackjack** game built with Python and Pygame, featuring beautiful card graphics, smooth animations, responsive layout design, authentic casino-style gameplay, and comprehensive statistics tracking. The game logic is organized around a `Game` class that manages all state and rendering, with modular components for animations, layout management, and game strategy.

**By: NathanGr33n**

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg) ![Pygame](https://img.shields.io/badge/Pygame-2.5.0+-green.svg) ![License](https://img.shields.io/badge/License-MIT-green.svg) ![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)

<p align="center">
  <img src="assets/screenshots/gameplay.png" alt="Gameplay Screenshot" width="600"/>
</p>

## ✨ What's New

### Version 2.0 Features
- 🎨 **Complete Animation System**: Smooth card dealing, flipping, and collection animations with configurable easing
- 📱 **Responsive Design**: UI automatically adapts to different window sizes and screen resolutions
- ⚡ **Performance Optimizations**: Improved rendering efficiency and memory management
- 🎯 **Enhanced Strategy Hints**: More accurate basic strategy recommendations with visual highlighting
- 📊 **Extended Statistics**: Track double downs, splits, and other advanced gameplay metrics

## 🎮 Features

### Core Gameplay
- **Complete 52-card deck** with proper shuffling and no card repetition
- **Authentic blackjack rules** including proper hand value calculation
- **Smart dealer AI** that follows standard casino rules (hits on 16, stands on 17)
- **Ace handling** with automatic high/low value adjustment
- **Bust detection** and win/loss conditions
- **Double Down** - Double your bet and receive exactly one more card
- **Split Pairs** - Split identical cards into two separate hands with individual bets

### Visual & Interactive Elements
- **High-quality card graphics** with realistic card designs
- **Advanced animation system** with smooth card dealing, flips, and movement effects
- **Responsive layout design** that adapts to different window sizes and resolutions
- **Animated chip stacks** with subtle bounce effects
- **Card shadows and borders** for enhanced visual appeal
- **Hidden dealer card** during player's turn for authentic gameplay
- **Intuitive button controls** for hit, stand, and betting
- **Optional strategy hints** showing recommended moves based on basic strategy

### Betting System
- **Starting bankroll** of $500
- **Adjustable betting** in $25 increments
- **Chip management** with win/loss tracking
- **Bankruptcy protection** - game ends when chips run out
- **Double Down support** - Double your bet after seeing initial cards
- **Split Pairs support** - Split identical cards into two separate hands

### Statistics
- **In-game statistics panel** showing wins, losses, pushes, busts, and chips won/lost
- **Press `E`** to export statistics to `stats.txt` and `stats.json`

## 🚀 Getting Started

### System Requirements
- **Python**: 3.7+ (developed and tested on 3.11+)
- **Pygame**: Latest version (automatically handles dependencies)
- **Operating System**: Windows, macOS, or Linux
- **Memory**: Minimal requirements (< 50MB RAM)
- **Display**: 800x600 minimum resolution

### Dependencies

This project requires the following dependencies:
- **pygame**: The primary game development library (version 2.5.0 or higher recommended)
- **typing-extensions**: For enhanced type annotations (Python 3.8-3.10 only)

All other functionality uses Python standard library modules:
- `sys`, `os`, `math`, `json`, `random`, `enum`, `dataclasses`, `typing`

We recommend installing dependencies via pip:
```bash
pip install pygame>=2.5.0 typing-extensions
```

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/NathanGr33n/blackjack_pygame.git
   cd blackjack_pygame
   ```

2. Install Pygame:
   ```bash
   pip install pygame
   ```

3. Run the game:
   ```bash
   python main.py
   ```

### Quick Start (One Command)
For a quick setup on most systems:
```bash
git clone https://github.com/NathanGr33n/blackjack_pygame.git && cd blackjack_pygame && pip install pygame>=2.5.0 typing-extensions && python main.py
```

## 🎯 How to Play

### Game Rules
1. **Adjust your bet** using the + and - buttons (minimum $25)
2. **Click "Start"** to deal the cards
3. **Hit** to draw another card or **Stand** to keep your current hand
4. **Toggle `Hint`** to display or hide a basic strategy recommendation
5. **Try to get as close to 21** as possible without going over
6. **Dealer plays automatically** after you stand
7. **Win conditions:**
   - Beat the dealer's hand without busting
   - Dealer busts while you don't
   - Get exactly 21 (Blackjack!)

### 🎮 Controls

**Mouse Controls:**
- **Left Click**: Interact with buttons (Hit, Stand, Double, Split, Start/Restart, Bet +/-)
- **+ Button**: Increase bet by $25
- **- Button**: Decrease bet by $25
- **Hit Button**: Draw another card
- **Stand Button**: Keep current hand and let dealer play
- **Double Button**: Double your bet and receive exactly one more card
- **Split Button**: Split a pair into two separate hands (when available)
- **Start/Restart Button**: Begin new round or restart after game over

**Keyboard Shortcuts:**
- **E**: Export statistics to `stats.txt` and `stats.json` files
- **ESC**: Reset animations if they get stuck (debug feature)
- **F11**: Toggle fullscreen mode (if supported by system)
- **R**: Quick restart of current game

## 🏗️ Project Structure

```
blackjack_pygame/
│
├── main.py                # Game class and main launcher
├── deck.py                # Card and Deck classes
├── basic_strategy.py      # Basic blackjack strategy recommendations
├── layout.py              # Responsive layout management system
├── animation_manager.py   # High-level animation coordination
├── animations.py          # Core animation system and utilities
├── animation_config.py    # Animation configuration settings
├── card_animations.py     # Card-specific animation implementations
├── test_animations.py     # Animation system test cases
├── test_responsive.py     # Responsive layout test cases
├── README.md              # This file
├── .gitignore             # Git ignore file
│
└── assets/
    ├── cards/png/         # Individual card images (52 cards + back)
    └── chips/             # Chip graphics for betting
```

## 🛠️ Technical Details

### Architecture & Code Organization
- **Object-Oriented Design**: Clean separation with `Card`, `Deck`, and central `Game` classes that handle deck management, player and dealer hands, chip tracking, and UI elements
- **MVC Pattern**: Clear separation of game logic, rendering, and user input
- **Modular Structure**: Separate files for core gameplay (`main.py`) and card logic (`deck.py`)
- **Strategy System**: Optional basic strategy hints with `basic_strategy.py` module

### Graphics & Rendering
- **Pygame Engine**: Hardware-accelerated 2D graphics
- **Custom Drawing Functions**: Card borders, shadows, and visual effects
- **Responsive Layout System**: Dynamic UI positioning based on window size
- **Image Scaling**: Adaptive resizing for consistent display across resolutions
- **Advanced Animation Framework**: 
  - Configurable easing functions (ease-in, ease-out, bounce, etc.)
  - Card dealing, flipping, and collection animations
  - Animation sequencing and callback support
  - Performance-optimized rendering
- **Chip Stack Animation**: Sine wave-based bouncing effects
- **Interactive UI Elements**: Button highlighting and visual feedback

### Game Logic Implementation
- **Authentic Blackjack Rules**: Standard casino rules with proper hand evaluation
- **Intelligent Ace Handling**: Automatic high/low value adjustment (11 → 1)
- **Dealer AI**: Follows standard casino rules (hit on ≤16, stand on ≥17)
- **Deck Management**: Proper shuffling, no card repetition until deck reset
- **State Transitions**: Clean round management and betting phases
- **Strategy Hints**: Optional basic strategy recommendations

### Data Management
- **Statistics Tracking**: Real-time win/loss/push/bust counters
- **Export Functionality**: JSON and TXT format statistics export
- **Game State Persistence**: Maintains chip count between rounds
- **Error Handling**: Graceful handling of missing assets and edge cases

### Performance Features
- **Efficient Rendering**: Only updates necessary screen regions
- **Memory Management**: Minimal RAM usage (< 50MB)
- **Cross-Platform**: Compatible with Windows, macOS, and Linux

## 🔧 Troubleshooting

### Common Issues

**"No module named 'pygame'" or other dependency errors**
```bash
pip install --upgrade pip
pip install pygame>=2.5.0 typing-extensions
```

**"Error loading PNG"**
- Ensure the `assets/` folder is in the same directory as `main.py`
- Verify all card images are present in `assets/cards/png/`
- Check that PNG files have proper permissions

**Game runs slowly or choppy**
- Update your graphics drivers
- Close other graphics-intensive applications
- Try running on a different display if using multiple monitors
- Adjust window size to a smaller resolution
- Consider disabling animations if performance is an issue

**Window resizing issues**
- If UI elements appear misaligned after resizing, try restarting the game
- Ensure window size is at least 640x480 pixels

**Animation glitches**
- If animations get stuck, press ESC to reset them
- Try restarting the game if animations behave unexpectedly

**Statistics not exporting**
- Check write permissions in the game directory
- Ensure the game directory is not read-only

### System-Specific Notes

**macOS**: You may need to install pygame using:
```bash
python3 -m pip install pygame
python3 main.py
```

**Linux**: Install required dependencies:
```bash
sudo apt-get install python3-pygame
# or
pip3 install pygame
```

## 🎨 Assets

### Card Graphics
Card graphics sourced from: [hayeah/playing-cards-assets](https://github.com/hayeah/playing-cards-assets)
- High-resolution PNG format (optimized for crisp display)
- Complete 52-card deck plus card back design
- Consistent styling and proportions

### Custom Graphics
- **Chip graphics**: Custom designed for this project with authentic casino styling
- **UI elements**: Buttons, borders, and visual effects created specifically for the game
- **Shadows and highlights**: Dynamic visual effects for enhanced gameplay experience

### Asset Requirements
To run the game, ensure all assets are present in the correct directory structure:
```
assets/
├── cards/png/           # 53 PNG files (52 cards + back.png)
│   ├── 2_of_hearts.png
│   ├── 3_of_hearts.png
│   ├── ...
│   └── back.png
└── chips/               # Chip graphics
    └── chip_25.png
```

## 📝 License

This project is open source and available under the MIT License.

```
MIT License

Copyright (c) 2025 NathanGr33n

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## 🤝 Contributing

Contributions are welcome! Whether you're fixing bugs, adding features, or improving documentation, your help is appreciated.

### How to Contribute

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes**: Implement your feature or bug fix
4. **Test your changes**: Ensure the game still works correctly
5. **Commit your changes**: `git commit -m 'Add amazing feature'`
6. **Push to the branch**: `git push origin feature/amazing-feature`
7. **Open a Pull Request**

### Development Guidelines

- **Code Style**: Follow existing code formatting and naming conventions
- **Comments**: Add clear comments for complex logic
- **Testing**: Test your changes thoroughly before submitting
- **Documentation**: Update README if you add new features or change functionality

### Ideas for Contributions

- **New Features**: Insurance bets, multiple deck support, side bets
- **UI Improvements**: Sound effects, themes, card design variants
- **Code Quality**: Unit tests, improved error handling, type annotations
- **Performance**: Optimization for lower-end systems, animation pooling
- **Documentation**: API documentation, tutorials, translations
- **Configuration**: Settings menu, game rule customization
- **Accessibility**: Keyboard controls, colorblind mode, screen reader support
- **Packaging**: Build scripts for executable creation, installer
- **Bug Reports**: Found an issue? Open an issue with detailed steps to reproduce

### Reporting Issues

When reporting bugs, please include:
- **Python version** (`python --version`)
- **Pygame version** (`pip show pygame`)
- **Operating system**
- **Steps to reproduce the issue**
- **Expected vs actual behavior**
- **Screenshots** (if applicable)

## 🎲 Future Enhancements

- [x] **Double down functionality** - ✅ Completed! Double your bet and receive one card
- [x] **Split pairs option** - ✅ Completed! Split matching cards into two hands
- [x] **Responsive layout design** - ✅ Completed! UI adapts to different window sizes
- [x] **Card animations** - ✅ Completed! Smooth dealing and movement effects
- [x] **Statistics tracking** - ✅ Completed! Comprehensive game statistics
- [x] **Basic strategy hint system** - ✅ Completed! Optimal play recommendations
- [ ] **Insurance bets** - Side bet when dealer shows an Ace
- [ ] **Multiple betting denominations** - Different chip values ($5, $10, $50, $100)
- [ ] **Sound effects and music** - Audio feedback and background music
- [ ] **Multiple deck options** - Single deck, 4-deck, 6-deck, 8-deck games
- [ ] **Tournament mode** - Compete against AI players or time limits
- [ ] **Settings menu** - Customize game rules, animations, and display options
- [ ] **Save/load functionality** - Resume games in progress
- [ ] **Advanced statistics** - Detailed analysis of gameplay patterns and decisions
- [ ] **Multiplayer support** - Local hot-seat play
- [ ] **Mobile-friendly design** - Touch controls and optimized layout

---

## 🙏 Acknowledgments

- **Card Graphics**: Thanks to [hayeah](https://github.com/hayeah) for the beautiful playing card assets
- **Pygame Community**: For excellent documentation and community support
- **Basic Strategy**: Based on mathematical analysis by Edward Thorp and other blackjack experts
- **Contributors**: Thanks to all contributors who have helped improve this project

## 🔗 Related Projects

- [Pygame Documentation](https://www.pygame.org/docs/): Official Pygame documentation
- [Python.org](https://www.python.org/): Python programming language
- [Blackjack Strategy](https://en.wikipedia.org/wiki/Blackjack_basic_strategy): Mathematical foundation for optimal play

## 📈 Project Stats

![GitHub stars](https://img.shields.io/github/stars/NathanGr33n/blackjack_pygame)
![GitHub forks](https://img.shields.io/github/forks/NathanGr33n/blackjack_pygame)
![GitHub issues](https://img.shields.io/github/issues/NathanGr33n/blackjack_pygame)
![GitHub pull requests](https://img.shields.io/github/issues-pr/NathanGr33n/blackjack_pygame)
![Code size](https://img.shields.io/github/languages/code-size/NathanGr33n/blackjack_pygame)
![Last commit](https://img.shields.io/github/last-commit/NathanGr33n/blackjack_pygame)

---

<p align="center">
  <strong>Enjoy playing Blackjack! 🎲</strong><br>
  <em>Made with ❤️ by NathanGr33n</em>
</p>
