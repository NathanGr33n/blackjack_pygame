# Blackjack Pygame

A fully-featured **Blackjack** game built with Python and Pygame, featuring beautiful card graphics, animated chip betting, and authentic casino-style gameplay. The game logic is organized around a `Game` class that manages all state and rendering.

![Blackjack Game](https://img.shields.io/badge/Python-3.11+-blue.svg) ![Pygame](https://img.shields.io/badge/Pygame-Required-green.svg)

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

### Betting System
- **Starting bankroll** of $500
- **Adjustable betting** in $25 increments
- **Chip management** with win/loss tracking
- **Bankruptcy protection** - game ends when chips run out

### Statistics
- **In-game statistics panel** showing wins, losses, pushes, busts, and chips won/lost
- **Press `E`** to export statistics to `stats.txt` and `stats.json`

## 🚀 Getting Started

### Prerequisites
- Python 3.11+ (should work with earlier versions too)
- Pygame library

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/blackjack_pygame.git
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

1. **Adjust your bet** using the + and - buttons (minimum $25)
2. **Click "Start"** to deal the cards
3. **Hit** to draw another card or **Stand** to keep your current hand
4. **Try to get as close to 21** as possible without going over
5. **Dealer plays automatically** after you stand
6. **Win conditions:**
   - Beat the dealer's hand without busting
   - Dealer busts while you don't
   - Get exactly 21 (Blackjack!)

## 🏗️ Project Structure

```
blackjack_pygame/
│
├── main.py              # Game class and minimal launcher
├── deck.py              # Card and Deck classes
├── README.md            # This file
├── .gitignore          # Git ignore file
│
└── assets/
    ├── cards/png/       # Individual card images (52 cards + back)
    └── chips/           # Chip graphics for betting
```

## 🛠️ Technical Details

- **Architecture:** Object-oriented design with separate Card, Deck, and central Game classes that handle deck management, player and dealer hands, chip tracking, and UI elements
- **Graphics:** Pygame-based rendering with custom drawing functions
- **Game Logic:** Proper blackjack mathematics with edge case handling
- **Animation:** Smooth chip stack animations using sine wave functions
- **State Management:** Clean game state handling for rounds and betting

## 🎨 Assets

Card graphics sourced from: [hayeah/playing-cards-assets](https://github.com/hayeah/playing-cards-assets)

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the issues page.

## 🎲 Future Enhancements

- [ ] Double down functionality
- [ ] Split pairs option
- [ ] Multiple betting denominations
- [ ] Sound effects and music
- [x] Statistics tracking
- [ ] Multiple deck options
