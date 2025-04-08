"""
----------------------button.py----------------------------
o This file is to manage the button class for the button
    objects for player to interact with
o Last Modified - November 11th 2024
----------------------------------------------------------
"""
import pygame

# local file imports, see individ file for details
import constants

# Button class for base construction of a general button to be interacted with
class Button:

    # Class Initializer
	# INPUT: x: x location on window
    #        y: y location on window
    #       width: width of button
    #       height: height of button
    #       font: text font for text inside button
    #       text: string text inside button
    #       foreground_color: text color on button
    #       background_color: button color
    #       hover_color: button color change when mouse collides with button
	# OUTPUT: button is created 
    def __init__(self, x, y, width, height, font, text="", foreground_color=constants.WHITE, background_color=constants.BLACK, hover_color=constants.LIGHT_GREEN):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.font = font
        self.text = text
        self.foreground_color = foreground_color
        self.background_color = background_color
        self.hover_color = hover_color
        self.rect = pygame.Rect(x, y, width, height) # collision rect
        self.clicked = False # event trigger

    # Method to draw the created button to the window object
	# INPUT: pygame surface object (window)
	# OUTPUT: Button is drawn to surface object, and will update button color if mouse collides with
    def draw_button(self, window):
	center = False
        mouse_pos = pygame.mouse.get_pos()
        # change to hovering color if mouse hovers over button
        if self.rect.collidepoint(mouse_pos):
            color = self.hover_color if self.hover_color else self.background_color
        else:
            color = self.background_color

        # if x is set to 1, button should be in the center of the screen
        if self.x == 1:
            self.rect.center = window.get_rect().center
            self.rect.centery = self.y
            newx = self.rect.centerx
            center = True
	
        pygame.draw.rect(window, color, self.rect)

        # dont display text in the button if button has no text
        if self.text !="":
            # render text
            text_surface = self.font.render(self.text, True, self.foreground_color)
            # center text onto button
            text_rect = text_surface.get_rect(center=(self.x + self.width / 2, self.y + self.height / 2))
            window.blit(text_surface, text_rect)

    # Method to determine if a button was clicked
	# INPUT: No input
	# OUTPUT: Boolean True returned if button was clicked
    def is_clicked(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0] == 1:
            return True
        
# Function to create the buttons in mass for the ai level setting
# INPUT: No input
# OUTPUT: list of the ai levels is created (0 --> 9)
def create_ai_level_buttons():
    ai_level_buttons = []
    ai_level = ("Easy", "Medium", "Hard")

    font = pygame.font.SysFont("Arial", 35)

    # 3 buttons
    for i in range(3):
        new_button = Button(x=(750 + (150*i)),y=645,width=125,height=50, 
													font=font,
													text=f"{ai_level[i]}", 
													foreground_color = constants.BLACK,
													background_color = constants.WHITE,
													hover_color = constants.LIGHT_GREEN)
        ai_level_buttons.append(new_button)
        
    return ai_level_buttons
