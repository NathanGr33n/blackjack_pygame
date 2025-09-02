# 🃏 Blackjack PyGame

A fully-featured **Blackjack** game built with Python and Pygame, featuring beautiful card graphics, animated chip betting, authentic casino-style gameplay, and comprehensive statistics tracking. The game logic is organized around a `Game` class that manages all state and rendering.

**By: NathanGr33n**

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg) ![Pygame](https://img.shields.io/badge/Pygame-Required-green.svg) ![License](https://img.shields.io/badge/License-MIT-green.svg)

## 🎮 Features

### Core Gameplay
- **Complete 52-card deck** with proper shuffling and no card repetition
- **Authentic blackjack rules** including proper hand value calculation
- **Smart dealer AI** that follows standard casino rules (hits on 16, stands on 17)
- **Ace handling** with automatic high/low value adjustment
- **Bust detection** and win/loss conditions

### Visual & Interactive Elements
- **High-quality card graphics** with realistic card designs
- **Animated chip stacks** with subtle bounce effects
- **Card shadows and borders** for enhanced visual appeal
- **Hidden dealer card** during player's turn for authentic gameplay
- **Intuitive button controls** for hit, stand, and betting
- **Optional strategy hints** showing recommended moves

### Betting System
- **Starting bankroll** of $500
- **Adjustable betting** in $25 increments
- **Chip management** with win/loss tracking
- **Bankruptcy protection** - game ends when chips run out

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

This project only requires one external dependency:
- **pygame**: The primary game development library

All other functionality uses Python standard library modules:
- `sys`, `os`, `math`, `json`, `random`

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
- **Left Click**: Interact with buttons (Hit, Stand, Start/Restart, Bet +/-)
- **+ Button**: Increase bet by $25
- **- Button**: Decrease bet by $25
- **Hit Button**: Draw another card
- **Stand Button**: Keep current hand and let dealer play
- **Start/Restart Button**: Begin new round or restart after game over

**Keyboard Shortcuts:**
- **E**: Export statistics to `stats.txt` and `stats.json` files

## 🏗️ Project Structure

```
blackjack_pygame/
│
├── main.py              # Game class and minimal launcher
├── deck.py              # Card and Deck classes
├── basic_strategy.py    # Basic blackjack strategy recommendations
├── README.md            # This file
├── .gitignore          # Git ignore file
│
└── assets/
    ├── cards/png/       # Individual card images (52 cards + back)
    └── chips/           # Chip graphics for betting
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
- **Image Scaling**: Dynamic resizing for consistent card display (80x120px)
- **Animation System**: Sine wave-based chip stack bouncing effects
- **UI Elements**: Button highlighting and interactive feedback

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

**"No module named 'pygame'"**
```bash
pip install --upgrade pip
pip install pygame
```

**"Error loading PNG"**
- Ensure the `assets/` folder is in the same directory as `main.py`
- Verify all card images are present in `assets/cards/png/`

**Game runs slowly or choppy**
- Update your graphics drivers
- Close other graphics-intensive applications
- Try running on a different display if using multiple monitors

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

Card graphics sourced from: [hayeah/playing-cards-assets](https://github.com/hayeah/playing-cards-assets)
Chip graphics: Custom designed for this project

## 📝 License

This project is open source and available under the MIT License.

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

- **New Features**: Double down, split pairs, insurance bets
- **UI Improvements**: Better animations, sound effects, themes
- **Code Quality**: Refactoring, optimization, error handling
- **Documentation**: Tutorials, code documentation, translations
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

- [ ] Double down functionality
- [ ] Split pairs option
- [ ] Multiple betting denominations
- [ ] Sound effects and music
- [x] Statistics tracking
- [x] Basic strategy hint system
- [ ] Multiple deck options
