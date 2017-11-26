#!/usr/bin/env python3

import curses
from random import randrange
import sys
import time
from curses.textpad import Textbox, rectangle

def move_cursor(win, key):
	MIN_ROW = 0
	MIN_COL = 0
	MAX_ROW, MAX_COL = win.getmaxyx()
	
	row, col = win.getyx()

	if key == curses.KEY_LEFT:
		if col > MIN_COL:
			col -= 1
	elif key == curses.KEY_RIGHT:
		if col < MAX_COL:
			col += 1
	elif key == curses.KEY_UP:
		if row > MIN_ROW:
			row -= 1
	elif key == curses.KEY_DOWN:
		if row < MAX_ROW:
			row += 1
	else:
		pass
		
	win.move(row, col)

	return(row, col)

def generate_food(win, foodType=0):
	defaultFood = "+"
	bonusFood = "@"
	food = defaultFood
	
	MIN_ROW = 0
	MIN_COL = 0
	MAX_ROW, MAX_COL = win.getmaxyx()
	
	foodX = randrange(MIN_ROW, MAX_ROW)
	foodY = randrange(MIN_COL, MAX_COL)
	foodLocation = (foodX, foodY)
	
	if foodType:
		food = bonusFood

	win.addstr(foodX, foodY, food)
	
	return(foodLocation)
		
def draw_snake(win, key, snakeHeadLocation, snakeHeadLastLocation):
	snakeBody = ""
	snakeHead = chr(0x00f7)
	snakeBodyH = "-"
	snakeBodyV = "|"
	
	if(key == curses.KEY_LEFT) or (key == curses.KEY_RIGHT):
		snakeBody = snakeBodyH
	elif(key == curses.KEY_UP) or (key == curses.KEY_DOWN):
		snakeBody = snakeBodyV
	else:
		pass

	win.addstr(snakeHeadLastLocation[0], snakeHeadLastLocation[1], snakeBody)
	win.addstr(snakeHeadLocation[0], snakeHeadLocation[1], snakeHead)

	return snakeBody
		
def move_snake(win, snakeSize, snakeLocation, snakeHeadLocation):
	SNAKE_DEFAULT_SIZE = 5
			
	if (snakeSize <= SNAKE_DEFAULT_SIZE):
		pass
	else:
		win.addstr(snakeLocation[0][0], (snakeLocation[0][1]), " ")
		del snakeLocation[0]
	
	snakeLocation.append(snakeHeadLocation)
	
	return(snakeLocation)

def init_game(win):
	foodLocation = generate_food(win, 0)
	defaultSnakePosition = (0, int((curses.COLS-1) / 2))
	win.move(defaultSnakePosition[0], defaultSnakePosition[1])
	snakeHeadLastLocation = defaultSnakePosition

	return(foodLocation, snakeHeadLastLocation)

def game_scores(score, scoretype=0):
	MAX_COL = curses.COLS-1
	scorePad = curses.newpad(1, MAX_COL)
	scorePad.addstr(0, 0, "Score: ")
	scorePad.addstr(str(score))
	scorePad.refresh(0, 0, 0, 0, 0, int(MAX_COL/2))
	
	return score+1

def setup_screen(debug=False):
	curses.curs_set(False)
	
	MIN_ROW = 0
	MIN_COL = 0
	MAX_ROW = curses.LINES - 1
	MAX_COL = curses.COLS - 1
	
	screens = []
	scoreWinCoordinates = (1, MAX_COL, 0, 0)
	gameWinCoordinates = (MAX_ROW-1, MAX_COL, 1, 0)
	
	if debug:
		gameWinCoordinates = (MAX_ROW-8, MAX_COL, 1, 0)
		debugWinCoordinates = (7, MAX_COL, MAX_ROW-7, 0)
		debugWin = curses.newwin(*debugWinCoordinates)
		screens.append(debugWin)

	scoreWin = curses.newwin(*scoreWinCoordinates)
	gameWin = curses.newwin(*gameWinCoordinates)
	screens.append(scoreWin)
	screens.append(gameWin)
	
	return(screens, len(screens))
	
def main(stdscr):
	screens, lenScreens = setup_screen()
	snakeLocation = []
	foodLocation, snakeHeadLastLocation = init_game(gameWin)
	snakeLocation.append(snakeHeadLastLocation)
	score = 0
	
	while True:
		key = gameWin.getch()
		gameWin.addstr(str(key))
		row, col = move_cursor(gameWin, key)
		snakeHeadLocation = (row, col)
		snakeBody = draw_snake(gameWin, key, snakeHeadLocation, snakeHeadLastLocation)
		snakeHeadLastLocation = snakeHeadLocation
		snakeLocation = move_snake(gameWin, snakeLocation, snakeHeadLocation)
		gameWin.move(row, col)
			
		if(snakeHeadLocation[0] == foodLocation[0] and snakeHeadLocation[1] == foodLocation[1]):
			score = game_scores(score, 0)
			foodLocation = generate_food(gameWin, 0)
			gameWin.move(row, col)

if(__name__ == "__main__"):
	curses.wrapper(main)
