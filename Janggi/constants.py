"""
----------------------constants.py--------------------------------
o This file is to hold any global constants to be used by program
o Place all global constants into here
o Last Modified - November 19th 2024
------------------------------------------------------------------
"""
import pygame

# initialize pygame instance
pygame.init()

info = pygame.display.Info()

# rectangle colors
WHITE = (255,255,255)
BLACK = (0,0,0)
GREY = (100,100,100)
RED = (200,16,46)
BLUE = (0,47,108,)
GREEN = (30,100,0)
LIGHT_GREEN = (35,200,0)

# reference window size
REFERENCE_WIDTH = 1600
REFERENCE_HEIGHT = 900

# window size
window_size = (1600, 900) #(1600, 900) 
#window_size = (640, 480)
#window_size = (900,580)

# scale factor for width and height
scale_w = 1
scale_h = 1

# UI mapping for resolution sizes

# 1920x1080 -> Supported
# 1440x900 -> Supported
# 680x480 -> In Developement

# resolutions dictionary
#uses the values of 1440x900 as a base reference for the size of objects
resolutions = {
    "1440x900": {
        #Half of these were unecessary as they were not even called anywhere in any file
        #and the other half are created outside of the dictionary to reduce redundancy.

        #"vertical_offset": 10,
        #"board_border_size": (900, 900),
        #"board_size": (800, 800),
        #"x_board_start_loc": 362,
        #"x_board_end_loc": 1273,
        #"x_spacing": 104.33,
        #"y_board_start_loc": 5,
        #"y_board_end_loc": 835,
        #"y_spacing": 92.22,
        #"x_coordinates": [368, 468, 568, 668, 768, 868, 968, 1068, 1168],
        #"y_coordinates": [19, 109, 199, 289, 379, 469, 558, 648, 737, 818],
        #"spot_collision_size": (50, 50),
        #"small_collision_size": (50, 50),
        #"small_size": (50, 50),
        #"med_collision_size": (60, 60),
        #"med_size": (70,70),
        #"large_collision_size": (80, 80),
        #"large_size": (90,90),
        
        #These subdictionaries are used to store the UI elements for the main menu, single player, and local multiplayer.

        "buttons": 
        {
            "main_menu" :
            {
                "single_player_button":
                {
                    "location": (615, 229.17),
                    "size": (375, 83.33),
                    "text": 
                    {
                        "font" : pygame.font.SysFont("Arial",size=40),
                        "string": "Play Against an AI",
                        "foreground_color": BLACK,
                        "background_color": WHITE,
                        "hover_color": LIGHT_GREEN

                    }
                },
                "local_multiplayer_button":
                {
                    "location": (615, 354.17),
                    "size": (375, 83.33),
                    "text": 
                    {
                        "font" : pygame.font.SysFont("Arial",size=40),
                        "string": "Play by Yourself",
                        "foreground_color": BLACK,
                        "background_color": WHITE,
                        "hover_color": LIGHT_GREEN

                    }
                },
                "multiplayer_button":
                {
                    "location": (615, 475),
                    "size": (375, 83.33),
                    "text": 
                    {
                        "font" : pygame.font.SysFont("Arial",size=40),
                        "string": "Play Against a Friend",
                        "foreground_color": BLACK,
                        "background_color": WHITE,
                        "hover_color": LIGHT_GREEN

                    }
                },
                "close_button":
                {
                    "location": (615, 600),
                    "size": (375, 83.33),
                    "text": 
                    {
                        "font" : pygame.font.SysFont("Arial",size=40),
                        "string": "Close The Application",
                        "foreground_color": BLACK,
                        "background_color": WHITE,
                        "hover_color": LIGHT_GREEN

                    }
                }       
            },
            "single_player" : 
            {
                "cho_button":
                  {
                    "location": (660, 200),
                    "size": (75, 33.33),
                    "text": 
                    {
                        "font" : pygame.font.SysFont("Arial",size=25),
                        "string": "Cho",
                        "foreground_color": BLACK,
                        "background_color": WHITE,
                        "hover_color": LIGHT_GREEN

                    }
                  },
                "han_button": 
                {
                    "location": (860, 200),
                    "size": (75, 33.33),
                    "text": 
                    {
                        "font" : pygame.font.SysFont("Arial",size=25),
                        "string": "Han",
                        "foreground_color": BLACK,
                        "background_color": WHITE,
                        "hover_color": LIGHT_GREEN

                    }
                },
                "standard_piece_convention_button": 
                {
                    "location": (600, 390),
                    "size": (125, 33.33),
                    "text": 
                    {
                        "font" : pygame.font.SysFont("Arial",size=25),
                        "string": "Standard",
                        "foreground_color": BLACK,
                        "background_color": WHITE,
                        "hover_color": LIGHT_GREEN

                    }
                },
                "internat_piece_convention_button": 
                {
                    "location": (880, 390),
                    "size": (125, 33.33),
                    "text": 
                    {
                        "font" : pygame.font.SysFont("Arial",size=25),
                        "string": "International",
                        "foreground_color": BLACK,
                        "background_color": WHITE,
                        "hover_color": LIGHT_GREEN

                    }
                },
                "easy_ai_button": 
                {
                    "location": (600, 570),
                    "size": (100, 33.33),
                    "text": 
                    {
                        "font" : pygame.font.SysFont("Arial",size=25),
                        "string": "Easy",
                        "foreground_color": BLACK,
                        "background_color": WHITE,
                        "hover_color": LIGHT_GREEN

                    }
                },
                "medium_ai_button": 
                {
                    "location": (750, 570),
                    "size": (100, 33.33),
                    "text": 
                    {
                        "font" : pygame.font.SysFont("Arial",size=25),
                        "string": "Medium",
                        "foreground_color": BLACK,
                        "background_color": WHITE,
                        "hover_color": LIGHT_GREEN

                    }
                },
                "hard_ai_button": 
                {
                    "location": (900, 570),
                    "size": (100, 33.33),
                    "text": 
                    {
                        "font" : pygame.font.SysFont("Arial",size=25),
                        "string": "Hard",
                        "foreground_color": BLACK,
                        "background_color": WHITE,
                        "hover_color": LIGHT_GREEN

                    }
                },
                "play_button": 
                {
                    "location": (762.5, 750),
                    "size": (75, 33.33),
                    "text": 
                    {
                        "font" : pygame.font.SysFont("Arial",size=25),
                        "string": "Play",
                        "foreground_color": BLACK,
                        "background_color": WHITE,
                        "hover_color": LIGHT_GREEN

                    }
                },
                "swap_left_horse_button": 
                {
                        "location": (510, 760),
                        "size": (75, 33.33),
                        "text": 
                        {
                            "font" : pygame.font.SysFont("Arial",size=25),
                            "string": "Swap",
                            "foreground_color": BLACK,
                            "background_color": WHITE,
                            "hover_color": LIGHT_GREEN

                        }
                },
                "swap_right_horse_button": 
                {

                    "location": (1010, 760),
                    "size": (75, 33.33),
                    "text": 
                    {
                        "font" : pygame.font.SysFont("Arial",size=25),
                        "string": "Swap",
                        "foreground_color": BLACK,
                        "background_color": WHITE,
                        "hover_color": LIGHT_GREEN

                    }
                },
                "confirm_swap_button": 
                {
                    "location": (755, 745),
                    "size": (90, 50),
                    "text": 
                    {
                        "font" : pygame.font.SysFont("Arial",size=25),
                        "string": "Confirm",
                        "foreground_color": BLACK,
                        "background_color": WHITE,
                        "hover_color": LIGHT_GREEN

                    }
                },
            },
            "local_MP" : 
            {
                "cho_button":
                  {
                    "location": (660, 200),
                    "size": (75, 33.33),
                    "text": 
                    {
                        "font" : pygame.font.SysFont("Arial",size=25),
                        "string": "Cho",
                        "foreground_color": BLACK,
                        "background_color": WHITE,
                        "hover_color": LIGHT_GREEN

                    }
                  },
                "han_button": 
                {
                    "location": (860, 200),
                    "size": (75, 33.33),
                    "text": 
                    {
                        "font" : pygame.font.SysFont("Arial",size=25),
                        "string": "Han",
                        "foreground_color": BLACK,
                        "background_color": WHITE,
                        "hover_color": LIGHT_GREEN

                    }
                },
                "standard_piece_convention_button": 
                {
                    "location": (600, 390),
                    "size": (125, 33.33),
                    "text": 
                    {
                        "font" : pygame.font.SysFont("Arial",size=25),
                        "string": "Standard",
                        "foreground_color": BLACK,
                        "background_color": WHITE,
                        "hover_color": LIGHT_GREEN

                    }
                },
                "internat_piece_convention_button": 
                {
                    "location": (880, 390),
                    "size": (125, 33.33),
                    "text": 
                    {
                        "font" : pygame.font.SysFont("Arial",size=25),
                        "string": "International",
                        "foreground_color": BLACK,
                        "background_color": WHITE,
                        "hover_color": LIGHT_GREEN

                    }
                },
                "play_button": 
                {
                    "location": (762.5, 750),
                    "size": (75, 33.33),
                    "text": 
                    {
                        "font" : pygame.font.SysFont("Arial",size=25),
                        "string": "Play",
                        "foreground_color": BLACK,
                        "background_color": WHITE,
                        "hover_color": LIGHT_GREEN

                    }
                },
                "host_swap_left_horse_button": 
                {
                        "location": (510, 760),
                        "size": (75, 33.33),
                        "text": 
                        {
                            "font" : pygame.font.SysFont("Arial",size=25),
                            "string": "Swap",
                            "foreground_color": BLACK,
                            "background_color": WHITE,
                            "hover_color": LIGHT_GREEN

                        }
                },
                "host_swap_right_horse_button": 
                {

                    "location": (1010, 760),
                    "size": (75, 33.33),
                    "text": 
                    {
                        "font" : pygame.font.SysFont("Arial",size=25),
                        "string": "Swap",
                        "foreground_color": BLACK,
                        "background_color": WHITE,
                        "hover_color": LIGHT_GREEN

                    }
                },
                "host_confirm_swap_button": 
                {
                    "location": (755, 745),
                    "size": (90, 50),
                    "text": 
                    {
                        "font" : pygame.font.SysFont("Arial",size=25),
                        "string": "Confirm",
                        "foreground_color": BLACK,
                        "background_color": WHITE,
                        "hover_color": LIGHT_GREEN

                    }
                },
                "guest_swap_left_horse_button": 
                {
                        "location": (510, 110),
                        "size": (75, 33.33),
                        "text": 
                        {
                            "font" : pygame.font.SysFont("Arial",size=25),
                            "string": "Swap",
                            "foreground_color": BLACK,
                            "background_color": WHITE,
                            "hover_color": LIGHT_GREEN

                        }
                },
                "guest_swap_right_horse_button": 
                {

                    "location": (1010, 110),
                    "size": (75, 33.33),
                    "text": 
                    {
                        "font" : pygame.font.SysFont("Arial",size=25),
                        "string": "Swap",
                        "foreground_color": BLACK,
                        "background_color": WHITE,
                        "hover_color": LIGHT_GREEN

                    }
                },
                "guest_confirm_swap_button": 
                {
                    "location": (755, 118),
                    "size": (90, 50),
                    "text": 
                    {
                        "font" : pygame.font.SysFont("Arial",size=25),
                        "string": "Confirm",
                        "foreground_color": BLACK,
                        "background_color": WHITE,
                        "hover_color": LIGHT_GREEN

                    }
                }
            }
        },
        "background_elements": 
        {
            "main_menu": 
            {
                "menu_background_size": (750, 750) 
            },
            "single_player": 
            {
                "button_background" : 
                {
                    "play_as": 
                    {
                        "text": 
                        {
                            "string" : "Select Side to Play As",
                            "location": (680, 135),
                            "font_size": 30,
                        },
                        "location": (625, 100),
                        "size": (350, 150)
                    },
                    "piece_convention": 
                    {
                        "text": 
                        {
                            "string" : "Select Piece Convention",
                            "location": (665, 325),
                            "font_size": 30,
                        },
                        "location": (575, 295),
                        "size": (450, 145)
                    },
                    "ai_level": 
                    {
                        "text": 
                        {
                            "string" : "Selected AI Difficulty:",
                            "location": (635, 500),
                            "font_size": 30,
                            "chosen_diff_location": (885, 500)
                        },
                        "location": (575, 470),
                        "size": (485, 170)
                    },
                    "play": 
                    {
                        "location": (710, 676),
                        "size": (180, 180)
                    },
                    "player_piece_display": 
                    {
                        "text": 
                        {
                            "string" : "Your Pieces",
                            "location": (360, 210),
                            "font_size": 25,
                        },
                        "location": (350, 245),
                        "size": (140, 700),
                        "player_header" :
                        {
                            "location": (350, 200),
                            "size": (140, 80)
                        }
                    },
                    "opponent_piece_display": 
                    {
                        "text": 
                        {
                            "location": (800, 210),
                            "font_size": 35,
                        },
                        "location": (1110, 245),
                        "size": (140, 700)
                    },
                    "swap_left_horse": 
                    {
                        "location": (450, 750),
                        "size": (200, 150)
                    },
                    "swap_right_horse": 
                    {
                        "location": (950, 750),
                        "size": (200, 150)
                    },
                    "confirm_swap":
                    {
                        "location": (710, 676),
                        "size": (180, 180)
                    },
                    "game_state":
                    {
                        "location": (0, 240),
                        "size": (400, 200),
                        
                    },
                    "game_over":
                    {
                        "location": (480, 340),
                        "size": (650, 200),
                        "notify_text":
                        {
                            "location": (525, 380),
                            "font_size": 45
                        },
                        "condition_text":
                        {
                            "location": (525, 485),
                            "font_size": 35
                        },
                        "result_text":
                        {
                            "location": (925, 380),
                            "font_size": 45
                        }
                    }
                }
            },
            "local_MP": 
            {
                "button_background" : 
                {
                    "play_as": 
                    {
                        "text": 
                        {
                            "string" : "Select Side to Play As",
                            "location": (680, 135),
                            "font_size": 30,
                        },
                        "location": (625, 100),
                        "size": (350, 150)
                    },
                    "piece_convention": 
                    {
                        "text": 
                        {
                            "string" : "Select Piece Convention",
                            "location": (665, 325),
                            "font_size": 30,
                        },
                        "location": (575, 295),
                        "size": (450, 145)
                    },
                    "play": 
                    {
                        "location": (710, 676),
                        "size": (180, 180)
                    },
                    "player_piece_display": 
                    {
                        "text": 
                        {
                            "string" : "Your Pieces",
                            "location": (360, 210),
                            "font_size": 25,
                        },
                        "location": (350, 245),
                        "size": (140, 700),
                        "player_header" :
                        {
                            "location": (350, 200),
                            "size": (140, 80)
                        }
                    },
                    "opponent_piece_display": 
                    {
                        "text": 
                        {
                            "location": (800, 210),
                            "font_size": 35,
                        },
                        "location": (1110, 245),
                        "size": (140, 700)
                    },
                    "host_swap_left_horse": 
                    {
                        "location": (450, 750),
                        "size": (200, 150)
                    },
                    "host_swap_right_horse": 
                    {
                        "location": (950, 750),
                        "size": (200, 150)
                    },
                    "host_confirm_swap":
                    {
                        "location": (710, 676),
                        "size": (180, 180)
                    },
                    "guest_swap_left_horse": 
                    {
                        "location": (450, 0),
                        "size": (200, 150)
                    },
                    "guest_swap_right_horse": 
                    {
                        "location": (950, 0),
                        "size": (200, 150)
                    },
                    "guest_confirm_swap":
                    {
                        "location": (710, 50),
                        "size": (180, 180)
                    },
                    "game_state":
                    {
                        "location": (0, 240),
                        "size": (400, 200),
                        
                    },
                    "game_over":
                    {
                        "location": (480, 340),
                        "size": (650, 200),
                        "notify_text":
                        {
                            "location": (525, 380),
                            "font_size": 45
                        },
                        "condition_text":
                        {
                            "location": (525, 485),
                            "font_size": 35
                        },
                        "result_text":
                        {
                            "location": (925, 380),
                            "font_size": 45
                        }
                    }
                }
            }
        },
    }
    
}

