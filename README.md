# Battleship Game

This is a Battleship game where two players face off on 10x10 boards. Each player places their fleet of ships on their board and takes turns attempting to sink their opponent's ships. The game ends when one player successfully sinks all the opponent’s ships.

## **Game Setup**

### **Board Size:**
- The board is a 10x10 grid.
- Columns are labeled A-J, rows are labeled 1-10.

### **Number of Ships:**
- Players decide on how many ships to play with (1-5).
- Each player has the same number and size of ships.

### **Ship Size:**
| Number of Ships | Ship Sizes             |
|-----------------|------------------------|
| 1 ship          | 1x1                    |
| 2 ships         | 1x1, 1x2               |
| 3 ships         | 1x1, 1x2, 1x3          |
| 4 ships         | 1x1, 1x2, 1x3, 1x4     |
| 5 ships         | 1x1, 1x2, 1x3, 1x4, 1x5|

### **Ship Placement:**
- Players secretly place their ships on the board.
- Ships can be placed either **horizontally** or **vertically**.

---

## **Gameplay**

### **Turns:**
- Players alternate turns firing shots at their opponent’s board by choosing a coordinate (e.g., B3).
- The game informs whether the shot was a "hit" or a "miss".

### **Sinking Ships:**
- When all spaces of a ship have been hit, the ship is considered sunk.

### **End Game:**
- The game ends when one player has sunk all of their opponent's ships.

---

## **Player Views**

### **Own Board:**
- Players see their own board, where ships are placed, and where their ships have been hit.

### **Opponent Board:**
- Players track their shots on their opponent’s board, showing hits and misses.

### **Icon Key:**
- ~: Water Tile
- O: Miss
- X: Hit
- S: Ship
- A: Air Strike Powerup
- D: Double Shot Powerup
- B: Bomb Powerup

---

## **How to Run the Game**

1. Clone the repository from GitHub:
    ```bash
    git clone https://github.com/ZainGhosheh/Battleship.git
    ```
2. Navigate to the game directory:
    ```bash
    cd battleship
    ```
3. Run the main script:
    ```bash
    python3 battleship.py
    ```
4. Follow the in-game prompts to choose the number of ships and place them.
5. Take turns with another player firing shots at each other's boards until the game is won.

---

## **Code Structure**

### **Main Game Logic:**
- Handles setup, player turns, and game outcomes.

### **Board Class:**
- Manages board setup, ship placement, and tracking shots.

### **Player Class:**
- Tracks player data like their ships and shot history.

### **UI Module:**
- Displays the board, takes user input, and updates the display after each shot.

---

## **Documentation**

- The full system documentation is available in the `documentation/` folder of the repository.
- Comments are provided throughout the code to explain the logic.
