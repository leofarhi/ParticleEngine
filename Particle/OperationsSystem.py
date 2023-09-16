#Ce script sert à géré toutes les opérations
#en lien avec l'application et permet de
#faire des redo et undo par exemple
from Particle.Modules.Includes import *

class OperationsSystem:
    def __init__(self) -> None:
        pass

    @AddCallBackToStack("OnCreateMenu",0)
    def OnCreateMenu():
        GlobalVars.Particle.AddCommandsMenu("Edit", {
            "Annuler": (),
            "Rétablir": ()
        },False)