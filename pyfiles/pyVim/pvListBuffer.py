import vim
import types
from pvWrap import pvBuffer
from pvWrap import GenerateRandomName
from pvWrap import PV_BUF_TYPE_READONLY , PV_BUF_TYPE_NORMAL

from pvKeyMap import pvKeyMapEvent , pvKeyMapObserver , pvKeyMapManager
from pvKeyMap import PV_KM_MODE_NORMAL


class pvListBufferObserver(object):
    def OnSelectItemChanged( self , item ):
        raise NotImplementedError("pvListBufferObserver::OnSelectItemChanged")

class pvListBuffer( pvBuffer , pvKeyMapObserver ):
    def __init__( self ):
        pvBuffer.__init__( self , PV_BUF_TYPE_READONLY , GenerateRandomName( 'PV_LISTBUF_' ) )
        self.items = []
        self.selection = 0
        self.resize = False
        self.format = "%-20s"
        self.hilight = 'Search'

        self.ob_list = []

        self.registerCommand('setlocal nowrap')
        self.registerCommand('setlocal nonumber')
        self.registerCommand('setlocal foldcolumn=0')

        db_click_event = pvKeyMapEvent( '<2-LeftMouse>' , PV_KM_MODE_NORMAL , self )
        pvKeyMapManager.registerObserver( db_click_event , self )

        enter_event = pvKeyMapEvent( '<Enter>' , PV_KM_MODE_NORMAL , self )
        pvKeyMapManager.registerObserver( enter_event , self )

    def registerObserver( self , ob ):
        self.ob_list.append( ob )

    def removeObserver( self , ob ):
        self.ob_list.remove( ob )


    def OnUpdate( self , ** kwdict ):
        """
        @brief update the list buffer content according to the member data [self.data]
        @param kwdict 
                      - selection : set the current selection item
                      - resize    : set if resize the window height
                      - format    : use to format the string to show
                      - hilight   : the group name for the hilight
        """

        # get selection and resize
        if 'selection' in kwdict:
            self.selection = kwdict['selection'] % len( self.items )
        else:
            self.selection = vim.current.buffer.cursor[0]
        selection = self.selection 

        if 'resize' in kwdict:
            self.resize = kwdict['resize']
        resize = self.resize

        if 'format' in kwdict:
            self.format = kwdict['format']
        format = self.format

        if 'hilight' in kwdict:
            self.hilight = kwdict['hilight']
        hilight = self.hilight


        # clear the screen
        self.buffer[:] = None

        # deal with internal data
        show_data = []
        for index in xrange( len( self.items ) ):
            show_data.append( format % self.items[index].MultibyteString  )

        # hilight the item
        if len( show_data ) != 0 :
            self.registerCommand('match %s /\V%s/' % ( hilight ,  show_data[self.selection] ) )

        # redraw the content
        if len( show_data ):
            self.buffer[0:len(show_data) -1 ] = show_data

        # resize window
        if self.resize :
            self.registerCommand('resize %d' % len( self.items ) if len( self.items) else 1 )


    def OnHandleKey( self , **kwdict ):
        self.updateBuffer()
        for ob in self.ob_list:
            ob.OnSelectItemChanged( self.items[self.selection] )



        


