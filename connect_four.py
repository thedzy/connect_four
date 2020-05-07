#!/usr/bin/env python3

"""
Script:	connect_four.py
Date:	2020-04-30

Platform: MacOS/Window/Linux

Description:
Connect Four or Connect 4
aka. Four Up, Plot Four, Find Four, Four in a Row, Four in a Line, Drop Four, and Gravitrips (in Soviet Union)'
"""

__author__ = 'thedzy'
__copyright__ = 'Copyright 2020, thedzy'
__license__ = 'GPL'
__version__ = '1.0'
__maintainer__ = 'thedzy'
__email__ = 'thedzy@hotmail.com'
__status__ = 'Developer'

import argparse
import os
import random


def main():
    # Set puzzle size
    if options.width == 0 or options.height == 0:
        terminal_width, terminal_height = os.get_terminal_size()

    if options.width == 0:
        options.width = int(terminal_width / 4)

    if options.height == 0:
        options.height = int(terminal_height / 2) - 4

    width = options.width
    height = options.height

    if options.length > min(width, height):
        print('Length of connects can only be as long as the shortest side, '
              'settings to {}'.format(min(width, height)))
        options.length = min(width, height)

    # Create a board
    # The actual board will work left to right and top to bottom and we will reverse this in visuals
    board = []
    for _ in range(width):
        col = []
        for _ in range(height):
            col.append(0)
        board.append(col)

    # Randomise who starts
    red_turn = random.choice([True, False])

    # Reset the screen
    set_cursor()

    while True:
        # Reset the cursor each time to draw over the existing board
        set_cursor(reset=options.debug)

        # Print the board
        print_board(board)
        print(' ' * 80, end='\r')

        # Check and see if there is a winner
        winner = check_winner(board, options.length)
        if winner is not 0:
            if winner == 1:
                print('Red Wins!')
            else:
                print('Blue Wins!')

            if options.debug:
                print('Last move in column: {}{}'.format(selection, ' ' * 40))
            exit(winner)

        # Check and see that there is more moves that can be made
        if not any(0 in row for row in board):
            print('Tie Game!')
            exit()

        # Display the persons move
        if red_turn:
            print('Turn: Red')
        else:
            print('Turn: Blue')

        # Get user selection
        print(' ' * 80, end='\r')
        if options.ai and red_turn:
            selection = str(ai_move(board, options.length, (1, 2)))
        else:
            if options.self_play:
                selection = str(ai_move(board, options.length, (2, 1)))
            else:
                selection = input('Column number? ')

        if selection == 'exit':
            exit()
        if not selection.isdigit():
            print('Invalid input')
            continue

        # Make sure the selection is an integer
        selection = int(selection)

        # Make sure the column exists
        if selection > width:
            print('Column does not exist')
            continue

        # Check that there is room in the column
        if board[selection - 1].count(0) == 0:
            print('Full try again')
            continue

        # Find the first available position for the move
        for index in range(height):
            if board[selection - 1][index] == 0:
                if red_turn:
                    board[selection - 1][index] = 1
                else:
                    board[selection - 1][index] = 2
                break

        # Move turn to the other player
        red_turn = False if red_turn else True


def print_board(board):
    """
    Print the board
    :param board: (list)(list) Board board matrix
    :return: (void)
    """

    # Get the height and width of the board
    height = len(board[0])
    width = len(board)

    def print_row(items):
        """
        Print a row in the board
        :param items: (list)(int) player with piece in position
        :return: (void)
        """
        symbol = [' ', 'O', 'X']
        if os.name is 'nt':
            colour = ['', '', '']

        else:
            colour = ['\033[0;37;40m', '\033[1;30;41m', '\x1b[6;30;44m']
        row_string = ''
        for item in items:
            row_string += '{}{} {} {}'.format('|', colour[item], symbol[item], colour[0])
        row_string += '{} '.format('|')

        print(row_string)

    def print_divider(length=8):
        """
        Bring the dividers between rows
        :param length: (int) NUmber of columns
        :return: (void)
        """
        header_string = ''
        for _ in range(length):
            header_string += '+---'
        header_string += '+'

        print(header_string)

    # Create and fill a new board of opposite dimensions
    new_board = []
    for _ in range(height):
        col = []
        for _ in range(width):
            col.append(0)
        new_board.append(col)

    # Reverse the data
    for x in range(width):
        for y in range(height):
            new_board[abs(y - height + 1)][x] = board[x][y]

    board = new_board

    # Print inverted board
    for row in board:
        print_divider(width)
        print_row(row)
    print_divider(width)

    footer = ' '
    for num in range(width):
        footer += str(num + 1).center(4)
    print(footer)


