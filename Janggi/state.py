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

	def load_board_boarder(self, window):
		# Get the current window dimensions.
		current_width, current_height = window.get_size()
		
		# Retrieve the base board border size from constants (this is your base configuration)
		base_size = constants.board_border_size  # e.g. (1080, 1080)
		
		# Scale the size using dynamic_scale_x and dynamic_scale_y
		new_width = helper_funcs.dynamic_scale_x(base_size[0], current_width)
		new_height = helper_funcs.dynamic_scale_y(base_size[1], current_height)
		new_size = (new_width, new_height)
		
		# Load and scale the board border image dynamically.
		self.menu_background = pygame.image.load("Board/Janggi_Board_Border.png").convert_alpha()
		self.menu_background = pygame.transform.scale(self.menu_background, new_size)
		
		# Optionally, update the center if needed.
		self.center = window.get_rect().center

	def load_board(self, window):
		# Get the current window dimensions.
		current_width, current_height = window.get_size()
		
		# Retrieve the base board size from constants (for example, (960, 960))
		base_size = constants.board_size
		
		# Scale the size based on the current window dimensions.
		new_width = helper_funcs.dynamic_scale_x(base_size[0], current_width)
		new_height = helper_funcs.dynamic_scale_y(base_size[1], current_height)
		new_size = (new_width, new_height)
		
		# Load and scale the playboard image dynamically.
		self.playboard = pygame.image.load("Board/Janggi_Board.png").convert_alpha()
		self.playboard = pygame.transform.scale(self.playboard, new_size)
		
		# Update the playboard center based on the scaled menu_background.
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
		# Get current window dimensions.
		current_width, current_height = window.get_size()
		
		# --- Blit the Game Over background ---
		base_bg_loc = constants.resolutions["1920x1080"]["background_elements"]["local_MP"]["button_background"]["game_over"]["location"]
		scaled_bg_loc = (helper_funcs.dynamic_scale_x(base_bg_loc[0], current_width),
                     helper_funcs.dynamic_scale_y(base_bg_loc[1], current_height))
		window.blit(self.game_over_background, scaled_bg_loc)
		
		# --- Draw Game Over notification text ---
		base_notify_text = "Game Over!"
		base_notify_loc = constants.resolutions["1920x1080"]["background_elements"]["local_MP"]["button_background"]["game_over"]["notify_text"]["location"]
		scaled_notify_loc = (helper_funcs.dynamic_scale_x(base_notify_loc[0], current_width),
                         helper_funcs.dynamic_scale_y(base_notify_loc[1], current_height))
		base_notify_font_size = constants.resolutions["1920x1080"]["background_elements"]["local_MP"]["button_background"]["game_over"]["notify_text"]["font_size"]
		scaled_notify_font_size = int(base_notify_font_size * (current_width / 1920))
		self.draw_text(window, base_notify_text, scaled_notify_loc[0], scaled_notify_loc[1], scaled_notify_font_size)
		
		# --- Draw Winner text ---
		base_winner_text = f"{self.winner.color} wins!"
		base_winner_loc = constants.resolutions["1920x1080"]["background_elements"]["local_MP"]["button_background"]["game_over"]["result_text"]["location"]
		scaled_winner_loc = (helper_funcs.dynamic_scale_x(base_winner_loc[0], current_width),
                         helper_funcs.dynamic_scale_y(base_winner_loc[1], current_height))
		base_winner_font_size = constants.resolutions["1920x1080"]["background_elements"]["local_MP"]["button_background"]["game_over"]["result_text"]["font_size"]
		scaled_winner_font_size = int(base_winner_font_size * (current_width / 1920))
		self.draw_text(window, base_winner_text, scaled_winner_loc[0], scaled_winner_loc[1], scaled_winner_font_size)
		
		# --- Draw Reasoning text ---
		base_reason_text = f"Check initiated by {self.winner.color} was unresolvable."
		base_reason_loc = constants.resolutions["1920x1080"]["background_elements"]["local_MP"]["button_background"]["game_over"]["condition_text"]["location"]
		scaled_reason_loc = (helper_funcs.dynamic_scale_x(base_reason_loc[0], current_width),
                         helper_funcs.dynamic_scale_y(base_reason_loc[1], current_height))
		base_reason_font_size = constants.resolutions["1920x1080"]["background_elements"]["local_MP"]["button_background"]["game_over"]["condition_text"]["font_size"]
		scaled_reason_font_size = int(base_reason_font_size * (current_width / 1920))
		self.draw_text(window, base_reason_text, scaled_reason_loc[0], scaled_reason_loc[1], scaled_reason_font_size)
		
	def render_bikjang_ending(self, window):
		current_width, current_height = window.get_size()

		base_bg_loc = constants.resolutions["1920x1080"]["background_elements"]["local_MP"]["button_background"]["game_over"]["location"]
		scaled_bg_loc = (helper_funcs.dynamic_scale_x(base_bg_loc[0], current_width),
                     helper_funcs.dynamic_scale_y(base_bg_loc[1], current_height))
		window.blit(self.game_over_background, scaled_bg_loc)

		base_notify_text = "Game Over!"
		base_notify_loc = constants.resolutions["1920x1080"]["background_elements"]["local_MP"]["button_background"]["game_over"]["notify_text"]["location"]
		scaled_notify_loc = (helper_funcs.dynamic_scale_x(base_notify_loc[0], current_width),
                         helper_funcs.dynamic_scale_y(base_notify_loc[1], current_height))
		base_notify_font_size = constants.resolutions["1920x1080"]["background_elements"]["local_MP"]["button_background"]["game_over"]["notify_text"]["font_size"]
		scaled_notify_font_size = int(base_notify_font_size * (current_width / 1920))
		self.draw_text(window, base_notify_text, scaled_notify_loc[0], scaled_notify_loc[1], scaled_notify_font_size)
		
		base_condition_text = f"Bikjang was initiated by {self.winner.color}."
		base_condition_loc = constants.resolutions["1920x1080"]["background_elements"]["local_MP"]["button_background"]["game_over"]["condition_text"]["location"]
		scaled_condition_loc = (helper_funcs.dynamic_scale_x(base_condition_loc[0], current_width),
                            helper_funcs.dynamic_scale_y(base_condition_loc[1], current_height))
		base_condition_font_size = constants.resolutions["1920x1080"]["background_elements"]["local_MP"]["button_background"]["game_over"]["condition_text"]["font_size"]
		scaled_condition_font_size = int(base_condition_font_size * (current_width / 1920))
		self.draw_text(window, base_condition_text, scaled_condition_loc[0], scaled_condition_loc[1], scaled_condition_font_size)
		
		base_result_text = "Draw..."
		base_result_loc = constants.resolutions["1920x1080"]["background_elements"]["local_MP"]["button_background"]["game_over"]["result_text"]["location"]
		scaled_result_loc = (helper_funcs.dynamic_scale_x(base_result_loc[0], current_width),
                         helper_funcs.dynamic_scale_y(base_result_loc[1], current_height))
		base_result_font_size = constants.resolutions["1920x1080"]["background_elements"]["local_MP"]["button_background"]["game_over"]["result_text"]["font_size"]
		scaled_result_font_size = int(base_result_font_size * (current_width / 1920))
		self.draw_text(window, base_result_text, scaled_result_loc[0], scaled_result_loc[1], scaled_result_font_size)


	def render_board(self, window):
		window.blit(self.menu_background, self.menu_background.get_rect(center = window.get_rect().center))
		window.blit(self.playboard, self.playboard.get_rect(center = window.get_rect().center))

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
	
	def load_button_background(self, window):
		# Get the current window dimensions
		current_width, current_height = window.get_size()
		
		# Retrieve the base size from your base resolution configuration (using "1920x1080" as base)
		base_bg_size = constants.resolutions["1920x1080"]["background_elements"]["local_MP"]["button_background"]["play_as"]["size"]
		
		# Calculate the new size using your dynamic scaling helper functions
		new_bg_size = (
        	helper_funcs.dynamic_scale_x(base_bg_size[0], current_width),
        	helper_funcs.dynamic_scale_y(base_bg_size[1], current_height)
    	)
		
		# Load and scale the button background image dynamically
		self.button_background = pygame.image.load("UI/Button_Background.png").convert_alpha()
		self.button_background = pygame.transform.scale(self.button_background, new_bg_size)


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

		# Get the current window dimensions.
		current_width, current_height = window.get_size()

		self.singleplayer_button = helper_funcs.create_dynamic_button(
			window, 0.37, 0.23, 0.26, 0.10, 50, "Play Against an AI",
			constants.BLACK, constants.WHITE, constants.LIGHT_GREEN
		)
		
		self.local_multiplayer_button = helper_funcs.create_dynamic_button(
			window, 0.37, 0.38, 0.26, 0.10, 50, "Play by Yourself",
			constants.BLACK, constants.WHITE, constants.LIGHT_GREEN
		)

		self.multiplayer_button = helper_funcs.create_dynamic_button(
			window, 0.37, 0.53, 0.26, 0.10, 50, "Play Against a Friend",
			constants.BLACK, constants.WHITE, constants.LIGHT_GREEN
		)

		self.exit_button = helper_funcs.create_dynamic_button(
			window, 0.37, 0.68, 0.26, 0.10, 50, "Close The Application",
			constants.BLACK, constants.WHITE, constants.LIGHT_GREEN
		)
		
		self.load_board_boarder(window)
		self.load_board(window)
		
		base_bg_size = constants.resolutions["1920x1080"]["background_elements"]["main_menu"]["menu_background_size"]
		# Calculate the new size using your dynamic scaling helper functions.
		new_bg_size = (
        	helper_funcs.dynamic_scale_x(base_bg_size[0], current_width),
        	helper_funcs.dynamic_scale_y(base_bg_size[1], current_height)
    	)
		self.button_background = pygame.image.load("UI/Button_Background_Poly.png").convert_alpha()
		self.button_background = pygame.transform.scale(self.button_background, new_bg_size)

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

	def update_layout(self, window):
		helper_funcs.update_button_layout(self.singleplayer_button, window, 0.37, 0.23, 0.26, 0.10, 50)
		helper_funcs.update_button_layout(self.local_multiplayer_button, window, 0.37, 0.38, 0.26, 0.10, 50)
		helper_funcs.update_button_layout(self.multiplayer_button, window, 0.37, 0.53, 0.26, 0.10, 50)
		helper_funcs.update_button_layout(self.exit_button, window, 0.37, 0.68, 0.26, 0.10, 50)


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
#  - inits board
class PreGameSettings(State):
	def __init__(self, window):
		super().__init__() # inherit the parent initializer
		self.next_state = None
		self.font = pygame.font.SysFont("Arial",size=35)
		# player and opponent will be created here to be inherited

		# host retains last settings, guest is opposite
		if self.host.color == "Cho":
			self.guest.color = "Han"
		else:
			self.guest.color = "Cho"

		self.load_button_background(window)
		self.load_board_boarder(window)
		self.load_board(window)
		self.__load_player_color_menu(window)
		self.__load_piece_convention_menu(window)
		self.__load_play_button(window)
		self.__load_player_piece_preview(window)

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

		elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
			self.next_state = "Main Menu"

	def handle_host_swap(self):
		if self.host_swap_right_horse_button.is_clicked():
			helper_funcs.swap_pieces(self.host, self.host.pieces[6], self.host.pieces[4])

		elif self.host_swap_left_horse_button.is_clicked():
			helper_funcs.swap_pieces(self.host, self.host.pieces[5], self.host.pieces[3])
		
		elif self.host_confirm_swap_button.is_clicked():
			self.opening_turn = False
			if self.guest.color == "Cho":
				helper_funcs.choose_ai_lineup(self.guest)
				self.host.is_turn = False
				self.guest.is_turn = True

			else:
				self.host.is_turn = True
				self.guest.is_turn = False

	def render(self, window):
		self.render_board(window)
		self.__render_player_color_menu(window)
		self.__render_piece_convention_menu(window)
		self.__render_player_piece_preview(window)
		self.__render_play_button(window)
	
	# LOADING AND RENDERING FUNCTIONS
	def __load_player_color_menu(self, window):
		current_width, current_height = window.get_size()
		
		# play as cho/han button background
		# Retrieve base size from the "1920x1080" configuration
		base_bg_size = constants.resolutions["1920x1080"]["background_elements"]["local_MP"]["button_background"]["play_as"]["size"]
		new_bg_size = (helper_funcs.dynamic_scale_x(base_bg_size[0], current_width), helper_funcs.dynamic_scale_y(base_bg_size[1], current_height))
		self.play_as_background = pygame.transform.scale(self.button_background, new_bg_size)

		# cho button
		cho_config = constants.resolutions["1920x1080"]["buttons"]["local_MP"]["cho_button"]
		self.cho_side_button = helper_funcs.create_button_from_config(window, cho_config)
		
		# han button
		han_config = constants.resolutions["1920x1080"]["buttons"]["local_MP"]["han_button"]
		self.han_side_button = helper_funcs.create_button_from_config(window, han_config)

	def __load_piece_convention_menu(self, window):
	    # Scale and set the piece convention background image dynamically.
	    # Retrieve the base size from the "1920x1080" configuration.
		base_bg_size = constants.resolutions["1920x1080"]["background_elements"]["local_MP"]["button_background"]["piece_convention"]["size"] 
		current_width, current_height = window.get_size()
		new_bg_size = (helper_funcs.dynamic_scale_x(base_bg_size[0], current_width),
	                   helper_funcs.dynamic_scale_y(base_bg_size[1], current_height))
		self.piece_convention_background = pygame.transform.scale(self.button_background, new_bg_size)
	
	    # Create the standard piece convention button dynamically.
		std_config = constants.resolutions["1920x1080"]["buttons"]["local_MP"]["standard_piece_convention_button"]
		self.standard_piece_convention_button = helper_funcs.create_button_from_config(window, std_config)
	
	    # Create the international piece convention button dynamically.
		intl_config = constants.resolutions["1920x1080"]["buttons"]["local_MP"]["internat_piece_convention_button"]
		self.internat_piece_convention_button = helper_funcs.create_button_from_config(window, intl_config)
	
	def __load_play_button(self, window):
	    # Scale and set the play button background image dynamically.
		base_bg_size = constants.resolutions["1920x1080"]["background_elements"]["local_MP"]["button_background"]["play"]["size"]
		current_width, current_height = window.get_size()
		new_bg_size = (helper_funcs.dynamic_scale_x(base_bg_size[0], current_width),
	                   helper_funcs.dynamic_scale_y(base_bg_size[1], current_height))
	    # Load and scale the background image.
		self.play_button_background = pygame.image.load("UI/Button_Background_Poly.png").convert_alpha()
		self.play_button_background = pygame.transform.scale(self.play_button_background, new_bg_size)
	
	    # Create the play button dynamically.
		play_config = constants.resolutions["1920x1080"]["buttons"]["local_MP"]["play_button"]
		self.play_button = helper_funcs.create_button_from_config(window, play_config)	


	def __load_player_piece_preview(self, window):
		# Get current window dimensions and define base resolution.
		current_width, current_height = window.get_size()
		base_width = 1920
		base_height = 1080
		
		# --- Player piece display background ---
		base_size = constants.resolutions["1920x1080"]["background_elements"]["local_MP"]["button_background"]["player_piece_display"]["size"]
		new_size = (
			helper_funcs.dynamic_scale_x(base_size[0], current_width, base_width),
			helper_funcs.dynamic_scale_y(base_size[1], current_height, base_height)
			)
		self.player_piece_display_background = pygame.image.load("UI/Button_Background.png").convert_alpha()
		self.player_piece_display_background = pygame.transform.rotate(self.player_piece_display_background, 90)
		self.player_piece_display_background = pygame.transform.scale(self.player_piece_display_background, new_size)
		
		# --- Player header background ---
		base_header_size = constants.resolutions["1920x1080"]["background_elements"]["local_MP"]["button_background"]["player_piece_display"]["player_header"]["size"]
		new_header_size = (
			helper_funcs.dynamic_scale_x(base_header_size[0], current_width, base_width),
			helper_funcs.dynamic_scale_y(base_header_size[1], current_height, base_height) 
			)
		self.player_header_background = pygame.image.load("UI/Button_Background.png").convert_alpha()
		self.player_header_background = pygame.transform.scale(self.player_header_background, new_header_size)
		
		# --- Opponent piece display background ---
		base_opponent_size = constants.resolutions["1920x1080"]["background_elements"]["local_MP"]["button_background"]["opponent_piece_display"]["size"]
		new_opponent_size = (
			helper_funcs.dynamic_scale_x(base_opponent_size[0], current_width, base_width),
			helper_funcs.dynamic_scale_y(base_opponent_size[1], current_height, base_height)
			)
		self.opponent_piece_display_background = pygame.image.load("UI/Button_Background.png").convert_alpha()
		self.opponent_piece_display_background = pygame.transform.rotate(self.opponent_piece_display_background, 270)
		self.opponent_piece_display_background = pygame.transform.scale(self.opponent_piece_display_background, new_opponent_size)


	def __render_player_color_menu(self, window):
    	# Get current window dimensions.
		current_width, current_height = window.get_size()
		
		# --- Scale and blit the background ---
		base_bg_loc = constants.resolutions["1920x1080"]["background_elements"]["local_MP"]["button_background"]["play_as"]["location"]
		scaled_bg_loc = (helper_funcs.dynamic_scale_x(base_bg_loc[0], current_width),
                     helper_funcs.dynamic_scale_y(base_bg_loc[1], current_height))
		window.blit(self.play_as_background, scaled_bg_loc)

    	# --- Draw the text for the "play as" area ---
		base_text = constants.resolutions["1920x1080"]["background_elements"]["local_MP"]["button_background"]["play_as"]["text"]["string"]
		base_text_loc = constants.resolutions["1920x1080"]["background_elements"]["local_MP"]["button_background"]["play_as"]["text"]["location"]
		scaled_text_loc = (helper_funcs.dynamic_scale_x(base_text_loc[0], current_width),
                       helper_funcs.dynamic_scale_y(base_text_loc[1], current_height))
		base_font_size = constants.resolutions["1920x1080"]["background_elements"]["local_MP"]["button_background"]["play_as"]["text"]["font_size"]
		scaled_font_size = int(base_font_size * (current_width / 1920))
		self.draw_text(window, base_text, scaled_text_loc[0], scaled_text_loc[1], scaled_font_size)
	
		# Draw the buttons
		self.cho_side_button.draw_button(window)
		self.han_side_button.draw_button(window)
	
	def __render_piece_convention_menu(self, window):
		# Get current window dimensions.
		current_width, current_height = window.get_size()
		
		# --- Scale and blit the piece convention background
		base_bg_loc = constants.resolutions["1920x1080"]["background_elements"]["local_MP"]["button_background"]["piece_convention"]["location"]
		scaled_bg_loc = (helper_funcs.dynamic_scale_x(base_bg_loc[0], current_width),
	                     helper_funcs.dynamic_scale_y(base_bg_loc[1], current_height))
		window.blit(self.piece_convention_background, scaled_bg_loc)

	    # --- Draw the text for the piece convention area ---
		base_text = constants.resolutions["1920x1080"]["background_elements"]["local_MP"]["button_background"]["piece_convention"]["text"]["string"]
		base_text_loc = constants.resolutions["1920x1080"]["background_elements"]["local_MP"]["button_background"]["piece_convention"]["text"]["location"]
		scaled_text_loc = (helper_funcs.dynamic_scale_x(base_text_loc[0], current_width),
	                       helper_funcs.dynamic_scale_y(base_text_loc[1], current_height))
		base_font_size = constants.resolutions["1920x1080"]["background_elements"]["local_MP"]["button_background"]["piece_convention"]["text"]["font_size"]
		scaled_font_size = int(base_font_size * (current_width / 1920))
		self.draw_text(window, base_text, scaled_text_loc[0], scaled_text_loc[1], scaled_font_size)

	    # Draw the convention buttons
		self.standard_piece_convention_button.draw_button(window)
		self.internat_piece_convention_button.draw_button(window)


	def __render_play_button(self, window):
    	# Get current window dimensions.
		current_width, current_height = window.get_size()
		
		# Retrieve the base background location from the "1920x1080" configuration.
		base_bg_loc = constants.resolutions["1920x1080"]["background_elements"]["local_MP"]["button_background"]["play"]["location"]
		scaled_bg_loc = (
			helper_funcs.dynamic_scale_x(base_bg_loc[0], current_width),
			helper_funcs.dynamic_scale_y(base_bg_loc[1], current_height)
			)
		# Blit the play button background at the dynamically scaled location.
		window.blit(self.play_button_background, scaled_bg_loc)
		
		# Draw the play button itself (its own internal dimensions should have been updated elsewhere).
		self.play_button.draw_button(window)


	def __render_player_piece_preview(self, window):
		# Get current window dimensions.
		current_width, current_height = window.get_size()
    
    	# --- Render the player header background ---
		base_header_loc = constants.resolutions["1920x1080"]["background_elements"]["single_player"]["button_background"]["player_piece_display"]["player_header"]["location"]
		scaled_header_loc = (
			helper_funcs.dynamic_scale_x(base_header_loc[0], current_width),
			helper_funcs.dynamic_scale_y(base_header_loc[1], current_height)
    	)
		window.blit(self.player_header_background, scaled_header_loc)
    
    	# --- Render the player header text ---
		base_text = constants.resolutions["1920x1080"]["background_elements"]["single_player"]["button_background"]["player_piece_display"]["text"]["string"]
		base_text_loc = constants.resolutions["1920x1080"]["background_elements"]["single_player"]["button_background"]["player_piece_display"]["text"]["location"]
		base_font_size = constants.resolutions["1920x1080"]["background_elements"]["single_player"]["button_background"]["player_piece_display"]["text"]["font_size"]
		scaled_text_loc = (
        	helper_funcs.dynamic_scale_x(base_text_loc[0], current_width),
        	helper_funcs.dynamic_scale_y(base_text_loc[1], current_height)
    	)
		scaled_font_size = int(base_font_size * (current_width / 1920))
		self.draw_text(window, base_text, scaled_text_loc[0], scaled_text_loc[1], scaled_font_size)
		
		# --- Render the player piece display background ---
		base_player_disp_loc = constants.resolutions["1920x1080"]["background_elements"]["single_player"]["button_background"]["player_piece_display"]["location"]
		scaled_player_disp_loc = (
        	helper_funcs.dynamic_scale_x(base_player_disp_loc[0], current_width),
        	helper_funcs.dynamic_scale_y(base_player_disp_loc[1], current_height)
    	)
		window.blit(self.player_piece_display_background, scaled_player_disp_loc)
    
    	# --- Render the opponent piece display background ---
		base_opponent_disp_loc = constants.resolutions["1920x1080"]["background_elements"]["single_player"]["button_background"]["opponent_piece_display"]["location"]
		scaled_opponent_disp_loc = (
        	helper_funcs.dynamic_scale_x(base_opponent_disp_loc[0], current_width),
        	helper_funcs.dynamic_scale_y(base_opponent_disp_loc[1], current_height)
    	)
		window.blit(self.opponent_piece_display_background, scaled_opponent_disp_loc)
		
		# --- Render the pieces ---
		render_funcs.PreGame_render_piece_display(window, self.host, self.guest)

	
	def load_host_side_swap_menu(self, window):
		# Get current window dimensions.
		current_width, current_height = window.get_size()
		
		# --- Host-side swap left-horse button ---
		left_horse_config = constants.resolutions["1920x1080"]["buttons"]["local_MP"]["host_swap_left_horse_button"]
		self.host_swap_left_horse_button = helper_funcs.create_button_from_config(window, left_horse_config)
		
		# --- Host-side swap right-horse button ---
		right_horse_config = constants.resolutions["1920x1080"]["buttons"]["local_MP"]["host_swap_right_horse_button"]
		self.host_swap_right_horse_button = helper_funcs.create_button_from_config(window, right_horse_config)

	    # --- Host-side swap left-horse background ---
		base_left_bg_size = constants.resolutions["1920x1080"]["background_elements"]["local_MP"]["button_background"]["host_swap_left_horse"]["size"]
		new_left_bg_size = (
	        helper_funcs.dynamic_scale_x(base_left_bg_size[0], current_width),
	        helper_funcs.dynamic_scale_y(base_left_bg_size[1], current_height)
	    )
	    
		# IMPORTANT: Also scale the background's location.
		base_left_bg_loc = constants.resolutions["1920x1080"]["background_elements"]["local_MP"]["button_background"]["host_swap_left_horse"]["location"]
		new_left_bg_loc = (
	        helper_funcs.dynamic_scale_x(base_left_bg_loc[0], current_width),
	        helper_funcs.dynamic_scale_y(base_left_bg_loc[1], current_height)
	    )
		self.host_swap_left_horse_background = pygame.image.load("UI/Button_Background.png").convert_alpha()
		self.host_swap_left_horse_background = pygame.transform.rotate(self.host_swap_left_horse_background, 180)
		self.host_swap_left_horse_background = pygame.transform.scale(self.host_swap_left_horse_background, new_left_bg_size)
	
	    # Store the new location so your render function can use it.
		self.host_swap_left_horse_background_pos = new_left_bg_loc

	    # --- Host-side swap right-horse background ---
		base_right_bg_size = constants.resolutions["1920x1080"]["background_elements"]["local_MP"]["button_background"]["host_swap_right_horse"]["size"]
		new_right_bg_size = (
	        helper_funcs.dynamic_scale_x(base_right_bg_size[0], current_width),
	        helper_funcs.dynamic_scale_y(base_right_bg_size[1], current_height)
	    )
		base_right_bg_loc = constants.resolutions["1920x1080"]["background_elements"]["local_MP"]["button_background"]["host_swap_right_horse"]["location"]
		new_right_bg_loc = (
	        helper_funcs.dynamic_scale_x(base_right_bg_loc[0], current_width),
	        helper_funcs.dynamic_scale_y(base_right_bg_loc[1], current_height)
	    )
		self.host_swap_right_horse_background = pygame.image.load("UI/Button_Background.png").convert_alpha()
		self.host_swap_right_horse_background = pygame.transform.rotate(self.host_swap_right_horse_background, 180)
		self.host_swap_right_horse_background = pygame.transform.scale(self.host_swap_right_horse_background, new_right_bg_size)
		self.host_swap_right_horse_background_pos = new_right_bg_loc

	    # --- Host-side confirm swap button ---
		confirm_config = constants.resolutions["1920x1080"]["buttons"]["local_MP"]["host_confirm_swap_button"]
		self.host_confirm_swap_button = helper_funcs.create_button_from_config(window, confirm_config)

	    # --- Host-side confirm swap button background ---
		base_confirm_bg_size = constants.resolutions["1920x1080"]["background_elements"]["local_MP"]["button_background"]["host_confirm_swap"]["size"]
		new_confirm_bg_size = (
	        helper_funcs.dynamic_scale_x(base_confirm_bg_size[0], current_width),
	        helper_funcs.dynamic_scale_y(base_confirm_bg_size[1], current_height)
	    )
		base_confirm_bg_loc = constants.resolutions["1920x1080"]["background_elements"]["local_MP"]["button_background"]["host_confirm_swap"]["location"]
		new_confirm_bg_loc = (
	        helper_funcs.dynamic_scale_x(base_confirm_bg_loc[0], current_width),
	        helper_funcs.dynamic_scale_y(base_confirm_bg_loc[1], current_height)
	    )
		self.host_confirm_swap_button_background = pygame.image.load("UI/Button_Background_Poly.png").convert_alpha()
		self.host_confirm_swap_button_background = pygame.transform.scale(self.host_confirm_swap_button_background, new_confirm_bg_size)
		self.host_confirm_swap_button_background_pos = new_confirm_bg_loc


	def load_guest_side_swap_menu(self, window):
		# Get current window dimensions
		current_width, current_height = window.get_size()
		
		# --- Guest-side swap left-horse button ---
		guest_left_config = constants.resolutions["1920x1080"]["buttons"]["local_MP"]["guest_swap_left_horse_button"]
		self.guest_swap_left_horse_button = helper_funcs.create_button_from_config(window, guest_left_config)
		
		# --- Guest-side swap right-horse button ---
		guest_right_config = constants.resolutions["1920x1080"]["buttons"]["local_MP"]["guest_swap_right_horse_button"]
		self.guest_swap_right_horse_button = helper_funcs.create_button_from_config(window, guest_right_config)
		
		# --- Guest-side swap left-horse background ---
		base_left_bg_size = constants.resolutions["1920x1080"]["background_elements"]["local_MP"]["button_background"]["guest_swap_left_horse"]["size"]
		new_left_bg_size = (
    	    helper_funcs.dynamic_scale_x(base_left_bg_size[0], current_width),
    	    helper_funcs.dynamic_scale_y(base_left_bg_size[1], current_height)
    	)
		base_left_bg_loc = constants.resolutions["1920x1080"]["background_elements"]["local_MP"]["button_background"]["guest_swap_left_horse"]["location"]
		new_left_bg_loc = (
    	    helper_funcs.dynamic_scale_x(base_left_bg_loc[0], current_width),
    	    helper_funcs.dynamic_scale_y(base_left_bg_loc[1], current_height)
    	)
		self.guest_swap_left_horse_background = pygame.image.load("UI/Button_Background.png").convert_alpha()
		self.guest_swap_left_horse_background = pygame.transform.scale(self.guest_swap_left_horse_background, new_left_bg_size)
		self.guest_swap_left_horse_background_pos = new_left_bg_loc
		
		# --- Guest-side swap right-horse background --- 
		base_right_bg_size = constants.resolutions["1920x1080"]["background_elements"]["local_MP"]["button_background"]["guest_swap_right_horse"]["size"]
		new_right_bg_size = (
    	    helper_funcs.dynamic_scale_x(base_right_bg_size[0], current_width),
    	    helper_funcs.dynamic_scale_y(base_right_bg_size[1], current_height)
    	)
		base_right_bg_loc = constants.resolutions["1920x1080"]["background_elements"]["local_MP"]["button_background"]["guest_swap_right_horse"]["location"]
		new_right_bg_loc = (
    	    helper_funcs.dynamic_scale_x(base_right_bg_loc[0], current_width),
    	    helper_funcs.dynamic_scale_y(base_right_bg_loc[1], current_height)
    	)
		self.guest_swap_right_horse_background = pygame.image.load("UI/Button_Background.png").convert_alpha()
		self.guest_swap_right_horse_background = pygame.transform.scale(self.guest_swap_right_horse_background, new_right_bg_size)
		self.guest_swap_right_horse_background_pos = new_right_bg_loc
		
		# --- Guest-side confirm swap button ---
		guest_confirm_config = constants.resolutions["1920x1080"]["buttons"]["local_MP"]["guest_confirm_swap_button"]
		self.guest_confirm_swap_button = helper_funcs.create_button_from_config(window, guest_confirm_config)
		
		# --- Guest-side confirm swap button background ---
		base_confirm_bg_size = constants.resolutions["1920x1080"]["background_elements"]["local_MP"]["button_background"]["guest_confirm_swap"]["size"]
		new_confirm_bg_size = (
    	    helper_funcs.dynamic_scale_x(base_confirm_bg_size[0], current_width),
    	    helper_funcs.dynamic_scale_y(base_confirm_bg_size[1], current_height)
    	)
		base_confirm_bg_loc = constants.resolutions["1920x1080"]["background_elements"]["local_MP"]["button_background"]["guest_confirm_swap"]["location"]
		new_confirm_bg_loc = (
    	    helper_funcs.dynamic_scale_x(base_confirm_bg_loc[0], current_width),
    	    helper_funcs.dynamic_scale_y(base_confirm_bg_loc[1], current_height)
    	)
		self.guest_confirm_swap_button_background = pygame.image.load("UI/Button_Background_Poly.png").convert_alpha()
		self.guest_confirm_swap_button_background = pygame.transform.scale(self.guest_confirm_swap_button_background, new_confirm_bg_size)
		self.guest_confirm_swap_button_background_pos = new_confirm_bg_loc

