# Must install Python library PYGAME 
import pygame 
import sys 
import random 
# Initializations 
pygame.init()
pygame.font.init()
clock = pygame.time.Clock()
# =======================================================================
# WINDOW DECLARE 
resolution = [850, 550]
window = pygame.display.set_mode((resolution[0],resolution[1]))
pygame.display.set_caption("PONG!")
# =======================================================================
# ASSETS 
# color
WHITE = (230, 230, 230)
BLACK = (0,0,0)
GREEN = (0, 255, 0)
# font 
title_font = pygame.font.SysFont("monospace", 30)
score_font = pygame.font.SysFont("arial", 30)
label_font = pygame.font.SysFont("arial", 25)
pause_font = pygame.font.SysFont("arial", 130)
# =======================================================================
# DRAW FUNCTIONS 
def draw_borders(resolution):
	# Net
	pos_x = resolution[0]//2-4
	pos_y = 0
	while pos_y < resolution[1]:
		pygame.draw.rect(window, GREEN, (pos_x, pos_y, 7, 7))
		pos_y += 10

	# Horizontal border
	pygame.draw.rect(window, WHITE, (0, 0, resolution[0], 60))
	pygame.draw.rect(window, WHITE, (0, resolution[1] -34 , resolution[0], 34))
	# Vertical Border
	pygame.draw.rect(window, WHITE, (0, 0, 7, resolution[1]))
	pygame.draw.rect(window, WHITE, (resolution[0] -7, 0, 7, resolution[1]))

def draw_texts(p1_score, p2_score):
	title = title_font.render('"PONG" by Eugene Reyes!', 1, BLACK)
	window.blit(title, (230, 10))

	p1 = "SCORE: " + str(p1_score)
	p1 = score_font.render(p1, 1, GREEN)
	window.blit(p1, (285, 70))

	p2 = "SCORE: " + str(p2_score)
	p2 = score_font.render(p2, 1, GREEN)
	window.blit(p2, (440, 70)) 

	label_txt = label_font.render('Play: Spacebar', 1, BLACK)
	window.blit(label_txt, (10, 518))

	label_txt = label_font.render('Restart: Escape', 1, BLACK)
	window.blit(label_txt, (680, 518))

def pause_text():
	pause_txt = pause_font.render('PAUSE', 1, GREEN)
	window.blit(pause_txt, (255, 200))

def draw_player1(pos):
	return pygame.draw.rect(window, GREEN, (pos[0], pos[1], 7, 70))
def draw_player2(pos):	
	return pygame.draw.rect(window, GREEN, (pos[0], pos[1], 7, 70))
def draw_ball(pos):
	return pygame.draw.rect(window, GREEN, (pos[0], pos[1], 7, 7))	
# =======================================================================
# INGAME BACKEND
def restart():
	pass

# Player Movement 
move = 35
def p1_move(pos, key):
	if key == pygame.K_w and pos[1] - move > 60:
		pos[1] =  pos[1] - move
	elif key == pygame.K_s and pos[1] + 70 + move < resolution[1] - 7:
		pos[1] =  pos[1] + move
	return pos 
def p2_move(pos, key):
	if key == pygame.K_UP and pos[1] - move > 60:
		pos[1] =  pos[1] - move
	elif key == pygame.K_DOWN and pos[1] + 70 + move < resolution[1] - 7:
		pos[1] =  pos[1] + move
	return pos 

# Ball movement 
def ball_move(pos,dr,m):
	# linear equation formula : Ax + By = C or y = mx + b	
	x, y_intercept = pos[0], pos[1]
	if dr == 0:
		x -= 7
		y = int((m * x) + y_intercept)  
	else:
		x += 7
		y = int((m * x) + y_intercept)
	pos = [x,y]
	return pos
def detect_collision(pos, m, p1_score, p2_score, reset, p_collision, ball_dir):
	# Player Collision 
	p1_collide = p_collision[0].colliderect(p_collision[1])
	p2_collide = p_collision[0].colliderect(p_collision[2])
	if p1_collide:
		ball_dir = 1
		# Invert angle (horizontal/ wall surface)
		m = 45 + (m/ 0.001)
		m = ((90 - m)- 45 )*0.001
	if p2_collide:
		ball_dir = 0
		# Invert angle (horizontal/ wall surface)
		m = 45 + (m/ 0.001)
		m = ((90 - m)- 45 )*0.001


	# Scoring 
	if pos[0] >= 850 or pos[0] <= 0:
		if pos[0] >= 850:
			p1_score += 1 
		else:
			p2_score += 1
		reset = True
	# Wall collision
	if pos[1] <= 60 or pos[1] >= 509:
		# Invert angle (horizontal/ wall surface)
		m = 45 + (m/ 0.001)
		m = ((90 - m)- 45 )*0.001


		# Make a collision detection for players
	return p1_score, p2_score, reset, m, ball_dir

# =======================================================================
def init_ball():
	# Initialize Ball Position and direction  
	ball_pos = [resolution[0]//2-4, resolution[1]//2-4]
	ball_dir = random.randint(0,1)
	ball_angle = (random.randint(1,90) - 45) * 0.001
	return ball_pos, ball_dir, ball_angle
def init_players():
	# Initialize player position X, Y and scores
	p1_pos = [25, resolution[1]//2-4]
	p2_pos = [resolution[0]-32, resolution[1]//2-4]
	p1_score = 0
	p2_score = 0
	return p1_pos, p2_pos, p1_score, p2_score
# Pause, reset ball and player position for every score 
def reset_ball_players():
	ball_pos, ball_dir, ball_angle = init_ball()
	p1_pos = [25, resolution[1]//2-4]
	p2_pos = [resolution[0]-32, resolution[1]//2-4]
	return ball_pos, ball_dir, ball_angle, p1_pos, p2_pos
# =======================================================================
# RUN APP
p1_pos, p2_pos, p1_score, p2_score = init_players()
ball_pos, ball_dir, ball_angle = init_ball()

run_app = True
iterate = 0 
pause = False 
reset = False 
while run_app:	
	#DISPLAY 
	window.fill(BLACK)
	draw_borders(resolution)
	draw_texts(p1_score,p2_score)
	p1 = draw_player1(p1_pos)
	p2 = draw_player2(p2_pos)
	ball = draw_ball(ball_pos)


	while pause:
		pause_text()
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
				pause, reset= False, False 
			if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
				print("restart")
				p1_pos, p2_pos, p1_score, p2_score = init_players()
				ball_pos, ball_dir, ball_angle = init_ball()
			if event.type == pygame.QUIT:
				sys.exit()
	# INGAME EVENTS 	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
					
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				print("restart")
				p1_pos, p2_pos, p1_score, p2_score = init_players()
				ball_pos, ball_dir, ball_angle = init_ball()
				pause = True
			if event.key == pygame.K_SPACE:
				pause = True 

			# Player movement
			if event.key == pygame.K_w or event.key == pygame.K_s:
				p1_pos = p1_move(p1_pos, event.key)
			if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
				p2_pos = p2_move(p2_pos, event.key)


	#UPDATE PER FRAME 
	if iterate > 2 and iterate % 2 == 0:
		ball_pos = ball_move(ball_pos, ball_dir, ball_angle)
		p1_score, p2_score, reset, ball_angle, ball_dir = detect_collision(ball_pos, ball_angle, p1_score, p2_score, reset, [ball,p1,p2], ball_dir)
	if reset: 
		ball_pos, ball_dir, ball_angle, p1_pos, p2_pos = reset_ball_players()
		pause = True 
	iterate += 1 
	clock.tick(60)
	pygame.display.flip()
	# pygame.display.update()