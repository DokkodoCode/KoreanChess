"""
------------------------main.py-----------------------------------
o This file is to hold the entry point to the program
o Last Modified - November 19th 2024
------------------------------------------------------------------
"""

# libraries
import os
import pygame
import sys

# local file imports, see individ file for details
import constants
import state
import state_machine
from helper_funcs import is_fullscr

def main():

	# use user's machine's screen size as reference to screen width/height
	os.environ['SDL_VIDEO_CENTERED'] = '1'


	# *
	info = pygame.display.Info()
	width, height = info.current_w, info.current_h
	print(width, height)


	# initialize pygame instance
	pygame.init()
	
	# frames
	clock = pygame.time.Clock()
	fps = 60

	# create logo for window
	icon = pygame.image.load("Pieces/Cho_King.png")
	pygame.display.set_icon(icon)

	# create the window
	window = pygame.display.set_mode((constants.screen_width, constants.screen_height), pygame.FULLSCREEN)

	pygame.display.update()
	pygame.display.set_caption("Janggi")

	# create state machine
	state_manager = state_machine.StateManager(window)
	
	# core loop
	#running = True
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
				constants.eWidth, constants.eHeight = event.size

				constants.screen_width, constants.screen_height = is_fullscr(constants.eWidth, constants.eHeight)

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
	main()
