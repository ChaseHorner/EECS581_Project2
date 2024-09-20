GRID_SIZE = 10
COLUMN_LETTERS = 'ABCDEFGHIJ'
MAX_SHIPS = 5

def letter_to_index(letter):
    return COLUMN_LETTERS.index(letter.upper())

def print_grid(grid):
    print("  " + " ".join(COLUMN_LETTERS))  # Print column headers
    for i, row in enumerate(grid):
        print(f"{i+1:2} " + " ".join(row))