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
        result = opponent.board.receive_attack(row, col, self, opponent)

        self.previous_result = result
        self.previous_shot = (row, col)

        if "Hit" in result:
            self.tracking_board[row][col] = 'X'  # Mark hit
        elif "Miss" in result:
            self.tracking_board[row][col] = 'O'  # Mark miss
        else:
            print("Invalid AI input. Try again.")

        return f"AI targeted ({index_to_letter(col)}, {row + 1}) | RESULT = {result}"
    
    def _get_shot_coord(self, opponent):
        """ Internal function to calculate coord that AI will fire at
        """
        # Depending on the AI difficulty
        match self.difficulty:
            # If it's difficulty 1 (easy)
            case 1:
                # Calls easy shot function
                return self._easy_shot()
            # If it's difficulty 2 (medium)
            case 2:
                # Calls medium shot function
                return self._medium_shot()
            # If it's difficulty 3 (hard)
            case 3:
                # Calls hard shot function
                return self._hard_shot(opponent)
            case _:
                # If it's not any of those numbers, that's bad, we should error
                raise ValueError(f"AIPlayer._get_shot_coord(): Invalid difficulty int {self.difficulty}")
            

    def _easy_shot(self):
        """Internal function for calculating shot if difficulty is "easy" (or 1)
        """
        # Gets a random row and column by selecting a number between 0 and 9
        row = random.choice(range(0,GRID_SIZE)) # Gets Row
        col = random.choice(range(0,GRID_SIZE)) # Gets Column

        # Until we end up with a coord that hasn't been fired at, keep generating new coords
        while self.tracking_board[row][col] != "~":
            row = random.choice(range(0,GRID_SIZE)) # Gets Row
            col = random.choice(range(0,GRID_SIZE)) # Gets Column

        # Return the final result
        return row, col



    def _medium_shot(self):
        """Internal function for calculating shot if difficulty is "medium" (or 2)
        """

        # If the last result was a hit, records the previous shot a "hit" that didn't sink
        if self.previous_result == "Hit!": 
            # Appends it to the tracking list
            self.non_sunk_hits.append(self.previous_shot)
        # If the last result resulted in a sunk ship...
        elif self.previous_result == "Hit! Ship sunk!":
            # Reset the known hits that aren't sunk
            self.non_sunk_hits = []

        # If we're not currently aware of any hits we've had that aren't sunk
        if len(self.non_sunk_hits) == 0:
            # If we don't know of any hits, we just do a random shot (AKA easy AI)
            return self._easy_shot()
        
        # If we have exactly one hit, we need to figure out direction
        if len(self.non_sunk_hits) == 1:
            # List to represent the four coords on the sides of the hit we know of
            possible_coords = [(self.non_sunk_hits[0][0]-1, self.non_sunk_hits[0][1]), (self.non_sunk_hits[0][0], self.non_sunk_hits[0][1]-1), (self.non_sunk_hits[0][0]+1, self.non_sunk_hits[0][1]), (self.non_sunk_hits[0][0], self.non_sunk_hits[0][1]+1)]
            # For each possible coord:
            for coord in possible_coords:
                # If the coord is within the 10x10
                if check_coord_valid(coord[0], coord[1]):
                    # If the spot has not been shot at already (as detected below)
                    if self.tracking_board[coord[0]][coord[1]] == "~":
                        # Return that coord as the shot
                        return coord[0], coord[1]

                        # If this was a hit, it will be marked as such at the beginning of the next call

        # If we've gotten here, there's been more than 1 hits that we know of and we know the direction we think we want to shoot

        # Calculate the difference between the first hit, and the most recent hit of the ship we're dealing with
        # Row
        row_dif = self.non_sunk_hits[-1][0] - self.non_sunk_hits[0][0]
        # Column
        col_dif = self.non_sunk_hits[-1][1] - self.non_sunk_hits[0][1]
        
        # If there's a difference in the row, then it is a vertical ship
        if row_dif != 0:
            # If we hit last time, and the next coord in the same direction is a valid shot
            if self.previous_result == "Hit!" and check_coord_valid(self.previous_shot[0]+(row_dif//abs(row_dif)), self.previous_shot[1]):
                # Then we return the previous coord, but with 1 added in the direction of the direction we're going
                return self.previous_shot[0]+(row_dif//abs(row_dif)), self.previous_shot[1]
            # Otherwise, if our last shot was a miss, then we must go the opposite way from the original point as it is likely our first shot was in the middle of a ship
            else:
                # If that coord is valid, then we can return it
                if check_coord_valid(self.non_sunk_hits[0][0]+((row_dif//abs(row_dif))*-1), self.non_sunk_hits[0][1]):
                    # Return the next coord in the opposite direction
                    return self.non_sunk_hits[0][0]+((row_dif//abs(row_dif))*-1), self.non_sunk_hits[0][1]
        
        # If there's a difference in the column, then it is a horizontal ship
        if col_dif != 0:
            # If we hit last time, and the next coord in the same direction is a valid shot
            if self.previous_result == "Hit!" and check_coord_valid(self.previous_shot[0], self.previous_shot[1]+(col_dif//abs(col_dif))):
                # Then we return the previous coord, but with 1 added in the direction of the direction we're going
                return self.previous_shot[0], self.previous_shot[1]+(col_dif//abs(col_dif))
            # Otherwise, if our last shot was a miss, then we must go the opposite way from the original point as it is likely our first shot was in the middle of a ship
            else:
                # If that coord is valid, then we can return it
                if check_coord_valid(self.non_sunk_hits[0][0], self.non_sunk_hits[0][1]+((col_dif//abs(col_dif))*-1)):
                    # Return the next coord in the opposite direction (hence multiplying by -1)
                    return self.non_sunk_hits[0][0], self.non_sunk_hits[0][1]+((col_dif//abs(col_dif))*-1)
        
        # If we get through all of that, and there's no valid coords, then we must have hit multiple ships, so we should check the other directions

        # Same code as above, finding the coords in all 4 cardinal direction
        possible_coords = [(self.non_sunk_hits[0][0]-1, self.non_sunk_hits[0][1]), (self.non_sunk_hits[0][0], self.non_sunk_hits[0][1]-1), (self.non_sunk_hits[0][0]+1, self.non_sunk_hits[0][1]), (self.non_sunk_hits[0][0], self.non_sunk_hits[0][1]+1)]
        
        # Goes through each direction
        for coord in possible_coords:
            # If that's in the 10x10
            if check_coord_valid(coord[0], coord[1]):
                # And the position has not been shot at
                if self.tracking_board[coord[0]][coord[1]] == "~":
                    # Return that coord
                    return coord[0], coord[1]
        
        # If all else fails, shoot randomly

        return self._easy_shot()

        

    def _hard_shot(self, opponent):
        """Internal function for calculating shot if difficulty is "hard" (or 3)
        """
        # Access opponents board
        opponent_board = opponent.board
        # Iterate through all rows and columns
        rows = range(GRID_SIZE)
        cols = range(GRID_SIZE)        
        for row in rows:
            for col in cols:
                # If there's a ship, return those coordinates (it will then be "hit" and not a "S" next time)
                if opponent_board.grid[row][col] == 'S':
                    return(row, col)
