import pygame
from pygame.locals import *
import math
import time
import random
import os

pygame.display.set_caption('S.')
icon = pygame.image.load("resources/icon/snake.png")
pygame.display.set_icon(icon)

# window (Adjust as necessary - Recommended resolution: 500x500 or higher)
WIDTH = 1000
HEIGHT = 1000

# icon sizes
SIZE = 50

# color attributes
BACKGROUND = (31, 31, 28)
TEXT = (56, 56, 53)
TEXT_LIGHT = (107, 101, 101)


class Point:
    def __init__(self, main):
        # set point image in the center of a 50x50 block (± 12.5px)
        self.x = (SIZE * 3) + SIZE/4
        self.y = (SIZE * 3) + SIZE/4
        self.point = pygame.image.load("resources/point/point-2.png")
        self.point = pygame.transform.smoothscale(self.point, (25, 25))
        self.point_rect = self.point.get_rect(topleft=[self.x, self.y])
        self.main = main

    def draw_point(self):
        self.main.blit(self.point, (self.x, self.y))
        pygame.display.flip()

    def draw_rect(self):
        self.point_rect.x = self.x
        self.point_rect.y = self.y

    def move(self):
        self.x = (random.randint(1, (math.floor(WIDTH/SIZE) - 1)) * SIZE) + float(SIZE/4)
        self.y = (random.randint(1, (math.floor(HEIGHT/SIZE) - 1)) * SIZE) + float(SIZE/4)

        self.draw_rect()


