# Minesweeper

A classic Minesweeper game implemented in Python using Pygame.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Gameplay](#gameplay)

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/clement-marty/minesweeper.git
    cd minesweeper
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv env
    source env/bin/activate  # On Windows use `env\Scripts\activate`
    ```

3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

Run the game using the following command:
```sh
python main.py
```

## Configuration

You can configure the game settings by editing the `config.ini` file:
```ini
[grid]
width=20
height=15

[renderer]
cell_size=32
frames_per_second=32

[game]
mine_count=25
```

- `width` and `height` define the size of the grid.
- `cell_size` defines the size of each cell in pixels.
- `frames_per_second` defines the game's frame rate.
- `mine_count` defines the number of mines in the grid.

## Gameplay

- Left-click to discover a cell.
- Right-click to flag or unflag a cell.
- The game ends when all mines are flagged or all non-mine cells are discovered.
