"""
Authors: Michael Stang, Zain W Ghosheh, Abdulahi Mohamed, Olufewa Alonge, Mahgoub Husien
Date: 09-20-2024
Assignment: EECS 581 Project 2
Description: A class for each player
Inputs: 
Output:
Collaborators/Other Sources: NONE
"""

from board import Board
import time

from utils import *

GRID_SIZE = 10
COLUMN_LETTERS = 'ABCDEFGHIJ'
MAX_SHIPS = 5

# Player class to manage player turns
class Player:
    def __init__(self, name):
        self.name = name
        self.board = Board()
        self.tracking_board = [['~' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

    def take_turn(self, opponent):
        while True:
            try:
                time.sleep(1)
                target = input(f"{self.name}, enter target (e.g. A1): ")
                col = letter_to_index(target[0])
                row = int(target[1:]) - 1

                if 0 <= col < GRID_SIZE and 0 <= row < GRID_SIZE:
                    result = opponent.board.receive_attack(row, col)
                    print(result)  # Announce hit or miss
                    if result == "Already attacked this spot.":
                        print("Try again.")
                        continue  # Allow the player to take another turn
                    elif "Hit" in result:
                        self.tracking_board[row][col] = 'X'  # Mark hit
                    elif "Miss" in result:
                        self.tracking_board[row][col] = 'O'  # Mark miss
                    break
                else:
                    print("Invalid input. Try again.")
            except (ValueError, IndexError):
                print("Invalid input. Please enter a valid coordinate (e.g., A1).")

    def display_tboards(self):
        print(f"{self.name}'s Tracking Board:")
        print_grid(self.tracking_board)

    def display_boards(self):
        print(f"{self.name}'s Board:")
        print_grid(self.board.grid)