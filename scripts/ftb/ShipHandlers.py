# Ship.py
# March 16, 2002
#
# by sleight42 aka Evan Light, all rights reserved
#
# Permission to redistribute this code as part of any other packaging requires
# the explicit permission of the author in advance.
##############################################################################

import App
import Registry
import MissionLib
import ftb.Ship
import Bridge.BridgeUtils
import ftb.GUIUtils

shipRegistry = Registry.Registry()

def GetShip( pShip):
    retval = None
    if pShip != None:
        retval = shipRegistry.GetName( pShip.this)
        if( retval == None):
            retval = ftb.Ship.Ship( pShip)
            shipRegistry.Register( retval, pShip.this)
    return retval

#### BEGIN EVENT HANDLERS
def FirePrimaryWeaponsOnList( pObject, pEvent):
    pShip = App.Game_GetCurrentPlayer()
    pMyShip = GetShip( pShip)
    if (pMyShip  == None):
    	return
    pMyShip.FireWeaponsOnList( pEvent.GetBool(), App.ShipClass.WG_PRIMARY)
    pObject.CallNextHandler(pEvent)

def FireSecondaryWeaponsOnList( pObject, pEvent):
    pShip = App.Game_GetCurrentPlayer()
    pMyShip = GetShip( pShip)
    if not pMyShip:
            return
    pMyShip.FireWeaponsOnList( pEvent.GetBool(), App.ShipClass.WG_SECONDARY)
    pObject.CallNextHandler(pEvent)

def FireTertiaryWeaponsOnList( pObject, pEvent):
    pShip = App.Game_GetCurrentPlayer()
    pMyShip = GetShip( pShip)
    if not pMyShip:
            return
    pMyShip.FireWeaponsOnList( pEvent.GetBool(), App.ShipClass.WG_TERTIARY)
    pObject.CallNextHandler(pEvent)

def ClearSecondaryTargets(pObject, pEvent):
    pPlayer = App.Game_GetCurrentPlayer()
    if pPlayer:
        pMyShip = GetShip( pPlayer)
        pMyShip.ClearSecondaryTargets()	

def ToggleSecondaryTarget(pObject, pEvent):
    pPlayer = App.Game_GetCurrentPlayer()
    if pPlayer:
        pMyShip = GetShip( pPlayer)
        #pMyShip.ToggleSecondaryTarget( GetTargetByIdx( pEvent.GetInt())) 
        if pPlayer.GetTarget():
                pMyShip.ToggleSecondaryTarget(App.ShipClass_Cast(pPlayer.GetTarget()))
#### END EVENT HANDLERS

def GetPlayerSet():
    pGame = App.Game_GetCurrentGame()
    return pGame.GetPlayerSet()

def GetTargetByIdx( idx):
    retval = None
    pEnemyGroup = MissionLib.GetEnemyGroup()
    lEnemies = pEnemyGroup.GetActiveObjectTupleInSet( GetPlayerSet())
    eCounter = 0
    for pEnemy in lEnemies:
        if( eCounter == idx ):
            retval = pEnemy
            break
        eCounter = eCounter + 1
    return retval