# flag for app run loop
running = True

# create window size based on user's machine
info = pygame.display.Info()

# set window sizes based on user's machine
#screen_width, screen_height = info.current_w, info.current_h
#screen_width, screen_height = 1920, 1080
screen_width, screen_height = 1440, 900         #key for 1440x900 resolution dictionary
#screen_width, screen_height = 640, 480

#ignoring this way of setting the variables to reduce redundancy
'''# set window variables ofr GUI elements
#vertical_offset = resolutions[f"{screen_width}x{screen_height}"]["vertical_offset"]
board_border_size = resolutions[f"{screen_width}x{screen_height}"]["board_border_size"]
board_size = resolutions[f"{screen_width}x{screen_height}"]["board_size"]
#x_board_start_loc = resolutions[f"{screen_width}x{screen_height}"]["x_board_start_loc"]
#x_board_end_loc = resolutions[f"{screen_width}x{screen_height}"]["x_board_end_loc"]
#x_spacing = resolutions[f"{screen_width}x{screen_height}"]["x_spacing"]
#y_board_start_loc = resolutions[f"{screen_width}x{screen_height}"]["y_board_start_loc"]
#y_board_end_loc = resolutions[f"{screen_width}x{screen_height}"]["y_board_end_loc"]
#y_spacing = resolutions[f"{screen_width}x{screen_height}"]["y_spacing"]
spot_collision_size = resolutions[f"{screen_width}x{screen_height}"]["spot_collision_size"]
small_collision_size = resolutions[f"{screen_width}x{screen_height}"]["small_collision_size"]
small_size = resolutions[f"{screen_width}x{screen_height}"]["small_size"]
med_collision_size = resolutions[f"{screen_width}x{screen_height}"]["med_collision_size"]
med_size = resolutions[f"{screen_width}x{screen_height}"]["med_size"]
large_collision_size = resolutions[f"{screen_width}x{screen_height}"]["large_collision_size"]
large_size = resolutions[f"{screen_width}x{screen_height}"]["large_size"]

x_coords = resolutions[f"{screen_width}x{screen_height}"]["x_coordinates"]
y_coords = resolutions[f"{screen_width}x{screen_height}"]["y_coordinates"]'''

#variables that handle board size, collision size, and piece coordinates
board_border_size = (900, 900)
board_size = (800, 800)

spot_collision_size = (50, 50)
small_collision_size = (50, 50)
small_size = (50, 50)
med_collision_size = (60, 60)
med_size = (70,70)
large_collision_size = (80, 80)
large_size = (90,90)

x_coords = [368, 468, 568, 668, 768, 868, 968, 1068, 1168]
y_coords = [19, 109, 199, 289, 379, 469, 558, 648, 737, 818]

x_coordinates = [coordinate for coordinate in x_coords]
y_coordinates = [coordinate for coordinate in y_coords]

# possible settings for checking if a settings pre-set file is correctly written
possible_colorside = ("Cho", "Han")
possible_piece_convention = ("Standard", "International")
possible_ai_level = ("Easy", "Medium", "Hard")