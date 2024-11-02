# Imports
from objects.board import Board
import pygame, sys, time

# MainWindow
class MainWindow:
    FRAMES_PER_SECOND = 50
    IMAGES = {
        "stopwatch": pygame.image.load("assets/images/stopwatch.png"),
        "flag": pygame.image.load("assets/images/flag.png"),
        "square": pygame.image.load("assets/images/square.png"),
        "B": pygame.image.load("assets/images/bomb.png"),
        "0": pygame.image.load("assets/images/0.png"),
        "1": pygame.image.load("assets/images/1.png"),
        "2": pygame.image.load("assets/images/2.png"),
        "3": pygame.image.load("assets/images/3.png"),
        "4": pygame.image.load("assets/images/4.png"),
        "5": pygame.image.load("assets/images/5.png"),
        "6": pygame.image.load("assets/images/6.png"),
        "7": pygame.image.load("assets/images/7.png"),
        "8": pygame.image.load("assets/images/8.png")}
    
    def __init__(self):
        """Initialize MainWindow-object"""

        # Window properties
        pygame.init()
        self.screen = pygame.display.set_mode((800, 1000))
        pygame.display.set_caption("Minesweeper - Erik Steigen")
        self.clock = pygame.time.Clock()
        
        # Default settings
        self.difficulty = "EASY"
        self.won = False

        # Initialize game
        self.bombImage = pygame.transform.scale(MainWindow.IMAGES["flag"], (100, 100))
        self.stopwatchImage = pygame.transform.scale(MainWindow.IMAGES["stopwatch"], (200, 200))
        self.initialize()

    def initialize(self):
        """Display the setup screen"""

        # Initialize buttons to be displayed
        self.buttons = {
            "DIFFICULTY": pygame.Rect(140, 200, 520, 80),
            "EASY": pygame.Rect(140, 300, 250, 100),
            "MEDIUM": pygame.Rect(410, 300, 250, 100),
            "HARD": pygame.Rect(140, 420, 250, 100),
            "IMPOSSIBLE": pygame.Rect(410, 420, 250, 100),
            "PLAY": pygame.Rect(250, 570, 300, 80)}

        # Gameloop for setup screen
        while True:

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handleClickMenu(event.pos)
            
            # Update screen
            self.screen.fill((255, 255, 255))
            self.drawButtons()
            pygame.display.flip()
            self.clock.tick(MainWindow.FRAMES_PER_SECOND)

    def drawButtons(self):
        """Draw buttons to choose difficulty, and play"""
        # Initialize font
        font = pygame.font.Font(None, 36)

        # Difficulties
        pygame.draw.rect(self.screen, (0, 0, 0), self.buttons["DIFFICULTY"])
        text = font.render("CHOOSE DIFFICULTY:", True, (255, 255, 255))
        self.screen.blit(text, text.get_rect(center=self.buttons["DIFFICULTY"].center))
        for difficulty in ["EASY", "MEDIUM", "HARD", "IMPOSSIBLE"]:
            color = (0, 200, 0) if self.difficulty == difficulty else (200, 200, 200)
            pygame.draw.rect(self.screen, color, self.buttons[difficulty])
            text = font.render(difficulty, True, (0, 0, 0))
            self.screen.blit(text, text.get_rect(center=self.buttons[difficulty].center))
        
        # Play-button
        pygame.draw.rect(self.screen, (0, 150, 0), self.buttons["PLAY"])
        text = font.render("Play!", True, (255, 255, 255))
        self.screen.blit(text, text.get_rect(center=self.buttons["PLAY"].center))

    def handleClickMenu(self, pos):
        """Handle button clicks to set difficulty and start game"""
        if self.buttons["PLAY"].collidepoint(pos):
            self.startGame()
        elif self.buttons["EASY"].collidepoint(pos):
            self.difficulty = "EASY"
        elif self.buttons["MEDIUM"].collidepoint(pos):
            self.difficulty = "MEDIUM"
        elif self.buttons["HARD"].collidepoint(pos):
            self.difficulty = "HARD"
        elif self.buttons["IMPOSSIBLE"].collidepoint(pos):
            self.difficulty = "IMPOSSIBLE"

    def startGame(self):
        """Start the game with selected settings"""
        # Initialize settings from difficulty
        self.board = Board(self.difficulty)
        self.squareSize = 800 / self.board.size[0]

        # Scale images
        self.images = {}
        for key, value in MainWindow.IMAGES.items():
            self.images[key] = pygame.transform.scale(value, (self.squareSize, self.squareSize))

        # Initialize stopwatch
        self.startTick = pygame.time.get_ticks()

        self.run()

    def run(self):
        """Gameloop"""
        while True:

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                # If mouseclick
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    
                    # Right-click
                    if event.button == 3:
                        self.rightClick(event.pos)

                    # Left-click
                    elif event.button == 1:
                        self.leftClick(event.pos)

            # Fill and update screen with given FPS
            self.screen.fill((255, 255, 255))
            self.drawGame()
            pygame.display.flip()
            self.clock.tick(MainWindow.FRAMES_PER_SECOND)

            # If finished
            if self.board.allSquaresCleared():
                time.sleep(5)
                self.initialize()

    def rightClick(self, pos):
        """Function for handling right-clicks wgile playing"""
        for y in self.board.board:
            for square in y:
                if square.rect.collidepoint(pos):
                    if not square.opened:
                        square.flagged = not square.flagged

    def leftClick(self, pos):
        """Function for handling left-clicks while playing"""
        for i, y in enumerate(self.board.board):
            for j, square in enumerate(y):
                if square.rect.collidepoint(pos):
                    if not square.opened and not square.flagged:
                        square.opened = True
                    if square.type == "0":
                        self.board.openZeros(j, i)
                    if square.type == "B":
                        self.gameOver()
    
    def gameOver(self):
        self.screen.fill((255, 255, 255))
        self.drawGame()
        pygame.display.flip()
        time.sleep(3)
        self.initialize()

    def drawGame(self):
        """Draw the board and topbar"""
        # Initialize font
        font = pygame.font.Font(None, 125)

        # Draw bombcounter
        self.screen.blit(self.bombImage, pygame.Rect(50, 50, 100, 100))
        flags = str(max(0, self.board.bombs - sum(1 for y in self.board.board for square in y if square.flagged)))
        text = font.render(flags, True, (50, 50, 50))
        self.screen.blit(text, text.get_rect(center=pygame.Rect(150, 60, 200, 80).center))

        # Draw stopwatch
        self.screen.blit(self.stopwatchImage, pygame.Rect(400, 35, 100, 100))
        text = font.render(str(float(round((pygame.time.get_ticks()-self.startTick)/1000, 1))), True, (50, 50, 50))
        self.screen.blit(text, text.get_rect(center=pygame.Rect(580, 50, 100, 100).center))

        # Draw squares
        for y in self.board.board:
            for square in y:
                # Draw opened
                if square.opened:
                    self.screen.blit(self.images[square.type], square.rect)
                # Draw flagged
                elif square.flagged:
                    self.screen.blit(self.images["flag"], square.rect)
                # Draw square
                else:
                    self.screen.blit(self.images["square"], square.rect)

        # Draw grid (Temporary)
        for row in range(self.board.size[0]):
            for col in range(self.board.size[1]):
                cellRect = pygame.Rect(col*self.squareSize, 200+row*self.squareSize, self.squareSize, self.squareSize)
                pygame.draw.rect(self.screen, (200, 200, 200), cellRect, 1)


def main():
    window = MainWindow()
    window.run()

if __name__ == "__main__":
    main()