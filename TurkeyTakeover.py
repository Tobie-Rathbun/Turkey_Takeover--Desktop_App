#created by Tobie Rathbun @thispaghetti
#MIT Licensed, feel free to work with this

#import libraries
import pygame
import random
from os import path

#screen property initial variables
fps = 30
	#frames per second
height = 540
	#screen width (16:9 resolution)

#screen property functions

##height
def getWidth():
	#gets height from width
	width = int(height * 16 / 9)
		#keeps ratio at 16:9
	return width
width = getWidth()
def getPlayerSize():
	#gets playerSize from width
	playerSize = int(width / 8)
	return playerSize
playerSize = getPlayerSize()	
##floor
def getFloor():
	#gets height of the floor from height
	floorHeight = int(height * 2 / 9)
		#floor height variable
	floor = height - floorHeight - int(playerSize/2)
		#defines the floor
	return floor
floor = getFloor()
##left side 
def getLeftSide():
	#gets left side wall from width
	leftSideWidth = width / 200
	lSide = leftSideWidth
	return lSide
lSide = getLeftSide()
	#where character is placed
def getCenterX():
	#gets centerX from width
	centerX = width/2
	return centerX
centerX = getCenterX()
def getCenterY():
	#gets centerY from height
	centerY = height/2
	return centerY
centerY = getCenterY()
def getJumpAccel():
	localJumpAccel = 5 + height / 60
	return localJumpAccel
jumpAccel = getJumpAccel()
def getGravity():
	localGravity = .098
	return localGravity	
getGravity = getGravity()
def getGunSize():
	gunSize = int(playerSize*2)
	return gunSize
gunSize = getGunSize()
def getShotgun():
	placement = height / 60
	return placement
shotgunShift = getShotgun()

#initializes pygame
pygame.init()
#initial pygame information
pygame.display.set_caption("Turkey Takover")
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

	
#define colors
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)


#import folders
img_dir = path.join(path.dirname(__file__), 'img') 



icon_dir = path.join(path.dirname(__file__), 'img/icon')
icon = pygame.image.load(path.join(icon_dir, "turkeyIcon.png")).convert()
icon.set_colorkey(white)
pygame.display.set_icon(icon)

def playerScale(image):
	#scales to player size
	scaledPlayer = pygame.transform.scale(image, (playerSize,playerSize))
	return scaledPlayer
	
def bgScale(image):
	#scales to bg size
	scaledBG = pygame.transform.scale(image, (width,height))
	return scaledBG


#loading turkey images
turkey_dir = path.join(path.dirname(__file__), 'img/turkey')
turkeyRunning1 = pygame.image.load(path.join(turkey_dir, "turkeyRunning1.png")).convert()
turkeyRunning2 = pygame.image.load(path.join(turkey_dir, "turkeyRunning2.png")).convert()
turkeyFlying1 = pygame.image.load(path.join(turkey_dir, "turkeyFlying1.png")).convert()
turkeyRunning1.set_colorkey(white)
turkeyRunning2.set_colorkey(white)
turkeyFlying1.set_colorkey(white)

#rolling turkey images
turkeyRolling1 = pygame.image.load(path.join(turkey_dir, "turkeyRolling1.png")).convert()
turkeyRolling2 = pygame.image.load(path.join(turkey_dir, "turkeyRolling2.png")).convert()
turkeyRolling3 = pygame.image.load(path.join(turkey_dir, "turkeyRolling3.png")).convert()
turkeyRolling4 = pygame.image.load(path.join(turkey_dir, "turkeyRolling4.png")).convert()
turkeyRolling1.set_colorkey(white)
turkeyRolling2.set_colorkey(white)
turkeyRolling3.set_colorkey(white)
turkeyRolling4.set_colorkey(white)

#loading gun images
guns_dir = path.join(path.dirname(__file__), 'img/guns')
shotgun = pygame.image.load(path.join(guns_dir, "shotgun.png")).convert()
shotgun.set_colorkey(white)

#loading background images
bg_dir = path.join(path.dirname(__file__), 'img/bg')
bg = pygame.image.load(path.join(bg_dir, "bg.png")).convert()


#loading obstacle images
obstacle_dir = path.join(path.dirname(__file__), 'img/obstacles')
fenceImg = pygame.image.load(path.join(obstacle_dir, "fence.png")).convert()
fenceImg.set_colorkey(black)


class Background():
	def __init__(self):
		self.backgroundStart = 0
		self.backgroundX1 = self.backgroundStart
		self.backgroundX2 = width + self.backgroundX1
		self.bgMomentum = 4
		self.obstacleSpawn = width + 200
		self.fenceX = self.obstacleSpawn
		self.backgroundSized = bgScale(bg)
		self.fenceImg = playerScale(fenceImg)
		self.fenceImg.set_colorkey(black)
		self.fenceRect = self.fenceImg.get_rect()

	def _update(self):
		self.bgMomentum *= 1.0001
		if self.backgroundX2 > self.backgroundX1:
			self.backgroundX1 -= self.bgMomentum
			self.backgroundX2 = width + self.backgroundX1
		else:
			self.backgroundX2 -= self.bgMomentum
			self.backgroundX1 = width + self.backgroundX2
			
		if self.backgroundX1 < -width:
			self.backgroundX2 -= self.bgMomentum
			self.backgroundX1 = width + self.backgroundX2
		elif self.backgroundX2 < -width:
			self.backgroundX1 -= self.bgMomentum
			self.backgroundX2 = width + self.backgroundX1
		self.fenceX -= self.bgMomentum
		if self.fenceX < self.backgroundStart - playerSize:
			self.fenceX = self.obstacleSpawn
	def _draw(self):
		screen.blit(self.backgroundSized,(self.backgroundX1,0))
		screen.blit(self.backgroundSized,(self.backgroundX2,0))
		screen.blit(self.fenceImg,(self.fenceX,floor))


