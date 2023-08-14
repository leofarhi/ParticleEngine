import json
import os
from Particule.Modules.Directory import *

CreateDir(os.getcwd() + "/lib/languages")

class LanguageSystem:
    Instance = None
    def __init__(self):
        LanguageSystem.Instance = self
        self.Languages = {}
        self.CurrentLanguage = "fr"
        LanguageSystem.LoadLanguages()
    def LoadLanguages():
        for file in os.listdir("lib/languages"):
            if file.endswith(".json"):
                #check if file exists in lib/languages/filename.json
                if not os.path.exists("lib/languages/"+file):
                    #if not, create it
                    with open("lib/languages/"+file, "w", encoding="utf-8") as f:
                        json.dump({}, f, indent=4)
                with open("lib/languages/"+file, "r", encoding="utf-8") as f:
                    LanguageSystem.Instance.Languages = json.load(f)
    def SetLanguage(lang):
        LanguageSystem.Instance.CurrentLanguage = lang
    def GetLanguage():
        return LanguageSystem.Instance.CurrentLanguage
    def SaveLanguage(lang):
        with open("lib/languages/"+lang+".json", "w", encoding="utf-8") as f:
            json.dump(LanguageSystem.Instance.Languages, f, indent=4)
    def GetText(text):
        if text not in LanguageSystem.Instance.Languages:
            LanguageSystem.Instance.Languages[text] = text
            LanguageSystem.SaveLanguage(LanguageSystem.Instance.CurrentLanguage)
        return LanguageSystem.Instance.Languages[text]
    def SetText(text, value):
        LanguageSystem.Instance.Languages[text] = value

LanguageSystem()