#--------------------------------------------------------------------------------
# THIS STATE WILL HANDLE SETTINGS FOR SETTING UP THE GAME AGAINST AN AI
#--------------------------------------------------------------------------------
class SinglePlayerPreGameSettings(PreGameSettings):

	# initialize the settings for the game
	# INPUT: No Input
	# OUTPUT: Settings menu is ready to be interacted with by player
	def __init__(self, window):
		print("calling ai init")
		self.ai_level = "Easy"
		self.host = player.Player(is_host=True, board_perspective="Bottom")
		self.guest = ai.OpponentAI(is_host=False, board_perspective="Top")
		super().__init__(window)
		self.load_ai_buttons()

	def handle_event(self, event):
		self.handle_left_cick(event)

		if self.play_button.is_clicked():
				helper_funcs.update_player_settings(self.host)
				self.next_state = "Single Player Game"

		# loop to set ai difficulty if altered
		for button in self.ai_level_buttons:
			if button.is_clicked():
				self.ai_level = button.text
				self.host.ai_level = button.text
				self.guest.ai_level = button.text
				
	def render(self, window):
		super().render(window)
		self.render_ai_buttons(window)

	def load_ai_buttons(self, window):
		self.ai_level_buttons = []
		
		# Easy button
		easy_config = constants.resolutions["1920x1080"]["buttons"]["single_player"]["easy_ai_button"]
		self.easy_ai_button = helper_funcs.create_button_from_config(window, easy_config)
		self.ai_level_buttons.append(self.easy_ai_button)
		
		# Medium button
		medium_config = constants.resolutions["1920x1080"]["buttons"]["single_player"]["medium_ai_button"]
		self.medium_ai_button = helper_funcs.create_button_from_config(window, medium_config)
		self.ai_level_buttons.append(self.medium_ai_button)
		
		# Hard button
		hard_config = constants.resolutions["1920x1080"]["buttons"]["single_player"]["hard_ai_button"]
		self.hard_ai_button = helper_funcs.create_button_from_config(window, hard_config)
		self.ai_level_buttons.append(self.hard_ai_button)

	def render_ai_buttons(self, window):
		current_width, current_height = window.get_size()
		
		# --- Render AI Level Background ---
		# Retrieve and scale the background location.
		base_bg_loc = constants.resolutions["1920x1080"]["background_elements"]["single_player"]["button_background"]["ai_level"]["location"]
		scaled_bg_loc = (helper_funcs.dynamic_scale_x(base_bg_loc[0], current_width),
                         helper_funcs.dynamic_scale_y(base_bg_loc[1], current_height))
		
		# Here, we assume that self.ai_level_background has been loaded beforehand.
		# # If you are using self.piece_convention_background as the background, then:
		window.blit(self.piece_convention_background, scaled_bg_loc)
		
		# --- Draw AI Level Description Text ---
		base_text = constants.resolutions["1920x1080"]["background_elements"]["single_player"]["button_background"]["ai_level"]["text"]["string"]
		base_text_loc = constants.resolutions["1920x1080"]["background_elements"]["single_player"]["button_background"]["ai_level"]["text"]["location"]
		scaled_text_loc = (helper_funcs.dynamic_scale_x(base_text_loc[0], current_width),
                           helper_funcs.dynamic_scale_y(base_text_loc[1], current_height))
		base_font_size = constants.resolutions["1920x1080"]["background_elements"]["single_player"]["button_background"]["ai_level"]["text"]["font_size"]
		scaled_font_size = int(base_font_size * (current_width / 1920))
		self.draw_text(window, base_text, scaled_text_loc[0], scaled_text_loc[1], scaled_font_size)
		
		# --- Draw the Chosen AI Level (e.g., from self.host.ai_level) ---
		chosen_text = self.host.ai_level  # assuming this holds the current AI difficulty as a string
		base_chosen_loc = constants.resolutions["1920x1080"]["background_elements"]["single_player"]["button_background"]["ai_level"]["text"]["chosen_diff_location"]
		scaled_chosen_loc = (helper_funcs.dynamic_scale_x(base_chosen_loc[0], current_width),
                             helper_funcs.dynamic_scale_y(base_chosen_loc[1], current_height))
		# Reuse scaled_font_size for the chosen text, or scale differently if needed.
		self.draw_text(window, chosen_text, scaled_chosen_loc[0], scaled_chosen_loc[1], scaled_font_size)
		
		# --- Render Each AI Level Button ---
		for btn in self.ai_level_buttons:
			btn.draw_button(window)