def MissionStart():
    #### REGISTER EVENT HANDLERS

    App.ET_INPUT_FIRE_PRIMARY_ON_LIST = 42*42*42
    App.ET_INPUT_FIRE_SECONDARY_ON_LIST = 42*42*42*2
    App.ET_INPUT_FIRE_TERTIARY_ON_LIST = 42*42*42*3
    App.ET_INPUT_CLEAR_SECONDARY_TARGETS= 42*42*42*4
    App.ET_INPUT_TOGGLE_SECONDARY_TARGET= 42*42*42*5

    lEventHandlerMap = (
        (App.ET_INPUT_CLEAR_SECONDARY_TARGETS, __name__ + ".ClearSecondaryTargets"),
        (App.ET_INPUT_TOGGLE_SECONDARY_TARGET, __name__ + ".ToggleSecondaryTarget"),
        (App.ET_INPUT_FIRE_TERTIARY_ON_LIST, __name__ + ".FireTertiaryWeaponsOnList"),
        (App.ET_INPUT_FIRE_SECONDARY_ON_LIST, __name__ + ".FireSecondaryWeaponsOnList"),
        (App.ET_INPUT_FIRE_PRIMARY_ON_LIST,	__name__ + ".FirePrimaryWeaponsOnList"),
        )

    for eType, sFunc in lEventHandlerMap:
        App.g_kEventManager.AddBroadcastPythonFuncHandler( eType, App.Game_GetCurrentGame(), sFunc)
            

    #### SET KEYBOARD MAPPINGS FOR EVENTS

    # CLEAR BINDINGS
#	App.g_kKeyboardBinding.ClearBinding(App.ET_INPUT_SELECT_X, App.KeyboardBinding.GET_INT_EVENT, 1)
#	App.g_kKeyboardBinding.ClearBinding(App.ET_INPUT_SELECT_X, App.KeyboardBinding.GET_INT_EVENT, 2)
#	App.g_kKeyboardBinding.ClearBinding(App.ET_INPUT_SELECT_X, App.KeyboardBinding.GET_INT_EVENT, 3)
#	App.g_kKeyboardBinding.ClearBinding(App.ET_INPUT_SELECT_X, App.KeyboardBinding.GET_INT_EVENT, 4)
#	App.g_kKeyboardBinding.ClearBinding(App.ET_INPUT_SELECT_X, App.KeyboardBinding.GET_INT_EVENT, 5)
#	App.g_kKeyboardBinding.ClearBinding(App.ET_INPUT_SELECT_X, App.KeyboardBinding.GET_INT_EVENT, 6)
#	App.g_kKeyboardBinding.ClearBinding(App.ET_INPUT_SELECT_X, App.KeyboardBinding.GET_INT_EVENT, 7)
#	App.g_kKeyboardBinding.ClearBinding(App.ET_INPUT_SELECT_X, App.KeyboardBinding.GET_INT_EVENT, 8)
#	App.g_kKeyboardBinding.ClearBinding(App.ET_INPUT_SELECT_X, App.KeyboardBinding.GET_INT_EVENT, 9)
#
#	App.g_kKeyboardBinding.ClearBinding(App.ET_INPUT_FIRE_PRIMARY, App.KeyboardBinding.GET_BOOL_EVENT, 0)
#	App.g_kKeyboardBinding.ClearBinding(App.ET_INPUT_FIRE_SECONDARY, App.KeyboardBinding.GET_BOOL_EVENT, 0)
#	App.g_kKeyboardBinding.ClearBinding(App.ET_INPUT_FIRE_TERTIARY, App.KeyboardBinding.GET_BOOL_EVENT, 0)
#	App.g_kKeyboardBinding.ClearBinding(App.ET_INPUT_FIRE_PRIMARY, App.KeyboardBinding.GET_BOOL_EVENT, 1)
#	App.g_kKeyboardBinding.ClearBinding(App.ET_INPUT_FIRE_SECONDARY, App.KeyboardBinding.GET_BOOL_EVENT, 1)
#	App.g_kKeyboardBinding.ClearBinding(App.ET_INPUT_FIRE_TERTIARY, App.KeyboardBinding.GET_BOOL_EVENT, 1)


    # ESTABLISH BINDINGS
    App.g_kKeyboardBinding.BindKey(App.WC_F, App.TGKeyboardEvent.KS_KEYDOWN, App.ET_INPUT_FIRE_PRIMARY_ON_LIST, App.KeyboardBinding.GET_BOOL_EVENT, 1)
    App.g_kKeyboardBinding.BindKey(App.WC_LBUTTON, App.TGKeyboardEvent.KS_KEYDOWN, App.ET_INPUT_FIRE_PRIMARY_ON_LIST, App.KeyboardBinding.GET_BOOL_EVENT, 1)
    App.g_kKeyboardBinding.BindKey(App.WC_F, App.TGKeyboardEvent.KS_KEYUP, App.ET_INPUT_FIRE_PRIMARY_ON_LIST, App.KeyboardBinding.GET_BOOL_EVENT, 0)
    App.g_kKeyboardBinding.BindKey(App.WC_LBUTTON, App.TGKeyboardEvent.KS_KEYUP, App.ET_INPUT_FIRE_PRIMARY_ON_LIST, App.KeyboardBinding.GET_BOOL_EVENT, 0)

    App.g_kKeyboardBinding.BindKey(App.WC_X, App.TGKeyboardEvent.KS_KEYDOWN, App.ET_INPUT_FIRE_SECONDARY_ON_LIST, App.KeyboardBinding.GET_BOOL_EVENT, 1)
    App.g_kKeyboardBinding.BindKey(App.WC_X, App.TGKeyboardEvent.KS_KEYUP, App.ET_INPUT_FIRE_SECONDARY_ON_LIST, App.KeyboardBinding.GET_BOOL_EVENT, 0)
    App.g_kKeyboardBinding.BindKey(App.WC_RBUTTON, App.TGKeyboardEvent.KS_KEYDOWN, App.ET_INPUT_FIRE_SECONDARY_ON_LIST, App.KeyboardBinding.GET_BOOL_EVENT, 1)
    App.g_kKeyboardBinding.BindKey(App.WC_RBUTTON, App.TGKeyboardEvent.KS_KEYUP, App.ET_INPUT_FIRE_SECONDARY_ON_LIST, App.KeyboardBinding.GET_BOOL_EVENT, 0)

    App.g_kKeyboardBinding.BindKey(App.WC_G, App.TGKeyboardEvent.KS_KEYDOWN, App.ET_INPUT_FIRE_TERTIARY_ON_LIST, App.KeyboardBinding.GET_BOOL_EVENT, 1)
    App.g_kKeyboardBinding.BindKey(App.WC_G, App.TGKeyboardEvent.KS_KEYUP, App.ET_INPUT_FIRE_TERTIARY_ON_LIST, App.KeyboardBinding.GET_BOOL_EVENT, 0)

