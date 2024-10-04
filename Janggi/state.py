"""
----------------------state.py----------------------------
o This file is to manage the current game mode (state) the
	program is in
o Last Modified - October 4th 2024
----------------------------------------------------------
"""

# libraries
import pygame

# local file imports, see individ file for details
import board
import button
import constants
import helper_funcs
import opponent
import player
import render_funcs

#--------------------------------------------------------------------------------
# Parent State to act as a base class to be inherited by 
#--------------------------------------------------------------------------------
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

	# Method to draw text information out to the window
	# INPUT: window object, text to be displayed, (x,y) of where to write on, font size
	# OUTPUT: Window contains the text to be displayed
	def draw_text(self, window, text, x=0, y=0, font_size=30):
		font = pygame.font.SysFont("Arial", font_size)
		text_surface = font.render(text, True, constants.WHITE)
		window.blit(text_surface, (x, y))

#--------------------------------------------------------------------------------
# MAIN MENU TO TRANSITION INTO SINGLEPLAYER/MULTIPLAYER/ETC...
#--------------------------------------------------------------------------------
class MainMenu(State):
	# initialize the settings for the game
	# INPUT: No Input
	# OUTPUT: Main menu is ready to be interacted with by player
	def __init__(self):
		super().__init__()
		self.next_state = None
		self.font = pygame.font.SysFont("Arial",50)
		self.singleplayer_button = (button.Button(250,350,500,100, 
									font=self.font,
							  		 text="Play against an AI", 
									 foreground_color = constants.WHITE,
									 background_color = constants.BLACK,  
									 hover_color = constants.LIGHT_GREEN))
		self.menu_background = pygame.image.load("Board/Janggi_Board.png").convert_alpha()
		self.menu_background = pygame.transform.scale(self.menu_background, constants.board_size)

	# Listen for and handle any event ticks (clicks/buttons)
	# INPUT: pygame event object
	# OUTPUT: Menu transitions are set accordingly
	def handle_event(self, event):
		if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
			if self.singleplayer_button.is_clicked():
				#self.next_state = "Single Player Game"
				self.next_state = "Single Player Pre-Game Settings"
			else:
				# multiplayer state change here here
				pass

	# Handle any rendering that needs to be done
	# INPUT: pygame surface object (window to display to)
	# OUTPUT: All menu attributes/actions are rendered
	def render(self, window):
		window.blit(self.menu_background, constants.board_image)
		self.singleplayer_button.draw_button(window)

