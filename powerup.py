"""
Author: Pierce Lane
Date: 09-24-2024
Assignment: EECS 581 Project 2
Description: A class for powerups
Collaborators/Other Sources: NONE
"""

# Import abstract base classes
from abc import ABC, abstractmethod


from globals import *
import os
from time import sleep

# need AIPlayer to prevent printing when they hit a powerup
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
        Function to print to whoever hit us that we've been hit!
        """

        # make sure we're not an AI
        if not isinstance(us, AIPlayer):
            # print out the thing and wait a sec
            print(f"You hit a{self.an_char} {self.name} Powerup!!")
            sleep(Powerup.long_delay)


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
        # error case, we should never be hit twice
        if self.hit:
            # using NameError because ValueError is caught later
            raise NameError("Powerup hit twice")

        # update tracking board with our original hit
        us.check_result("Hit", row, col)

        # tell the user what's going on before we do the animation (conditional on AIPlayer)
        self.print_hitme(us)

        # run through the cols
        for col_iter in range(GRID_SIZE):
            # skip over col_iter == col to avoid double shooting
            if col_iter == col:
                continue

            # shoot with constant row
            result = opponent.board.receive_attack(row, col_iter, opponent, us)

            # clear the screen
            if not isinstance(us, AIPlayer): # this "not isinstance" junk could be a variable
                os.system('clear')
            
            # update our tracking board accordingly
            us.check_result(result, row, col_iter)

            # print the boards if us is not an AIPlayer
            if not isinstance(us, AIPlayer):
                us.display_boards()
                us.display_tboards()

            # pause for dramatic effect
            sleep(Powerup.delay)

        # run through rows
        for row_iter in range(GRID_SIZE):
            # skip over row_iter == row to avoid double shooting
            if row_iter == row:
                continue

            # shoot with constant col
            result = opponent.board.receive_attack(row_iter, col, opponent, us)

            # clear the screen
            if not isinstance(us, AIPlayer):
                os.system('clear')
            
            # update our tracking board accordingly
            us.check_result(result, row_iter, col)

            # print the boards
            us.display_boards()
            us.display_tboards()

            # pause for dramatic effect
            sleep(Powerup.delay)

        sleep(Powerup.long_delay)


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
        pass

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
        
        # error case, we should never be hit twice
        if self.hit:
            raise NameError("Powerup hit twice")

        # update tracking board with our original hit
        us.check_result("Hit", row, col)

        # print that we hit (conditional on if we're an AIPlayer)
        self.print_hitme(us)

        # Loop through a 3x3 with (row, col) at the center
        for i in range(-1, 2):
            for j in range(-1, 2):
                # make sure we're in bounds
                if 0 <= row + i < GRID_SIZE and 0 <= col + j < GRID_SIZE:
                    # hit the spot on the board
                    result = opponent.board.receive_attack(row + i, col + j, opponent, us)

                    # check the result and print it accordingly
                    us.check_result(result, row + i, col + j)
                    if not isinstance(us, AIPlayer):
                        os.system('clear')
                        us.display_boards()
                        us.display_tboards()
                        sleep(Powerup.delay)
