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
import piece
import multiplayer

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

    # render functions
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
        self.host = player.Player(is_host=True, board_perspective="Bottom")
        # self.player_ai = player.Player(is_host=False, board_perspective="Top")
        self.guest = ai.OpponentAI(is_host=False, board_perspective="Top")

        # host retains last settings, guest is opposite
        if self.host.color == "Cho":
            self.guest.color = "Han"
        else:
            self.guest.color = "Cho"

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
            # OTHERWISE FIND IF ANY OF THE AI LEVELS WERE SET
            else:
                for button in self.ai_level_buttons:
                    if button.is_clicked():
                        self.ai_level = button.text
                        self.host.ai_level = button.text
                        self.guest.ai_level = button.text
                        
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
        text = self.host.ai_level
        x, y = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["single_player"]["button_background"]["ai_level"]["text"]["chosen_diff_location"]
        font_size = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["single_player"]["button_background"]["ai_level"]["text"]["font_size"]
        self.draw_text(window, text, x, y, font_size)

        for button in self.ai_level_buttons:
            button.draw_button(window)
                
        # DISPLAY PREVIEW OF THE PIECES ON HOW THEY WILL LOOK	
        if self.host is not None and self.guest is not None:

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

        self.bikjang_initiater = None  # this is used in line 582 and 670, both times it is checked if it's set to None, but the value is never changed. So this is redundant?

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
    def print_fen(self, optional_message=""):
        string_board = self.guest.convert_board(self.board, self.host)
        fen = self.guest.generate_fen(string_board)
        print(optional_message, fen)

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
class LocalSinglePlayerPreGameSettings(State):


    # initialize the settings for the game
    # INPUT: No Input
    # OUTPUT: Settings menu is ready to be interacted with by player
    def __init__(self, window):
        super().__init__() # inherit the parent initializer
        self.next_state = None
        self.font = pygame.font.SysFont("Arial",size=35)
        # player and opponent will be created here to be inherited
        self.host = player.Player(is_host=True, board_perspective="Bottom")
        self.guest = player.Player(is_host=False, board_perspective="Top")

        # host retains last settings, guest is opposite
        if self.host.color == "Cho":
            self.guest.color = "Han"
        else:
            self.guest.color = "Cho"

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
        self.load_board_boarder(window)
        self.load_board()

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
            elif self.play_button.is_clicked():
                helper_funcs.update_player_settings(self.host)
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
        if self.host is not None:

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
            render_funcs.PreGame_render_piece_display(window, self.host, self.guest)
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
            render_funcs.render_pieces(self.host, self.guest, window)

        # DISPLAY END GAME CONDITIONS/GAME_STATES
        if self.game_over and self.bikjang:
            self.render_bikjang_ending(window)

        if self.game_over and self.check:
            self.render_check_ending(window)

    def swap_turn(self):
        self.active_player, self. waiting_player = self.waiting_player, self.active_player
        # temp_info = self.active_player
        # self.active_player = self.waiting_player
        # self.waiting_player = temp_info


