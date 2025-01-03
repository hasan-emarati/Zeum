import pygame
import random
import math

# Initialize pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pac-Man")

# Set up colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Pac-Man class
class PacMan:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.size = 40  # Increased size for better visibility
        self.speed = 5
        self.angle = 60  # Starting angle for the "mouth"
        self.direction = "RIGHT"
        self.emotion = "HAPPY"  # Default emotion
        self.moving = False  # Movement status (initially not moving)
    
    def move(self):
        if self.moving:
            if self.direction == "UP":
                self.y -= self.speed
            elif self.direction == "DOWN":
                self.y += self.speed
            elif self.direction == "LEFT":
                self.x -= self.speed
            elif self.direction == "RIGHT":
                self.x += self.speed
    
    def draw(self, screen):
        # Draw Pac-Man with a wide, open mouth and improved look
        arc_rect = pygame.Rect(self.x - self.size, self.y - self.size, self.size * 2, self.size * 2)
        pygame.draw.arc(screen, YELLOW, arc_rect, math.radians(self.angle), math.radians(360 - self.angle), self.size)
        
        # Fill the rest of the body to create a more detailed look
        body_rect = pygame.Rect(self.x - self.size, self.y - self.size, self.size * 2, self.size * 2)
        pygame.draw.arc(screen, YELLOW, body_rect, math.radians(360 - self.angle), math.radians(360 + self.angle), self.size)

        # Drawing the eyes: Larger eyes for more expression
        eye_radius = 8
        pygame.draw.circle(screen, WHITE, (self.x + 12, self.y - 12), eye_radius)
        pygame.draw.circle(screen, WHITE, (self.x - 12, self.y - 12), eye_radius)
        pygame.draw.circle(screen, BLACK, (self.x + 12, self.y - 12), 3)
        pygame.draw.circle(screen, BLACK, (self.x - 12, self.y - 12), 3)

        # Drawing the mouth based on Pac-Man's emotion
        if self.emotion == "HAPPY":
            mouth_rect = pygame.Rect(self.x - self.size, self.y - self.size // 2, self.size * 2, self.size)
            pygame.draw.arc(screen, BLACK, mouth_rect, math.radians(30), math.radians(330), self.size // 2)
        elif self.emotion == "SCARED":
            mouth_rect = pygame.Rect(self.x - self.size, self.y - self.size // 2, self.size * 2, self.size)
            pygame.draw.arc(screen, BLACK, mouth_rect, math.radians(50), math.radians(310), self.size // 4)
        
        # Adding some extra shine to the eyes to make them look more lively
        shine_radius = 3
        pygame.draw.circle(screen, WHITE, (self.x + 10, self.y - 14), shine_radius)
        pygame.draw.circle(screen, WHITE, (self.x - 10, self.y - 14), shine_radius)

# Ghost class
class Ghost:
    def __init__(self, color, x, y):
        self.x = x
        self.y = y
        self.size = 30
        self.color = color
        self.speed = 3
        self.emotion = "HAPPY"  # Default emotion
    
    def move(self, pacman_x, pacman_y):
        # Move randomly or towards Pac-Man
        if random.random() < 0.5:  # 50% chance to move randomly
            self.x += random.choice([-1, 1]) * self.speed
            self.y += random.choice([-1, 1]) * self.speed
        else:  # 50% chance to move towards Pac-Man
            if self.x < pacman_x:
                self.x += self.speed
            elif self.x > pacman_x:
                self.x -= self.speed
            if self.y < pacman_y:
                self.y += self.speed
            elif self.y > pacman_y:
                self.y -= self.speed
    
    def draw(self, screen):
        # Draw ghost as a circle with eyes (2 eyes)
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.size)
        eye_radius = 6
        pygame.draw.circle(screen, WHITE, (self.x - 10, self.y - 10), eye_radius)
        pygame.draw.circle(screen, WHITE, (self.x + 10, self.y - 10), eye_radius)
        pygame.draw.circle(screen, BLACK, (self.x - 10, self.y - 10), 2)
        pygame.draw.circle(screen, BLACK, (self.x + 10, self.y - 10), 2)

        # Adjust mouth based on ghost's emotion
        if self.emotion == "ANGRY":
            mouth_rect = pygame.Rect(self.x - self.size, self.y + self.size // 3, self.size * 2, self.size)
            pygame.draw.arc(screen, BLACK, mouth_rect, math.radians(40), math.radians(140), self.size // 4)
        elif self.emotion == "SCARED":
            mouth_rect = pygame.Rect(self.x - self.size, self.y + self.size // 3, self.size * 2, self.size)
            pygame.draw.arc(screen, BLACK, mouth_rect, math.radians(140), math.radians(220), self.size // 4)
        elif self.emotion == "HAPPY":
            mouth_rect = pygame.Rect(self.x - self.size, self.y + self.size // 3, self.size * 2, self.size)
            pygame.draw.arc(screen, BLACK, mouth_rect, math.radians(0), math.radians(360), self.size // 4)

# Main game loop
def game():
    pacman = PacMan()
    ghosts = [Ghost(RED, random.randint(50, 750), random.randint(50, 550)) for _ in range(4)]
    
    clock = pygame.time.Clock()
    running = True
    while running:
        screen.fill(BLACK)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    pacman.direction = "UP"
                    pacman.moving = True  # Start moving when key is pressed
                if event.key == pygame.K_DOWN:
                    pacman.direction = "DOWN"
                    pacman.moving = True
                if event.key == pygame.K_LEFT:
                    pacman.direction = "LEFT"
                    pacman.moving = True
                if event.key == pygame.K_RIGHT:
                    pacman.direction = "RIGHT"
                    pacman.moving = True
            if event.type == pygame.KEYUP:
                if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                    pacman.moving = False  # Stop moving when key is released
        
        # Simulating some emotions
        if pacman.x < WIDTH // 3:  # If Pac-Man is on the left side of the screen
            pacman.emotion = "HAPPY"
        elif pacman.x > WIDTH // 1.5:  # If Pac-Man is on the right side
            pacman.emotion = "SCARED"
        
        # Move Pac-Man and Ghosts
        pacman.move()
        for ghost in ghosts:
            ghost.move(pacman.x, pacman.y)
            if (pacman.x - ghost.x) ** 2 + (pacman.y - ghost.y) ** 2 < (pacman.size + ghost.size) ** 2:
                ghost.emotion = "ANGRY"
            elif ghost.x < WIDTH // 3:
                ghost.emotion = "HAPPY"
            else:
                ghost.emotion = "SCARED"
        
        # Draw Pac-Man and Ghosts with emotions
        pacman.draw(screen)
        for ghost in ghosts:
            ghost.draw(screen)
        
        pygame.display.update()
        clock.tick(30)
    
    pygame.quit()

# Start the game
game()
