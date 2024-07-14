from snake import Snake
from items import Food, Bonus, Poison, Slow
from render import Render
import config
import pygame


class Game:
  def __init__(self):
    # initialize pygame essentials
    pygame.init()
    pygame.mixer.init(buffer=128)  # Initialize the mixer module
    self.clock = pygame.time.Clock()
    
    # set game variables
    self.width = config.WIDTH
    self.height = config.HEIGHT
    self.speed = config.SPEED
    self.score = 0
    self.food_score = 0
    self.running = True
   
    # set up screen
    self.screen = pygame.display.set_mode((self.width, self.height))
    pygame.display.set_caption("Snake Game")

    # load game images
    self.background_img = pygame.image.load(config.background_img)
    self.snake_head_img = pygame.image.load(config.snake_head_img)
    self.snake_body_img = pygame.image.load(config.snake_img)
    self.food_img = pygame.image.load(config.food_img)
    self.bonus_img = pygame.image.load(config.bonus_img)
    self.poison_img = pygame.image.load(config.poison_img)
    self.slow_img = pygame.image.load(config.slow_img)
    self.score_img = pygame.image.load(config.score_img)
    self.speed_img = pygame.image.load(config.speed_img)
    self.bush_img = pygame.image.load(config.bush_img)
    self.tile_img = pygame.image.load(config.tile_img)
    
    
    # initialize game elements
    self.snake = Snake(self.snake_head_img, self.snake_body_img, self.width // 2, self.height // 2)
    self.food = Food(self.food_img, self.width, self.height, self.snake.snake_body)
    self.bonus = Bonus(self.bonus_img, self.width, self.height, self.snake.snake_body)
    self.poison = Poison(self.poison_img, self.width, self.height, self.snake.snake_body)
    self.slow = Slow(self.slow_img, self.width, self.height, self.snake.snake_body)
    self.render = Render(self.background_img, self.screen, self.snake_head_img, self.snake_body_img, self.food_img, self.bonus_img, self.poison_img, self.slow_img, self.tile_img, self.bush_img)
    
    # initialize game sounds
    self.bonus_sound = pygame.mixer.Sound(config.bonus_sound)
    self.explode_sound = pygame.mixer.Sound(config.explode_sound)
    self.eat_sound = pygame.mixer.Sound(config.bites_sound)
    self.game_over_sound = pygame.mixer.Sound(config.game_over_sound)


  def run(self):
    while self.running:
      self.handle_events()
      self.render.draw_background()
      self.snake.move()
      self.check_collisions_happened()
      self.draw_elements()
      self.check_game_over()
      pygame.display.flip()
      self.clock.tick(self.speed)
      
    pygame.quit()

  def check_game_over(self):
      if self.score < 0:
        self.running = False
      if not self.running:
        self.render.draw_game_over()
        self.game_over_sound.play()
        pygame.display.flip()
        pygame.time.wait(2600)  

  def check_collisions_happened(self):
      if self.snake_collide_item(self.food):
        self.eat_sound.play()
        self.score += 1
        self.food_score += 1
        self.food.position = self.food.create()
        if self.food_score % 5 == 0:
          self.speed += 1
      else:
        self.snake.remove_tail()

      if self.bonus.visible and self.snake_collide_item(self.bonus):
        self.bonus_sound.play()
        self.bonus.hide()
        self.score += 2
        self.snake.remove_tail()

      if self.slow.visible and self.snake_collide_item(self.slow):
        self.bonus_sound.play()
        self.slow.hide()
        self.speed -= 2
        self.score -= 4
      
      if self.poison.visible and self.snake_collide_item(self.poison):
        self.explode_sound.play()
        self.poison.hide()
        self.score -= 5
        self.speed += 2

      if self.snake_collide_walls():
        self.running = False

  def draw_elements(self):
      self.render.draw_snake(self.snake)
      for item in [self.food, self.bonus, self.slow, self.poison]:
        if item.visible:
          self.render.draw_item(item)
      self.render.draw_label(self.score, self.score_img, 0.025, -0.00625)
      self.render.draw_label(self.speed, self.speed_img, 0.1, 0.06875)
  
  def snake_collide_walls(self):
    bush_width = 20
    bush_height = 20
    return(
      self.snake.head.left < bush_width
      or self.snake.head.right > (self.width - bush_width)
      or self.snake.head.top < bush_height
      or self.snake.head.bottom > (self.height - bush_height)
      or self.snake.head in self.snake.snake_body[1:]
    )

  def snake_collide_item(self, item):
    return self.snake.head.colliderect(item.position)

  def handle_events(self):
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        self.running = False
      elif event.type == pygame.KEYDOWN:
        self.handle_keypress(event.key)
      elif event.type == self.bonus.show_event:
        self.bonus.show()
      elif event.type == self.bonus.hide_event:
        self.bonus.hide()
      elif event.type == self.poison.show_event:
        self.poison.show()
      elif event.type == self.poison.hide_event:
        self.poison.hide()
      elif event.type == self.slow.show_event:
        self.slow.show()
      elif event.type == self.slow.hide_event:
        self.slow.hide()
      
  def handle_keypress(self, key):
    if key == pygame.K_UP and self.snake.direction != 'down':
      self.snake.direction = 'up'
    elif key == pygame.K_DOWN and self.snake.direction != 'up':
      self.snake.direction = 'down'
    elif key == pygame.K_LEFT and self.snake.direction != 'right':
      self.snake.direction = "left"
    elif key == pygame.K_RIGHT and self.snake.direction != 'left':
      self.snake.direction = "right"