class Snake:
    def __init__(self, main, body):
        self.main = main
        self.body = body
        self.block = pygame.image.load("resources/snake/block.png")

        #### disconnected snake ####
        self.block = pygame.transform.scale(self.block, (40, 40))
        self.block_rect = self.block.get_rect(topleft=[SIZE, SIZE])
        # set snake image in the center of a 50x50 block (± 5px)
        self.x = [SIZE + 5] * body
        self.y = [SIZE + 5] * body

        #### connected snake ####
        # self.block = pygame.transform.scale(self.block, (50, 50))
        # self.block_rect = self.block.get_rect(topleft=[SIZE, SIZE])
        # self.x = [SIZE] * body
        # self.y = [SIZE] * body

        # 1 - up, 2 - down, 3 - left, 4 - right
        self.move = 0

    def draw(self):
        self.main.fill(BACKGROUND)
        for i in range(self.body):
            self.main.blit(self.block, (self.x[i], self. y[i]))

    def snake_bigger(self):
        self.body += 1
        self.x.append(-1)
        self.y.append(-1)

    def move_up(self):
        self.move = 1

    def move_down(self):
        self.move = 2

    def move_left(self):
        self.move = 3

    def move_right(self):
        self.move = 4

    def slither(self):
        # update body
        for i in range(self.body - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        # update head
        if self.move == 1:
            self.y[0] -= SIZE
            self.block_rect.top -= SIZE
        if self.move == 2:
            self.y[0] += SIZE
            self.block_rect.bottom += SIZE
        if self.move == 3:
            self.x[0] -= SIZE
            self.block_rect.left -= SIZE
        if self.move == 4:
            self.x[0] += SIZE
            self.block_rect.right += SIZE

        self.draw()


class Game:
    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode((WIDTH, HEIGHT))
        self.surface.fill(BACKGROUND)
        self.snake = Snake(self.surface, 1)
        self.snake.draw()
        self.point = Point(self.surface)
        self.point.draw_point()

    def play(self):
        self.snake.slither()
        self.point.draw_point()
        self.score()
        pygame.display.flip()

        # +1 point collision
        if self.collision_point(self.snake, self.point):
            self.snake.snake_bigger()
            self.point.move()

        # wall collision
        if self.collision_wall(self.snake.x[0], self.snake.y[0], WIDTH, HEIGHT):
            raise "Game Over"

        # snake self collision
        for i in range(1, self.snake.body):
            if self.collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                raise "Game Over"

    def collision(self, x1, y1, x2, y2):
        # collision detection with x, y position
        if x2 <= x1 < x2 + SIZE:
            if y2 <= y1 < y2 + SIZE:
                return True
        return False

    def collision_point(self, snake, point):
        # collision detection with colliderect function
        if snake.block_rect.colliderect(point.point_rect):
            return True
        return False

    def collision_wall(self, x1, y1, x2, y2):
        if x1 < 0:
            return True
        elif x2 < x1:
            return True
        elif y1 < 0:
            return True
        elif y2 < y1:
            return True
        return False

    def text_generate(self, size):
        font_file = os.path.join(os.path.dirname(__file__), "resources/fonts/retro_gaming/Retro Gaming.ttf")
        font = pygame.font.Font(font_file, size)
        return font

    def score(self):
        score= self.text_generate(50).render(f"{self.snake.body}", True, TEXT_LIGHT)
        score_back = self.text_generate(50).render(f"{self.snake.body}", True, TEXT)
        if self.snake.body <= 9:
            self.surface.blit(score_back, (WIDTH - 50, HEIGHT - 65))
            self.surface.blit(score, (WIDTH - 54, HEIGHT - 69))

        # formatted position for bigger numbers
        if 9 < self.snake.body <= 19:
            self.surface.blit(score_back, (WIDTH - 73, HEIGHT - 65))
            self.surface.blit(score, (WIDTH - 77, HEIGHT - 69))
        # same thing here
        if 19 < self.snake.body <= 99:
            self.surface.blit(score_back, (WIDTH - 87, HEIGHT - 65))
            self.surface.blit(score, (WIDTH - 90, HEIGHT - 69))
        if self.snake.body > 99:
            self.surface.blit(score_back, (WIDTH - 108, HEIGHT - 65))
            self.surface.blit(score, (WIDTH - 112, HEIGHT - 69))

    def game_over(self):
        self.surface.fill(BACKGROUND)
        # 'Game Over'
        over = self.text_generate(30).render("Game Over", True, TEXT)
        over_rect = over.get_rect(center=[WIDTH/2, HEIGHT/2 - HEIGHT/10])
        self.surface.blit(over, over_rect)

        # '[insert score]'
        final_score = self.text_generate(80).render(f"{self.snake.body}", True, TEXT)
        final_score_rect = final_score.get_rect(center=[over_rect.centerx, over_rect.centery + 60])
        self.surface.blit(final_score, final_score_rect)
        final_back = self.text_generate(80).render(f"{self.snake.body}", True, TEXT_LIGHT)
        final_back_rect = final_score.get_rect(center=[over_rect.centerx - 4, over_rect.centery + 64])
        self.surface.blit(final_back, final_back_rect)

        # "press enter"
        enter = self.text_generate(20).render("press enter to play ...", True, TEXT)
        enter = pygame.transform.rotozoom(enter, 90, 1)
        enter_rect = enter.get_rect(topleft=[WIDTH - 35, HEIGHT - 300])
        self.surface.blit(enter, enter_rect)

        pygame.display.flip()

    def reset(self):
        self.snake = Snake(self.surface, 1)
        self.point = Point(self.surface)

    def run(self):
        run_game = True
        stop = False
        while run_game:
            for e in pygame.event.get():
                if e.type == KEYDOWN:
                    if e.key == K_ESCAPE:
                        run_game = False

                    if e.key == K_RETURN:
                        stop = False

                    if not stop:
                        # key press up, down, left, right moves the snake respectively
                        if e.key == K_UP:
                            self.snake.move_up()
                        if e.key == K_DOWN:
                            self.snake.move_down()
                        if e.key == K_LEFT:
                            self.snake.move_left()
                        if e.key == K_RIGHT:
                            self.snake.move_right()

                elif e.type == QUIT:
                    run_game = False

            try:
                if not stop:
                    self.play()
            except Exception as over:
                stop = True
                self.game_over()
                self.reset()

            time.sleep(0.08)


if __name__ == "__main__":
    game = Game()
    game.run()


