import pygame
from pygame.math import Vector2
import sys
import random

class Fruit:
    def __init__(self):
        self.x = random.randint(0, num - 1)
        self.y = random.randint(0, num - 1)
        self.pos = Vector2(self.x, self.y)
    def draw(self):
        fruit_rect = pygame.Rect(self.pos.x*cell, self.pos.y*cell, cell, cell)
        screen.blit(mouse, fruit_rect)

class Snake:
    def __init__(self):
        self.body = [Vector2(9,17),Vector2(9,18),Vector2(9,19)]
        self.direction = Vector2(0,-1)
        self.eat = pygame.mixer.Sound("media\woo_htcxajK.mp3")
        self.grow = False
    def draw(self):
        head = pygame.Rect(self.body[0][0]*cell, self.body[0][1]*cell, cell, cell)
        pygame.draw.rect(screen,"#cc6600", head)
        for i in self.body[1:]:
            snake_block_rect = pygame.Rect(i[0]*cell, i[1]*cell, cell, cell)
            pygame.draw.rect(screen, "#994d00", snake_block_rect)
    def move(self):
        self.border()
        if self.grow == True:
            self.eat.play()
            copy = self.body[:]
            copy.insert(0, copy[0] + self.direction)
            self.body = copy
            self.grow = False
        else:
            copy = self.body[:-1]
            copy.insert(0, copy[0] + self.direction)
            self.body = copy
    def add(self):
        self.grow = True
    
    def border(self):
        x = num-1
        if self.body[0][0] > x:
            self.body[0][0] = 0
        elif self.body[0][0] < 0:
            self.body[0][0] = x
        elif self.body[0][1] > x:
            self.body[0][1] = 0
        elif self.body[0][1] < 0:
            self.body[0][1] = x

    def touch(self):
        if self.body[0] in self.body[1:]:
            return True
        return False
              
class Game:
    def __init__(self):
        self.snake = Snake()
        self.fruit = Fruit()
    def update(self):
        self.snake.move()
    def draw(self):
        self.fruit.draw()
        self.snake.draw()
    def check(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit = Fruit()
            self.snake.add()
    def over(self):
        pygame.quit()
        sys.exit()
    def score(self):
        score_text = str(len(self.snake.body) - 3)
        score_surf = font.render(score_text, True, "#000000")
        screen.blit(score_surf,(10,10))
    def reset(self):
        print(len(self.snake.body)-3)
        x = random.randint(0,10)
        self.snake.body = [Vector2(x,x+1),Vector2(x,x+2),Vector2(x,x+3)]

def check_direction(key):
    if event.key == pygame.K_UP:
        game.snake.direction = check_key(game.snake.direction,Vector2(0,-1))
    if event.key == pygame.K_RIGHT:
        game.snake.direction = check_key(game.snake.direction,Vector2(1,0))
    if event.key == pygame.K_DOWN:
        game.snake.direction = check_key(game.snake.direction,Vector2(0,1))
    if event.key == pygame.K_LEFT:
        game.snake.direction = check_key(game.snake.direction,Vector2(-1,0))

def check_key(old_key, new_key):
    if old_key + new_key == (0,0):
        return old_key
    return new_key

cell = 32
num = 15
pygame.mixer.pre_init(44100,-16,2,512)
pygame.init()
mouse = pygame.image.load("images/mouse1.png")
bg = pygame.image.load("images/cropped 800x800.jpg")
mouse = pygame.transform.scale(mouse,(cell,cell))
game = Game()
pygame.display.set_caption("Snake Game")
screen = pygame.display.set_mode((cell*num, cell*num))
clock = pygame.time.Clock()
font = pygame.font.Font("Prompt-Regular.ttf", 50)
ost = pygame.mixer.Sound("media/gravity-falls-gachi.mp3")
lost = pygame.mixer.Sound("media/fuckyou_N4ocxxs.mp3")
ost.play(loops=50)

screen_update = pygame.USEREVENT
pygame.time.set_timer(screen_update,80)

    
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game.over()
        elif event.type == screen_update:
            game.snake.move()
            if game.snake.touch():
                game.reset()
        elif event.type == pygame.KEYDOWN:
            check_direction(event.key)
    screen.blit(bg, (0,0))
    game.draw()
    game.score()  
    game.check()
    pygame.display.update()
    clock.tick(60)