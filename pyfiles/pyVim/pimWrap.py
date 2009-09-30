import vim

PIM_BUF_TYPE_READONLY   = 0x0001
PIM_BUF_TYPE_NORMAL     = 0x0002

def CreateRandomName( base ):
    import random
    random_ext = random.randint( 0 , 999999 )
    return '%s.%06d' % ( base , random_ext )


class pimBuffer:
    """
    Totally wrapper for the vim-buffer-object(VBO)
    This class can create , wipeout , and used to the class for a
    real buffer in the vim.
    """
    def __init__( self ,  type = PIM_BUF_TYPE_NORMAL , name = None):
        # save property
        self.type = type

        # get name if given , otherwise give the system random name
        self.name = name if name != None else CreateRandomName('PIM.BUF')

        # make enter first, use this flag to do the first enter # initialization
        self.firstEnter = True

        # create buffer, get the buffer id ( which is unique )
        bufferId = int( vim.eval('bufnr( "%s" ,1 )' % self.name ) )

        # get the vim buffer object
        self._buffer = filter( lambda x : x.number == bufid , vim.buffers )[0]

    def __del__( self ):
        if self._buffer != None:
            self.wipeout()


    def isExist( self ):
        if self._buffer == None :
            return False
        else:
            # if the buffer delete , the object has no member
            return dir(self._buffer ) != []

    def isShown(self):
        return int( vim.eval( 'bufwinnr(%d)' % self._buffer.number ) ) != -1 

    def getID( self ):
        return self._buffer.number
        
    def getName( self ):
        return self._buffer.name

    def wipeout( self ):
        vim.command('bwipeout %d' % self._buffer.number )
        self._buffer = None
        
    def setBufferType( self ):
        if self.type == PIM_BUF_TYPE_READONLY:
            ## can not write
            vim.command('setlocal nomodifiable')
            vim.command('setlocal noswapfile')
            vim.command('setlocal buftype=nofile')
            vim.command('setlocal readonly')
            vim.command('setlocal nowrap')
            
            ## maintain the shape
            vim.command('setlocal nonumber')
            #vim.command('setlocal cursorline')
            vim.command('setlocal foldcolumn=0')
            
            ## about buffer
            vim.command('setlocal bufhidden=hide')
            vim.command('setlocal nobuflisted')

        elif self.type == PIM_BUF_TYPE_NORMAL:
            vim.command('setlocal buflisted')
    
        
    def showBuffer( self , parentwin , **kwdict ):
        # the buffer does not exist
        if not self.isExist() : return

        # can not focus the parent win , win is closed maybe
        if parentwin and ( not parentwin.setFocus() ):
            return 
            
        vim.command('buffer %d' % self._buffer.number )

        # if this is the first time to show the buffer , set property
        if self.firstEnter :
            self.setBufferType()
            self.firstEnter = False

        # close readonly if need to
        if self.type == PIM_BUF_TYPE_READONLY :
            vim.command('setlocal modifiable')
            vim.command('setlocal noreadonly')
            
        self.OnUpdate( ** kwdict )
        
        # open readonly after update buffer
        if self.type == PIM_BUF_TYPE_READONLY :
            vim.command('setlocal nomodifiable')
            vim.command('setlocal readonly')
            
    def OnUpdate(self , ** kwdict ):
        # give the change to user to update the context
        pass


class pimWindow:
    """
    pimWindow is the wrap to a vim-window-object(VWO)
    This class just attach to the VWO , not create it.
    To create the VWO ,use the WindowsManager ,and WindowsManager just
    return the pimWindow Object.
    """
    def __init__( self , winObj = None ):
        self._window = winObj if winObj else vim.current.window
        #self._statusline= None

    def closeWindow( self ):
        # get win id , -1 means has been closed
        if self.getWindowID() == -1 :
            return
        else:
            self.setFocus()
            vim.command("close")
            
    def setFocus( self ):
        winID = self.getWindowID()
        # window has been close( destroyed ) 
        if winID == -1 :
            return False

        # focus the win
        vim.command("%dwincmd w" % ( self.getWindowID() + 1 , ) )
        return True

    def getWindowID( self ):
        # no window object is attach
        if self._window == None :
            return -1

        import re
        winStr = str( self._window )
        reMatch = re.match( '<window (?P<id>\d+)>' , winStr )
        if reMatch:
            return int( reMatch.group('id') )

        reMatch = re.match( 
                '<window object \(deleted\) at [A-Z0-9]{8}>' ,
                winStr)
        if reMatch:
            return -1
        raise

    def isShown( self ):
        return self.getWindowID() != -1

    #def setStatusLine(self , statusline = None ):
    #    self._statusline = statusline
    #    #print "%d %s" % ( self.getWindowID() , self._statusline )

        


    #def addBuffer( self , bufferObj , clearInvalid = True ):
    #    if clearInvalid : 
    #        self.clearInvalidBuffer()
    #    self.buflist.append( bufferObj )

    #def clearInvalidBuffer( self ):
    #    removelist = []
    #    for index , buf in enumerate( self.buflist ):
    #        if not buf.isExist():
    #            removelist.append( index )

    #    removelist.reverse()
    #    for index in removelist:
    #        del self.buflist[index]

    #def removeBuffer( self , id , clearInvalid = True ):
    #    _getter = self._makeGetter( type(id) )
    #    if clearInvalid : 
    #        self.clearInvalidBuffer()

    #    removedBuf = None
    #    for index , buf in enumerate( self.buflist ):
    #        if _getter(buf) == id :
    #            removedBuf = buf
    #            del self.buflist[index]
    #            break
    #    return removedBuf

    #def _makeGetter( self , idType ):
    #    import types
    #    property_getter = None
    #    if idType == types.IntType :
    #        property_getter = lambda x : x.getID()
    #    elif idType == types.StringType:
    #        property_getter = lambda x : x.getName()

    #    return property_getter

    #def wipoutBuffer( self , id ):
    #    delBuf = self.removeBufferFromList( id )
    #    if delBuf :
    #        delBuf.wipeout()
        
    #def showBuffer(self , id ):
    #    _getter = self._makeGetter( type(id) )
    #    for buf in self.buflist :
    #        if _getter(buf) == id :
    #            x.showBuffer( self )



