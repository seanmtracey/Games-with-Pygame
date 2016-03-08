import pygame, sys, random
import pygame.locals as GAME_GLOBALS
import pygame.event as GAME_EVENTS

pygame.init()
clock = pygame.time.Clock()

windowWidth = 640
windowHeight = 480

surface = pygame.display.set_mode((windowWidth, windowHeight))

pygame.display.set_caption('Pygame Shapes!')

squareX = 0
squareY = 0

#Code Block 2 Variables
greenSquareX = windowWidth / 2
greenSquareY = windowHeight / 2

#Code Block 3 Variables
blueSquareX = 0.0
blueSquareY = 0.0
blueSquareVX = 1
blueSquareVY = 1

while True:

	surface.fill((0,0,0))

	# Code block 1 - Drawing Shapes in Time and Space
	pygame.draw.rect(surface, (255,0,0), (random.randint(0, windowWidth), random.randint(0, windowHeight), 10, 10 ) )

	#Code Block 2 - Moving Shapes Across Space in Time
	'''
	pygame.draw.rect(surface, (0, 255, 0), (greenSquareX, greenSquareY, 10, 10))

	greenSquareX += 1
	#greenSquareY += 1
	'''
	#Code block 3 - Moving Shapes with Acceleration
	'''
	pygame.draw.rect(surface, (0, 0, 255), (blueSquareX, blueSquareY, 10, 10))

	blueSquareX += blueSquareVX
	blueSquareY += blueSquareVY

	blueSquareVX -= 0.2
	blueSquareVY += 0.1
	'''

	for event in GAME_EVENTS.get():

		if event.type == GAME_GLOBALS.QUIT:

			pygame.quit()

			sys.exit()

	clock.tick(60)
	pygame.display.update()
