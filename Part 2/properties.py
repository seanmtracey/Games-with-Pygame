import pygame, sys, random
import pygame.locals as GAME_GLOBALS
import pygame.event as GAME_EVENTS

pygame.init()
clock = pygame.time.Clock()

windowWidth = 640
windowHeight = 480

surface = pygame.display.set_mode((windowWidth, windowHeight))

pygame.display.set_caption('Pygame Shapes!')

# Code block 1 variables

rectX = windowWidth / 2
rectY = windowHeight / 2
rectWidth = 50
rectHeight = 50

# Code block 2 variables

squaresRed = random.randint(0, 255)
squaresBlue = random.randint(0, 255)
squaresGreen = random.randint(0, 255)

while True:

	surface.fill((0,0,0))

	# Code block 1

	pygame.draw.rect(surface, (255,255,0), (rectX - rectWidth / 2, rectY - rectHeight / 2, rectWidth, rectHeight))

	rectWidth -= 1
	rectHeight -= 1

	#Code block 2
	'''
	pygame.draw.rect(surface, (squaresRed, squaresGreen, squaresBlue), (50, 50, windowWidth / 2, windowHeight / 2))

	if squaresRed >= 255:
		squaresRed = random.randint(0, 255)
	else:
		squaresRed += 1

	if squaresGreen >= 255:
		squaresGreen = random.randint(0, 255)
	else:
		squaresGreen += 1

	if squaresBlue >= 255:
		squaresBlue = random.randint(0, 255)
	else:
		squaresBlue += 1
	'''

	for event in GAME_EVENTS.get():

		if event.type == GAME_GLOBALS.QUIT:

			pygame.quit()

			sys.exit()

	clock.tick(60)
	pygame.display.update()
