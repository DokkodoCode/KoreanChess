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
from piece import update_piece_positions
#from helper_funcs import is_fullscr


#Function that gets the scaling factors for the width and height
#Takes in the current width and height of the window and divides it by the reference width and height
#to get the scale factor for the width and height.
def get_scaling_factors(current_width, current_height):
	constants.scale_w = current_width / constants.REFERENCE_WIDTH
	constants.scale_h = current_height / constants.REFERENCE_HEIGHT
	constants.REFERENCE_WIDTH = current_width
	constants.REFERENCE_HEIGHT = current_height


#Function that scales the board size, board border size, spot collision size, and piece coordinates
#(Everything outside of the dictionary)
def scale_everything():
		constants.board_size = ((constants.board_size[0] * constants.scale_w), (constants.board_size[1] * constants.scale_h))
		#print(f"supposed board size: {constants.board_size}")
		constants.board_border_size = ((constants.board_border_size[0] * constants.scale_w), (constants.board_border_size[1] * constants.scale_h))

		constants.spot_collision_size = ((constants.spot_collision_size[0] * constants.scale_w), (constants.spot_collision_size[1] * constants.scale_h))

		constants.small_collision_size = ((constants.small_collision_size[0] * constants.scale_w), (constants.small_collision_size[1] * constants.scale_h))

		constants.small_size = ((constants.small_size[0] * constants.scale_w), (constants.small_size[1] * constants.scale_h))

		constants.med_collision_size = ((constants.med_collision_size[0] * constants.scale_w), (constants.med_collision_size[1] * constants.scale_h))

		constants.med_size = ((constants.med_size[0] * constants.scale_w), (constants.med_size[1] * constants.scale_h))

		constants.large_collision_size = ((constants.large_collision_size[0] * constants.scale_w), (constants.large_collision_size[1] * constants.scale_h))

		constants.large_size = ((constants.large_size[0] * constants.scale_w), (constants.large_size[1] * constants.scale_h))

		constants.x_coordinates = [x * constants.scale_w for x in constants.x_coordinates]

		constants.y_coordinates = [y * constants.scale_h for y in constants.y_coordinates]


#Prints the resolutions dictionary
def print_resolutions(resolutions, indent=0):
    for key, value in resolutions.items():
        if isinstance(value, dict):  # If the value is a nested dictionary
            print("  " * indent + f"{key}:")
            print_resolutions(value, indent + 1)  # Recursively print nested dictionaries
        else:
            print("  " * indent + f"{key}: {value}")


#Function that scales everything in the resolutions dictionary
def scale_resolutions(resolutions, scale_w, scale_h):
    for key, value in resolutions.items():
        if isinstance(value, dict):  # If the value is a nested dictionary
            scale_resolutions(value, scale_w, scale_h)  # Recursively scale nested dictionaries
        elif isinstance(value, tuple) and len(value) == 2 and all(isinstance(v, (int, float)) for v in value):
            # Scale tuples with numeric values (e.g., (width, height))
            resolutions[key] = (value[0] * scale_w, value[1] * scale_h)


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

	#set window to intial size
	#get_scaling_factors(constants.window_size[0], constants.window_size[1])
	#scale_everything()
	#scale_resolutions(constants.resolutions, constants.scale_w, constants.scale_h)

	# create the window
	
	window = pygame.display.set_mode(constants.window_size, pygame.RESIZABLE)
    
	#print_resolutions(constants.resolutions)

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

				window = pygame.display.set_mode(event.size, pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE)

				window_width, window_height = window.get_size()

				constants.window_size = window.get_size()

				#print(f"Window size: {constants.window_size}")

				#Get the scaling factors for the width and height
				get_scaling_factors(window_width, window_height)

				#Scale the resolutions dictionary
				scale_resolutions(constants.resolutions, constants.scale_w, constants.scale_h)

				#Scale the board size, board border size, spot collision size, and piece coordinates
				scale_everything()

				# Update piece positions
				update_piece_positions()
				
				#print_resolutions(constants.resolutions)
                
				#state_manager.current_state.load_board_boarder(window)
				#state_manager.current_state.load_board()
				#state_manager.current_state.__init__(window)
				state_manager.current_state.resize(window)
				state_manager.current_state.render(window)
                
				

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
