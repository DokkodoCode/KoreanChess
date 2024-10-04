"""
----------------------state_machine.py----------------------------
o This file is the actual state machine that will handle the 
	transitioning between gamestates (Menu,Game, etc...)
o Last Modified - September 24th 2024
----------------------------------------------------------
"""
# specific local file importing of the States
from state import MainMenu, SinglePlayerGame, SinglePlayerPreGameSettings

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
	def __init__(self):
		self.states = {
			"Main Menu" : MainMenu, 
			"Single Player Pre-Game Settings" : SinglePlayerPreGameSettings,
			"Single Player Game" : SinglePlayerGame
		}
		
		self.states_unitialized = {}
		self.current_state = None
		# for debugging reasons, start at gameplay for now
		self.change_state("Main Menu")

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
	def update(self):
		if self.current_state:
			self.current_state.update()
			if self.current_state.next_state:
				self.change_state(self.current_state.next_state)

	# Method that will change what state the program is in
	# INPUT: The new_state to transition to as a string
	# OUTPUT: State of program is changed
	def change_state(self, new_state):
		# state to change to
		#if new_state == "Main Menu":
		if new_state == "Single Player Game":
			self.states_unitialized["Single Player Game"] = SinglePlayerGame()
			#self.states_unitialized["Main Menu"] = MainMenu()
		# initialize a valid starting state if there is none
		elif (new_state not in self.states_unitialized and new_state in self.states):
			self.states_unitialized[new_state] = self.states[new_state]()

		# change to the newly initialized state
		self.current_state = self.states_unitialized[new_state]
		self.current_state.next_state = None

	# Renderer that will call the render method of the current state
	# INPUT: pygame surface object ()window to display to)
	# OUTPUT: State renders its appropriate atrributes
	def render(self, window):
		if self.current_state:
			self.current_state.render(window)