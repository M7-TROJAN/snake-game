import pygame
import config


class Render:
  def __init__(self,background_img, screen, snake_head_img, snake_body_img, food_img, bonus_img, poison_img, slow_img, tile_img, bush_img):
    # initialize screen and colors
    self.screen = screen
    self.green = config.COLORS["green"]
    self.red = config.COLORS["red"]
    self.white = config.COLORS["white"]
    self.black = config.COLORS["black"]
    self.background = config.COLORS["navy"]

    # initialize font
    self.font_size = min(config.WIDTH, config.HEIGHT) // 24
    self.font = pygame.font.Font(None, self.font_size)

    #initialize game images
    self.tile_img = tile_img
    self.bush_img = bush_img
    self.bush_right = pygame.transform.rotate(self.bush_img, 90)
    self.bush_left = pygame.transform.rotate(self.bush_img, -90)
    self.bush_top = pygame.transform.rotate(self.bush_img, 180)
    self.snake_head_img = snake_head_img
    self.snake_body_img = snake_body_img
    self.background_img = pygame.transform.scale(background_img, (config.WIDTH, config.HEIGHT))


  def draw_background(self):
    # Draw the background tiles
    tile_size = 20
    for x in range(0, config.WIDTH, tile_size):
        for y in range(0, config.HEIGHT, tile_size):
            self.screen.blit(self.tile_img, (x, y), (0, 0, tile_size, tile_size))

    # Draw the boundary bushes
    bush_width = 20
    bush_height = 20

    for x in range(0, config.WIDTH, bush_width):
        self.screen.blit(self.bush_top, (x, 0), (0, 0, bush_width, bush_height))
        self.screen.blit(self.bush_img, (x, config.HEIGHT - bush_height), (0, 0, bush_width, bush_height))
    for y in range(0, config.HEIGHT, bush_height):
        self.screen.blit(self.bush_left, (0, y - bush_height), (0, 0, bush_width, bush_height))
        self.screen.blit(self.bush_right, (config.WIDTH - bush_width, y - bush_height), (0, 0, bush_width, bush_height))


  def draw_snake(self, snake):
    # Draw the head
    head_image = self.get_rotated_head_image(snake.direction)
    self.screen.blit(head_image, snake.head.topleft)
    # Draw the body
    for segment in snake.snake_body[1:]:
        self.screen.blit(self.snake_body_img, segment.topleft)


  # a method that rotates the snake head image according to direction
  def get_rotated_head_image(self, direction):
    if direction == 'up':
        return pygame.transform.rotate(self.snake_head_img, 90)
    elif direction == 'down':
        return pygame.transform.rotate(self.snake_head_img, -90)
    elif direction == 'left':
        return pygame.transform.rotate(self.snake_head_img, 180)
    else:  # direction == 'right'
        return self.snake_head_img

  # a method to draw the eatable items
  def draw_item(self, item):
    if item.position:
        self.screen.blit(item.img, item.position.topleft)

  
  # a method to draw the score and speed labels and change their placement according to screen size
  def draw_label(self, label, label_img, x_offset, img_x_offset):
    x_position = config.WIDTH * 0.04
    y_position = config.HEIGHT * 0.05
    text = self.font.render(str(label), True, self.white)
    x_change = int(config.WIDTH * x_offset)
    x_img_change = int(config.WIDTH * img_x_offset)
    text_rect = text.get_rect(topleft=(x_position + x_change, y_position + 3))
    self.screen.blit(label_img, (x_position + x_img_change, y_position))
    self.screen.blit(text, text_rect)


  def draw_game_over(self):
    self.font.set_bold(True)
    text = self.font.render("Game over", True, self.white)
    center_x = self.screen.get_width() // 2 - text.get_width() // 2
    center_y = self.screen.get_height() // 2 - text.get_height() // 2
    self.screen.blit(text, (center_x, center_y))