def ai_move(board, length=4, player_order=(1, 2)):
    """
    Calculate the best move for the ai
    NOt the best ai, but more reasonable enough to make the game a bit of a challenge
    :param board: (list)(list) Game board matrix
    :param length: (int) length of move to start at
    :param player_range: (tuple)(int) Player, opponent
    :return: (int) Move column
    """
    desired_length = length

    def feasibility(positions, test_player=1):
        """
        Check the feasibility that there is a pattern before trying to find the move
        Essentially check that there is a pattern that could be a move
        :param positions: (list)(int) Pattern we are checking
        :param test_player: (int) Player was are testing for
        :return:
        """
        test_opposition = 2 if test_player == 1 else 1
        if positions.count(test_player) == desired_length - 1 and positions.count(test_opposition) == 0:
            if options.debug:
                print('\n', positions)
            return True
        return False

    height = len(board[0])
    width = len(board)

    # Iterate through the lengths starting from the top
    while True:
        # Check for self and opposition to block
        for player in player_order:
            # Threshold where it does make sens to try and block the opposition
            if desired_length < length and player == player_order[1]:
                continue

            # Check every position on the board for a move in the desired length
            for col in range(height):
                for row in range(width):
                    try:
                        feasible = feasibility(list(board[row + n][col + 0] for n in range(desired_length)), player)
                        if feasible:
                            n = 0
                            while True:
                                if board[row + n][col + 0] == 0:
                                    break
                                n += 1

                            if options.debug:
                                print('Direction:', '-', 'Length:', desired_length, 'Position: ', row + n, col + 0)

                            if col + 0 == 0:
                                return row + n + 1
                            elif board[row + n][col + 0 - 1] != 0:
                                return row + n + 1
                    except IndexError:
                        pass
                    try:
                        feasible = feasibility(list(board[row + 0][col + n] for n in range(desired_length)), player)
                        if feasible:
                            n = 0
                            while True:
                                if board[row + 0][col + n] == 0:
                                    break
                                n += 1

                            if options.debug:
                                print('Direction:', '|', 'Length:', desired_length, 'Position: ', row + 0, col + n)

                            if col + n == 0:
                                return row + 0 + 1
                            elif board[row + 0][col + n - 1] != 0:
                                return row + 0 + 1
                    except IndexError:
                        pass
                    try:
                        feasible = feasibility(list(board[row + n][col + n] for n in range(desired_length)), player)
                        if feasible:
                            n = 0
                            while True:
                                if board[row + n][col + n] == 0:
                                    break
                                n += 1

                            if options.debug:
                                print('Direction:', '/', 'Length:', desired_length, 'Position: ', row + n, col + n)

                            if col + n == 0:
                                return row + n + 1
                            elif board[row + n][col + n - 1] != 0:
                                return row + n + 1
                    except IndexError:
                        pass
                    try:
                        feasible = feasibility(list(board[row + n][col - n] for n in range(desired_length)), player)
                        if col - (desired_length - 1) < 0:
                            if feasible:
                                n = 0
                                while True:
                                    if board[row + n][col - n] == 0:
                                        break
                                    n += 1

                                if options.debug:
                                    print('Direction:', '\\', 'Length:', desired_length, 'Position: ', row + n, col - n)

                                if col - n == 0:
                                    return row + n + 1
                                elif board[row + n][col - n - 1] != 0:
                                    return row + n + 1
                    except IndexError:
                        pass
        desired_length -= 1
        if desired_length <= 1:
            return random.randint(0, width)


def check_winner(board, length=4):
    """
    Check if there is a winner in the board
    :param board: (list)(list) Game board matrix
    :param length: (int) The length of the connect required, ex 4
    :return: (int) Winner, 0 for None
    """

    def test(positions):
        if len(set(positions)) == 1:
            return True
        else:
            return False

    height = len(board[0])
    width = len(board)

    for col in range(height):
        for row in range(width):
            # There are only 8 paths to win, seeing as we will check from each position in the board,
            # we only need to check in 4 directions
            if board[row][col] != 0:
                try:
                    if test(list(board[row + n][col + 0] for n in range(length))):
                        return board[row][col]
                except IndexError:
                    pass
                try:
                    if test(list(board[row + 0][col + n] for n in range(length))):
                        return board[row][col]
                except IndexError:
                    pass
                try:
                    if test(list(board[row + n][col + n] for n in range(length))):
                        return board[row][col]
                except IndexError:
                    pass
                try:
                    if test(list(board[row + n][col - n] for n in range(length))):
                        if col - (length - 1) < 0:
                            # Do not allow negative integers
                            return 0
                        return board[row][col]
                except IndexError:
                    pass
    return 0


