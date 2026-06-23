import tkinter as tk 


class BaseDialog(tk.Toplevel):
    """
    Base class for all toolbar dialogs.
    """
    def __init__(self, root, title):
        super().__init__(root)
        self.title(title)
        self.resizable(False, False)
        self.grab_set()  # make modal
        self.build()
        self._center()

    def build(self):
        """
        MUST be imprmented for subclasses.
        """
        raise NotImplementedError("Dialogs must implement build()")

    def _center(self):
        """
        Position the dialog in the centre of the screen.
        """
        self.update_idletasks()
        w = self.winfo_width()
        h = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (w // 2)
        y = (self.winfo_screenheight() // 2) - (h // 2)
        self.geometry(f"{w}x{h}+{x}+{y}")

    def close(self):
        self.destroy()


class HowToDialog(BaseDialog):
    """
    Displays a brief summary of Wordle rules.
    """
    RULES = [
        "Guess the WORDLE in 6 tries.",
        "",
        "Each guess must be a valid 5-letter word.",
        "Press ENTER to submit your guess.",
        "Press BACKSPACE to delete a letter.",
        "",
        "After each guess, the colour of the tiles",
        "will change to show how close your guess was.",
        "",
        "  Green  — correct letter, correct spot",
        "  Yellow — correct letter, wrong spot",
        "  Grey   — letter is not in the word",
        "",
        "A new game starts automatically after each round.",
    ]

    def __init__(self, root):
        super().__init__(root, "How To Play")

    def build(self):
        frame = tk.Frame(self, padx=28, pady=20)
        frame.pack()

        title = tk.Label(frame, text="HOW TO PLAY", font=("Courier", 16, "bold"))
        title.pack(pady=(0, 12))

        separator = tk.Frame(frame, height=1, bg="#cccccc")
        separator.pack(fill=tk.X, pady=(0, 12))

        for line in self.RULES:
            lbl = tk.Label(frame, text=line, font=("Courier", 12), anchor="w", justify="left")
            lbl.pack(fill=tk.X)

        self._build_colour_examples(frame)

        tk.Button(
            frame,
            text="Got it!",
            font=("Courier", 12, "bold"),
            width=10,
            command=self.close,
        ).pack(pady=(20, 0))

    def _build_colour_examples(self, parent):
        """
        Render three coloured tile examples illustrating green/yellow/grey.
        """
        examples = [
            ("W", "green",      "Correct letter, correct spot"),
            ("O", "yellow",     "Correct letter, wrong spot"),
            ("R", "light grey",    "Letter not in the word"),
        ]

        frame = tk.Frame(parent, pady=10)
        frame.pack(fill=tk.X)

        for letter, colour, description in examples:
            row = tk.Frame(frame)
            row.pack(anchor="w", pady=3)

            tile = tk.Canvas(row, width=36, height=36, highlightthickness=0)
            tile.pack(side=tk.LEFT, padx=(0, 10))
            tile.create_rectangle(2, 2, 34, 34, fill=colour, outline="")
            tile.create_text(18, 18, text=letter, font=("Courier", 16, "bold"), fill="black")

            tk.Label(row, text=description, font=("Courier", 12), anchor="w").pack(side=tk.LEFT)


class StatisticsDialog(BaseDialog):
    """
    Displays the running game statistics.
    """
    _BAR_COLOR = "#333333"
    _MAX_WIDTH = 200

    def __init__(self, root, stats):
        self._stats = stats
        super().__init__(root, "Statistics")

    def build(self):
        frame = tk.Frame(self, padx=28, pady=20)
        frame.pack()

        tk.Label(frame, text="STATISTICS", font=("Courier", 16, "bold")).pack(pady=(0, 12))
        self._build_summary(frame)

        tk.Frame(frame, height=1, bg="#cccccc").pack(fill=tk.X, pady=(16, 12))
        tk.Label(frame, text="GUESS DISTRIBUTION", font=("Courier", 12, "bold")).pack(pady=(0, 8))
        self._build_distribution(frame)

        tk.Button(
            frame,
            text="Close",
            font=("Courier", 12, "bold"),
            width=10,
            command=self.close,
        ).pack(pady=(20, 0))

    def _build_summary(self, parent):
        """
        Render the played/win/lost summary.
        """
        summary = [
            ("Played", self._stats.gamesPlayed()),
            ("Win %",  self._stats.winPercentage()),
            ("Lost",   self._stats.gamesLost()),
        ]
        row = tk.Frame(parent)
        row.pack()
        for label, value in summary:
            cell = tk.Frame(row, padx=14)
            cell.pack(side=tk.LEFT)
            tk.Label(cell, text=str(value), font=("Courier", 20, "bold")).pack()
            tk.Label(cell, text=label, font=("Courier", 10), fg="#555555").pack()

    def _build_distribution(self, parent):
        """
        Render one labelled bar per guess count.
        """
        distribution = self._stats.guessDistribution()
        max_val = max(distribution.values()) if any(distribution.values()) else 1

        for guesses, count in distribution.items():
            row = tk.Frame(parent)
            row.pack(fill=tk.X, pady=2)

            tk.Label(row, text=str(guesses), font=("Courier", 12, "bold"), width=2, anchor="e").pack(side=tk.LEFT, padx=(0, 8))

            bar_w = max(4, int(self._MAX_WIDTH * count / max_val)) if count > 0 else 4
            bar = tk.Canvas(row, width=self._MAX_WIDTH + 30, height=22, highlightthickness=0)
            bar.pack(side=tk.LEFT)
            bar.create_rectangle(0, 1, bar_w, 21, fill=self._BAR_COLOR, outline="")
            bar.create_text(bar_w + 6, 11, text=str(count), font=("Courier", 11), anchor="w")
