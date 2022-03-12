import pygame
import sys
import random
import math

class Apple:
    def __init__(self):
        self.height = 0
        self.new_apple()

    def reset(self):
        self.height = 0
        self.new_apple()

    def new_apple(self):
        self.height += 1
        self.coords = (random.randint(0, NUMBER_OF_BLOCKS-1), random.randint(0, NUMBER_OF_BLOCKS-1))
        self.id = random.random()

        if self.id < 0.5:
            self.type = "normal"
            self.color = RED
        elif self.id < 0.55:
            self.type = "rgb"
            self.color = PURPLE
        elif self.id < 0.69:
            self.type = "slow"
            self.color = BLUE
        elif self.id < 0.7:
            self.type = "egg"
            self.color = LGRAY
        elif self.id < 0.99:
            self.type = "fast"
            self.color = YELLOW
        elif self.id < 0.9999:
            self.type = "bomb"
            self.color = BLACK
        else:
            self.type = "super"
            self.color = WHITE

class Snake:
    def __init__(self, body, rgb):
        self.body = body
        self.rgb = rgb
        self.default_color = random.choice([RED, YELLOW, GREEN, BLUE])
        self.default_color = (int(random.random()*256), int(random.random()*256), int(random.random()*256))

    def get_color(self):
        if not self.rgb:
            return self.default_color
        else:
            return (128 + math.sin(total_frames/10)*128, 128 + math.sin(total_frames/10 + c1)*128, 128 + math.sin(total_frames*math.pi/10 + c2)*128)


BLOCK_SIZE = 20
NUMBER_OF_BLOCKS = 20
WIDTH, HEIGHT = BLOCK_SIZE*NUMBER_OF_BLOCKS, BLOCK_SIZE*NUMBER_OF_BLOCKS
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")

total_frames = 0

c1 = 2*math.pi/3
c2 = c1 * 2

GRAY = (42, 42, 42)
RED = (204, 0, 34)
GREEN = (0, 204, 0)
YELLOW = (204, 204, 0)
BLUE = (0, 102, 204)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LGRAY = (50, 50, 50)
PURPLE = (204, 0, 204)

FPS = 10
apple = Apple()
grid = [["X"]*NUMBER_OF_BLOCKS for _ in range(NUMBER_OF_BLOCKS)]


def new_game():
    global snake
    global command
    global FPS

    apple.reset()
    snake = [Snake([(0, 4), (1, 4)], False)]
    command = (1, 0)
    FPS = 15

def main():
    global command
    global total_frames
    global total_snakes_body

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        total_frames += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    command = (-1, 0)

                if event.key == pygame.K_RIGHT:
                    command = (1, 0)

                if event.key == pygame.K_UP:
                    command = (0, -1)

                if event.key == pygame.K_DOWN:
                    command = (0, 1)

        if snake == []:
            game_over()

        total_snakes_body = [None]
        for k in snake:
            for i in range(len(k.body)-1):
                total_snakes_body.append(k.body[i])
        move()
        draw()
        pygame.display.update()

    pygame.quit()
    sys.exit()

def move():
    for k in snake:
        k.body.pop(0)
        k.body.append((k.body[-1][0] + command[0], k.body[-1][1] + command[1]))

        for i in k.body:
            if not(0 <= i[0] < NUMBER_OF_BLOCKS) or not(0 <= i[1] < NUMBER_OF_BLOCKS):
                kill_snake(k)
        if k.body[-1] == apple.coords:
            new_apple(k)

        head = k.body[-1]
        k.body.pop(-1)
        if head in total_snakes_body:
            kill_snake(k)
        else:
            k.body.append(head)

def draw():
    WIN.fill(GRAY)
    #Gray lines
    for i in range(NUMBER_OF_BLOCKS-1):
        pygame.draw.line(WIN, LGRAY, (BLOCK_SIZE*i+BLOCK_SIZE-1, 0), (BLOCK_SIZE*i+BLOCK_SIZE-1, BLOCK_SIZE*NUMBER_OF_BLOCKS), 2)
        pygame.draw.line(WIN, LGRAY, (0, BLOCK_SIZE*i+BLOCK_SIZE-1), (BLOCK_SIZE*NUMBER_OF_BLOCKS, BLOCK_SIZE*i+BLOCK_SIZE-1), 2)
    #Snake
    for k in snake:
        for i in k.body:
            pygame.draw.rect(WIN, get_snake_color(k.body.index(i), len(k.body), k), (i[0] * BLOCK_SIZE, i[1] * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
    try:
        pygame.draw.rect(WIN, WHITE, (
        k.body[-1][0] * BLOCK_SIZE + BLOCK_SIZE / 4, k.body[-1][1] * BLOCK_SIZE + BLOCK_SIZE / 4, BLOCK_SIZE / 2,
        BLOCK_SIZE / 2))

        pygame.draw.rect(WIN, BLACK, (
        k.body[-1][0] * BLOCK_SIZE + BLOCK_SIZE*3 / 8, k.body[-1][1] * BLOCK_SIZE + BLOCK_SIZE*3 / 8, BLOCK_SIZE / 4,
        BLOCK_SIZE / 4))
    except:
        game_over()

    #Apple
    pygame.draw.circle(WIN, apple.color, (apple.coords[0] * BLOCK_SIZE + BLOCK_SIZE/2, apple.coords[1] * BLOCK_SIZE + BLOCK_SIZE/2), BLOCK_SIZE/2, BLOCK_SIZE)


def game_over():
    if apple.height > 5:
        a = open("highscores.txt", "a")
        a.write(str(apple.height) + "points, " + str(NUMBER_OF_BLOCKS) + "² blocks" "\n")
        a.close()

    new_game()

def new_apple(k):
    global FPS

    k.body.insert(0, k.body[0])
    if apple.type == "slow":
        FPS *= 0.9
    elif apple.type == "fast":
        FPS *= 1.1
    elif apple.type == "bomb":
        for i in range(int(len(k.body)/2)):
            k.body.pop(0)
        apple.height *= 0.5
    elif apple.type == "super":
        for i in range(len(k.body)):
            k.body.insert(0, k.body[0])
        apple.height *= 2
    elif apple.type == "rgb":
        k.rgb = not k.rgb
    elif apple.type == "egg":
        for i in range(10):
            new_snake()
    apple.new_apple()
    while apple.coords in total_snakes_body:
        print("yo")
        apple.new_apple()

def get_snake_color(index, lenght, k):
    return (int(k.get_color()[0]*index/lenght), int(k.get_color()[1]*index/lenght), int(k.get_color()[2]*index/lenght))

def kill_snake(k):
    try:
        snake.pop(snake.index(k))
    except:
        pass

def new_snake():
    snake.append(Snake([(random.randint(0, int(NUMBER_OF_BLOCKS/2)), random.randint(0, int(NUMBER_OF_BLOCKS))), (random.randint(0, int(NUMBER_OF_BLOCKS/2)), random.randint(0, int(NUMBER_OF_BLOCKS)))], False))

new_game()

if __name__ == "__main__":
    main()
