"""
----------------------state.py----------------------------
o This file is to manage the current game mode (state) the
	program is in
o Last Modified - November 19th 2024
----------------------------------------------------------
"""

# libraries
import pygame

# local file imports, see individ file for details
import ai
import board
import button
import constants
import helper_funcs
import player
import render_funcs

#--------------------------------------------------------------------------------
# Parent State to act as a base class to be inherited by 
#--------------------------------------------------------------------------------
class State():
	# initializer
	def __init__(self):
		self.next_state = None

		# game state variables
		# only used in:
		#   SinglePlayerGame()
		#   LocalSinglePlayerGame()
		#   Multiplayer()
		self.opening_turn = True  # check to see if its the first turn of the game
		self.bikjang = False      # When both generals face each other unobstructed
		self.check = False        # When a general is in threat of being captured
		self.condition = "None"   # this is being set between either Check, Bikjang, and None. But there's aleady checks for that?
		self.game_over = False
		self.winner = None        # set to a player object, used to display what player won

	def handle_event(self, event):
		pass

	def render(self, window):
		pass

	def update(self):
		pass

	# functions to detect the type of user input
	def is_left_click(self, event):
		if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
			return True
		return False
	
	def is_middle_click(self, event):
		if event.type == pygame.MOUSEBUTTONDOWN and event.button == 2:
			return True
		return False
	
	def is_right_click(self, event):
		if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
			return True
		return False

	# function that will load the board boarder image into memory
	def load_board_boarder(self, window):
		self.menu_background = pygame.image.load("Board/Janggi_Board_Border.png").convert_alpha()
		self.menu_background = pygame.transform.scale(self.menu_background, constants.board_border_size)
		self.center = window.get_rect().center

	#  function that will load board into memory
	def load_board(self):
		self.playboard = pygame.image.load("Board/Janggi_Board.png").convert_alpha()
		self.playboard = pygame.transform.scale(self.playboard, constants.board_size)
		self.playboard_center = self.menu_background.get_rect().center

	# Method to draw text information out to the window
	# INPUT: window object, text to be displayed, (x,y) of where to write on, font size
	# OUTPUT: Window contains the text to be displayed
	def draw_text(self, window, text, x=0, y=0, font_size=30):
		font = pygame.font.SysFont("Arial", font_size)
		text_surface = font.render(text, True, constants.WHITE)
		window.blit(text_surface, (x, y))

	# Checks flags to see if the game is over by check
	def is_game_over(self):
		if (not helper_funcs.resolve_condition(self.active_player, self.waiting_player, self.board, self.condition) and
	  		self.condition == "Check"):
			return True
		return False

	# render functions for elements of menus
	def render_check_ending(self, window):
		# DRAW THE BACKGROUND FOR DISPLAYING GAME OVER TEXT
		window.blit(self.game_over_background,
			constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["local_MP"]["button_background"]["game_over"]["location"])
			
		# DISPLAY GAME OVER TEXT
		text = "Game Over!"
		x, y = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["local_MP"]["button_background"]["game_over"]["notify_text"]["location"]
		font_size = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["local_MP"]["button_background"]["game_over"]["notify_text"]["font_size"]
		self.draw_text(window, text, x, y, font_size)
		
		# DISPLAY THE WINNER
		text = f"{self.winner.color} wins!"
		x, y = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["local_MP"]["button_background"]["game_over"]["result_text"]["location"]
		font_size = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["local_MP"]["button_background"]["game_over"]["result_text"]["font_size"]
		self.draw_text(window, text, x, y, font_size)

		# DISPLAY REASONING
		text = f"Check initiated by {self.winner.color} was unresolvable."
		x, y = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["local_MP"]["button_background"]["game_over"]["condition_text"]["location"]
		font_size = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["local_MP"]["button_background"]["game_over"]["condition_text"]["font_size"]
		self.draw_text(window, text, x, y, font_size)

	def render_bikjang_ending(self, window):
		# DRAW THE BACKGROUND FOR DISPLAYING GAME OVER TEXT
		window.blit(self.game_over_background,
		constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["local_MP"]["button_background"]["game_over"]["location"])
		
		# DISPLAY GAME OVER TEXT
		text = "Game Over!"
		x, y = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["local_MP"]["button_background"]["game_over"]["notify_text"]["location"]
		font_size = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["local_MP"]["button_background"]["game_over"]["notify_text"]["font_size"]
		self.draw_text(window, text, x, y, font_size)

		# DISPLAY ANY RESULT-AFFECTING CONDITIONS
		text = f"Bikjang was initiated by {self.winner.color}."
		x, y = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["local_MP"]["button_background"]["game_over"]["condition_text"]["location"]
		font_size = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["local_MP"]["button_background"]["game_over"]["condition_text"]["font_size"]
		self.draw_text(window, text, x, y, font_size)

		# DISPLAY THE FINAL RESULT
		text = "Draw..."
		x, y = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["local_MP"]["button_background"]["game_over"]["result_text"]["location"]
		font_size = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["local_MP"]["button_background"]["game_over"]["result_text"]["font_size"]
		self.draw_text(window, text, x, y, font_size)

	def render_player_color_menu(self, window):
		# SELECT PIECE SIDE TO PLAY AS (CHO/HAN)
		window.blit(self.play_as_background, 
			   constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["local_MP"]["button_background"]["play_as"]["location"])
		text = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["local_MP"]["button_background"]["play_as"]["text"]["string"]
		x, y = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["local_MP"]["button_background"]["play_as"]["text"]["location"]
		font_size = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["local_MP"]["button_background"]["play_as"]["text"]["font_size"]

		self.draw_text(window, text, x, y, font_size)
		self.cho_side_button.draw_button(window)
		self.han_side_button.draw_button(window)
	
	def render_piece_convention_menu(self, window):
		window.blit(self.piece_convention_background, 
			   constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["local_MP"]["button_background"]["piece_convention"]["location"])
		text = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["local_MP"]["button_background"]["piece_convention"]["text"]["string"]
		x, y = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["local_MP"]["button_background"]["piece_convention"]["text"]["location"]
		font_size = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["local_MP"]["button_background"]["piece_convention"]["text"]["font_size"]

		self.draw_text(window, text, x, y, font_size)
		self.standard_piece_convention_button.draw_button(window)
		self.internat_piece_convention_button.draw_button(window)

	def render_play_button(self, window):
		window.blit(self.play_button_background, 
		constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["local_MP"]["button_background"]["play"]["location"])
		self.play_button.draw_button(window)

	def render_board(self, window):
		window.blit(self.menu_background, self.menu_background.get_rect(center = window.get_rect().center))
		window.blit(self.playboard, self.playboard.get_rect(center = window.get_rect().center))

	def render_player_piece_preview(self, window):
		# player header to notify which display is player's
		window.blit(self.player_header_background, 
			constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]
			["background_elements"]["single_player"]["button_background"]["player_piece_display"]["player_header"]["location"])
		
		# player header text display
		text = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["single_player"]["button_background"]["player_piece_display"]["text"]["string"]
		x, y = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["single_player"]["button_background"]["player_piece_display"]["text"]["location"]
		font_size = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["single_player"]["button_background"]["player_piece_display"]["text"]["font_size"]
		self.draw_text(window, text, x, y, font_size)

		# player piece display
		window.blit(self.player_piece_display_background, 
			constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["single_player"]["button_background"]["player_piece_display"]["location"])

			
		# opponent piece display
		window.blit(self.opponent_piece_display_background, 
			constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["single_player"]["button_background"]["opponent_piece_display"]["location"])

		# render pieces
		render_funcs.PreGame_render_piece_display(window, self.host, self.guest)

	def handle_piece_move(self, host, guest, mouse_pos):
		# finds possible spots for piece to move, if player clicks avaiable spot, returns true
		if helper_funcs.attempt_move(host, guest, self.board, mouse_pos, self.condition):

			# reset is_clicked flags for player and piece
			helper_funcs.player_piece_unclick(host)
			
			# if bikjang occurs, set appropriate flags
			if helper_funcs.detect_bikjang(host, guest):
				self.bikjang = True
				self.condition = "Bikjang"
				self.winner = host
				self.game_over = True

			# if check occurs, set appropriate flags
			elif helper_funcs.detect_check(guest, host, self.board):
				self.check = True
				self.condition = "Check"
				self.guest.is_checked = True
												
			self.swap_turn()
			self.immediate_render = True

		# otherwise the player is clicking another piece or invalid spot
		else:
			# reset click state
			helper_funcs.player_piece_unclick(host)
			# update click to new piece if valid clicked
			helper_funcs.player_piece_clicked(host, mouse_pos)

	def load_player_color_menu(self):
		# play as cho/han button background
		self.play_as_background = (
			pygame.transform.scale(self.button_background,
				constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["local_MP"]["button_background"]["play_as"]["size"]))
		
		# cho button
		x, y = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["local_MP"]["cho_button"]["location"]
		width, height = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["local_MP"]["cho_button"]["size"]
		font = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["local_MP"]["cho_button"]["text"]["font"]
		text = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["local_MP"]["cho_button"]["text"]["string"]
		foreground_color = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["local_MP"]["cho_button"]["text"]["foreground_color"]
		background_color = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["local_MP"]["cho_button"]["text"]["background_color"]
		hover_color = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["local_MP"]["cho_button"]["text"]["hover_color"]
		self.cho_side_button = (button.Button(x, y, width, height, font, text, foreground_color, background_color, hover_color))
		
		# han button
		x, y = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["local_MP"]["han_button"]["location"]
		width, height = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["local_MP"]["han_button"]["size"]
		font = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["local_MP"]["han_button"]["text"]["font"]
		text = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["local_MP"]["han_button"]["text"]["string"]
		foreground_color = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["local_MP"]["han_button"]["text"]["foreground_color"]
		background_color = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["local_MP"]["han_button"]["text"]["background_color"]
		hover_color = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["local_MP"]["han_button"]["text"]["hover_color"]
		self.han_side_button = (button.Button(x, y, width, height, font, text, foreground_color, background_color, hover_color))

	def load_piece_convention_menu(self):
		self.piece_convention_background = (
			pygame.transform.scale(self.button_background,
				constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["local_MP"]["button_background"]["piece_convention"]["size"]))
		
		# standard piece convention button
		x, y = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["local_MP"]["standard_piece_convention_button"]["location"]
		width, height = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["local_MP"]["standard_piece_convention_button"]["size"]
		font = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["local_MP"]["standard_piece_convention_button"]["text"]["font"]
		text = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["local_MP"]["standard_piece_convention_button"]["text"]["string"]
		foreground_color = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["local_MP"]["standard_piece_convention_button"]["text"]["foreground_color"]
		background_color = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["local_MP"]["standard_piece_convention_button"]["text"]["background_color"]
		hover_color = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["local_MP"]["standard_piece_convention_button"]["text"]["hover_color"]
		self.standard_piece_convention_button = (button.Button(x, y, width, height, font, text, foreground_color, background_color, hover_color))
		
		# international piece convention button
		x, y = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["local_MP"]["internat_piece_convention_button"]["location"]
		width, height = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["local_MP"]["internat_piece_convention_button"]["size"]
		font = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["local_MP"]["internat_piece_convention_button"]["text"]["font"]
		text = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["local_MP"]["internat_piece_convention_button"]["text"]["string"]
		foreground_color = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["local_MP"]["internat_piece_convention_button"]["text"]["foreground_color"]
		background_color = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["local_MP"]["internat_piece_convention_button"]["text"]["background_color"]
		hover_color = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["local_MP"]["internat_piece_convention_button"]["text"]["hover_color"]
		self.internat_piece_convention_button = (button.Button(x, y, width, height, font, text, foreground_color, background_color, hover_color))
		
	def load_play_button(self):
		self.play_button_background = pygame.image.load("UI/Button_Background_Poly.png").convert_alpha()
		self.play_button_background = (pygame.transform.scale(self.play_button_background,
				constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["local_MP"]["button_background"]["play"]["size"]))
		
		# play button
		x, y = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["local_MP"]["play_button"]["location"]
		width, height = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["local_MP"]["play_button"]["size"]
		font = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["local_MP"]["play_button"]["text"]["font"]
		text = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["local_MP"]["play_button"]["text"]["string"]
		foreground_color = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["local_MP"]["play_button"]["text"]["foreground_color"]
		background_color = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["local_MP"]["play_button"]["text"]["background_color"]
		hover_color = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["local_MP"]["play_button"]["text"]["hover_color"]
		self.play_button = (button.Button(x, y, width, height, font, text, foreground_color, background_color, hover_color))

	def load_player_piece_preview(self):
		# player piece display background
		self.player_piece_display_background = pygame.image.load("UI/Button_Background.png").convert_alpha()
		self.player_piece_display_background = pygame.transform.rotate(self.player_piece_display_background, 90)
		self.player_piece_display_background = pygame.transform.scale(self.player_piece_display_background,
				constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["local_MP"]["button_background"]["player_piece_display"]["size"])
		
		# player header background
		self.player_header_background = pygame.image.load("UI/Button_Background.png").convert_alpha()
		self.player_header_background = pygame.transform.scale(self.player_header_background,
				constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["local_MP"]["button_background"]["player_piece_display"]["player_header"]["size"])
		
		# opponent piece display background
		self.opponent_piece_display_background = pygame.image.load("UI/Button_Background.png").convert_alpha()
		self.opponent_piece_display_background = pygame.transform.rotate(self.opponent_piece_display_background, 270)
		self.opponent_piece_display_background = pygame.transform.scale(self.opponent_piece_display_background,
				constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["local_MP"]["button_background"]["opponent_piece_display"]["size"])
	
	def load_button_background(self):
		# load button backgrounds
		self.button_background = pygame.image.load("UI/Button_Background.png").convert_alpha()
		self.button_background = (
			pygame.transform.scale(self.button_background,
				constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["local_MP"]["button_background"]["play_as"]["size"]))