PIM_SPLIT_TYPE_MOST_TOP     = 0x01
PIM_SPLIT_TYPE_MOST_BOTTOM  = 0x02
PIM_SPLIT_TYPE_MOST_RIGHT   = 0x04
PIM_SPLIT_TYPE_MOST_LEFT    = 0x08
PIM_SPLIT_TYPE_CUR_TOP      = 0x10
PIM_SPLIT_TYPE_CUR_BOTTOM   = 0x20
PIM_SPLIT_TYPE_CUR_LEFT     = 0x40
PIM_SPLIT_TYPE_CUR_RIGHT    = 0x80

class pimWinSplitter:
    _split_map = {
            PIM_SPLIT_TYPE_MOST_TOP   : 'topleft' ,
            PIM_SPLIT_TYPE_MOST_RIGHT : 'vertical botright',
            PIM_SPLIT_TYPE_MOST_LEFT  : 'vertical topleft',
            PIM_SPLIT_TYPE_MOST_BOTTOM: 'botright' ,
            PIM_SPLIT_TYPE_CUR_TOP    : 'aboveleft' ,
            PIM_SPLIT_TYPE_CUR_BOTTOM : 'rightbelow' ,
            PIM_SPLIT_TYPE_CUR_LEFT   : 'vertical aboveleft' ,
            PIM_SPLIT_TYPE_CUR_RIGHT  : 'vertical rightbelow' }

    _resize_map = {
            PIM_SPLIT_TYPE_MOST_TOP   : '',
            PIM_SPLIT_TYPE_MOST_RIGHT : 'vertical',
            PIM_SPLIT_TYPE_MOST_LEFT  : 'vertical',
            PIM_SPLIT_TYPE_MOST_BOTTOM: '',
            PIM_SPLIT_TYPE_CUR_TOP    : '',
            PIM_SPLIT_TYPE_CUR_BOTTOM : '',
            PIM_SPLIT_TYPE_CUR_LEFT   : 'vertical',
            PIM_SPLIT_TYPE_CUR_RIGHT  : 'vertical' }

    _split_command = 'split'
    _split_format = '%(type)s %(width)d%(cmd)s'

    _resize_command = 'resize'
    _resize_format = '%(type)s %(cmd)s %(width)d'
            
    def __init__( self , type , width , base_window = None):
        if type & 0xF0 and base_window == None :
            raise "pimWinSplitter : Must give base window when split with CUR"

        self.type = type
        self._basewin = base_window
        self.width = width

    def getResizeCmd( self ):
        return self._resize_format % {
                'type': self._resize_map[self.type],
                'cmd' : self._resize_command ,
                'width' : self.width }

    def getSplitCmd( self ):
        return self._split_format % {
                'width' : self.width , 
                'type'  : self._split_map[self.type] , 
                'cmd'   : self._split_command }
        
    def doSplit(self):
        if self._basewin :
            self._basewin.setFocus()

        command = self.getSplitCmd()
        vim.command( command )

        return pimWindow ( vim.current.window )


class pimWindowManager():
    def __init__( self , description_file = None ):
        self.window_info = {}

    def makeWindows( self ):
        self.window_info['main'] = pimWindow()
        self.window_info['panel'] = pimWinSplitter( PIM_SPLIT_TYPE_MOST_RIGHT , 30 ).doSplit()
        self.window_info['list'] = pimWinSplitter( 
                PIM_SPLIT_TYPE_CUR_BOTTOM , 10 , self.window_info['panel'] ).doSplit()





