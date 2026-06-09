import tkinter as tk
from conf import TOOLBAR


class ToolbarButton:
    """
    Abstract base class for all toolbar buttons.

    Subclasses must implement:
      - build(parent)  — construct and pack the button widget(s) into the toolbar frame
      - on_click()     — define what happens when the button is activated
    """
    def __init__(self, toolbar):
        self.toolbar = toolbar
        self.build(toolbar.frame)

    @property
    def app(self):
        """Live reference to the game App, read through the toolbar.

        The toolbar owns the App reference and may have it assigned after
        buttons are registered, so buttons must read it lazily rather than
        capturing it at construction time.
        """
        return self.toolbar.app

    def build(self, parent):
        raise NotImplementedError("Toolbar buttons must implement build()")

    def on_click(self):
        raise NotImplementedError("Toolbar buttons must implement on_click()")


class Toolbar:
    """
    Horizontal toolbar frame that sits above the game canvas.

    Buttons are added via register(), which instantiates the given
    ToolbarButton subclass and appends it to the internal button list.
    """
    def __init__(self, root, app):
        self.root = root
        self.app = app
        self.buttons = []

        self.frame = tk.Frame(root, height=TOOLBAR["height"])
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        self.title = tk.Label(
            self.frame,
            text="WORDLE",
            font=TOOLBAR["font"]
        )
        self.title.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    def register(self, button_class):
        """Instantiate a ToolbarButton subclass and add it to the toolbar."""
        button = button_class(self)
        self.buttons.append(button)
        return button
