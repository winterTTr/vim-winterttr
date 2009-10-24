import vim
import types

from pvWrap import pvBuffer
from pvWrap import GenerateRandomName
from pvWrap import PV_BUF_TYPE_READONLY , PV_BUF_TYPE_NORMAL

class pvListBufferItem(object):
    def __str__( self ):
        raise RuntimeError('no implement')

    def __eq__( self , other ):
        return str( self ) == str( other )

class pvListBuffer(pvBuffer):
    def __init__( self ):
        pvBuffer.__init__( self , PV_BUF_TYPE_READONLY , GenerateRandomName( 'PV_LISTBUF' ) )
        self.item = []
        self.selection = 0
        self.resize = False
        self.format = "%-20s"
        self.hilight = 'Search'

    def getItemList( self ):
        return self.item

    def getSelection( self ):
        return self.selection

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
        try:
            self.selection = kwdict['selection']
        except:
            selection = self.selection 

        try:
            self.resize = kwdict['resize']
        except:
            resize = self.resize

        try:
            self.format = kwdict['format']
        except:
            format = self.format

        try:
            self.hilight = kwdict['hilight']
        except:
            hilight = self.hilight

        if self.selection >= len( self.item ):
            self.selection = 0

        # clear the screen
        self.buffer[:] = None

        # deal with internal data
        show_data = []
        for index in xrange( len( self.item ) ):
            show_data.append( format % str( self.item[index] ) )

        # hilight the item
        if len( show_data ) != 0 :
            vim.command('match %s /\V%s/' % ( hilight ,  show_data[self.selection] ) )

        # redraw the content
        self.buffer[0:len(show_data) -1 ] = show_data

        # resize window
        if self.resize : vim.command('resize %d' % len( self.item ) )

        
