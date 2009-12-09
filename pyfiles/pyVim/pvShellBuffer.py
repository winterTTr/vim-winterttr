import vim

from pvWrap import pvBuffer
from pvWrap import GenerateRandomName
from pvWrap import PV_BUF_TYPE_READONLY , PV_BUF_TYPE_NORMAL

from pvKeyMap import pvKeyMapEvent , pvKeyMapObserver , pvKeyMapManager
from pvKeyMap import PV_KM_MODE_INSERT , PV_KM_MODE_NORMAL


class pvShellBuffer( pvBuffer , pvKeyMapObserver ):
    def __init__( self ):
        super( pvShellBuffer , self ).__init__( PV_BUF_TYPE_NORMAL , GenerateRandomName('PV_SHLBUF_') )

        # the max line store in this buffer
        # if over , delete the former lines
        self.__max_line = 1000


        # window property
        self.registerCommand('setlocal foldcolumn=0')

        # buffer property
        self.registerCommand('setlocal buftype=nofile')
        self.registerCommand('setlocal bufhidden=hide')
        self.registerCommand('setlocal nobuflisted')

        # connect to a shell instance

    

