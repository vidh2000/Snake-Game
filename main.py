import pygame
import time
import random
import csv

#initialise pygame
pygame.init()

#Screen window
screen_width = 500
screen_height = 500
edge = 0
window = pygame.display.set_mode((screen_width, screen_height)) 		# Draws a window

pygame.display.set_caption("Snake game") 								# displays a title of the window

# Objects

class Snake():

	totalLength = 20
	# Turns
	turn = False
	turnRD = False         	#Class method
	turnRU = False         	#Class method
	turnLD = False         	#Class method
	turnLU = False         	#Class method
	turnUR = False         	#Class method
	turnUL = False         	#Class method
	turnDR = False         	#Class method
	turnDL = False         	#Class method

	vel = 2 				#velocity
	def __init__(self, x, y, colour, direction):
		""" Direction is a string of "left, right, down, up"""
		self.x = x
		self.y = y
		self.width = 20
		self.length = 20
		self.left = False
		self.right = False
		self.up = False
		self.down = False
		self.colour = colour
		self.visible = True	
		self.direction = direction

		if self.direction == "left":
			self.left = True
		if self.direction == "right":
			self.right = True
		if self.direction == "up":
			self.up = True
		if self.direction == "down":
			self.down = True

		# Blocks position/turning/alligment
		if self.left:
			self.hitbox = (self.x, self.y, self.length, self.width)
		if self.right:
			self.x = x - self.length
			self.hitbox = (self.x, self.y, self.length, self.width) 		
		if self.up:
			self.hitbox = (self.x, self.y, self.width, self.length)
		if self.down:
			self.y = y - self.length
			self.hitbox = (self.x, self.y, self.width, self.length)

		# Head
		if self.right:
			self.head = (self.x, self.y, 0, self.width)
		if self.left:
			self.head = (self.x, self.y, 0, self.width)
		if self.up:
			self.head = (self.x, self.y, self.width, 0)
		if self.down:
			self.head = (self.x, self.y, self.width, 0)
		

	def draw(self):

		# Move by itself
		if self.right:
			self.x += self.vel
		if self.left:
			self.x -= self.vel
		if self.up:
			self.y -= self.vel
		if self.down:
			self.y += self.vel

		# Refreshing hitbox and snake
		if self.left:
			self.hitbox = (self.x, self.y, self.length, self.width)
		if self.right:
			self.hitbox = (self.x - self.length, self.y, self.length, self.width) 		# self.x - self.length
		if self.up:
			self.hitbox = (self.x, self.y, self.width, self.length)
		if self.down:
			self.hitbox = (self.x, self.y - self.length, self.width, self.length)  		# self.y - self.length   ponavljam line 55-65?

		# Head
		if self.right:
			self.head = (self.x, self.y, 0, self.width)
		if self.left:
			self.head = (self.x, self.y, 0, self.width)
		if self.up:
			self.head = (self.x, self.y, self.width, 0)
		if self.down:
			self.head = (self.x, self.y, self.width, 0)

		# Drawing
		
		# Body
		pygame.draw.rect(window, self.colour, self.hitbox)											# draws the snake
		#pygame.draw.rect(window, (0,255,0), self.hitbox, 2)											# draws snake's hitbox
		# Head
		#pygame.draw.rect(window, (0,0,255), self.head, 2)											# draws the head hitbox
		

class Apple(object):

	def __init__(self, x, y, colour, birthtime, lifetime):
		self.visible = False
		self.x = x
		self.y = y
		self.colour = colour
		self.birthtime = birthtime
		self.lifetime = lifetime
		self.hitbox = (self.x,self.y,20,20)
		self.timer = 0

	def draw(self):
		if self.visible:
			pygame.draw.circle(window, self.colour, (self.x, self.y), 10)									# draws the apple
			#pygame.draw.rect(window,(255,0,0), self.hitbox, 2)												# draws apple hitbox


# Updates the content displayed

def redraw_screen():

	window.fill((0,0,0))														# refreshes background
	for snake in snakes:
		snake.draw()															# redraws the snake

	for apple in apples:
		apple.draw()															# redraws apples

	window.blit(scoreText, (screen_width - scoreText.get_width() - 20, 20))		# redraws the score

	pygame.display.update()



# Fps stuff
fps = 60
clock = pygame.time.Clock()


# Objects on the screen
mamaSnake = Snake(screen_width/2, screen_height/2, (255,0,0), "right") 
snakes = [mamaSnake]					# list of snake object
apples = []																	# list of apple objects


