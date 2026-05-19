from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Rectangle, Color
from random import randint

Window.fullscreen = True


class Game(Widget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # ===== PLAYER =====
        self.x = 150
        self.y = 300
        self.vel_y = 0
        self.gravity = 1
        self.jump_power = 18
        self.ground = 300
        self.size = 80

        # ===== SPIKE =====
        self.spike_x = Window.width
        self.spike_speed = 10
        self.spike_size = 80

        # ===== GAME STATE =====
        self.game_over = False
        self.score = 0

        # ===== DRAW =====
        with self.canvas:
            Color(0, 1, 1)
            self.player = Rectangle(pos=(self.x, self.y), size=(self.size, self.size))

            Color(1, 0, 0)
            self.spike = Rectangle(pos=(self.spike_x, self.ground), size=(self.spike_size, self.spike_size))

        Clock.schedule_interval(self.update, 1 / 60)

    # ===== TAP TO JUMP =====
    def on_touch_down(self, touch):
        if self.game_over:
            self.reset()
        else:
            if self.y <= self.ground:
                self.vel_y = self.jump_power

    # ===== RESET =====
    def reset(self):
        self.game_over = False
        self.score = 0
        self.spike_x = Window.width
        self.y = self.ground

    # ===== GAME LOOP =====
    def update(self, dt):

        if self.game_over:
            return

        # GRAVITÀ
        self.vel_y -= self.gravity
        self.y += self.vel_y

        if self.y < self.ground:
            self.y = self.ground
            self.vel_y = 0

        # SPIKE MOVE
        self.spike_x -= self.spike_speed

        if self.spike_x < -100:
            self.spike_x = Window.width + randint(100, 400)
            self.score += 1

        # COLLISIONE
        if (self.x < self.spike_x + self.spike_size and
            self.x + self.size > self.spike_x and
            self.y < self.ground + self.spike_size and
            self.y + self.size > self.ground):

            self.game_over = True


        self.player.pos = (self.x, self.y)
        self.spike.pos = (self.spike_x, self.ground)


class KundoGame(App):
    def build(self):
        return Game()


KundoGame().run()