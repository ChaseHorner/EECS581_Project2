"""
Author: Pierce Lane
Date: 09-24-2024
Assignment: EECS 581 Project 2
Description: A class for powerups
Collaborators/Other Sources: NONE
"""

# Ship class to manage individual ship's state
class Powerup:
    def __init__(self, variety):
        """
        Constructor for Powerup class.
        variety is the letter that will display in the board
        """
        self.variety = variety
        self.coordinates = [] 
        self.hit = False