#--------------------------------------------------------------------------------
# MAIN MENU TO TRANSITION INTO SINGLEPLAYER/MULTIPLAYER/ETC...
#--------------------------------------------------------------------------------
class MainMenu(State):
	# initialize the settings for the game
	# INPUT: No Input
	# OUTPUT: Main menu is ready to be interacted with by player
	def __init__(self, window):
		super().__init__() # inherit the parent initializer
		self.next_state = None
		self.font = pygame.font.SysFont("Arial",size=50)

		# button for single player
		x, y = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["main_menu"]["single_player_button"]["location"]
		width, height = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["main_menu"]["single_player_button"]["size"]
		font = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["main_menu"]["single_player_button"]["text"]["font"]
		text = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["main_menu"]["single_player_button"]["text"]["string"]
		foreground_color = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["main_menu"]["single_player_button"]["text"]["foreground_color"]
		background_color = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["main_menu"]["single_player_button"]["text"]["background_color"]
		hover_color = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["main_menu"]["single_player_button"]["text"]["hover_color"]
		self.singleplayer_button = (button.Button(x, y, width, height, font, text, foreground_color, background_color, hover_color))

		# button for local-mulyiplayer player
		x, y = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["main_menu"]["local_multiplayer_button"]["location"]
		width, height = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["main_menu"]["local_multiplayer_button"]["size"]
		font = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["main_menu"]["local_multiplayer_button"]["text"]["font"]
		text = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["main_menu"]["local_multiplayer_button"]["text"]["string"]
		foreground_color = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["main_menu"]["local_multiplayer_button"]["text"]["foreground_color"]
		background_color = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["main_menu"]["local_multiplayer_button"]["text"]["background_color"]
		hover_color = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["main_menu"]["local_multiplayer_button"]["text"]["hover_color"]
		self.local_multiplayer_button = (button.Button(x, y, width, height, font, text, foreground_color, background_color, hover_color))

		# button for multiplayer
		x, y = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["main_menu"]["multiplayer_button"]["location"]
		width, height = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["main_menu"]["multiplayer_button"]["size"]
		font = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["main_menu"]["multiplayer_button"]["text"]["font"]
		text = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["main_menu"]["multiplayer_button"]["text"]["string"]
		foreground_color = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["main_menu"]["multiplayer_button"]["text"]["foreground_color"]
		background_color = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["main_menu"]["multiplayer_button"]["text"]["background_color"]
		hover_color = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["main_menu"]["multiplayer_button"]["text"]["hover_color"]
		self.multiplayer_button = (button.Button(x, y, width, height, font, text, foreground_color, background_color, hover_color))

		# button for exiting application
		x, y = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["main_menu"]["close_button"]["location"]
		width, height = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["main_menu"]["close_button"]["size"]
		font = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["main_menu"]["close_button"]["text"]["font"]
		text = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["main_menu"]["close_button"]["text"]["string"]
		foreground_color = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["main_menu"]["close_button"]["text"]["foreground_color"]
		background_color = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["main_menu"]["close_button"]["text"]["background_color"]
		hover_color = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["main_menu"]["close_button"]["text"]["hover_color"]
		self.exit_button = (button.Button(x, y, width, height, font, text, foreground_color, background_color, hover_color))

		self.load_board_boarder(window)
		self.load_board()
		self.button_background = pygame.image.load("UI/Button_Background_Poly.png").convert_alpha()
		self.button_background = pygame.transform.scale(self.button_background,
									constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["main_menu"]["menu_background_size"])

	# Listen for and handle any event ticks (clicks/buttons)
	# INPUT: pygame event object
	# OUTPUT: Menu transitions are set accordingly
	def handle_event(self, event):
		if self.is_left_click(event):
			if self.singleplayer_button.is_clicked():
				self.next_state = "Single Player Pre-Game Settings"

			if self.local_multiplayer_button.is_clicked():
				self.next_state = "Local Single Player Pre-Game Settings"

			# FUTURE TODO: ONLINE MULTIPLAYER
			elif self.multiplayer_button.is_clicked():
				self.next_state = "Multi Player Pre-Game Settings"

			if self.exit_button.is_clicked():
				constants.running = False

	# Handle any rendering that needs to be done
	# INPUT: pygame surface object (window to display to)
	# OUTPUT: All menu attributes/actions are rendered
	def render(self, window):
		# background
		window.blit(self.menu_background, self.menu_background.get_rect(center = window.get_rect().center))
		window.blit(self.playboard, self.playboard.get_rect(center = window.get_rect().center))
		window.blit(self.button_background, 
					self.button_background.get_rect(center = window.get_rect().center))
		
		# draw buttons to window
		self.singleplayer_button.draw_button(window)
		self.local_multiplayer_button.draw_button(window)
		self.multiplayer_button.draw_button(window)
		self.exit_button.draw_button(window)

