"""
----------------------constants.py--------------------------------
o This file is to hold any global constants used by program
o Place all global constants into here
o Last Modified - April 8th 2025
------------------------------------------------------------------
"""
import pygame
import res_config
from helper_funcs import scale_x, scale_y, is_fullscr

# initialize pygame instance
pygame.init()

info = pygame.display.Info()
eWidth, eHeight = is_fullscr(info.current_w, info.current_h)


screen_width, screen_height = res_config.ewidth, res_config.eheight
print(screen_width, screen_height)

# rectangle colors
WHITE = (255,255,255)
BLACK = (0,0,0)
GREY = (100,100,100)
RED = (200,16,46)
BLUE = (0,47,108)
GREEN = (30,100,0)
LIGHT_GREEN = (35,200,0)

# UI mapping for resolution sizes
# 111x111 -> MAC/Resize
# 1920x1080 -> Supported
# 1440x900 -> Supported
# 680x480 -> In Developement
resolutions = {
"1360x796":
{
    "vertical_offset": 50,
    "board_border_size": (796, 796),
    "board_size": (676, 676),
    "x_board_start_loc": 447,
    "x_board_end_loc": 1552,
    "x_spacing": 119.77,
    "y_board_start_loc": 32.5,
    "y_board_end_loc": 676,
    "y_spacing": 106.4,
    # "x_coordinates": [448, 568, 688, 808, 928, 1047, 1168, 1288, 1406], -123
    "x_coordinates": [312, 395, 478, 565, 647, 733, 817, 900, 983],
    # "x_coordinates": [eWidth // 7 + 20, 568, 688, 808, 928, 1047, 1168, 1288, eWidth // 7 + 985],
    "y_coordinates": [29, 108, 180, 257, 332, 407, 483, 560, 634, 700],
    # "y_coordinates": [29, 136.5, 245, 252, 360, 467, 575, 682, 790, 887],
    "piece_reformat_size": (32, 32),
    "spot_collision_size": (65, 65),
    "small_collision_size": (30, 30),
    "small_size": (45, 45),
    "med_collision_size": (55, 55),
    "med_size": (70,70),
    "large_collision_size": (85, 85),
    "large_size": (95,95),
    "buttons": 
    {
        "main_menu" :
        {
            "single_player_button":
            {
                # "location": (715, 275),
                "location": (1, 245),
                "size": (400, 80),
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
                # "location": (715, 425),
                "location": (1, 345),
                "size": (400, 80),
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
                # "location": (715, 570),
                "location": (1, 445),
                "size": (400, 80),
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
                # "location": (715, 720),
                "location": (1, 545),
                "size": (400, 80),
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
                # "location": (800, 195),
                "location": (scale_x(750, info), scale_y(210, info)),
                "size": (100, 40),

                "text": 
                {
                    "font" : pygame.font.SysFont("Arial",size=35),
                    "string": "Cho",
                    "foreground_color": BLACK,
                    "background_color": WHITE,
                    "hover_color": LIGHT_GREEN

                }
              },
            "han_button": 
            {
                # "location": (1010, 195),
                "location": (scale_x(1030, info), scale_y(210, info)),
                "size": (100, 40),
                "text": 
                {
                    "font" : pygame.font.SysFont("Arial",size=35),
                    "string": "Han",
                    "foreground_color": BLACK,
                    "background_color": WHITE,
                    "hover_color": LIGHT_GREEN

                }
            },
            "standard_piece_convention_button": 
            {
                # "location": (700, 455),
                "location": (scale_x(625, info), scale_y(475, info)),
                "size": (175, 50),
                "text": 
                {
                    "font" : pygame.font.SysFont("Arial",size=35),
                    "string": "Standard",
                    "foreground_color": BLACK,
                    "background_color": WHITE,
                    "hover_color": LIGHT_GREEN

                }
            },
            "internat_piece_convention_button": 
            {
                # "location": (1050, 455),
                "location": (scale_x(1075, info), scale_y(475, info)),
                "size": (175, 50),
                "text": 
                {
                    "font" : pygame.font.SysFont("Arial",size=30),
                    "string": "International",
                    "foreground_color": BLACK,
                    "background_color": WHITE,
                    "hover_color": LIGHT_GREEN

                }
            },
            "easy_ai_button": 
            {
                # "location": (700, 725),
                "location": (489, 520),
                "size": (100, 40),
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
                # "location": (900, 725),
                "location": (632, 520),
                "size": (100, 40),
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
                # "location": (1100, 725),
                "location": (775, 520),
                "size": (100, 40),
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
                # "location": (910, 895),
                "location": (1, scale_y(960, info)),
                "size": (100, 50),
                "text": 
                {
                    "font" : pygame.font.SysFont("Arial",size=35),
                    "string": "Play",
                    "foreground_color": BLACK,
                    "background_color": WHITE,
                    "hover_color": LIGHT_GREEN

                }
            },
            "swap_left_horse_button": 
            {
                    # "location": (610, 890),
                    "location": (325, scale_y(605, info)),
                    "size": (100, 50),
                    "text": 
                    {
                        "font" : pygame.font.SysFont("Arial",size=30),
                        "string": "Swap",
                        "foreground_color": BLACK,
                        "background_color": WHITE,
                        "hover_color": LIGHT_GREEN

                    }
            },
            "swap_right_horse_button": 
            {

                # "location": (1210, 890),
                "location": (1050, scale_y(605, info)),
                "size": (100, 50),
                "text": 
                {
                    "font" : pygame.font.SysFont("Arial",size=30),
                    "string": "Swap",
                    "foreground_color": BLACK,
                    "background_color": WHITE,
                    "hover_color": LIGHT_GREEN

                }
            },
            "confirm_swap_button": 
            {
                # "location": (910, 895),
                "location": (1, scale_y(550, info)),
                "size": (120, 50),
                "text": 
                {
                    "font" : pygame.font.SysFont("Arial",size=30),
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
                # "location": (800, 195),
                "location": (552, 140),
                "size": (80, 35),
                "text": 
                {
                    "font" : pygame.font.SysFont("Arial",size=30),
                    "string": "Cho",
                    "foreground_color": BLACK,
                    "background_color": WHITE,
                    "hover_color": LIGHT_GREEN

                }
            },
            "han_button": 
            {
                # "location": (1010, 195),
                "location": (732, 140),
                "size": (80, 35),
                "text": 
                {
                    "font" : pygame.font.SysFont("Arial",size=30),
                    "string": "Han",
                    "foreground_color": BLACK,
                    "background_color": WHITE,
                    "hover_color": LIGHT_GREEN

                }
            },
            "standard_piece_convention_button": 
            {
                # "location": (700, 455), 625 435
                "location": (477, 330),
                "size": (140, 40),
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
                # "location": (1050, 455), 1075 435
                "location": (745, 330),
                "size": (140, 40),
                "text": 
                {
                    # "font" : pygame.font.SysFont("Arial",size=35),
                    "font" : pygame.font.SysFont("Arial",size=25),
                    "string": "International",
                    "foreground_color": BLACK,
                    "background_color": WHITE,
                    "hover_color": LIGHT_GREEN

                }
            },
        
            "play_button": 
            {
                "location": (1, 665),
                "size": (90, 40),
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
                    # "location": (610, 890),
                    "location": (395, 420),
                    "size": (70, 35),
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

                # "location": (1210, 890),
                "location": (900, 420),
                "size": (70, 35),
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
                # "location": (910, 895),
                "location": (1, 403),
                "size": (96, 40),
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
                    # "location": (610, 135),
                    "location": (395, 345),
                    "size": (70, 35),
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

                # "location": (1210, 135),
                "location": (900, 345),
                "size": (70, 35),
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
                # "location": (910, 140),
                "location": (1, 403),
                "size": (96, 40),
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
            "menu_background_size": (700, 700)
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
                        # "location": (815, 100),
                        "location": (680, 384),
                        # "font_size": 35,
                        "font_size": 30,
                    },
                    # "location": (780, 75),
                    "location": (680, 75),
                    "size": (100, 25)
                },
                "piece_convention": 
                {
                    "text": 
                    {
                        "string" : "Select Piece Convention",
                        # "location": (800, 355),
                        "location": (eWidth // 2 - 185, scale_y(355, info)),
                        "font_size": 35,
                    },
                    # "location": (660, 300),
                    "location": (eWidth // 2 - 300, scale_y(300, info)),
                    "size": (3300, 125)
                },
                "ai_level": 
                {
                    "text": 
                    {
                        "string" : "Selected AI Difficulty: ",
                        # "location": (775, 625),
                        "location": (525, 455),
                        "font_size": 25,
                        "chosen_diff_location": (770, 455)
                    },
                    # "location": (660, 570),
                    "location": (455, 420),
                    "size": (600, 225)
                },
                "play": 
                {
                    # "location": (855, 815),
                    "location": (eWidth // 2 - 105, scale_y(840, info)),
                    "size": (210, 210)
                },
                "player_piece_display": 
                {
                    "text": 
                    {
                        "string" : "Your Pieces",
                        # "location": (430, 240),
                        "location": (289, 175),
                        "font_size": 25,
                    },
                    # "location": (410, 285),
                    "location": (278, 209),
                    "size": (200, 810),
                    "player_header" :
                    {
                        # "location": (410, 230),
                        "location": (278, 163),
                        "size": (60, 70)
                    }
                },
                "opponent_piece_display": 
                {
                    "text": 
                    {
                        # "location": (800, 100),
                        "location": (eWidth // 7 + 905, 140),
                        "font_size": 35,
                    },
                    # "location": (1310, 285),
                     "location": (935, 209),
                    "size": (200, 810)
                },
                "swap_left_horse": 
                {
                    # "location": (535, 865),
                    "location": (384, 407),
                    "size": (150, 100)
                },
                "swap_right_horse": 
                {
                    # "location": (1135, 865),
                    "location": (889, 407),
                    "size": (150, 100)
                },
                "confirm_swap":
                {
                    # "location": (855, 815),
                    "location": (605, 326),
                    "size": (210, 210)
                },
                "game_state":
                {
                    "location": (0, 240),
                    "size": (400, 200),
                    "bikjang":
                    {
                        "text":
                        {
                            "string": "Bikjang!",
                            "location": (90, 250),
                            "font_size": 75
                        },
                    },
                    "check":
                    {
                        "text":
                        {
                            "string": "Check!",
                            "location": (90, 250),
                            "font_size": 75
                        },
                    },
                    
                    "turn":
                    {
                        "location": (245, 385),
                        "font_size": 35
                    },
                },
                "game_over":
                {
                    # "location": (535, 380),
                    "location": (371, 360),
                    "size": (730, 250),
                    "notify_text":
                    {
                        # "location": (600, 440),
                        "location": (430, 420),
                        "font_size": 60
                    },
                    "condition_text":
                    {
                        # "location": (600, 560),
                        "location": (560, 555),
                        "font_size": 25
                    },
                    "result_text":
                    {
                        # "location": (1060, 440),
                        "location": (810, 420),
                        "font_size": 60
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
                        # "location": (815, 100),
                        "location": (557, 75),
                        # "font_size": 35,
                        "font_size": 25,
                    },
                    # "location": (780, 75),
                    "location": (532, 60),
                    "size": (300, 125)
                },
                "piece_convention": 
                {
                    "text": 
                    {
                        "string" : "Select Piece Convention",
                        # "location": (800, 355), 315 160
                        "location": (535, 260),
                        "font_size": 25,
                    },
                    # "location": (660, 300), 260
                    "location": (455, 230),
                    "size": (450, 150)
                },
                "play": 
                {
                    # "location" : (855, 815) 775
                    "location": (608, 590),
                    "size": (146, 146)
                },
                "player_piece_display": 
                {
                    "text": 
                    {
                        "string" : "Your Pieces",
                        # "location": (430, 240),
                        "location": (eWidth // 7 + 5, 140),
                        "font_size": 30,
                    },
                    # "location": (410, 285),
                    "location": (200, 225),
                    "size": (150, 587),
                    "player_header" :
                    {
                        # "location": (410, 230),
                        "location": (eWidth // 7 - 15, 130),
                        "size": (150, 75)
                    }
                },
                "opponent_piece_display": 
                {
                    "text": 
                    {
                        # "location": (800, 100),
                        "location": (eWidth // 7 + 905, 140),
                        "font_size": 35,
                    },
                    # "location": (1310, 285),
                    "location": (eWidth // 7 + 885, 225),
                    "size": (150, 589)
                },
                "host_swap_left_horse": 
                {
                    # "location": (535, 865),
                    "location": (384, 407),
                    "size": (90, 60)
                },
                "host_swap_right_horse": 
                {
                    # "location": (1135, 865),
                    "location": (889, 407),
                    "size": (90, 60)
                },
                "host_confirm_swap":
                {
                    # "location": (855, 815),
                    "location": (605, 326),
                    "size": (150, 150)
                },
                "guest_swap_left_horse": 
                {
                    # "location": (535, 0),
                    "location": (384, 332),
                    "size": (90, 60)
                },
                "guest_swap_right_horse": 
                {
                    # "location": (1135, 0),
                    "location": (889, 332),
                    "size": (90, 60)
                },
                "guest_confirm_swap":
                {
                    # "location": (855, 65),
                    "location": (605, 326),
                    "size": (150, 150)
                },
                "game_state":
                {
                    "location": (0, 240),
                    "size": (400, 200),
                    "bikjang":
                    {
                        "text":
                        {
                            "string": "Bikjang!",
                            "location": (90, 250),
                            "font_size": 75
                        },
                    },
                    "check":
                    {
                        "text":
                        {
                            "string": "Check!",
                            "location": (90, 250),
                            "font_size": 75
                        },
                    },
                    
                    "turn":
                    {
                        "location": (245, 385),
                        "font_size": 35
                    },
                },
                "game_over":
                {
                    # "location": (535, 380),
                    "location": (315, 275),
                    "size": (730, 250),
                    "notify_text":
                    {
                        # "location": (600, 440),
                        "location": (374, 335),
                        "font_size": 60
                    },
                    "condition_text":
                    {
                        # "location": (600, 560),
                        "location": (534, 470),
                        "font_size": 25
                    },
                    "result_text":
                    {
                        # "location": (1060, 440),
                        "location": (784, 335),
                        "font_size": 60
                    }
                }
                
            },
        }
    },
},
"1920x1080":
{
    "vertical_offset": 50,
    "board_border_size": (1080, 1080),
    "board_size": (960, 960),
    "x_board_start_loc": 447,
    "x_board_end_loc": 1552,
    "x_spacing": 119.77,
    "y_board_start_loc": 32.5,
    "y_board_end_loc": 960,
    "y_spacing": 106.4,
    "x_coordinates": [470, 584, 699, 814, 928, 1043, 1157, 1273, 1384],
    "y_coordinates": [53, 156, 258, 361, 463, 566, 669, 771, 874, 968],
    "piece_reformat_size": (32, 32),
    "spot_collision_size": (65, 65),
    "small_collision_size": (50, 50),
    "small_size": (65, 65),
    "med_collision_size": (75, 75),
    "med_size": (90,90),
    "large_collision_size": (105, 105),
    "large_size": (115,115),
    "buttons":
    {
        "main_menu" :
        {
            "single_player_button":
            {
                "location": (715, 275),
                "size": (500, 100),
                "text":
                {
                    "font" : pygame.font.SysFont("Arial",size=50),
                    "string": "Play Against an AI",
                    "foreground_color": BLACK,
                    "background_color": WHITE,
                    "hover_color": LIGHT_GREEN

                }
            },
            "local_multiplayer_button":
            {
                "location": (715, 410),
                "size": (500, 100),
                "text":
                {
                    "font" : pygame.font.SysFont("Arial",size=50),
                    "string": "Play by Yourself",
                    "foreground_color": BLACK,
                    "background_color": WHITE,
                    "hover_color": LIGHT_GREEN

                }
            },
            "multiplayer_button":
            {
                "location": (715, 545),
                "size": (500, 100),
                "text":
                {
                    "font" : pygame.font.SysFont("Arial",size=50),
                    "string": "Play Against a Friend",
                    "foreground_color": BLACK,
                    "background_color": WHITE,
                    "hover_color": LIGHT_GREEN

                }
            },
            "close_button":
            {
                "location": (715, 680),
                "size": (500, 100),
                "text":
                {
                    "font" : pygame.font.SysFont("Arial",size=50),
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
                "location": (800, 195),
                "size": (100, 40),
                "text":
                {
                    "font" : pygame.font.SysFont("Arial",size=35),
                    "string": "Cho",
                    "foreground_color": BLACK,
                    "background_color": WHITE,
                    "hover_color": LIGHT_GREEN

                }
              },
            "han_button":
            {
                "location": (1010, 195),
                "size": (100, 40),
                "text":
                {
                    "font" : pygame.font.SysFont("Arial",size=35),
                    "string": "Han",
                    "foreground_color": BLACK,
                    "background_color": WHITE,
                    "hover_color": LIGHT_GREEN

                }
            },
            "standard_piece_convention_button":
            {
                "location": (700, 455),
                "size": (175, 50),
                "text":
                {
                    "font" : pygame.font.SysFont("Arial",size=35),
                    "string": "Standard",
                    "foreground_color": BLACK,
                    "background_color": WHITE,
                    "hover_color": LIGHT_GREEN

                }
            },
            "internat_piece_convention_button":
            {
                "location": (1050, 455),
                "size": (175, 50),
                "text":
                {
                    "font" : pygame.font.SysFont("Arial",size=35),
                    "string": "International",
                    "foreground_color": BLACK,
                    "background_color": WHITE,
                    "hover_color": LIGHT_GREEN

                }
            },
            "easy_ai_button":
            {
                "location": (700, 715),
                "size": (125, 50),
                "text":
                {
                    "font" : pygame.font.SysFont("Arial",size=35),
                    "string": "Easy",
                    "foreground_color": BLACK,
                    "background_color": WHITE,
                    "hover_color": LIGHT_GREEN

                }
            },
            "medium_ai_button":
            {
                "location": (900, 715),
                "size": (125, 50),
                "text":
                {
                    "font" : pygame.font.SysFont("Arial",size=35),
                    "string": "Medium",
                    "foreground_color": BLACK,
                    "background_color": WHITE,
                    "hover_color": LIGHT_GREEN

                }
            },
            "hard_ai_button":
            {
                "location": (1100, 715),
                "size": (125, 50),
                "text":
                {
                    "font" : pygame.font.SysFont("Arial",size=35),
                    "string": "Hard",
                    "foreground_color": BLACK,
                    "background_color": WHITE,
                    "hover_color": LIGHT_GREEN

                }
            },
            "play_button":
            {
                "location": (910, 895),
                "size": (100, 50),
                "text":
                {
                    "font" : pygame.font.SysFont("Arial",size=35),
                    "string": "Play",
                    "foreground_color": BLACK,
                    "background_color": WHITE,
                    "hover_color": LIGHT_GREEN

                }
            },
            "swap_left_horse_button":
            {
                    "location": (610, 890),
                    "size": (100, 50),
                    "text":
                    {
                        "font" : pygame.font.SysFont("Arial",size=35),
                        "string": "Swap",
                        "foreground_color": BLACK,
                        "background_color": WHITE,
                        "hover_color": LIGHT_GREEN

                    }
            },
            "swap_right_horse_button":
            {

                "location": (1210, 890),
                "size": (100, 50),
                "text":
                {
                    "font" : pygame.font.SysFont("Arial",size=35),
                    "string": "Swap",
                    "foreground_color": BLACK,
                    "background_color": WHITE,
                    "hover_color": LIGHT_GREEN

                }
            },
            "confirm_swap_button":
            {
                "location": (910, 895),
                "size": (100, 50),
                "text":
                {
                    "font" : pygame.font.SysFont("Arial",size=35),
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
                "location": (800, 195),
                "size": (100, 40),
                "text":
                {
                    "font" : pygame.font.SysFont("Arial",size=35),
                    "string": "Cho",
                    "foreground_color": BLACK,
                    "background_color": WHITE,
                    "hover_color": LIGHT_GREEN

                }
            },
            "han_button":
            {
                "location": (1010, 195),
                "size": (100, 40),
                "text":
                {
                    "font" : pygame.font.SysFont("Arial",size=35),
                    "string": "Han",
                    "foreground_color": BLACK,
                    "background_color": WHITE,
                    "hover_color": LIGHT_GREEN

                }
            },
            "standard_piece_convention_button":
            {
                "location": (700, 445),
                "size": (175, 50),
                "text":
                {
                    "font" : pygame.font.SysFont("Arial",size=35),
                    "string": "Standard",
                    "foreground_color": BLACK,
                    "background_color": WHITE,
                    "hover_color": LIGHT_GREEN

                }
            },
            "internat_piece_convention_button":
            {
                "location": (1050, 445),
                "size": (175, 50),
                "text":
                {
                    # "font" : pygame.font.SysFont("Arial",size=35),
                    "font" : pygame.font.SysFont("Arial",size=30),
                    "string": "International",
                    "foreground_color": BLACK,
                    "background_color": WHITE,
                    "hover_color": LIGHT_GREEN

                }
            },

            "play_button":
            {
                # "location": (900, 895),
                "location": (1, 900),
                "size": (125, 50),
                "text":
                {
                    "font" : pygame.font.SysFont("Arial",size=35),
                    "string": "Play",
                    "foreground_color": BLACK,
                    "background_color": WHITE,
                    "hover_color": LIGHT_GREEN

                }
            },
            "host_swap_left_horse_button":
            {
                    "location": (570, 585),
                    "size": (100, 50),
                    "text":
                    {
                        "font" : pygame.font.SysFont("Arial",size=35),
                        "string": "Swap",
                        "foreground_color": BLACK,
                        "background_color": WHITE,
                        "hover_color": LIGHT_GREEN

                    }
            },
            "host_swap_right_horse_button":
            {

                "location": (1260, 585),
                "size": (100, 50),
                "text":
                {
                    "font" : pygame.font.SysFont("Arial",size=35),
                    "string": "Swap",
                    "foreground_color": BLACK,
                    "background_color": WHITE,
                    "hover_color": LIGHT_GREEN

                }
            },
            "host_confirm_swap_button":
            {
                "location": (895, 520),
                "size": (130, 50),
                "text":
                {
                    "font" : pygame.font.SysFont("Arial",size=35),
                    "string": "Confirm",
                    "foreground_color": BLACK,
                    "background_color": WHITE,
                    "hover_color": LIGHT_GREEN

                }
            },
            "guest_swap_left_horse_button":
            {
                    "location": (570, 465),
                    "size": (100, 50),
                    "text":
                    {
                        "font" : pygame.font.SysFont("Arial",size=35),
                        "string": "Swap",
                        "foreground_color": BLACK,
                        "background_color": WHITE,
                        "hover_color": LIGHT_GREEN

                    }
            },
            "guest_swap_right_horse_button":
            {

                "location": (1260, 465),
                "size": (100, 50),
                "text":
                {
                    "font" : pygame.font.SysFont("Arial",size=35),
                    "string": "Swap",
                    "foreground_color": BLACK,
                    "background_color": WHITE,
                    "hover_color": LIGHT_GREEN

                }
            },
            "guest_confirm_swap_button":
            {
                "location": (895, 520),
                "size": (130, 50),
                "text":
                {
                    "font" : pygame.font.SysFont("Arial",size=35),
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
            "menu_background_size": (920, 920)
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
                        "location": (815, 100),
                        "font_size": 35,
                    },
                    "location": (780, 75),
                    "size": (350, 175)
                },
                "piece_convention":
                {
                    "text":
                    {
                        "string" : "Select Piece Convention",
                        "location": (800, 355),
                        "font_size": 35,
                    },
                    "location": (660, 300),
                    "size": (600, 225)
                },
                "ai_level":
                {
                    "text":
                    {
                        "string" : "Selected AI Difficulty:",
                        "location": (735, 615),
                        "font_size": 35,
                        "chosen_diff_location": (1075, 615)
                    },
                    "location": (660, 560),
                    "size": (600, 225)
                },
                "play":
                {
                    "location": (855, 815),
                    "size": (210, 210)
                },
                "player_piece_display":
                {
                    "text":
                    {
                        "string" : "Your Pieces",
                        "location": (420, 240),
                        "font_size": 35,
                    },
                    "location": (410, 285),
                    "size": (200, 810),
                    "player_header" :
                    {
                        "location": (410, 230),
                        "size": (200, 100)
                    }
                },
                "opponent_piece_display":
                {
                    "text":
                    {
                        "location": (800, 100),
                        "font_size": 35,
                    },
                    "location": (1310, 285),
                    "size": (200, 810)
                },
                "swap_left_horse":
                {
                    "location": (550, 560),
                    "size": (140, 100)
                },
                "swap_right_horse":
                {
                    "location": (1239, 560),
                    "size": (140, 100)
                },
                "confirm_swap":
                {
                    "location": (860, 444),
                    "size": (200, 200)
                },
                "game_state":
                {
                    "location": (0, 240),
                    "size": (400, 200),
                    "bikjang":
                    {
                        "text":
                        {
                            "string": "Bikjang!",
                            "location": (90, 250),
                            "font_size": 75
                        },
                    },
                    "check":
                    {
                        "text":
                        {
                            "string": "Check!",
                            "location": (90, 250),
                            "font_size": 75
                        },
                    },

                    "turn":
                    {
                        "location": (245, 385),
                        "font_size": 35
                    },
                },
                "game_over":
                {
                    "location": (535, 380),
                    "size": (850, 250),
                    "notify_text":
                    {
                        "location": (600, 440),
                        "font_size": 60
                    },
                    "condition_text":
                    {
                        "location": (600, 560),
                        "font_size": 45
                    },
                    "result_text":
                    {
                        "location": (1060, 440),
                        "font_size": 60
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
                        "location": (810, 100),
                        "font_size": 30,
                    },
                    "location": (780, 75),
                    "size": (350, 175)
                },
                "piece_convention":
                {
                    "text":
                    {
                        "string" : "Select Piece Convention",
                        "location": (775, 345),
                        "font_size": 35,
                    },
                    "location": (660, 290),
                    "size": (600, 225)
                },
                "play":
                {
                    "location": (860, 800),
                    "size": (200, 200)
                },
                "player_piece_display":
                {
                    "text":
                    {
                        "string" : "Your Pieces",
                        "location": (430, 240),
                        "font_size": 35,
                    },
                    "location": (410, 285),
                    "size": (200, 810),
                    "player_header" :
                    {
                        "location": (410, 230),
                        "size": (200, 100)
                    }
                },
                "opponent_piece_display":
                {
                    "text":
                    {
                        "location": (800, 100),
                        "font_size": 35,
                    },
                    "location": (1310, 285),
                    "size": (200, 810)
                },
                "host_swap_left_horse":
                {
                    "location": (550, 560),
                    "size": (140, 100)
                },
                "host_swap_right_horse":
                {
                    "location": (1239, 560),
                    "size": (140, 100)
                },
                "host_confirm_swap":
                {
                    "location": (860, 444),
                    "size": (200, 200)
                },
                "guest_swap_left_horse":
                {
                    "location": (550, 440),
                    "size": (140, 100)
                },
                "guest_swap_right_horse":
                {
                    "location": (1239, 440),
                    "size": (140, 100)
                },
                "guest_confirm_swap":
                {
                    "location": (860, 444),
                    "size": (200, 200)
                },
                "game_state":
                {
                    "location": (0, 240),
                    "size": (400, 200),
                    "bikjang":
                    {
                        "text":
                        {
                            "string": "Bikjang!",
                            "location": (90, 250),
                            "font_size": 75
                        },
                    },
                    "check":
                    {
                        "text":
                        {
                            "string": "Check!",
                            "location": (90, 250),
                            "font_size": 75
                        },
                    },

                    "turn":
                    {
                        "location": (245, 385),
                        "font_size": 35
                    },
                },
                "game_over":
                {
                    "location": (535, 380),
                    "size": (850, 250),
                    "notify_text":
                    {
                        "location": (655, 440),
                        "font_size": 60
                    },
                    "condition_text":
                    {
                        "location": (650, 560),
                        "font_size": 45
                    },
                    "result_text":
                    {
                        "location": (1040, 440),
                        "font_size": 60
                    }
                }

            },
        }
    },
}

}


# flag for app run loop
running = True

# flag for AI difficulty
stored_difficulty = "Easy"

# set window variables for GUI elements
vertical_offset = None
board_border_size = None
board_size = None
x_board_start_loc = None
x_board_end_loc = None
x_spacing = None
y_board_start_loc = None
y_board_end_loc = None
y_spacing = None
spot_collision_size = None
small_collision_size = None
small_size = None
med_collision_size = None
med_size = None
large_collision_size = None
large_size = None
x_coords = None
y_coords = None

x_coordinates = None
y_coordinates = None

# possible settings for checking if a settings pre-set file is correctly written
possible_colorside = ("Cho", "Han")
possible_piece_convention = ("Standard", "International")
possible_ai_level = ("Easy", "Medium", "Hard")

def get_resolution_config(res):
    """
    Returns the configuration dictionary for the given resolution.
    Defaults to the configuration for "1360x796".
    """
    return resolutions.get(res, resolutions["1360x796"])

def initialize_constants(config):
    """
    Updates global resolution-dependent constants using the provided config dictionary.
    This function sets the global values which will be used elsewhere in your program.
    """
    global vertical_offset, board_border_size, board_size
    global x_board_start_loc, x_board_end_loc, x_spacing
    global y_board_start_loc, y_board_end_loc, y_spacing
    global spot_collision_size, small_collision_size, small_size
    global med_collision_size, med_size, large_collision_size, large_size
    global x_coords, y_coords, x_coordinates, y_coordinates

    vertical_offset = config["vertical_offset"]
    board_border_size = config["board_border_size"]
    board_size = config["board_size"]
    x_board_start_loc = config["x_board_start_loc"]
    x_board_end_loc = config["x_board_end_loc"]
    x_spacing = config["x_spacing"]
    y_board_start_loc = config["y_board_start_loc"]
    y_board_end_loc = config["y_board_end_loc"]
    y_spacing = config["y_spacing"]
    spot_collision_size = config["spot_collision_size"]
    small_collision_size = config["small_collision_size"]
    small_size = config["small_size"]
    med_collision_size = config["med_collision_size"]
    med_size = config["med_size"]
    large_collision_size = config["large_collision_size"]
    large_size = config["large_size"]
    x_coords = config["x_coordinates"]
    y_coords = config["y_coordinates"]
    x_coordinates = [coordinate for coordinate in x_coords]
    y_coordinates = [coordinate for coordinate in y_coords]
