from conf import ALPHABET, SCORE_COLORS


class Keyboard:
    """
    The on-screen alphabet keyboard drawn at the bottom of the board.
    """
    _ROWS = [0, 1]
    _COLS = 13

    def __init__(self, canvas):
        self.canvas = canvas
        self.letters = ALPHABET["letters"]
        self.backgrounds = []
        self.labels = []

    def draw(self):
        x0, y0, ts = ALPHABET["x_offset"], ALPHABET["y_offset"], ALPHABET["tile_size"]
        for row in self._ROWS:
            for col in range(self._COLS):
                self.backgrounds.append(self.canvas.create_rectangle(
                    x0 + ts*col,
                    y0 + ts*row,
                    x0 + ts*col + ts,
                    y0 + ts*row + ts,
                    outline=ALPHABET["outline"],
                ))
                self.labels.append(self.canvas.create_text(
                    x0 + ts*col + ts//2,
                    y0 + ts*row + ts//2,
                    text=self.letters[row*self._COLS + col],
                    font=ALPHABET["font"],
                ))

    def clear(self):
        for row in self._ROWS:
            for col in range(self._COLS):
                self.canvas.delete(self.backgrounds[col + self._COLS*row])
                self.canvas.delete(self.labels[col + self._COLS*row])
        self.backgrounds = []
        self.labels = []

    def update(self, wordBank):
        """
        Recolour each letter tile to match its status.
        """
        for i in range(len(self.letters)):
            color = wordBank.get(self.letters[i].lower())
            if color in SCORE_COLORS:
                self.canvas.itemconfig(self.backgrounds[i], fill=SCORE_COLORS[color])