# SUBCLASS for pregame settings
# What does it contain?
#  - loads and renders board, color selection, piece style, piece preview, and play button
#  - handles button presses for those menus
#  - inits board and players
class PreGameSettings(State):
	def __init__(self, window):
		super().__init__() # inherit the parent initializer
		self.next_state = None
		self.font = pygame.font.SysFont("Arial",size=35)
		self.ai_level = "Easy"
		# player and opponent will be created here to be inherited
		self.host = player.Player(is_host=True, board_perspective="Bottom")

		# host retains last settings, guest is opposite
		if self.host.color == "Cho":
			self.guest.color = "Han"
		else:
			self.guest.color = "Cho"

		self.load_button_background()
		self.load_board_boarder(window)
		self.load_board()
		self.load_player_color_menu()
		self.load_piece_convention_menu()
		self.load_play_button()
		self.load_player_piece_preview()

	def handle_event(self, event):
		pass

	def handle_left_cick(self, event):
		if self.is_left_click(event):
			# PLAY AS CHO
			if self.cho_side_button.is_clicked():
				self.host.color ="Cho"
				self.guest.color = "Han"
			# PLAY AS HAN
			elif self.han_side_button.is_clicked():
				self.host.color = "Han"
				self.guest.color = "Cho"
			# PLAY WITH STANDARD PIECE LOGOS
			elif self.standard_piece_convention_button.is_clicked():
				self.host.piece_convention = "Standard"
				self.guest.piece_convention = "Standard"
			# PLAY WITH INTERNATIONAL PIECE LOGOS
			elif self.internat_piece_convention_button.is_clicked():
				self.host.piece_convention = "International"
				self.guest.piece_convention = "International"
			# CLICK CONFIRM SETTINGS IF ALL ARE SET
			elif (self.play_button.is_clicked() 
		 		  and self.host is not None):
				helper_funcs.update_player_settings(self.host)
				self.next_state = "Single Player Game"

		elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
			self.next_state = "Main Menu"

	def render(self, window):
		self.render_board(window)
		self.render_player_color_menu(window)
		self.render_piece_convention_menu(window)
		self.render_player_piece_preview(window)
		self.render_play_button(window)

