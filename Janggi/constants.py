"""
----------------------constants.py--------------------------------
o This file is to hold any global constants to be used by program
o Place all global constants into here
o Last Modified - April 8th 2025
------------------------------------------------------------------
"""
import pygame

# initialize pygame instance
pygame.init()

screen_height, screen_width = 0,0

# rectangle colors
WHITE = (255,255,255)
BLACK = (0,0,0)
GREY = (100,100,100)
RED = (200,16,46)
BLUE = (0,47,108)
GREEN = (30,100,0)
LIGHT_GREEN = (35,200,0)

# UI mapping for resolution sizes
# 1920x1080 -> Supported
# 1360x796 -> Supported

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
            "x_coordinates": [312, 395, 478, 565, 647, 733, 817, 900, 983],
            "y_coordinates": [29, 108, 180, 257, 332, 407, 483, 560, 634, 700],
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
                            "easy_ai_button":
                                {
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
                                }
                        },
                    "local_MP" :
                        {
                            "cho_button":
                                {
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
                                    "location": (745, 330),
                                    "size": (140, 40),
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
                                    "ai_level":
                                        {
                                            "text":
                                                {
                                                    "string" : "Selected AI Difficulty: ",
                                                    "location": (525, 455),
                                                    "font_size": 25,
                                                    "chosen_diff_location": (770, 455)
                                                },
                                            "location": (455, 420),
                                        },
                                    "player_piece_display":
                                        {
                                            "text":
                                                {
                                                    "string" : "Your Pieces",
                                                    "location": (289, 175),
                                                    "font_size": 25,
                                                },
                                            "location": (278, 209),
                                            "player_header" :
                                                {
                                                    "location": (278, 163),
                                                    "size": (60, 70)
                                                }
                                        },
                                    "opponent_piece_display":
                                        {
                                            "location": (935, 209)
                                        },
                                    "swap_left_horse":
                                        {
                                            "location": (384, 407)
                                        },
                                    "swap_right_horse":
                                        {
                                            "location": (889, 407)
                                        },
                                    "confirm_swap":
                                        {
                                            "location": (605, 326)
                                        },
                                    "game_state":
                                        {
                                            "size": (400, 200)
                                        },
                                    "game_over":
                                        {
                                            "size": (730, 250),
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
                                                    "location": (557, 75),
                                                    "font_size": 25,
                                                },
                                            "location": (532, 60),
                                            "size": (300, 125)
                                        },
                                    "piece_convention":
                                        {
                                            "text":
                                                {
                                                    "string" : "Select Piece Convention",
                                                    "location": (535, 260),
                                                    "font_size": 25,
                                                },
                                            "location": (455, 230),
                                            "size": (450, 150)
                                        },
                                    "play":
                                        {
                                            "location": (608, 590),
                                            "size": (146, 146)
                                        },
                                    "player_piece_display":
                                        {
                                            "size": (150, 587),
                                            "player_header" :
                                                {
                                                    "size": (150, 75)
                                                }
                                        },
                                    "opponent_piece_display":
                                        {
                                            "size": (150, 589)
                                        },
                                    "host_swap_left_horse":
                                        {
                                            "location": (384, 407),
                                            "size": (90, 60)
                                        },
                                    "host_swap_right_horse":
                                        {
                                            "location": (889, 407),
                                            "size": (90, 60)
                                        },
                                    "host_confirm_swap":
                                        {
                                            "location": (605, 326),
                                            "size": (150, 150)
                                        },
                                    "guest_swap_left_horse":
                                        {
                                            "location": (384, 332),
                                            "size": (90, 60)
                                        },
                                    "guest_swap_right_horse":
                                        {
                                            "location": (889, 332),
                                            "size": (90, 60)
                                        },
                                    "guest_confirm_swap":
                                        {
                                            "location": (605, 326),
                                            "size": (150, 150)
                                        },
                                    "game_state":
                                        {
                                            "size": (400, 200)
                                        },
                                    "game_over":
                                        {
                                            "location": (315, 275),
                                            "size": (730, 250),
                                            "notify_text":
                                                {
                                                    "location": (374, 335),
                                                    "font_size": 60
                                                },
                                            "condition_text":
                                                {
                                                    "location": (534, 470),
                                                    "font_size": 25
                                                },
                                            "result_text":
                                                {
                                                    "location": (784, 335),
                                                    "font_size": 60
                                                }
                                        }

                                }
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
                                    "location": (1, 330),
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
                                    "location": (1, 470),
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
                                    "location": (1, 610),
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
                                    "location": (1, 750),
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
                                }
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
                                            "font" : pygame.font.SysFont("Arial",size=30),
                                            "string": "International",
                                            "foreground_color": BLACK,
                                            "background_color": WHITE,
                                            "hover_color": LIGHT_GREEN

                                        }
                                },

                            "play_button":
                                {
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
                                            "font": pygame.font.SysFont("Arial", size=35),
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
                                            "font": pygame.font.SysFont("Arial", size=35),
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
                                            "font": pygame.font.SysFont("Arial", size=35),
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
                                            "font": pygame.font.SysFont("Arial", size=35),
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
                                            "font": pygame.font.SysFont("Arial", size=35),
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
                            "button_background":
                                {
                                    "ai_level":
                                        {
                                            "text":
                                                {
                                                    "string": "Selected AI Difficulty:",
                                                    "location": (735, 615),
                                                    "font_size": 35,
                                                    "chosen_diff_location": (1075, 615)
                                                },
                                            "location": (660, 560)
                                        },
                                    "player_piece_display":
                                        {
                                            "text":
                                                {
                                                    "string": "Your Pieces",
                                                    "location": (420, 240),
                                                    "font_size": 35,
                                                },
                                            "location": (410, 285),
                                            "player_header":
                                                {
                                                    "location": (410, 230),
                                                    "size": (200, 100),
                                                }
                                        },
                                    "opponent_piece_display":
                                        {
                                            "location": (1310, 285)
                                        },
                                    "swap_left_horse":
                                        {
                                            "location": (550, 560)
                                        },
                                    "swap_right_horse":
                                        {
                                            "location": (1239, 560)
                                        },
                                    "confirm_swap":
                                        {
                                            "location": (860, 444)
                                        },
                                    "game_state":
                                        {
                                            "size": (400, 200)
                                        },
                                    "game_over":
                                        {
                                            "size": (850, 250)
                                        }
                                }
                        },
                    "local_MP":
                        {
                            "button_background":
                                {
                                    "play_as":
                                        {
                                            "text":
                                                {
                                                    "string": "Select Side to Play As",
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
                                                    "string": "Select Piece Convention",
                                                    "location": (775, 345),
                                                    "font_size": 35,
                                                },
                                            "location": (660, 290),
                                            "size": (600, 225)
                                        },
                                    "play":
                                        {
                                            "location": (860, 800),
                                            "size": (200, 200),
                                        },
                                    "player_piece_display":
                                        {
                                            "size": (200, 810),
                                            "player_header":
                                                {
                                                    "size": (200, 100)
                                                }
                                        },
                                    "opponent_piece_display":
                                        {
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
                                            "size": (400, 200)
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