# Main loop
lengthCount = Snake.totalLength
snakeCount = 0       							#because they are in lists with indices from 0
snakeTurnTimer = 0
score = 0
appleCount = 0
i = 0
run = True
while run:


	clock.tick(fps)																		# Game runs at fps
	
	if snakes[snakeCount].visible:

		# Timer
		for apple in apples:
			apple.timer += 1

		# Checks if snake is located on screen
		if snakes[snakeCount].x < screen_width and snakes[snakeCount].x > 0:
			if snakes[snakeCount].y < screen_height and snakes[snakeCount].y > 0:

				# Enables closing the window tab
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						run = False

				#Displaying score
				fontScore = pygame.font.SysFont("comicsanse", 30, True)					# Creates font
				scoreText = fontScore.render("Score: " + str(score), 1, (0,255,255))	# Tells what to display

				# If i click on keys it sends a command that the key was/is pressed
				keys = pygame.key.get_pressed()
				LEFT = keys[pygame.K_LEFT]
				RIGHT = keys[pygame.K_RIGHT]
				UP = keys[pygame.K_UP]
				DOWN = keys[pygame.K_DOWN]

				# Clicking on keys boosts the snake in the chosen direction
				boost = 2

				# Makes sure snake turns only once
				for snake in snakes:
					if snake.turn:
						snake.turn = False
						snake.turnRD = False         	#Class method
						snake.turnRU = False         	#Class method
						snake.turnLD = False         	#Class method
						snake.turnLU = False         	#Class method
						snake.turnUR = False         	#Class method
						snake.turnUL = False         	#Class method
						snake.turnDR = False         	#Class method
						snake.turnDL = False         	#Class method
					
				# Controls
				
				# Disables LEFT when going right etc
				if snakes[snakeCount].right:
					if LEFT:
						pass
				if snakes[snakeCount].left:
					if RIGHT:
						pass
				if snakes[snakeCount].up:
					if DOWN:
						pass
				if snakes[snakeCount].down:
					if UP:
						pass

				# Makes sure pressing more buttons doesn't affect anything
				if DOWN and LEFT:
					pass
				if DOWN and RIGHT:
					pass
				if UP and LEFT:
					pass
				if UP and RIGHT:
					pass
				if UP:
					if LEFT and RIGHT:
						pass
				if DOWN:
					if LEFT and RIGHT:
						pass

				# Checks if snake is turning and that it doesn't turn too quickly
				if snakeTurnTimer > 20:
					if snakes[snakeCount].up:
						if LEFT:
							snakes[snakeCount].turn = True
							snakes[snakeCount].turnUL = True
							
						if RIGHT:
							snakes[snakeCount].turn = True
							snakes[snakeCount].turnUR = True

					if snakes[snakeCount].down:
						if LEFT:
							snakes[snakeCount].turn = True
							snakes[snakeCount].turnDL = True

						if RIGHT:
							snakes[snakeCount].turn = True
							snakes[snakeCount].turnDR = True

					if snakes[snakeCount].right:
						if UP:
							snakes[snakeCount].turn = True
							snakes[snakeCount].turnRU = True

						if DOWN:
							snakes[snakeCount].turn = True
							snakes[snakeCount].turnRD = True

					if snakes[snakeCount].left:
						if UP:
							snakes[snakeCount].turn = True
							snakes[snakeCount].turnLU = True

						if DOWN:
							snakes[snakeCount].turn = True
							snakes[snakeCount].turnLD = True
					snakeTurnTimer = 0

				# Adds counter of snakes +1 after a turn
				if snakes[snakeCount].turn:
					snakeCount += 1

				# What to do if it is turning
				for snake in snakes:
					if snake.turn:
						if snake.turnRU:
							# Makes a new snake('s head)
							snakes.append(Snake(snakes[snakeCount-1].x - snakes[snakeCount-1].width, snakes[snakeCount-1].y, (255,0,0), "up"))
							# Sets new snake's length to 0
							snakes[snakeCount].length = 20
							# Tail
							snakes[snakeCount-1].vel = 0
							snakes[snakeCount-1].head = (0,0,0,0)

						if snake.turnRD:
							# Makes a new snake('s head)
							snakes.append(Snake(snakes[snakeCount-1].x - snakes[snakeCount-1].width, snakes[snakeCount-1].y + 2* snakes[snakeCount-1].width, (255,0,0), "down"))
							# Sets new snake's length to 0
							snakes[snakeCount].length = 20
							# Tail
							snakes[snakeCount-1].vel = 0
							snakes[snakeCount-1].head = (0,0,0,0)

						if snake.turnLU:
							# Makes a new snake('s head)
							snakes.append(Snake(snakes[snakeCount-1].x, snakes[snakeCount-1].y, (255,0,0), "up"))
							# Sets new snake's length to 0
							snakes[snakeCount].length = 20
							# Tail
							snakes[snakeCount-1].vel = 0
							snakes[snakeCount-1].head = (0,0,0,0)
							
						if snake.turnLD:
							# Makes a new snake('s head)
							snakes.append(Snake(snakes[snakeCount-1].x, snakes[snakeCount-1].y + 2 * snakes[snakeCount-1].width, (255,0,0), "down"))
							# Sets new snake's length to 0
							snakes[snakeCount].length = 20
							# Tail
							snakes[snakeCount-1].vel = 0
							snakes[snakeCount-1].head = (0,0,0,0)
						if snake.turnUL:
							# Makes a new snake('s head)
							snakes.append(Snake(snakes[snakeCount-1].x, snakes[snakeCount-1].y, (255,0,0), "left"))
							# Sets new snake's length to 0
							snakes[snakeCount].length = 20
							# Tail
							snakes[snakeCount-1].vel = 0
							snakes[snakeCount-1].head = (0,0,0,0)
						if snake.turnUR:
							# Makes a new snake('s head)
							snakes.append(Snake(snakes[snakeCount-1].x + 2* snakes[snakeCount-1].width, snakes[snakeCount-1].y, (255,0,0), "right"))
							# Sets new snake's length to 0
							snakes[snakeCount].length = 20
							# Tail
							snakes[snakeCount-1].vel = 0
							snakes[snakeCount-1].head = (0,0,0,0)
						if snake.turnDL:
							# Makes a new snake('s head)
							snakes.append(Snake(snakes[snakeCount-1].x, snakes[snakeCount-1].y - snakes[snakeCount-1].width, (255,0,0), "left"))
							# Sets new snake's length to 0
							snakes[snakeCount].length = 20
							# Tail
							snakes[snakeCount-1].vel = 0
							snakes[snakeCount-1].head = (0,0,0,0)
						if snake.turnDR:
							# Makes a new snake('s head)
							snakes.append(Snake(snakes[snakeCount-1].x + 2* snakes[snakeCount-1].width, snakes[snakeCount-1].y - snakes[snakeCount-1].width, (255,0,0), "right"))
							# Sets new snake's length to 0
							snakes[snakeCount].length = 20
							# Tail
							snakes[snakeCount-1].vel = 0
							snakes[snakeCount-1].head = (0,0,0,0)

				# Updates the head of the snake
				if snakes[snakeCount].length <= Snake.totalLength:
					snakes[snakeCount].length += Snake.vel
					
				# Updates the tail of the snake
				if len(snakes) != 1:
					if snakes[0].length > snakes[0].width:
						snakes[0].length -= Snake.vel
					else:
						snakes.pop(0)							# removes the tail
						snakeCount -= 1

				# What to do if it isn't turning
				if snakes[snakeCount].turn == False:
					if snakes[snakeCount].up:
						if UP:
							snakes[snakeCount].y -= boost
							if len(snakes) != 1:
								snakes[0].length -= boost
								snakes[snakeCount].length += boost
								# Disables doing turns before snake has travelled 1 width of the snake
								snakeTurnTimer += boost
							
					if snakes[snakeCount].down:
						if DOWN:
							snakes[snakeCount].y += boost
							if len(snakes) != 1:
								snakes[0].length -= boost
								snakes[snakeCount].length += boost
								# Disables doing turns before snake has travelled 1 width of the snake
								snakeTurnTimer += boost

					if snakes[snakeCount].right:
						if RIGHT:
							snakes[snakeCount].x += boost
							if len(snakes) != 1:
								snakes[0].length -= boost
								snakes[snakeCount].length += boost
								# Disables doing turns before snake has travelled 1 width of the snake
								snakeTurnTimer += boost
					if snakes[snakeCount].left:
						if LEFT:
							snakes[snakeCount].x -= boost
							if len(snakes) != 1:
								snakes[0].length -= boost
								snakes[snakeCount].length += boost
								# Disables doing turns before snake has travelled 1 width of the snake
								snakeTurnTimer += boost

				# Disables doing turns before snake has travelled 1 width of the snake
				snakeTurnTimer += snake.vel


				# Snake mustn't eat its tail

				for snake in snakes:
					if snakes.index(snake) != snakeCount:
						if snake.left:
							if snakes[snakeCount].head[0] > snake.hitbox[0] and snakes[snakeCount].head[0] < snake.hitbox[0] + snake.length:
								if snakes[snakeCount].head[1] > snake.hitbox[1] and snakes[snakeCount].head[1] < snake.hitbox[1] + snake.width:
									snakes[snakeCount].visible = False

						if snake.right:
							if snakes[snakeCount].head[0] > snake.hitbox[0] and snakes[snakeCount].head[0] < snake.hitbox[0] + snake.length:
								if snakes[snakeCount].head[1] > snake.hitbox[1] and snakes[snakeCount].head[1] < snake.hitbox[1] + snake.width:
									snakes[snakeCount].visible = False
						if snake.up:
							if snakes[snakeCount].head[0] > snake.hitbox[0] and snakes[snakeCount].head[0] < snake.hitbox[0] + snake.width:
								if snakes[snakeCount].head[1] > snake.hitbox[1] and snakes[snakeCount].head[1] < snake.hitbox[1] + snake.length:
									snakes[snakeCount].visible = False	
						if snake.down:
							if snakes[snakeCount].head[0] > snake.hitbox[0] and snakes[snakeCount].head[0] < snake.hitbox[0] + snake.width:
								if snakes[snakeCount].head[1] > snake.hitbox[1] and snakes[snakeCount].head[1] < snake.hitbox[1] + snake.length:
									snakes[snakeCount].visible = False	



				# If snake eats the apple, apple dissapears and snake grows
				for apple in apples:
					if snakes[len(snakes)-1].hitbox[0] + snakes[len(snakes)-1].hitbox[2] > apple.hitbox[0] and snakes[len(snakes)-1].hitbox[0] < apple.hitbox[0] + snakes[len(snakes)-1].width:
						if snakes[len(snakes)-1].hitbox[1] + snakes[len(snakes)-1].hitbox[3] > apple.hitbox[1] and snakes[len(snakes)-1].hitbox[1] < apple.hitbox[1] + snakes[len(snakes)-1].width:
							score += 10
							Snake.totalLength += 20
							snakes[0].length += 20
							apples.pop(apples.index(apple))
							appleCount -= 1


				#Lifetime of new apples
				while appleCount < 2:
					apples.append(Apple(int(random.uniform(20, screen_width - 20)), int(random.uniform(20, screen_height  - 20)), (255,255,255), random.uniform(1,5), random.uniform(5, 10)))
					appleCount += 1

				for apple in apples:
					if apple.timer > apple.birthtime * fps:
						apple.visible = True
						apple.hitbox = (apple.x - 10, apple.y - 10, 20, 20)
						
					if apple.timer > (apple.birthtime + apple.lifetime) * fps:
						apples.pop(apples.index(apple))
						appleCount -= 1

				redraw_screen()

			else: snakes[snakeCount].visible = False
		else:
			snakes[snakeCount].visible = False

	else:
		run = False

