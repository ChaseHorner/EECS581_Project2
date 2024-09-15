import time
import os

# Constants
GRID_SIZE = 10
COLUMN_LETTERS = 'ABCDEFGHIJ'
MAX_SHIPS = 5

# Helper functions to convert coordinates
def letter_to_index(letter):
    return COLUMN_LETTERS.index(letter.upper())

def print_grid(grid):
    print("  " + " ".join(COLUMN_LETTERS))  # Print column headers
    for i, row in enumerate(grid):
        print(f"{i+1:2} " + " ".join(row))

# Ship class to manage individual ship's state
class Ship:
    def __init__(self, size):
        self.size = size
        self.hits = 0
        self.coordinates = [] 

    def is_sunk(self):
        return self.hits >= self.size

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

# Main game loop
def play_game():
    print("Welcome to Battleship!")
    player1 = Player("Player 1")
    player2 = Player("Player 2")

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

    # Ship placement phase
    for player in [player1, player2]:
        if player.name == "Player 2":
            os.system('clear')
            print("Switching to Player 2's turn...")
            time.sleep(2)
            while True:
                key = input("Player 2, press Enter to continue...")
                if key ==  "":
                    break
                else:
                    print("Invalid input. Please press Enter to continue...")

        print(f"{player.name}, place your ships!")
        for size in range(1, num_ships + 1):
            ship = Ship(size)
            while True:
                try:
                    start = input(f"Enter starting position for ship of size {size} (Letters: A-J Numbers: 1-10): ")
                    orientation = input("Enter orientation (H for horizontal, V for vertical): ").upper()
                    while True:
                        if orientation not in ['H', 'V']:
                            orientation = input("Invalid input. Enter H for horizontal or V for vertical: ").upper()
                        else:
                            break
                    col = letter_to_index(start[0])
                    row = int(start[1:]) - 1

                    if player.board.place_ship(ship, row, col, orientation):
                        print(f"{player.name}'s board after placing ship of size {size}:")
                        print_grid(player.board.grid)  # Print the board after each placement
                        time.sleep(2)
                        break
                    else:
                        print("Invalid ship placement. Try again.")
                except (ValueError, IndexError):
                    print("Invalid input. Try again.")

    # Game loop
    while True:
        time.sleep(1)
        os.system('clear')
        player1.display_tboards()
        player1.take_turn(player2)
        if player2.board.all_ships_sunk():
            print(player1.display_tboards())
            print(f"{player1.name} wins!")

            break

        player2.display_tboards()
        player2.take_turn(player1)
        if player1.board.all_ships_sunk():
            print(player2.display_tboards())
            print(f"{player2.name} wins!")
            break

if __name__ == "__main__":
    play_game()
