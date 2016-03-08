import pygame, sys, random, math
import pygame.locals as GAME_GLOBALS
import pygame.event as GAME_EVENTS
import pygame.time as GAME_TIME
import ships

windowWidth = 1024
windowHeight = 614

pygame.init()
pygame.font.init()
clock = pygame.time.Clock()
surface = pygame.display.set_mode((windowWidth, windowHeight))

pygame.display.set_caption('Alien\'s Are Gonna Kill Me!')
textFont = pygame.font.SysFont("monospace", 50)

gameStarted = False
gameStartedTime = 0
gameFinishedTime = 0
gameOver = False

#Mouse Variables
mousePosition = (0,0)
mouseStates = None
mouseDown = False

#Image Variables
startScreen = pygame.image.load("assets/start_screen.png")
background = pygame.image.load("assets/background.png")

#Ships
ship = ships.Player(windowWidth / 2, windowHeight, pygame, surface)
enemyShips = []

lastEnemyCreated = 0
enemyInterval = random.randint(1000, 2500)

#Sound Setup
pygame.mixer.init()

def updateGame():

  global mouseDown, gameOver

  if mouseStates[0] is 1 and mouseDown is False:
    ship.fire()
    mouseDown = True
  elif mouseStates[0] is 0 and mouseDown is True:
    mouseDown = False

  ship.setPosition(mousePosition)

  enemiesToRemove = []

  for idx, enemy in enumerate(enemyShips):

    if enemy.y < windowHeight:
      enemy.move()
      enemy.tryToFire()
      shipIsDestroyed = enemy.checkForHit(ship)
      enemyIsDestroyed = ship.checkForHit(enemy)

      if enemyIsDestroyed is True:
        enemiesToRemove.append(idx)

      if shipIsDestroyed is True:
        gameOver = True
        print "\n\n\nYou Died\n\n\n"
        quitGame()

    else:
      enemiesToRemove.append(idx)

  for idx in enemiesToRemove:
    del enemyShips[idx]

def drawGame():
    surface.blit(background, (0, 0))
    ship.draw()
    ship.drawBullets()

    for enemy in enemyShips:
      enemy.draw()
      enemy.drawBullets()

def quitGame():
  pygame.quit()
  sys.exit()

# 'main' loop
while True:

  timeTick = GAME_TIME.get_ticks()
  mousePosition = pygame.mouse.get_pos()
  mouseStates = pygame.mouse.get_pressed()

  if gameStarted is True and gameOver is False:

    updateGame()
    drawGame()

  elif gameStarted is False and gameOver is False:
    surface.blit(startScreen, (0, 0))

    if mouseStates[0] is 1:

      if mousePosition[0] > 445 and mousePosition[0] < 580 and mousePosition[1] > 450 and mousePosition[1] < 510:

        gameStarted = True

    elif mouseStates[0] is 0 and mouseDown is True:
      mouseDown = False

  elif gameStarted is True and gameOver is True:
    surface.blit(startScreen, (0, 0))
    timeLasted = (gameFinishedTime - gameStartedTime) / 1000

  # Handle user and system events 
  for event in GAME_EVENTS.get():

    if event.type == pygame.KEYDOWN:

      if event.key == pygame.K_ESCAPE:
        quitGame()

  if GAME_TIME.get_ticks() - lastEnemyCreated > enemyInterval and gameStarted is True:
    enemyShips.append(ships.Enemy(random.randint(0, windowWidth), -60, pygame, surface, 1))
    lastEnemyCreated = GAME_TIME.get_ticks()

  if event.type == GAME_GLOBALS.QUIT:
    quitGame()
 
  clock.tick(60)
  pygame.display.update()