#--------------------------------------------------------------------------------
# THIS STATE WILL HANDLE SETTINGS FOR SETTING UP THE GAME AGAINST AN AI
#--------------------------------------------------------------------------------
class SinglePlayerPreGameSettings(State):
	# player and opponent will be created here to be inherited
	player = player.Player()
	opponent = opponent.Opponent()

	# initialize the settings for the game
	# INPUT: No Input
	# OUTPUT: Settings menu is ready to be interacted with by player
	def __init__(self):
		self.next_state = None
		self.font = pygame.font.SysFont("Arial",35)
		self.ai_level = "Easy"

		# DECLARE BUTTONS FOR PRE-GAME SETTINGS
		self.cho_side_button = (button.Button(185,225,100,50, 
									font=self.font,
							  		 text="Cho", 
									 foreground_color = constants.BLACK,
									 background_color = constants.WHITE,
									 hover_color = constants.LIGHT_GREEN))
		self.han_side_button = (button.Button(335,225,100,50, 
									font=self.font,
							  		 text="Han", 
									 foreground_color = constants.BLACK,
									 background_color = constants.WHITE,
									 hover_color = constants.LIGHT_GREEN))
		self.standard_piece_convention_button = (button.Button(175,425,175,50, 
													font=self.font,
													text="Standard", 
													foreground_color = constants.BLACK,
													background_color = constants.WHITE,
													hover_color = constants.LIGHT_GREEN))
		self.internat_piece_convention_button = (button.Button(375,425,175,50, 
													font=self.font,
													text="International", 
													foreground_color = constants.BLACK,
													background_color = constants.WHITE,
													hover_color = constants.LIGHT_GREEN))
		# create a button for each ai level 0 --> 9
		self.ai_level_buttons = button.create_ai_level_buttons()

		self.play_button = (button.Button(445,785,125,50, 
									font=self.font,
							  		 text="Play", 
									 foreground_color = constants.BLACK,
									 background_color = constants.WHITE,
									 hover_color = constants.LIGHT_GREEN))
		
		self.menu_background = pygame.image.load("Board/Janggi_Board.png").convert_alpha()
		self.menu_background = pygame.transform.scale(self.menu_background, constants.board_size)

	# Listen for and handle any event ticks (clicks/buttons)
	# INPUT: pygame event object
	# OUTPUT: settings are set accordingly
	def handle_event(self, event):
		# on left mouse click, determine which button if any were clicked
		if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
			# PLAY AS CHO
			if self.cho_side_button.is_clicked():
				SinglePlayerPreGameSettings.player.color ="Cho"
				SinglePlayerPreGameSettings.opponent.color = "Han"
			# PLAY AS HAN
			elif self.han_side_button.is_clicked():
				SinglePlayerPreGameSettings.player.color = "Han"
				SinglePlayerPreGameSettings.opponent.color = "Cho"
			# PLAY WITH STANDARD PIECE LOGOS
			elif self.standard_piece_convention_button.is_clicked():
				SinglePlayerPreGameSettings.player.piece_convention = "Standard"
			# PLAY WITH INTERNATIONAL PIECE LOGOS
			elif self.internat_piece_convention_button.is_clicked():
				SinglePlayerPreGameSettings.player.piece_convention = "International"
			# CLICK CONFIRM SETTINGS IF ALL ARE SET
			elif (self.play_button.is_clicked() 
		 		  and SinglePlayerPreGameSettings.player is not None):
				helper_funcs.update_player_settings(SinglePlayerPreGameSettings.player)
				self.next_state = "Single Player Game"
			# OTHERWISE FIND IF ANY OF THE AI LEVELS WERE SET
			else:
				for button in self.ai_level_buttons:
					if button.is_clicked():
						self.ai_level = button.text
						SinglePlayerPreGameSettings.player.ai_level = button.text

				
	# Handle any rendering that needs to be done
	# INPUT: pygame surface object (window to display to)
	# OUTPUT: All pre-game settings attributes/actions are rendered
	def render(self, window):
		# USE BOARD AS BACKGROUND
		window.blit(self.menu_background, constants.board_image)

		# SELECT PIECE SIDE TO PLAY AS (CHO/HAN)
		self.side_button_background_rect = (150, 165, 325, 125)
		pygame.draw.rect(window, constants.BLACK, self.side_button_background_rect)
		self.draw_text(window, "Select Side to Play as", 175, 175, 35)
		self.cho_side_button.draw_button(window)
		self.han_side_button.draw_button(window)

		# SELECT PIECE TYPE CONVENTION TO PLAY WITH (STANDARD/INTERNATIONAL)
		self.piece_type_button_background_rect = (150, 365, 425, 125)
		pygame.draw.rect(window, constants.BLACK, self.piece_type_button_background_rect)
		self.draw_text(window, "Select Piece Convention", 175, 365, 35)
		self.standard_piece_convention_button.draw_button(window)
		self.internat_piece_convention_button.draw_button(window)

		# SELECT AI LEVEL TO PLAY AGAINST (Easy/Medium/Hard)
		self.ai_level_buttons_rect = (150, 585, 475, 125)
		pygame.draw.rect(window, constants.BLACK, self.ai_level_buttons_rect)
		self.draw_text(window, "Select AI Difficulty Level: ", 175, 585, 35)
		self.draw_text(window, f"{SinglePlayerPreGameSettings.player.ai_level}", 500, 585, 35)
		for button in self.ai_level_buttons:
			button.draw_button(window)

		# CONFIRM SETTINGS BUTTON
		self.play_button_background_rect = (432.5, 760, 150, 100)
		pygame.draw.rect(window, constants.BLACK, self.play_button_background_rect)
		self.play_button.draw_button(window)

		# DISPLAY PREVIEW OF THE PIECES ON HOW THEY WILL LOOK	
		if SinglePlayerPreGameSettings.player is not None:
			self.piece_display_background_rect = (654, 110, 100, 650)
			pygame.draw.rect(window, constants.BLACK, self.piece_display_background_rect)
			render_funcs.PreGame_render_piece_display(window, SinglePlayerPreGameSettings.player)

			"""
			# KEEP IMPLEMENTATION HERE JUST IN-CASE/ OR FOR DEBUG PURPOSES
			# SHOW SUMMARY OF CURRENT SELECTION OF SETTINGS
			self.current_settings_background_rect = (150, 650, 485, 150)
			pygame.draw.rect(window, constants.BLACK, self.current_settings_background_rect)
			self.current_settings_background_rect_ai = (150, 750, 685, 50)
			pygame.draw.rect(window, constants.BLACK, self.current_settings_background_rect_ai)
			self.draw_text(window, f"You will be playing as {SinglePlayerPreGameSettings.player.color}", 160, 650, 35) 
			self.draw_text(window, f"You will be using {SinglePlayerPreGameSettings.player.piece_convention} pieces", 160, 700, 35) 
			self.draw_text(window, f"You will be playing against a(n) {self.ai_level} AI opponent", 160, 750, 35)
			"""

#--------------------------------------------------------------------------------
# Inherited State for single player gaming against an ai
#--------------------------------------------------------------------------------
class SinglePlayerGame(SinglePlayerPreGameSettings):
	# initialize the gamestate
	# INPUT: No Input
	# OUTPUT: Gamestate is initialized and ready for playing
	def __init__(self):
		super().__init__()
		# create game objects
		self.board = board.Board()
		self.player = SinglePlayerPreGameSettings.player
		self.opponent = SinglePlayerPreGameSettings.opponent
		
		# display the window
		self.window = pygame.display.set_mode(
			(constants.window_width, constants.window_height))
		pygame.display.set_caption("Janggi")

		if self.player.color == "Cho":
			self.player.is_turn = True
		else:
			self.opponent.is_turn = True

	# Listen for and handle any event ticks (clicks/buttons)
	# INPUT: pygame event object
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
		#render_funcs.render_piece_collisions(self.player, self.opponent, self.window)
		# load the pieces on the board for both teams
		render_funcs.render_pieces(self.player, self.opponent, self.window)