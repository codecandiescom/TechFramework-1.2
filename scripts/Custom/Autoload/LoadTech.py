import App
import Foundation
import techfunc


mode = Foundation.MutatorDef("New Technology System")

class FTBTrigger(Foundation.TriggerDef):
        def __init__(self, name, eventKey, dict = {}):
                Foundation.TriggerDef.__init__(self, name, eventKey, dict)

        def __call__(self, pObject, pEvent, dict = {}):
                techfunc.ImportTechs()

        def Deactivate(self):
                techfunc.pluginsLoaded = {}

FTBTrigger('FTB Trigger', App.ET_MISSION_START, dict = { 'modes': [ mode ] } )
