# hangman.py

A traditional connect four of connect 4 game game.\
aka. Four Up, Plot Four, Find Four, Four in a Row, Four in a Line, Drop Four, and Gravitrips (in Soviet Union)

```
+---+---+---+---+---+---+---+
|   |   |   |   |   |   |   |
+---+---+---+---+---+---+---+
|   |   |   |   |   |   |   |
+---+---+---+---+---+---+---+
|   |   |   |   |   |   |   |
+---+---+---+---+---+---+---+
|   |   |   |   |   |   | O |
+---+---+---+---+---+---+---+
|   |   |   |   |   |   | X |
+---+---+---+---+---+---+---+
|   |   | X |   | O | O | X |
+---+---+---+---+---+---+---+
  1   2   3   4   5   6   7
```
Note: Does have colour in game (not in Windows)

## What?

Play a single or two player connect 4/connect four game.

You can use a custom dthe puzzle size and connect length\
Connect 5 anyone?

```bash
usage: connect_four.py [-h] [-s] [-x  WIDTH] [-y HEIGHT] [-c {3,4,5,6,7,8,9,10,11,12,13,14,15}] [-r] [--debug] [--self]

Connect Four
aka. Four Up, Plot Four, Find Four, Four in a Row, Four in a Line, Drop Four, and Gravitrips (in Soviet Union)

optional arguments:
    -h, --help
            show this help message and exit
    -s, --single-player
            Play against the computer
    -x  WIDTH, --width WIDTH
            Custom width of the board, use zero for maximum width
            Default: 7
    -y HEIGHT, --height HEIGHT
            Custom height of the board, use zero for maximum height
            Default: 6
    -c {3,4,5,6,7,8,9,10,11,12,13,14,15}, --length {3,4,5,6,7,8,9,10,11,12,13,14,15}
            Connect length, how many must link to win
            Default: 4
    -r, --how-to-play
            See how to play
    --debug
            Debug the program
            Default: False
    --self  Let the computer run on its own
            Default: False
```

## Why?
Great question.

## Improvements?
Improve the ```

```
## State?
I saw in one test that it did not find the win.  The only unique thing I can say I saw was the board was full but that doesn't explain it.
