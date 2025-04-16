Mac Related notes and concerns.

There are two major aspects to the Mac development process: The stockfish executable and the packaging for a stand alone game. 


Stockfish executable:

In the process of development this semester I have come across many notes and concerts which I will now note. 
If you weren't aware, Mac cannot handle .exe files. This means we cannot use the provided stockfish .exe file. Because of this we have created our own executable for mac
The windows version is named “fairy-stockfish-largeboard_x86_-64.exe”
The mac version is named “stockfish”
Note that in the code there is platform specific code to determine the OS and assign the path name accordingly. 
This has been extensively used with no reported issues.
The mac executable is very picky with file permissions so check that before use. You may have to chmod if you run into problems. 
This executable has been passed around to other mac users with no issues, Ill note that most of the permission issues come during the packaging process. 
The mac executable was compiled by me and I have no idea who did the windows version.
Notes on creating the stockfish executable if things go awry:
The general step is use the stockfish github and compile it yourself in a different folder then you should be good to copy and paste only the executable. 
MAKE SURE YOU USE THE FAIRY-STOCKFISH GITHUB NOT THE STOCKFISH GITHUB.
Personal note: the documentation of both projects link back and forth to each other so be sure when you actually go to create it you are following the steps to use the fairy-stockfish version. The original stockfish version will not work. Ask me how I found out. 
My understanding is the fair-stockfish contains all of the random variants. 
Follow the general steps for compilation used in the notes for mac. I will add that If you try to do it exactly you'll run into issues. The best thing to do is clone the github, then run make to view a list of commands. There should be some help or something to that extent to pull up a list of all of the flags to add to the compilation command in order to run it. In general, just use the default for your OS architecture and you shouldnt have any issues compiling, HOWEVER, if you use the default values, it wont work. You must add two different flags in order to make it work. Make sure to use the largeboard variant and make sure that variants=yes. If you have an executable that connects and does not crash this code, but it isnt working as expected, you likely just have an issue with the executable. Compilation is fairly simple to understand but you're in for a world of pain if you don't do it right. There is absolutely 0 error handling in this code and adding some should be a major concern for the next classes. I will add that because there's no error handling, if something doesn't work the code just crashes which is nice from a dev perspective because you know exactly what broke. I would definitely consider adding error handling in the future though. 

Everything before now in this doc is what we call phase 1. Phase 1 went rather well and only took several weeks to implement. Most of the issues I was unable to resolve are beyond this point and are all related to packaging. 
Packaging on a mac is not fun.
Here's some random notes:
READ ALL OF THIS BEFORE DOING ANYTHING
I attempted to use two different packages for python: Pyinstaller and Cx_Freeze. 
Pyinstaller is relatively easy to use. The setup process is rather simple. The biggest issue you'll face is adding all of the assets into the compilation. 
I was able to see immediate results with the pyinstaller in less than a week. I was able to package the game, and run ONLY the single player version with no issues.
File permission problems on the stockfish executable are largely the hold up and preoccupied me for several weeks. I still haven't found a working solution. 
Upon launching the game, the game would crash and I would be unable to access the stockfish executable due to file permission errors. 	
Solutions tried include properly and improperly adding the executable just to see if I get lucky, trying to write code to CHMOD the file inside of the script (did not work) and writing code to use an indirect and direct file path to the file.
To this day I still don't know why it doesn't work. Both pyinstaller and Cx_Freeze didnt work so I'm not sure.
All of this leads me to the Second major problem I ran into. Every piece of code in this program assumes you are in the Janggi directory and is completely relative. Not being in the proper directory will cause the code not to work. What this means is that when I tried to compile down to a single executable, nothing worked at all. Also I realized that the program was just accessing the githubs .png resources and not the png resources in the executable because I was just navigating my directory to Janggi via subprocess commands in main.py. 
Note: this is objectively a dumb idea and i don't know why i did this. This is not in the code anymore but essentially I was navigating the working directory into users/me/vscode/koreanChess/Janggi inorder to make the executables work. I (somehow) only realized that as soon as you move the file to another machine the whole thing will break . I then removed all code like this and shifted my focus to discovering how to access the resources in the package, which I never solved. 
I only had a few weeks to actually dedicate to this so I was unable to discover how to properly access all of the data. You'll see what I mean when you try to run one of the build scripts. 
Anytime there is  a Load Image part of the code, its accessing local resources and not package resources so that is a problem to be fixed. 
There are two different build files in github right now. One for cx_freeze and one for pyinstaller. In order to build, just run either python3 build.py build or python3 createPackage.py.  I'm convinced that the problem lies somewhere in these two files and me doing something improperly. I just ran out of time. 
Future steps
I would continue on with these if I had more time I just don't
Improved error handling
There's nothing graceful about this code. 
Improved documentation
When we started this project there wasn't even a main readme. Any comments or text docs to explain stuff is so great. 
Finishing the package	
My guess is pyinstaller is the best bet, I'm just missing some piece of info.
Restart. 
A Lot of this code needs so much work you might just be better off on a redo. 


Best of luck.