#--------------------------------------------------------------------------------
# THIS STATE WILL HANDLE SETTINGS FOR SETTING UP THE GAME AGAINST AN AI
#--------------------------------------------------------------------------------
class SinglePlayerPreGameSettings(PreGameSettings):

	# initialize the settings for the game
	# INPUT: No Input
	# OUTPUT: Settings menu is ready to be interacted with by player
	def __init__(self, window):
		self.guest = ai.OpponentAI(is_host=False, board_perspective="Top")
		super().__init__(window)
		self.load_ai_buttons()

	def handle_event(self, event):
		self.handle_left_cick(event)
		for button in self.ai_level_buttons:
			if button.is_clicked():
				self.ai_level = button.text
				self.host.ai_level = button.text
				self.guest.ai_level = button.text
				
	def render(self, window):
		super().render(window)
		self.render_ai_buttons(window)


	def load_ai_buttons(self):
		self.ai_level_buttons = []

		# easy button
		x, y = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["single_player"]["easy_ai_button"]["location"]
		width, height = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["single_player"]["easy_ai_button"]["size"]
		font = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["single_player"]["easy_ai_button"]["text"]["font"]
		text = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["single_player"]["easy_ai_button"]["text"]["string"]
		foreground_color = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["single_player"]["easy_ai_button"]["text"]["foreground_color"]
		background_color = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["single_player"]["easy_ai_button"]["text"]["background_color"]
		hover_color = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["single_player"]["easy_ai_button"]["text"]["hover_color"]
		self.easy_ai_button = (button.Button(x, y, width, height, font, text, foreground_color, background_color, hover_color))
		self.ai_level_buttons.append(self.easy_ai_button)

		# medium button
		x, y = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["single_player"]["medium_ai_button"]["location"]
		width, height = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["single_player"]["medium_ai_button"]["size"]
		font = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["single_player"]["medium_ai_button"]["text"]["font"]
		text = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["single_player"]["medium_ai_button"]["text"]["string"]
		foreground_color = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["single_player"]["medium_ai_button"]["text"]["foreground_color"]
		background_color = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["single_player"]["medium_ai_button"]["text"]["background_color"]
		hover_color = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["single_player"]["medium_ai_button"]["text"]["hover_color"]
		self.medium_ai_button = (button.Button(x, y, width, height, font, text, foreground_color, background_color, hover_color))
		self.ai_level_buttons.append(self.medium_ai_button)

		# hard button
		x, y = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["single_player"]["hard_ai_button"]["location"]
		width, height = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["single_player"]["hard_ai_button"]["size"]
		font = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["single_player"]["hard_ai_button"]["text"]["font"]
		text = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["single_player"]["hard_ai_button"]["text"]["string"]
		foreground_color = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["single_player"]["hard_ai_button"]["text"]["foreground_color"]
		background_color = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["single_player"]["hard_ai_button"]["text"]["background_color"]
		hover_color = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["single_player"]["hard_ai_button"]["text"]["hover_color"]
		self.hard_ai_button = (button.Button(x, y, width, height, font, text, foreground_color, background_color, hover_color))
		self.ai_level_buttons.append(self.hard_ai_button)

	def render_ai_buttons(self, window):
		window.blit(self.piece_convention_background, 
			   constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["single_player"]["button_background"]["ai_level"]["location"])
		text = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["single_player"]["button_background"]["ai_level"]["text"]["string"]
		x, y = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["single_player"]["button_background"]["ai_level"]["text"]["location"]
		font_size = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["single_player"]["button_background"]["ai_level"]["text"]["font_size"]
		
		self.draw_text(window, text, x, y, font_size)
		text = self.host.ai_level
		x, y = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["single_player"]["button_background"]["ai_level"]["text"]["chosen_diff_location"]
		font_size = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["single_player"]["button_background"]["ai_level"]["text"]["font_size"]
		self.draw_text(window, text, x, y, font_size)

		for button in self.ai_level_buttons:
			button.draw_button(window)

#--------------------------------------------------------------------------------
# Inherited State for single player gaming against an ai
#--------------------------------------------------------------------------------
class SinglePlayerGame(SinglePlayerPreGameSettings):
	
	# initialize the gamestate
	# INPUT: No Input
	# OUTPUT: Gamestate is initialized and ready for playing

	def __init__(self, window):
		super().__init__(window)
		# load then display board image
		self.load_board_boarder(window)
		self.load_board()

		# swap left-horse button
		x, y = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["single_player"]["swap_left_horse_button"]["location"]
		width, height = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["single_player"]["swap_left_horse_button"]["size"]
		font = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["single_player"]["swap_left_horse_button"]["text"]["font"]
		text = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["single_player"]["swap_left_horse_button"]["text"]["string"]
		foreground_color = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["single_player"]["swap_left_horse_button"]["text"]["foreground_color"]
		background_color = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["single_player"]["swap_left_horse_button"]["text"]["background_color"]
		hover_color = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["single_player"]["swap_left_horse_button"]["text"]["hover_color"]
		self.swap_left_horse_button = (button.Button(x, y, width, height, font, text, foreground_color, background_color, hover_color))

		# swap right-horse  button
		x, y = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["single_player"]["swap_right_horse_button"]["location"]
		width, height = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["single_player"]["swap_right_horse_button"]["size"]
		font = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["single_player"]["swap_right_horse_button"]["text"]["font"]
		text = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["single_player"]["swap_right_horse_button"]["text"]["string"]
		foreground_color = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["single_player"]["swap_right_horse_button"]["text"]["foreground_color"]
		background_color = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["single_player"]["swap_right_horse_button"]["text"]["background_color"]
		hover_color = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["single_player"]["swap_right_horse_button"]["text"]["hover_color"]
		self.swap_right_horse_button = (button.Button(x, y, width, height, font, text, foreground_color, background_color, hover_color))

		# swap left-horse background
		self.swap_left_horse_background = pygame.image.load("UI/Button_Background.png").convert_alpha()
		self.swap_left_horse_background = pygame.transform.rotate(self.swap_left_horse_background, 180)
		self.swap_left_horse_background = pygame.transform.scale(self.swap_left_horse_background,
				constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["single_player"]["button_background"]["swap_left_horse"]["size"])

		# swap right-horse background
		self.swap_right_horse_background = pygame.image.load("UI/Button_Background.png").convert_alpha()
		self.swap_right_horse_background = pygame.transform.rotate(self.swap_right_horse_background, 180)
		self.swap_right_horse_background = pygame.transform.scale(self.swap_right_horse_background,
				constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["single_player"]["button_background"]["swap_right_horse"]["size"])
		
		# confirm swap button
		x, y = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["single_player"]["confirm_swap_button"]["location"]
		width, height = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["single_player"]["confirm_swap_button"]["size"]
		font = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["single_player"]["confirm_swap_button"]["text"]["font"]
		text = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["single_player"]["confirm_swap_button"]["text"]["string"]
		foreground_color = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["single_player"]["confirm_swap_button"]["text"]["foreground_color"]
		background_color = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["single_player"]["confirm_swap_button"]["text"]["background_color"]
		hover_color = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["single_player"]["confirm_swap_button"]["text"]["hover_color"]
		self.confirm_swap_button = (button.Button(x, y, width, height, font, text, foreground_color, background_color, hover_color))

		# confirm swap button background
		self.confirm_swap_button_background = pygame.image.load("UI/Button_Background_Poly.png").convert_alpha()
		self.confirm_swap_button_background = pygame.transform.scale(self.confirm_swap_button_background,
				constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["single_player"]["button_background"]["confirm_swap"]["size"])
		
		# condition warning/turn tab
		self.game_state_background = pygame.image.load("UI/Button_Background.png").convert_alpha()
		self.game_state_background = pygame.transform.scale(self.game_state_background,
				constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["single_player"]["button_background"]["game_state"]["size"])
		
		# game over pop-up display
		self.game_over_background = pygame.image.load("UI/Button_Background.png").convert_alpha()
		self.game_over_background = pygame.transform.scale(self.game_over_background,
				constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["single_player"]["button_background"]["game_over"]["size"])

		# create game objects
		self.board = board.Board()

		# pre-set ai if it goes first
		# Han player chooses first horse swaps
		if self.guest.color == "Han":
			helper_funcs.choose_ai_lineup(self.guest)
			self.active_player = self.host
			self.waiting_player = self.guest
		else:
			self.active_player = self.guest
			self.waiting_player = self.host

	# Listen for and handle any event ticks (clicks/buttons)
	# INPUT: pygame event object
	# OUTPUT: User triggered game events are handled appropriately
	def handle_event(self, event):
		self.immediate_render = False
		# get the player's mouse position for click tracking
		mouse_pos = pygame.mouse.get_pos()

		# check for game over conditions at the top of the player's turn
		if self.is_game_over():
				self.game_over = True
				self.winner = self.guest

		# listen for an event trigger via click from right-mouse-button
		elif self.is_left_click(event) and not self.game_over:
				
				# OPENING TURN ONLY
				if self.opening_turn:
					self.handle_swap()

				# GAMEPLAY TURN
				# if it is player's turn
				elif self.host.is_turn:

					# if player is attempting to move a piece
					if self.host.is_clicked:
						self.handle_piece_move(self.host, self.guest, mouse_pos)

					# otherwise, check if any player-side pieces were clicked
					elif helper_funcs.player_piece_clicked(self.host, mouse_pos):
						# FUTURE LOGIC HERE
						pass

		# if RMB clicked and ...
		elif (self.is_right_click(event) 
				and self.host.is_turn 
				and not self.bikjang 
				and not self.check
				and not self.game_over):

				if self.host is not None:
					helper_funcs.player_piece_unclick(self.host)
					# KING piece is always the first piece in the list
					if self.host.pieces[0].collision_rect.collidepoint(mouse_pos):
						# swap turns
						self.swap_turn()

		# escape from game to main menu
		if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
			self.next_state = "Main Menu"

