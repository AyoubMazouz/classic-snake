import pygame, random
from settings import *
from scene_manager import *
from ui import *
from engine import *

pygame.init()

data = Data()

class Main_menu(Scene):
    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        self.surface = pygame.Surface(SCREEN_SIZE)
        self.walls = False
        self.easy_btn = Button(self.surface, (100, 400), text='Easy', command=lambda:self.choice(200))
        self.normal_btn = Button(self.surface, (250, 400), text='Normal', command=lambda:self.choice(100))
        self.hard_btn = Button(self.surface, (400, 400), text='Hard', command=lambda:self.choice(50))

    def choice(self, arg):
        data.game_speed = arg
        self.next_scene = Game(self.screen)

    def process_input(self, events, pressed_keys=[]):
        pass

    def update(self):
        self.easy_btn.update()
        self.normal_btn.update()
        self.hard_btn.update()

    def render(self):
        self.surface.fill(BG)
        self.easy_btn.render()
        self.normal_btn.render()
        self.hard_btn.render()
        self.screen.blit(self.surface, (0, 0))

class Game(Scene):
    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        self.surface = pygame.Surface(SCREEN_SIZE)
        self.game_over = False
        self.NEW_EVENT = pygame.USEREVENT + 1
        self.snake = Snake(self.surface)
        self.food = Food(self.surface)
        self.score = Score(self.surface)
        self.wall = Walls(self.surface, 'walls_type')
        self.used_spaces = self.wall.used_spaces
        self.init()

    def init(self):
        pygame.time.set_timer(self.NEW_EVENT, data.game_speed)
        self.food.new_food(self.used_spaces)
        
    def process_input(self, events, pressed_keys=[]):
        for event in events:
            if not self.game_over:
                if event.type == self.NEW_EVENT:
                    self.snake.move(self.snake.direction)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.snake.movement((Vector2(0, -1)))
                    elif event.key == pygame.K_DOWN:
                        self.snake.movement((Vector2(0, 1)))
                    elif event.key == pygame.K_RIGHT:
                        self.snake.movement((Vector2(1, 0)))
                    elif event.key == pygame.K_LEFT:
                        self.snake.movement((Vector2(-1, 0)))
                    elif event.key == pygame.K_w:
                        self.snake.movement((Vector2(0, -1)))
                    elif event.key == pygame.K_s:
                        self.snake.movement((Vector2(0, 1)))
                    elif event.key == pygame.K_d:
                        self.snake.movement((Vector2(1, 0)))
                    elif event.key == pygame.K_a:
                        self.snake.movement((Vector2(-1, 0)))
            else:
                self.next_scene = Main_menu(self.screen)

    def update(self):
        if not data.walls:
            self.snake.mirror_wall_collision()
            self.game_over = self.snake.self_collision()
        else:
            self.game_over = self.snake.walls_collision() or self.snake.self_collision()
        
        if self.snake.food_collision(self.food.pos):
            self.score.increase_score()
            self.food.new_food(self.used_spaces)
    
    def render(self):
        self.surface.fill(BG)        
        self.score.render()
        self.food.render()
        self.snake.render()
        self.wall.render()
        self.screen.blit(self.wall.surface, (0, 0))
        self.screen.blit(self.surface, (0, 0))

    
