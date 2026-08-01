# Tic Tac Toe

A classic Tic Tac Toe game built with Python and Pygame. Play against a friend in two-player mode, or test your skills against a smart (but beatable) AI opponent.

## Features

- Two game modes
  - **Player vs Player** — take turns on the same machine
  - **Player vs AI** — you play as **X**, the computer plays as **O**
- Smart but beatable AI — it wins when it can, blocks your winning moves, takes the center when free, and otherwise plays randomly. A short 500 ms "thinking" delay makes its moves feel natural.
- Win & draw detection — rows, columns, and both diagonals are checked automatically
- Winning-line highlight — a green line strikes through the three winning squares when a game ends
- Play Again button — start a fresh round without leaving the screen
- Main Menu button — return to the mode select screen at any time

## Requirements

- Python 3.8+
- [Pygame](https://www.pygame.org/) 2.x

## Installation

1. Clone or download this repository.
2. Install the dependency:

   ```bash
   pip install pygame
   ```

   (Or on some systems: `pip3 install pygame`)

## Running the Game

From the project directory:

```bash
python main.py
```

(Or `python3 main.py` on macOS/Linux if `python` points to Python 2.)

A 720x720 window opens showing the main menu.

## How to Play

1. On the main menu, click **Player vs Player** or **Player vs AI**.
2. Click any empty square on the 3x3 grid to place your mark:
   - **Player vs Player**: players alternate as **X** and **O**.
   - **Player vs AI**: you are always **X** and go first; the AI responds as **O**.
3. The first player to line up three marks — horizontally, vertically, or diagonally — wins.
4. If all nine squares fill with no winner, the game is a draw.

## Project Structure

```
.
├── main.py      # Entry point: the Game class, window setup, and main loop
├── states.py    # Game states: Menu, PVP, and PVAI (with the AI logic)
└── README.md    # This file
```

### Code Overview

- **`main.py`** — Creates the 720x720 window, builds the state machine (`menu`, `pvp`, `pvai`), and runs the main loop that handles events, updates state, and draws the screen at 60 FPS.
- **`states.py`** — Contains three state classes:
  - `Menu` — the mode-select screen with the two buttons.
  - `PVP` — two-player gameplay: board state, click handling, win/draw detection, and drawing.
  - `PVAI` — extends `PVP` and adds the computer opponent's move logic (`find_move` and `ai_move`).
