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

	# event handler
	def handle_event(self, event):
		pass

	# handle rendering
	def render(self, window):
		pass

	# no current use, needed only by state machine
	def update(self):
		pass

	# functions to handle input from player
	def is_left_click(event):
		if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
			return True
		return False
	
	def is_middle_click(event):
		if event.type == pygame.MOUSEBUTTONDOWN and event.button == 2:
			return True
		return False
	
	def is_right_click(event):
		if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
			return True
		return False

	def load_board(self, window):
		self.menu_background = pygame.image.load("Board/Janggi_Board_Border.png").convert_alpha()
		self.menu_background = pygame.transform.scale(self.menu_background, constants.board_border_size)
		self.center = window.get_rect().center

	def render_board(self):
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

		# FUTURE TODO: ONLINE MULTIPLAYER
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

		self.menu_background = pygame.image.load("Board/Janggi_Board_Border.png").convert_alpha()
		self.menu_background = pygame.transform.scale(self.menu_background, constants.board_border_size)
		self.center = window.get_rect().center

		self.playboard = pygame.image.load("Board/Janggi_Board.png").convert_alpha()
		self.playboard = pygame.transform.scale(self.playboard, constants.board_size)

		self.button_background = pygame.image.load("UI/Button_Background_Poly.png").convert_alpha()
		self.button_background = pygame.transform.scale(self.button_background,
									constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["main_menu"]["menu_background_size"])

	# Listen for and handle any event ticks (clicks/buttons)
	# INPUT: pygame event object
	# OUTPUT: Menu transitions are set accordingly
	def handle_event(self, event):
		if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
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
		# FUTURE TODO: ONLINE MULTIPLAYER
		self.multiplayer_button.draw_button(window)
		self.exit_button.draw_button(window)