#--------------------------------------------------------------------------------
# AI STUFF IS HERE
		# Handle AI Opponent's turn
		# check for game over conditions at the top of the ai's turn
		if self.is_game_over():
				self.game_over = True
				self.winner = self.host

		# ai move logic
		elif not self.immediate_render and self.guest.is_turn and not self.opening_turn and not self.game_over:
			new_board = self.guest.convert_board(self.board, self.host)
			fen = self.guest.generate_fen(new_board)
				
			self.print_fen("AI:")

			if self.ai_level == "Easy":
				depth = 1
			elif self.ai_level == "Medium":
				depth = 5
			elif self.ai_level == "Hard":
				depth = 10
			
			self.guest.send_command(f"position fen {fen}")
			self.guest.send_command(f"go depth {str(depth)}")
			best_move = self.guest.get_engine_move()
			
			if helper_funcs.ai_move(self.host, self.guest, self.board, best_move, new_board, fen):
				if helper_funcs.detect_bikjang(self.guest, self.host):
					self.bikjang = True
					self.winner = self.guest
					self.condition = "Bikjang"
					self.game_over = True

				elif helper_funcs.detect_check(self.host, self.guest, self.board):
					self.check = True
					self.condition = "Check"
			
			self.swap_turn()
			self.guest.is_checked = False

	# Handle any rendering that needs to be done
	# INPUT: pygame surface object (window to display to)
	# OUTPUT: All game attributes/actions are rendered
	def render(self, window):
		# display board to window
		window.blit(self.menu_background, self.menu_background.get_rect(center = window.get_rect().center))
		window.blit(self.playboard, self.playboard.get_rect(center = window.get_rect().center))

		# DISPLAY THE OPTION TO SWAP HORSES AT THE START OF THE GAME
		if self.opening_turn:
			window.blit(self.swap_left_horse_background, 
			   constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["single_player"]["button_background"]["swap_left_horse"]["location"])
			self.swap_left_horse_button.draw_button(window)

			window.blit(self.swap_right_horse_background,
			   constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["single_player"]["button_background"]["swap_right_horse"]["location"])
			self.swap_right_horse_button.draw_button(window)

		# if player has a piece currently clicked, render where it can go
		if self.host is not None and self.host.is_clicked:
			render_funcs.render_possible_spots(self.host, self.guest, self.board, window, self.condition)

		# render collision rectangles for the pieces on both sides
		#render_funcs.render_piece_collisions(self.active_player, self.waiting_player, window)

		# display confirm button for swapping pieces
		if self.opening_turn:
			# confirm swap button
			window.blit(self.confirm_swap_button_background,
			   constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["single_player"]["button_background"]["confirm_swap"]["location"])
			self.confirm_swap_button.draw_button(window)

		# HIGHLIGHT BIKJANG/CHECK CONDITIONS WHEN APPLICABLE
		if self.bikjang:
			render_funcs.render_bikjang_highlight(self.host, self.guest, window)
		if self.check:
			if self.guest.is_checked:
				render_funcs.render_check_highlight(self.guest, window)
			else:
				render_funcs.render_check_highlight(self.host, window)

		render_funcs.render_pieces(self.host, self.guest, window)

		# DISPLAY END GAME CONDITIONS/GAME_STATES
		# BIKJANG CONDITION
		if self.game_over and self.bikjang:
			self.render_bikjang_ending(window)

		# GAME ENDING CHECK
		if self.game_over and self.check:
			self.render_check_ending(window)

	# Prints out the fen string of the current board

	# inverts turn flags and swaps the active and waiting player variables
	def swap_turn(self):
		self.host.is_turn = not self.host.is_turn
		self.guest.is_turn = not self.guest.is_turn

		if self.active_player == self.host:
			self.active_player = self.guest
			self.waiting_player = self.host
		else:
			self.active_player = self.host
			self.waiting_player = self.guest

	# player may swap horses with elephants, confirm swap to end turn
	# Han player chooses first then Cho
	def handle_swap(self):
		if self.swap_right_horse_button.is_clicked():
			helper_funcs.swap_pieces(self.host, self.host.pieces[6], self.host.pieces[4])

		elif self.swap_left_horse_button.is_clicked():
			helper_funcs.swap_pieces(self.host, self.host.pieces[5], self.host.pieces[3])
		
		elif self.confirm_swap_button.is_clicked():
			self.opening_turn = False
			if self.guest.color == "Cho":
				helper_funcs.choose_ai_lineup(self.guest)
				self.host.is_turn = False
				self.guest.is_turn = True
			else:
				self.host.is_turn = True
				self.guest.is_turn = False

#--------------------------------------------------------------------------------
class LocalSinglePlayerPreGameSettings(PreGameSettings):


	# initialize the settings for the game
	# INPUT: No Input
	# OUTPUT: Settings menu is ready to be interacted with by player
	def __init__(self, window):
		self.guest = player.Player(is_host=False, board_perspective="Top")
		super().__init__(window)

	# Listen for and handle any event ticks (clicks/buttons)
	# INPUT: pygame event object
	# OUTPUT: settings are set accordingly
	def handle_event(self, event):
		self.handle_left_cick(event)
				
	# Handle any rendering that needs to be done
	# INPUT: pygame surface object (window to display to)
	# OUTPUT: All pre-game settings attributes/actions are rendered
	def render(self, window):
		super().render(window)
