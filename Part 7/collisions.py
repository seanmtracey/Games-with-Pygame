import pygame, sys, random, math
import pygame.locals as GAME_GLOBALS
import pygame.event as GAME_EVENTS
import pygame.time as GAME_TIME

windowWidth = 1024
windowHeight = 768

pygame.init()
clock = pygame.time.Clock()
surface = pygame.display.set_mode((windowWidth, windowHeight))

pygame.display.set_caption('Collisions')

previousMousePosition = [0,0]
mousePosition = None
mouseDown = False

collidables = []
currentObject = None
expanding = True

drawAttractions = False

gravity = 1.0

def drawCollidables():

	for anObject in collidables:
		anObject["position"][0] += anObject["velocity"][0]
		anObject["position"][1] += anObject["velocity"][1]

		pygame.draw.circle(surface, (255,255,255), (int(anObject["position"][0]), int(anObject["position"][1])), int(anObject["radius"]), 0)

def drawCurrentObject():

	global expanding, currentObject

	currentObject["position"][0] = mousePosition[0]
	currentObject["position"][1] = mousePosition[1]

	if expanding is True and currentObject["radius"] < 30:
		currentObject["radius"] += 0.2

		if currentObject["radius"] >= 30:
			expanding = False
			currentObject["radius"] = 9.9

	elif expanding is False and currentObject["radius"] > 1:
		currentObject["radius"] -= 0.2

		if currentObject["radius"] <= 1:
			expanding = True
			currentObject["radius"] = 1.1

	currentObject["mass"] = currentObject["radius"]

	pygame.draw.circle(surface, (255,0,0), (int(currentObject["position"][0]), int(currentObject["position"][1])), int(currentObject["radius"]), 0)

def calculateMovement():

	for anObject in collidables:

		for theOtherObject in collidables:

			if anObject is not theOtherObject:
				
				direction = (theOtherObject["position"][0] - anObject["position"][0], theOtherObject["position"][1] - anObject["position"][1]) 
				magnitude = math.hypot(theOtherObject["position"][0] - anObject["position"][0], theOtherObject["position"][1] - anObject["position"][1]) 
				nDirection = (direction[0] / magnitude, direction[1] / magnitude)

				if magnitude < 5:
					magnitude = 5
				elif magnitude > 15:
					magnitude = 15

				strength = ((gravity * anObject["mass"] * theOtherObject["mass"]) / (magnitude * magnitude)) / theOtherObject["mass"]

				appliedForce = (nDirection[0] * strength, nDirection[1] * strength)

				theOtherObject["velocity"][0] -= appliedForce[0]
				theOtherObject["velocity"][1] -= appliedForce[1]

				if drawAttractions is True:
					pygame.draw.line(surface, (255,255,255), (anObject["position"][0],anObject["position"][1]), (theOtherObject["position"][0],theOtherObject["position"][1]), 1)

def handleCollisions():

	h = 0

	while h < len(collidables):

		i = 0

		anObject = collidables[h]

		while i < len(collidables):

			otherObject = collidables[i]

			if anObject != otherObject:

				distance = math.hypot(otherObject["position"][0] - anObject["position"][0], otherObject["position"][1] - anObject["position"][1])

				if distance < otherObject["radius"] + anObject["radius"]:

					# First we get the angle of the collision between the two objects
					collisionAngle = math.atan2(anObject["position"][1] - otherObject["position"][1], anObject["position"][0] - otherObject["position"][0])

					#Then we need to calculate the speed of each object
					anObjectSpeed = math.sqrt(anObject["velocity"][0] * anObject["velocity"][0] + anObject["velocity"][1] * anObject["velocity"][1])
					theOtherObjectSpeed = math.sqrt(otherObject["velocity"][0] * otherObject["velocity"][0] + otherObject["velocity"][1] * otherObject["velocity"][1])

					# Now, we work out the direction of the objects in radians
					anObjectDirection = math.atan2(anObject["velocity"][1], anObject["velocity"][0])
					theOtherObjectDirection = math.atan2(otherObject["velocity"][1], otherObject["velocity"][0])

					# Now we calculate the new X/Y values of each object for the collision
					anObjectsNewVelocityX = anObjectSpeed * math.cos(anObjectDirection - collisionAngle)
					anObjectsNewVelocityY = anObjectSpeed * math.sin(anObjectDirection - collisionAngle)

					otherObjectsNewVelocityX = theOtherObjectSpeed * math.cos(theOtherObjectDirection - collisionAngle)
					otherObjectsNewVelocityY = theOtherObjectSpeed * math.sin(theOtherObjectDirection - collisionAngle)
					
					# We adjust the velocity based on the mass of the objects
					anObjectsFinalVelocityX = ((anObject["mass"] - otherObject["mass"]) * anObjectsNewVelocityX + (otherObject["mass"] + otherObject["mass"]) * otherObjectsNewVelocityX)/(anObject["mass"] + otherObject["mass"])
					otherObjectsFinalVelocityX = ((anObject["mass"] + anObject["mass"]) * anObjectsNewVelocityX + (otherObject["mass"] - anObject["mass"]) * otherObjectsNewVelocityX)/(anObject["mass"] + otherObject["mass"])

					# Now we set those values
					anObject["velocity"][0] = anObjectsFinalVelocityX
					otherObject["velocity"][0] = otherObjectsFinalVelocityX


			i += 1

		h += 1

def handleMouseDown():
	global currentObject

	currentObject = {
		"radius" : 3,
		"mass" : 3,
		"velocity" : [0,0],
		"position" : [0,0]
	}

def quitGame():
	pygame.quit()
	sys.exit()

# 'main' loop
while True:

	surface.fill((0,0,0))
	mousePosition = pygame.mouse.get_pos()

	# Handle user and system events 
	for event in GAME_EVENTS.get():

		if event.type == pygame.KEYDOWN:

			if event.key == pygame.K_ESCAPE:
				quitGame()

		if event.type == pygame.KEYUP:

			if event.key == pygame.K_r:
				collidables = []
			if event.key == pygame.K_a:
				if drawAttractions is True:
					drawAttractions = False
				elif drawAttractions is False:
					drawAttractions = True

		if event.type == pygame.MOUSEBUTTONDOWN:
			mouseDown = True
			handleMouseDown()

		if event.type == pygame.MOUSEBUTTONUP:
			mouseDown = False

		if event.type == GAME_GLOBALS.QUIT:
			quitGame()

	calculateMovement()
	handleCollisions()
	drawCollidables()

	if currentObject is not None:
		drawCurrentObject()

		# If our user has released the mouse, add the new anObject to the collidables list and let gravity do its thing
		if mouseDown is False:
			currentObject["velocity"][0] = (mousePosition[0] - previousMousePosition[0]) / 4
			currentObject["velocity"][1] = (mousePosition[1] - previousMousePosition[1]) / 4
			collidables.append(currentObject)
			currentObject = None

	# Store the previous mouse coordinates to create a vector when we release a new anObject
	previousMousePosition = mousePosition

	clock.tick(60)
	pygame.display.update()