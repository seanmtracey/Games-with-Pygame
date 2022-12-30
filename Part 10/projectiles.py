class Bullet():

  x = 0
  y = 0
  image = None
  pygame = None
  surface = None
  width = 0
  height = 0
  speed = 0.0

  def loadImages(self):
    self.image = self.pygame.image.load(self.image)

  def draw(self, windowHeight):
    if self.y + self.height + self.speed <= windowHeight:
      self.surface.blit(self.image, (self.x, self.y))

  def move(self, windowHeight):
    if self.y + self.height + self.speed <= windowHeight:
      self.y += self.speed

  def checkForHit(self, thingToCheckAgainst):
    if self.x > thingToCheckAgainst.x and self.x < thingToCheckAgainst.x + thingToCheckAgainst.width:
      if self.y > thingToCheckAgainst.y and self.y < thingToCheckAgainst.y + thingToCheckAgainst.height:
        thingToCheckAgainst.registerHit()
        return True

    return False

  def __init__(self, x, y, pygame, surface, speed, image):
    self.x = x
    self.y = y
    self.pygame = pygame
    self.surface = surface
    self.image = image
    self.loadImages()
    self.speed = speed

    dimensions = self.image.get_rect().size
    self.width = dimensions[0]
    self.height = dimensions[1]

    self.x -= self.width / 2