import pygame
import random
import sys
from pygame import surface
import pygame_gui
from settings import *
from scene_manager import *
from engine import *

pygame.init()

# The global data object.
data = Data()


class Main_menu(Scene):
    def __init__(self):
        super().__init__()
        self.surface = pygame.Surface(SCREEN_SIZE)
        self.manager = pygame_gui.UIManager(SCREEN_SIZE)
        # variables.
        self.btn_size = (100, 50)
        # UI elements.
        self.title = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(
                (HEIGHT / 2 - self.btn_size[0] / 2, 100), self.btn_size
            ),
            text="Snake",
            manager=self.manager,
        )
        self.play_btn = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (HEIGHT / 2 - self.btn_size[0] / 2, 300), self.btn_size
            ),
            text="Play",
            manager=self.manager,
        )
        self.exit_btn = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (HEIGHT / 2 - self.btn_size[0] / 2, 400), self.btn_size
            ),
            text="Exit",
            manager=self.manager,
        )

    def process_input(self, events, pressed_keys=[]):
        for event in events:
            self.manager.process_events(event)
            if event.type == pygame.USEREVENT:
                # If A Button Is Pressed.
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.play_btn:
                        self.next_scene = Play()
                    if event.ui_element == self.exit_btn:
                        pygame.quit()
                        sys.exit()

    def update(self, delta_time):
        self.manager.update(delta_time)

    def render(self, screen):
        self.surface.fill(BG)
        self.manager.draw_ui(self.surface)
        screen.blit(self.surface, (0, 0))


class Play(Scene):
    def __init__(self):
        super().__init__()
        self.surface = pygame.Surface(SCREEN_SIZE)
        self.manager = pygame_gui.UIManager(SCREEN_SIZE)
        # Varibables
        self.btn_size = (100, 50)
        self.small_btn_size = (50, 50)
        self.errow_btn_size = (20, 20)
        self.walls_btn_strings = ["On", "Off"]
        self.walls_btn_state = False
        self.theme_index = 1
        # UI elements.
        # Back.
        self.back_btn = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((10, 10), self.btn_size),
            text="< Back",
            manager=self.manager,
        )
        # Theme.
        self.theme_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((150 - self.btn_size[0] / 2, 100), self.btn_size),
            text="Theme:",
            manager=self.manager,
        )
        self.theme_left_btn = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((250, 100), self.small_btn_size),
            text="<",
            manager=self.manager,
        )
        self.theme_right_btn = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((450, 100), self.small_btn_size),
            text=">",
            manager=self.manager,
        )
        # Speed.
        self.walls_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((250, 170), (60, 20)),
            text="Fast",
            manager=self.manager,
        )
        self.walls_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((345, 170), (60, 20)),
            text="Normal",
            manager=self.manager,
        )
        self.walls_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((440, 170), (60, 20)),
            text="Slow",
            manager=self.manager,
        )
        self.speed_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((150 - self.btn_size[0] / 2, 200), self.btn_size),
            text="speed:",
            manager=self.manager,
        )
        self.speed_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((300 - self.btn_size[0] / 2, 200), (250, 50)),
            start_value=125,
            value_range=(50, 200),
            manager=self.manager,
        )
        # Walls.
        self.walls_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((100, 300), self.btn_size),
            text="Walls:",
            manager=self.manager,
        )
        self.walls_btn = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((250, 300), self.small_btn_size),
            text="Off",
            manager=self.manager,
        )
        # start.
        self.start_btn = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((100, 400), self.btn_size),
            text="Start",
            manager=self.manager,
        )

    def toggle_walls_btn(self):
        # This function toggle between walls = False and walls == true.
        # Like toggle button.
        if self.walls_btn_state:
            self.walls_btn.set_text(self.walls_btn_strings[1])
            self.walls_btn_state = False
        else:
            self.walls_btn.set_text(self.walls_btn_strings[0])
            self.walls_btn_state = True

    def next_theme(self):
        # This function change selected theme in data class to the next theme.
        themes = data.themes
        themes_number = len(themes)
        if self.theme_index != themes_number:
            self.theme_index += 1
            data.selected_theme = data.themes[self.theme_index]
        else:
            self.theme_index = 1
            data.selected_theme = data.themes[self.theme_index]

    def previous_theme(self):
        # This function change selected theme in data class to the previous theme.
        themes = data.themes
        themes_number = len(themes)
        if self.theme_index != 1:
            self.theme_index -= 1
            data.selected_theme = data.themes[self.theme_index]
        else:
            self.theme_index = themes_number
            data.selected_theme = data.themes[self.theme_index]

    def store_data(self):
        # This function store all the data gadered from this scene to use in other scenes.
        data.walls = self.walls_btn_state
        data.speed = self.speed_slider.get_current_value()
        data.theme = None

    def process_input(self, events):
        # all input and events are prcessed here.
        for event in events:
            self.manager.process_events(event)
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.back_btn:
                        self.next_scene = Main_menu()
                    if event.ui_element == self.theme_left_btn:
                        self.previous_theme()
                    if event.ui_element == self.theme_right_btn:
                        self.next_theme()
                    if event.ui_element == self.walls_btn:
                        self.toggle_walls_btn()
                    if event.ui_element == self.start_btn:
                        self.store_data()
                        self.next_scene = Game()

    def update(self, delta_time):
        self.manager.update(delta_time)

    def render(self, screen):
        # drawing the main surface to the screnn
        self.manager.draw_ui(self.surface)
        self.surface.blit(
            create_theme_selection_preview(data.selected_theme), (315, 28)
        )
        screen.blit(self.surface, (0, 0))


