#
# ShipManager
#
# by Evan Light aka sleight42
# All Rights Reserved
#
# This module acts as a Factory and repository of ftb.Ship.Ship objects 
# and it's subclasses.
##################################################################

import App
import Registry
import MissionLib
import ftb.Ship
import ftb.Carrier

classRegistry = Registry.Registry()
shipRegistry = Registry.Registry()

def GetShip(pShip):
    retval = None
    if (pShip != None):
        pShip = App.ShipClass_Cast( pShip)
        if( pShip != None):
            retval = shipRegistry.GetName( pShip.this)
            if (retval == None):
                shipClass = GetShipClass(pShip.GetShipProperty().GetShipName())
                retval = shipClass(pShip)
                shipRegistry.Register(retval, pShip.this)
    return retval


def RemoveShip(pShip):
        pShip = App.ShipClass_Cast(pShip)
        if pShip:
                shipRegistry.Remove(pShip.this)


def RegisterShipClass(className, shipClass):
    if (className == None):
        print("ValueError in ftb.ShipManager.RegisterShipClass() - className cannot be None") # we maybe print an error
    if (shipClass == None):
        print("ValueError in ftb.ShipManager.RegisterShipClass() - shipClass cannot be None") # but we do not raise one!
    classRegistry.Register(shipClass, className)


def GetShipClass(className):
    retval = classRegistry.GetName(className)
    if (retval == None):
        retval = ftb.Ship.Ship
    return retval


# Based off of Dasher's LoadExtraPlugins based off of Banbury's GetShipList()
# ;) sleight42
def LoadExtraPlugins(dir = 'scripts\\Custom\\Carriers\\'):
    import nt
    import string

    list = nt.listdir(dir)
    list.sort()

    dotPrefix = string.join(string.split(dir, '\\')[1:], '.')

    for plugin in list:
        s = string.split(plugin, '.')
        pluginFile = ''
        # We don't want to accidentally load the wrong ship.
        # Indexing by -1 lets us be sure we're grabbing the extension. -Dasher42
        if len(s) > 1 and \
           ( s[-1] == 'pyc' or s[-1] == 'py'):
            pluginFile = s[0]
        else:
            continue

        try:
            pModule = __import__(dotPrefix + pluginFile)
        except ImportError:
            pass

LoadExtraPlugins()
