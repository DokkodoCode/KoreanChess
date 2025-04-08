"""
----------------------state_machine.py----------------------------
o This file is the actual state machine that will handle the 
	transitioning between gamestates (Menu,Game, etc...)
o Last Modified - April 5, 2025
----------------------------------------------------------
"""
# libraries
import pygame
import time
import traceback

# specific local file importing of the States
import state
import multiplayer

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

		elif new_state == "Multi Player Game":
			# Initialize the new refactored Multiplayer class
			try:
				# Create a new multiplayer game instance with fresh connection
				if "Multi Player Game" in self.states_unitialized:
					# Try to properly close any existing connection
					try:
						if hasattr(self.states_unitialized["Multi Player Game"], 'connection') and \
						   self.states_unitialized["Multi Player Game"].connection is not None:
							self.states_unitialized["Multi Player Game"].connection.close()
					except:
						traceback.print_exc()
					
					del self.states_unitialized["Multi Player Game"]
				
				# Initialize the new Multiplayer class
				self.states_unitialized["Multi Player Game"] = state.Multiplayer(window)
				
				print(f"Initialized new multiplayer game")

			except Exception as e:
				print(f"Error initializing multiplayer game: {e}")
				traceback.print_exc()
				# Fallback to main menu in case of error
				new_state = "Main Menu"
				self.states_unitialized["Main Menu"] = state.MainMenu(window)

		# change to the newly initialized state
		self.current_state = self.states_unitialized[new_state]
		self.current_state.next_state = None

	# Renderer that will call the render method of the current state
	# INPUT: pygame surface object ()window to display to)
	# OUTPUT: State renders its appropriate atrributes
	def render(self, window):
		if self.current_state:
			self.current_state.render(window)