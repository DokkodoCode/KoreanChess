CURRENT STATES 

 

MAC 

CURRENT STATE: The game is workable in terminal version. No known issues or errors. Executables for stockfish work as expected.  
 
BROKEN STATE: No known issues in the main as of right now.  
 
FUTURE IDEAS: Figure out how to compile down to executable or .app status for startup on application launch. The end goal is to move out of the terminal. Also eventually add more mac friendly resolutions to AI purposes.  
 

UI/UX 

CURRENT STATE: The current state of UI has the program scale statically. The user is prompted to choose a screen resolution upon running the program but cannot be changed later on. The values for on-screen objects are stored in a dictionary and are hard coded. 
 
BROKEN STATE: Currently, if the window is resized dynamically while a game is being played some program elements are not properly scaled/moved to what would be their new positions. (Examples for resizing dynamically can be seen in the Resizing-Style1 and Resizing-Style2 branches.) 
 
FUTURE IDEAS: Ideally, all program elements can be resized dynamically in any game state. 
 

MULTIPLAYER  

CURRENT STATE: Right now, multiplayer only works with two computers on the same network in a LAN environment. It grabs the private IP of your computer rather than using public IP which is needed to play across two different networks. The logic for Multiplayer gameplay is completely working as intended. 
 
BROKEN STATE : No known issues in multiplayer other than it only working in a LAN environment. 
 
FUTURE IDEAS: The primary goal should be enabling the game to work outside of LAN environments.  We would recommend implementing NAT traversal techniques and proper public IP address support with clear port forwarding instructions for players.  
