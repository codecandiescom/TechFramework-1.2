# MissionLib
# April 17, 2002
#
# by EvanLight aka sleight42
# All Rights Reserved
#
# Updated February 2004 by ftbUpdate team
# 18.04.2004, Defiant: Moved some stuff from ReturnShuttles
##############################################################

import App
import MissionLib
import string

# Version etc
MODINFO = { "Author": "eMail: ftb@defiant.homedns.org",
            "Download": "http://defiant.homedns.org/~ftb/",
            "Version": "20050301",
            "License": "GPL",
            "Description": "script to Launch Shuttles"
            }

##############################################################
# Adds the ship, specified by DisplayName, to the Friendly group
# sShipName - The display name of the ship to add to the Friendly group
def AddObjectToFriendlyGroup( sObjectName):
    pMission = App.Game_GetCurrentGame().GetCurrentEpisode().GetCurrentMission()
    pMission.GetFriendlyGroup().AddName( sObjectName)

def AddObjectToEnemyGroup( sObjectName):
    pMission = App.Game_GetCurrentGame().GetCurrentEpisode().GetCurrentMission()
    pMission.GetEnemyGroup().AddName( sObjectName)

def AddObjectToNeutralGroup( sObjectName):
    pMission = App.Game_GetCurrentGame().GetCurrentEpisode().GetCurrentMission()
    pMission.GetNeutralGroup().AddName( sObjectName)

# broken in Bridge Commander? Looks like the game gives the same event type away several times.
# Fix arround that by adding an offset
def GetFTBNextEventType():
    return 222 + App.Mission_GetNextEventType()

#############################################################
#
# GetShuttleOEP(pShip) - This function is designed for use in
#                        mission coding, when you want to
#                        launch a ship from an AI ship
#                        and need to find the OEP
#                       
# Returns the first shuttle OEP found on pShip
# or None
# Taken from ShipScriptActions.LaunchObject and mutilated
#
#############################################################
def GetShuttleOEP(pShip):
	# Find any object emitter properties on the ship.
	pPropSet = pShip.GetPropertySet()
	pEmitterInstanceList = pPropSet.GetPropertiesByType(App.CT_OBJECT_EMITTER_PROPERTY)

	pEmitterInstanceList.TGBeginIteration()
	iNumItems = pEmitterInstanceList.TGGetNumItems()

	pLaunchProperty = None

	for i in range(iNumItems):
		pInstance = pEmitterInstanceList.TGGetNext()

		# Check to see if the property for this instance is a shuttle
		# emitter point.
		pProperty = App.ObjectEmitterProperty_Cast(pInstance.GetProperty())
		if (pProperty != None):
			# If we have the right type of OEP, bail now
			if (pProperty.GetEmittedObjectType() == App.ObjectEmitterProperty.OEP_SHUTTLE):
				pLaunchProperty = pProperty
				break

	pEmitterInstanceList.TGDoneIterating()
	pEmitterInstanceList.TGDestroy()

	return(pLaunchProperty)


# Here we Count the Shuttles in our Bay
# Basicly copied from the Shuttle Launching Framework by sleight42 (ftb.LaunchShipHandlers.AddLaunchButtons() )
def GetShuttlesInBay(sFiringShipName = None):        
        if not sFiringShipName:
            sFiringShipName = App.Game_GetCurrentPlayer().GetName()
        
        import ftb.ShipManager
        pCarrier = ftb.ShipManager.GetShip(MissionLib.GetShip(sFiringShipName))
        if not hasattr(pCarrier, "GetLaunchers"):
            return
        pLaunchers = pCarrier.GetLaunchers()
        numTypes = len( pLaunchers)
        for index in range( numTypes):
                launchType = pLaunchers[index].GetLaunchType()
                if (string.find(str(launchType), 'Mine') == -1):
                        numLaunches = pLaunchers[index].GetNumLaunches( launchType)
                else:
                        numLaunches = 0

                launchType = pLaunchers[index].NextLaunchType()
                firstlaunchType = None
        
                i = 0
                while (launchType != firstlaunchType):
                        if (launchType != firstlaunchType): #and string.find(str(launchType), 'Mine') == -1):
                                numLaunches =  numLaunches + pLaunchers[index].GetNumLaunches(launchType)
                        if (i == 0):
                                firstlaunchType = launchType
                        launchType = pLaunchers[index].NextLaunchType()
                        if ( i > 10 ):
                        # This makes sure the Game is not crashing if we have 0 Shuttles in Bay.
                                return 0
                        i = i + 1

	return numLaunches


