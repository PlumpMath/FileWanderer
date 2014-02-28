README for FileWanderer

SETUP:
Keep these files in the same folder somewhere:
* ”fileWanderer.py”
* ”fileWandererHideFiles.py”
* ”fileWandererRestartGame.py”

TO PLAY:
Run “fileWanderer.py”

TO QUIT:
Use CTRL + C to safely quit the game (it will automatically save your progress)

TO HIDE FILES:
Run “fileWandererHideFiles.py”
This will hide all files associated with the game (but not get rid of your saved progress).

TO DELETE FILES / START NEW GAME:
Run “fileWandererRestartGame.py”
This will permanently delete everything associated with the current game, allowing you to start fresh.

DEVELOPMENT:
The basic FileWanderer library is stored in “wndr.py” - at the moment that’s where most of the game logic is. The main loop and some other game logic is in “fileWanderer.py”