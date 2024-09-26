"""
Author: Pierce Lane
Date: 09-24-2024
Assignment: EECS 581 Project 2
Description: A few classes for powerups
Collaborators/Other Sources: NONE
"""

import os
from time import sleep
# Import abstract base classes
from abc import ABC, abstractmethod

# grab our utils
from utils import *


# need this to prevent printing when they hit a powerup
from ai import AIPlayer

# Powerup interface
class Powerup(ABC):

    # define delay lengths for all powerups
    long_delay = 1.5
    delay = .2

    # Abstract methods, need to be implemented in concrete subclasses
    @abstractmethod
    def __init__(self):
        self.coordinates = []
        self.hit = False
        # variety and name to be implemented in subclasses
        self.variety = None
        self.name = None

        # funny case - when printing "Hit a {name} Powerup!", Air Strikes have a grammatical
        # error (Hit a Air Strike Powerup!) -- to fix this, print an_char after "a"
        self.an_char = ""

    @abstractmethod
    def do_power(self, row, col, us, opponent):
        """
        ABSTRACT
        Does the power of the powerup at (row, col)
        """
        pass

    def print_hitme(self, us):
        """
        CONCRETE
        Helper function to print to whoever hit us that we've been hit!
        """

        # make sure we're not an AI
        if not isinstance(us, AIPlayer):
            # print out the thing and wait a sec
            print(f"You hit a{self.an_char} {self.name} Powerup!!")
            # just regular sleep, don't need to check if we're not an AI rn
            sleep(Powerup.long_delay)

    def init_do_power(self, row, col, us):
        """
        CONCRETE
        Helper function to run at the start of do_power
        """
        # error case, we should never be hit twice
        if self.hit:
            raise NameError("Powerup hit twice")

        # update trackign board with our original hit
        us.check_result("Hit", row, col)

        # print that we hit (conditional on if we're an AIPlayer)
        self.print_hitme(us)

        # print our boards now that they've been updated
        self.print_boards(us)


    def print_boards(self, us):
        """
        CONCRETE
        Helper function to print our boards if we're not an AI player
        """
        if not isinstance(us, AIPlayer):
            os.system('clear')
            us.display_boards()
            us.display_tboards()

    def sleep_if_not_ai(self, delay, us):
        """
        CONCRETE
        Helper function to sleep only if we're not an AIPlayer
        """
        if not isinstance(us, AIPlayer):
            sleep(delay)


class AirStrike(Powerup):
    def __init__(self):
        # run super constructor
        super().__init__()
        # set variety to 'A' for air strike
        self.variety = 'A'
        self.name = "Air Strike"

        # need to be gramatically correct!!
        self.an_char = "n"

    def do_power(self, row, col, us, opponent):
        """
        Hits the entire row and column of the powerup
        """
        # run common prefix code
        super().init_do_power(row, col, us)

        # run through the cols
        for col_iter in range(GRID_SIZE):
            # shoot with constant row
            result = opponent.board.receive_attack(row, col_iter, opponent, us)

            # update our tracking board accordingly
            us.check_result(result, row, col_iter)

            # print the boards if us is not an AIPlayer
            self.print_boards(us)

            # pause for dramatic effect
            self.sleep_if_not_ai(Powerup.delay, us)

        # run through rows
        for row_iter in range(GRID_SIZE):
            # shoot with constant col
            result = opponent.board.receive_attack(row_iter, col, opponent, us)

            # update our tracking board accordingly
            us.check_result(result, row_iter, col)

            # print the boards
            self.print_boards(us)

            # pause for dramatic effect
            self.sleep_if_not_ai(Powerup.delay, us)

        
        self.sleep_if_not_ai(Powerup.long_delay, us)

        return f"Hit a{self.an_char} {self.name} Powerup!"

class DoubleShot(Powerup):
    def __init__(self):
        # run super constructor
        super().__init__()
        # set variety to 'D' for double shot
        self.variety = 'D'
        self.name = "Double Shot"

    def do_power(self, row, col, us, opponent):
        """
        Gives the player that shot it another turn
        """
        # run common prefix code
        super().init_do_power(row, col, us)

        # define blank prepend result for AI players so we can display whether
        # they hit a double shot or not
        result = ""
        if isinstance(us, AIPlayer):
            result = f"Hit a{self.an_char} {self.name} Powerup!\n"
        
        # I mean just take another turn and return its result string
        return result + us.take_turn(opponent)

class Bomb(Powerup):
    def __init__(self):
        # run super constructor
        super().__init__()
        # set variety to 'B' for bomb
        self.variety = 'B'
        self.name = "Bomb"

    def do_power(self, row, col, us, opponent):
        """
        Hits a 3x3 area around the powerup
        """
        # run common prefix code
        super().init_do_power(row, col, us)

        # define bomb_size
            # the intention is to make this be a user-configurable value later
        bomb_size = 5
        if bomb_size % 2 == 0:
            bomb_size += 1

        # Loop through an NxN with (row, col) at the center
        for i in range(-(bomb_size//2), bomb_size//2 + 1):
            for j in range(-(bomb_size//2), bomb_size//2 + 1):
                # make sure we're in bounds
                if 0 <= row + i < GRID_SIZE and 0 <= col + j < GRID_SIZE:
                    # hit the spot on the board
                    result = opponent.board.receive_attack(row + i, col + j, opponent, us)

                    # check the result and print it accordingly
                    us.check_result(result, row + i, col + j)

                    # print the boards
                    self.print_boards(us)
                    # pause for dramatic effect
                    self.sleep_if_not_ai(Powerup.delay, us)

        # sleep for effect again
        self.sleep_if_not_ai(Powerup.long_delay, us)
        return f"Hit a{self.an_char} {self.name} Powerup!"