# Now the hard Work with the ftb begins!
def IncreaseShuttleCount(ShipType, sFiringShipName = None):
        verbose = 0
        if verbose: print("Trying to increase Shuttle Count")

        if (sFiringShipName == None):
                if verbose: print("Problem: No Firing Ship - Using Players Ship as default")
                sFiringShipName = App.Game_GetCurrentPlayer().GetName()
        
        ShuttleCount = ShuttlesInBayOfThisType(ShipType, sFiringShipName)
        if verbose: print("ShipType:", ShipType, "ShipCount1: ", ShuttleCount)
        pShip = MissionLib.GetShip(sFiringShipName)

	# Thats from the Carrier System config by Sleight42
	import ftb.LauncherManager
        launcher = ftb.LauncherManager.GetLauncher(GetFirstShuttleBayName(sFiringShipName), pShip)
	launcher.AddLaunchable(ShipType, "QuickBattle.QuickBattleFriendlyAI", 1)

        # There maybe a Problem with some Carrier configurations, correct those
        if (ShuttleCount >= ShuttlesInBayOfThisType(ShipType, sFiringShipName)):
                if verbose: print("ShipCount Problem: ", ShuttlesInBayOfThisType(ShipType, sFiringShipName))
                launcher.AddLaunchable(ShipType, "QuickBattle.QuickBattleFriendlyAI", ShuttleCount + 1)

	# and finally reload the Button - yeah we fixed the damm Problem!
        import ftb.LaunchShipHandlers
	ftb.LaunchShipHandlers.SetToggleLaunchButton()
	if verbose: print("ShipCount2: ", ShuttlesInBayOfThisType(ShipType, sFiringShipName))


# just a split of the old GetShuttleBay()
def GetShuttleBaySize(OurShipName, pShip):
        ShuttleBaySize = FindAShuttleBay(pShip)
        if ShuttleBaySize:
                return ShuttleBaySize.GetRadius()
        return 0


# This make sure we don't destroy the other Shuttles in this Bay
# Its mostly the same like GetShuttlesInBay(), so also from the Shuttle Launching Framework by sleight42.
def ShuttlesInBayOfThisType(Type, sFiringShipName = None):
        if (sFiringShipName == None):
                sFiringShipName = App.Game_GetCurrentPlayer().GetName()
        
        import ftb.ShipManager
        pCarrier = ftb.ShipManager.GetShip(MissionLib.GetShip(sFiringShipName))
        pLaunchers = pCarrier.GetLaunchers()
        numTypes = len( pLaunchers)
        for index in range( numTypes):
                launchType = None
                i = 0
                while (launchType != Type):
                        launchType = pLaunchers[index].NextLaunchType()
                        numLaunches =  pLaunchers[index].GetNumLaunches( launchType)
                        if ( i > 10 ):
                        # Stop crashing Stupid Game
                                return 0
                        i = i + 1

	return numLaunches


# Actually based on MissionLib().FindShuttleBay()
def FindAShuttleBay(pShip):
	iShipID = pShip.GetObjID()

	pPropSet = pShip.GetPropertySet()
	pHullPropInstanceList = pPropSet.GetPropertiesByType(App.CT_HULL_PROPERTY)
	
	pHullPropInstanceList.TGBeginIteration()
	iNumItems = pHullPropInstanceList.TGGetNumItems()
	
	pLaunchProperty = None

	for i in range(iNumItems):
		pInstance = pHullPropInstanceList.TGGetNext()

		# Check to see if the property for this instance is a Hull Property
		pProperty = App.HullProperty_Cast(pInstance.GetProperty())

		if (pProperty != None):
			if ( pProperty.GetName().CompareC("Shuttle", 1) != -1 ):
				pHullPropInstanceList.TGDoneIterating()
				pHullPropInstanceList.TGDestroy()
				return(pProperty)


# How much Shuttles can we get in our Bay?
# Created by Sim Rex
def SetMaxShuttlesInBay(OurShipName):
    import ftb.ShipManager
    pCarrier = ftb.ShipManager.GetShip(MissionLib.GetShip(OurShipName))
    if hasattr(pCarrier, "GetMaxShuttles"):
        iMaxShuttles = pCarrier.GetMaxShuttles()
    else:
        iMaxShuttles = int(MissionLib.GetShip(OurShipName).GetHull().GetRadius()*4)
    return iMaxShuttles


# Created by Sim Rex
# Quote: Took far too long to work that out.. 
# It's a shame that the BC Python version doesn't have the very useful help() function...
# Would've saved me a lot of opening and closing of BC...
def GetOEPs(sFiringShipName = None):
        if not sFiringShipName:
            sFiringShipName = App.Game_GetCurrentPlayer().GetName()
        
        import ftb.ShipManager
	pCarrier = ftb.ShipManager.GetShip(MissionLib.GetShip(sFiringShipName))
	if not hasattr(pCarrier, "GetLaunchers"):
            return
        pFTBLaunchers = pCarrier.GetLaunchers() 
	OEPList = [] 
	for launcher in pFTBLaunchers: 
		OEPs = launcher.GetLaunchers() 
		OEPList = OEPList + OEPs 
	return OEPList

# Just give me the name of our first Shuttle Bay plz:
def GetFirstShuttleBayName(sFiringShipName = None):
        if not App.Game_GetCurrentPlayer().GetName():
                return
        if not sFiringShipName:
            sFiringShipName = App.Game_GetCurrentPlayer().GetName()

	ShuttleBayName = GetOEPs(sFiringShipName) #calling Sim Rex's Function
        if not ShuttleBayName:
            return
	return ShuttleBayName[0] # yes, thats the easy Version ;)


# next Shuttle Bay:
def GetNextShuttleBayName(sFiringShipName, LastBay):
	ShuttleBayNames = GetOEPs(sFiringShipName) #calling Sim Rex's Function
        if not ShuttleBayNames:
            return
        i = 0
        for i in range (len(ShuttleBayNames)):
                if (ShuttleBayNames[i] == LastBay):
                    if (i + 1 < len(ShuttleBayNames)):
                        return ShuttleBayNames[i + 1]
                    else:
                        return ShuttleBayNames[0]

