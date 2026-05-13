# Genius Star Project
## Overview
Genius Star is a replayable, competitive, 2-person physical puzzle game. 
https://www.smartgames.eu/uk/one-player-games/genius-star.
The game starts by rolling 7 dices that dictate where starting obstacles are placed on the board. The board is star shaped and made up of 48 triangles. There are then 12 pieces of 11 unique shapes that each player will try to add into board such that all spaces are filled. The game is a competition to see which of the two players can fill their board fastest.

## Local Development
The virtual environment used to run the games locally can be enabled via:
source /Users/notchjohnson/Mouseion/Mouseion/GeniusStar/.venv/bin/activate

## Development & Tasks
** Game Movement **
- Pieces are drawn in id order, we should display picked-up pieces first, if they exist

** Game Mechanics **
- Game should identify when it has been successfully solved

** Game UI **
- Create Start Screen. Display Dice Rolls.
- Introduce help option for piece movement

** Code Improvements **
- Abstract Board class to inherit Piece class
- Refactor the Piece Placement Check Logic

** Fastest Solver **
- Implement First Iteration of Fastest Solver

** Exhaustive Solver **
- Convert to use new board structure, and OOP.
- Setup Parrallel Processes to improve speed. 

