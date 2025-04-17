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
import multiplayer
import json
import time
import traceback
from piece import Position

#--------------------------------------------------------------------------------
# Parent State to act as a base class to be inherited by 
#--------------------------------------------------------------------------------
class State():
    # initializer
    def __init__(self):
        self.next_state = None

        # game state variables
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
        if constants.screen_height == 796:
            self.menu_background = pygame.transform.scale(self.menu_background, (796, 796))
        else:
            self.menu_background = pygame.transform.scale(self.menu_background, (1080, 1080))
        self.center = window.get_rect().center

    #  function that will load board into memory
    def load_board(self):
        self.playboard = pygame.image.load("Board/Janggi_Board.png").convert_alpha()
        if constants.screen_height == 796:
            self.playboard = pygame.transform.scale(self.playboard, (676, 676))
        else:
            self.playboard = pygame.transform.scale(self.playboard, (917, 917))
        self.playboard_center = self.menu_background.get_rect().center

    # Method to draw text information out to the window
    # returns the size of the text surface
    def draw_text(self, window, text, x=0, y=0, font_size=30):
        font = pygame.font.SysFont("Arial", font_size)
        text_surface = font.render(text, True, constants.WHITE)
        window.blit(text_surface, (x, y))
        return text_surface.get_width(), text_surface.get_height()

    def get_text_size(self, window, text, font_size=30):
        font = pygame.font.SysFont("Arial", font_size)
        text_surface = font.render(text, True, constants.WHITE)
        return text_surface.get_width(), text_surface.get_height()


    def render_message(self, window, message:str, pos:tuple[int,int]):
        # window.blit(self.game_over_background, pos[0], pos[1])
        MARGIN = 10
        size = self.get_text_size(window, message, 33)
        size = (size[0]+MARGIN, size[1]+MARGIN)
        rect = pygame.Rect(pos[0]-(size[0]/2), pos[1]-(size[1]/2), size[0], size[1])
        pygame.draw.rect(window, 'black', rect)
        self.draw_text(window, message,
                       pos[0]-(size[0]/2)+MARGIN/2, pos[1]-(size[1]/2)+MARGIN/2, 33)

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

            elif self.multiplayer_button.is_clicked():
                self.next_state = "Multi Player Game"

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
        self.render_player_color_menu(window)
        self.render_piece_convention_menu(window)
        self.render_player_piece_preview(window)
        self.render_play_button(window)

    # LOADING AND RENDERING FUNCTIONS
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
        return font_size, x, y

    def render_piece_convention_menu(self, window):
        window.blit(self.piece_convention_background, 
                constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["local_MP"]["button_background"]["piece_convention"]["location"])
        text = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["local_MP"]["button_background"]["piece_convention"]["text"]["string"]
        x, y = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["local_MP"]["button_background"]["piece_convention"]["text"]["location"]
        font_size = constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["local_MP"]["button_background"]["piece_convention"]["text"]["font_size"]

        self.draw_text(window, text, x, y, font_size)
        self.standard_piece_convention_button.draw_button(window)
        self.internat_piece_convention_button.draw_button(window)
        return font_size, x, y

    def render_play_button(self, window):
        window.blit(self.play_button_background, 
        constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["local_MP"]["button_background"]["play"]["location"])
        self.play_button.draw_button(window)

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
        return font_size, x, y

    def load_host_side_swap_menu(self):
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

    def load_guest_side_swap_menu(self):
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
				# Store AI difficulty in constants
				constants.stored_difficulty = button.text
				self.guest.set_difficulty(button.text.lower())
				
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

        self.ai_level = constants.stored_difficulty
        print("Stored difficulty is " + constants.stored_difficulty)
        self.guest.set_difficulty(constants.stored_difficulty.lower())

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

        self.handle_ai_move()

    # Handle any rendering that needs to be done
    # INPUT: pygame surface object (window to display to)
    # OUTPUT: All game attributes/actions are rendered
    def render(self, window):
        # display board to window
        self.render_board(window)

        # DISPLAY THE OPTION TO SWAP HORSES AT THE START OF THE GAME
        if self.opening_turn:
            window.blit(self.host_swap_left_horse_background, 
                constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["single_player"]["button_background"]["swap_left_horse"]["location"])
            self.host_swap_left_horse_button.draw_button(window)

            window.blit(self.host_swap_right_horse_background,
                constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["single_player"]["button_background"]["swap_right_horse"]["location"])
            self.host_swap_right_horse_button.draw_button(window)

        # if player has a piece currently clicked, render where it can go
        if self.host is not None and self.host.is_clicked:
            render_funcs.render_possible_spots(self.host, self.guest, self.board, window, self.condition)

        # display confirm button for swapping pieces
        if self.opening_turn:
            # confirm swap button
            window.blit(self.host_confirm_swap_button_background,
                constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["single_player"]["button_background"]["confirm_swap"]["location"])
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
            
            print(f"Making move with depth of {depth}")
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
		print("locala sinhle player game called")
		# load then display board image
		self.load_board_boarder(window)
		self.load_board()
		self.load_host_side_swap_menu()
		self.load_guest_side_swap_menu()
		
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
		self.active_player = self.cho_player
		self.waiting_player = self.han_player
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
		self.render_board(window)

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

import socket
HOST, PORT = socket.gethostbyname(socket.gethostname()), 5000