#--------------------------------------------------------------------------------
# Inherited State for single player gaming against an ai
#--------------------------------------------------------------------------------
class SinglePlayerGame(SinglePlayerPreGameSettings):
	
	# initialize the gamestate
	# INPUT: No Input
	# OUTPUT: Gamestate is initialized and ready for playing

	def __init__(self, window):
		super().__init__(window)

		self.load_host_side_swap_menu()
		
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
					self.handle_host_swap()

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
		

	# Handle any rendering that needs to be done
	# INPUT: pygame surface object (window to display to)
	# OUTPUT: All game attributes/actions are rendered
	def render(self, window):
		# display board to window
		self.render_board(window)

		# DISPLAY THE OPTION TO SWAP HORSES AT THE START OF THE GAME
		if self.opening_turn:
			window.blit(self.host_swap_left_horse_background, self.host_swap_left_horse_background_pos)
			self.host_swap_left_horse_button.draw_button(window)

			window.blit(self.host_swap_right_horse_background, self.host_swap_right_horse_background_pos)
			self.host_swap_right_horse_button.draw_button(window)

		# if player has a piece currently clicked, render where it can go
		if self.host is not None and self.host.is_clicked:
			render_funcs.render_possible_spots(self.host, self.guest, self.board, window, self.condition)

		# display confirm button for swapping pieces
		if self.opening_turn:
			# confirm swap button
			window.blit(self.host_confirm_swap_button_background, self.host_confirm_swap_button_background_pos)
			self.host_confirm_swap_button.draw_button(window)

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

	def handle_ai_move(self):
		if self.is_game_over():
				self.game_over = True
				self.winner = self.host

		# ai move logic
		elif not self.immediate_render and self.guest.is_turn and not self.opening_turn and not self.game_over:
			new_board = self.guest.convert_board(self.board, self.host)
			fen = self.guest.generate_fen(new_board)
				
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

