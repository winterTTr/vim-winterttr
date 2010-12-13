ATGlobalTypeDict = {}

def LoadConfig( typeid ):
    if ATGlobalTypeDict.has_key( typeid ):
        ATGlobalTypeDict[typeid].LoadConfig()

def ResetConfig( typeid ):
    if ATGlobalTypeDict.has_key( typeid ):
        ATGlobalTypeDict[typeid].ResetConfig()

def UpdateTags( typeid ):
    if ATGlobalTypeDict.has_key( typeid ):
        ATGlobalTypeDict[typeid].UpdateTags()

def DoCommand():
    from ATCmdManager import ATCmdManager
    ATCmdManager( ATGlobalTypeDict ).DoCommand()

def RegisterLoader( loader ):
    ATGlobalTypeDict[loader.GetTypeID()] = loader
