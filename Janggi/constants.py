"""
----------------------constants.py--------------------------------
o This file is to hold any global constants to be used by program
o Place all global constants into here
o Last Modified - November 19th 2024
------------------------------------------------------------------
"""
import pygame

from helper_funcs import scale_x, scale_y, is_fullscr


# initialize pygame instance
pygame.init()


info = pygame.display.Info()
eWidth, eHeight = info.current_w, info.current_h

# if f"{eWidth}x{eHeight}" == "1920x1080":
#     screen_width, screen_height = 1920, 1080
# else:
#     screen_width, screen_height = 111, 111

screen_width, screen_height = is_fullscr(eWidth, eHeight)
print(screen_width, screen_height)

# rectangle colors
WHITE = (255,255,255)
BLACK = (0,0,0)
GREY = (100,100,100)
RED = (200,16,46)
BLUE = (0,47,108,)
GREEN = (30,100,0)
LIGHT_GREEN = (35,200,0)

# UI mapping for resolution sizes

# 111x111 -> MAC/Resize

# 1920x1080 -> Supported
# 1440x900 -> Supported
# 680x480 -> In Developement
resolutions = {

    "111x111":
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
        # "x_coordinates": [448, 568, 688, 808, 928, 1047, 1168, 1288, 1406],
        "x_coordinates": [eWidth // 7 + 20, 568, 688, 808, 928, 1047, 1168, 1288, eWidth // 7 + 985],
        # "y_coordinates": [29, 136.5, 245, 352, 460, 567, 675, 782, 890, 987],
        "y_coordinates": [29, 136.5, 245, 252, 360, 467, 575, 682, 790, 887],
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
                    # "location": (715, 275),
                    "location": (1, scale_y(325, info)),
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
                    # "location": (715, 425),
                    "location": (1, scale_y(475, info)),
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
                    # "location": (715, 570),
                    "location": (1, scale_y(620, info)),
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
                    # "location": (715, 720),
                    "location": (1, scale_y(770, info)),
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
                    "location": (700, 725),
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
                    "location": (900, 725),
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
                    "location": (1100, 725),
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
                    # "location": (700, 455), 625 435
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
                    # "location": (1050, 455), 1075 435
                    "location": (scale_x(1075, info), scale_y(475, info)),
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
                    "location": (1, scale_y(935, info)),
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
                "host_swap_right_horse_button": 
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
                "host_confirm_swap_button": 
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
                "guest_swap_left_horse_button": 
                {
                        "location": (610, 135),
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

                    "location": (1210, 135),
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
                    "location": (910, 140),
                    "size": (100, 60),
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
                "menu_background_size": (1000, 1000) 
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
                            "location": (775, 625),
                            "font_size": 35,
                            "chosen_diff_location": (1050, 625)
                        },
                        "location": (660, 570),
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
                    "swap_left_horse": 
                    {
                        "location": (535, 865),
                        "size": (250, 210)
                    },
                    "swap_right_horse": 
                    {
                        "location": (1135, 865),
                        "size": (250, 210)
                    },
                    "confirm_swap":
                    {
                        "location": (855, 815),
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
                            # "location": (815, 100),
                            "location": (eWidth // 2 - 155, scale_y(100, info)),
                            # "font_size": 35,
                            "font_size": 30,
                        },
                        # "location": (780, 75),
                        "location": (eWidth // 2 - 180, scale_y(75, info)),
                        "size": (350, 175)
                    },
                    "piece_convention": 
                    {
                        "text": 
                        {
                            "string" : "Select Piece Convention",
                            # "location": (800, 355), 315
                            "location": (eWidth // 2 - 165, scale_y(355, info)),
                            "font_size": 35,
                        },
                        # "location": (660, 300), 260
                        "location": (eWidth // 2 - 300, scale_y(300, info)),
                        "size": (600, 225)
                    },
                    "play": 
                    {
                        # "location" : (855, 815) 775
                        "location": (eWidth // 2 - 105, scale_y(815, info)),
                        "size": (210, 210)
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
                        "location": (eWidth // 7 - 15, 185),
                        "size": (200, 810),
                        "player_header" :
                        {
                            # "location": (410, 230),
                            "location": (eWidth // 7 - 15, 130),
                            "size": (200, 100)
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
                        "location": (eWidth // 7 + 885, 185),
                        "size": (200, 810)
                    },
                    "host_swap_left_horse": 
                    {
                        "location": (535, 865),
                        "size": (250, 210)
                    },
                    "host_swap_right_horse": 
                    {
                        "location": (1135, 865),
                        "size": (250, 210)
                    },
                    "host_confirm_swap":
                    {
                        "location": (855, 815),
                        "size": (210, 210)
                    },
                    "guest_swap_left_horse": 
                    {
                        "location": (535, 0),
                        "size": (250, 210)
                    },
                    "guest_swap_right_horse": 
                    {
                        "location": (1135, 0),
                        "size": (250, 210)
                    },
                    "guest_confirm_swap":
                    {
                        "location": (855, 65),
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
        "x_coordinates": [448, 568, 688, 808, 928, 1047, 1168, 1288, 1406],
        "y_coordinates": [29, 136.5, 245, 352, 460, 567, 675, 782, 890, 987],
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
                    # "location": (715, 275),
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
                    # "location": (715, 425),
                    "location": (715, 475),
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
                    # "location": (715, 570),
                    "location": (715, 620),
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
                    # "location": (715, 720),
                    "location": (715, 770),
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
                    "location": (700, 725),
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
                    "location": (900, 725),
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
                    "location": (1100, 725),
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
                    "location": (900, 900),
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
                "host_swap_right_horse_button": 
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
                "host_confirm_swap_button": 
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
                "guest_swap_left_horse_button": 
                {
                        "location": (610, 135),
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

                    "location": (1210, 135),
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
                    "location": (910, 140),
                    "size": (100, 60),
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
                "menu_background_size": (1000, 1000) 
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
                            "location": (775, 625),
                            "font_size": 35,
                            "chosen_diff_location": (1050, 625)
                        },
                        "location": (660, 570),
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
                    "swap_left_horse": 
                    {
                        "location": (535, 865),
                        "size": (250, 210)
                    },
                    "swap_right_horse": 
                    {
                        "location": (1135, 865),
                        "size": (250, 210)
                    },
                    "confirm_swap":
                    {
                        "location": (855, 815),
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
                        "location": (535, 865),
                        "size": (250, 210)
                    },
                    "host_swap_right_horse": 
                    {
                        "location": (1135, 865),
                        "size": (250, 210)
                    },
                    "host_confirm_swap":
                    {
                        "location": (855, 815),
                        "size": (210, 210)
                    },
                    "guest_swap_left_horse": 
                    {
                        "location": (535, 0),
                        "size": (250, 210)
                    },
                    "guest_swap_right_horse": 
                    {
                        "location": (1135, 0),
                        "size": (250, 210)
                    },
                    "guest_confirm_swap":
                    {
                        "location": (855, 65),
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
                    
                },
            }
        },
    },
    "1440x900": {
        "vertical_offset": 0,
        "board_border_size": (900, 900),
        "board_size": (800, 800),
        "x_board_start_loc": 362,
        "x_board_end_loc": 1273,
        "x_spacing": 104.33,
        "y_board_start_loc": 5,
        "y_board_end_loc": 835,
        "y_spacing": 92.22,
        "x_coordinates": [368, 468, 568, 668, 768, 868, 968, 1068, 1168],
        "y_coordinates": [19, 109, 199, 289, 379, 469, 558, 648, 737, 818],
        "spot_collision_size": (50, 50),
        "small_collision_size": (50, 50),
        "small_size": (50, 50),
        "med_collision_size": (60, 60),
        "med_size": (70,70),
        "large_collision_size": (80, 80),
        "large_size": (90,90),
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
    },
    
    "640x480": {
        "vertical_offset": 15,
        "board_border_size": (640, 640),
        "board_size": (540, 540),
        "x_board_start_loc": 88,
        "x_board_end_loc": 716,
        "x_spacing": 69.78,
        "y_board_start_loc": -8,
        "y_board_end_loc": 558,
        "y_spacing": 62,
        "x_coordinates": [98, 166, 233, 301, 368, 436, 503.5, 571, 637],
        "y_coordinates": [0, 60, 120, 181, 241, 301, 362, 422, 483, 538],
        "spot_collision_size": (30, 30),
        "small_collision_size": (35, 35),
        "small_size": (35, 35),
        "med_collision_size": (50, 50),
        "med_size": (50,50),
        "large_collision_size": (70, 70),
        "large_size": (70,70),
    }    
}

# flag for app run loop
running = True

# create window size based on user's machine
info = pygame.display.Info()

# set window sizes based on user's machine

# screen_width, screen_height = info.current_w, info.current_h
screen_width, screen_height = 1920, 1080
#screen_width, screen_height = info.current_w, info.current_h
#screen_width, screen_height = 111, 111

#screen_width, screen_height = 1440, 900

#screen_width, screen_height = info.current_w, info.current_h
#screen_width, screen_height = 1920, 1080
#screen_width, screen_height = 1440, 900

#screen_width, screen_height = 640, 480

# set window variables ofr GUI elements
vertical_offset = resolutions[f"{screen_width}x{screen_height}"]["vertical_offset"]
board_border_size = resolutions[f"{screen_width}x{screen_height}"]["board_border_size"]
board_size = resolutions[f"{screen_width}x{screen_height}"]["board_size"]
x_board_start_loc = resolutions[f"{screen_width}x{screen_height}"]["x_board_start_loc"]
x_board_end_loc = resolutions[f"{screen_width}x{screen_height}"]["x_board_end_loc"]
x_spacing = resolutions[f"{screen_width}x{screen_height}"]["x_spacing"]
y_board_start_loc = resolutions[f"{screen_width}x{screen_height}"]["y_board_start_loc"]
y_board_end_loc = resolutions[f"{screen_width}x{screen_height}"]["y_board_end_loc"]
y_spacing = resolutions[f"{screen_width}x{screen_height}"]["y_spacing"]
spot_collision_size = resolutions[f"{screen_width}x{screen_height}"]["spot_collision_size"]
small_collision_size = resolutions[f"{screen_width}x{screen_height}"]["small_collision_size"]
small_size = resolutions[f"{screen_width}x{screen_height}"]["small_size"]
med_collision_size = resolutions[f"{screen_width}x{screen_height}"]["med_collision_size"]
med_size = resolutions[f"{screen_width}x{screen_height}"]["med_size"]
large_collision_size = resolutions[f"{screen_width}x{screen_height}"]["large_collision_size"]
large_size = resolutions[f"{screen_width}x{screen_height}"]["large_size"]

x_coords = resolutions[f"{screen_width}x{screen_height}"]["x_coordinates"]
y_coords = resolutions[f"{screen_width}x{screen_height}"]["y_coordinates"]

x_coordinates = [coordinate for coordinate in x_coords]
y_coordinates = [coordinate for coordinate in y_coords]

# possible settings for checking if a settings pre-set file is correctly written
possible_colorside = ("Cho", "Han")
possible_piece_convention = ("Standard", "International")
possible_ai_level = ("Easy", "Medium", "Hard")