import pygame, random
from pygame import *
from settings import *

pygame.init()


class Score:
    def __init__(self, surface):
        self.surface = surface
        self.score = 0
        self.font = pygame.font.Font(None, 332)

    def update():
        pass

    def increase_score(self):
        self.score += 1

    def render(self):
        score_surface = self.font.render(str(self.score), True, 'white')
        score_surface.set_alpha(100)
        pos = WIDTH / 2 - score_surface.get_size()[0] / 2, HEIGHT / 2 - score_surface.get_size()[1] / 2
        self.surface.blit(score_surface, (pos))

class Snake:
    def __init__(self, surface):
        self.surface = surface
        self.body = [Vector2(10, 10), Vector2(10, 9), Vector2(10, 8)]
        self.direction = Vector2(0, 1)

    def movement(self, direction):
        x = abs(self.direction.x) != abs(direction.x)
        y = abs(self.direction.y) != abs(direction.y)
        if self.direction != direction:
            if x or y:
                self.direction = direction
                
    def move(self, direction):
        new_body = self.body[:-1]
        new_body.insert(0, self.body[0] + direction)
        self.body = new_body
    
    def walls_collision(self):
        if self.body[0].x >= 20 or self.body[0].x < 0:
       		return True
        elif self.body[0].y >= 20 or self.body[0].y < 0:
       		return True
        return False 

    def food_collision(self, food_pos):
        if food_pos == self.body[0]: 
            self.add_new_part()
            return True
    
    def self_collision(self):
        for part in self.body[1:]:
            if self.body[0] == part:
                return True
            
    def mirror_wall_collision(self):
        if self.body[0].x < 0:
            self.body[0] += Vector2(20, 0)
        elif self.body[0].x >= 20:
            self.body[0] += Vector2(-20, 0)
        elif self.body[0].y < 0:
            self.body[0] += Vector2(0, 20)
        elif self.body[0].y >= 20:
            self.body[0] += Vector2(0, -20)


    def add_new_part(self):
    	self.body.insert(0, self.body[0] + self.direction)

    def render(self):
        for part in self.body:
            part = pygame.Rect(int(part.x * GRID_SIZE), int(part.y * GRID_SIZE), GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(self.surface, 'white', part)

class Food:
    def __init__(self, surface):
        self.surface = surface
        self.food = None
        self.pos = None
    
    def get_random_vector(self):
        return Vector2(random.randint(0, GRID_NUMBER-1), random.randint(0, GRID_NUMBER-1))

    def new_food(self, used_spaces):
        self.pos = self.get_random_vector()
        while self.pos in used_spaces:
            self.pos = self.get_random_vector()
            print('we tried again')
        self.food = pygame.Rect(self.pos.x * GRID_SIZE, self.pos.y * GRID_SIZE, GRID_SIZE, GRID_SIZE)

    def render(self):
    	pygame.draw.rect(self.surface, 'green', self.food)

class Walls:
    def __init__(self, surface, walls_type):
        self.surface = surface
        self.walls_type = walls_type
        self.used_spaces = []
        self.x, self.y = 0, 0
        self.four_sides_wall = ['11111100000011111111',
                                '10000000000000000001',
                                '10000000000000000001',
                                '10000000000000000001',
                                '10000000000000000001',
                                '10000000000000000001',
                                '00000000000000000000',
                                '00000000000000000000',
                                '00000000000000000000',
                                '00000000000000000000',
                                '00000000000000000000',
                                '00000000000000000000',
                                '00000000000000000000',
                                '00000000000000000000',
                                '00000000000000000001',
                                '10000000000000000001',
                                '10000000000000000001',
                                '10000000000000000001',
                                '10000000000000000001',
                                '11111110000001111111',
                                ]

    def render(self):
        for row in self.four_sides_wall:
            for col in list(row):
                if col == '1':
                    pygame.draw.rect(self.surface, 'yellow', (self.x * GRID_SIZE, self.y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
                    self.used_spaces.append(Vector2(self.x, self.y))
                self.x += 1
            self.x = 0
            self.y += 1
        self.y = 0


    