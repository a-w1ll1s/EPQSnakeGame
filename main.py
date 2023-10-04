# SNAKE MAIN

import pygame as py
from pygame.locals import *
import time
import random as r
block = 20


class Apple:
    def __init__(self, win):
        self.win = win
        self.x = 120
        self.y = 120

    def draw(self):
        py.draw.rect(self.win, (255, 0, 0), (self.x, self.y, 20, 20), 0)
        py.display.flip()

    def move(self):
        self.x = r.randint(0, 24) * block
        self.y = r.randint(0, 24) * block


class Snake:
    def __init__(self, win, length):
        self.win = win
        self.length = length
        self.x = [block] * length
        self.y = [block] * length
        self.direction = "none"

    def increase_len(self):
        self.length += 1
        self.x.append(0)
        self.y.append(0)

    def move_up(self):
        if self.direction != "down":
            self.direction = "up"

    def move_down(self):
        if self.direction != "up":
            self.direction = "down"

    def move_left(self):
        if self.direction != "right":
            self.direction = "left"

    def move_right(self):
        if self.direction != "left":
            self.direction = "right"

    def draw(self):
        self.win.fill((0, 0, 0))
        for i in range(self.length):
            py.draw.rect(self.win, (0, 255, 0), (self.x[i], self.y[i], 20, 20), 0)
        py.display.flip()

    def move(self):

        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        if self.direction == "up":
            self.y[0] -= block
        if self.direction == "down":
            self.y[0] += block
        if self.direction == "left":
            self.x[0] -= block
        if self.direction == "right":
            self.x[0] += block

        self.draw()


class Game:
    def __init__(self):

        py.init()

        self.win = py.display.set_mode((500, 500))
        py.display.set_caption("snake")
        self.win.fill((0, 0, 0))

        self.snake = Snake(self.win, 1)
        self.snake.draw()

        self.apple = Apple(self.win)
        self.apple.draw()

        self.frame_iteration = 0

    def collision(self, x1, y1, x2, y2):

        if x2 <= x1 < x2 + block:
            if y2 <= y1 < y2 + block:
                return True

        return False

    def border_collision(self, x, y):

        if 0 <= x < 490:
            if 0 <= y < 490:
                return False

        return True

    def play(self):
        self.snake.move()
        self.apple.draw()
        self.score()

        if self.border_collision(self.snake.x[0], self.snake.y[0]):
            raise "game_over"


        for i in range(0, self.snake.length):
            if self.collision(self.snake.x[i], self.snake.y[i], self.apple.x, self.apple.y):
                self.snake.increase_len()
                self.apple.move()

        for i in range(3, self.snake.length):
            if self.collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                raise "game_over"

    def game_over(self):

        self.win.fill((0, 0, 0))

        file = open("SCORES.txt", "a")
        file.write(str(self.snake.length-1))
        file.write("\n")
        file.close()

        py.display.update()

    def reset(self):

        self.snake = Snake(self.win, 1)
        self.apple = Apple(self.win)

    def score(self):
        font = py.font.SysFont("arial", 20)
        points = font.render((str(self.snake.length - 1)), True, (0, 0, 255))
        self.win.blit(points, (self.snake.x[0], self.snake.y[0]))
        py.display.update()

    def run(self):

        running = True
        paused = False

        while running:
            time.sleep(0.1)

            for event in py.event.get():

                if event.type == KEYDOWN:

                    if event.key == K_ESCAPE:
                        running = False

                    if not paused:
                        if event.key == K_UP:
                            self.snake.move_up()
                        if event.key == K_DOWN:
                            self.snake.move_down()
                        if event.key == K_LEFT:
                            self.snake.move_left()
                        if event.key == K_RIGHT:
                            self.snake.move_right()

                if event.type == QUIT:
                    running = False

            try:
                if not paused:
                    self.play()
            except Exception as e:
                self.game_over()
                paused = False
                self.reset()


if __name__ == "__main__":
    game = Game()
    game.run()



