"""
Authors: Michael Stang, Zain W Ghosheh, Abdulahi Mohamed, Olufewa Alonge, Mahgoub Husien
Date: 09-20-2024
Assignment: EECS 581 Project 2
Description: A class for each ship
Collaborators/Other Sources: NONE
"""

# Ship class to manage individual ship's state
class Ship:
    def __init__(self, size):
        self.size = size
        self.hits = 0
        self.coordinates = [] 

    def is_sunk(self):
        return self.hits >= self.size
