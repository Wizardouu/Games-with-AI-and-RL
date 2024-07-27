import pygame
import random
from enum import Enum
from collections import namedtuple

pygame.init()
font = pygame.font.Font('arial.ttf', 25)



class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4


Point = namedtuple('Point', 'x, y')

# RGB colors
WHITE = (255, 255, 255)
RED = (245, 0, 0)
BLUE1 = (20, 200, 255)
BLUE2 = (30, 190, 255)
BLACK = (0, 0, 0)

BLOCK_SIZE = 20
SPEED = 15


class SnakeGame:

    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h
        # Init display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()
        # Set initial direction right
        self.direction = Direction.RIGHT
        # Initial snake head position at center of screen
        self.head = Point(self.w / 2, self.h / 2)
        # Snake consists of three blocks sticked to each other
        self.snake = [self.head,
                      Point(self.head.x - BLOCK_SIZE, self.head.y),
                      Point(self.head.x - (2 * BLOCK_SIZE), self.head.y)]
        self.count = 1
        self.bigfood = 0
        self.added_time = 0
        self.score = 0
        self.food = None
        self._place_food()

    def _place_food(self):
        x = random.randint(0, (self.w - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (self.h - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()

    def _place_food2(self):
        x = random.randint(0, (self.w - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (self.h - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        if Point(x, y) in self.snake:
            self._place_food2()
        return Point(x, y)

    def play_step(self):
        # 1. Collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and self.direction != Direction.RIGHT:
                    self.direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT and self.direction != Direction.LEFT:
                    self.direction = Direction.RIGHT
                elif event.key == pygame.K_UP and self.direction != Direction.DOWN:
                    self.direction = Direction.UP
                elif event.key == pygame.K_DOWN and self.direction != Direction.UP:
                    self.direction = Direction.DOWN

        # 2. Move
        self._move(self.direction)
        # Add block from the head in next position towards moving direction and remove from last after check if ate food
        self.snake.insert(0, self.head)

        # 3. Check if game over
        game_over = False
        # Is_collision checks if the snake hits itself
        if self._is_collision():
            game_over = True
            return game_over, self.score

        # 4. Place new food or just move
        if self.head == self.food:
            self.score += 1
            self._place_food()
            self.count = self.count + 1
        elif self.bigfood == 0 :
            self.snake.pop()
        elif self.head == self.bigfood or (self.head.x == self.bigfood.x + BLOCK_SIZE and self.head.y == self.bigfood.y + BLOCK_SIZE):
            self.score += 5
            for i in range(1, 4):
                if self.direction == Direction.RIGHT:
                    self.snake.append(Point(self.head.x - i * BLOCK_SIZE, self.head.y))
                elif self.direction == Direction.LEFT:
                    self.snake.append(Point(self.head.x + i * BLOCK_SIZE, self.head.y))
                elif self.direction == Direction.UP:
                    self.snake.append(Point(self.head.x, self.head.y + i * BLOCK_SIZE))
                elif self.direction == Direction.DOWN:
                    self.snake.append(Point(self.head.x, self.head.y - i * BLOCK_SIZE))

            self.bigfood = 0
        else:
            self.snake.pop()

        # 5. Update UI and clock
        # Update function until now we only have the right points but we didn't draw the snake or food so it does that and color the background
        self._update_ui()
        self.clock.tick(SPEED)
        # 6. Return game over and score
        return game_over, self.score

    def _is_collision(self):
        # Hits itself
        if self.head in self.snake[1:]:
            return True
        return False

    def _update_ui(self):
        self.display.fill(WHITE)

        for pt in self.snake:
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, BLUE2, pygame.Rect(pt.x + 4, pt.y + 4, 12, 12))

        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))
        seconds = (pygame.time.get_ticks() - self.added_time) // 1000
        if (seconds > 20 * (1 / SPEED)):
            self.bigfood = 0
        if(self.count % 5 == 0):
            self.bigfood = self._place_food2()
            self.added_time = pygame.time.get_ticks()
            self.count = self.count + 1
        if(self.bigfood != 0):
            pygame.draw.rect(self.display, RED, pygame.Rect(self.bigfood.x, self.bigfood.y, BLOCK_SIZE*2, BLOCK_SIZE*2))

        text = font.render("Score: " + str(self.score), True, BLACK)
        self.display.blit(text, [0, 0])
        pygame.display.flip()

    def _move(self, direction):
        x = self.head.x
        y = self.head.y
        if direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif direction == Direction.UP:
            y -= BLOCK_SIZE

        # Wrap around screen boundaries
        if x >= self.w:
            x = 0
        elif x < 0:
            x = self.w - BLOCK_SIZE
        if y >= self.h:
            y = 0
        elif y < 0:
            y = self.h - BLOCK_SIZE

        self.head = Point(x, y)


if __name__ == '__main__':
    game = SnakeGame()

    # Game loop
    while True:
        game_over, score = game.play_step()

        if game_over:
            break

    print('Final Score', score)

    pygame.quit()
