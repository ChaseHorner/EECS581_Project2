"""
Authors: Michael Stang, Zain W Ghosheh, Abdulahi Mohamed, Olufewa Alonge, Mahgoub Husien
Date: 09-20-2024
Assignment: EECS 581 Project 2
Description: A class for representing the board
Inputs: 
Output:
Collaborators/Other Sources: NONE
"""

GRID_SIZE = 10
COLUMN_LETTERS = 'ABCDEFGHIJ'
MAX_SHIPS = 5

# Board class to handle ship placement and attacks
class Board:
    def __init__(self):
        self.grid = [['~' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.ships = []

    def place_ship(self, ship, start_row, start_col, orientation):
        coordinates = []
        for i in range(ship.size):
            if orientation == 'H':
                col = start_col + i
                if col >= GRID_SIZE or self.grid[start_row][col] != '~':
                    return False
                coordinates.append((start_row, col))
            elif orientation == 'V':
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

    def receive_attack(self, row, col):
        if self.grid[row][col] == 'S':
            self.grid[row][col] = 'X'  # Hit
            for ship in self.ships:
                if (row, col) in ship.coordinates:
                    ship.hits += 1
                    if ship.is_sunk():
                        return "Hit! Ship sunk!"
                    return "Hit!"
        elif self.grid[row][col] == '~':
            self.grid[row][col] = 'O'  # Miss
            return "Miss!\n"
        return "Already attacked this spot."

    def all_ships_sunk(self):
        return all(ship.is_sunk() for ship in self.ships)