else:

	# GAME OVER final screen

	#Allows quitting during the GAME OVER screen       -       doesnt work?
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

	window.fill((0,0,0))
	pygame.display.update()


	# Highscores and previous scores

with open("Highscores.csv","a", newline='') as spreadsheet:
	spreadsheet = csv.writer(spreadsheet, delimiter = ',')
	spreadsheet.writerow([f'{score}'])

with open("Highscores.csv","r") as spreadsheet:
	reader = csv.reader(spreadsheet, delimiter = ',')
	sortedspreadsheet = sorted(reader, key = lambda row: int(row[0]), reverse = True)
	highscore = int(sortedspreadsheet[0][0])

	#Game Over text displayed
	fontFinal = pygame.font.SysFont("comicsanse", 80, True)
	fontFinalscore = pygame.font.SysFont("comicsanse", 40, True)
	gameOver = fontFinal.render("GAME OVER!", 1, (255,255,255))
	finalScore = fontFinalscore.render("FINAL SCORE: " + str(score), 1, (255, 0, 0))
	if score == highscore:	
		highScore = fontFinalscore.render(" NEW HIGH SCORE: " + str(highscore), 1, (255,0,0))
		window.blit(highScore, (screen_width/2 - highScore.get_width()/2, screen_height/2))
	else:
		highScore = fontFinalscore.render(" HIGH SCORE: " + str(highscore), 1, (0,255,0))
		window.blit(finalScore, (screen_width/2 - finalScore.get_width()/2, screen_height/2))
		window.blit(highScore, (screen_width/2 - highScore.get_width()/2, screen_height *2/3))
	
	window.blit(gameOver, (screen_width/2 - gameOver.get_width()/2, screen_height/3))

	pygame.display.update()

	#Quit game
	if not snakes[snakeCount].visible:
		time.sleep(3)
	pygame.quit()
