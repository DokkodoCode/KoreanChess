"""
------------------------main.py-----------------------------------
o This file is to hold the entry point to the program
o Last Modified - September 12th 2024
------------------------------------------------------------------
"""

# libraries
import pygame
import sys

# local file imports
import constants
import state_machine

def main():
	# initialize pygame instance
	pygame.init()

	# frames
	clock = pygame.time.Clock()
	fps = 60

	# display the window
	window = pygame.display.set_mode((constants.window_width, constants.window_height))
	pygame.display.set_caption("Janggi")

	# create state machine
	state_manager = state_machine.StateManager()
	
	# core loop
	running = True
	while running:
		# find matching event calls by player to pygame event calls
		for event in pygame.event.get():
			# if player closes window
			if event.type == pygame.QUIT:
				# halt execution
				running = False

			# otherwise call the state machine
			else:
				state_manager.handle_event(event)

		# clear screen/window
		window.fill((0,0,0))

		# render the next frame
		state_manager.render(window)

		# state manager logic
		state_manager.update()
		
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
