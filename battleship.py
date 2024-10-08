"""
Authors: Holden Vail, Michael Stang, Chase Horner, Zain W Ghosheh, Abdulahi Mohamed, Olufewa Alonge, Mahgoub Husien.
Date: 09-11-2024
Assignment: EECS 581 Project 2
Description: Builds the game battleship which can be played on the terminal with all the required functionality.
Inputs: none
Output: Battleship game.
Collaborators/Other Sources:
"""


import time
import os

from player import Player
from ai import AIPlayer
from board import Board
from ship import Ship
from powerups import *

from utils import *

# Main game loop
def play_game():
    os.system('clear')
    print("Welcome to Battleship!")
    player1 = Player("Player 1")

    # Let Player 1 choose the number of players
    while True:
        try:
            num_players = int(input("Choose the number of players (1 or 2): "))
            if 1 <= num_players <= 2:
                break
            else:
                print(f"Invalid input. Please choose between 1 and 2.")
        except ValueError:
            print("Please enter a number between 1 and 2.")
    
    # Let Player 1 choose the number of ships (between 1 and 5)
    while True:
        try:
            num_ships = int(input("Choose the number of ships (1-5): "))
            if 1 <= num_ships <= MAX_SHIPS:
                break
            else:
                print(f"Invalid input. Please choose between 1 and {MAX_SHIPS}.")
        except ValueError:
            print("Please enter a number between 1 and 5.")

    # If applicable, let Player 1 choose the difficulty of AI to play against
    if num_players == 1: 
        while True:
            try:
                difficulty = int(input("Choose the difficulty:\nEasy = 1, Medium = 2, Hard = 3: "))
                if 1 <= difficulty <= 3:
                    break
                else:
                    print(f"Invalid input. Please choose between 1 and 3.")
            except ValueError:
                print("Please enter a number between 1 and 3.")
        player2 = AIPlayer("AI", difficulty)
    else:
        player2 = Player("Player 2")

    
    # Ask if they want to play with powerups
    while True:
        do_powerups = input("Play with powerups enabled (y/n)?: ").lower()
        if do_powerups in ("y", "n"):
            break
        else:
            print("Please enter y or n")

    do_powerups = do_powerups == "y"

    # Ship placement phase
    for player in [player1, player2]:
        if player.name == "AI":
            player.random_placement(num_ships)  # Place ships randomly for AI
        else:
            if player.name == "Player 2":
                os.system('clear')
                print("Switching to Player 2's turn...")

            print(f"{player.name}, place your ships!")
            placement = input(f"Random or Manual ship placement (R or M): ").upper()    # Allows Player 1 to place ships randomly
            while True:
                if placement not in ['R', 'M']:
                    placement = input("Invalid input. Enter R for random or M for manual: ").upper()
                else:
                    break
            if placement == 'R':
                player.random_placement(num_ships)
            # Begin manual ship placement 
            else:
                for size in range(1, num_ships + 1):
                    ship = Ship(size)
                    while True:
                        try:
                            start = input(f"Enter starting position for ship of size {size} (Letters: A-J Numbers: 1-10): ")
                            if size != 1:    
                                orientation = input("Enter orientation (H for horizontal, V for vertical): ").upper()
                                while True:
                                    if orientation not in ['H', 'V']:
                                        orientation = input("Invalid input. Enter H for horizontal or V for vertical: ").upper()
                                    else:
                                        break
                            else:
                                orientation = 'H'
                            col = letter_to_index(start[0])
                            row = int(start[1:]) - 1

                            if player.board.place_ship(ship, row, col, orientation):
                                print(f"{player.name}'s board after placing ship of size {size}:")
                                print_grid(player.board.grid)  # Print the board after each placement
                                time.sleep(1)
                                break
                            else:
                                print("Invalid ship placement. Try again.")
                        except (ValueError, IndexError):
                            print("Invalid input. Try again.")

    # Powerup placement if applicable
    if do_powerups:
        for player in [player1, player2]:
            # Define the powerups to be used
            powerups = [AirStrike(), DoubleShot(), Bomb()]
            # Place them randomly
            player.place_powerups(powerups)

    # Game loop
    result = None
    while True:
        # Transition to player 1
        os.system('clear')
        if result: # If first loop, don't print player 2's nonexistant result
            print(result)
        input("Player 1 press enter...")
        os.system('clear')

        # Player 1's turn
        if not isinstance(player1, AIPlayer):
            player1.display_boards()
            player1.display_tboards()
        result = player1.take_turn(player2)

        # Check if that turn ended the game
        if player2.board.all_ships_sunk():
            os.system('clear')
            player1.display_boards()
            player1.display_tboards()
            print(f"{player1.name} wins!")
            break

        # Transition to player 2
        os.system('clear')
        print(result)
        input("Player 2 press enter...")
        os.system('clear')

        # Player 2's turn
        if not isinstance(player2, AIPlayer):
            player2.display_boards()
            player2.display_tboards()
        result = player2.take_turn(player1)

        # Check if that turn ended the game
        if player1.board.all_ships_sunk():
            os.system('clear')
            player2.display_boards()
            player2.display_tboards()
            print(f"{player2.name} wins!")
            break

if __name__ == "__main__":
    play_game()
