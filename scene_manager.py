# Imports
import pygame

# Scenes parent class (Scene manager).
class Scene:
    def __init__(self):
        self.next_scene = self

    def process_input(self, events, pressed_keys=[]):
        raise NotImplementedError

    def update(self, delta_time):
        raise NotImplementedError

    def render(self, screen):
        raise NotImplementedError

    def terminate(self):
        self.next_scene = None


# Where all data is stored.
class Data:
    def __init__(self):
        self.speed = None
        self.walls = True
        self.score = 0
        self.theme = "defult"
        self.themes = {
            1: {
                "snake": "white",
                "food": "green",
                "score": "brown",
                "walls": "brown",
                "bg": "black",
            },
            2: {
                "snake": "#FFB830",
                "food": "#3DB2FF",
                "score": "#FF2442",
                "walls": "#FF2442",
                "bg": "#FFEDDA",
            },
            3: {
                "snake": "#FFB830",
                "food": "#368B85",
                "score": "#FF2442",
                "walls": "#FF2442",
                "bg": "#261C2C",
            },
        }
        self.selected_theme = self.themes[1]

    def get_game_speed(self):
        return self.speed
