
# Imports
import pygame

# Scenes parent class.
class Scene():
    def __init__(self):
        self.next_scene = self
        self.game_speed = None
        self.walls = False

    def process_input(self, events, pressed_keys = []):
        raise NotImplementedError
    
    def update(self):
        raise NotImplementedError
    
    def render(self):
        raise NotImplementedError

    def terminate(self):
        self.next_scene = None

    def set_game_speed(self, arg):
        self.game_speed = arg

class Data:
    def __init__(self):
        self.game_speed = None
        self.walls = None