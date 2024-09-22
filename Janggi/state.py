"""
----------------------state.py----------------------------
o This file is to manage the current game mode (state) the
	program is in
o Last Modified - September 16th 2024
----------------------------------------------------------
"""

# libraries
import pygame

# local file imports, see individ file for details
import board
import constants
import helper_funcs
import opponent
import player
import render_funcs

# Parent State to act as a base class to be inherited by 
# future state implementations
class State():
	# initializer
	def __init__(self):
		self.next_state = None

	# event handler
	def handle_event(self, event):
		pass

	# handle rendering
	def render(self, window):
		pass

	# no current use, needed only by state machine
	def update(self):
		pass

# FUTURE IMPLEMENTATION
class MainMenu(State):
	def __init__(self):
		pass

# CURRENT WIP TODO
# Inherited State for single player gaming against an ai
class SinglePlayerGame(State):
	# initialize the gamestate
	# INPUT: No Input
	# OUTPUT: Gamestate is initialized and ready for playing
	def __init__(self):
		# create game objects
		self.board = board.Board()
		self.player = player.Player()
		self.opponent = opponent.Opponent()
		
		# display the window
		self.window = pygame.display.set_mode(
			(constants.window_width, constants.window_height))
		pygame.display.set_caption("Janggi")

	# Listen for and handle any event ticks (clicks/buttons)
	#	INPUT: pygame event object
	# OUTPUT: User triggered game events are handled appropriately
	def handle_event(self, event):
		# get the player's mouse position for click tracking
		mouse_pos = pygame.mouse.get_pos()
		# listen for an event trigger via click from right-mouse-button
		if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
			# check if the player is currently attempting to move a piece
			if self.player.is_clicked:
				# unclick that piece if the move was successful/valid
				if helper_funcs.attempt_move(self.player, self.opponent, self.board, mouse_pos):
					helper_funcs.player_piece_unclick(self.player)
				# otherwise the player is clicking another piece or invalid spot
				else:
					# reset click state
					helper_funcs.player_piece_unclick(self.player)
					# update click to new piece if valid clicked
					helper_funcs.player_piece_clicked(self.player, mouse_pos)

			# otherwise, check if any player-side pieces were clicked
			elif helper_funcs.player_piece_clicked(self.player, mouse_pos):
				# FUTURE LOGIC HERE
				pass
			# IMPLEMENT FURTHER BRANCHES HERE FOR FUTURE IMPLEMENTATIONS
		# if something...
			# do something ...
		# elif something
			# do etc...
				
	# Handle any rendering that needs to be done
	# INPUT: pygame surface object (window to display to)
	# OUTPUT: All game attributes/actions are rendered
	def render(self, window):
		# load then display board image
		menu_background = pygame.image.load("Board/Janggi_Board.png").convert_alpha()
		menu_background = pygame.transform.scale(menu_background, constants.board_size)
		window.blit(menu_background, constants.board_image)

		# if player has a piece currently clicked, render where it can go
		if self.player.is_clicked:
			render_funcs.render_possible_spots(self.player, self.opponent, self.board, self.window)
		# render collision rectangles for the pieces on both teams
		render_funcs.render_piece_collisions(self.player, self.opponent, self.window)
		# load the pieces on the board for both teams
		render_funcs.render_pieces(self.player, self.opponent, self.window)