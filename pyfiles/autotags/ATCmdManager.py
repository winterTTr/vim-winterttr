import vim
import sys
from ATVimFuncWrapper import VimConfirm

class ATCmdManager:
    def __init__( self , typedict ):
        self.typedict = typedict


    def GetUserSelection( self , prompt , selection_list ):
        selection_list_ex = [prompt]
        for index in xrange( len ( selection_list ) ):
            selection_list_ex.append( '%d> %s' % ( index + 1 , selection_list[index] ) )
        return int(  vim.eval( 'inputlist(%s)' % str( selection_list_ex ) ) ) 

    def DoCommand( self ):
        # type id 
        typeidlist = [ key for key in self.typedict.keys() ]
        if typeidlist is [] :
            print "Autotags ==> No type registered!"
            return

        typeid = self.GetUserSelection( 'Select type id:' , typeidlist )

        if typeid == 0 :
            return
        elif typeid -1 > len( typeidlist ):
            return

        typeid = typeidlist[typeid - 1]

        # action type : Create | Remove
        actionlist = [ "Create Repos" , "Remove Repos" ]
        action = self.GetUserSelection("Select action type:" , actionlist )
        if action == 0 :
            return

        if action == 1 :
            self.typedict[ typeid ].CreateRepository()
        elif action == 2 :
            self.typedict[ typeid ].RemoveRepository()


