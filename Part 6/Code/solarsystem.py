import pygame, copy

images = {
	"mercury" : pygame.image.load("assets/mercury.png"),
	"venus" : pygame.image.load("assets/venus.png"),
	"earth" : pygame.image.load("assets/earth.png"),
	"mars" : pygame.image.load("assets/mars.png"),
	"jupiter" : pygame.image.load("assets/jupiter.png"),
	"saturn" : pygame.image.load("assets/saturn.png"),
	"neptune" : pygame.image.load("assets/neptune.png"),
	"uranus" : pygame.image.load("assets/uranus.png"),
}

planets = [{
	"name" : "mercury",
	"radius" : 15.0,
	"mass" : 0.6,
	"velocity" : [0,0],
	"position" : [0,0]
},
{
	"name" : "venus",
	"radius" : 23.0,
	"mass" : 0.95,
	"velocity" : [0,0],
	"position" : [0,0]
},
{
	"name" : "earth",
	"radius" : 24.0,
	"mass" : 1.0,
	"velocity" : [0,0],
	"position" : [0,0]
},
{
	"name" : "mars",
	"radius" : 15.0,
	"mass" : 0.4,
	"velocity" : [0,0],
	"position" : [0,0]
},
{
	"name" : "jupiter",
	"radius" : 37.0,
	"mass" : 15.0,
	"velocity" : [0,0],
	"position" : [0,0]
},
{
	"name" : "saturn",
	"radius" : 30.0,
	"mass" : 4,
	"velocity" : [0,0],
	"position" : [0,0]
},
{
	"name" : "neptune",
	"radius" : 30.0,
	"mass" : 4.2,
	"velocity" : [0,0],
	"position" : [0,0]
},
{
	"name" : "uranus",
	"radius" : 30.0,
	"mass" : 3.8,
	"velocity" : [0,0],
	"position" : [0,0]
}]

def makeNewPlanet(which):

	for pieceOfRock in planets:

		if pieceOfRock["name"] == which:
			return copy.deepcopy(pieceOfRock)

	return False