#--------------------------------------------------------------------------------
# THIS STATE WILL HANDLE SETTINGS FOR SETTING UP THE GAME AGAINST AN AI
#--------------------------------------------------------------------------------
class SinglePlayerPreGameSettings(State):

	# initialize the settings for the game
	# INPUT: No Input
	# OUTPUT: Settings menu is ready to be interacted with by player
	def __init__(self, window):
		super().__init__() # inherit the parent initializer
		self.next_state = None
		self.font = pygame.font.SysFont("Arial",size=35)
		self.ai_level = "Easy"
		# player and opponent will be created here to be inherited
		self.player = player.Player(is_host=True, board_perspective="Bottom")
		# self.player_ai = player.Player(is_host=False, board_perspective="Top")
		self.opponent = ai.OpponentAI(is_host=False, board_perspective="Top")

		# host retains last settings, guest is opposite
		if self.player.color == "Cho":
			self.opponent.color = "Han"
		else:
			self.opponent.color = "Cho"

		# DECLARE BUTTONS FOR PRE-GAME SETTINGS
		# cho button
		x, y = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["single_player"]["cho_button"]["location"]
		width, height = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["single_player"]["cho_button"]["size"]
		font = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["single_player"]["cho_button"]["text"]["font"]
		text = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["single_player"]["cho_button"]["text"]["string"]
		foreground_color = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["single_player"]["cho_button"]["text"]["foreground_color"]
		background_color = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["single_player"]["cho_button"]["text"]["background_color"]
		hover_color = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["single_player"]["cho_button"]["text"]["hover_color"]
		self.cho_side_button = (button.Button(x, y, width, height, font, text, foreground_color, background_color, hover_color))
		
		# han button
		x, y = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["single_player"]["han_button"]["location"]
		width, height = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["single_player"]["han_button"]["size"]
		font = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["single_player"]["han_button"]["text"]["font"]
		text = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["single_player"]["han_button"]["text"]["string"]
		foreground_color = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["single_player"]["han_button"]["text"]["foreground_color"]
		background_color = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["single_player"]["han_button"]["text"]["background_color"]
		hover_color = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["single_player"]["han_button"]["text"]["hover_color"]
		self.han_side_button = (button.Button(x, y, width, height, font, text, foreground_color, background_color, hover_color))
		
		# standard piece convention button
		x, y = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["single_player"]["standard_piece_convention_button"]["location"]
		width, height = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["single_player"]["standard_piece_convention_button"]["size"]
		font = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["single_player"]["standard_piece_convention_button"]["text"]["font"]
		text = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["single_player"]["standard_piece_convention_button"]["text"]["string"]
		foreground_color = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["single_player"]["standard_piece_convention_button"]["text"]["foreground_color"]
		background_color = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["single_player"]["standard_piece_convention_button"]["text"]["background_color"]
		hover_color = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["single_player"]["standard_piece_convention_button"]["text"]["hover_color"]
		self.standard_piece_convention_button = (button.Button(x, y, width, height, font, text, foreground_color, background_color, hover_color))
		
		# international piece convention button
		x, y = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["single_player"]["internat_piece_convention_button"]["location"]
		width, height = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["single_player"]["internat_piece_convention_button"]["size"]
		font = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["single_player"]["internat_piece_convention_button"]["text"]["font"]
		text = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["single_player"]["internat_piece_convention_button"]["text"]["string"]
		foreground_color = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["single_player"]["internat_piece_convention_button"]["text"]["foreground_color"]
		background_color = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["single_player"]["internat_piece_convention_button"]["text"]["background_color"]
		hover_color = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["single_player"]["internat_piece_convention_button"]["text"]["hover_color"]
		self.internat_piece_convention_button = (button.Button(x, y, width, height, font, text, foreground_color, background_color, hover_color))
		
		# play button
		x, y = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["single_player"]["play_button"]["location"]
		width, height = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["single_player"]["play_button"]["size"]
		font = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["single_player"]["play_button"]["text"]["font"]
		text = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["single_player"]["play_button"]["text"]["string"]
		foreground_color = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["single_player"]["play_button"]["text"]["foreground_color"]
		background_color = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["single_player"]["play_button"]["text"]["background_color"]
		hover_color = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["single_player"]["play_button"]["text"]["hover_color"]
		self.play_button = (button.Button(x, y, width, height, font, text, foreground_color, background_color, hover_color))
		
		# boards
		self.menu_background = pygame.image.load("Board/Janggi_Board_Border.png").convert_alpha()
		self.menu_background = pygame.transform.scale(self.menu_background, constants.board_border_size)
		self.center = window.get_rect().center

		self.playboard = pygame.image.load("Board/Janggi_Board.png").convert_alpha()
		self.playboard = pygame.transform.scale(self.playboard, constants.board_size)
		self.playboard_center = self.menu_background.get_rect().center

		# load button backgrounds
		self.button_background = pygame.image.load("UI/Button_Background.png").convert_alpha()

		self.button_background = (
			pygame.transform.scale(self.button_background,
				constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["single_player"]["button_background"]["play_as"]["size"]))
		
		# play as cho/han button background
		self.play_as_background = (
			pygame.transform.scale(self.button_background,
				constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["single_player"]["button_background"]["play_as"]["size"]))
		
		# piece convention button background
		self.piece_convention_background = (
			pygame.transform.scale(self.button_background,
				constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["single_player"]["button_background"]["piece_convention"]["size"]))
		
		# play button background
		self.play_button_background = pygame.image.load("UI/Button_Background_Poly.png").convert_alpha()
		self.play_button_background = (pygame.transform.scale(self.play_button_background,
				constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["single_player"]["button_background"]["play"]["size"]))
		
		# player piece display background
		self.player_piece_display_background = pygame.image.load("UI/Button_Background.png").convert_alpha()
		self.player_piece_display_background = pygame.transform.rotate(self.player_piece_display_background, 90)
		self.player_piece_display_background = pygame.transform.scale(self.player_piece_display_background,
				constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["single_player"]["button_background"]["player_piece_display"]["size"])
		
		# player header background
		self.player_header_background = pygame.image.load("UI/Button_Background.png").convert_alpha()
		self.player_header_background = pygame.transform.scale(self.player_header_background,
				constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["single_player"]["button_background"]["player_piece_display"]["player_header"]["size"])
		
		# opponent piece display background
		self.opponent_piece_display_background = pygame.image.load("UI/Button_Background.png").convert_alpha()
		self.opponent_piece_display_background = pygame.transform.rotate(self.opponent_piece_display_background, 270)
		self.opponent_piece_display_background = pygame.transform.scale(self.opponent_piece_display_background,
				constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["single_player"]["button_background"]["opponent_piece_display"]["size"])
		
		# create a button for each ai level
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

		# board images	
		self.menu_background = pygame.image.load("Board/Janggi_Board_Border.png").convert_alpha()
		self.menu_background = pygame.transform.scale(self.menu_background, constants.board_border_size)
		self.center = window.get_rect().center

		self.playboard = pygame.image.load("Board/Janggi_Board.png").convert_alpha()
		self.playboard = pygame.transform.scale(self.playboard, constants.board_size)
		self.playboard_center = self.menu_background.get_rect().center

	# Listen for and handle any event ticks (clicks/buttons)
	# INPUT: pygame event object
	# OUTPUT: settings are set accordingly
	def handle_event(self, event):
		# on left mouse click, determine which button if any were clicked
		if self.is_left_click():
			# PLAY AS CHO
			if self.cho_side_button.is_clicked():
				self.player.color ="Cho"
				self.opponent.color = "Han"
			# PLAY AS HAN
			elif self.han_side_button.is_clicked():
				self.player.color = "Han"
				self.opponent.color = "Cho"
			# PLAY WITH STANDARD PIECE LOGOS
			elif self.standard_piece_convention_button.is_clicked():
				self.player.piece_convention = "Standard"
				self.opponent.piece_convention = "Standard"
			# PLAY WITH INTERNATIONAL PIECE LOGOS
			elif self.internat_piece_convention_button.is_clicked():
				self.player.piece_convention = "International"
				self.opponent.piece_convention = "International"
			# CLICK CONFIRM SETTINGS IF ALL ARE SET
			elif (self.play_button.is_clicked() 
		 		  and self.player is not None):
				helper_funcs.update_player_settings(self.player)
				self.next_state = "Single Player Game"
			# OTHERWISE FIND IF ANY OF THE AI LEVELS WERE SET
			else:
				for button in self.ai_level_buttons:
					if button.is_clicked():
						self.ai_level = button.text
						self.player.ai_level = button.text
						self.opponent.ai_level = button.text
						
	# escape to main menu
		elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
			self.next_state = "Main Menu"
				
	# Handle any rendering that needs to be done
	# INPUT: pygame surface object (window to display to)
	# OUTPUT: All pre-game settings attributes/actions are rendered
	def render(self, window):
		# USE BOARD AS BACKGROUND
		window.blit(self.menu_background, self.menu_background.get_rect(center = window.get_rect().center))
		window.blit(self.playboard, self.playboard.get_rect(center = window.get_rect().center))
		
		# SELECT PIECE SIDE TO PLAY AS (CHO/HAN)
		window.blit(self.play_as_background, 
			   constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["single_player"]["button_background"]["play_as"]["location"])
		text = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["single_player"]["button_background"]["play_as"]["text"]["string"]
		x, y = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["single_player"]["button_background"]["play_as"]["text"]["location"]
		font_size = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["single_player"]["button_background"]["play_as"]["text"]["font_size"]

		self.draw_text(window, text, x, y, font_size)
		self.cho_side_button.draw_button(window)
		self.han_side_button.draw_button(window)
		
		# SELECT PIECE TYPE CONVENTION TO PLAY WITH (STANDARD/INTERNATIONAL)
		window.blit(self.piece_convention_background, 
			   constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["single_player"]["button_background"]["piece_convention"]["location"])
		text = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["single_player"]["button_background"]["piece_convention"]["text"]["string"]
		x, y = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["single_player"]["button_background"]["piece_convention"]["text"]["location"]
		font_size = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["single_player"]["button_background"]["piece_convention"]["text"]["font_size"]

		self.draw_text(window, text, x, y, font_size)
		self.standard_piece_convention_button.draw_button(window)
		self.internat_piece_convention_button.draw_button(window)

		# SELECT AI LEVEL TO PLAY AGAINST (Easy/Medium/Hard)
		window.blit(self.piece_convention_background, 
			   constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["single_player"]["button_background"]["ai_level"]["location"])
		text = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["single_player"]["button_background"]["ai_level"]["text"]["string"]
		x, y = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["single_player"]["button_background"]["ai_level"]["text"]["location"]
		font_size = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["single_player"]["button_background"]["ai_level"]["text"]["font_size"]
		
		self.draw_text(window, text, x, y, font_size)
		text = self.player.ai_level
		x, y = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["single_player"]["button_background"]["ai_level"]["text"]["chosen_diff_location"]
		font_size = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["single_player"]["button_background"]["ai_level"]["text"]["font_size"]
		self.draw_text(window, text, x, y, font_size)

		for button in self.ai_level_buttons:
			button.draw_button(window)
				
		# DISPLAY PREVIEW OF THE PIECES ON HOW THEY WILL LOOK	
		if self.player is not None and self.opponent is not None:

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
			render_funcs.PreGame_render_piece_display(window, self.player, self.opponent)


		# PLAY BUTTON
		window.blit(self.play_button_background, 
			   constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["single_player"]["button_background"]["play"]["location"])
		self.play_button.draw_button(window)