#--------------------------------------------------------------------------------
# Inherited State for single player gaming against an ai
#--------------------------------------------------------------------------------
class LocalSinglePlayerGame(LocalSinglePlayerPreGameSettings):

	# initialize the gamestate
	# INPUT: No Input
	# OUTPUT: Gamestate is initialized and ready for playing
	def __init__(self, window):
		super().__init__(window)
		# load then display board image
		self.load_board_boarder(window)
		self.load_board()

		# host-side swap left-horse button
		x, y = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["local_MP"]["host_swap_left_horse_button"]["location"]
		width, height = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["local_MP"]["host_swap_left_horse_button"]["size"]
		font = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["local_MP"]["host_swap_left_horse_button"]["text"]["font"]
		text = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["local_MP"]["host_swap_left_horse_button"]["text"]["string"]
		foreground_color = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["local_MP"]["host_swap_left_horse_button"]["text"]["foreground_color"]
		background_color = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["local_MP"]["host_swap_left_horse_button"]["text"]["background_color"]
		hover_color = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["local_MP"]["host_swap_left_horse_button"]["text"]["hover_color"]
		self.host_swap_left_horse_button = (button.Button(x, y, width, height, font, text, foreground_color, background_color, hover_color))

		# host-side swap right-horse  button
		x, y = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["local_MP"]["host_swap_right_horse_button"]["location"]
		width, height = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["local_MP"]["host_swap_right_horse_button"]["size"]
		font = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["local_MP"]["host_swap_right_horse_button"]["text"]["font"]
		text = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["local_MP"]["host_swap_right_horse_button"]["text"]["string"]
		foreground_color = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["local_MP"]["host_swap_right_horse_button"]["text"]["foreground_color"]
		background_color = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["local_MP"]["host_swap_right_horse_button"]["text"]["background_color"]
		hover_color = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["local_MP"]["host_swap_right_horse_button"]["text"]["hover_color"]
		self.host_swap_right_horse_button = (button.Button(x, y, width, height, font, text, foreground_color, background_color, hover_color))

		# host-side swap left-horse background
		self.host_swap_left_horse_background = pygame.image.load("UI/Button_Background.png").convert_alpha()
		self.host_swap_left_horse_background = pygame.transform.rotate(self.host_swap_left_horse_background, 180)
		self.host_swap_left_horse_background = pygame.transform.scale(self.host_swap_left_horse_background,
				constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["local_MP"]["button_background"]["host_swap_left_horse"]["size"])

		# host-side swap right-horse background
		self.host_swap_right_horse_background = pygame.image.load("UI/Button_Background.png").convert_alpha()
		self.host_swap_right_horse_background = pygame.transform.rotate(self.host_swap_right_horse_background, 180)
		self.host_swap_right_horse_background = pygame.transform.scale(self.host_swap_right_horse_background,
				constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["local_MP"]["button_background"]["host_swap_right_horse"]["size"])
		
		# host-side confirm swap button
		x, y = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["local_MP"]["host_confirm_swap_button"]["location"]
		width, height = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["local_MP"]["host_confirm_swap_button"]["size"]
		font = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["local_MP"]["host_confirm_swap_button"]["text"]["font"]
		text = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["local_MP"]["host_confirm_swap_button"]["text"]["string"]
		foreground_color = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["local_MP"]["host_confirm_swap_button"]["text"]["foreground_color"]
		background_color = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["local_MP"]["host_confirm_swap_button"]["text"]["background_color"]
		hover_color = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["local_MP"]["host_confirm_swap_button"]["text"]["hover_color"]
		self.host_confirm_swap_button = (button.Button(x, y, width, height, font, text, foreground_color, background_color, hover_color))

		# host-side confirm swap button background
		self.host_confirm_swap_button_background = pygame.image.load("UI/Button_Background_Poly.png").convert_alpha()
		self.host_confirm_swap_button_background = pygame.transform.scale(self.host_confirm_swap_button_background,
				constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["local_MP"]["button_background"]["host_confirm_swap"]["size"])
		
		# guest-side swap left-horse button
		x, y = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["local_MP"]["guest_swap_left_horse_button"]["location"]
		width, height = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["local_MP"]["guest_swap_left_horse_button"]["size"]
		font = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["local_MP"]["guest_swap_left_horse_button"]["text"]["font"]
		text = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["local_MP"]["guest_swap_left_horse_button"]["text"]["string"]
		foreground_color = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["local_MP"]["guest_swap_left_horse_button"]["text"]["foreground_color"]
		background_color = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["local_MP"]["guest_swap_left_horse_button"]["text"]["background_color"]
		hover_color = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["local_MP"]["guest_swap_left_horse_button"]["text"]["hover_color"]
		self.guest_swap_left_horse_button = (button.Button(x, y, width, height, font, text, foreground_color, background_color, hover_color))

		# guest-side swap right-horse  button
		x, y = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["local_MP"]["guest_swap_right_horse_button"]["location"]
		width, height = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["local_MP"]["guest_swap_right_horse_button"]["size"]
		font = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["local_MP"]["guest_swap_right_horse_button"]["text"]["font"]
		text = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["local_MP"]["guest_swap_right_horse_button"]["text"]["string"]
		foreground_color = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["local_MP"]["guest_swap_right_horse_button"]["text"]["foreground_color"]
		background_color = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["local_MP"]["guest_swap_right_horse_button"]["text"]["background_color"]
		hover_color = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["local_MP"]["guest_swap_right_horse_button"]["text"]["hover_color"]
		self.guest_swap_right_horse_button = (button.Button(x, y, width, height, font, text, foreground_color, background_color, hover_color))

		# guest-side swap left-horse background
		self.guest_swap_left_horse_background = pygame.image.load("UI/Button_Background.png").convert_alpha()
		self.guest_swap_left_horse_background = pygame.transform.scale(self.guest_swap_left_horse_background,
				constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["local_MP"]["button_background"]["guest_swap_left_horse"]["size"])

		# guest-side swap right-horse background
		self.guest_swap_right_horse_background = pygame.image.load("UI/Button_Background.png").convert_alpha()
		self.guest_swap_right_horse_background = pygame.transform.scale(self.guest_swap_right_horse_background,
				constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["local_MP"]["button_background"]["guest_swap_right_horse"]["size"])
		
		# guest-side confirm swap button
		x, y = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["local_MP"]["guest_confirm_swap_button"]["location"]
		width, height = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["local_MP"]["guest_confirm_swap_button"]["size"]
		font = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["local_MP"]["guest_confirm_swap_button"]["text"]["font"]
		text = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["local_MP"]["guest_confirm_swap_button"]["text"]["string"]
		foreground_color = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["local_MP"]["guest_confirm_swap_button"]["text"]["foreground_color"]
		background_color = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["local_MP"]["guest_confirm_swap_button"]["text"]["background_color"]
		hover_color = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["local_MP"]["guest_confirm_swap_button"]["text"]["hover_color"]
		self.guest_confirm_swap_button = (button.Button(x, y, width, height, font, text, foreground_color, background_color, hover_color))

		# guest-side confirm swap button background
		self.guest_confirm_swap_button_background = pygame.image.load("UI/Button_Background_Poly.png").convert_alpha()
		self.guest_confirm_swap_button_background = pygame.transform.scale(self.guest_confirm_swap_button_background,
				constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["local_MP"]["button_background"]["guest_confirm_swap"]["size"])

		# condition warning/turn tab
		self.game_state_background = pygame.image.load("UI/Button_Background.png").convert_alpha()
		self.game_state_background = pygame.transform.scale(self.game_state_background,
				constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["local_MP"]["button_background"]["game_state"]["size"])
		
		# game over pop-up display
		self.game_over_background = pygame.image.load("UI/Button_Background.png").convert_alpha()
		self.game_over_background = pygame.transform.scale(self.game_over_background,
				constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["local_MP"]["button_background"]["game_over"]["size"])

		# create game objects
		self.board = board.Board()
		self.han_player = self.host if self.host.color == "Han" else self.guest
		self.cho_player = self.guest if self.guest.color == "Cho" else self.host
		self.active_player = None
		self.waiting_player = None
	# Listen for and handle any event ticks (clicks/buttons)
	# INPUT: pygame event object
	# OUTPUT: User triggered game events are handled appropriately
	def handle_event(self, event):
		# get the player's mouse position for click tracking
		mouse_pos = pygame.mouse.get_pos()
		# check for game over conditions at the top of the turn
		if self.is_game_over():
				self.game_over = True
				self.winner = self.waiting_player

		# listen for an event trigger via click from left-mouse-button
		if self.is_left_click(event) and not self.game_over:
			# OPENING TURN ONLY
			if self.opening_turn and not self.han_player.is_ready:
				# player may swap horses with elephants, confirm swap to end turn
				# Han player chooses first then Cho
				# HAN IS HOST
				if self.han_player.is_host:
					if self.host_swap_right_horse_button.is_clicked():
						helper_funcs.swap_pieces(self.han_player, self.han_player.pieces[6], self.han_player.pieces[4])
					
					elif self.host_swap_left_horse_button.is_clicked():
						helper_funcs.swap_pieces(self.han_player, self.han_player.pieces[5], self.han_player.pieces[3])
					
					elif self.host_confirm_swap_button.is_clicked():
						self.waiting_player = self.han_player
						self.waiting_player.is_ready = True
				
				# HAN IS GUEST
				else:
					if self.guest_swap_right_horse_button.is_clicked():
						helper_funcs.swap_pieces(self.han_player, self.han_player.pieces[6], self.han_player.pieces[4])
					elif self.guest_swap_left_horse_button.is_clicked():
						helper_funcs.swap_pieces(self.han_player, self.han_player.pieces[5], self.han_player.pieces[3])
					elif self.guest_confirm_swap_button.is_clicked():
						self.waiting_player = self.han_player
						self.waiting_player.is_ready = True
			
			# Cho player chooses second
			elif self.opening_turn and not self.cho_player.is_ready:
				# CHO IS HOST
				if self.cho_player.is_host:
					if self.host_swap_right_horse_button.is_clicked():
						helper_funcs.swap_pieces(self.cho_player, self.cho_player.pieces[6], self.cho_player.pieces[4])
					
					elif self.host_swap_left_horse_button.is_clicked():
						helper_funcs.swap_pieces(self.cho_player, self.cho_player.pieces[5], self.cho_player.pieces[3])
					
					elif self.host_confirm_swap_button.is_clicked():
						self.active_player = self.cho_player
						self.active_player.is_ready = True
						self.opening_turn = False
				
				# CHO IS GUEST
				else:
					if self.guest_swap_right_horse_button.is_clicked():
						helper_funcs.swap_pieces(self.cho_player, self.cho_player, self.cho_player.pieces[6], self.cho_player.pieces[4])

					elif self.guest_swap_left_horse_button.is_clicked():
						helper_funcs.swap_pieces(self.cho_player, self.cho_player, self.cho_player.pieces[5], self.cho_player.pieces[3])

					elif self.guest_confirm_swap_button.is_clicked():
						self.active_player = self.cho_player
						self.active_player.is_ready = True
						self.active_player.is_turn = True
						self.opening_turn = False

			# check if the player is currently attempting to move a piece
			elif self.active_player is not None and self.active_player.is_clicked:
				# unclick that piece if the move was successful/valid
				self.handle_piece_move(self.active_player, self.waiting_player, mouse_pos)

			# otherwise, check if any player-side pieces were clicked
			elif helper_funcs.player_piece_clicked(self.active_player, mouse_pos):
				# FUTURE LOGIC HERE
				pass

		# right-clicking your king will pass the turn
		elif (event.type == pygame.MOUSEBUTTONDOWN and event.button == 3 
			and self.condition == "None" 
			and not self.opening_turn 
			and not self.game_over):
			if self.active_player is not None:
				helper_funcs.player_piece_unclick(self.active_player)
				# KING piece is always the first piece in the list
				if self.active_player.pieces[0].collision_rect.collidepoint(mouse_pos):
					# swap turns
					temp_info = self.active_player
					self.active_player = self.waiting_player
					self.waiting_player = temp_info

		# escape from game to main menu
		elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
			self.next_state = "Main Menu"
			
	# Handle any rendering that needs to be done
	# INPUT: pygame surface object (window to display to)
	# OUTPUT: All game attributes/actions are rendered
	def render(self, window):
		# display board to window
		self.render_board()

		# DISPLAY THE OPTION TO SWAP HORSES AT THE START OF THE GAME
		# HAN
		if self.opening_turn and not self.han_player.is_ready:
			# HOST (BOTTOM-VIEW)
			if self.han_player.is_host:
				button_key = "host"
				window.blit(self.host_swap_left_horse_background, 
					constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["local_MP"]["button_background"][f"{button_key}_swap_left_horse"]["location"])
				self.host_swap_left_horse_button.draw_button(window)

				window.blit(self.host_swap_right_horse_background,
					constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["local_MP"]["button_background"][f"{button_key}_swap_right_horse"]["location"])
				self.host_swap_right_horse_button.draw_button(window)
			# GUEST (TOP-VIEW)
			else:
				button_key = "guest"
				window.blit(self.guest_swap_left_horse_background, 
					constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["local_MP"]["button_background"][f"{button_key}_swap_left_horse"]["location"])
				self.guest_swap_left_horse_button.draw_button(window)

				window.blit(self.guest_swap_right_horse_background,
					constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["local_MP"]["button_background"][f"{button_key}_swap_right_horse"]["location"])
				self.guest_swap_right_horse_button.draw_button(window)
		# CHO
		elif self.opening_turn and not self.cho_player.is_ready:
			# HOST (BOTTOM-VIEW)
			if self.cho_player.is_host:
				button_key = "host"
				window.blit(self.host_swap_left_horse_background, 
					constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["local_MP"]["button_background"][f"{button_key}_swap_left_horse"]["location"])
				self.host_swap_left_horse_button.draw_button(window)

				window.blit(self.host_swap_right_horse_background,
					constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["local_MP"]["button_background"][f"{button_key}_swap_right_horse"]["location"])
				self.host_swap_right_horse_button.draw_button(window)
			# GUEST (TOP-VIEW)
			else:
				button_key = "guest"
				window.blit(self.guest_swap_left_horse_background, 
					constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["local_MP"]["button_background"][f"{button_key}_swap_left_horse"]["location"])
				self.guest_swap_left_horse_button.draw_button(window)

				window.blit(self.guest_swap_right_horse_background,
					constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["local_MP"]["button_background"][f"{button_key}_swap_right_horse"]["location"])
				self.guest_swap_right_horse_button.draw_button(window)

		# DISPLAY CONFIRM FOR PIECE SWAP
		# Han
		if self.opening_turn and not self.han_player.is_ready:
			if self.han_player.is_host:
				button_key = "host"
				window.blit(self.host_confirm_swap_button_background,
			  		 constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["local_MP"]["button_background"][f"{button_key}_confirm_swap"]["location"])
				self.host_confirm_swap_button.draw_button(window)
			else:
				button_key = "guest"
				window.blit(self.guest_confirm_swap_button_background,
			   constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["local_MP"]["button_background"][f"{button_key}_confirm_swap"]["location"])
				self.guest_confirm_swap_button.draw_button(window)
		# Cho
		elif self.opening_turn and not self.cho_player.is_ready:
			if self.cho_player.is_host:
				button_key = "host"
				window.blit(self.host_confirm_swap_button_background,
			  		 constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["local_MP"]["button_background"][f"{button_key}_confirm_swap"]["location"])
				self.host_confirm_swap_button.draw_button(window)
			else:
				button_key = "guest"
				window.blit(self.guest_confirm_swap_button_background,
			   constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["local_MP"]["button_background"][f"{button_key}_confirm_swap"]["location"])
				self.guest_confirm_swap_button.draw_button(window)

		# RENDER WHERE CLICKED PIECE MAY GO
		if self.active_player is not None and self.active_player.is_clicked:
			render_funcs.render_possible_spots(self.active_player, self.waiting_player, self.board, window, self.condition)

		# HIGHLIGHT BIKJANG/CHECK CONDITIONS WHEN APPLICABLE
		if self.bikjang:
			render_funcs.render_bikjang_highlight(self.active_player, self.waiting_player, window)
		if self.check:
			render_funcs.render_check_highlight(self.active_player, window)

		# DISPLAY PIECES
		if self.active_player is not None and self.waiting_player is not None:
			render_funcs.render_pieces(self.active_player, self.waiting_player, window)

		# COVER CASE WHERE NO PLAYER HAS STARTED THEIR TURN YET
		else:
			render_funcs.render_pieces(self.host, self.guest, window)

		# DISPLAY END GAME CONDITIONS/GAME_STATES
		if self.game_over and self.bikjang:
			self.render_bikjang_ending(window)

		if self.game_over and self.check:
			self.render_check_ending(window)

	def swap_turn(self):
		self.active_player, self. waiting_player = self.waiting_player, self.active_player