#    App.g_kKeyboardBinding.BindKey(App.WC_NUMPADENTER, App.TGKeyboardEvent.KS_KEYDOWN, App.ET_INPUT_CLEAR_SECONDARY_TARGETS, App.KeyboardBinding.GET_INT_EVENT, 0, App.KeyboardBinding.KBT_SINGLE_KEY_TO_EVENT)

#    App.g_kKeyboardBinding.BindKey(App.WC_NUMPAD2, App.TGKeyboardEvent.KS_KEYDOWN, App.ET_INPUT_TOGGLE_SECONDARY_TARGET, App.KeyboardBinding.GET_INT_EVENT, 1, App.KeyboardBinding.KBT_SINGLE_KEY_TO_EVENT)

#    App.g_kKeyboardBinding.BindKey(App.WC_NUMPAD3, App.TGKeyboardEvent.KS_KEYDOWN, App.ET_INPUT_TOGGLE_SECONDARY_TARGET, App.KeyboardBinding.GET_INT_EVENT, 2, App.KeyboardBinding.KBT_SINGLE_KEY_TO_EVENT)

#    App.g_kKeyboardBinding.BindKey(App.WC_NUMPAD4, App.TGKeyboardEvent.KS_KEYDOWN, App.ET_INPUT_TOGGLE_SECONDARY_TARGET, App.KeyboardBinding.GET_INT_EVENT, 3, App.KeyboardBinding.KBT_SINGLE_KEY_TO_EVENT)