#--------------------------------------------------------------------------------
class LocalSinglePlayerPreGameSettings(PreGameSettings):


	# initialize the settings for the game
	# INPUT: No Input
	# OUTPUT: Settings menu is ready to be interacted with by player
	def __init__(self, window):
		self.guest = player.Player(is_host=False, board_perspective="Top")
		self.host = player.Player(is_host=True, board_perspective="Bottom")
		super().__init__(window)

	# Listen for and handle any event ticks (clicks/buttons)
	# INPUT: pygame event object
	# OUTPUT: settings are set accordingly
	def handle_event(self, event):
		self.handle_left_cick(event)
		if (self.play_button.is_clicked() 
			and self.host is not None):
				helper_funcs.update_player_settings(self.host)
				self.next_state = "Local Single Player Game"
				
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
		print("local single player game called")
		# load then display board image
		self.load_board_boarder(window)
		self.load_board(window)
		self.load_host_side_swap_menu(window)
		self.load_guest_side_swap_menu(window)
		
		# condition warning/turn tab
		base_game_state_size = constants.resolutions["1920x1080"]["background_elements"]["single_player"]["button_background"]["game_state"]["size"]
		self.game_state_background = helper_funcs.load_scaled_image(window, "UI/Button_Background.png", base_game_state_size)
		
		# game over pop-up display
		base_game_over_size = constants.resolutions["1920x1080"]["background_elements"]["single_player"]["button_background"]["game_over"]["size"]
		self.game_over_background = helper_funcs.load_scaled_image(window, "UI/Button_Background.png", base_game_over_size)

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
					# self.handle_host_swap()
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
					self.handle_host_swap()
				
				# CHO IS GUEST
				else:
					if self.guest_swap_right_horse_button.is_clicked():
						helper_funcs.swap_pieces(self.cho_player, self.cho_player.pieces[6], self.cho_player.pieces[4])

					elif self.guest_swap_left_horse_button.is_clicked():
						helper_funcs.swap_pieces(self.cho_player, self.cho_player.pieces[5], self.cho_player.pieces[3])

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
		self.render_board(window)

		# DISPLAY THE OPTION TO SWAP HORSES AT THE START OF THE GAME
		# HAN
		if self.opening_turn and not self.han_player.is_ready:
			# HOST (BOTTOM-VIEW)
			if self.han_player.is_host:
				button_key = "host"
				window.blit(self.host_swap_left_horse_background, self.host_swap_left_horse_background_pos)
				self.host_swap_left_horse_button.draw_button(window)

				window.blit(self.host_swap_right_horse_background, self.host_swap_right_horse_background_pos)
				self.host_swap_right_horse_button.draw_button(window)
			# GUEST (TOP-VIEW)
			else:
				button_key = "guest"
				window.blit(self.guest_swap_left_horse_background, self.guest_swap_left_horse_background_pos)
				self.guest_swap_left_horse_button.draw_button(window)

				window.blit(self.guest_swap_right_horse_background, self.guest_swap_right_horse_background_pos)
				self.guest_swap_right_horse_button.draw_button(window)
		# CHO
		elif self.opening_turn and not self.cho_player.is_ready:
			# HOST (BOTTOM-VIEW)
			if self.cho_player.is_host:
				button_key = "host"
				window.blit(self.host_swap_left_horse_background, self.host_swap_left_horse_background_pos)
				self.host_swap_left_horse_button.draw_button(window)

				window.blit(self.host_swap_right_horse_background, self.host_swap_right_horse_background_pos)
				self.host_swap_right_horse_button.draw_button(window)
			# GUEST (TOP-VIEW)
			else:
				button_key = "guest"
				window.blit(self.guest_swap_left_horse_background, self.guest_swap_left_horse_background_pos)
				self.guest_swap_left_horse_button.draw_button(window)

				window.blit(self.guest_swap_right_horse_background, self.guest_swap_right_horse_background_pos)
				self.guest_swap_right_horse_button.draw_button(window)

		# DISPLAY CONFIRM FOR PIECE SWAP
		# Han
		if self.opening_turn and not self.han_player.is_ready:
			if self.han_player.is_host:
				button_key = "host"
				window.blit(self.host_confirm_swap_button_background, self.host_confirm_swap_button_background_pos)
				self.host_confirm_swap_button.draw_button(window)	
			else:
				button_key = "guest"
				window.blit(self.guest_confirm_swap_button_background, self.guest_confirm_swap_button_background_pos)
				self.guest_confirm_swap_button.draw_button(window)
		# Cho
		elif self.opening_turn and not self.cho_player.is_ready:
			if self.cho_player.is_host:
				button_key = "host"
				window.blit(self.host_confirm_swap_button_background, self.host_confirm_swap_button_background_pos)
				self.host_confirm_swap_button.draw_button(window)
			else:
				button_key = "guest"
				window.blit(self.guest_confirm_swap_button_background, self.guest_confirm_swap_button_background_pos)
				self.guest_confirm_swap_button.draw_button(window)

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



	    
		# RENDER WHERE CLICKED PIECE MAY GO
		if self.active_player is not None and self.active_player.is_clicked:
			render_funcs.render_possible_spots(self.active_player, self.waiting_player, self.board, window, self.condition)


		# DISPLAY END GAME CONDITIONS/GAME_STATES
		if self.game_over and self.bikjang:
			self.render_bikjang_ending(window)

		if self.game_over and self.check:
			self.render_check_ending(window)

	def swap_turn(self):
		self.active_player, self. waiting_player = self.waiting_player, self.active_player