#--------------------------------------------------------------------------------
# Inherited State for single player gaming against an ai
#--------------------------------------------------------------------------------
class SinglePlayerGame(SinglePlayerPreGameSettings):
	
	# initialize the gamestate
	# INPUT: No Input
	# OUTPUT: Gamestate is initialized and ready for playing
	# PROCESS:
	# 	1. loads board picture
	# 	2. loads horse-elephant swapping menus
	# 	3. Inits class variables
	# 	4. Inits board instance5

	def __init__(self, window):
		super().__init__(window)
		# load then display board image
		self.load_board(window)
		self.render_board()


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

		self.bikjang_initiater = None  # this is used in line 582 and 670, both times it is checked if it's set to None, but the value is never changed. So this is redundant?

		# create game objects
		self.board = board.Board()

		# pre-set ai if it goes first
		# Han player chooses first horse swaps
		if self.opponent.color == "Han":
			helper_funcs.choose_ai_lineup(self.opponent)
			self.active_player = self.player
			self.waiting_player = self.opponent
		else:
			self.active_player = self.opponent
			self.waiting_player = self.player

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
				self.winner = self.opponent

		# listen for an event trigger via click from right-mouse-button
		elif self.is_left_click(event) and not self.game_over:
				
				# OPENING TURN ONLY
				if self.opening_turn:
					# player may swap horses with elephants, confirm swap to end turn
					# Han player chooses first then Cho
					if self.swap_right_horse_button.is_clicked():
						helper_funcs.swap_pieces(self.player, self.player.pieces[6], self.player.pieces[4])

					elif self.swap_left_horse_button.is_clicked():
						helper_funcs.swap_pieces(self.player, self.player.pieces[5], self.player.pieces[3])
					
					elif self.confirm_swap_button.is_clicked():
						self.opening_turn = False
						if self.opponent.color == "Cho":
							helper_funcs.choose_ai_lineup(self.opponent)
							self.player.is_turn = False
							self.opponent.is_turn = True
						else:
							self.player.is_turn = True
							self.opponent.is_turn = False

				# GAMEPLAY TURN
				elif self.player.is_turn:
					self.print_fen("PLAYER:")
					# check if the player is currently attempting to move a piece
					if self.player.is_clicked:
						# unclick that piece if the move was successful/valid
						if helper_funcs.attempt_move(self.player, self.opponent, self.board, mouse_pos, self.condition):
							helper_funcs.player_piece_unclick(self.player)
							# end of turn update
							if helper_funcs.detect_bikjang(self.player, self.opponent):
								self.bikjang = True
								self.winner = self.player
								self.game_over = True
								self.condition = "Bikjang"

							elif helper_funcs.detect_check(self.opponent, self.player, self.board):
								self.check = True
								self.opponent.is_checked = True
								self.condition = "Check"
																
							self.swap_turn()
							self.immediate_render = True

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

		# if RMB clicked and ...
		elif (self.is_right_click() 
				and self.player.is_turn 
				and not self.bikjang 
				and not self.check
				and not self.game_over):

				if self.player is not None:
					helper_funcs.player_piece_unclick(self.player)
					# KING piece is always the first piece in the list
					if self.player.pieces[0].collision_rect.collidepoint(mouse_pos):
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
				self.winner = self.player

		# ai move logic
		elif not self.immediate_render and self.opponent.is_turn and not self.opening_turn and not self.game_over:
			new_board = self.opponent.convert_board(self.board, self.player)
			fen = self.opponent.generate_fen(new_board)
				
			self.print_fen("AI:")

			if self.ai_level == "Easy":
				depth = 1
			elif self.ai_level == "Medium":
				depth = 5
			elif self.ai_level == "Hard":
				depth = 10
			
			self.opponent.send_command(f"position fen {fen}")
			self.opponent.send_command(f"go depth {str(depth)}")
			best_move = self.opponent.get_engine_move()
			
			if helper_funcs.ai_move(self.player, self.opponent, self.board, best_move, new_board, fen):
				if helper_funcs.detect_bikjang(self.opponent, self.player):
					self.bikjang = True
					self.winner = self.opponent
					self.condition = "Bikjang"
					self.game_over = True

				elif helper_funcs.detect_check(self.player, self.opponent, self.board):
					self.check = True
					self.condition = "Check"
			
			self.swap_turn()
			self.opponent.is_checked = False

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
		if self.player is not None and self.player.is_clicked:
			render_funcs.render_possible_spots(self.player, self.opponent, self.board, window, self.condition)

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
			render_funcs.render_bikjang_highlight(self.player, self.opponent, window)
		if self.check:
			if self.opponent.is_checked:
				render_funcs.render_check_highlight(self.opponent, window)
			else:
				render_funcs.render_check_highlight(self.player, window)

		# DISPLAY GAME STATE INFORMATION
		# if self.player is not None and self.opponent is not None:
		# 	render_funcs.render_pieces(self.player, self.opponent, window)

		# # COVER CASE WHERE NO PLAYER HAS STARTED THEIR TURN YET
		# else:
		# 	render_funcs.render_pieces(self.player, self.opponent, window)
		render_funcs.render_pieces(self.player, self.opponent, window)

		# DISPLAY END GAME CONDITIONS/GAME_STATES
		# BIKJANG CONDITION
		if self.game_over and self.bikjang:
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

		# GAME ENDING CHECK
		if self.game_over and self.check:
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

	# Prints out the fen string of the current board
	def print_fen(self, optional_message=""):
		string_board = self.opponent.convert_board(self.board, self.player)
		fen = self.opponent.generate_fen(string_board)
		print(optional_message, fen)

	# inverts turn flags and swaps the active and waiting player variables
	def swap_turn(self):
		self.player.is_turn = not self.player.is_turn
		self.opponent.is_turn = not self.opponent.is_turn

		if self.active_player == self.player:
			self.active_player = self.opponent
			self.waiting_player = self.player
		else:
			self.active_player = self.player
			self.waiting_player = self.opponent

