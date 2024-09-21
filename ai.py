"""
Authors: Michael Stang, Chase Horner
Date: 09-20-2024
Assignment: EECS 581 Project 2
Description: A class for an AI player with multiple difficulty modes
Inputs: Difficulty
Output: AI player moves
Collaborators/Other Sources: NONE
"""

import time
import random

from player import Player

from utils import *

class AIPlayer(Player):
    def __init__(self, name, difficulty):
        """ AIPlayer has one extra member variable (so far), and that's its difficulty level
        """
        # Initiate the AIPlayer, which inherits Player
        self.difficulty = difficulty # 0 = easy, 1 = medium, 2 = hard
        super().__init__(name)

    def take_turn(self, opponent):
        """Same variable used in Player, but overridden to automate coord selection
        """
        row, col = self._get_shot_coord(opponent)
        result = opponent.board.receive_attack(row, col)
        print(f"AI targeted ({index_to_letter(col)}, {row + 1}) | RESULT = {result}")
        time.sleep(1.5)
        if "Hit" in result:
            self.tracking_board[row][col] = 'X'  # Mark hit
        elif "Miss" in result:
            self.tracking_board[row][col] = 'O'  # Mark miss
        else:
            print("Invalid AI input. Try again.")
    
    def _get_shot_coord(self, opponent):
        """ Internal function to calculate coord that AI will fire at
        """
        match self.difficulty:
            case 1:
                return self._easy_shot()
            case 2:
                return self._medium_shot()
            case 3:
                return self._hard_shot(opponent)
            case _:
                raise ValueError(f"AIPlayer._get_shot_coord(): Invalid difficulty int {self.difficulty}")
            

    def _easy_shot(self):
        """Internal function for calculating shot if difficulty is "easy" (or 1)
        """
        row = random.choice(range(0,10))
        col = random.choice(range(0,10))
        while self.tracking_board[row][col] != "~":
            row = random.choice(range(0,10))
            col = random.choice(range(0,10))

        return row, col



    def _medium_shot(self):
        """Internal function for calculating shot if difficulty is "medium" (or 2)
        """
        pass

    def _hard_shot(self, opponent):
        """Internal function for calculating shot if difficulty is "hard" (or 3)
        """
        opponent_board = opponent.board
        rows = range(10)
        cols = range(10)        
        for row in rows:
            for col in cols:
                if opponent_board.grid[row][col] == 'S':
                    return(row, col)
