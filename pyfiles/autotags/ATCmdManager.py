import vim
import sys
from ATVimFuncWrapper import VimConfirm

class ATCmdManager:
    def __init__( self , typedict ):
        self.typedict = typedict

    def DoCommand( self ):
        # type id 
        typeidlist = [ key for key in self.typedict.keys() ]
        if typeidlist is [] :
            print "Autotags ==> No type registered!"
            return
        typeid = VimConfirm('Select type id :' , typeidlist )
        if typeid == None :
            print "Autotags ==> User Cancel Action!"
            return

        # action type : Create | Remove
        actionlist = [ "Create Repos" , "Remove Repos" ]
        action = VimConfirm("Select action type:" , actionlist )
        if action == None :
            print "Autotags ==> User Cancel Action!"
            return

        if action == "Create Repos" :
            self.typedict[ typeid ].CreateRepository()
        elif action == "Remove Repos" :
            self.typedict[ typeid ].RemoveRepository()


