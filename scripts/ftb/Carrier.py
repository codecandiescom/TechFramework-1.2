# Carrier
# March 27, 2002
#
# by Evan Light aka sleight42
#
# All rights reserved
# Permission to redistribute this code as part of any other packaging requires
# the explicit permission of the author in advance.
##############################################################################

from Registry import Registry
import ftb.LaunchShip
import ftb.Ship

# TODO: Createa a default launch group for people who don't care
class Carrier( ftb.Ship.Ship):
    "A Ship subclass that carries a series of launchers carrying other ships/objects" 

    def __init__( self, pShip):
        ftb.Ship.Ship.__init__( self, pShip)
        # TODO: change self.launchers to a Registry
        self.launchers = Registry()

    def AddLauncher( self, launcherName, launcher):
        if( launcherName != None and launcher != None):
            self.launchers.Register( launcher, launcherName)

    def GetLauncher( self, launcherName):
        if( launcherName != None and self.launchers.has_key( launcherName)):
            return self.launchers.GetName( launcherName)

    def GetLaunchers( self):
        return self.launchers

    def GetNumLaunches( self, launchName):
        "Iterates over all of a Carriers launchers and tallies up the number of a particular Launch aboard"
        retval = 0
        if( launchName != None):
            for launcherName in self.launchers._keyList:
                launcher = self.launchers[launcherName]
                retval = retval + launcher.GetNumLaunches( launchName)
        return retval

    def HasMoreLaunches( self, shuttle): 
        return self.GetNumLaunches( shuttle)

    def GetLaunchType( self, launcherName):
        return self.launchers.GetName( launcherName).GetLaunchType()

    def NextLaunchType( self, launcherName):
        return self.launchers.GetName( launcherName).NextLaunchType()
        
    def LaunchShip( self, shuttle, launcherName):
        return self.Launchers.GetName( launcherName).LaunchShip( shuttle)

    def LaunchShip( self, shuttle, launcherIndex):
        return self.Launchers[launcherIndex].LaunchShip( shuttle)
