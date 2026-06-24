from pathlib import Path

_SRC_DIR = Path(__file__).parent
_DATA_DIR = _SRC_DIR.parent / "data"

# Wordle answers and guesses file paths.
DATA = {
    "answers": _DATA_DIR / "wordle_answers.csv",
    "guesses": _DATA_DIR / "wordle_guesses.csv",
}

# Solver settings
SOLVER = {
    # Fixed opening guess that is constant every game.
    # This speeds up turn 1 by not running full-dictionary entropy cost.
    "opener": "soare",
}


# Window size
WINDOW = {
    "title": "Wordle",
    "geometry": "800x760",
    "width": 800,
    "height": 760,
}

# Toolbar size
TOOLBAR = {
    "height":50,
    "font": ("Courier", 24, "bold"),
}

# Canvas size
CANVAS = {
    "width": 800,
    "height": 710,
}

# Guess tile grid
TILE = {
    "rows": 6,
    "cols": 5,
    "size": 80, 
    "step": 100,
    "x_offset": 160,
    "y_offset": 10,
    "outline": "black",
    "font": ("Courier", 64),
    "invalid_color": "red",
}

# Score colours
SCORE_COLORS = {
    2: "green",
    1: "yellow",
    0: "light grey",
}

# Alphabet keyboard
ALPHABET = {
    "letters": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"],
    "tile_size": 50,
    "x_offset": 75,
    "y_offset": 600,
    "outline": "white",
    "font": ("Courier", 16),
}

# End-game banner (winner / loser overlay)
END_BANNER = {
    "x0": 75,
    "y0": 600,
    "x1": 725,
    "y1": 700,
    "cx": 400,
    "cy": 650,
    "fill": "black",
    "text_color": "white",
    "text": ["Marvelous", "Splendid", "Fantastic", "Extraordinary", "Wonderful", "Incredbile", "Phenominal"],
    "font": ("Courier", 64),
}
