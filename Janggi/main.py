"""
------------------------main.py-----------------------------------
o This file is to hold the entry point to the program
o Last Modified - April 8th 2025
------------------------------------------------------------------
"""

# libraries
import os
from turtle import Screen

import pygame
import sys

# local file imports, see individ file for details
import button
import constants
import res_config

# import state
# import state_machine
# from helper_funcs import is_fullscr

def res_select():

	screen = pygame.display.set_mode((1360, 796), pygame.RESIZABLE)

	icon = pygame.image.load("Pieces/Cho_King.png")
	pygame.display.set_icon(icon)

	pygame.display.set_caption("Janggi")

	while res_config.res:
		screen.fill("black")

		mouse_pos = pygame.mouse.get_pos()

		font = pygame.font.Font("UI/HIROMISAKE.ttf", size=120)
		intro_text = font.render("Welcome to Janggi", True, (255,255,255))
		screen.blit(intro_text, (125, 130))

		font = pygame.font.SysFont("Arial", size=35)
		main_text = font.render("Select Game Resoultion", True, (255,255,255))
		screen.blit(main_text, (495, 320))

		win_button = button.Button(480, 400, 400, 80, font, "1360 x 760 (Window)", (0,0,0), (255,255,255), (255,0,0))
		full_button = button.Button(480, 520, 400, 80, font, "1920 x 1080 (Fullscreen)", (0,0,0), (255,255,255), (0,0,255))

		win_button.draw_button(screen)
		full_button.draw_button(screen)

		for event in pygame.event.get():
			if event.type == pygame.MOUSEBUTTONDOWN:
				if win_button.is_clicked():
					res_config.ewidth, res_config.eheight = 1360, 796
					constants.screen_width, constants.screen_height = 1360, 796

					config = constants.get_resolution_config("1360x796")
					constants.initialize_constants(config)

					print(res_config.ewidth, res_config.eheight)

					main(res_config.ewidth, res_config.eheight)
					pygame.display.update()
					res_config.res = False

				if full_button.is_clicked():
					res_config.ewidth, res_config.eheight = 1920, 1080
					constants.screen_width, constants.screen_height = 1920, 1080

					config = constants.get_resolution_config("1920x1080")
					constants.initialize_constants(config)

					print(res_config.ewidth, res_config.eheight)

					main(res_config.ewidth, res_config.eheight)
					pygame.display.update()
					res_config.res = False

		pygame.display.update()



def main(ewidth, eheight):
	import state_machine

	# use user's machine's screen size as reference to screen width/height
	os.environ['SDL_VIDEO_CENTERED'] = '1'

	# initialize pygame instance
	pygame.init()
	
	# frames
	clock = pygame.time.Clock()
	fps = 60

	# create logo for window
	icon = pygame.image.load("Pieces/Cho_King.png")
	pygame.display.set_icon(icon)

	# create the window
	if ewidth == 1360:
		window = pygame.display.set_mode((ewidth, eheight))
	else:
		window = pygame.display.set_mode((ewidth, eheight), pygame.FULLSCREEN)

	pygame.display.update()
	pygame.display.set_caption("Janggi")

	# create state machine
	state_manager = state_machine.StateManager(window)
	
	# core loop
	# running = True
	while constants.running:
		# find matching event calls by player to pygame event calls
		for event in pygame.event.get():
			# if player closes window
			if event.type == pygame.QUIT:
				# halt execution
				constants.running = False
			# if player resizes the window via dragging border
			elif event.type == pygame.VIDEORESIZE:

				window = pygame.display.set_mode(event.size, pygame.RESIZABLE)


				# window = pygame.display.set_mode(event.size, pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE)

			# otherwise call the state machine
			else:
				state_manager.handle_event(event)

		# clear screen/window
		window.fill((0,0,0))

		# render the next frame
		state_manager.render(window)

		# state manager logic
		state_manager.update(window)
		
		# update the window with any drawing methods that were called
		pygame.display.flip()

		# cap frame rate
		clock.tick(fps)

	# end program
	pygame.quit()
	# clean exit
	sys.exit()


if __name__ == "__main__":
	res_select()