#    App.g_kKeyboardBinding.BindKey(App.WC_NUMPAD5, App.TGKeyboardEvent.KS_KEYDOWN, App.ET_INPUT_TOGGLE_SECONDARY_TARGET, App.KeyboardBinding.GET_INT_EVENT, 4, App.KeyboardBinding.KBT_SINGLE_KEY_TO_EVENT)

#    App.g_kKeyboardBinding.BindKey(App.WC_NUMPAD6, App.TGKeyboardEvent.KS_KEYDOWN, App.ET_INPUT_TOGGLE_SECONDARY_TARGET, App.KeyboardBinding.GET_INT_EVENT, 5, App.KeyboardBinding.KBT_SINGLE_KEY_TO_EVENT)

#    App.g_kKeyboardBinding.BindKey(App.WC_NUMPAD7, App.TGKeyboardEvent.KS_KEYDOWN, App.ET_INPUT_TOGGLE_SECONDARY_TARGET, App.KeyboardBinding.GET_INT_EVENT, 6, App.KeyboardBinding.KBT_SINGLE_KEY_TO_EVENT)

#    App.g_kKeyboardBinding.BindKey(App.WC_NUMPAD8, App.TGKeyboardEvent.KS_KEYDOWN, App.ET_INPUT_TOGGLE_SECONDARY_TARGET, App.KeyboardBinding.GET_INT_EVENT, 7, App.KeyboardBinding.KBT_SINGLE_KEY_TO_EVENT)

#    App.g_kKeyboardBinding.BindKey(App.WC_NUMPAD9, App.TGKeyboardEvent.KS_KEYDOWN, App.ET_INPUT_TOGGLE_SECONDARY_TARGET, App.KeyboardBinding.GET_INT_EVENT, 8, App.KeyboardBinding.KBT_SINGLE_KEY_TO_EVENT)

#    App.g_kKeyboardBinding.BindKey(App.WC_NUMPAD0, App.TGKeyboardEvent.KS_KEYDOWN, App.ET_INPUT_TOGGLE_SECONDARY_TARGET, App.KeyboardBinding.GET_INT_EVENT, 9, App.KeyboardBinding.KBT_SINGLE_KEY_TO_EVENT)

#    App.g_kEventManager.RemoveBroadcastHandler(App.ET_MISSION_START, App.Game_GetCurrentGame(), __name__ + ".MissionStart")
def AddKeyBind(KeyName, pEvent, EventInt = 0, Group = "Ship", eType = App.KeyboardBinding.GET_INT_EVENT):
	import Foundation
	import Custom.Autoload.LoadTech
	if not hasattr(Foundation, "g_kKeyBucket"):
		return
        mode = Custom.Autoload.LoadTech.mode
        Foundation.g_kKeyBucket.AddKeyConfig(Foundation.KeyConfig(KeyName, KeyName, pEvent, eType, EventInt, Group, dict = {"modes": [mode]}))


MissionStart()

# Buttons
pMenu = ftb.GUIUtils.GetTacticalMenu()

pSTMenu = App.STMenu_CreateW(App.TGString("Secondary Targetting"))
if pSTMenu:
	pMenu.AddChild(pSTMenu)

	pTakeTargetButton = ftb.GUIUtils.CreateIntButton("take secondary Target", App.ET_INPUT_TOGGLE_SECONDARY_TARGET, MissionLib.GetMission(), 0)
	pSTMenu.PrependChild(pTakeTargetButton)
	AddKeyBind("take secondary Target", App.ET_INPUT_TOGGLE_SECONDARY_TARGET)

	pclearTargetsButton = ftb.GUIUtils.CreateIntButton("clear sec Targets", App.ET_INPUT_CLEAR_SECONDARY_TARGETS, MissionLib.GetMission(), 0)
	pSTMenu.PrependChild(pclearTargetsButton)
	AddKeyBind("clear sec Targets", App.ET_INPUT_CLEAR_SECONDARY_TARGETS)
