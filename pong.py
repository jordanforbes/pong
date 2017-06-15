import pygame, sys
from pygame.locals import *

# number of frames per second 
# slows down or speeds up the game 
FPS = 200

#global variables
WINDOWWIDTH = 400
WINDOWHEIGHT = 300
LINETHICKNESS = 10
PADDLESIZE = 50
PADDLEOFFSET = 20

#set up the colors
BLACK	=(0, 0, 0)
WHITE 	=(255, 255, 255)

#draws arena
def drawArena():
	DISPLAYSURF.fill((0,0,0))
	#draw outline of arena
	pygame.draw.rect(DISPLAYSURF, WHITE, ((0,0), (WINDOWWIDTH, WINDOWHEIGHT)), LINETHICKNESS * 2)
	#draw center line
	pygame.draw.line(DISPLAYSURF, WHITE, ((WINDOWWIDTH/2),0),((WINDOWWIDTH/2), WINDOWHEIGHT), (LINETHICKNESS/4))

#draws paddle
def drawPaddle(paddle):
	#stops paddle moving too low
	if paddle.bottom >WINDOWHEIGHT - LINETHICKNESS:
		paddle.bottom = WINDOWHEIGHT - LINETHICKNESS
	#stops paddle moving too high
	elif paddle.top <LINETHICKNESS :
		paddle.top = LINETHICKNESS
	#draws paddle
	pygame.draw.rect(DISPLAYSURF, WHITE, paddle)

#draws ball
def drawBall(ball):
	pygame.draw.rect(DISPLAYSURF, WHITE, ball)

#moves ball returns new position
def moveBall(ball, ballDirX, ballDirY):
	ball.x += ballDirX
	ball.y += ballDirY
	return ball

#checks for a new collision with a wall and bounces off of it 
#returns new direction
def checkEdgeCollision(ball, ballDirX, ballDirY):
	if ball.top == (LINETHICKNESS) or ball.bottom == (WINDOWHEIGHT - LINETHICKNESS):
		ballDirY = ballDirY * -1
	if ball.left ==(LINETHICKNESS) or ball.right ==(WINDOWWIDTH - LINETHICKNESS):
		ballDirX = ballDirX * -1
	return ballDirX, ballDirY

#collision with paddle
def checkHitBall(ball, paddle1, paddle2, ballDirX):
	if ballDirX == -1 and paddle1.right == ball.left and paddle1.top < ball.top and paddle1.bottom > ball.bottom:
		return -1
	elif ballDirX == 1 and paddle2.right == ball.right and paddle2.top < ball.top and paddle2.bottom > ball.bottom:
		return -1
	else: return 1


#artificial intelligence
def artificialIntelligence(ball, ballDirX, paddle2):
	#if ball is moving away from paddle, center bat
	if ballDirX == -1:
		if paddle2.centery < (WINDOWHEIGHT/2):
			paddle2.y += 1
		elif paddle2.centery > (WINDOWHEIGHT/2):
			paddle2.y -= 1
	#if ball moving towards bat, track its movement
	elif ballDirX == 1:
		if paddle2.centery < ball.centery:
			paddle2.y +=1
		else:
			paddle2.y -=1
	return paddle2


#main function 

def main():
	pygame.init()
	global DISPLAYSURF

	FPSCLOCK = pygame.time.Clock()
	DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
	pygame.display.set_caption('pong')

	#initiate variables and starting positions
	#any future changes made within rectangles
	ballX = WINDOWWIDTH/2 - LINETHICKNESS/2
	ballY = WINDOWHEIGHT/2 - LINETHICKNESS/2
	playerOnePosition = (WINDOWHEIGHT - PADDLESIZE) /2
	playerTwoPosition = (WINDOWHEIGHT - PADDLESIZE) /2

	#keeps track of ball direction
	ballDirX = -1 ## -1 =  left, 1 = right
	ballDirY = -1 ## -1 = up, 1 = down

	#creates rectangles for Paddles
	paddle1 = pygame.Rect(PADDLEOFFSET,playerOnePosition, LINETHICKNESS, PADDLESIZE)
	paddle2 = pygame.Rect(WINDOWWIDTH-PADDLEOFFSET-LINETHICKNESS,playerTwoPosition, LINETHICKNESS, PADDLESIZE)
	ball = pygame.Rect(ballX, ballY, LINETHICKNESS, LINETHICKNESS)


	drawArena()
	drawPaddle(paddle1)
	drawPaddle(paddle2)
	drawBall(ball)

	pygame.mouse.set_visible(0) #make cursor invisible

	while True: #main game loop
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			#mouse move commands
			elif event.type == MOUSEMOTION:
				mousex, mousey = event.pos
				paddle1.y = mousey

		drawArena()
		drawPaddle(paddle1)
		drawPaddle(paddle2)
		drawBall(ball)

		ball = moveBall(ball, ballDirX, ballDirY)
		ballDirX, ballDirY = checkEdgeCollision(ball, ballDirX, ballDirY)
		ballDirX = ballDirX * checkHitBall(ball, paddle1, paddle2, ballDirX)
		paddle2 = artificialIntelligence (ball,ballDirX, paddle2)

		pygame.display.update()
		FPSCLOCK.tick(FPS)

if __name__=='__main__':
	main()