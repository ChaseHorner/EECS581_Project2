# global variable definitions
GRID_SIZE = 10
COLUMN_LETTERS = 'ABCDEFGHIJ'
MAX_SHIPS = 5

def letter_to_index(letter):
    return COLUMN_LETTERS.index(letter.upper())

def index_to_letter(num):
    return chr(num + ord("A"))

def print_grid(grid):
    print("   " + " ".join(COLUMN_LETTERS))  # Print column headers
    for i, row in enumerate(grid):
        print(f"{i+1:2} " + " ".join(row))

def check_coord_valid(row, col):
    """Checks if a given coord is within the 10x10"""
    # Checks the if the rows and columns are all between (0-9) [inclusive]
    return (row >= 0 and row <= 9) and (col >= 0 and col <= 9)
