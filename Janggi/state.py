"""
----------------------state.py----------------------------
o This file is to manage the current game mode (state) the
	program is in
o Last Modified - October 31st 2024
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
import ai

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
	def __init__(self, window):
		super().__init__() # inherit the parent initializer
		self.next_state = None
		self.font = pygame.font.SysFont("Arial",size=50)
		# button for single player
		self.singleplayer_button = (button.Button(x=635,y=350,width=500,height=100, 
									font=self.font,
							  		text="Play against an AI", 
									foreground_color = constants.WHITE,
									background_color = constants.BLACK,  
									hover_color = constants.LIGHT_GREEN))

		# button for multiplayer
		self.multiplayer_button = (button.Button(x=635,y=550,width=500,height=100, 
									font=self.font,
							  		text="Play against a friend", 
									foreground_color = constants.WHITE,
									background_color = constants.BLACK,  
									hover_color = constants.LIGHT_GREEN))

		# button for exiting application
		self.exit_button = (button.Button(x=635,y=750,width=500,height=100, 
									font=self.font,
							  		text="Close application", 
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
				self.next_state = "Single Player Pre-Game Settings"

			elif self.multiplayer_button.is_clicked():
				self.next_state = "Multi Player Pre-Game Settings"

			elif self.exit_button.is_clicked():
				constants.running = False

	# Handle any rendering that needs to be done
	# INPUT: pygame surface object (window to display to)
	# OUTPUT: All menu attributes/actions are rendered
	def render(self, window):
		# background
		window.blit(self.menu_background, constants.board_image)

		# draw buttons to window
		self.singleplayer_button.draw_button(window)
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
		self.player = player.Player()
		self.opponent = opponent.Opponent()

		# DECLARE BUTTONS FOR PRE-GAME SETTINGS
		self.cho_side_button = (button.Button(x=750,y=225,width=100,height=50, 
									font=self.font,
							  		text="Cho", 
									foreground_color = constants.BLACK,
									background_color = constants.WHITE,
									hover_color = constants.LIGHT_GREEN))
		
		self.han_side_button = (button.Button(x=915, y=225,width=100,height=50, 
									font=self.font,
							  		text="Han", 
									foreground_color = constants.BLACK,
									background_color = constants.WHITE,
									hover_color = constants.LIGHT_GREEN))
		
		self.standard_piece_convention_button = (button.Button(x=750,y=425,width=175,height=50, 
													font=self.font,
													text="Standard", 
													foreground_color = constants.BLACK,
													background_color = constants.WHITE,
													hover_color = constants.LIGHT_GREEN))
		self.internat_piece_convention_button = (button.Button(x=950,y=425,width=175,height=50, 
													font=self.font,
													text="International", 
													foreground_color = constants.BLACK,
													background_color = constants.WHITE,
													hover_color = constants.LIGHT_GREEN))

		self.play_button = (button.Button(x=735,y=835,width=125,height=50, 
									font=self.font,
							  		text="Play", 
									foreground_color = constants.BLACK,
									background_color = constants.WHITE,
									hover_color = constants.LIGHT_GREEN))
		
		# create a button for each ai level 0 --> 9
		self.ai_level_buttons = button.create_ai_level_buttons()
		
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
				self.player.color ="Cho"
				self.opponent.color = "Han"
			# PLAY AS HAN
			elif self.han_side_button.is_clicked():
				self.player.color = "Han"
				self.opponent.color = "Cho"
			# PLAY WITH STANDARD PIECE LOGOS
			elif self.standard_piece_convention_button.is_clicked():
				self.player.piece_convention = "Standard"
			# PLAY WITH INTERNATIONAL PIECE LOGOS
			elif self.internat_piece_convention_button.is_clicked():
				self.player.piece_convention = "International"
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
						
	# escape to main menu
		elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
			self.next_state = "Main Menu"
				
	# Handle any rendering that needs to be done
	# INPUT: pygame surface object (window to display to)
	# OUTPUT: All pre-game settings attributes/actions are rendered
	def render(self, window):
		# USE BOARD AS BACKGROUND
		window.blit(self.menu_background, constants.board_image)

		# SELECT PIECE SIDE TO PLAY AS (CHO/HAN)
		#								 (x, y, size_x, size_y)
		self.side_button_background_rect = (720, 165, 325, 125)
		pygame.draw.rect(window, color=constants.BLACK, rect=self.side_button_background_rect)
		self.draw_text(window, text="Select Side to Play as", x=750, y=175, font_size=35)
		self.cho_side_button.draw_button(window)
		self.han_side_button.draw_button(window)

		# SELECT PIECE TYPE CONVENTION TO PLAY WITH (STANDARD/INTERNATIONAL)
		#										(x,	y, size_x, size_y)
		self.piece_type_button_background_rect = (720, 365, 425, 125)
		pygame.draw.rect(window, color=constants.BLACK, rect=self.piece_type_button_background_rect)
		self.draw_text(window, text="Select Piece Convention", x=750, y=365, font_size=35)
		self.standard_piece_convention_button.draw_button(window)
		self.internat_piece_convention_button.draw_button(window)

		# SELECT AI LEVEL TO PLAY AGAINST (Easy/Medium/Hard)
		#							(x,	y, size_x, size_y)
		self.ai_level_buttons_rect = (720, 585, 475, 125)
		pygame.draw.rect(window, color=constants.BLACK, rect=self.ai_level_buttons_rect)
		self.draw_text(window, text="Select AI Difficulty Level: ", x=750, y=585, font_size=35)
		self.draw_text(window, text=f"{self.player.ai_level}", x=1075, y=585, font_size=35)
		for button in self.ai_level_buttons:
			button.draw_button(window)

		# CONFIRM SETTINGS BUTTON
		#									(x,	y, size_x, size_y)
		self.play_button_background_rect = (720, 810, 150, 100)
		pygame.draw.rect(window, color=constants.BLACK, rect=self.play_button_background_rect)
		self.play_button.draw_button(window)

		# DISPLAY PREVIEW OF THE PIECES ON HOW THEY WILL LOOK	
		if self.player is not None:
			#									(x,	y, size_x, size_y)
			self.piece_display_background_rect = (517.5, 120, 100, 700)
			pygame.draw.rect(window, color=constants.BLACK, rect=self.piece_display_background_rect)
			render_funcs.PreGame_render_piece_display(window, player=self.player, opponent=None)

#--------------------------------------------------------------------------------
# Inherited State for single player gaming against an ai
#--------------------------------------------------------------------------------
class SinglePlayerGame(SinglePlayerPreGameSettings):
	# initialize the gamestate
	# INPUT: No Input
	# OUTPUT: Gamestate is initialized and ready for playing
	def __init__(self, window):
		super().__init__(window)
		# create game objects
		self.board = board.Board()
		self.player = self.player
		self.opponent = ai.OpponentAI()

		# load then display board image
		menu_background = pygame.image.load("Board/Janggi_Board.png").convert_alpha()
		menu_background = pygame.transform.scale(menu_background, constants.board_size)

		# Cho side goes first
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
		# escape from game to main menu
		elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
			self.next_state = "Main Menu"

		# Handle AI Opponent's turn
		if self.opponent.is_turn:
			fen = self.opponent.generate_fen(self.board, self.opponent.active_player)

			self.opponent.send_command(f"position fen {fen}")
			self.opponent.send_command("go depth 1")	# Pick based on difficulty

			# Retrieve the engine's move
			try:
				best_move = self.opponent.get_engine_move()
				print(f"Engine's move: {best_move}")
			except Exception as e:
				print(f"Error retrieving move: {e}")

			# This code tranlates the stockfish best move "i3h3" into
			# numbers that we can use for the actual move.

			####################################
			# We need to after this, actually update the move of the oppenent 
			########################################
			starting_col = 0
			starting_row = 0
			ending_col = 0
			ending_row = 0

			starting_col = ord(best_move[0].lower()) - 96
			starting_row = int(best_move[1])
			ending_col = ord(best_move[2].lower()) - 96
			ending_row = int(best_move[3])

				
			
			# Apply the move
			#self.apply_move(best_move)

			self.opponent.send_command("quit")

			self.opponent.is_turn = False
			self.player.is_turn = True
			
	# Handle any rendering that needs to be done
	# INPUT: pygame surface object (window to display to)
	# OUTPUT: All game attributes/actions are rendered
	def render(self, window):
		# display board to window
		window.blit(self.menu_background, constants.board_image)

		# if player has a piece currently clicked, render where it can go
		if self.player.is_clicked:
			render_funcs.render_possible_spots(self.player, self.opponent, self.board, window)

		# render collision rectangles for the pieces on both sides
		render_funcs.render_piece_collisions(self.player, self.opponent, window)

		# load the pieces on the board for both teams
		render_funcs.render_pieces(self.player, self.opponent, window)

#--------------------------------------------------------------------------------
# THIS STATE WILL HANDLE SETTINGS FOR SETTING UP GAME AGAINST ANOTHER A PLAYER
#--------------------------------------------------------------------------------
class MultiPlayerPreGameSettings(State):
	# initialize the settings for the game
	# INPUT: No Input	
	# OUTPUT: Settings menu is ready to be interacted with by player
	def __init__(self, window):
		super().__init__() # inherit the parent initializer
		self.next_state = None
		self.font = pygame.font.SysFont("Arial",35)
		self.is_connected = False
		# players will be created here to be inherited
		self.player_host = player.Player()
		self.player_guest = None

		# DECLARE BUTTONS FOR PRE-GAME SETTINGS
		self.cho_side_button = (button.Button(x=750,y=225,width=100,height=50, 
									font=self.font,
							  		text="Cho", 
									foreground_color = constants.BLACK,
									background_color = constants.WHITE,
									hover_color = constants.LIGHT_GREEN))
		
		self.han_side_button = (button.Button(x=915, y=225,width=100,height=50, 
									font=self.font,
							  		text="Han", 
									foreground_color = constants.BLACK,
									background_color = constants.WHITE,
									hover_color = constants.LIGHT_GREEN))
		
		self.standard_piece_convention_button = (button.Button(x=700,y=425,width=175,height=50, 
													font=self.font,
													text="Standard", 
													foreground_color = constants.BLACK,
													background_color = constants.WHITE,
													hover_color = constants.LIGHT_GREEN))
		
		self.internat_piece_convention_button = (button.Button(x=900,y=425,width=175,height=50, 
													font=self.font,
													text="International", 
													foreground_color = constants.BLACK,
													background_color = constants.WHITE,
													hover_color = constants.LIGHT_GREEN))

		"""self.matchmake_button = (button.Button(x=750,y=615,width=200,height=50, 
										font=self.font,
										text="Invite a friend via e-mail", 
										foreground_color = constants.BLACK,
										background_color = constants.WHITE,
										hover_color = constants.LIGHT_GREEN))"""
		
		self.play_button = (button.Button(x=820,y=850,width=125,height=50, 
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
				self.player_host.color ="Cho"
				if self.player_guest is not None:
					self.player_guest.color = "Han"
			# PLAY AS HAN
			elif self.han_side_button.is_clicked():
				self.player_host.color = "Han"
				if self.player_guest is not None:
					self.player_guest.color = "Cho"
			# PLAY WITH STANDARD PIECE LOGOS
			elif self.standard_piece_convention_button.is_clicked():
				self.player_host.piece_convention = "Standard"
			# PLAY WITH INTERNATIONAL PIECE LOGOS
			elif self.internat_piece_convention_button.is_clicked():
				self.player_host.piece_convention = "International"
			# CLICK CONFIRM SETTINGS IF ALL ARE SET
			elif (self.play_button.is_clicked() 
		 		  and self.player_guest is not None):
				helper_funcs.update_player_settings(self.player_host)
				self.next_state = "Main Menu"
			# OTHERWISE FIND IF ANY OF THE AI LEVELS WERE SET
			else: # multiplayer connecting stuff here
				pass
	# escape to main menu
		elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
			self.next_state = "Main Menu"
				
	# Handle any rendering that needs to be done
	# INPUT: pygame surface object (window to display to)
	# OUTPUT: All pre-game settings attributes/actions are rendered
	def render(self, window):
		# USE BOARD AS BACKGROUND
		window.blit(self.menu_background, constants.board_image)

		# SELECT PIECE SIDE TO PLAY AS (CHO/HAN)
		#								 (x, y, size_x, size_y)
		self.side_button_background_rect = (720, 165, 325, 125)
		pygame.draw.rect(window, color=constants.BLACK, rect=self.side_button_background_rect)
		self.draw_text(window, text="Select Side to Play as", x=750, y=175, font_size=35)
		self.cho_side_button.draw_button(window)
		self.han_side_button.draw_button(window)

		# SELECT PIECE TYPE CONVENTION TO PLAY WITH (STANDARD/INTERNATIONAL)
		#										(x,	y, size_x, size_y)
		self.piece_type_button_background_rect = (672, 365, 425, 125)
		pygame.draw.rect(window, color=constants.BLACK, rect=self.piece_type_button_background_rect)
		self.draw_text(window, text="Select Piece Convention", x=725, y=365, font_size=35)
		self.standard_piece_convention_button.draw_button(window)
		self.internat_piece_convention_button.draw_button(window)

		# MATCHMAKE TEXT BOX
		#							(x,	y, size_x, size_y)
		self.matchmake_button_rect = (672.5, 575, 425, 200)
		pygame.draw.rect(window, color=constants.BLACK, rect=self.matchmake_button_rect)
		self.draw_text(window, text="Send an Invite Link Via E-mail", x=700, y=575, font_size=35)

		# CONFIRM SETTINGS BUTTON
		#									(x,	y, size_x, size_y)
		self.play_button_background_rect = (805.5, 825, 150, 100)
		pygame.draw.rect(window, color=constants.BLACK, rect=self.play_button_background_rect)
		self.play_button.draw_button(window)

		# DISPLAY PREVIEW OF THE PIECES ON HOW THEY WILL LOOK	
		if self.player_guest is not None:
			#										(x,	y, size_x, size_y)
			self.guest_piece_display_background_rect = (1150.5, 120, 100, 700)
			pygame.draw.rect(window, color=constants.BLACK, rect=self.guest_piece_display_background_rect)
		if self.player_host is not None:
			#											(x,	y, size_x, size_y)
			self.host_piece_display_background_rect = (517.5, 120, 100, 700)
			pygame.draw.rect(window, color=constants.BLACK, rect=self.host_piece_display_background_rect)
			render_funcs.PreGame_render_piece_display(window, self.player_host, self.player_guest)
