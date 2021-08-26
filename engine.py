import pygame
import random
from pygame import Rect, Vector2
from settings import *

pygame.init()


class Score:
    def __init__(self, color):
        # This class is responsible of score and drawing score to the game surface.
        self.font = pygame.font.Font(None, 332)
        self.score = 0
        self.color = color

    def increase_score(self):
        self.score += 1

    def render(self, main_surface):
        score_surface = self.font.render(str(self.score), True, self.color)
        score_surface.set_alpha(100)
        pos = [
            WIDTH / 2 - score_surface.get_size()[0] / 2,
            HEIGHT / 2 - score_surface.get_size()[1] / 2,
        ]
        main_surface.blit(score_surface, pos)


class Snake:
    def __init__(self, color):
        self.body = [Vector2(10, 10), Vector2(10, 9), Vector2(10, 8)]
        self.direction = Vector2(1, 0)
        self.color = color

    def get_pos(self):
        # Returns head position.
        return self.body[0]

    def change_direction(self, direction):
        # This function prevent the snake from turning 180 degree in the opisite direction,
        # if the new direction is not valid just return old direction (direction don't change)
        # if otherwise return the new direction.
        if direction is not None:
            if self.direction != direction:
                if abs(self.direction.x) != abs(direction.x) or abs(
                    self.direction.y
                ) != abs(direction.y):
                    self.direction = direction
                    return direction
        return self.direction

    def move(self, direction=None):
        # This function make a copy of the snake body and removing the last item and adding
        # a new one at the begining of the list according to the direction.
        body_copy = self.body[:-1]
        body_copy.insert(0, self.body[0] + self.change_direction(direction))
        self.body = body_copy

    def add_new_part(self):
        # Add new part to the body list according to the direction of the snake.
        self.body.insert(0, self.body[0] + self.direction)

    def self_collision(self):
        # This function check if the snake collide with it self.
        for part in self.body[1:]:
            if self.body[0] == part:
                return True
        return False

    def wall_collision(self):
        # Check if the snake collided with a wall.
        # (Walls: On)
        if self.body[0].x >= 19 or self.body[0].x < 1:
            return True
        elif self.body[0].y >= 19 or self.body[0].y < 1:
            return True
        return False

    def mirror_wall_collision(self):
        # This function is responsible for teleporting the snake to opposite side of the screen.
        # (Walls: Off)
        if self.body[0].x < 0:
            self.body[0] += Vector2(20, 0)
        elif self.body[0].x >= 20:
            self.body[0] += Vector2(-20, 0)
        elif self.body[0].y < 0:
            self.body[0] += Vector2(0, 20)
        elif self.body[0].y >= 20:
            self.body[0] += Vector2(0, -20)

    def render(self, main_surface):
        # Draw all snake body parts to the game surface (main_surface).
        for part in self.body:
            rect = pygame.Rect(
                int(part.x * GRID_SIZE),
                int(part.y * GRID_SIZE),
                GRID_SIZE - 4,
                GRID_SIZE - 4,
            )
            pygame.draw.rect(main_surface, self.color, rect)


class Food:
    def __init__(self, color):
        self.color = color
        self.food = None
        self.pos = None
        self.new_food("walls")

    def get_random_position(self, walls):
        # If walls == 'walls' avoid the walls used spaces.
        # Else: Use all screen.
        if walls == "no_walls":
            return [
                random.randint(0, GRID_NUMBER - 1),
                random.randint(0, GRID_NUMBER - 1),
            ]
        else:
            return [
                random.randint(1, GRID_NUMBER - 2),
                random.randint(1, GRID_NUMBER - 2),
            ]

    def get_pos(self):
        # Return food position.
        return self.pos

    def new_food(self, walls):
        # Create a new food by storing the new food position in self.pos and increasing score.
        self.pos = self.get_random_position(walls)

    def render(self, main_surface):
        # Draw food to the game surface.
        pygame.draw.circle(
            main_surface,
            self.color,
            (
                self.pos[0] * GRID_SIZE + GRID_SIZE / 2,
                self.pos[1] * GRID_SIZE + GRID_SIZE / 2,
            ),
            GRID_SIZE / 2 - 2,
        )


def render_walls(main_surface, color):
    # This list contain four Rect object wich will be draw to the screen by itterating on rect_list.
    rect_list = [
        ((0, 0), (GRID_SIZE, WIDTH)),  # top
        ((0, 0), (HEIGHT, GRID_SIZE)),  # left
        ((0, HEIGHT - GRID_SIZE), (WIDTH, GRID_SIZE)),  # bottom
        ((WIDTH - GRID_SIZE, 0), (GRID_SIZE, HEIGHT)),  # right
    ]
    for rect in rect_list:
        pygame.draw.rect(main_surface, color, rect)


def create_theme_selection_preview(colors):
    grid_size = 15
    # Creating a Surface with 8 colums and 8 rows to use it as a grid for the matrix
    # wich is a premade map of the preview show all items in the game wich will help
    # illustrate how the game will look with each theme.
    surface = pygame.Surface((grid_size * 8, grid_size * 8))
    snake, food, _, wall, bg = colors.values()
    matrix = [
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 2, 0, 0, 1],
        [1, 0, 0, 0, 2, 2, 2, 1],
        [1, 0, 0, 0, 0, 0, 2, 1],
        [1, 3, 0, 2, 2, 2, 2, 1],
        [1, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
    ]

    # Using the local variables x, y to track position of each component.
    # 0: Background.
    # 1: Walls.
    # 2: Snake.
    # 3" Food.
    # Itterating trough the matrix, we check for the value of each row,
    # according to the value, we draw a rect with diffrent colors.
    # Finaly return the surface to place in the Play scene.

    x, y = 0, 0
    for col in matrix:
        for row in col:
            if row == 0:
                pygame.draw.rect(
                    surface, bg, (x * grid_size, y * grid_size, grid_size, grid_size)
                )
            if row == 1:
                pygame.draw.rect(
                    surface, wall, (x * grid_size, y * grid_size, grid_size, grid_size)
                )
            if row == 2:
                pygame.draw.rect(
                    surface, snake, (x * grid_size, y * grid_size, grid_size, grid_size)
                )
            if row == 3:
                pygame.draw.rect(
                    surface, food, (x * grid_size, y * grid_size, grid_size, grid_size)
                )
            x += 1
        x, y = 0, y + 1
    return surface