class Player():
	def __init__(self):
		#player position
		self.playerX = lSide
		self.playerY = centerY
		self.playerYacc = 0
		#jumping
		self.jumpCooldown = 0
		self.jumpCount = 0
		self.maxJumps = 3
		self.playerJumpAccel = jumpAccel
		#keystate reading
		self.lastKeyUp = 0
		self.lastKeyDown = 0
		#diving
		self.diveCount = 0
		self.maxDives = 1
		#gravity
		self.gravityVar = getGravity
		self.gravity = self.gravityVar
		#rolling
		self.rollCounter = 0
		self.turkeyRolling1 = playerScale(turkeyRolling1)
		self.playerRoll = self.turkeyRolling1
		self.hideGun = 0
		#scaling
		self.player = playerScale(turkeyRunning1)
		self.playerJump = playerScale(turkeyFlying1)
		self.shotgun = playerScale(shotgun)
		self.playerRolling1 = playerScale(turkeyRolling1)
		self.playerRolling2 = playerScale(turkeyRolling2)
		self.playerRolling3 = playerScale(turkeyRolling3)
		self.playerRolling4 = playerScale(turkeyRolling4)
		
		
	def _update(self):
		#player touching floor
		if self.playerY >= floor:
			self.gravityVar = getGravity
			self.gravity = self.gravityVar
			self.jumpCount = self.maxJumps
			self.diveCount = self.maxDives
			self.playerYacc = 0
			self.playerY = floor
			#rolling cycle
			if self.lastKeyDown > 0:
				#if player is pressing down
				#counts the roll
				self.rollCounter += .5
				if self.rollCounter == 1:
					self.playerRoll = self.playerRolling1
				if self.rollCounter == 2:
					self.playerRoll = self.playerRolling2
				if self.rollCounter == 3:
					self.playerRoll = self.playerRolling3
				if self.rollCounter == 4:
					self.playerRoll = self.playerRolling4
					self.rollCounter = 0
		else:
		#not touching floor
			#diving
			if self.diveCount > 0:
				#checks number of maxDives left
				if 0 < self.lastKeyDown < 2:
					#if down is pressed without diving
						self.diveCount -= 1
							#dive is counted
						self.playerYacc = -self.playerJumpAccel*2
							#player acceleration is adjusted
			if self.lastKeyDown > 2:
				#checks if holding down
				self.gravityVar = int(self.gravityVar * 1.33)
			else:
				self.gravityVar = getGravity
			self.gravity += self.gravityVar
		
			
		#jumping
		if self.jumpCooldown < 1:
			#if not already jumping
			if self.jumpCount > 0:
				#if there are available maxJumps left
				if 0 < self.lastKeyUp < 2:
					#if up is pressed
					self.jumpCount -= 1	
						#counts the jump
					self.gravity = self.gravityVar
					self.playerYacc = self.playerJumpAccel
						#adjust acceleration upwards
					self.jumpCooldown = 10
						#begin countdown that limits next jump
		#gliding
		if self.lastKeyUp > 17:
			self.gravity = .0098
		else:
			self.gravityVar = getGravity
		#jump countdown
		if self.jumpCooldown > 0:				
			self.jumpCooldown -= 1
		


		
		
			
		#key reading
		self.keystate = pygame.key.get_pressed()
			
		#up counter
		if self.keystate[pygame.K_UP]:
			#checks if the up arrow is being pressed
			self.lastKeyUp += 1
					#counts how many frames up has been pressed
		else:
			self.lastKeyUp = 0
				#sets counter to 0 if nothing was pressed
				
		#down counter
		if self.keystate[pygame.K_DOWN]:
			#checks if the up arrow is being pressed
				self.lastKeyDown += 1
					#counts how many frames up has been pressed
		else:
			self.lastKeyDown = 0
				#sets counter to 0 if nothing was pressed
				
		
			
		
		
		
		
		
		self.playerYacc -= self.gravity
				#player acceleration is affected by gravity		
		self.playerY -= self.playerYacc	
			#player position is affected by player acceleration
			
			
		if self.playerY > floor:
			self.playerY = floor
			
		
		
		
	def _draw(self):
		print("gravity:", self.gravity," yAcc:", self.playerYacc, " gravity var:", self.gravityVar)
		#rolling
		if self.playerY >= floor:
			#if player is on the floor
			if self.lastKeyDown > 0:
				#if player is pressing down
				screen.blit(self.playerRoll,(self.playerX,self.playerY))
					#draws rolling character
			else:
				screen.blit(self.player,(self.playerX,self.playerY))
		else:
			#if player is off of the floor
			screen.blit(self.playerJump,(self.playerX,self.playerY))
				#draw walking player
		if self.lastKeyDown < 1:
			#draws shotgun on player
			screen.blit(self.shotgun,(self.playerX + shotgunShift,self.playerY))

#pygame class variables
player = Player()
background = Background()


#game loop
running = True
	#set running to false to end game
while running:
	#keep loop running at right speed
	clock.tick(fps)
	#process input
	for event in pygame.event.get():
		#check for closing window
		if event.type == pygame.QUIT:
			running = False
	keystate = pygame.key.get_pressed()
	if keystate[pygame.K_ESCAPE]:		
		running = False
	#update
	player._update()
	background._update()
	
	#draw render
	background._draw()
	player._draw()
	#after drawing, flips to the next frame
	pygame.display.flip()


pygame.quit()
