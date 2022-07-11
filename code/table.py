import time
from rpi_ws281x import *
from variables import *


class Table:
	def __init__(self):
		self.selected_game = 0
		self.players = False
		
	def select_game(self, value): # Need get from sensors
		self.selected_game = value 
		self.players = False

	def ColoringTable_Start(self, strip):
		for i in range(16):
			for j in range(16):
				if j < 8:
					r, g, b, w = 0, j * 10, 255, 0
				else:
					r, g, b, w = 255, i * 10, 0, 0
				strip.setPixelColor(order[i][j], Color(r, g, b, w))
			time.sleep(0.05)
			strip.show()

	def ColoringTable_Wait(self, strip, k):
		for i in range(16):
			for j in range(16):
				if j < 8:
					r, g, b, w = 0, j * 10, 255, k
				else:
					r, g, b, w = 255, i * 10, 0, k
				strip.setPixelColor(order[i][j], Color(r, g, b, w))
		strip.show()
			
	def ColoringTable_Error(strip):
		Table.ColoringTable_JustColor(strip, 255, 0, 0, 0)
		time.sleep(0.15)
		Table.ColoringTable_JustColor(strip, 50, 0, 0, 0)
		time.sleep(0.15)
		Table.ColoringTable_JustColor(strip, 255, 0, 0, 0)
		time.sleep(0.3)

	def ColoringTable_JustColor(strip, r, g, b, w):
		for i in range(16):
			for j in range(16):
				strip.setPixelColor(order[i][j], Color(r, g, b, w))
		strip.show() 

	def start_game(self, strip):
		
		if self.selected_game == 1:
			print('YOU SELECTED THE FIRST GAME - CHECKERS')
			Soft_down_brightness(strip)
			from checkers_game import Checkers
			checkers = Checkers()
			checkers.play(strip)
		elif self.selected_game == 2:
			print('YOU SELECTED THE SECOND GAME - TIK TAK TOE')
			Soft_down_brightness(strip)
			from tiktaktoe_game import TikTakToe
			tiktaktoe = TikTakToe()
			tiktaktoe.play(strip)
		elif self.selected_game == 3:
			print('YOU SELECTED THE THIRD GAME - not yet available. Repeat insert please')
			Soft_brightness(strip)
		elif self.selected_game == 0:
			Soft_down_brightness(strip)
			from developer_mode import DevOp
			developer = DevOp()
			developer.playRaw(strip)
		else:
			Table.ColoringTable_Error(strip)
			print('Incorrect input. Repeat please')
