import pygame
from components import Paddle 
from components import Ball

pygame.init()       #is a function call used to initialize all the modules in the Pygame library that are necessary for the game to run.

# SCREEN DIMENSIONS
WIDTH , HEIGHT = 700, 500

# PADDLE AND BALL SETTINGS
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 90
BALL_RADIUS = 7

# COLORS
BLACK = (0,0,0)
WHITE = (255,255,255)

# GAME SETTINGS
WINNING_SCORE = 3
FPS = 60
SCORE_FONT = pygame.font.SysFont("comicsans",30)


# ****************************************************

# Class that handles the Bounce Battle Game
class Game():
    def __init__(self):
        self.window = pygame.display.set_mode((WIDTH,HEIGHT)) 
        pygame.display.set_caption("AI Bounce Battle")
        self.clock = pygame.time.Clock()

        self.left_paddle = Paddle(10,HEIGHT //2 - PADDLE_HEIGHT // 2,PADDLE_WIDTH,PADDLE_HEIGHT)
        self.right_paddle = Paddle(WIDTH - 10 - PADDLE_WIDTH, HEIGHT //2 - PADDLE_HEIGHT // 2,PADDLE_WIDTH,PADDLE_HEIGHT)

        self.ball = Ball(WIDTH //2 ,HEIGHT //2,BALL_RADIUS)
        
        self.left_score = 0
        self.right_score = 0
    
    def draw_scoreboard(self):
        left_text_score = SCORE_FONT.render(f"{self.left_score}",1,WHITE) # 1- anti-aliasing makes txt smoother
        right_text_score = SCORE_FONT.render(f"{self.right_score}",1,WHITE)
        self.window.blit(left_text_score,(WIDTH // 4 ,10))  #draws the score at a specific location on the screen
        self.window.blit(right_text_score,(WIDTH * 3//4,10))

# Events include things like closing the window, mouse movements, or key presses
    def handleEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        return True
    
    def handle_key_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.left_paddle.move("up")
        elif keys[pygame.K_s]:
            self.left_paddle.move("down")
        elif keys[pygame.K_UP]:
            self.right_paddle.move("up")
        elif keys[pygame.K_DOWN]:
            self.right_paddle.move("down")
    
    def handle_ball_collision(self):
        if self.ball.y + self.ball.radius >= HEIGHT or self.ball.y - self.ball.radius <= 0:
            self.ball.y_velocity *= -1

        if self.ball.x_velocity < 0 and self.ball.x - self.ball.radius <= self.left_paddle.x + self.left_paddle.width:  # means ball is leading for collision
            if self.ball.y >= self.left_paddle.y and self.ball.y <= self.left_paddle.y + self.left_paddle.height:   # Checking if the ball is in the range of the whole paddle
                self.ball.x_velocity *= -1
                middle_y = self.left_paddle.y + self.left_paddle.height / 2
                difference_in_y = middle_y - self.ball.y 
                reduction_factor = self.left_paddle.height / (2 * self.ball.max_velocity)
                self.ball.y_velocity = -difference_in_y / reduction_factor

        if self.ball.x_velocity > 0 and self.ball.x + self.ball.radius >= self.right_paddle.x:
            if self.ball.y >= self.right_paddle.y and self.ball.y <= self.right_paddle.y + self.right_paddle.height:
                self.ball.x_velocity *= -1
                middle_y = self.right_paddle.y + self.right_paddle.height / 2
                difference_in_y = middle_y - self.ball.y 
                reduction_factor = self.right_paddle.height / (2 * self.ball.max_velocity)
                self.ball.y_velocity = -difference_in_y / reduction_factor

    def update_game_state(self):
        self.ball.move()
        self.handle_ball_collision()
        if self.ball.x < -20:
            self.left_paddle.reset_to_stating_pos()
            self.right_paddle.reset_to_stating_pos()
            self.ball.reset_to_stating_pos()
            self.right_score +=1

        elif self.ball.x > WIDTH + 20:
            self.left_paddle.reset_to_stating_pos()
            self.right_paddle.reset_to_stating_pos()
            self.ball.reset_to_stating_pos()
            self.left_score += 1

    def display_winner(self):
        if self.left_score >= WINNING_SCORE:
            winner_text = "Left Player Won!"
        elif self.right_score >= WINNING_SCORE:
            winner_text = "Right Player Won!"
        else:
            return
        text = SCORE_FONT.render(winner_text, 1, WHITE)
        self.window.blit(text, (WIDTH // 2  - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
        pygame.display.update()
        pygame.time.delay(2000)
        self.left_score = 0
        self.right_score = 0

    def run(self):
        # main
        running = True
        while running:
            self.window.fill(BLACK)
            self.draw_scoreboard()
            self.left_paddle.draw(self.window)
            self.right_paddle.draw(self.window)
            self.ball.draw(self.window)
            pygame.display.update()     # Redraws the Game Screen

            running = self.handleEvents()
            self.handle_key_input()
            self.update_game_state()
            self.display_winner()

            self.clock.tick(FPS)     #Frame per second(FPS)

        pygame.quit()