class Game(Scene):
    def __init__(self):
        super().__init__()
        self.surface = pygame.Surface(SCREEN_SIZE)
        # Events
        self.NEW_EVENT = pygame.USEREVENT + 1
        # Variables.
        self.game_over = False
        self.colors = [color for color in data.selected_theme.values()]
        # Objects
        self.snake = Snake(self.colors[0])
        self.food = Food(self.colors[1])
        self.score = Score(self.colors[2])

        # set Global timer.
        pygame.time.set_timer(self.NEW_EVENT, data.get_game_speed())

    def no_walls(self):
        # This fucntion handle logic when no walls option selected.

        # Check for gameover.
        if self.snake.self_collision():
            self.game_over = True

        # When snake eat food (collision).
        if self.snake.get_pos() == self.food.get_pos():
            self.score.increase_score()
            self.food.new_food("no_walls")
            self.snake.add_new_part()

        self.snake.mirror_wall_collision()

    def walls(self):
        # This fucntion handle logic when no walls option selected.

        # Check for gameover.
        if self.snake.self_collision() or self.snake.wall_collision():
            self.game_over = True

        # When snake eat food (collision).
        if self.snake.get_pos() == self.food.get_pos():
            self.score.increase_score()
            self.food.new_food("walls")
            self.snake.add_new_part()

    def process_input(self, events, pressed_keys=[]):
        for event in events:
            if not self.game_over:
                if event.type == self.NEW_EVENT:
                    self.snake.move()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.next_scene = Main_menu()
                    elif event.key == pygame.K_UP:
                        self.snake.change_direction((Vector2(0, -1)))
                    elif event.key == pygame.K_DOWN:
                        self.snake.change_direction((Vector2(0, 1)))
                    elif event.key == pygame.K_RIGHT:
                        self.snake.change_direction((Vector2(1, 0)))
                    elif event.key == pygame.K_LEFT:
                        self.snake.change_direction((Vector2(-1, 0)))
                    elif event.key == pygame.K_w:
                        self.snake.change_direction((Vector2(0, -1)))
                    elif event.key == pygame.K_s:
                        self.snake.change_direction((Vector2(0, 1)))
                    elif event.key == pygame.K_d:
                        self.snake.change_direction((Vector2(1, 0)))
                    elif event.key == pygame.K_a:
                        self.snake.change_direction((Vector2(-1, 0)))
            else:
                data.score = self.score.score
                self.next_scene = LosingScreen()

    def update(self, delta_time):
        if data.walls:
            self.walls()
        else:
            self.no_walls()

    def render(self, screen):
        # Drawing the game surface to the screen and calling rendering functions.
        self.surface.fill(self.colors[4])
        self.score.render(self.surface)
        self.food.render(self.surface)
        self.snake.render(self.surface)
        # If walls option selected draw walls.
        if data.walls:
            render_walls(self.surface, self.colors[3])
        screen.blit(self.surface, (0, 0))


class LosingScreen(Scene):
    def __init__(self):
        super().__init__()
        self.surface = pygame.Surface(SCREEN_SIZE)
        self.manager = pygame_gui.UIManager(SCREEN_SIZE)
        # UI elements.
        self.score_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((250, 150), (100, 50)),
            text=f"Score: {data.score}",
            manager=self.manager,
        )
        self.play_again_btn = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((250, 300), (100, 50)),
            text="Play Again",
            manager=self.manager,
        )
        self.main_menu_btn = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((250, 400), (100, 50)),
            text="Main Menu",
            manager=self.manager,
        )
        self.exit_btn = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((250, 500), (100, 50)),
            text="Exit",
            manager=self.manager,
        )

    def process_input(self, events):
        for event in events:
            self.manager.process_events(event)
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.play_again_btn:
                        self.next_scene = Game()
                    if event.ui_element == self.main_menu_btn:
                        self.next_scene = Main_menu()
                    if event.ui_element == self.exit_btn:
                        pygame.quit()
                        sys.exit()

    def update(self, delta_time):
        self.manager.update(delta_time)

    def render(self, screen):
        self.surface.fill(BG)
        self.manager.draw_ui(self.surface)
        screen.blit(self.surface, (0, 0))