class Multiplayer(PreGameSettings):    
    def __init__(self, window):
        self.guest = player.Player(is_host=False, board_perspective="Top")
        self.host = player.Player(is_host=True, board_perspective="Bottom")
        self.font = pygame.font.SysFont("Arial",size=35)

        super().__init__(window)

        # positions have -50 to adjust for size of button
        self.host_button = button.Button(constants.screen_width * (1/3)-50,
                                         constants.screen_height/2-(75/2),
                                         100, 75,
                                         self.font, 'host')
        self.client_button = button.Button(constants.screen_width * (2/3)-50,
                                           constants.screen_height/2-(75/2),
                                           100, 75,
                                           self.font, 'client')
        self.choice = None # for choosing betwenn host and client

        self.ip_prompt = InputBox((constants.screen_width/2, constants.screen_height/2), (300, 50))
        # vars for handling incorrect IP input
        self.invalid_ip = False
        self.connection_error = False

        self.load_host_side_swap_menu()

        from piece import Position
        self.Position = Position
        
        # Initialize basic state
        self.next_state = None
        self.window = window
        self.connection = None
        self.is_host = None
        self.game_phase = multiplayer.GamePhase.CONNECTING
        
        # Initialize UI elements
        self.font = pygame.font.SysFont("Arial", size=35)
        self.load_board_boarder(window)
        self.load_board()
        self.load_button_background() 
        self.board = board.Board()
        
        # Gameplay state
        self.immediate_render = False
        self.last_sync_time = 0
        self.sync_interval = 0.5  #  seconds between syncs
        self.last_validation_time = 0
        self.validation_interval = 3.0  # seconds between validations
        self.post_swap_grace = False  # Prevents immediate game end after swap phase
        self.waiting_for_opponent_swap = False
                
        # Initialize connection
        # self.establish_connection()
                
        # Setup player perspectives based on role
        self.initialize_perspectives()
        
        from piece import Position
        self.Position = Position
        
        # Create piece backups for validation
        self.backup_pieces()
        
        # Initialize UI elements for horse swap phase
        self.load_game_state_elements()
        
        # Start the game state machine
        # self.transition_to_settings()
        print('switching to create_join_game')
        self.game_phase = multiplayer.GamePhase.CREATE_JOIN_GAME

    def initialize_perspectives(self):
        """Initialize player perspectives based on host/client role"""
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
            
        # Initialize pieces with correct perspectives
        self.host.pieces = self.host.fill_pieces()
        self.guest.pieces = self.guest.fill_pieces()
        
        # Initialize Cho/Han player references
        self.han_player = self.host if self.host.color == "Han" else self.guest
        self.cho_player = self.guest if self.guest.color == "Cho" else self.host
        
        # Set active player based on current game phase
        if self.is_host:
            self.active_player = self.host          # Host moves first in swap phase
            self.waiting_player = self.guest
        else:
            self.active_player = self.guest         # Client moves after host in swap phase
            self.waiting_player = self.host

    def backup_pieces(self):
        """Create backups of all pieces for validation and restoration"""
        from piece import Piece
        
        role_prefix = "HOST: " if self.is_host else "CLIENT: "
        
        # Create backup copies of pieces for validation
        self.host_pieces_backup = []
        self.guest_pieces_backup = []
        
        # Create deep copies of each piece
        for p in self.host.pieces:
            from piece import Piece
            new_piece = Piece(
                p.piece_type, 
                p.location, 
                p.image_location,
                pygame.Rect(p.collision_rect), 
                p.point_value
            )
            # Ensure ID and position are copied correctly
            if hasattr(p, 'id'):
                new_piece.id = p.id
            # Ensure position is set correctly
            new_piece.position = self.Position(p.position.file, p.position.rank)
            new_piece.is_clicked = p.is_clicked
            self.host_pieces_backup.append(new_piece)
            
        for p in self.guest.pieces:
            new_piece = Piece(
                p.piece_type, 
                p.location, 
                p.image_location,
                pygame.Rect(p.collision_rect), 
                p.point_value
            )
            # Ensure ID and position are copied correctly
            if hasattr(p, 'id'):
                new_piece.id = p.id
            # Ensure position is set correctly
            new_piece.position = self.Position(p.position.file, p.position.rank)
            new_piece.is_clicked = p.is_clicked
            self.guest_pieces_backup.append(new_piece)

    def restore_pieces_from_backup(self):
        """Restore pieces from backup if validation fails"""
        from piece import Piece
        
        role_prefix = "HOST: " if self.is_host else "CLIENT: "
        
        # Make sure we have backups to restore from
        if not hasattr(self, 'host_pieces_backup') or not hasattr(self, 'guest_pieces_backup'):
            print(f"{role_prefix}ERROR: No backups available to restore from")
            return
        
        # Count before restoration for reporting
        host_before = len(self.host.pieces)
        guest_before = len(self.guest.pieces)
        
        # Clear existing pieces
        self.host.pieces = []
        self.guest.pieces = []
        
        # Restore from backups
        for p in self.host_pieces_backup:
            new_piece = Piece(
                p.piece_type, 
                p.location, 
                p.image_location, 
                pygame.Rect(p.collision_rect), 
                p.point_value
            )
            # Restore ID and position
            if hasattr(p, 'id'):
                new_piece.id = p.id
            if hasattr(p, 'position'):
                new_piece.position = self.Position(p.position.file, p.position.rank)
            else:
                new_piece.position = self.Position.from_pixel(p.location)
            new_piece.is_clicked = p.is_clicked
            self.host.pieces.append(new_piece)
            
        for p in self.guest_pieces_backup:
            new_piece = Piece(
                p.piece_type, 
                p.location, 
                p.image_location, 
                pygame.Rect(p.collision_rect), 
                p.point_value
            )
            # Restore ID and position
            if hasattr(p, 'id'):
                new_piece.id = p.id
            if hasattr(p, 'position'):
                new_piece.position = self.Position(p.position.file, p.position.rank)
            else:
                new_piece.position = self.Position.from_pixel(p.location)
            new_piece.is_clicked = p.is_clicked
            self.guest.pieces.append(new_piece)
            
        # Make sure all pieces have correct collision rectangles
        self.realign_piece_collisions(self.host)
        self.realign_piece_collisions(self.guest)
        
        # Reset game conditions
        self.bikjang = False
        self.check = False
        self.condition = "None"
        
        # Log restoration results
        host_after = len(self.host.pieces)
        guest_after = len(self.guest.pieces)
        print(f"{role_prefix}Restored from backup: Host {host_before}→{host_after}, Guest {guest_before}→{guest_after}")

    def validate_board_state(self):
        """Validate the current board state to detect errors"""
        role_prefix = "HOST: " if self.is_host else "CLIENT: "
        
        # Basic validation that applies in all phases
        print(f"{role_prefix}Validating board state")
        
        # 1. Check for kings - each side must have exactly one
        host_kings = [p for p in self.host.pieces if p.piece_type.value == "King"]
        guest_kings = [p for p in self.guest.pieces if p.piece_type.value == "King"]
        
        if len(host_kings) != 1 or len(guest_kings) != 1:
            print(f"{role_prefix}ERROR: King count incorrect - Host: {len(host_kings)}, Guest: {len(guest_kings)}")
            self.restore_pieces_from_backup()
            return False
        
        # 2. Check for overlapping pieces (shouldn't happen in any phase)
        all_positions = []
        for piece in self.host.pieces + self.guest.pieces:
            # Use both grid position and pixel location for robustness
            position_key = (piece.position.file, piece.position.rank)
            location_key = piece.location
            
            if position_key in all_positions or location_key in all_positions:
                print(f"{role_prefix}WARNING: Overlapping piece at position {position_key} or location {location_key}")
                self.restore_pieces_from_backup()
                return False
                
            all_positions.append(position_key)
            all_positions.append(location_key)
        
        # 3. Check for pieces outside board boundaries (shouldn't happen in any phase)
        for piece in self.host.pieces + self.guest.pieces:
            if not hasattr(piece, 'position') or not isinstance(piece.position, self.Position):
                print(f"{role_prefix}WARNING: Piece missing valid position: {piece}")
                self.restore_pieces_from_backup()
                return False
                
            file, rank = piece.position.file, piece.position.rank
            if file < 0 or file > 8 or rank < 0 or rank > 9:
                print(f"{role_prefix}WARNING: Piece at invalid grid position {file},{rank}")
                self.restore_pieces_from_backup()
                return False
                
            x, y = piece.location
            if (x not in constants.x_coordinates or 
                y not in constants.y_coordinates):
                print(f"{role_prefix}WARNING: Piece at invalid pixel location {piece.location}")
                self.restore_pieces_from_backup()
                return False
        
        # In setup phases, we also check piece counts
        if self.game_phase != multiplayer.GamePhase.GAMEPLAY:
            if len(self.host.pieces) != 16 or len(self.guest.pieces) != 16:
                print(f"{role_prefix}WARNING: Piece count error - Host: {len(self.host.pieces)}, "
                    f"Guest: {len(self.guest.pieces)}")
                self.restore_pieces_from_backup()
                return False
        # For gameplay, do more lenient checks
        else:
            # 4. During gameplay, check that piece count difference isn't too large
            host_count = len(self.host.pieces)
            guest_count = len(self.guest.pieces)
            if abs(host_count - guest_count) > 5:
                print(f"{role_prefix}WARNING: Piece count extremely imbalanced - Host: {host_count}, Guest: {guest_count}")
                self.restore_pieces_from_backup()
                return False
        
        # All checks passed
        return True

    # -------------------------------------------------------------------------
    # Message Handling
    # -------------------------------------------------------------------------
    
    def send_message(self, msg_type, data=None):
        """Send a standardized message to the opponent"""
        if not self.connection:
            return False
            
        message = {
            "type": msg_type.value,
            "timestamp": time.time()
        }
        
        if data:
            message["data"] = data
        
        return self.connection.send(message)

    def check_for_messages(self):
        """Check for incoming messages and process them"""
        if not self.connection:
            return
            
        try:
            message = self.connection.receive()
            if not message:
                return
                
            try:
                role_prefix = "HOST: " if self.is_host else "CLIENT: "
                
                msg_data = json.loads(message)
                msg_type = msg_data.get("type")
                data = msg_data.get("data", {})
                
                # Process based on message type
                if msg_type == multiplayer.MessageType.CONNECT.value:
                    self.process_connect_message(data)
                elif msg_type == multiplayer.MessageType.SETTINGS.value:
                    self.process_settings_message(data)
                elif msg_type == multiplayer.MessageType.SWAP.value:
                    self.process_swap_message(data)
                elif msg_type == multiplayer.MessageType.SWAP_DONE.value:
                    self.process_swap_done_message(data)
                elif msg_type == multiplayer.MessageType.MOVE.value:
                    self.process_move_message(data)
                elif msg_type == multiplayer.MessageType.SYNC.value:
                    self.process_sync_message(data)
                elif msg_type == multiplayer.MessageType.TURN.value:
                    self.process_turn_message(data)
                elif msg_type == multiplayer.MessageType.PASS.value:
                    self.process_pass_message(data)
                elif msg_type == multiplayer.MessageType.EXIT.value:
                    self.process_exit_message(data)
                else:
                    print(f"{role_prefix}Unknown message type: {msg_type}")
            except json.JSONDecodeError:
                print(f"{role_prefix}Error decoding message: {message}")
            except Exception as e:
                print(f"{role_prefix}Error processing message: {e}")
                traceback.print_exc()
                
        except Exception as e:
            role_prefix = "HOST: " if self.is_host else "CLIENT: "
            print(f"{role_prefix}Error checking for messages: {e}")
            traceback.print_exc()

    def process_connect_message(self, data):
        """Process initial connection message"""
        print(f"Connection established: {data}")
        if not self.is_host:
            # Client receives connect confirmation from host
            self.transition_to_settings()

    def process_settings_message(self, data):
        """Process game settings message"""
        print(f"Received settings: {data}")
        
        if not self.is_host:
            # Client receiving settings from host
            if "host_color" in data and "piece_convention" in data:
                host_color = data["host_color"]
                piece_convention = data["piece_convention"]
                
                # Apply settings
                self.host.color = host_color
                self.host.piece_convention = piece_convention
                
                # Set guest (client) color to opposite of host
                self.guest.color = "Han" if host_color == "Cho" else "Cho"
                self.guest.piece_convention = piece_convention
                
                # Send acknowledgment
                self.send_message(multiplayer.MessageType.SETTINGS, {
                    "status": "received",
                    "guest_color": self.guest.color
                })
                
                # Update player references
                self.han_player = self.host if self.host.color == "Han" else self.guest
                self.cho_player = self.guest if self.guest.color == "Cho" else self.host
                
                # Transition to horse swap phase
                self.transition_to_host_swap()
        else:
            # Host receiving acknowledgment from client
            if data.get("status") == "received":
                print("Client acknowledged settings")
                # Don't transition if already in swap phases
                if (self.game_phase != multiplayer.GamePhase.HOST_HORSE_SWAP and 
                    self.game_phase != multiplayer.GamePhase.CLIENT_HORSE_SWAP):
                    self.transition_to_host_swap()
                else:
                    print("Already in a horse swap phase - skipping redundant transition")

    def process_swap_message(self, data):
        """Process horse swap message"""
        print(f"Received swap: {data}")
        
        side = data.get("side")
        
        # Find the pieces to swap
        if side == "left":
            self.swap_left_pieces_for_remote()
        elif side == "right":
            self.swap_right_pieces_for_remote()
        
        # Realign collision rectangles after swap
        self.realign_piece_collisions(self.remote_player)
        
        # Update piece backups
        self.backup_pieces()

    def process_swap_done_message(self, data):
        """Process swap completion message"""
        role_prefix = "HOST: " if self.is_host else "CLIENT: "
        print(f"{role_prefix}Processing SWAP_DONE message with data: {data}")
        
        client_phase = data.get("phase", "unknown")
        client_done = data.get("client_done", False)
        host_done = data.get("host_done", False)
        sender_color = data.get("player_color", "unknown")
        
        print(f"{role_prefix}Current phase: {self.game_phase.value}, Sender phase: {client_phase}")
        print(f"{role_prefix}Sender color: {sender_color}, Client done: {client_done}, Host done: {host_done}")
        
        # Add delay to ensure local swaps are fully processed
        time.sleep(0.1)  # Small delay to ensure stable state
        
        # CASE 1: CLIENT done with own swap
        if not self.is_host and self.game_phase == multiplayer.GamePhase.CLIENT_HORSE_SWAP:
            print(f"{role_prefix}Client processing its own swap done message")
            # First realign all collision rectangles
            self.realign_piece_collisions(self.host)
            self.realign_piece_collisions(self.guest)
            
            # Create new backups AFTER swaps are completed
            self.backup_pieces()
            
            # Force immediate sync BEFORE transitioning
            self.force_sync()
            
            # Only then transition to gameplay
            self.transition_to_gameplay()
            return
        
        # CASE 2: HOST receiving client's swap done
        elif self.is_host and client_done and client_phase == "client_horse_swap":
            print(f"{role_prefix}Host processing client's swap done message")
            # Realign collision rectangles first
            self.realign_piece_collisions(self.host)
            self.realign_piece_collisions(self.guest)
            
            # Create new backups AFTER all swaps are completed
            self.backup_pieces()
            
            # First force a sync to ensure client has latest state
            self.force_sync()
            
            # Small delay to ensure client processes sync before transitioning
            time.sleep(0.2)
            
            # Now transition to gameplay
            self.transition_to_gameplay()
            return
        
        # CASE 3: HOST done with own swap
        elif self.is_host and self.game_phase == multiplayer.GamePhase.HOST_HORSE_SWAP:
            print(f"{role_prefix}Host completed own swap, transitioning to client swap phase")
            # Realign collision rectangles
            self.realign_piece_collisions(self.host)
            self.realign_piece_collisions(self.guest)
            
            # Force sync before transitioning to ensure client has up-to-date pieces
            self.force_sync()
            
            # Create an intermediate backup after host swap
            self.backup_pieces()
            
            # Transition to client swap
            self.transition_to_client_swap()
            return
        
        # CASE 4: CLIENT receiving host's swap done
        elif not self.is_host and self.game_phase == multiplayer.GamePhase.HOST_HORSE_SWAP:
            print(f"{role_prefix}Client received host swap done, transitioning to client swap")
            # Realign collision rectangles
            self.realign_piece_collisions(self.host)
            self.realign_piece_collisions(self.guest)
            
            # Force a sync to get latest host pieces
            self.force_sync()
            
            # Create an intermediate backup
            self.backup_pieces()
            
            # Now transition to client swap phase
            self.transition_to_client_swap()
            return
        
        # Unexpected cases - log and try to recover
        else:
            print(f"{role_prefix}Unexpected state in process_swap_done - is_host: {self.is_host}, phase: {self.game_phase.value}")
            print(f"{role_prefix}Attempting to recover by forcing sync")
            self.force_sync()
            if self.game_phase == multiplayer.GamePhase.HOST_HORSE_SWAP:
                self.transition_to_client_swap()
            elif self.game_phase == multiplayer.GamePhase.CLIENT_HORSE_SWAP:
                self.transition_to_gameplay()

    def process_move_message(self, data):
        """Process move message from opponent"""
        role_prefix = "HOST: " if self.is_host else "CLIENT: "
        
        # Extract move information
        piece_type = data.get("piece_type")
        piece_id = data.get("piece_id")
        from_pos_data = data.get("from_pos", {})
        to_pos_data = data.get("to_pos", {})
        local_perspective = data.get("local_perspective", False)
        
        # Create Position objects
        from_file = from_pos_data.get('file', 0)
        from_rank = from_pos_data.get('rank', 0)
        to_file = to_pos_data.get('file', 0)
        to_rank = to_pos_data.get('rank', 0)
        
        # Only transform coordinates if receiving as client FROM host
        # If host received from client, coordinates are already canonical
        # If client received from host, need to transform from canonical to client view
        if self.is_host:
            # Don't transform - coordinates from client are already canonical
            pass
        else:
            # Transform from canonical to client perspective
            from_file = 8 - from_file  # Flip horizontally
            from_rank = 9 - from_rank  # Flip vertically
            to_file = 8 - to_file
            to_rank = 9 - to_rank
        
        # Find the piece to move
        found_piece = None
        
        # Try to find by ID first
        if piece_id:
            for p in self.remote_player.pieces:
                if hasattr(p, 'id') and p.id == piece_id:
                    found_piece = p
                    break
        
        # If not found by ID, try by position and type
        if not found_piece:
            for p in self.remote_player.pieces:
                if (p.piece_type.value == piece_type and 
                    p.position.file == from_file and 
                    p.position.rank == from_rank):
                    found_piece = p
                    break
        
        # If still not found, try just by type (closest)
        if not found_piece:
            candidates = [p for p in self.remote_player.pieces if p.piece_type.value == piece_type]
            if candidates:
                closest_piece = None
                min_distance = float('inf')
                
                for p in candidates:
                    dist = abs(p.position.file - from_file) + abs(p.position.rank - from_rank)
                    if dist < min_distance:
                        min_distance = dist
                        closest_piece = p
                
                found_piece = closest_piece
        
        if found_piece:       
            # Store original position for debugging
            orig_file = found_piece.position.file
            orig_rank = found_piece.position.rank
            
            # Update grid position
            found_piece.position = self.Position(to_file, to_rank)
            
            # Update pixel locations
            pixel_loc = found_piece.position.to_pixel()
            found_piece.location = pixel_loc
            found_piece.image_location = pixel_loc
            
            # Update collision rectangle
            found_piece.collision_rect = helper_funcs.reformat_piece_collision(pixel_loc, found_piece.collision_rect)
            
            # Check if this move resolves a check (if remote player was in check)
            if self.check and self.remote_player.is_checked:
                print(f"{role_prefix}Checking if opponent's move resolves their check...")
                still_in_check = helper_funcs.detect_check(self.remote_player, self.local_player, self.board)
                print(f"{role_prefix}Opponent still in check? {still_in_check}")
                if not still_in_check:
                    print(f"{role_prefix}Check resolved by opponent's move")
                    self.check = False
                    self.condition = "None"
                    self.remote_player.is_checked = False
            
            # Only check for captures using grid position
            pieces_to_remove = []
            for p in self.local_player.pieces:
                if p.position.file == to_file and p.position.rank == to_rank:
                    pieces_to_remove.append(p)
            
            # Remove captured pieces
            for p in pieces_to_remove:
                self.local_player.pieces.remove(p)
            
            # Check game conditions
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
        else:
            # Request a full sync 
            self.request_sync()

    def process_sync_message(self, data):
        """Process board sync message"""
        role_prefix = "HOST: " if self.is_host else "CLIENT: "
        
        if not data:
            print(f"{role_prefix}Warning: Empty sync data")
            return
        
        # Extract host and guest piece data
        host_data = data.get("host", {})
        guest_data = data.get("guest", {})
        timestamp = data.get("timestamp", 0)
        
        # Save piece counts before sync for verification
        host_count_before = len(self.host.pieces)
        guest_count_before = len(self.guest.pieces)
        
        # Determine perspective for deserialization
        perspective = (multiplayer.Perspective.HOST if self.is_host 
                    else multiplayer.Perspective.CLIENT)
        
        # Track recently moved pieces to prevent them from being overwritten
        moved_pieces = {}
        
        # If client, identify pieces that were moved locally in the last 2 seconds
        if not self.is_host:
            current_time = time.time()
            for piece in self.local_player.pieces:
                if hasattr(piece, 'last_moved_time') and current_time - piece.last_moved_time < 2.0:
                    moved_pieces[piece.id] = piece
        
        # Update pieces using modified deserialization to respect recently moved pieces
        if host_data:
            multiplayer.deserialize_piece_positions(host_data, self.host.pieces, perspective, moved_pieces)
        
        if guest_data:
            multiplayer.deserialize_piece_positions(guest_data, self.guest.pieces, perspective, moved_pieces)
        
        # Verify we didn't lose any pieces unexpectedly
        host_count_after = len(self.host.pieces)
        guest_count_after = len(self.guest.pieces)
        
        # If host lost more pieces than seems reasonable, this is likely a sync error
        if (self.is_host and 
            host_count_before > host_count_after and 
            host_count_before - host_count_after > 1):
            print(f"{role_prefix}WARNING: Host lost {host_count_before - host_count_after} pieces in sync")
            # Only restore from backup if we have one
            if hasattr(self, 'host_pieces_backup'):
                print(f"{role_prefix}Restoring host pieces from backup")
                self.host.pieces = []
                for p in self.host_pieces_backup:
                    from piece import Piece
                    new_piece = Piece(
                        p.piece_type, 
                        p.location, 
                        p.image_location,
                        pygame.Rect(p.collision_rect), 
                        p.point_value
                    )
                    if hasattr(p, 'position'):
                        new_piece.position = self.Position(p.position.file, p.position.rank)
                    if hasattr(p, 'id'):
                        new_piece.id = p.id
                    self.host.pieces.append(new_piece)
        
        # Realign collision rectangles after sync
        self.realign_piece_collisions(self.host)
        self.realign_piece_collisions(self.guest)
        
        self.immediate_render = True
        
    def process_turn_message(self, data):
        """Process turn update message"""
        role_prefix = "HOST: " if self.is_host else "CLIENT: "
        active_color = data.get("active_player")
        condition = data.get("condition", "None")
        timestamp = data.get("timestamp", 0)
        
        # Only process if this message is newer than our last known state
        if hasattr(self, 'last_turn_timestamp') and timestamp <= self.last_turn_timestamp:
            return
        
        # Store timestamp for future reference
        self.last_turn_timestamp = timestamp
        
        print(f"{role_prefix}Processing turn message: active={active_color}, condition={condition}")
        
        # Update active player and turn flags
        if active_color == self.local_player.color:
            # It's now local player's turn
            self.active_player = self.local_player
            self.waiting_player = self.remote_player
            self.local_player.is_turn = True
            self.remote_player.is_turn = False
        else:
            # It's now remote player's turn
            self.active_player = self.remote_player
            self.waiting_player = self.local_player
            self.remote_player.is_turn = True
            self.local_player.is_turn = False
        
        # Update condition
        self.condition = condition
        
        # Update check state based on condition
        if condition == "Check":
            self.check = True
            # We need to check which player is in check - the active player is making the move,
            # so the waiting player is the one in check
            if self.active_player == self.local_player:
                self.remote_player.is_checked = True
                self.local_player.is_checked = False
            else:
                self.local_player.is_checked = True
                self.remote_player.is_checked = False
        elif condition == "None":
            self.check = False
            self.local_player.is_checked = False
            self.remote_player.is_checked = False
        
        # Force a sync to ensure board state matches turn state
        if self.is_host:
            self.force_sync()
        
        self.immediate_render = True

    # -------------------------------------------------------------------------
    # Game State Transitions
    # -------------------------------------------------------------------------
    
    def transition_to_settings(self):
        """Transition to settings selection phase"""
        self.game_phase = multiplayer.GamePhase.SETTINGS
        
        if self.is_host:
            print("Host entering settings phase")
            # Host selects settings first
            # Will send settings when player clicks Play button
        else:
            print("Client entering settings phase")
            # Client waits for settings from host

    def transition_to_host_swap(self):
        """Transition to host horse swap phase"""
        self.game_phase = multiplayer.GamePhase.HOST_HORSE_SWAP
        
        if self.is_host:
            print("Host beginning horse swap")
            self.opening_turn = True
            self.active_player = self.host
            self.waiting_player = self.guest
        else:
            print("Client waiting for host's horse swap")
            self.opening_turn = True
            self.waiting_for_opponent_swap = True

    def transition_to_client_swap(self):
        """Transition to client horse swap phase"""
        self.game_phase = multiplayer.GamePhase.CLIENT_HORSE_SWAP
        
        if self.is_host:
            print("Host waiting for client's horse swap")
            self.waiting_for_opponent_swap = True
        else:
            print("Client beginning horse swap")
            self.waiting_for_opponent_swap = False
            self.active_player = self.guest
            self.waiting_player = self.host

    def transition_to_gameplay(self):
        """Transition to regular gameplay phase"""
        role_prefix = "HOST: " if self.is_host else "CLIENT: "
        self.game_phase = multiplayer.GamePhase.GAMEPLAY
        print(f"{role_prefix}Transitioning to gameplay phase")
        
        # Set active and waiting players based on Cho/Han assignment
        # Cho player always goes first in Janggi
        self.active_player = self.cho_player
        self.waiting_player = self.han_player
        
        # Explicit turn flag setting
        self.cho_player.is_turn = True
        self.han_player.is_turn = False
        
        # Make sure local_player and remote_player have correct is_turn
        self.local_player.is_turn = (self.local_player == self.cho_player)
        self.remote_player.is_turn = (self.remote_player == self.cho_player)
        
        # Update flags
        self.opening_turn = False
        self.waiting_for_opponent_swap = False
        self.bikjang = False
        self.check = False
        self.condition = "None"
        
        # Set a grace period after swap to prevent immediate game over
        self.post_swap_grace = True
        
        # Realign all collision rectangles before gameplay
        self.realign_piece_collisions(self.host)
        self.realign_piece_collisions(self.guest)
        
        #Create new piece state backup after all swaps are complete
        self.backup_pieces()
        
        # Make sure all pieces are present
        self.validate_board_state()
        
        # Send turn update to notify opponent about gameplay phase and active player
        turn_data = {
            "active_player": self.active_player.color,
            "condition": self.condition,
            "game_phase": multiplayer.GamePhase.GAMEPLAY.value
        }
        self.send_message(multiplayer.MessageType.TURN, turn_data)
        
        # Send full sync to ensure consistency
        self.force_sync()  # Use force sync instead of normal sync to ensure immediate sync


    # -------------------------------------------------------------------------
    # Game Logic Methods
    # -------------------------------------------------------------------------
    
    def handle_event(self, event):
        """Handle input events based on game phase"""
        # Get mouse position for click detection
        mouse_pos = pygame.mouse.get_pos()
        
        # Check for incoming messages
        self.check_for_messages()
        
        # Handle escape key to exit
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.handle_exit()
            return
            
        # Process clicks based on game phase
        # if self.is_left_click(event):
        match(self.game_phase):
            case multiplayer.GamePhase.CREATE_JOIN_GAME:
                self.handle_host_client_choice()
            case multiplayer.GamePhase.CREATE_GAME:
                self.handle_host_init()
            case multiplayer.GamePhase.JOIN_GAME:
                self.handle_client_init(event)
            case multiplayer.GamePhase.SETTINGS:
                self.handle_settings_click(mouse_pos)
            case multiplayer.GamePhase.HOST_HORSE_SWAP:
                if self.is_host and not self.waiting_for_opponent_swap:
                    self.handle_horse_swap_click(mouse_pos)
            case multiplayer.GamePhase.CLIENT_HORSE_SWAP:
                if not self.is_host and not self.waiting_for_opponent_swap:
                    self.handle_horse_swap_click(mouse_pos)
            case multiplayer.GamePhase.GAMEPLAY:
                if not self.game_over and self.active_player == self.local_player:
                    self.handle_gameplay_click(mouse_pos)
            case multiplayer.GamePhase.GAME_OVER:
                pass
            case _:
                print('HOW DID YOU GET HERE???')
                exit()
        # Handle right-click for passing turn
        if self.is_right_click(event):
            if (self.game_phase == multiplayer.GamePhase.GAMEPLAY and
                not self.game_over and 
                self.active_player == self.local_player):
                self.handle_pass_turn(mouse_pos)

    def handle_host_client_choice(self):
        """Establish connection as host or client"""
        if hasattr(self, 'connection') and self.connection is not None:
            print("Using existing connection")
            return
            
        if self.host_button.is_clicked():
            self.game_phase = multiplayer.GamePhase.CREATE_GAME
            
        elif self.client_button.is_clicked():
            self.game_phase = multiplayer.GamePhase.JOIN_GAME

    def handle_host_init(self):
        print("Starting as host. Waiting for client to connect...")
        print(HOST)
        
        # create server, wait for client, move to next game phase
        try:
            self.connection = multiplayer.Server(HOST, PORT)
            self.connection.create_socket()
            self.connection.bind_socket()
            self.connection.listen()
            print("Waiting for client connection...")
            self.connection.accept_client(timeout=60)
            print("Client connected!")
            self.is_host = True        
            self.connection.set_client_non_blocking(True)
            self.send_message(multiplayer.MessageType.CONNECT, {"status": "connected"})
            self.game_phase = multiplayer.GamePhase.SETTINGS
        except Exception as e:
            self.connection_error = True
            print(f'error: {e}')
            print('retrying')

   
    def handle_client_init(self, event):
        # text box for ip addr input        
        self.ip_prompt.handle_event(event)
        # self.ip_prompt.update()

        # try to connect with given ip
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            host = self.ip_prompt.get_input()
            try:
                socket.inet_aton(host)
                self.connection = multiplayer.Client(host, PORT)
                self.connection.connect(timeout=60)
                self.is_host = False
                self.connection.set_non_blocking(True)
                print("Connected to host!")
                self.game_phase = multiplayer.GamePhase.SETTINGS
            except socket.error as e:
                print("not a valid ip")
                self.invalid_ip = True
            except Exception as e:
                print(f"Failed to connect to host: {e}")
                self.connection = None
                self.connection_error = True

    def handle_settings_click(self, mouse_pos):
        """Handle clicks in settings selection phase"""
        if not self.is_host:
            # Client can't change settings
            return
            
        # Handle color selection
        if hasattr(self, 'cho_side_button') and self.cho_side_button.is_clicked():
            self.host.color = "Cho"
            self.guest.color = "Han"
            
        elif hasattr(self, 'han_side_button') and self.han_side_button.is_clicked():
            self.host.color = "Han"
            self.guest.color = "Cho"
            
        # Handle piece convention selection
        elif hasattr(self, 'standard_piece_convention_button') and self.standard_piece_convention_button.is_clicked():
            self.host.piece_convention = "Standard"
            self.guest.piece_convention = "Standard"
            
        elif hasattr(self, 'internat_piece_convention_button') and self.internat_piece_convention_button.is_clicked():
            self.host.piece_convention = "International"
            self.guest.piece_convention = "International"
            
        # Handle play button
        elif hasattr(self, 'play_button') and self.play_button.is_clicked():
            # Send settings to client
            self.send_message(multiplayer.MessageType.SETTINGS, {
                "host_color": self.host.color,
                "piece_convention": self.host.piece_convention
            })
            
            # Update han/cho player references
            self.han_player = self.host if self.host.color == "Han" else self.guest
            self.cho_player = self.guest if self.guest.color == "Cho" else self.host
            
            # Transition to host swap phase
            self.transition_to_host_swap()

    def handle_horse_swap_click(self, mouse_pos):
        """Handle clicks during horse swap phase"""
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
        
        # Handle left horse swap
        if (hasattr(self, 'host_swap_left_horse_button') and 
            self.host_swap_left_horse_button.is_clicked() and 
            left_horse and left_elephant):
            
            helper_funcs.swap_pieces(self.local_player, left_horse, left_elephant)
            print(f"Player swapped left horse and elephant")
            
            # Send swap message to opponent
            self.send_message(multiplayer.MessageType.SWAP, {
                "side": "left"
            })
            
        # Handle right horse swap
        elif (hasattr(self, 'host_swap_right_horse_button') and 
            self.host_swap_right_horse_button.is_clicked() and 
            right_horse and right_elephant):
            
            helper_funcs.swap_pieces(self.local_player, right_horse, right_elephant)
            print(f"Player swapped right horse and elephant")
            
            # Send swap message to opponent
            self.send_message(multiplayer.MessageType.SWAP, {
                "side": "right"
            })
            
        # Handle confirm button
        elif hasattr(self, 'host_confirm_swap_button') and self.host_confirm_swap_button.is_clicked():
            print(f"{'CLIENT' if not self.is_host else 'HOST'}: Confirming swap, current phase: {self.game_phase.value}")
            
            # Prepare detailed message with debug info
            swap_done_data = {
                "phase": self.game_phase.value,
                "client_done": True if not self.is_host else False,
                "host_done": True if self.is_host else False,
                "player_color": self.local_player.color,
                "timestamp": time.time()
            }
            
            success = self.send_message(multiplayer.MessageType.SWAP_DONE, swap_done_data)
            
            # Send full board sync
            self.send_sync()
            
            # Update state based on role and phase
            if self.is_host and self.game_phase == multiplayer.GamePhase.HOST_HORSE_SWAP:
                # Host done with swap, wait for client
                print("HOST: Done with swap, transitioning to client swap phase")
                self.transition_to_client_swap()
                
            elif not self.is_host and self.game_phase == multiplayer.GamePhase.CLIENT_HORSE_SWAP:
                # Client done with swap, game starts
                print("CLIENT: Done with swap, transitioning to gameplay phase")
                self.transition_to_gameplay()

    def handle_gameplay_click(self, mouse_pos):
        """Handle clicks during regular gameplay using grid coordinates"""
        role_prefix = "HOST: " if self.is_host else "CLIENT: "
        local_player = self.local_player
        remote_player = self.remote_player
        
        # Check if it's this player's turn
        if not local_player.is_turn:
            return
        
        # CASE 1: Player has a piece selected and is attempting to move
        if local_player.is_clicked:
            # Track the piece's original position
            clicked_piece = None
            from_pos = None
            
            for p in local_player.pieces:
                if p.is_clicked:
                    clicked_piece = p
                    from_pos = self.Position(p.position.file, p.position.rank)
                    from_pixel = p.location
                    break
                    
            if clicked_piece and helper_funcs.attempt_move(
                local_player, remote_player, self.board, mouse_pos, self.condition
            ):
                # Successful move made - get new position AFTER the move
                to_pos = self.Position(clicked_piece.position.file, clicked_piece.position.rank)
                to_pixel = clicked_piece.location
                
                # Mark the piece as recently moved and timestamp it
                clicked_piece.last_moved_time = time.time()
                
                # Realign collision rectangles after move
                self.realign_piece_collisions(local_player)
                
                # Check if this move resolves a check (if local player was in check)
                if self.check and local_player.is_checked:
                    still_in_check = helper_funcs.detect_check(local_player, remote_player, self.board)
                    if not still_in_check:
                        self.check = False
                        self.condition = "None"
                        local_player.is_checked = False
                
                # Create move data with grid positions and piece ID
                # Transform coordinates to canonical perspective for the host
                from_file = from_pos.file
                from_rank = from_pos.rank
                to_file = to_pos.file
                to_rank = to_pos.rank
                
                # If client, convert to canonical coordinates (flipped)
                if not self.is_host:
                    from_file = 8 - from_file  # Flip horizontally
                    from_rank = 9 - from_rank  # Flip vertically
                    to_file = 8 - to_file
                    to_rank = 9 - to_rank
                
                move_data = {
                    'piece_type': clicked_piece.piece_type.value,
                    'piece_id': clicked_piece.id if hasattr(clicked_piece, 'id') else None,
                    'from_pos': {'file': from_file, 'rank': from_rank},
                    'to_pos': {'file': to_file, 'rank': to_rank},
                    'local_perspective': not self.is_host,  # Flag to indicate if coordinates are from client perspective
                    'timestamp': time.time()
                }
                
                self.send_message(multiplayer.MessageType.MOVE, move_data)
                
                # Reset clicked piece state
                helper_funcs.player_piece_unclick(local_player)
                
                # Check if we captured a piece using grid position only (more reliable than pixel)
                captured = False
                for piece in list(remote_player.pieces):  # Use a copy of the list
                    if piece.position.file == to_pos.file and piece.position.rank == to_pos.rank:
                        remote_player.pieces.remove(piece)
                        captured = True
                        break
                
                # Check for game conditions if not in grace period
                if not self.post_swap_grace:
                    if helper_funcs.detect_bikjang(local_player, remote_player):
                        self.bikjang = True
                        self.condition = "Bikjang"
                        self.winner = local_player
                        self.game_over = True
                        self.game_phase = multiplayer.GamePhase.GAME_OVER
                        
                    elif helper_funcs.detect_check(remote_player, local_player, self.board):
                        self.check = True
                        self.condition = "Check"
                        remote_player.is_checked = True
                else:
                    # We've made our first move after swaps, disable grace period
                    self.post_swap_grace = False
                
                # Only swap turns ONCE
                self.swap_turn()  # This will send the TURN message
                
                # Force a sync to ensure both sides have same state
                # INCREASED DELAY from 0.1s to 0.5s to ensure move is processed first
                if not self.is_host:
                    # Client should wait longer before syncing
                    time.sleep(0.5)
                else:
                    # Host can use shorter delay
                    time.sleep(0.1)
                
                self.force_sync()
                
                self.immediate_render = True
                
            else:
                # If move was invalid, just unselect the piece
                helper_funcs.player_piece_unclick(local_player)
                
        # CASE 2: Player clicked on one of their pieces (piece selection)
        elif helper_funcs.player_piece_clicked(local_player, mouse_pos):
            # The piece clicked state is set by helper_funcs.player_piece_clicked
            for p in local_player.pieces:
                if p.is_clicked:
                    # No need to sync here - just a local selection
                    self.immediate_render = True
                    break
                    
    def handle_pass_turn(self, mouse_pos):
        """Handle passing the turn"""
        # Check if player clicked on the king
        king_piece = None
        for piece in self.local_player.pieces:
            if piece.piece_type.value == "King":
                king_piece = piece
                break
                
        if king_piece and king_piece.collision_rect.collidepoint(mouse_pos):
            # Reset any clicked piece
            helper_funcs.player_piece_unclick(self.local_player)
            
            # Send pass turn message
            self.send_message(multiplayer.MessageType.PASS, {"passing": True})
            
            # Swap turns locally
            self.swap_turn()
            self.immediate_render = True

    def handle_exit(self):
        """Handle exiting the game"""
        # Send exit message
        if self.connection:
            self.send_message(multiplayer.MessageType.EXIT, {"exiting": True})
            
            # Close connection
            try:
                self.connection.close()
            except:
                pass
                
        # Return to main menu
        self.next_state = "Main Menu"

    def swap_turn(self):
        """Swap active and waiting players with proper synchronization"""
        role_prefix = "HOST: " if self.is_host else "CLIENT: "
        
        # 1. Update is_turn flags
        self.active_player.is_turn = False
        self.waiting_player.is_turn = True
        
        # 2. Swap active and waiting players
        temp = self.active_player
        self.active_player = self.waiting_player
        self.waiting_player = temp
        
        # 3. Send turn update message 
        self.send_message(multiplayer.MessageType.TURN, {
            "active_player": self.active_player.color,
            "condition": self.condition,
            "game_over": self.game_over,
            "timestamp": time.time()  #
        })

    def send_sync(self):
        """Send a full board state sync to opponent"""
        current_time = time.time()
        if current_time - self.last_sync_time < self.sync_interval:
            return
            
        self.last_sync_time = current_time
        
        # Create board state with proper perspective
        perspective = (multiplayer.Perspective.HOST if self.is_host 
                      else multiplayer.Perspective.CLIENT)
        
        board_state = multiplayer.serialize_board_state(
            self.host.pieces, 
            self.guest.pieces, 
            perspective
        )
        
        # Send sync message
        self.send_message(multiplayer.MessageType.SYNC, board_state)

    def request_sync(self):
        """Request a board sync from opponent"""
        self.send_message(multiplayer.MessageType.SYNC, {"request": True})

    def swap_left_pieces_for_remote(self):
        """Swap left horse and elephant for remote player"""
        # Find the pieces to swap
        left_elephant = None
        left_horse = None
        
        for piece in self.remote_player.pieces:
            if piece.piece_type.value == "Elephant":
                if not left_elephant or piece.location[0] < left_elephant.location[0]:
                    left_elephant = piece
            elif piece.piece_type.value == "Horse":
                if not left_horse or piece.location[0] < left_horse.location[0]:
                    left_horse = piece
        
        # Perform the swap
        if left_elephant and left_horse:
            helper_funcs.swap_pieces(self.remote_player, left_horse, left_elephant)

    def swap_right_pieces_for_remote(self):
        """Swap right horse and elephant for remote player"""
        # Find the pieces to swap
        right_elephant = None
        right_horse = None
        
        for piece in self.remote_player.pieces:
            if piece.piece_type.value == "Elephant":
                if not right_elephant or piece.location[0] > right_elephant.location[0]:
                    right_elephant = piece
            elif piece.piece_type.value == "Horse":
                if not right_horse or piece.location[0] > right_horse.location[0]:
                    right_horse = piece
        
        # Perform the swap
        if right_elephant and right_horse:
            helper_funcs.swap_pieces(self.remote_player, right_horse, right_elephant)

    def realign_piece_collisions(self, player):
        """Realign all piece collision rectangles and update grid positions"""
        if not player or not player.pieces:
            return
            
        role_prefix = "HOST: " if self.is_host else "CLIENT: "
        
        for piece in player.pieces:
            if piece and piece.location:
                # Store original rect and position for debugging
                old_rect = pygame.Rect(piece.collision_rect)
                old_pos = piece.position if hasattr(piece, 'position') else None
                
                # Reformat collision rectangle to match current pixel location
                piece.collision_rect = helper_funcs.reformat_piece_collision(
                    piece.location, piece.collision_rect)
                
                # Make sure grid position matches pixel location
                piece.position = self.Position.from_pixel(piece.location)
                
                # Make sure image location matches location
                piece.image_location = piece.location

    def force_sync(self):
        """Force an immediate board sync"""
        role_prefix = "HOST: " if self.is_host else "CLIENT: "
        
        # Create board state with proper perspective
        perspective = (multiplayer.Perspective.HOST if self.is_host 
                    else multiplayer.Perspective.CLIENT)
        
        # Make backup copies before syncing
        if self.is_host:
            self.host_pieces_backup = []
            for p in self.host.pieces:
                from piece import Piece
                new_piece = Piece(
                    p.piece_type, 
                    p.location, 
                    p.image_location,
                    pygame.Rect(p.collision_rect), 
                    p.point_value
                )
                if hasattr(p, 'position'):
                    new_piece.position = self.Position(p.position.file, p.position.rank)
                if hasattr(p, 'id'):
                    new_piece.id = p.id
                self.host_pieces_backup.append(new_piece)
        
        # Ensure collision rectangles are properly aligned before serializing
        self.realign_piece_collisions(self.host)
        self.realign_piece_collisions(self.guest)
        
        # Serialize the current state
        board_state = multiplayer.serialize_board_state(
            self.host.pieces, 
            self.guest.pieces, 
            perspective
        )
        
        # Add timestamp to track sync sequence
        board_state['timestamp'] = time.time()
        
        # Send sync message
        self.send_message(multiplayer.MessageType.SYNC, board_state)
        
        # Update the last sync time
        self.last_sync_time = time.time()
        
        
    def verify_piece_data(self, piece_data, pieces):
        """Verify piece data before applying it"""
        # Group existing pieces by type for comparison
        piece_map = {}
        for piece in pieces:
            piece_type = piece.piece_type.value
            if piece_type not in piece_map:
                piece_map[piece_type] = []
            piece_map[piece_type].append(piece)
        
        # Basic checks for each piece type
        for piece_type, positions in piece_data.items():
            # Skip verification during gameplay (due to captures)
            if self.game_phase == multiplayer.GamePhase.GAMEPLAY:
                continue
                
            # During setup, ensure we have the right piece counts
            if piece_type not in piece_map:
                return False
                
            # During setup we expect exact match
            if len(piece_map[piece_type]) != len(positions):
                return False        
        return True

    def update(self):
        """Perform regular game updates"""
        # Check for incoming messages
        self.check_for_messages()
        
        # Check if we need to perform a validation
        current_time = time.time()
        if hasattr(self, 'validation_interval') and hasattr(self, 'last_validation_time'):
            if current_time - self.last_validation_time > self.validation_interval:
                # Verify all pieces have valid positions
                for p in self.host.pieces + self.guest.pieces:
                    if not hasattr(p, 'position') or not hasattr(p.position, 'file') or not hasattr(p.position, 'rank'):
                        self.restore_pieces_from_backup()
                        break
                
                self.last_validation_time = current_time
                
        # If hosting, perform occasional full syncs during gameplay
        if self.is_host and self.game_phase == multiplayer.GamePhase.GAMEPLAY:
            if current_time - self.last_sync_time > self.sync_interval * 5:  # Every 2.5 seconds
                self.force_sync()


    # -------------------------------------------------------------------------
    # UI Initialization and Rendering
    # -------------------------------------------------------------------------
    def load_game_state_elements(self):
        """Load UI elements for game state display"""
        # Game state background
        self.game_state_background = pygame.image.load("UI/Button_Background.png").convert_alpha()
        self.game_state_background = pygame.transform.scale(self.game_state_background,
                constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["single_player"]["button_background"]["game_state"]["size"])
        
        # Game over background
        self.game_over_background = pygame.image.load("UI/Button_Background.png").convert_alpha()
        self.game_over_background = pygame.transform.scale(self.game_over_background,
                constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["single_player"]["button_background"]["game_over"]["size"])
        

    def render(self, window):
            """Render the game based on current phase"""
            # Render board
            self.render_board(window)
            
            # Render phase-specific elements
            match(self.game_phase):
                case multiplayer.GamePhase.CREATE_JOIN_GAME:
                    self.render_create_join_game(window)
                case multiplayer.GamePhase.JOIN_GAME:
                    self.render_join_game(window)
                case multiplayer.GamePhase.CREATE_GAME:
                    self.render_create_game(window)
                case multiplayer.GamePhase.SETTINGS:
                    self.render_settings(window)
                case multiplayer.GamePhase.HOST_HORSE_SWAP:
                    self.render_host_swap(window)
                case multiplayer.GamePhase.CLIENT_HORSE_SWAP:
                    self.render_client_swap(window)
                case multiplayer.GamePhase.GAMEPLAY:
                    self.render_gameplay(window)
                case multiplayer.GamePhase.GAME_OVER:
                    self.render_game_over(window)
                
            # Always show connection status
            self.render_connection_status(window)

    def render_create_join_game(self, window):
        self.render_message(window, 'Host or Client?',
                            (constants.screen_width/2, constants.screen_height/2))
        self.host_button.draw_button(window)
        self.client_button.draw_button(window)

    def render_create_game(self, window):
        self.render_message(window, f"Give IP to the other player: {HOST}",
                                    (constants.screen_width//2, constants.screen_height//2))
        if self.connection_error:
            self.render_message(window, f"There was a problem connecting player. Press esc to retry",
                                (constants.screen_width//2, constants.screen_height//2+100))

    def render_join_game(self, window):
        self.render_message(window, 'enter IP of host', (constants.screen_width//2, constants.screen_height//2-100))
        self.ip_prompt.render(window)
        if self.connection_error:
            self.render_message(window, f"There was a problem connecting player. Press esc to retry",
                                (constants.screen_width//2, constants.screen_height//2+100))
        if self.invalid_ip:
            self.render_message(window, f"Invalid ip given, try again",
                                (constants.screen_width//2, constants.screen_height//2+100))

    def render_settings(self, window):
            """Render settings selection phase"""
            if self.is_host:
                # Host can select settings
                self.render_settings_ui(window)
            else:
                # Client waits for settings from host
                self.render_message(window, "Waiting for host to select settings...",
                                    (constants.screen_width//2, constants.screen_height//2))

    def render_settings_ui(self, window):
        """Render settings UI for host"""
        # Skip rendering if elements aren't initialized yet
        if not hasattr(self, 'play_as_background') or not self.play_as_background:
            self.draw_text(window, "Loading settings UI...", 
                          constants.screen_width//2 - 200, constants.screen_height//2, 30)
            return
            
        font_size, x, y = self.render_player_color_menu(window)
        # Show selected color
        selected_color = "Cho" if self.host.color == "Cho" else "Han"
        self.draw_text(window, f"Selected: {selected_color}", x, y + 40, font_size - 10)
        
        font_size, x, y = self.render_piece_convention_menu(window)
        # Show selected convention
        self.draw_text(window, f"Selected: {self.host.piece_convention}", x, y + 40, font_size - 10)
        
        self.render_play_button(window)        
        self.render_player_piece_preview(window)

    def render_host_swap(self, window):
        """Render host horse swap phase"""
        if self.is_host and not self.waiting_for_opponent_swap:
            # Host is swapping horses
            self.render_swap_ui(window)
            message = "Host's Horse Swap Phase"
        else:
            # Client is waiting for host to swap
            message = "Waiting for host to complete horse swap..."

        self.render_pieces(self.host, self.guest, window)
        self.draw_text(window, message, constants.screen_width//2 - 220, constants.screen_height//2, 30)

    def render_client_swap(self, window):
        """Render client horse swap phase"""
        if not self.is_host and not self.waiting_for_opponent_swap:
            self.render_swap_ui(window)
            message = "Client's Horse Swap Phase"
        else:
            # Host is waiting for client to swap
            message = "Waiting for client to complete horse swap..."

        self.render_pieces(self.host, self.guest, window)
        self.draw_text(window, message, constants.screen_width//2 - 220, constants.screen_height//2, 30)

    def render_gameplay(self, window):
        """Render regular gameplay phase"""
        # Render pieces
        self.render_pieces(self.local_player, self.remote_player, window)
        
        # If player has a piece clicked, render possible moves
        if self.local_player.is_clicked:
            render_funcs.render_possible_spots(self.local_player, self.remote_player, 
                                              self.board, window, self.condition)
            
        # Render special conditions
        if self.bikjang:
            render_funcs.render_bikjang_highlight(self.active_player, self.waiting_player, window)
        if self.check:
            if self.guest.is_checked:
                render_funcs.render_check_highlight(self.guest, window)
            else:
                render_funcs.render_check_highlight(self.host, window)
                
        # Render turn indicator
        turn_text = "Your Turn" if self.active_player == self.local_player else "Opponent's Turn"
        self.draw_text(window, turn_text, constants.screen_width - 200, 80, 25)
        
        # Render condition indicator if any
        if self.condition != "None":
            self.draw_text(window, f"Condition: {self.condition}", constants.screen_width - 200, 110, 25)
            
    def render_game_over(self, window):
        """Render game over state"""
        # Render pieces in final position
        self.render_pieces(self.local_player, self.remote_player, window)
        
        # Render special conditions
        if self.bikjang:
            self.render_bikjang_ending(window)
        elif self.check:
            self.render_check_ending(window)

    def render_swap_ui(self, window):
        """Render horse swap UI"""
        # Left horse swap button
        window.blit(self.host_swap_left_horse_background, 
            constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["single_player"]["button_background"]["swap_left_horse"]["location"])
        self.host_swap_left_horse_button.draw_button(window)

        # Right horse swap button
        window.blit(self.host_swap_right_horse_background,
            constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["single_player"]["button_background"]["swap_right_horse"]["location"])
        self.host_swap_right_horse_button.draw_button(window)

        # Confirm button
        window.blit(self.host_confirm_swap_button_background,
            constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["single_player"]["button_background"]["confirm_swap"]["location"])
        self.host_confirm_swap_button.draw_button(window)

    def render_connection_status(self, window):
        """Render connection status and game phase"""
        # Display connection status
        status_x = 20
        status_y = 20
        role = "Host" if self.is_host else "Client"
        
        # Format the phase name to be more readable
        phase_raw = self.game_phase.value
        # Split by underscore and capitalize each word
        phase_words = phase_raw.split('_')
        phase = ' '.join(word.capitalize() for word in phase_words)
        
        # Display connection info
        self.draw_text(window, f"Connected as: {role}", status_x, status_y, 20)
        self.draw_text(window, f"Game Phase: {phase}", status_x, status_y + 25, 20)
        
        # Display color info
        your_color = self.local_player.color
        self.draw_text(window, f"Your color: {your_color}", status_x, status_y + 50, 20)
                      
    def render_pieces(self, local_player, remote_player, window):
        """Render pieces with correct perspective"""
        render_funcs.render_pieces(local_player, remote_player, window)

    def load_button_background(self):
        """Load button backgrounds for settings UI"""
        super().load_button_background()
        
        # Player piece display background
        self.player_piece_display_background = pygame.image.load("UI/Button_Background.png").convert_alpha()
        self.player_piece_display_background = pygame.transform.rotate(self.player_piece_display_background, 90)
        self.player_piece_display_background = pygame.transform.scale(self.player_piece_display_background,
                constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["local_MP"]["button_background"]["player_piece_display"]["size"])
        
        # Player header background
        self.player_header_background = pygame.image.load("UI/Button_Background.png").convert_alpha()
        self.player_header_background = pygame.transform.scale(self.player_header_background,
                constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["local_MP"]["button_background"]["player_piece_display"]["player_header"]["size"])
        
        # Opponent piece display background
        self.opponent_piece_display_background = pygame.image.load("UI/Button_Background.png").convert_alpha()
        self.opponent_piece_display_background = pygame.transform.rotate(self.opponent_piece_display_background, 270)
        self.opponent_piece_display_background = pygame.transform.scale(self.opponent_piece_display_background,
                constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["local_MP"]["button_background"]["opponent_piece_display"]["size"])
        
        # Play button background
        self.play_button_background = pygame.image.load("UI/Button_Background_Poly.png").convert_alpha()
        self.play_button_background = pygame.transform.scale(self.play_button_background,
                constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["local_MP"]["button_background"]["play"]["size"])
        
        # Play as background
        self.play_as_background = pygame.transform.scale(self.button_background,
                constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["local_MP"]["button_background"]["play_as"]["size"])
        
        # Piece convention background
        self.piece_convention_background = pygame.transform.scale(self.button_background,
                constants.resolutions[f"{constants.screen_width}x{constants.screen_height}"]["background_elements"]["local_MP"]["button_background"]["piece_convention"]["size"])

COLOR_INACTIVE = pygame.Color('grey')
COLOR_ACTIVE = pygame.Color('white')
FONT = pygame.font.Font(None, 32)

class InputBox:

    def __init__(self, pos, size, text='', font=None, font_size=32):
        pos = pos[0]-(size[0]/2), pos[1]-(size[1]/2)
        self.rect = pygame.Rect(pos[0], pos[1], size[0], size[1])
        self.color = 'white'
        self.text = text
        self.to_return = None
        self.txt_surface = FONT.render(text, True, 'black')
        self.active = False

    def get_input(self):
         return self.to_return

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    self.to_return = self.text
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, 'black')

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def render(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, 'black', self.rect, 2)
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
