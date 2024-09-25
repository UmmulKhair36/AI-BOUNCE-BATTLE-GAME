import pygame
import random
# Class to represent a paddle and ball

# COLORS
BLACK = (0,0,0)
WHITE = (255,255,255)

# SCREEN DIMENSIONS
WIDTH , HEIGHT = 700, 500

class Paddle():
    def __init__(self,x,y,width,height,color=WHITE):
        self.x = self.x_start = x
        self.y = self.y_start = y
        self.height = height
        self.width = width
        self.color = color
        self.velocity = 4

    def draw(self,window):
        pygame.draw.rect(window,self.color,pygame.Rect(self.x,self.y,self.width,self.height))


# The top of the screen is y = 0, and the bottom is y = HEIGHT
    def move(self,direction):
        if direction == "up" and self.y > 0:    # Ensures the paddle doesn’t move past the top of the screen
            self.y -= self.velocity
        elif direction == "down" and self.y + self.height < HEIGHT:
            self.y += self.velocity

    def reset_to_stating_pos(self):
        self.x = self.x_start
        self.y = self.y_start

class Ball():
    def __init__(self,x,y,radius,color=WHITE):
        self.x = self.x_start = x
        self.y = self.y_start = y
        self.radius = radius
        self.color = color
        self.max_velocity = 5
        self.x_velocity = random.choice([5,-5])
        self.y_velocity = 0

    def draw(self,window):
        pygame.draw.circle(window,self.color,(self.x,self.y),self.radius)

    def move(self):
        self.x += self.x_velocity
        self.y += self.y_velocity

    def reset_to_stating_pos(self):
        self.x = self.x_start
        self.y = self.y_start
        self.x_velocity = random.choice([5,-5])
        self.y_velocity = 0