#--------------------------------------------------------------------------------
class LocalSinglePlayerPreGameSettings(State):


	# initialize the settings for the game
	# INPUT: No Input
	# OUTPUT: Settings menu is ready to be interacted with by player
	def __init__(self, window):
		super().__init__() # inherit the parent initializer
		self.next_state = None
		self.font = pygame.font.SysFont("Arial",size=35)
		# player and opponent will be created here to be inherited
		self.player_host = player.Player(is_host=True, board_perspective="Bottom")
		self.player_guest = player.Player(is_host=False, board_perspective="Top")

		# host retains last settings, guest is opposite
		if self.player_host.color == "Cho":
			self.player_guest.color = "Han"
		else:
			self.player_guest.color = "Cho"

		# DECLARE BUTTONS FOR PRE-GAME SETTINGS

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
		
		# play button
		x, y = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["local_MP"]["play_button"]["location"]
		width, height = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["local_MP"]["play_button"]["size"]
		font = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["local_MP"]["play_button"]["text"]["font"]
		text = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["local_MP"]["play_button"]["text"]["string"]
		foreground_color = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["local_MP"]["play_button"]["text"]["foreground_color"]
		background_color = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["local_MP"]["play_button"]["text"]["background_color"]
		hover_color = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["local_MP"]["play_button"]["text"]["hover_color"]
		self.play_button = (button.Button(x, y, width, height, font, text, foreground_color, background_color, hover_color))
		
		# boards
		self.load_board(window)
		self.render_board()

		# load button backgrounds
		self.button_background = pygame.image.load("UI/Button_Background.png").convert_alpha()

		self.button_background = (
			pygame.transform.scale(self.button_background,
				constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["local_MP"]["button_background"]["play_as"]["size"]))
		
		# play as cho/han button background
		self.play_as_background = (
			pygame.transform.scale(self.button_background,
				constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["local_MP"]["button_background"]["play_as"]["size"]))
		
		# piece convention button background
		self.piece_convention_background = (
			pygame.transform.scale(self.button_background,
				constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["local_MP"]["button_background"]["piece_convention"]["size"]))
		
		# play button background
		self.play_button_background = pygame.image.load("UI/Button_Background_Poly.png").convert_alpha()
		self.play_button_background = (pygame.transform.scale(self.play_button_background,
				constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["local_MP"]["button_background"]["play"]["size"]))
		
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

	# Listen for and handle any event ticks (clicks/buttons)
	# INPUT: pygame event object
	# OUTPUT: settings are set accordingly
	def handle_event(self, event):
		# on left mouse click, determine which button if any were clicked
		if self.is_left_click(event):
			# PLAY AS CHO
			if self.cho_side_button.is_clicked():
				self.player_host.color ="Cho"
				self.player_guest.color = "Han"
			# PLAY AS HAN
			elif self.han_side_button.is_clicked():
				self.player_host.color = "Han"
				self.player_guest.color = "Cho"
			# PLAY WITH STANDARD PIECE LOGOS
			elif self.standard_piece_convention_button.is_clicked():
				self.player_host.piece_convention = "Standard"
				self.player_guest.piece_convention = "Standard"
			# PLAY WITH INTERNATIONAL PIECE LOGOS
			elif self.internat_piece_convention_button.is_clicked():
				self.player_host.piece_convention = "International"
				self.player_guest.piece_convention = "International"
			# CLICK CONFIRM SETTINGS IF ALL ARE SET
			elif self.play_button.is_clicked():
				helper_funcs.update_player_settings(self.player_host)
				self.next_state = "Local Single Player Game"
						
		# escape to main menu
		elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
			self.next_state = "Main Menu"
				
	# Handle any rendering that needs to be done
	# INPUT: pygame surface object (window to display to)
	# OUTPUT: All pre-game settings attributes/actions are rendered
	def render(self, window):
		# USE BOARD AS BACKGROUND
		window.blit(self.menu_background, self.menu_background.get_rect(center = window.get_rect().center))
		window.blit(self.playboard, self.playboard.get_rect(center = window.get_rect().center))
		
		# SELECT PIECE SIDE TO PLAY AS (CHO/HAN)
		window.blit(self.play_as_background, 
			   constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["local_MP"]["button_background"]["play_as"]["location"])
		text = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["local_MP"]["button_background"]["play_as"]["text"]["string"]
		x, y = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["local_MP"]["button_background"]["play_as"]["text"]["location"]
		font_size = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["local_MP"]["button_background"]["play_as"]["text"]["font_size"]

		self.draw_text(window, text, x, y, font_size)
		self.cho_side_button.draw_button(window)
		self.han_side_button.draw_button(window)
		
		# SELECT PIECE TYPE CONVENTION TO PLAY WITH (STANDARD/INTERNATIONAL)
		window.blit(self.piece_convention_background, 
			   constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["local_MP"]["button_background"]["piece_convention"]["location"])
		text = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["local_MP"]["button_background"]["piece_convention"]["text"]["string"]
		x, y = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["local_MP"]["button_background"]["piece_convention"]["text"]["location"]
		font_size = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["local_MP"]["button_background"]["piece_convention"]["text"]["font_size"]

		self.draw_text(window, text, x, y, font_size)
		self.standard_piece_convention_button.draw_button(window)
		self.internat_piece_convention_button.draw_button(window)

		# PLAY BUTTON
		window.blit(self.play_button_background, 
			   constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["local_MP"]["button_background"]["play"]["location"])
		self.play_button.draw_button(window)

		

		# DISPLAY PREVIEW OF THE PIECES ON HOW THEY WILL LOOK	
		if self.player_host is not None:

			# player header to notify which display is player's
			window.blit(self.player_header_background, 
			   constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]
			   ["background_elements"]["local_MP"]["button_background"]["player_piece_display"]["player_header"]["location"])
			
			# player header text display
			text = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["local_MP"]["button_background"]["player_piece_display"]["text"]["string"]
			x, y = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["local_MP"]["button_background"]["player_piece_display"]["text"]["location"]
			font_size = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["local_MP"]["button_background"]["player_piece_display"]["text"]["font_size"]
			self.draw_text(window, text, x, y, font_size)

			# player piece display
			window.blit(self.player_piece_display_background, 
			   constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["local_MP"]["button_background"]["player_piece_display"]["location"])

			   	
			# opponent piece display
			window.blit(self.opponent_piece_display_background, 
			   constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["local_MP"]["button_background"]["opponent_piece_display"]["location"])

			# render pieces
			render_funcs.PreGame_render_piece_display(window, self.player_host, self.player_guest)
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
		self.load_board(window)
		self.render_board()

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
		self.han_player = self.player_host if self.player_host.color == "Han" else self.player_guest
		self.cho_player = self.player_guest if self.player_guest.color == "Cho" else self.player_host
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
			elif self.active_player is not None and self.active_player.is_clicked and not self.opening_turn:
				# unclick that piece if the move was successful/valid
				if helper_funcs.attempt_move(self.active_player, self.waiting_player, self.board, mouse_pos, self.condition):
					helper_funcs.player_piece_unclick(self.active_player)
					# end of turn update
					if helper_funcs.detect_bikjang(self.active_player, self.waiting_player):
						self.bikjang = True
						self.condition = "Bikjang"
						self.winner = self.active_player
						self.game_over = True
					elif helper_funcs.detect_check(self.waiting_player, self.active_player, self.board):
						self.check = True
						self.condition = "Check"
					# switch turns
					temp_info = self.active_player
					self.active_player = self.waiting_player
					self.waiting_player = temp_info

				# otherwise the player is clicking another piece or invalid spot
				else:
					# reset click state
					helper_funcs.player_piece_unclick(self.active_player)
					# update click to new piece if valid clicked
					helper_funcs.player_piece_clicked(self.active_player, mouse_pos)

			# otherwise, check if any player-side pieces were clicked
			elif helper_funcs.player_piece_clicked(self.active_player, mouse_pos):
				# FUTURE LOGIC HERE
				pass
			# IMPLEMENT FURTHER BRANCHES HERE FOR FUTURE IMPLEMENTATIONS
		# if something...
			# do something ...
		# elif something
			# do etc...

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
		window.blit(self.menu_background, self.menu_background.get_rect(center = window.get_rect().center))
		window.blit(self.playboard, self.playboard.get_rect(center = window.get_rect().center))

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
			render_funcs.render_pieces(self.player_host, self.player_guest, window)

		# DISPLAY END GAME CONDITIONS/GAME_STATES
		# BIKJANG CONDITION
		if self.game_over and self.bikjang:
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

		# GAME ENDING CHECK
		if self.game_over and self.check:
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

# class MultiplayerPreGameSettings(State):
# 	pass

class Multiplayer(State):

	def __init__(self, window):
		super().__init__()
		# load and render board
		self.load_board(window)
		self.render_board()

		# initalizing players
		self.player_host = player.Player(is_host=True, board_perspective="Bottom")
		self.player_guest = player.Player(is_host=False, board_perspective="Top")

	def handle_event(self, event):
		self.immediate_render = False
		# get the player's mouse position for click tracking
		mouse_pos = pygame.mouse.get_pos()

	def render(self, window):
		window.blit(self.menu_background, self.menu_background.get_rect(center = window.get_rect().center))
		window.blit(self.playboard, self.playboard.get_rect(center = window.get_rect().center))

		render_funcs.render_pieces(self.player_host, self.player_guest, window)