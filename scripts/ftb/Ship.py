# Ship.py
# March 16, 2002
#
# by sleight42 aka Evan Light, all rights reserved
#
# Permission to redistribute this code as part of any other packaging requires
# the explicit permission of the author in advance.
##############################################################################

import App
import ShipHandlers
import TacticalInterfaceHandlers

class Ship:
    def __init__(self,pShip):
        self.lSecondaryTargets = []
        self.pShip = pShip

    def __SetSecondaryTargets(self,lTargets):
        self.lSecondaryTargets = lTargets

    def GetSecondaryTargetsRef(self):
        return self.lSecondaryTargets

    def GetSecondaryTargets(self):
        return self.lSecondaryTargets[:]

    def HasAsSecondaryTarget(self,pShip):
        retval = 0
        for pTarget in self.lSecondaryTargets:
            if (pShip == pTarget):
                retval = 1
        return retval

    def ToggleSecondaryTarget(self,pShip):
        if self.HasAsSecondaryTarget(pShip):
            self.lSecondaryTargets.remove(pShip)
        else:
            self.lSecondaryTargets.append(pShip)

    def ClearSecondaryTargets(self):
        print "Clearing secondaries"
        self.lSecondaryTargets = []

    def FireWeaponsOnList(self, bFiring, eGroup):
        TacticalInterfaceHandlers.FireWeapons( self.pShip, bFiring, eGroup)
        pSystem = self.pShip.GetWeaponSystemGroup( eGroup)
        if (pSystem != None):
            pGame = App.Game_GetCurrentGame()
            if ( bFiring == 1):
                for pTarget in self.lSecondaryTargets:
                    retval = pSystem.StartFiring( pTarget,pTarget.GetTargetOffsetTG())
                    pSystem.SetForceUpdate( 1) # update and fire immediately
            else:
                pSystem.StopFiring()
