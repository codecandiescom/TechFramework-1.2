# Launcher
# April 18, 2002
#
# by Evan Light aka sleight42
#
# All rights reserved
# Permission to redistribute this code as part of any other packaging requires
# the explicit permission of the author in advance.
##############################################################################

from Registry import Registry
import ftb.LaunchShip

LaunchAIShip = ftb.LaunchShip.LaunchAIShip

class Launcher:
    "A proxy for a ship's subsystem capable of launching an object"

    # pSystem   - The Hull System (targetable and destroyable) component of
    #             our launcher
    # pProperty - The ObjectEmitterProperty for the launcher
    def __init__( self, pSystem, pProperty, pShip):
        # TODO: Ensure compatability with LaunchGroup
        self.pHullSystem = pSystem
        self.pOEPProperty = pProperty
        self.Complement = Registry() 
        self.bClearToLaunch = 1
        self.fLaunchInterval = 2.0
        self.sLaunchType = None
        self.pShip = pShip

    def AddLaunchable( self, \
                       launchScriptName, \
                       aiModuleName, \
                       numberOfLaunch, \
                       commandable = 1):
        if( launchScriptName != None and numberOfLaunch >= 0):
            launchable = Launchable( aiModuleName, numberOfLaunch, commandable)
            self.Complement.Register( launchable, launchScriptName)

    def RemoveLaunchable( self, launchScriptName, numberOfLaunch):
        if launchScriptName != None and \
           numberOfLaunch >= 0:
            for launchType in self.Complement:
                if launchType == launchScriptName:
                    self.Complement.Remove( launchScriptName)

    def GetComplement( self):
        return self.Complement

    def GetNumLaunches( self, launch): 
        "Returns the number of Launches remaining of the requested type"
        retval = 0
        if( self.Complement._keyList.has_key( launch)):
            retval = self.Complement.GetName( launch).count
        return retval

    def HasMoreLaunches( self, launch): 
        return self.GetNumLaunches( launch)

    def SetLaunchInterval( self, interval):
        self.fLaunchInterval = interval

    def SetClearToLaunch( self, clear):
        "Sets this Launcher's semaphore to allow a Launch to deply"
        self.bClearToLaunch = clear

    def GetLaunchType( self):
        "Get the current Launch type."
        if( self.sLaunchType == None):
            keys = self.Complement._keyList.keys()
            for type in keys:
                if( self.Complement.GetName( type )> 0):
                    self.sLaunchType = type
        return self.sLaunchType
    
    def NextLaunchType( self):
        "Cycle to the next Launch type"
        retval = None
        if( self.sLaunchType == None):
            retval = self.GetLaunchType()
        else:
            keys = self.Complement._keyList.keys()
            startingIdx = keys.index( self.sLaunchType)
            index = startingIdx
            while( 1):
                if( len( keys) - 1 == index):
                    index = 0 
                elif( index < len( keys) -1):
                    index = index + 1
                if( index == startingIdx):
                    # we've cycled the whole dict.  we're out of ships
                    break
                elif( self.Complement[index] > 0):
                    retval = keys[index]
                    self.sLaunchType = retval
        return retval

    def LaunchShip( self):
        return self.LaunchShip( self.sLaunchType)
        
    def LaunchShip( self, launch, bTimer = None):
        "Decrement our count of this type of Launch and then launch an instance of this type of Launch"
        retval = 0
        if self.bClearToLaunch == 1 and \
           self.Complement._keyList.has_key( launch) and \
           self.Complement.GetName( launch) > 0:
            self.bClearToLaunch = 0
            launchable = self.Complement.GetName( launch)
            launchCount = launchable.count - 1
            if( bTimer == None):
                bTimer = launchCount
            self.Complement.Register( Launchable( launchable.aiModuleName, \
                                                  launchCount), \
                                      launch)
            LaunchAIShip( self.pShip, \
                          self.pOEPProperty, \
                          self.pHullSystem, \
                          launch, \
                          self.fLaunchInterval, \
                          launchable.aiModuleName, \
                          launchable.commandable, \
                          bTimer)
            retval = 1
        return retval

    def Equals( self, other):
        retval = 0
        if self.GetComplement() == other.GetComplement():
            retval = 1
        return retval

class Launchable:
    def __init__( self, aiModuleName, count, commandable = 1):
        self.count = count
        self.aiModuleName = aiModuleName
        self.commandable = commandable
