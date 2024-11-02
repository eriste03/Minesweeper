# Imports
from objects.square import Square
import os, json, random, pygame

# Initialize config from file
configPath = os.path.join(os.path.dirname(__file__), "..", "configs", "board_config.json")
with open(configPath, "r") as configFile:
    config = json.load(configFile)

# Board class
class Board:
    
    def __init__(self, difficulty):
        self.size = config[difficulty]["SIZE"]
        self.bombs = config[difficulty]["BOMBS"]
        self.generateBoard()
    
    def generateBoard(self):
        """
        Generates self.board with bombs and numbers
        """
        self.board = []
        for y in range(self.size[1]):
            self.board.append([])
            for x in range(self.size[0]):
                self.board[y].append(Square(self.size))
        
        # Add x bombs to board
        boardPositions = [(i, j) for i in range(self.size[1]) for j in range(self.size[0])]
        bombPositions = random.sample(boardPositions, self.bombs)
        for (i, j) in bombPositions:
            self.board[i][j].type = "B"
        
        # Check how many bombs the square borders to
        for i, y in enumerate(self.board):
            for j, x in enumerate(self.board[i]):
                if self.board[i][j].type != "B":
                    self.board[i][j].type = self.checkBordersBombs(j, i)
        
        # Generate rects for the squares
        for i, y in enumerate(self.board):
            for j, x in enumerate(y):
                self.board[i][j].rect = pygame.Rect(j*self.board[i][j].size, 200+i*self.board[i][j].size, self.board[i][j].size, self.board[i][j].size)

    def checkBordersBombs(self, x, y):
        """
        Checks all borders to given square for bombs
        Returns: amount of bombs it borders to
        """
        # Initialize all bordering squares and amount
        borders = [
            [x-1, y-1], [x, y-1], [x+1, y-1],
            [x-1, y],             [x+1, y],
            [x-1, y+1], [x, y+1], [x+1, y+1]]
        amount = 0

        # Check each bordering square
        for border in borders:
            if self.checkSquare(border[0], border[1], "B"):
                amount += 1

        # Return amount
        return str(amount)
    
    def openZeros(self, x, y, visited=None):
        """Function for opening all surrounded zeros to a zero"""
        # Initialize visited squares
        if visited is None:
            visited = set()

        # Add the current square to visited
        visited.add((x, y))

        # Define the surrounding squares
        borders = [
            [x-1, y-1], [x, y-1], [x+1, y-1],
            [x-1, y],             [x+1, y],
            [x-1, y+1], [x, y+1], [x+1, y+1]]
        
        for border in borders:
            bx, by = border
            
            if (bx, by) not in visited and self.checkSquare(bx, by):    # Check if square has been visited and exists
                self.board[by][bx].opened = True                        # Open square

                if self.checkSquare(bx, by, "0"):                       # Check if square is 0
                    self.openZeros(bx, by, visited)                     # Open squares around new 0
    
    def allSquaresCleared(self):
        """Returns True if all squares have been cleared"""
        num = 0
        for y in self.board:
            for square in y:
                if not square.opened and square.type != "B":
                    return False
        return True

    def checkSquare(self, x, y, check=None):
        """
        Checks if specific square is bomb
        Returns: True if "==check", False if not or non existing (ex. [-1, 3])
        """
        if x == -1 or y == -1 or x >= self.size[0] or y >= self.size[1]:
            return False
        try:
            if self.board[y][x].type == check or check == None:
                return True
            return False
        except:
            print(f"Failure on checking coordinate: {x, y}")
        return False