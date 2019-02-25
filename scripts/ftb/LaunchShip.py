# LaunchShip.py
# March 22, 2002
#
# by Evan Light aka sleight42, all rights reserved
#
# Permission to redistribute this code as part of any other packaging requires
# the explicit permission of the author in advance.
#
#
##############################################################################

import App
import loadspacehelper
import MissionLib
import ftb.FTB_MissionLib

ShuttleCounter = 1
GetOnBoard = 0

# TODO: handle damage to shuttle bays by destroying ships contained within
# when damage == some integer increment X / Y where Y is the # of ships 
# contained in the bay

ET_MAY_LAUNCH_SHUTTLE_AGAIN = ftb.FTB_MissionLib.GetFTBNextEventType()

#print "ftb.LaunchShip"

#### MISSION START INITIALIZER ####

def MissionStart():
    #print "LaunchShip.MissionStart"
    #### REGISTER EVENT HANDLERS
    App.g_kEventManager.AddBroadcastPythonFuncHandler( ET_MAY_LAUNCH_SHUTTLE_AGAIN, App.Game_GetCurrentGame(), "ftb.LaunchShipHandlers.MayLaunchShuttleAgain")

#### ASSORTED HELPERS #####

class LaunchLocation:
    def __init__( self, sShipClass, pProperty):
        self.sShipClass = sShipClass
        self.pOEPProperty = pProperty

##############################################################################
# Launches a friendly AI controlled Ship from the specified ship
# pLaunchingShip    - a ShipClass specifying the ship to launch from
# sShipClass        - the class of ship to launch (a String containing the
#                     actual module name for the ship as from /script/ships)
# iLaunchInterval   - the delay time before the pLaunchingShip will be allowed
#                     to launch another vessel
# aiScriptName      - the name of the AI module to use for this ship
def LaunchAIShip( pLaunchingShip, pOEPProperty, pLaunchSystem, sShipClass, iLaunchInterval, aiScriptName, commandable=None, bTimer=None, side="Friendly", sShipName=None, ForceDirectAI=0):
    global ShuttleCounter 
    ShuttleCounter = ShuttleCounter + 1
    #sShipName = "Ship " + str( ShuttleCounter)
    # Change by Occas
    if sShipName == None:
            sShipName = sShipClass + " - " + str(ShuttleCounter)
    while(MissionLib.GetShip(sShipName)):
            ShuttleCounter = ShuttleCounter + 1
            sShipName = sShipClass + " - " + str(ShuttleCounter)
    LaunchShipByClass( pLaunchingShip, pOEPProperty, pLaunchSystem, sShipClass, sShipName)
    pSet = pLaunchingShip.GetContainingSet()
    pLaunchedShip = App.ShipClass_GetObject( pSet, sShipName)
    if not pLaunchedShip:
            print("Unknown Shuttle Launching Error (LaunchShip.py): Ship was not created")
            return
    if side == "Friendly":
        ftb.FTB_MissionLib.AddObjectToFriendlyGroup( sShipName)
    elif side == "Neutral":
        ftb.FTB_MissionLib.AddObjectToNeutralGroup( sShipName)
    elif side == "Enemy":
        ftb.FTB_MissionLib.AddObjectToEnemyGroup(sShipName)
    if( bTimer):
        StartLaunchIntervalTimer( pLaunchSystem, iLaunchInterval) 
    if commandable:
        MissionLib.AddCommandableShip( sShipName)
    pAI = None
    global GetOnBoard
    from ReturnShuttles import Transport
    if GetOnBoard:
	Transport(sShipName)
	pPlayer = MissionLib.GetPlayer()
	pPlayer.SetTarget(pLaunchingShip.GetName())
    else:
	pHull = pLaunchingShip.GetHull()
	pLauncherShipName = pLaunchingShip.GetName()
	pRadius = pHull.GetRadius()
        if ForceDirectAI == 0:
	        pDoneAI = aiScriptName
	        pTempAI = __import__ ("ftb.PassThroughAI")
                pAI = pTempAI.CreateAI( pLaunchedShip, pDoneAI, pRadius, pLauncherShipName)
                pLaunchingShip.SetAI( pAI)
        else:
                try:
                        aiModule = __import__( aiScriptName)
                        pAI = aiModule.CreateAI( pLaunchedShip)
                        pLaunchingShip.SetAI( pAI)
                except ValueError: 
                        pass


