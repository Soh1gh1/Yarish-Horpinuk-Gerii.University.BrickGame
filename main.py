import pygame
import sys
import random

WIDTH = 840
HEIGHT = 600
FPS = 60
score = 0
lives = 3

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# initialize Pygame
pygame.init()
pygame.mixer.init()

# set up the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Breakout")
clock = pygame.time.Clock()

class Ball(pygame.sprite.Sprite):
    def __init__(self, color, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 10))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 5
        self.dx = random.choice([-1, 1])
        self.dy = -1

    def update(self):
        self.rect.x += self.speed * self.dx
        self.rect.y += self.speed * self.dy

        if self.rect.top <= 0:
            self.dy = 1
        if self.rect.bottom >= HEIGHT:
            self.dy = -1

        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.dx *= -1

class Paddle(pygame.sprite.Sprite):
    def __init__(self, color, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((100, 10))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

class Brick(pygame.sprite.Sprite):
    def __init__(self, color, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((80, 20))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

# create sprite groups
all_sprites = pygame.sprite.Group()
bricks = pygame.sprite.Group()

# create the paddle and ball
paddle = Paddle(WHITE, WIDTH/2, HEIGHT-50)
ball = Ball(WHITE, WIDTH/2, HEIGHT-70)

# add the paddle and ball to the sprite group
all_sprites.add(paddle)
all_sprites.add(ball)

# create the bricks
level = 1  # start with level 1
for i in range(10):
    for j in range(5):
        brick = Brick((255-i*25, i*25, 0), i*80+60, j*25+50)
        bricks.add(brick)
        all_sprites.add(brick)

# game loop
running = True
while running:
    # set the game speed
    clock.tick(FPS)

    # handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # update the sprites
    all_sprites.update()

    # check for collision between ball and paddle
    if pygame.sprite.collide_rect(ball, paddle):
        ball.dy = -1

        # increase ball speed when hitting paddle
        ball.speed += 0.1

        # limit the maximum speed of the ball
        if ball.speed > 5:
            ball.speed = 5

    # check for collision between ball and bricks
    hits = pygame.sprite.spritecollide(ball, bricks, True)
    if hits:
        ball.dy *= -1
        score += 10

        # check if all the bricks have been destroyed
        if not bricks:
            level += 1
            if level > 3:
                # if all levels have been completed, display the victory message and exit the game
                running = False
                font = pygame.font.SysFont(None, 48)
                text = font.render("YOU WIN!", True, WHITE)
                screen.blit(text, (WIDTH / 2 - 100, HEIGHT / 2))
            else:
                # if not all levels have been completed, create a new set of bricks for the next level
                for i in range(10):
                    for j in range(5):
                        brick = Brick((255 - i * 25, i * 25, 0), i * 80 + 60, j * 25 + 50)
                        bricks.add(brick)
                        all_sprites.add(brick)
# draw the game
    screen.fill(BLACK)
    all_sprites.draw(screen)

    # display the score and level
    font = pygame.font.SysFont(None, 30)
    text = font.render("Score: " + str(score), True, WHITE)
    screen.blit(text, (10, 10))
    text = font.render("Level: " + str(level), True, WHITE)
    screen.blit(text, (10, 30))

    # check for game over
    if ball.rect.bottom >= HEIGHT:
        lives -= 1
        if lives == -1:
            # if no lives left, display game over message and exit the game
            running = False
            font = pygame.font.SysFont(None, 48)
            text = font.render("GAME OVER", True, WHITE)
            screen.blit(text, (WIDTH / 2 - 100, HEIGHT / 2))
        else:
            # if lives left, reset the ball and paddle position
            ball.rect.center = (WIDTH / 2, HEIGHT - 70)
            paddle.rect.center = (WIDTH / 2, HEIGHT - 50)

    # display the number of lives left
    text = font.render("Lives: " + str(lives), True, WHITE)
    screen.blit(text, (WIDTH - 80, 10))

    # update the display
    pygame.display.flip()

# quit the game
pygame.quit()
sys.exit()