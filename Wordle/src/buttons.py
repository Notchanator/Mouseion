import tkinter as tk
from toolbar import ToolbarButton
from dialogs import HowToDialog, StatisticsDialog


class HowToButton(ToolbarButton):
    """
    Circular '?' button that opens the How To Play dialog.
    Rendered as a small canvas oval so it appears as a true circle.
    """
    _CIRCLE_SIZE   = 32
    _CIRCLE_COLOR  = "#333333"
    _CIRCLE_HOVER  = "#555555"
    _LABEL_COLOR   = "white"

    def build(self, parent):
        self.canvas = tk.Canvas(
            parent,
            width=self._CIRCLE_SIZE,
            height=self._CIRCLE_SIZE,
            highlightthickness=0,
        )
        self.canvas.pack(side=tk.LEFT, padx=10, pady=9)

        self._oval = self.canvas.create_oval(
            2, 2, self._CIRCLE_SIZE - 2, self._CIRCLE_SIZE - 2,
            fill=self._CIRCLE_COLOR, outline="",
        )
        self._label = self.canvas.create_text(
            self._CIRCLE_SIZE // 2, self._CIRCLE_SIZE // 2,
            text="?", fill=self._LABEL_COLOR, font=("Courier", 15, "bold"),
        )

        self.canvas.bind("<Button-1>",  lambda e: self.on_click())
        self.canvas.bind("<Enter>",     lambda e: self._hover(True))
        self.canvas.bind("<Leave>",     lambda e: self._hover(False))

    def _hover(self, entering):
        colour = self._CIRCLE_HOVER if entering else self._CIRCLE_COLOR
        self.canvas.itemconfig(self._oval, fill=colour)

    def on_click(self):
        HowToDialog(self.toolbar.root)


class StatisticsButton(ToolbarButton):
    """
    Circular medal button that opens the Statistics dialog.
    Sits on the right side of the toolbar.
    """
    _CIRCLE_SIZE  = 32
    _CIRCLE_COLOR = "#333333"
    _CIRCLE_HOVER = "#555555"
    _LABEL_COLOR  = "white"

    def build(self, parent):
        self.canvas = tk.Canvas(
            parent,
            width=self._CIRCLE_SIZE,
            height=self._CIRCLE_SIZE,
            highlightthickness=0,
        )
        self.canvas.pack(side=tk.RIGHT, padx=10, pady=9)

        self._oval = self.canvas.create_oval(
            2, 2, self._CIRCLE_SIZE - 2, self._CIRCLE_SIZE - 2,
            fill=self._CIRCLE_COLOR, outline="",
        )
        self._label = self.canvas.create_text(
            self._CIRCLE_SIZE // 2, self._CIRCLE_SIZE // 2,
            text="🏅", fill=self._LABEL_COLOR, font=("Courier", 13),
        )

        self.canvas.bind("<Button-1>", lambda e: self.on_click())
        self.canvas.bind("<Enter>",    lambda e: self._hover(True))
        self.canvas.bind("<Leave>",    lambda e: self._hover(False))

    def _hover(self, entering):
        colour = self._CIRCLE_HOVER if entering else self._CIRCLE_COLOR
        self.canvas.itemconfig(self._oval, fill=colour)

    def on_click(self):
        StatisticsDialog(self.toolbar.root, self.app.stats)