##############################################################################
# Launches a ship from a source ship
# pLaunchingShip    - a ShipClass specifying the ship to launch from
# sShipClass        - the class of ship to launch (a String containing the
#                     actual module name for the ship as from /script/ships)
# sLaunchedShipName - the DisplayName for the new ship
def LaunchShipByClass( pLaunchingShip, pOEPProperty, pLaunchSystem, sShipClass, sLaunchedShipName):
        "Creates a simple TGSequence to launch a ship"

        if( not pLaunchingShip) or ( pLaunchingShip.IsDoingInSystemWarp() == 1):
                return 0
        pSequence = App.TGSequence_Create()
        launchLoc = LaunchLocation( sShipClass, pOEPProperty)
        pSequence.AppendAction( App.TGScriptAction_Create( __name__, "LaunchObject", pLaunchingShip.GetObjID(), sLaunchedShipName, launchLoc))
        pSequence.Play()


##############################################################################
# Creates a Timer that controls when the launching system will be permitted
# to launch another object
# pLaunchingShip    - a ShipClass specifying the ship to launch from
# iLaunchInterval   - the delay time before the pLaunchingShip will be allowed
#                     to launch another vessel
def StartLaunchIntervalTimer( pSystem, iLaunchInterval):
    pEvent = App.TGEvent_Create()
    #pEvent.SetObjPtr( pSystem)
    pEvent.SetEventType( ET_MAY_LAUNCH_SHUTTLE_AGAIN)
    #pEvent.SetSource( pSystem)
    pEvent.SetDestination( pSystem)
    pTimer = App.TGTimer_Create()
    pTimer.SetTimerStart( App.g_kUtopiaModule.GetGameTime() + iLaunchInterval)
    pTimer.SetDelay( 0)
    pTimer.SetDuration( 0)
    pTimer.SetEvent( pEvent)
    App.g_kTimerManager.AddTimer( pTimer)

# NOTE: Lifted from Actions.ShipScriptActions by TG
# Minor modifications by EL
def LaunchObject(pAction, iShipID, pcName, launchLoc):
    "Launches an object from the given ship."

    pShip = App.ShipClass_Cast(App.TGObject_GetTGObjectPtr(iShipID))

    if (pShip == None):
        return(0)

    # Find any object emitter properties on the ship.
    pPropSet = pShip.GetPropertySet()

    pLaunchProperty = App.ObjectEmitterProperty_Cast( launchLoc.pOEPProperty)

    if (pLaunchProperty != None):
        # We found a valid launch bay. Create the object, and point it 
        # facing out of the shuttle bay.

        pSet = pShip.GetContainingSet()

        # Create the object.
        pcScript = launchLoc.sShipClass
        if( pcScript == None):
            # We can't create anything.
            return(0)

        # Create the object.
        pObject = loadspacehelper.CreateShip(pcScript, pSet, pcName, "", 0, 1)

        if (pObject != None):
            # Now change the position and facing of the object to match the 
            #emitter.
            pFwd = pLaunchProperty.GetForward()
            pUp = pLaunchProperty.GetUp()

            pRotation = pShip.GetWorldRotation()

            pPosition = pLaunchProperty.GetPosition()
            pPosition.MultMatrixLeft(pRotation)
            pPosition.Add(pShip.GetWorldLocation())
            pObject.SetTranslate(pPosition)

            pFwd.MultMatrixLeft(pRotation)
            pUp.MultMatrixLeft(pRotation)
            pObject.AlignToVectors(pFwd, pUp)
            pObject.UpdateNodeOnly()

            # Don't collide with the ship that created us.
            pObject.EnableCollisionsWith(pShip, 0)
            #TODO: Re-enable collisions with pShip using a TGTimer

    # Woohoo, we're done.
    return(0)