class MultiplayerPreGameSettings(PreGameSettings):
	def __init__(self, window):
		self.host = player.Player(is_host=True, board_perspective="Bottom")
		self.guest = player.Player(is_host=False, board_perspective="Top")
		super().__init__(window)
		
	# Listen for and handle any event ticks (clicks/buttons)
	# INPUT: pygame event object
	# OUTPUT: settings are set accordingly
	def handle_event(self, event):
		self.handle_left_cick(event)
		if (self.play_button.is_clicked() 
			and self.host is not None):
				helper_funcs.update_player_settings(self.host)
				self.next_state = "Multi Player Game"
				
	# Handle any rendering that needs to be done
	# INPUT: pygame surface object (window to display to)
	# OUTPUT: All pre-game settings attributes/actions are rendered
	def render(self, window):
		super().render(window)

class Multiplayer(MultiplayerPreGameSettings):

	def __init__(self, window):
		super().__init__(window)
		self.load_board_boarder(window)
		self.load_board(window)
		self.load_host_side_swap_menu(window)
		self.load_guest_side_swap_menu(window)
		self.board = board.Board()

		self.active_player = self.host
		self.waiting_player = self.guest


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
				self.handle_host_swap()

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

	def render_swap_menu(self, window):		
		# DISPLAY THE OPTION TO SWAP HORSES AT THE START OF THE GAME
		if self.opening_turn:
			window.blit(self.host_swap_left_horse_background, self.host_swap_left_horse_background_pos)
			self.host_swap_left_horse_button.draw_button(window)

			window.blit(self.host_swap_right_horse_background, self.host_swap_left_horse_background_pos)
			self.host_swap_right_horse_button.draw_button(window)

		# if player has a piece currently clicked, render where it can go
		if self.host is not None and self.host.is_clicked:
			render_funcs.render_possible_spots(self.host, self.guest, self.board, window, self.condition)

		# display confirm button for swapping pieces
		if self.opening_turn:
			# confirm swap button
			window.blit(self.host_confirm_swap_button_background, self.host_confirm_swap_button_background_pos)
			self.host_confirm_swap_button.draw_button(window)

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
