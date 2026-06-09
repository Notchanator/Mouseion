# Wordle UI Expansion — Design Document

## Overview

This document outlines the proposed architecture for adding a toolbar with interactive buttons to the Wordle Tkinter application. The goal is a scalable structure that makes it easy to add new buttons and their associated panels in the future without touching core game logic.

---

## Proposed Architecture

### High-Level Structure

```
root (tk.Tk)
├── Toolbar (tk.Frame)          ← new: lives above the canvas
│   ├── RulesButton
│   ├── KeybindsButton
│   ├── ForfeitButton
│   └── StatisticsButton
│   └── (future buttons...)
└── App (tk.Canvas)             ← unchanged: game board lives here
```

The root window stacks the `Toolbar` frame above the `App` canvas using `.grid()`, giving a clean separation between navigation UI and game UI.

---

## Class Design

### `Toolbar` (tk.Frame)

A thin container frame responsible for:
- Holding and laying out all toolbar buttons in a horizontal row
- Holding a reference to `App` so buttons can read/mutate game state when needed (e.g. Forfeit)
- Providing a registration method so new buttons can be added without modifying `Toolbar` itself

```
Toolbar
├── __init__(root, app)
├── register(button: ToolbarButton)   ← adds a button to the row
└── buttons: list[ToolbarButton]
```

---

### `ToolbarButton` (Abstract Base / tk.Button)

A base class all toolbar buttons inherit from. Standardises:
- Visual styling (font, padding, relief) so all buttons look consistent
- A required `on_click()` method each subclass implements
- Holding a reference to `app` for state access

```
ToolbarButton (tk.Button)
├── __init__(toolbar, app)
└── on_click()                        ← abstract, implemented by each subclass
```

---

### Individual Button Classes

Each button is its own class inheriting from `ToolbarButton`. Their sole responsibility is defining `on_click()`, which opens their associated dialog.

| Class | Responsibility |
|---|---|
| `RulesButton` | Opens `RulesDialog` |
| `KeybindsButton` | Opens `KeybindsDialog` |
| `ForfeitButton` | Opens `ForfeitDialog` (requires app reference to end the round) |
| `StatisticsButton` | Opens `StatisticsDialog` (reads `app.stats`) |

---

### Dialog Classes (tk.Toplevel)

Each button opens a modal `tk.Toplevel` window — a separate floating window that blocks interaction with the main window until closed. Each dialog is its own class.

```
BaseDialog (tk.Toplevel)
├── __init__(root)
├── build()           ← abstract, subclass fills in content
└── close()

RulesDialog(BaseDialog)
KeybindsDialog(BaseDialog)
ForfeitDialog(BaseDialog)      ← has confirm/cancel buttons; calls app.forfeit() on confirm
StatisticsDialog(BaseDialog)   ← receives stats dict from app and renders it
```

Using `tk.Toplevel` over drawing panels on the canvas keeps dialog content completely separate from game rendering and avoids needing to clear/redraw the board when a panel opens or closes.

---

## Data Flow

```
User clicks ForfeitButton
    → ForfeitButton.on_click()
        → ForfeitDialog(root, app) opens
            → User confirms
                → app.forfeit() called        ← dialog reaches into app for state mutation
                → dialog closes
```

Dialogs that only read state (Rules, Keybinds) need no `app` reference. Dialogs that affect game state (Forfeit) receive `app` via their constructor. Statistics reads `app.stats` but does not mutate — it can receive a snapshot of the stats dict rather than the full `app` reference.

---

## File Structure

```
src/
├── wordle.py           ← unchanged
├── playWordle.py       ← App class unchanged; Toolbar instantiated here at root level
├── toolbar.py          ← Toolbar + ToolbarButton base class
├── buttons.py          ← RulesButton, KeybindsButton, ForfeitButton, StatisticsButton
└── dialogs.py          ← BaseDialog, RulesDialog, KeybindsDialog, ForfeitDialog, StatisticsDialog
```

Splitting buttons and dialogs into their own files keeps `playWordle.py` from growing unwieldy and makes it easy to add a new button/dialog pair by touching only `buttons.py`, `dialogs.py`, and the registration call in `playWordle.py`.

---

## Adding a New Button in the Future

1. Add a new subclass to `buttons.py`
2. Add a corresponding dialog to `dialogs.py`
3. Register the button in `playWordle.py` with `toolbar.register(NewButton(toolbar, app))`

No other files need to change.

---

## What Stays the Same

- `App` (the canvas) is not modified — it remains the single owner of game state
- `Wordle` (the core logic class) is not modified
- Keybindings (`root.bind`) remain on the root and continue to work alongside the toolbar