def set_cursor(y_position=0, x_position=0, reset=True):
    """
    Set the terminal/console cursor position and whether to clear the screen
    :param y_position: (int) Row
    :param x_position: (int) Column
    :param reset: (bool) Clear the screen
    :return: (void)
    """
    if os.name is not 'nt':
        # Send an ansi clear
        if reset:
            print('\033[2J')
        # Set the cursor
        print('\033[{:d};{:d}H'.format(y_position, x_position))


def how_to_play():
    """
    Game help screen
    :return: (void)
    """
    print('Connect Four is based on a Milton Bradley game.\n'
          'https://en.wikipedia.org/wiki/Connect_Four\n')
    print('At the top of the screen is the puzzle\n'
          'Example:\n'
          '+---+---+---+---+---+---+---+ \n'
          '|   |   |   |   |   |   |   | \n'
          '+---+---+---+---+---+---+---+ \n'
          '|   |   |   |   |   |   |   | \n'
          '+---+---+---+---+---+---+---+ \n'
          '|   |   |   |   |   |   |   | \n'
          '+---+---+---+---+---+---+---+ \n'
          '|   |   |   |   |   |   | O | \n'
          '+---+---+---+---+---+---+---+ \n'
          '|   |   |   |   |   |   | X | \n'
          '+---+---+---+---+---+---+---+ \n'
          '|   |   | X |   | O | O | X | \n'
          '+---+---+---+---+---+---+---+ \n'
          '  1   2   3   4   5   6   7   \n')
    print('And below is the input\n'
          'Example:\n'
          '╒═════════════════════════════════════╕\n'
          '│ Turn: Blue                          │\n'
          '│ Column number?                      │\n'
          '│                                     │\n'
          '╘═════════════════════════════════════╛')
    print('You can enter a column number where your piece will fall until the bottom or another piece.')
    print('Get 4 pieces in a diagonal or up/down arrangement to win')

    print('Type \'exit\' to quit\n')


if __name__ == '__main__':

    def parser_formatter(format_class, **kwargs):
        """
        Use a raw parser to use line breaks, etc
        :param format_class: (class) formatting class
        :param kwargs: (dict) kwargs for class
        :return: (class) formatting class
        """
        try:
            return lambda prog: format_class(prog, **kwargs)
        except TypeError:
            return format_class


    parser = argparse.ArgumentParser(
        description='Connect Four \n'
                    'aka. Four Up, Plot Four, Find Four, '
                    'Four in a Row, Four in a Line, Drop Four, and Gravitrips (in Soviet Union)',
        formatter_class=parser_formatter(argparse.RawTextHelpFormatter,
                                         indent_increment=4, max_help_position=12, width=160))

    parser.add_argument('-s', '--single-player',
                        action='store_true', dest='ai', default=False,
                        help='Play against the computer')

    # Custom width and heights
    parser.add_argument('-x ', '--width', type=int,
                        action='store', dest='width', default=7,
                        help='Custom width of the board, use zero for maximum width'
                             '\nDefault: %(default)s')
    parser.add_argument('-y', '--height', type=int,
                        action='store', dest='height', default=6,
                        help='Custom height of the board, use zero for maximum height'
                             '\nDefault: %(default)s')
    parser.add_argument('-c', '--length', type=int,
                        action='store', dest='length', default=4, choices=range(3, 16),
                        help='Connect length, how many must link to win'
                             '\nDefault: %(default)s')

    # How to play
    parser.add_argument('-r', '--how-to-play',
                        action='store_true', dest='how', default=False,
                        help='See how to play')

    # Testing and debugging
    parser.add_argument('--debug',
                        action='store_true', dest='debug', default=False,
                        help='Debug the program'
                             '\nDefault: %(default)s')
    parser.add_argument('--self',
                        action='store_true', dest='self_play', default=False,
                        help='Let the computer run on its own'
                             '\nDefault: %(default)s')

    options = parser.parse_args()

    if options.self_play:
        options.ai = True

    if options.how:
        how_to_play()
    else:
        main()
