import pygame, sys, random, math
import pygame.locals as GAME_GLOBALS
import pygame.event as GAME_EVENTS
import pygame.time as GAME_TIME
import ships

import gameLevels

windowWidth = 1024
windowHeight = 614
timeTick = 0

pygame.init()
pygame.font.init()
clock = pygame.time.Clock()
surface = pygame.display.set_mode((windowWidth, windowHeight), pygame.FULLSCREEN|pygame.HWSURFACE|pygame.DOUBLEBUF)

pygame.display.set_caption('Alien\'s Are Gonna Kill Me!')
textFont = pygame.font.SysFont("monospace", 50)

gameStarted = False
gameStartedTime = 0
gameFinishedTime = 0
gameOver = False
gameWon = False

currentLevel = 0
currentWave = 0
lastSpawn = 0
nextLevelTS = 0

#Mouse Variables
mousePosition = (0,0)
mouseStates = None
mouseDown = False

#Image Variables
startScreen = pygame.image.load("assets/start_screen.png")
background = pygame.image.load("assets/background.png")
loseScreen = pygame.image.load("assets/lose_screen.png")
winScreen = pygame.image.load("assets/win_screen.png")
nextWave = pygame.image.load("assets/next_level.png")
finalWave = pygame.image.load("assets/final_level.png")

#Ships
ship = ships.Player(windowWidth / 2, windowHeight, pygame, surface)
enemyShips = []

leftOverBullets = []

#Sound Setup
pygame.mixer.init()

def launchWave():

  global lastSpawn, currentWave, currentLevel, gameOver, gameWon, nextLevelTS

  thisLevel = gameLevels.level[currentLevel]["structure"]

  if currentWave < len(thisLevel):

    thisWave = thisLevel[currentWave]

    for idx, enemyAtThisPosition in enumerate(thisWave):
      if enemyAtThisPosition is 1:
        enemyShips.append(ships.Enemy(((windowWidth / len(thisWave)) * idx), -60, pygame, surface, 1))

  elif currentLevel + 1 < len(gameLevels.level) :
    currentLevel += 1
    currentWave = 0
    ship.shields = ship.maxShields
    nextLevelTS = timeTick + 5000
  else:
    gameWon = True

  lastSpawn = timeTick
  currentWave += 1

def updateGame():

  global mouseDown, gameOver, gameWon, leftOverBullets

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
        gameWon = False
        return

    else:
      enemiesToRemove.append(idx)

  oC = 0

  for idx in enemiesToRemove:
    for remainingBullets in enemyShips[idx - oC].bullets:
      leftOverBullets.append(remainingBullets)

    del enemyShips[idx - oC]
    oC += 1

  oC = 0

  for idx, aBullet in enumerate(leftOverBullets):
      aBullet.move()
      hitShip = aBullet.checkForHit(ship)

      if hitShip is True or aBullet.y > windowHeight:
        del leftOverBullets[idx - oC]
        oC += 1

def drawGame():

    global leftOverBullets, nextLevelTS, timeTick, gameWon

    surface.blit(background, (0, 0))
    ship.draw()
    ship.drawBullets()

    for aBullet in leftOverBullets:
      aBullet.draw()

    healthColor = [(62, 180, 76), (180, 62, 62)]
    whichColor = 0

    if(ship.health <= 1):
      whichColor = 1

    for enemy in enemyShips:
      enemy.draw()
      enemy.drawBullets()

    pygame.draw.rect(surface, healthColor[whichColor], (0, windowHeight - 5, (windowWidth / ship.maxHealth) * ship.health, 5))
    pygame.draw.rect(surface, (62, 145, 180), (0, windowHeight - 10, (windowWidth / ship.maxShields) * ship.shields, 5))

    if timeTick < nextLevelTS:
      if gameWon is True:
        surface.blit(finalWave, (250, 150))
      else:
        surface.blit(nextWave, (250, 150))

def restartGame():
  global gameOver, gameStart, currentLevel, currentWave, lastSpawn, nextLevelTS, leftOverBullets, gameWon, enemyShips, ship

  gameOver = False
  gameWon = False
  currentLevel = 0 
  currentWave = 0
  lastSpawn = 0
  nextLevelTS = 0
  leftOverBullets = []
  enemyShips = []
  ship.health = ship.maxHealth
  ship.shields = ship.maxShields
  ship.bullets = []

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
        pygame.mouse.set_visible(False)
        gameStarted = True

    elif mouseStates[0] is 0 and mouseDown is True:
      mouseDown = False

  elif gameStarted is True and gameOver is True and gameWon is False:
    surface.blit(loseScreen, (0, 0))
    timeLasted = (gameFinishedTime - gameStartedTime) / 1000
  
  if gameStarted is True and gameWon is True and len(enemyShips) is 0:
    surface.blit(winScreen, (0, 0))

  # Handle user and system events 
  for event in GAME_EVENTS.get():

    if event.type == pygame.KEYDOWN:

      if event.key == pygame.K_ESCAPE:
        quitGame()

      if event.key == pygame.K_SPACE:
        if gameStarted is True and gameOver is True or gameStarted is True and gameWon is True:
          restartGame()

  if timeTick - lastSpawn > gameLevels.level[currentLevel]["interval"] * 1000 and gameStarted is True and gameOver is False:
    launchWave()

  if event.type == GAME_GLOBALS.QUIT:
    quitGame()
  
  clock.tick(60)
  pygame.display.update()
