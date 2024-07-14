import random
import pygame
import config

class Item:
    def __init__(self, img, width, height, snake_body, show_event_offset=0, hide_event_offset=0, show_interval=(0, 0), hide_interval=0):
        self.img = img
        self.img_width = img.get_width()
        self.img_height = img.get_height()
        self.width = width
        self.height = height
        self.snake_body = snake_body
        self.position = None
        self.visible = False
        self.show_event = pygame.USEREVENT + show_event_offset
        self.hide_event = pygame.USEREVENT + hide_event_offset
        self.show_interval = show_interval
        self.hide_interval = hide_interval
        self.shine_sound = pygame.mixer.Sound(config.shine_sound)
        self.set_next_show_time()

    def set_next_show_time(self):
        if self.show_interval != (0, 0):
            show_time = random.randint(self.show_interval[0], self.show_interval[1]) * 1000
            pygame.time.set_timer(self.show_event, show_time, True)

    def show(self):
        self.position = self.create()
        self.shine_sound.play()
        self.visible = True
        if self.hide_interval > 0:
            pygame.time.set_timer(self.hide_event, self.hide_interval * 1000, True)

    def hide(self):
        self.position = None
        self.visible = False
        self.set_next_show_time()

    def create(self):
        labels_width = self.width * 0.15
        labels_height = self.height * 0.05
        labels_area = pygame.Rect(0, 0, labels_width, labels_height)
        bush_width = self.width // 800 * 32
        bush_height = self.height // 600 * 32
        margin = 10

        # Calculate safe boundaries
        min_x = (bush_width + margin) // self.img_width + 1
        min_y = (bush_height + margin) // self.img_height + 1
        max_x = (self.width - bush_width - margin) // self.img_width - 1
        max_y = (self.height - bush_height - margin) // self.img_height - 1

        while True:
            x = random.randint(min_x, max_x) * self.img_width
            y = random.randint(min_y, max_y) * self.img_height
            item_rect = pygame.Rect(x, y, self.img_width, self.img_height)
            overlapping = (
                item_rect.colliderect(labels_area) or
                any(item_rect.colliderect(segment) for segment in self.snake_body)
            )
            if not overlapping:
                return item_rect


class Poison(Item):
    def __init__(self, img, width, height, snake_body):
        super().__init__(img, width, height, snake_body, 3, 4, (3, 15), 7)


class Bonus(Item):
    def __init__(self, img, width, height, snake_body):
        super().__init__(img, width, height, snake_body, 1, 2, (7, 20), 5)

class Slow(Item):
    def __init__(self, img, width, height, snake_body):
        super().__init__(img, width, height, snake_body, 5, 6, (20, 45), 4)


class Food(Item):
    def __init__(self, img, width, height, snake_body):
        super().__init__(img, width, height, snake_body, 0, 0, (0, 0), 0)
        self.position = self.create()  # Auto-generate position for the food
        self.visible = True
