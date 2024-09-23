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
        self.non_sunk_hits = []
        self.previous_shot = set()
        self.previous_result = None
        super().__init__(name)

    def take_turn(self, opponent):
        """Same variable used in Player, but overridden to automate coord selection
        """
        row, col = self._get_shot_coord(opponent)
        result = opponent.board.receive_attack(row, col)

        self.previous_result = result
        self.previous_shot = (row, col)

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

        if self.previous_result == "Hit!":
            self.non_sunk_hits.append(self.previous_shot)
        elif self.previous_result == "Hit! Ship sunk!":
            self.non_sunk_hits = []

        # If we're not currently aware of any hits we've had that aren't sunk
        if len(self.non_sunk_hits) == 0:
            return self._easy_shot()
        
        # If we have exactly one hit, we need to figure out direction
        if len(self.non_sunk_hits) == 1:
            possible_coords = [(self.non_sunk_hits[0][0]-1, self.non_sunk_hits[0][1]), (self.non_sunk_hits[0][0], self.non_sunk_hits[0][1]-1), (self.non_sunk_hits[0][0]+1, self.non_sunk_hits[0][1]), (self.non_sunk_hits[0][0], self.non_sunk_hits[0][1]+1)]
            for coord in possible_coords:
                if check_coord_valid(coord[0], coord[1]):
                    if self.tracking_board[coord[0]][coord[1]] == "~":
                        return coord[0], coord[1]

        row_dif = self.non_sunk_hits[-1][0] - self.non_sunk_hits[0][0]
        col_dif = self.non_sunk_hits[-1][1] - self.non_sunk_hits[0][1]
        
        if row_dif != 0:
            if self.previous_result == "Hit!" and check_coord_valid(self.previous_shot[0]+(row_dif//abs(row_dif)), self.previous_shot[1]):
                return self.previous_shot[0]+(row_dif//abs(row_dif)), self.previous_shot[1]
            else:
                if check_coord_valid(self.non_sunk_hits[0][0]+((row_dif//abs(row_dif))*-1), self.non_sunk_hits[0][1]):
                    return self.non_sunk_hits[0][0]+((row_dif//abs(row_dif))*-1), self.non_sunk_hits[0][1]
        if col_dif != 0:
            if self.previous_result == "Hit!" and check_coord_valid(self.previous_shot[0], self.previous_shot[1]+(col_dif//abs(col_dif))):
                return self.previous_shot[0], self.previous_shot[1]+(col_dif//abs(col_dif))
            else:
                if check_coord_valid(self.non_sunk_hits[0][0], self.non_sunk_hits[0][1]+((col_dif//abs(col_dif))*-1)):
                    return self.non_sunk_hits[0][0], self.non_sunk_hits[0][1]+((col_dif//abs(col_dif))*-1)
        
        possible_coords = [(self.non_sunk_hits[0][0]-1, self.non_sunk_hits[0][1]), (self.non_sunk_hits[0][0], self.non_sunk_hits[0][1]-1), (self.non_sunk_hits[0][0]+1, self.non_sunk_hits[0][1]), (self.non_sunk_hits[0][0], self.non_sunk_hits[0][1]+1)]
        for coord in possible_coords:
            if check_coord_valid(coord[0], coord[1]):
                if self.tracking_board[coord[0]][coord[1]] == "~":
                    return coord[0], coord[1]

        

    def _hard_shot(self, opponent):
        """Internal function for calculating shot if difficulty is "hard" (or 3)
        """
        #access opponents board
        opponent_board = opponent.board
        #iterate through all rows and columns
        rows = range(10)
        cols = range(10)        
        for row in rows:
            for col in cols:
                #If there's a ship, return those coordinates (it will then be "hit" and not a "S" next time)
                if opponent_board.grid[row][col] == 'S':
                    return(row, col)
