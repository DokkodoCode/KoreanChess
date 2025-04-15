# Korean Chess Program

## Overview

This project is a Korean chess program that supports multiple game modes, including single-player (against AI) and local multiplayer. The program uses Pygame for its graphical user interface. UI elements such as buttons, boards, and backgrounds scale dynamically relative to the window size based on a base resolution (1920×1080).

## Completed Features

- **Dynamic UI Scaling (Main Menu & Pregame)**
  - **Main Menu:** All major buttons (single-player, local multiplayer, multiplayer, and exit) are dynamically resized and repositioned when the window is resized.
  - **Pregame Settings:** Color selection, piece convention, and AI level buttons dynamically adjust their size, position, and font based on the window dimensions.
  
- **Piece Rendering**
  - Pieces are rendered using scaled positions based on stored base values (using the 1920×1080 base configuration).
  - Piece objects store their base (original) image locations and collision sizes, and these are updated when the window is resized.

## Known Issues

1. **Bounding Box (Collision Rectangle) Scaling**
   - Although the piece images are scaled correctly, the bounding boxes used for click detection (the collision rectangles) are not being updated reliably after the window is resized.
   - This leads to a discrepancy where the rendered piece and its clickable area do not align perfectly, causing the player to sometimes click in the wrong area.

2. **Window Resizing Limitations During Gameplay**
   - Currently, the game supports window resizing only in the main menu.
   - If the window is resized during gameplay, the UI does not update accordingly until the user returns to the main menu.

## Future Work

- **Fix Collision Rectangle Scaling**
  - Adjust the update logic for piece collision rectangles so that they scale in sync with the rendered piece images.
  
- **Universal Window Resizing**
  - Extend the resizing functionality to work in all game states, not just in the main menu.
  - Ensure the UI updates immediately when the window is resized during gameplay.

## Usage

1. **Launching the Program**
   - Run the program from the main entry point. The main menu will load and display all UI elements scaled based on your current window dimensions.
   
2. **Resizing the Window**
   - Resize the window at the main menu to see the UI elements adjust in size and position.
   - **Note:** If you change the window size during gameplay, the UI will not update until you return to the main menu.

3. **Game Interaction**
   - In gameplay, the pieces will render at the expected positions; however, due to the bounding box issue, you might need to click slightly off-target until collision boundaries are improved.

---

This version of the program provides nearly all the desired features; however, work remains on aligning the clickable areas with the rendered pieces and on supporting dynamic resizing during gameplay.
