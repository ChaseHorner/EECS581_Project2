"""
Authors: Holden Vail, Michael Stang, Chase Horner, Zain W Ghosheh, Abdulahi Mohamed, Olufewa Alonge, Mahgoub Husien
Date: 09-20-2024
Assignment: EECS 581 Project 2
Description: A class for each player
Inputs: 
Output:
Collaborators/Other Sources: NONE
"""

from board import Board
from ship import Ship
import time
import random

from utils import *

from globals import *

# Player class to manage player turns
class Player:
    def __init__(self, name):
        self.name = name
        self.board = Board()
        self.tracking_board = [['~' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

    def take_turn(self, opponent):
        """This method implements the game logic for a player to take their turn"""
        ret = ""
        while True:
            try:
                target = input(f"{self.name}, enter target (e.g. A1): ")
                col = letter_to_index(target[0])
                row = int(target[1:]) - 1

                if 0 <= col < GRID_SIZE and 0 <= row < GRID_SIZE:
                    result = opponent.board.receive_attack(row, col, opponent, self)
                    ret = result
                    if result == "Already attacked this spot.":
                        print(result)
                        print("Try again.")
                        continue  # Allow the player to take another turn
                    
                    # update our tracking board accordingly
                    self.check_result(result, row, col)

                    break
                else:
                    print("Invalid input. Try again.")
            except (ValueError, IndexError):
                print("Invalid input. Please enter a valid coordinate (e.g., A1).")

        return ret

    def display_tboards(self):
        print(f"{self.name}'s Tracking Board:")
        print_grid(self.tracking_board)


    def display_boards(self):
        print(f"{self.name}'s Board:")
        print_grid(self.board.grid)


    def random_placement(self, num_ships):
        """This function is used to randomly place any number of ships on the board"""
        for i in range(num_ships):
            success = False
            while success == False:     # Try placing ships until is a guaranteed placement. Could be problematic for larger num_ships
                ship = Ship(i + 1)
                row = random.randint(0, GRID_SIZE -1)       # Randomly chooses ways to place the ship
                col = random.randint(0, GRID_SIZE - 1)
                orientation = random.choice(["H", "V"])
                success = self.board.place_ship(ship, row, col, orientation)    # Attemps placement

    def place_powerups(self, powerup_list):
        """Will place the powerups given randomly and safely on the board"""
        for powerup in powerup_list:
            success = False
            # Place powerups randomly until it sticks
            while success == False:
                # Choose some coordinates
                row = random.randint(0, GRID_SIZE - 1)
                col = random.randint(0, GRID_SIZE - 1)
                # Try placing the powerup there
                success = self.board.place_powerup(powerup, row, col)
            
    def check_result(self, result, row, col):
        """
        Helper method to check results of shots
        """
        if "Hit" in result:
            self.tracking_board[row][col] = 'X'  # Mark hit
        elif "Miss" in result:
            self.tracking_board[row][col] = 'O'  # Mark miss
        # silently fail on everything else

