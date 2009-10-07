import vim

from pvWrap import pvBuffer
from pvWrap import CreateRandomName
from pvWrap import PV_BUF_TYPE_READONLY , PV_BUF_TYPE_NORMAL

class pvListBuffer(pvBuffer):
    data_format = "%(mark)1s [%(name)s]"
    def __init__( self ):
        pvBuffer.__init__( self , PV_BUF_TYPE_READONLY , CreateRandomName( 'PV.LISTBUF' ) )
        self.data = []
        self.selection = 0
        self.resize = False


    
    def OnUpdate( self , ** kwdict ):
        """
        @brief update the list buffer content according to the member data [self.data]
        @param kwdict 
                      - selection : set the current selection item
                      - resize    : set if resize the window height
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

        if self.selection >= len( self.data ):
            self.selection = 0

        # clear the screen
        self._buffer[:] = None

        # deal with internal data
        show_data = []
        for index in xrange( len( self.data ) ):
            show_data.append( 
                    self.data_format % {
                        'mark' : '>' if self.selection == index else ' ' ,
                        'name' : self.data[index] } )

        # redraw the content
        self._buffer[0:len(show_data) -1 ] = show_data

        # resize window
        if self.resize : vim.command('resize %d' % len( self.data ) )

        