class MultiplayerPreGameSettings(State):
    def __init__(self, window):
        super().__init__()  # inherit the parent initializer
        self.next_state = None
        self.font = pygame.font.SysFont("Arial", size=35)
        self.is_host = None
        self.connection = None
        self.settings_confirmed = False
        
        # Initialize players
        self.host = player.Player(is_host=True, board_perspective="Bottom")
        self.guest = player.Player(is_host=False, board_perspective="Top")

        # Initialize UI elements
        self.__init_buttons()
        self.load_board_boarder(window)
        self.load_board()
        self.__load_backgrounds()
        
        # Establish connection
        self.establish_connection()

    def establish_connection(self):
        """Establish connection as either host or client"""
        if hasattr(self, 'connection') and self.connection is not None:
            print("Already connected, skipping connection establishment")
            return
            
        print("Establishing new connection...")
        choice = input("Do you want to be a host (h) or client (c)? ").lower()
        
        if choice == 'h':
            # Creating a server (host)
            print("Starting as host. Waiting for client to connect...")
            host = "127.0.0.1"  # Using localhost for now
            port = 12345
            
            self.connection = multiplayer.Server(host, port)
            self.connection.create_socket()
            self.connection.bind_socket()
            self.connection.listen()
            
            print("Waiting for client connection...")
            self.connection.accept_client()
            print("Client connected!")
            
            self.is_host = True
            
            # Set socket to non-blocking for better game loop
            if hasattr(self.connection, 'set_client_non_blocking'):
                self.connection.set_client_non_blocking(True)
            
            # Test connection
            self.connection.send("CONNECTED")
            
        elif choice == 'c':
            # Creating a client
            print("Starting as client. Connecting to host...")
            host = "127.0.0.1"  # localhost
            port = 12345
            
            self.connection = multiplayer.Client(host, port)
            if self.connection.connect():
                print("Connected to host!")
                self.is_host = False
                
                # Set socket to non-blocking
                self.connection.set_non_blocking(True)
            else:
                print("Failed to connect to host")
                self.connection = None

    def __init_buttons(self):
        """Initialize all UI buttons"""
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

    def __load_backgrounds(self):
        """Load all UI background elements"""
        # Background loading code (unchanged)
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

    def handle_event(self, event):
        # Ensure connection is established
        if self.connection is None:
            self.establish_connection()
            return
            
        # Client logic - receive settings from host
        if not self.is_host:
            if not self.settings_confirmed:
                try:
                    # Check for settings message from host
                    message = self.connection.receive()
                    if message and message.startswith("SETTINGS:"):
                        # Parse settings from message
                        parts = message.split('|')
                        if len(parts) >= 3:
                            _, client_color, piece_convention = parts
                            print(f"Received settings from host: {client_color}, {piece_convention}")
                            
                            # Client takes the color assigned by host
                            self.guest.color = client_color
                            self.host.color = "Cho" if client_color == "Han" else "Han"
                            
                            # Both use the same piece convention
                            self.guest.piece_convention = piece_convention
                            self.host.piece_convention = piece_convention
                            
                            # Settings confirmed
                            self.settings_confirmed = True
                            self.connection.send("SETTINGS_RECEIVED")
                            
                            # Go directly to game screen
                            self.next_state = "Multi Player Game"
                            print("Client: Going to game screen")
                            return
                except Exception as e:
                    print(f"Error receiving settings: {e}")
                    
            # Client only observes settings, doesn't change them
            return
        
        # Host logic - select settings and send to client
        if self.is_left_click(event):
            # Only host can change settings
            if self.cho_side_button.is_clicked():
                self.host.color = "Cho"
                self.guest.color = "Han"
            elif self.han_side_button.is_clicked():
                self.host.color = "Han"
                self.guest.color = "Cho"
            elif self.standard_piece_convention_button.is_clicked():
                self.host.piece_convention = "Standard"
                self.guest.piece_convention = "Standard"
            elif self.internat_piece_convention_button.is_clicked():
                self.host.piece_convention = "International"
                self.guest.piece_convention = "International"
            elif self.play_button.is_clicked():
                # Send settings to client
                try:
                    # Client will use the opposite color of host
                    client_color = "Han" if self.host.color == "Cho" else "Cho"
                    
                    # Send settings message
                    settings_message = f"SETTINGS:|{client_color}|{self.host.piece_convention}"
                    print(f"Sending settings to client: {settings_message}")
                    self.connection.send(settings_message)
                    
                    # Don't wait for acknowledgment - proceed to game
                    print("Host proceeding to game without waiting for client acknowledgment")
                    helper_funcs.update_player_settings(self.host)
                    self.settings_confirmed = True
                    self.next_state = "Multi Player Game"
                    
                except Exception as e:
                    print(f"Error sending settings: {e}")
                        
        # Escape to main menu
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            # Close connection before returning to main menu
            if self.connection:
                try:
                    self.connection.send("EXIT")
                    self.connection.close()
                except:
                    pass
            self.next_state = "Main Menu"
                
    def render(self, window):
        # USE BOARD AS BACKGROUND
        window.blit(self.menu_background, self.menu_background.get_rect(center = window.get_rect().center))
        window.blit(self.playboard, self.playboard.get_rect(center = window.get_rect().center))
        
        # Show connection status
        status_x = constants.screen_width - 200
        status_y = 30
        if self.connection is None:
            self.draw_text(window, "Not Connected", status_x, status_y, 20)
        else:
            status = "Host" if self.is_host else "Client"
            self.draw_text(window, f"Connected as {status}", status_x, status_y, 20)
        
        # For client, show waiting message
        if not self.is_host:
            self.draw_text(window, "Waiting for host to select settings...", 
                          constants.screen_width//2 - 200, constants.screen_height//2, 30)
            return
            
        # For host, show settings UI
        # SELECT PIECE SIDE TO PLAY AS (CHO/HAN)
        window.blit(self.play_as_background, 
               constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["local_MP"]["button_background"]["play_as"]["location"])
        text = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["local_MP"]["button_background"]["play_as"]["text"]["string"]
        x, y = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["local_MP"]["button_background"]["play_as"]["text"]["location"]
        font_size = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["local_MP"]["button_background"]["play_as"]["text"]["font_size"]

        self.draw_text(window, text, x, y, font_size)
        self.cho_side_button.draw_button(window)
        self.han_side_button.draw_button(window)
        
        # Show selected color
        selected_color = "Cho" if self.host.color == "Cho" else "Han"
        self.draw_text(window, f"Selected: {selected_color}", x, y + 40, font_size - 10)
        
        # SELECT PIECE TYPE CONVENTION TO PLAY WITH (STANDARD/INTERNATIONAL)
        window.blit(self.piece_convention_background, 
               constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["local_MP"]["button_background"]["piece_convention"]["location"])
        text = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["local_MP"]["button_background"]["piece_convention"]["text"]["string"]
        x, y = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["local_MP"]["button_background"]["piece_convention"]["text"]["location"]
        font_size = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["local_MP"]["button_background"]["piece_convention"]["text"]["font_size"]

        self.draw_text(window, text, x, y, font_size)
        self.standard_piece_convention_button.draw_button(window)
        self.internat_piece_convention_button.draw_button(window)
        
        # Show selected convention
        self.draw_text(window, f"Selected: {self.host.piece_convention}", x, y + 40, font_size - 10)

        # PLAY BUTTON
        window.blit(self.play_button_background, 
               constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["local_MP"]["button_background"]["play"]["location"])
        self.play_button.draw_button(window)

        # DISPLAY PREVIEW OF THE PIECES
        if self.host is not None:
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
            render_funcs.PreGame_render_piece_display(window, self.host, self.guest)

class Multiplayer(MultiplayerPreGameSettings):
    def __init__(self, window):
        super().__init__(window)
        
        # Skip connection establishment if already initialized externally
        if not hasattr(self, 'connection') or self.connection is None:
            print("No connection found, establishing new connection...")
            self.establish_connection()
        else:
            print(f"Using existing connection as {'host' if self.is_host else 'client'}")

        # Initialize game board and state
        self.load_board_boarder(window)
        self.load_board()
        self.board = board.Board()
        self.condition = "None"
        self.bikjang = False
        self.check = False
        self.game_over = False
        self.immediate_render = False
        self.last_move_time = 0
        self.sync_cooldown = 100  # milliseconds between syncs
        self.post_swap_grace = False  # Prevents bikjang right after swap phase
        
        # Debug info
        print(f"Multiplayer game state initialized with connection: {self.connection is not None}")
        print(f"Is host: {self.is_host}, Settings confirmed: {hasattr(self, 'settings_confirmed') and self.settings_confirmed}")
        
        # Make sure each player has the correct board perspective
        # Host always sees their own pieces at the bottom
        # Client always sees their own pieces at the bottom
        if self.is_host:
            # Host perspective setup
            self.host.board_perspective = "Bottom"  # Host sees their pieces at bottom
            self.guest.board_perspective = "Top"    # Host sees opponent at top
            self.local_player = self.host           # Host's local player is host
            self.remote_player = self.guest         # Host's remote player is guest
            print("Host perspective: own pieces (Bottom), opponent pieces (Top)")
        else:
            # Client perspective setup
            self.host.board_perspective = "Top"     # Client sees host at top
            self.guest.board_perspective = "Bottom" # Client sees their pieces at bottom
            self.local_player = self.guest          # Client's local player is guest
            self.remote_player = self.host          # Client's remote player is host
            print("Client perspective: own pieces (Bottom), opponent pieces (Top)")
        
        # Initialize player pieces with correct perspectives
        self.initialize_pieces()
        
        # Initialize Cho/Han player references
        self.han_player = self.host if self.host.color == "Han" else self.guest
        self.cho_player = self.guest if self.guest.color == "Cho" else self.host
        
        # Initialize game state based on role (host/client)
        if self.is_host:
            # Host starts with horse swap phase
            self.opening_turn = True
            self.waiting_for_opponent_swap = False
            self.active_player = self.host           # Host's turn first
            self.waiting_player = self.guest
        else:
            # Client waits for host to complete horse swap
            self.opening_turn = True 
            self.waiting_for_opponent_swap = True
            self.active_player = self.guest          # Will be client's turn after host swaps
            self.waiting_player = self.host
        
        # Initialize swap UI
        self.init_swap_menu()

    def initialize_pieces(self):
        """Initialize pieces for both players with correct perspectives"""
        # Import Piece class for creating new pieces
        from piece import Piece
        
        # Clear existing pieces
        self.host.pieces = []
        self.guest.pieces = []
        
        # Create new pieces with the proper perspective
        self.host.pieces = self.host.fill_pieces()
        self.guest.pieces = self.guest.fill_pieces()
        
        # Create backup copies of pieces for validation or reset
        self.host_pieces_backup = []
        self.guest_pieces_backup = []
        
        for piece in self.host.pieces:
            # Deep copy piece attributes
            new_piece = Piece(piece.piece_type, piece.location, piece.image_location, 
                            pygame.Rect(piece.collision_rect), piece.point_value)
            self.host_pieces_backup.append(new_piece)
            
        for piece in self.guest.pieces:
            # Deep copy piece attributes
            new_piece = Piece(piece.piece_type, piece.location, piece.image_location, 
                            pygame.Rect(piece.collision_rect), piece.point_value)
            self.guest_pieces_backup.append(new_piece)
        
        # Debug output
        print(f"Initialized pieces - Host ({self.host.color}): {len(self.host.pieces)}, Guest ({self.guest.color}): {len(self.guest.pieces)}")
        print(f"Host perspective: {self.host.board_perspective}, Guest perspective: {self.guest.board_perspective}")
        print(f"Local player: {self.local_player.color}, Remote player: {self.remote_player.color}")

    def validate_pieces(self):
        """Ensure all pieces are present - restore from backup if needed"""
        from piece import Piece
        
        valid = True
        
        if len(self.host.pieces) < 16:  # Should have 16 pieces
            print(f"WARNING: Host pieces reduced to {len(self.host.pieces)}, restoring from backup")
            self.host.pieces = []
            for piece in self.host_pieces_backup:
                # Deep copy from backup
                new_piece = Piece(piece.piece_type, piece.location, piece.image_location, 
                                pygame.Rect(piece.collision_rect), piece.point_value)
                self.host.pieces.append(new_piece)
            valid = False
            
        if len(self.guest.pieces) < 16:  # Should have 16 pieces
            print(f"WARNING: Guest pieces reduced to {len(self.guest.pieces)}, restoring from backup")
            self.guest.pieces = []
            for piece in self.guest_pieces_backup:
                # Deep copy from backup
                new_piece = Piece(piece.piece_type, piece.location, piece.image_location, 
                                pygame.Rect(piece.collision_rect), piece.point_value)
                self.guest.pieces.append(new_piece)
            valid = False
            
        if not valid:
            # Reset game state after restoration
            self.bikjang = False
            self.check = False
            self.condition = "None"
            self.game_over = False
            
        return valid

    def handle_event(self, event):
        self.immediate_render = False
        
        # Get the player's mouse position for click tracking
        mouse_pos = pygame.mouse.get_pos()
        
        # Check for incoming messages
        self.check_for_messages()
        
        # Check for game over
        if self.is_game_over():
            self.game_over = True
            self.winner = self.waiting_player
            return

        # Process player mouse clicks
        if self.is_left_click(event) and not self.game_over:
            # Only process clicks if it's our turn or our swap phase
            if (self.is_our_turn() or 
                (self.opening_turn and not self.waiting_for_opponent_swap)):
                
                # OPENING TURN - Horse swap phase
                if self.opening_turn and not self.waiting_for_opponent_swap:
                    print(f"Horse swap phase, processing click at {mouse_pos}")
                    self.handle_horse_swap(mouse_pos)
                
                # GAMEPLAY TURN - Regular move phase
                elif not self.opening_turn and not self.waiting_for_opponent_swap:
                    self.handle_game_move(mouse_pos)

        # Right-click to pass turn
        elif (self.is_right_click(event) and 
              self.is_our_turn() and 
              not self.bikjang and not self.check and not self.game_over and
              not self.opening_turn and not self.waiting_for_opponent_swap):
            
            self.handle_pass_turn(mouse_pos)

        # Escape to main menu
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.handle_exit()

    def is_our_turn(self):
        """Check if it's the local player's turn"""
        return self.active_player == self.local_player
            
    def check_for_messages(self):
        """Check for incoming network messages and process them"""
        if self.connection is None:
            return
            
        try:
            message = self.connection.receive()
            if message:
                print(f"Received message: {message}")
                
                if message == "PASS":
                    # Opponent passed their turn
                    print("Opponent passed their turn")
                    self.swap_turn()
                    
                elif message == "EXIT":
                    # Opponent has left the game
                    print("Opponent has left the game")
                    self.next_state = "Main Menu"
                    
                elif message.startswith("SWAP:"):
                    # Process horse swap from opponent
                    self.process_swap_message(message)
                    
                elif message.startswith("MOVE:"):
                    # Process move from opponent
                    self.process_move_message(message)
                    
                elif message.startswith("SYNC:"):
                    # Process full board sync from opponent
                    self.process_sync_message(message)
                    
                elif message.startswith("TURN:"):
                    # Process turn information
                    self.process_turn_message(message)
                    
        except Exception as e:
            print(f"Error processing message: {e}")
            import traceback
            traceback.print_exc()
            
    def handle_horse_swap(self, mouse_pos):
        """Handle horse swap clicks during the opening phase"""
        # Find the pieces that will be swapped
        left_elephant = None
        left_horse = None
        right_elephant = None
        right_horse = None
        
        # Get pieces based on type and relative position
        for piece in self.local_player.pieces:
            if piece.piece_type.value == "Elephant":
                if not left_elephant or piece.location[0] < left_elephant.location[0]:
                    right_elephant, left_elephant = left_elephant, piece
                else:
                    right_elephant = piece
            elif piece.piece_type.value == "Horse":
                if not left_horse or piece.location[0] < left_horse.location[0]:
                    right_horse, left_horse = left_horse, piece
                else:
                    right_horse = piece
        
        # Process swap button clicks
        if self.swap_left_horse_button.is_clicked() and left_horse and left_elephant:
            helper_funcs.swap_pieces(self.local_player, left_horse, left_elephant)
            print(f"Player swapped left horse and elephant")
            
            # Send swap information to opponent
            try:
                import json
                swap_data = {
                    'side': 'left',
                    'piece1': {'type': left_horse.piece_type.value},
                    'piece2': {'type': left_elephant.piece_type.value}
                }
                swap_msg = f"SWAP:|{json.dumps(swap_data)}"
                self.connection.send(swap_msg)
                print(f"Sent swap message: {swap_msg}")
            except Exception as e:
                print(f"Error sending swap message: {e}")
                
        elif self.swap_right_horse_button.is_clicked() and right_horse and right_elephant:
            helper_funcs.swap_pieces(self.local_player, right_horse, right_elephant)
            print(f"Player swapped right horse and elephant")
            
            # Send swap information to opponent
            try:
                import json
                swap_data = {
                    'side': 'right',
                    'piece1': {'type': right_horse.piece_type.value},
                    'piece2': {'type': right_elephant.piece_type.value}
                }
                swap_msg = f"SWAP:|{json.dumps(swap_data)}"
                self.connection.send(swap_msg)
                print(f"Sent swap message: {swap_msg}")
            except Exception as e:
                print(f"Error sending swap message: {e}")
                
        elif self.confirm_swap_button.is_clicked():
            try:
                # Send appropriate message based on role
                if self.is_host:
                    self.connection.send("SWAP:HOST_DONE")
                    print("Host sent swap completion notification")
                else:
                    self.connection.send("SWAP:CLIENT_DONE")
                    print("Client sent swap completion notification")
                
                # After a brief delay, send the sync message
                import time
                time.sleep(0.1)
                
                # Create and send board sync
                from multiplayer import serialize_board_sync
                sync_message = serialize_board_sync(self.host.pieces, self.guest.pieces)
                self.connection.send(sync_message)
                print(f"Sent board sync after swap")
                
                # Update game state based on role
                if self.is_host:
                    self.waiting_for_opponent_swap = True
                    print("Host completed swap, waiting for client")
                else:
                    self.opening_turn = False
                    self.waiting_for_opponent_swap = False
                    
                    # Game starts with Cho player, explicitly disable condition checking
                    self.bikjang = False  # Force to false to prevent immediate bikjang
                    self.check = False    # Also ensure check is false
                    self.condition = "None"  # Reset condition
                    self.post_swap_grace = True  # Set grace period
                    self.game_over = False
                    
                    # Validate pieces before gameplay begins
                    self.validate_pieces()
                    
                    self.active_player = self.cho_player
                    self.waiting_player = self.han_player
                    print(f"Game starting with {self.cho_player.color} player")
                    
            except Exception as e:
                print(f"Error sending swap completion: {e}")
                import traceback
                traceback.print_exc()

    def handle_game_move(self, mouse_pos):
        """Handle game moves during the regular play phase"""
        # Get the player whose pieces we're manipulating
        local_player = self.local_player
        remote_player = self.remote_player
        
        # If player has a piece selected and is attempting to move
        if local_player.is_clicked:
            # Track the piece's original position
            clicked_piece = None
            from_pos = None
            
            for piece in local_player.pieces:
                if piece.is_clicked:
                    clicked_piece = piece
                    from_pos = piece.location
                    break
                    
            if clicked_piece and helper_funcs.attempt_move(local_player, remote_player, self.board, mouse_pos, self.condition):
                # Successful move made
                to_pos = clicked_piece.location
                print(f"Move successful: {clicked_piece.piece_type.value} from {from_pos} to {to_pos}")
                
                # Send move to opponent
                try:
                    import json
                    # Create move data
                    move_data = {
                        'piece_type': clicked_piece.piece_type.value,
                        'from_pos': from_pos,
                        'to_pos': to_pos
                    }
                    
                    # Send move message
                    move_msg = f"MOVE:|{json.dumps(move_data)}"
                    self.connection.send(move_msg)
                    print(f"Sent move message: {move_msg}")
                    
                    # Also send a board sync
                    import time
                    time.sleep(0.1)
                    from multiplayer import serialize_board_sync
                    sync_message = serialize_board_sync(self.host.pieces, self.guest.pieces)
                    self.connection.send(sync_message)
                    print(f"Sent board sync after move")
                    
                    # Send turn information
                    turn_data = {
                        'active_player': self.waiting_player.color,
                        'condition': self.condition
                    }
                    turn_msg = f"TURN:|{json.dumps(turn_data)}"
                    self.connection.send(turn_msg)
                    
                except Exception as e:
                    print(f"Error sending move: {e}")
                    import traceback
                    traceback.print_exc()
                
                # Reset clicked piece state
                helper_funcs.player_piece_unclick(local_player)
                
                # Only check for game conditions if we're past the post-swap grace period
                if not self.post_swap_grace:
                    # Check for special game conditions
                    if helper_funcs.detect_bikjang(local_player, remote_player):
                        self.bikjang = True
                        self.condition = "Bikjang"
                        self.winner = local_player
                        self.game_over = True
                    elif helper_funcs.detect_check(remote_player, local_player, self.board):
                        self.check = True
                        self.condition = "Check"
                        remote_player.is_checked = True
                else:
                    # We've made our first move after swaps, disable grace period
                    self.post_swap_grace = False
                
                # Swap turns
                self.swap_turn()
                self.immediate_render = True
                
        # Check if player clicked on one of their pieces
        elif helper_funcs.player_piece_clicked(local_player, mouse_pos):
            # This just sets the clicked state for the piece
            pass

    def handle_pass_turn(self, mouse_pos):
        """Handle passing the turn with a right-click on the king"""
        local_player = self.local_player
        
        if local_player is not None:
            helper_funcs.player_piece_unclick(local_player)
            # KING piece is always the first piece in the list
            if local_player.pieces[0].collision_rect.collidepoint(mouse_pos):
                # Send pass turn message
                self.connection.send("PASS")
                print("Sent pass turn message")
                
                # Swap turns
                self.swap_turn()
                self.immediate_render = True

    def handle_exit(self):
        """Handle exiting the game"""
        # Close the connection before exiting
        if self.connection:
            try:
                self.connection.send("EXIT")
                self.connection.close()
            except:
                pass
        self.next_state = "Main Menu"

    def process_swap_message(self, message):
        """Process horse swap message from opponent"""
        try:
            print(f"Processing swap message: {message}")
            
            if message == "SWAP:HOST_DONE":
                if not self.is_host:  # Client received host's swap completion
                    print("Host completed their swap, client's turn now")
                    self.waiting_for_opponent_swap = False
                    
            elif message == "SWAP:CLIENT_DONE":
                if self.is_host:  # Host received client's swap completion
                    print("Client completed their swap, game starting")
                    self.opening_turn = False
                    self.waiting_for_opponent_swap = False
                    
                    # EXPLICITLY VALIDATE ALL PIECES ARE PRESENT
                    self.validate_pieces()
                    
                    # Ensure clean state
                    self.bikjang = False
                    self.check = False
                    self.condition = "None"
                    self.game_over = False
                    self.post_swap_grace = True  # Set grace period
                    
                    # Game starts with Cho player
                    self.active_player = self.cho_player
                    self.waiting_player = self.han_player
                    print(f"Starting game with {self.cho_player.color} player")
                    
            elif message.startswith("SWAP:|"):
                # Parse the swap data
                import json
                swap_data = json.loads(message.split('|', 1)[1])
                side = swap_data['side']
                
                # Find the pieces to swap in the remote player's pieces
                left_elephant = None
                left_horse = None
                right_elephant = None
                right_horse = None
                
                for piece in self.remote_player.pieces:
                    if piece.piece_type.value == "Elephant":
                        if not left_elephant or piece.location[0] < left_elephant.location[0]:
                            right_elephant, left_elephant = left_elephant, piece
                        else:
                            right_elephant = piece
                    elif piece.piece_type.value == "Horse":
                        if not left_horse or piece.location[0] < left_horse.location[0]:
                            right_horse, left_horse = left_horse, piece
                        else:
                            right_horse = piece
                
                # Perform the swap based on side
                if side == "left" and left_horse and left_elephant:
                    helper_funcs.swap_pieces(self.remote_player, left_horse, left_elephant)
                    print(f"Swapped opponent's left horse and elephant")
                elif side == "right" and right_horse and right_elephant:
                    helper_funcs.swap_pieces(self.remote_player, right_horse, right_elephant)
                    print(f"Swapped opponent's right horse and elephant")

                # Update backups after swap
                self.host_pieces_backup = []
                self.guest_pieces_backup = []
                
                for piece in self.host.pieces:
                    # Deep copy piece attributes
                    new_piece = piece(piece.piece_type, piece.location, piece.image_location, 
                                     pygame.Rect(piece.collision_rect), piece.point_value)
                    self.host_pieces_backup.append(new_piece)
                    
                for piece in self.guest.pieces:
                    # Deep copy piece attributes
                    new_piece = piece(piece.piece_type, piece.location, piece.image_location, 
                                     pygame.Rect(piece.collision_rect), piece.point_value)
                    self.guest_pieces_backup.append(new_piece)

        except Exception as e:
            print(f"Error processing horse swap: {e}")
            import traceback
            traceback.print_exc()

    def process_move_message(self, message):
        """Process move message from opponent"""
        try:
            if message.startswith("MOVE:|"):
                # Parse the move data
                import json
                move_data = json.loads(message.split('|', 1)[1])
                
                piece_type = move_data['piece_type']
                from_pos = tuple(move_data['from_pos'])
                to_pos = tuple(move_data['to_pos'])
                
                # Find the moved piece in remote player's pieces
                moved_piece = None
                for piece in self.remote_player.pieces:
                    if piece.piece_type.value == piece_type and piece.location == from_pos:
                        moved_piece = piece
                        break
                
                if not moved_piece:
                    # Try finding by piece type only (in case coordinates are different due to perspective)
                    candidates = [p for p in self.remote_player.pieces if p.piece_type.value == piece_type]
                    if candidates:
                        moved_piece = candidates[0]
                
                if moved_piece:
                    # Update piece position
                    moved_piece.location = to_pos
                    moved_piece.image_location = to_pos
                    moved_piece.collision_rect.topleft = to_pos
                    
                    # Check for captures
                    for piece in list(self.local_player.pieces):  # Create a copy to safely modify during iteration
                        if piece.location == to_pos:
                            self.local_player.pieces.remove(piece)
                            print(f"Piece captured: {piece.piece_type.value}")
                            break
                    
                    # Only check for game conditions if we're past the post-swap grace period
                    if not self.post_swap_grace:
                        # Check for special conditions
                        if helper_funcs.detect_bikjang(self.remote_player, self.local_player):
                            self.bikjang = True
                            self.condition = "Bikjang"
                            self.winner = self.remote_player
                            self.game_over = True
                            
                        elif helper_funcs.detect_check(self.local_player, self.remote_player, self.board):
                            self.check = True
                            self.condition = "Check"
                            self.local_player.is_checked = True
                    else:
                        # Opponent made their first move after swaps, disable grace period
                        self.post_swap_grace = False
                    
                    # Swap turns
                    self.swap_turn()
                    self.immediate_render = True
                
        except Exception as e:
            print(f"Error processing move: {e}")
            import traceback
            traceback.print_exc()

    def process_sync_message(self, message):
        """Process full board sync message with correct perspective handling"""
        try:
            if message.startswith("SYNC:"):
                print("Processing sync message")
                
                # Extract the JSON data
                json_str = message[5:]  # Remove "SYNC:" prefix
                
                # Remove leading pipe character if present
                if json_str.startswith('|'):
                    json_str = json_str[1:]
                    
                # Add safety check for empty JSON
                if not json_str or json_str.isspace():
                    print("Warning: Received empty sync data")
                    return
                    
                import json
                try:
                    sync_data = json.loads(json_str)
                except json.JSONDecodeError as e:
                    print(f"JSON decode error: {e}")
                    print(f"Problematic JSON string: '{json_str}'")
                    return
                
                print(f"Successfully parsed JSON data")
                
                # DURING THE OPENING TURN, BOTH HOST AND CLIENT IGNORE POSITION UPDATES
                # This preserves their correct initial perspectives
                if self.opening_turn or self.waiting_for_opponent_swap:
                    print(f"During opening phase: ignoring piece position updates to preserve perspective")
                    
                    # Only update game state flags, not piece positions
                    if self.is_host and self.waiting_for_opponent_swap:
                        # Host receives client's swap completion
                        print("Host: Received client's swap completion via sync")
                        self.opening_turn = False
                        self.waiting_for_opponent_swap = False
                        
                        # Game starts with Cho
                        self.active_player = self.cho_player
                        self.waiting_player = self.han_player
                        
                        # Ensure pieces are valid
                        self.validate_pieces()
                        
                        # Reset conditions to prevent false bikjang
                        self.bikjang = False
                        self.check = False
                        self.condition = "None"
                        self.game_over = False
                        self.post_swap_grace = True
                        
                    elif not self.is_host and self.waiting_for_opponent_swap:
                        # Client receives host's swap completion
                        print("Client: Received host's swap completion via sync")
                        self.waiting_for_opponent_swap = False
                        
                        # Ensure pieces are valid
                        self.validate_pieces()
                else:
                    # DURING REGULAR GAMEPLAY - Apply updates for opponent pieces
                    remote_data = None
                    
                    if self.is_host:
                        # Host updates guest (opponent) pieces
                        if 'guest' in sync_data and sync_data['guest']:
                            remote_data = sync_data['guest']
                    else:
                        # Client updates host (opponent) pieces
                        if 'host' in sync_data and sync_data['host']:
                            remote_data = sync_data['host']
                    
                    if remote_data:
                        from multiplayer import deserialize_piece_positions
                        deserialize_piece_positions(remote_data, self.remote_player.pieces)
                        print(f"Updated remote player pieces based on sync data")
                
                    # Validate that all pieces are still present
                    self.validate_pieces()
                
                # Only check for special conditions after post_swap_grace period
                if not self.post_swap_grace:
                    # Check if we can detect special conditions
                    if helper_funcs.detect_bikjang(self.remote_player, self.local_player):
                        self.bikjang = True
                        self.condition = "Bikjang"
                        self.winner = self.remote_player
                        self.game_over = True
                        
                    elif helper_funcs.detect_check(self.local_player, self.remote_player, self.board):
                        self.check = True
                        self.condition = "Check"
                        self.local_player.is_checked = True
                    
                self.immediate_render = True
                
        except Exception as e:
            print(f"Error processing sync message: {e}")
            import traceback
            traceback.print_exc()

    def process_turn_message(self, message):
        """Process turn information from opponent"""
        try:
            if message.startswith("TURN:|"):
                import json
                turn_data = json.loads(message.split('|', 1)[1])
                
                active_player_color = turn_data['active_player']
                condition = turn_data.get('condition', "None")
                
                # Update whose turn it is
                if active_player_color == self.local_player.color:
                    self.active_player = self.local_player
                    self.waiting_player = self.remote_player
                else:
                    self.active_player = self.remote_player
                    self.waiting_player = self.local_player
                
                # Update game condition
                self.condition = condition
                if condition == "Bikjang":
                    self.bikjang = True
                elif condition == "Check":
                    self.check = True
                    
                print(f"Updated turn info - Active player: {active_player_color}, Condition: {condition}")
                self.immediate_render = True
                
        except Exception as e:
            print(f"Error processing turn message: {e}")
            import traceback
            traceback.print_exc()

    def init_swap_menu(self):
            """Initialize the horse swap menu buttons and backgrounds"""
            # Create swap buttons for horse pieces
            x, y = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["single_player"]["swap_left_horse_button"]["location"]
            width, height = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["single_player"]["swap_left_horse_button"]["size"]
            font = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["single_player"]["swap_left_horse_button"]["text"]["font"]
            text = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["single_player"]["swap_left_horse_button"]["text"]["string"]
            fg_color = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["single_player"]["swap_left_horse_button"]["text"]["foreground_color"]
            bg_color = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["single_player"]["swap_left_horse_button"]["text"]["background_color"]
            hover_color = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["single_player"]["swap_left_horse_button"]["text"]["hover_color"]
            self.swap_left_horse_button = button.Button(x, y, width, height, font, text, fg_color, bg_color, hover_color)

            # Right horse swap button
            x, y = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["single_player"]["swap_right_horse_button"]["location"]
            width, height = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["single_player"]["swap_right_horse_button"]["size"]
            font = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["single_player"]["swap_right_horse_button"]["text"]["font"]
            text = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["single_player"]["swap_right_horse_button"]["text"]["string"]
            fg_color = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["single_player"]["swap_right_horse_button"]["text"]["foreground_color"]
            bg_color = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["single_player"]["swap_right_horse_button"]["text"]["background_color"]
            hover_color = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["single_player"]["swap_right_horse_button"]["text"]["hover_color"]
            self.swap_right_horse_button = button.Button(x, y, width, height, font, text, fg_color, bg_color, hover_color)

            # Confirm button
            x, y = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["single_player"]["confirm_swap_button"]["location"]
            width, height = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["single_player"]["confirm_swap_button"]["size"]
            font = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["single_player"]["confirm_swap_button"]["text"]["font"]
            text = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["single_player"]["confirm_swap_button"]["text"]["string"]
            fg_color = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["single_player"]["confirm_swap_button"]["text"]["foreground_color"]
            bg_color = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["single_player"]["confirm_swap_button"]["text"]["background_color"]
            hover_color = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["buttons"]["single_player"]["confirm_swap_button"]["text"]["hover_color"]
            self.confirm_swap_button = button.Button(x, y, width, height, font, text, fg_color, bg_color, hover_color)

            # Load button backgrounds
            self.swap_left_horse_background = pygame.image.load("UI/Button_Background.png").convert_alpha()
            self.swap_left_horse_background = pygame.transform.rotate(self.swap_left_horse_background, 180)
            self.swap_left_horse_background = pygame.transform.scale(self.swap_left_horse_background,
                    constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["single_player"]["button_background"]["swap_left_horse"]["size"])

            self.swap_right_horse_background = pygame.image.load("UI/Button_Background.png").convert_alpha()
            self.swap_right_horse_background = pygame.transform.rotate(self.swap_right_horse_background, 180)
            self.swap_right_horse_background = pygame.transform.scale(self.swap_right_horse_background,
                    constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["single_player"]["button_background"]["swap_right_horse"]["size"])

            self.confirm_swap_button_background = pygame.image.load("UI/Button_Background_Poly.png").convert_alpha()
            self.confirm_swap_button_background = pygame.transform.scale(self.confirm_swap_button_background,
                    constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["single_player"]["button_background"]["confirm_swap"]["size"])
            
            # Game state backgrounds
            self.game_state_background = pygame.image.load("UI/Button_Background.png").convert_alpha()
            self.game_state_background = pygame.transform.scale(self.game_state_background,
                    constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["single_player"]["button_background"]["game_state"]["size"])
            
            self.game_over_background = pygame.image.load("UI/Button_Background.png").convert_alpha()
            self.game_over_background = pygame.transform.scale(self.game_over_background,
                    constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["single_player"]["button_background"]["game_over"]["size"])

    def render_swap_menu(self, window):
        """Render the horse swap UI"""
        # Render swap buttons at the bottom of the screen
        window.blit(self.swap_left_horse_background, 
            constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["single_player"]["button_background"]["swap_left_horse"]["location"])
        self.swap_left_horse_button.draw_button(window)

        window.blit(self.swap_right_horse_background,
            constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["single_player"]["button_background"]["swap_right_horse"]["location"])
        self.swap_right_horse_button.draw_button(window)

        # Display confirm button
        window.blit(self.confirm_swap_button_background,
            constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["single_player"]["button_background"]["confirm_swap"]["location"])
        self.confirm_swap_button.draw_button(window)

    def render(self, window):
        # EMERGENCY CHECK - validate pieces at start of frame
        if not self.opening_turn and (len(self.host.pieces) < 16 or len(self.guest.pieces) < 16):
            print("EMERGENCY: Missing pieces detected, restoring from backups")
            self.validate_pieces()
            self.bikjang = False  # Force reset Bikjang
            self.check = False
            self.condition = "None"
            self.game_over = False
        
        # Display board
        window.blit(self.menu_background, self.menu_background.get_rect(center=window.get_rect().center))
        window.blit(self.playboard, self.playboard.get_rect(center=window.get_rect().center))

        # Display connection status
        status_x = constants.screen_width - 200
        status_y = 30
        status = "Host" if self.is_host else "Client"
        your_color = self.local_player.color
        self.draw_text(window, f"Connected as {status} ({your_color})", status_x, status_y, 20)
        
        # Display game phase
        phase_text = ""
        if self.opening_turn:
            if self.waiting_for_opponent_swap:
                phase_text = "Waiting for opponent's horse swap"
            else:
                phase_text = "Your horse swap turn"
        else:
            if self.active_player == self.local_player:
                phase_text = "YOUR TURN"
            else:
                phase_text = "Opponent's turn"
        
        self.draw_text(window, phase_text, status_x, status_y + 25, 20)
        
        # Display colors and turn information
        self.draw_text(window, f"Host: {self.host.color}", status_x, status_y + 50, 20)
        self.draw_text(window, f"Guest: {self.guest.color}", status_x, status_y + 75, 20)
        self.draw_text(window, f"You: {self.local_player.color}", status_x, status_y + 100, 20)
        self.draw_text(window, f"Turn: {self.active_player.color}", status_x, status_y + 125, 20)
        
        # Display condition if any
        if self.condition != "None":
            self.draw_text(window, f"Condition: {self.condition}", status_x, status_y + 150, 20)

        # Render horse swap UI if in that phase
        if self.opening_turn and not self.waiting_for_opponent_swap:
            self.render_swap_menu(window)
        elif self.waiting_for_opponent_swap:
            message_x = constants.screen_width // 2 - 200
            message_y = constants.screen_height // 2
            self.draw_text(window, "Waiting for opponent to finish swaps...", message_x, message_y, 30)

        # Show valid moves for clicked piece
        if self.active_player == self.local_player and self.local_player.is_clicked:
            render_funcs.render_possible_spots(self.local_player, self.remote_player, self.board, window, self.condition)

        # Highlight special conditions (bikjang/check)
        if self.bikjang:
            render_funcs.render_bikjang_highlight(self.active_player, self.waiting_player, window)
        if self.check:
            if self.guest.is_checked:
                render_funcs.render_check_highlight(self.guest, window)
            else:
                render_funcs.render_check_highlight(self.host, window)

        # Render pieces - always render local player at bottom, remote at top
        render_funcs.render_pieces(self.local_player, self.remote_player, window)

        # ONLY show game over if it's a confirmed game over AND we have all pieces (prevents false game overs)
        if self.game_over and self.bikjang and self.condition == "Bikjang" and len(self.host.pieces) >= 16 and len(self.guest.pieces) >= 16:
            self.render_bikjang_ending(window)
        elif self.game_over and self.check and self.condition == "Check" and len(self.host.pieces) >= 16 and len(self.guest.pieces) >= 16:
            self.render_check_ending(window)

    def swap_turn(self):
        """Swap active and waiting players and update turn state"""
        # Update is_turn flags
        self.active_player.is_turn = False
        self.waiting_player.is_turn = True
        
        # Swap active and waiting players
        temp = self.active_player
        self.active_player = self.waiting_player
        self.waiting_player = temp
        
        print(f"Turn swapped. Active player: {self.active_player.color} (Host: {self.active_player == self.host})")
        
        # Send turn update to opponent
        try:
            import json
            turn_data = {
                'active_player': self.active_player.color,
                'condition': self.condition
            }
            turn_msg = f"TURN:|{json.dumps(turn_data)}"
            self.connection.send(turn_msg)
            print(f"Sent turn update: {turn_msg}")
        except Exception as e:
            print(f"Error sending turn update: {e}")