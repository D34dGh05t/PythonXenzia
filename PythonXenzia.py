#!/usr/bin/env python3

import curses
from random import randrange
import sys
import time

def move_cursor(win, key):
	MIN_ROW = 0
	MIN_COL = 0
	MAX_ROW = curses.LINES - 1
	MAX_COL = curses.COLS - 1
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
	food = ""
	defaultFood = "+"
	bonusFood = "@"
	
	MIN_ROW = 0
	MIN_COL = 0
	MAX_ROW = curses.LINES - 1
	MAX_COL = curses.COLS - 1
	
	foodX = randrange(MIN_ROW, MAX_ROW)
	foodY = randrange(MIN_COL, MAX_COL)
	foodLocation = (foodX, foodY)
	
	if foodType:
		food = bonusFood
	else:
		food = defaultFood
	
	win.addstr(foodX, foodY, food)
	
	return(foodLocation)
		
def snake(key, stdscr, snakeHeadLocation, snakeHeadLastLocation):
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

	stdscr.addstr(snakeHeadLastLocation[0], snakeHeadLastLocation[1], snakeBody)
	stdscr.addstr(snakeHeadLocation[0], snakeHeadLocation[1], snakeHead)

	return snakeBody
		
def move_snake(stdscr, snakeLocation, snakeHeadLocation):
	snakeDefaultSize = 5
	snakeSize = len(snakeLocation)
			
	if(snakeSize <= snakeDefaultSize):
		pass
	else:
		stdscr.addstr(snakeLocation[0][0], (snakeLocation[0][1]), " ")
		del snakeLocation[0]
	
	snakeLocation.append(snakeHeadLocation)
	
	return(snakeLocation)

def init_game(win):
	foodLocation = generate_food(win, 0)
	defaultSnakePosition = (0, int((curses.COLS-1) / 2))
	win.move(defaultSnakePosition[0], defaultSnakePosition[1])
	snakeHeadLastLocation = defaultSnakePosition

	return(foodLocation, defaultSnakePosition, snakeHeadLastLocation)

def main(stdscr):
	curses.curs_set(False)

	snakeLocation = []
	foodLocation, defaultSnakePosition, snakeHeadLastLocation = init_game(stdscr)
	snakeLocation.append(snakeHeadLastLocation)
	
	while True:
		key = stdscr.getch()
		row, col = move_cursor(stdscr, key)
		snakeHeadLocation = (row, col)
		snakeBody = snake(key, stdscr, snakeHeadLocation, snakeHeadLastLocation)
		snakeHeadLastLocation = snakeHeadLocation
		snakeLocation = move_snake(stdscr, snakeLocation, snakeHeadLocation)
		stdscr.move(row, col)
	
		if(snakeHeadLocation[0] == foodLocation[0] and snakeHeadLocation[1] == foodLocation[1]):
			foodLocation = generate_food(stdscr, 0)
			stdscr.move(row, col)

if(__name__ == "__main__"):
	curses.wrapper(main)
