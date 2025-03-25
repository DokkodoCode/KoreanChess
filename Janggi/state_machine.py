"""
----------------------state_machine.py----------------------------
o This file is the actual state machine that will handle the 
	transitioning between gamestates (Menu,Game, etc...)
o Last Modified - March 21st 2025
----------------------------------------------------------
"""
# libraries
import pygame
import time

# specific local file importing of the States
import state

# The State Machine that will transiton the program between states
class StateManager():
	# Class initializer
	# INPUT: None
	# OUTPUT: 
	#			1) Dictionary containg all available game states
	#				 to transition between
	#			2) An empty dictionary that will allow us to create 
	#				 new game states during runtime (for things such as
	#				 escaping to a menu)
	#			3) The starting state of the program
	def __init__(self, window):
		self.states = {
			"Main Menu" : state.MainMenu, 
			"Single Player Pre-Game Settings" : state.SinglePlayerPreGameSettings,
			"Single Player Game" : state.SinglePlayerGame,
			"Local Single Player Pre-Game Settings" : state.LocalSinglePlayerPreGameSettings,
			"Local Single Player Game" : state.LocalSinglePlayerGame,
			"Multi Player Pre-Game Settings" : state.MultiplayerPreGameSettings,
			"Multi Player Game" : state.Multiplayer
		}
		
		self.states_unitialized = {}
		self.current_state = None
		# start here
		self.change_state("Main Menu", window)

	# Event handler that will call the event handler for the current given state
	# INPUT: pygame event object
	# OUTPUT: Current state event is handled
	def handle_event(self, event):
		if self.current_state:
			self.current_state.handle_event(event)
			
	# Updater that will call the update method of the current state or change
	# states when appropriate
	# INPUT: None
	# OUTPUT: Current state event is handled, or state change is called for
	def update(self, window):
		if self.current_state:
			self.current_state.update()
			if self.current_state.next_state:
				self.change_state(self.current_state.next_state, window)

	# Method that will change what state the program is in
	# INPUT: The new_state to transition to as a string
	# OUTPUT: State of program is changed
	def change_state(self, new_state, window):
		# state to change to
		if new_state == "Single Player Game":
			if "Single Player Game" in self.states_unitialized:
				del self.states_unitialized["Single Player Game"]
			self.states_unitialized["Single Player Game"] = state.SinglePlayerGame(window)

		elif new_state == "Single Player Pre-Game Settings":
			if "Single Player Pre-Game Settings" in self.states_unitialized:
				del self.states_unitialized["Single Player Pre-Game Settings"]
			self.states_unitialized["Single Player Pre-Game Settings"] = state.SinglePlayerPreGameSettings(window)

		elif new_state == "Local Single Player Pre-Game Settings":
			if "Local Single Player Pre-Game Settings" in self.states_unitialized:
				del self.states_unitialized["Local Single Player Pre-Game Settings"]
			self.states_unitialized["Local Single Player Pre-Game Settings"] = state.LocalSinglePlayerPreGameSettings(window)

		elif new_state == "Local Single Player Game":
			if "Local Single Player Game" in self.states_unitialized:
				del self.states_unitialized["Local Single Player Game"]
			self.states_unitialized["Local Single Player Game"] = state.LocalSinglePlayerGame(window)

		elif new_state == "Main Menu":
			if "Main Menu" in self.states_unitialized:
				del self.states_unitialized["Main Menu"]
			self.states_unitialized["Main Menu"] = state.MainMenu(window)

		elif new_state == "Multi Player Pre-Game Settings":
			if "Multi Player Pre-Game Settings" in self.states_unitialized:
				del self.states_unitialized["Multi Player Pre-Game Settings"]
			self.states_unitialized["Multi Player Pre-Game Settings"] = state.MultiplayerPreGameSettings(window)

		elif new_state == "Multi Player Game":
			# Preserve the connection and settings from the pre-game settings state
			prev_settings = None
			connection = None
			is_host = None
			settings_confirmed = False
			
			if "Multi Player Pre-Game Settings" in self.states_unitialized:
				prev_settings = self.states_unitialized["Multi Player Pre-Game Settings"]
				print(f"Found previous multiplayer settings: {prev_settings is not None}")
				
				# Save connection and relevant settings before we delete the settings state
				if prev_settings and hasattr(prev_settings, 'connection'):
					connection = prev_settings.connection
					is_host = prev_settings.is_host
					settings_confirmed = getattr(prev_settings, 'settings_confirmed', False)
					host_color = prev_settings.host.color
					guest_color = prev_settings.guest.color
					piece_convention = prev_settings.host.piece_convention
			
			# Create a new multiplayer game instance without triggering a new connection
			multiplayer_game = state.Multiplayer.__new__(state.Multiplayer)
			
			# Initialize the base State class
			state.State.__init__(multiplayer_game)
			
			# Set critical attributes to prevent new connection
			multiplayer_game.connection = connection
			multiplayer_game.is_host = is_host
			multiplayer_game.settings_confirmed = settings_confirmed
			
			# Manual initialization without calling establish_connection()
			multiplayer_game.next_state = None
			multiplayer_game.font = pygame.font.SysFont("Arial", size=35)
			
			# Initialize players
			multiplayer_game.host = state.player.Player(is_host=True, board_perspective="Bottom")
			multiplayer_game.guest = state.player.Player(is_host=False, board_perspective="Top")
			
			# Transfer player settings
			multiplayer_game.host.color = host_color
			multiplayer_game.guest.color = guest_color
			multiplayer_game.host.piece_convention = piece_convention
			multiplayer_game.guest.piece_convention = piece_convention
			
			# Initialize game board and state
			multiplayer_game.load_board_boarder(window)
			multiplayer_game.load_board()
			multiplayer_game.board = state.board.Board()
			multiplayer_game.condition = "None"
			multiplayer_game.bikjang = False
			multiplayer_game.check = False
			multiplayer_game.game_over = False
			multiplayer_game.immediate_render = False
			multiplayer_game.last_move_time = 0
			multiplayer_game.sync_cooldown = 100
			
			# Make sure each player has the correct board perspective
			if multiplayer_game.is_host:
				# Host perspective setup
				multiplayer_game.host.board_perspective = "Bottom"
				multiplayer_game.guest.board_perspective = "Top"
				multiplayer_game.local_player = multiplayer_game.host
				multiplayer_game.remote_player = multiplayer_game.guest
			else:
				# Client perspective setup
				multiplayer_game.host.board_perspective = "Top"
				multiplayer_game.guest.board_perspective = "Bottom"
				multiplayer_game.local_player = multiplayer_game.guest
				multiplayer_game.remote_player = multiplayer_game.host
			
			# Initialize player pieces with correct perspectives
			multiplayer_game.initialize_pieces = state.Multiplayer.initialize_pieces.__get__(multiplayer_game)
			multiplayer_game.initialize_pieces()
			
			# Initialize Cho/Han player references
			multiplayer_game.han_player = multiplayer_game.host if multiplayer_game.host.color == "Han" else multiplayer_game.guest
			multiplayer_game.cho_player = multiplayer_game.guest if multiplayer_game.guest.color == "Cho" else multiplayer_game.host
			
			# Initialize game state based on role (host/client)
			if multiplayer_game.is_host:
				# Host starts with horse swap phase
				multiplayer_game.opening_turn = True
				multiplayer_game.waiting_for_opponent_swap = False
				multiplayer_game.active_player = multiplayer_game.host
				multiplayer_game.waiting_player = multiplayer_game.guest
			else:
				# Client waits for host to complete horse swap
				multiplayer_game.opening_turn = True
				multiplayer_game.waiting_for_opponent_swap = True
				multiplayer_game.active_player = multiplayer_game.guest
				multiplayer_game.waiting_player = multiplayer_game.host
			
			# Initialize swap UI
			multiplayer_game.init_swap_menu = state.Multiplayer.init_swap_menu.__get__(multiplayer_game)
			multiplayer_game.init_swap_menu()
			
			# Initialize event handler methods
			multiplayer_game.is_our_turn = state.Multiplayer.is_our_turn.__get__(multiplayer_game)
			multiplayer_game.check_for_messages = state.Multiplayer.check_for_messages.__get__(multiplayer_game)
			multiplayer_game.process_swap_message = state.Multiplayer.process_swap_message.__get__(multiplayer_game)
			multiplayer_game.process_move_message = state.Multiplayer.process_move_message.__get__(multiplayer_game)
			multiplayer_game.process_sync_message = state.Multiplayer.process_sync_message.__get__(multiplayer_game)
			multiplayer_game.process_turn_message = state.Multiplayer.process_turn_message.__get__(multiplayer_game)
			multiplayer_game.handle_horse_swap = state.Multiplayer.handle_horse_swap.__get__(multiplayer_game)
			multiplayer_game.handle_game_move = state.Multiplayer.handle_game_move.__get__(multiplayer_game)
			multiplayer_game.handle_pass_turn = state.Multiplayer.handle_pass_turn.__get__(multiplayer_game)
			multiplayer_game.handle_exit = state.Multiplayer.handle_exit.__get__(multiplayer_game)
			multiplayer_game.swap_turn = state.Multiplayer.swap_turn.__get__(multiplayer_game)
			
			print(f"Initialized multiplayer game with connection: {multiplayer_game.connection is not None}")
			print(f"Is host: {multiplayer_game.is_host}")
			print(f"Local player: {multiplayer_game.local_player.color}, Remote player: {multiplayer_game.remote_player.color}")
			
			# Store in initialized states
			if "Multi Player Game" in self.states_unitialized:
				del self.states_unitialized["Multi Player Game"]
			self.states_unitialized["Multi Player Game"] = multiplayer_game

		# change to the newly initialized state
		self.current_state = self.states_unitialized[new_state]
		self.current_state.next_state = None

	# Renderer that will call the render method of the current state
	# INPUT: pygame surface object ()window to display to)
	# OUTPUT: State renders its appropriate atrributes
	def render(self, window):
		if self.current_state:
			self.current_state.render(window)
			