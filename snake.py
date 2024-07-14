import pygame

class Snake:
  def __init__(self, head_img, body_img, initial_x, initial_y):
    self.head_img = head_img
    self.body_img = body_img
    self.body_width = body_img.get_width()
    self.body_height = body_img.get_height()
    self.head = pygame.Rect(initial_x, initial_y, self.body_width, self.body_height)
    self.snake_body = [
        self.head,
        pygame.Rect(initial_x - self.body_width, initial_y, self.body_width, self.body_height),
        pygame.Rect(initial_x - 2 * self.body_width, initial_y, self.body_width, self.body_height)
      ]
    self.direction = "right"


  def move(self):
    if self.direction == 'up':
      new_head = pygame.Rect(self.head.x, self.head.y - self.head.height, self.head.width, self.head.height)
    elif self.direction == 'down':
        new_head = pygame.Rect(self.head.x, self.head.y + self.head.height, self.head.width, self.head.height)
    elif self.direction == 'left':
      new_head = pygame.Rect(self.head.x - self.head.width, self.head.y, self.head.width, self.head.height)
    elif self.direction == 'right':
      new_head = pygame.Rect(self.head.x + self.head.width, self.head.y, self.head.width, self.head.height)

    self.snake_body.insert(0, new_head)
    self.head = self.snake_body[0]

  def remove_tail(self):
    self.snake_body.pop()