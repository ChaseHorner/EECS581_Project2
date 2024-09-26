"""
Authors: Michael Stang, Zain W Ghosheh, Abdulahi Mohamed, Olufewa Alonge, Mahgoub Husien
Date: 09-20-2024
Assignment: EECS 581 Project 2
Description: A class for representing the board
Inputs: 
Output:
Collaborators/Other Sources: NONE
"""

from utils import *

# Board class to handle ship placement and attacks
class Board:
    def __init__(self):
        self.grid = [['~' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.ships = []
        self.powerups = []

    def place_ship(self, ship, start_row, start_col, orientation):
        """
        This method allows for a ship to be placed on a board object. 
        It accepts a ship object, two ints, and a string H or V respectively
        """
        coordinates = []
        for i in range(ship.size):  # Validates placement for horizontal placement
            if orientation == 'H':
                col = start_col + i
                if col >= GRID_SIZE or self.grid[start_row][col] != '~':
                    return False
                coordinates.append((start_row, col))
            elif orientation == 'V':    # Validates placemtn for vertical placement
                row = start_row + i
                if row >= GRID_SIZE or self.grid[row][start_col] != '~':
                    return False
                coordinates.append((row, start_col))

        # Place ship after validation
        for row, col in coordinates:
            self.grid[row][col] = 'S'
        ship.coordinates = coordinates
        self.ships.append(ship)
        return True

    def place_powerup(self, powerup, row, col):
        """
        Places a powerup object at row, col
        """
        # Validate coordinates given
        if self.grid[row][col] != '~':
            return False

        # Place powerup after validation
        self.grid[row][col] = powerup.variety
        powerup.coordinates = [row, col]
        self.powerups.append(powerup)
        return True

    def receive_attack(self, row, col, us, opponent):
        """This method allows for a ship on a board to be attacked"""

        # define what letters we can hit
        hit_letters = ['S']
        for powerup in self.powerups:
            hit_letters.append(powerup.variety)

        # if we hit one
        if self.grid[row][col] in hit_letters:
            # mark it as such
            self.grid[row][col] = 'X'  # Hit

            # check for a ship hit
            for ship in self.ships:
                if (row, col) in ship.coordinates:
                    ship.hits += 1
                    if ship.is_sunk():
                        return "Hit! Ship sunk!"
                    return "Hit!"
            
            # check for a powerup hit
            for powerup in self.powerups:
                if [row, col] == powerup.coordinates:
                    # do the powerup
                    result = powerup.do_power(row, col, us, opponent)
                    powerup.hit = True
                    # return that we hit! (an_char is "" or "n")
                    return result

        # if we hit a water tile, we've missed
        elif self.grid[row][col] == '~':
            self.grid[row][col] = 'O'  # Miss
            return "Miss!\n"

        return "Already attacked this spot."
    
    def all_ships_sunk(self):
        return all(ship.is_sunk() for ship in self.ships)
    
