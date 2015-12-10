import projectiles, random

class Player():

  x = 0
  y = 0
  firing = False
  image = None
  shieldImage = None
  drawShield = False
  soundEffect = 'sounds/player_laser.wav'
  pygame = None
  surface = None
  width = 0
  height = 0
  bullets = []
  bulletImage = "assets/you_pellet.png"
  bulletSpeed = -10
  health = 5
  maxHealth = health
  shields = 3
  maxShields = shields

  def loadImages(self):
    self.image = self.pygame.image.load("assets/you_ship.png")
    self.shieldImage = self.pygame.image.load("assets/shield2.png")

  def draw(self):
    self.surface.blit(self.image, (self.x, self.y))
    if self.drawShield == True:
      self.surface.blit(self.shieldImage, (self.x - 3, self.y - 2))
      self.drawShield = False

  def setPosition(self, pos):
    self.x = pos[0] - self.width / 2

  def fire(self):
    self.bullets.append(projectiles.Bullet(self.x + self.width / 2, self.y, self.pygame, self.surface, self.bulletSpeed, self.bulletImage))
    a = self.pygame.mixer.Sound(self.soundEffect)
    a.set_volume(0.2)
    a.play()

  def drawBullets(self):
    for b in self.bullets:
      b.move()
      b.draw()

  def registerHit(self):
    if self.shields == 0:
      self.health -= 1
    else :
      self.shields -= 1
      self.drawShield = True

  def checkForHit(self, thingToCheckAgainst):
    bulletsToRemove = []

    for idx, b in enumerate(self.bullets):
      if b.x > thingToCheckAgainst.x and b.x < thingToCheckAgainst.x + thingToCheckAgainst.width:
        if b.y > thingToCheckAgainst.y and b.y < thingToCheckAgainst.y + thingToCheckAgainst.height:
          thingToCheckAgainst.registerHit()
          bulletsToRemove.append(idx)
    bC = 0
    for usedBullet in bulletsToRemove:
      del self.bullets[usedBullet - bC]
      bC += 1

    if thingToCheckAgainst.health <= 0:
      return True

  def __init__(self, x, y, pygame, surface):
    self.x = x
    self.y = y
    self.pygame = pygame
    self.surface = surface
    self.loadImages()

    dimensions = self.image.get_rect().size
    self.width = dimensions[0]
    self.height = dimensions[1]

    self.x -= self.width / 2
    self.y -= self.height + 10

class Enemy(Player):

  x = 0
  y = 0
  firing = False
  image = None
  soundEffect = 'sounds/enemy_laser.wav'
  bulletImage = "assets/them_pellet.png"
  bulletSpeed = 10
  speed = 4
  shields = 0

  def move(self):
    self.y += self.speed

  def tryToFire(self):
    shouldFire = random.random()

    if shouldFire <= 0.01:
      self.fire()

  def loadImages(self):
    self.image = self.pygame.image.load("assets/them_ship.png")

  def __init__(self, x, y, pygame, surface, health):
    self.x = x
    self.y = y
    self.pygame = pygame
    self.surface = surface
    self.loadImages()
    self.bullets = []
    self.health = health

    dimensions = self.image.get_rect().size
    self.width = dimensions[0]
    self.height = dimensions[1]

    self.x += self.width / 2 