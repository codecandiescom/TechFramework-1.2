# Setup function - does whatever needed to be in LoadBridge.py
# This shouldn't need anything more...
import App

def Setup():
	if ( App.Game_GetCurrentGame() != None ):
		# Importing Secondary Targetting Mod by sleight42
		import ftb.Ship
