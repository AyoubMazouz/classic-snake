# Imports.

import pygame
import random
import sys
from pygame import Vector2
from scene_manager import *
from scenes import *
from engine import *
from settings import *

# initialize pygame.
pygame.init()


class Main:
    def __init__(self):
        # Screen, clock, and setting up the game title.
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Snake")
        # Seting the first scene to the main menu scene.
        self.active_scene = Main_menu()
        self.events = []

    # Main loop.
    def main_loop(self):
        # if there is no scene stop the main loop and quit the program.
        while self.active_scene is not None:

            delta_time = self.clock.tick(FPS) / 100.0

            # To process events in diffrent scene we use the event varriable to store all event then
            # pass it to prcess event function then reset the event variable every frame.

            for event in pygame.event.get():
                self.events.append(event)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Process input and other events.
            self.active_scene.process_input(self.events)
            # Update.
            self.active_scene.update(delta_time)
            # Render graphics.
            self.active_scene.render(self.screen)
            # We assign self.active_scene.next_scene every frame to switch between scenes.
            self.active_scene = self.active_scene.next_scene
            # Clearing the event list each frame.
            self.events = []

            # Update display and cap frame rate.
            pygame.time.Clock().tick(FPS)
            pygame.display.update()


if __name__ == "__main__":
    main = Main()
    main.main_loop()
