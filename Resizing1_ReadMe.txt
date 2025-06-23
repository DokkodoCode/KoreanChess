Just a heads up, this branch is older than what is in the main branch. (No multiplayer)

The main thing that needs to be adjusted in this is getting the font to resize and getting peices to relocate properly when resized during a game.

This branch has made change to main.py, constants.py, state.py, button.py, and piece.py

main.py
    -added functions: get_scaling_factors(), scale_everything(), scale_resolutions(), and print_resolutions()

        *get_scaling_factors(current_width, current_height): gets the scaling factors to use to scale object variables 

        *scale_everything(): scale objects outside the resolutions dictionary in constants.py

        *scale_resolutions(resolutions, scale_w, scale_h): scales objects in the resolutions dictionary

        *print_resolutions(resolutions, indent=0): prints out all values of the values in the resolutions dictionary

    -added variables window_width and window_height that hold the dimensions of the game window
    -added calls to functions in while constants.running loop in the elif that looks for a resizing event
    -added calls to resize and render to reload objects with new values

constants.py 
    -overhaul of reslutions dictionary to reduce repetitiveness
    -added REFERENCE_WIDTH, REFERENCE_HEIGHT, window_size, scale_w, and scale_h
        *REFERENCE_WIDTH and REFERENCE_HEIGHT: used to hold previous window size to help calculate scale factors
        *window_size: holds current window size
        *scale_w and scale_h: used to scale objects

state.py
    -added resize function to help reload sizes of objects (not implemented to all classes)

button.py
    -added border_radius for buttons to give them rounded corners

piece.py
    -added update_pieece_positions() to reload new piece locations (updates piece loactions if resized before pressing play but doesn't update when resized during game)