class MultiplayerPreGameSettings(PreGameSettings):
	def __init__(self, window):
		super().__init__(window)
		self.guest = player.Player(is_host=False, board_perspective="Top")

		
	# Listen for and handle any event ticks (clicks/buttons)
	# INPUT: pygame event object
	# OUTPUT: settings are set accordingly
	def handle_event(self, event):
		self.handle_left_cick(event)
				
	# Handle any rendering that needs to be done
	# INPUT: pygame surface object (window to display to)
	# OUTPUT: All pre-game settings attributes/actions are rendered
	def render(self, window):
		super().render(window)

class Multiplayer(MultiplayerPreGameSettings):

	def __init__(self, window):
		super().__init__(window)
		self.load_board_boarder(window)
		self.load_board()

		self.host = player.Player(is_host=True, board_perspective="Bottom")
		self.guest = player.Player(is_host=False, board_perspective="Top")
		self.active_player = self.host
		self.waiting_player = self.guest

		self.board = board.Board()

		self.load_swap_menu()

	def handle_event(self, event):
		self.immediate_render = False
		# get the player's mouse position for click tracking
		mouse_pos = pygame.mouse.get_pos()

	# check for game over conditions at the top of the player's turn
		if self.is_game_over():
				self.game_over = True
				self.winner = self.guest

		# listen for an event trigger via click from right-mouse-button
		elif self.is_left_click(event) and not self.game_over:
				
			# OPENING TURN ONLY
			if self.opening_turn:
				self.handle_swap()

			# GAMEPLAY TURN
			# if it is player's turn
			elif self.host.is_turn:

				# if player is attempting to move a piece
				if self.host.is_clicked:
					self.handle_piece_move(self.host, self.guest, mouse_pos)

				# otherwise, check if any player-side pieces were clicked
				elif helper_funcs.player_piece_clicked(self.host, mouse_pos):
					# FUTURE LOGIC HERE
					pass

				self.board.update_board_pieces(self.host, self.guest)
				print(self.board.get_fen(self.host))

		# if RMB clicked and ...
		elif (self.is_right_click(event) 
			  and self.host.is_turn and not self.bikjang and not self.check and not self.game_over):

				helper_funcs.player_piece_unclick(self.host)
				# KING piece is always the first piece in the list
				if self.host.pieces[0].collision_rect.collidepoint(mouse_pos):
					self.swap_turn()

		# escape from game to main menu
		if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
			self.next_state = "Main Menu"

		self.swap_turn()

	def render(self, window):
		window.blit(self.menu_background, self.menu_background.get_rect(center = window.get_rect().center))
		window.blit(self.playboard, self.playboard.get_rect(center = window.get_rect().center))

		self.render_swap_menu(window)

		render_funcs.render_pieces(self.host, self.guest, window)

	def handle_swap(self):
		if self.swap_right_horse_button.is_clicked():
			helper_funcs.swap_pieces(self.host, self.host.pieces[6], self.host.pieces[4])

		elif self.swap_left_horse_button.is_clicked():
			helper_funcs.swap_pieces(self.host, self.host.pieces[5], self.host.pieces[3])
		
		elif self.confirm_swap_button.is_clicked():
			self.opening_turn = False
			if self.guest.color == "Cho":
				self.host.is_turn = False
				self.guest.is_turn = True
			else:
				self.host.is_turn = True
				self.guest.is_turn = False

	def render_swap_menu(self, window):		
		# DISPLAY THE OPTION TO SWAP HORSES AT THE START OF THE GAME
		if self.opening_turn:
			window.blit(self.swap_left_horse_background, 
			   constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["single_player"]["button_background"]["swap_left_horse"]["location"])
			self.swap_left_horse_button.draw_button(window)

			window.blit(self.swap_right_horse_background,
			   constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["single_player"]["button_background"]["swap_right_horse"]["location"])
			self.swap_right_horse_button.draw_button(window)

		# if player has a piece currently clicked, render where it can go
		if self.host is not None and self.host.is_clicked:
			render_funcs.render_possible_spots(self.host, self.guest, self.board, window, self.condition)

		# render collision rectangles for the pieces on both sides
		#render_funcs.render_piece_collisions(self.active_player, self.waiting_player, window)

		# display confirm button for swapping pieces
		if self.opening_turn:
			# confirm swap button
			window.blit(self.confirm_swap_button_background,
			   constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["single_player"]["button_background"]["confirm_swap"]["location"])
			self.confirm_swap_button.draw_button(window)

	# inverts turn flags and swaps the active and waiting player variables
	def swap_turn(self):
		self.host.is_turn = not self.host.is_turn
		self.guest.is_turn = not self.guest.is_turn

		if self.active_player == self.host:
			self.active_player = self.guest
			self.waiting_player = self.host
		else:
			self.active_player = self.host
			self.waiting_player = self.guest
