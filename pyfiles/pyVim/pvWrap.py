import vim
import re

PV_BUF_TYPE_READONLY   = 0x0001
PV_BUF_TYPE_NORMAL     = 0x0002

def CreateRandomName( base ):
    import random
    random_ext = random.randint( 0 , 999999 )
    return '%s_%06d' % ( base , random_ext )


class pvBuffer(object):
    """
    Totally wrapper for the vim-buffer-object(VBO)
    This class can create , wipeout , and used to the class for a
    real buffer in the vim.
    """
    def __init__( self ,  type = PV_BUF_TYPE_NORMAL , name = None):
        # save property
        self.type = type

        # get name if given , otherwise give the system random name
        self.name = name if name != None else CreateRandomName('PV_BUF')

        # save the buffered command , when the buffer is open , the
        # command will be executed
        if type == PV_BUF_TYPE_READONLY :
            self.buffered_command_list = [
                    'setlocal nomodifiable' ,
                    'setlocal noswapfile' , 
                    'setlocal buftype=nofile' ,
                    'setlocal readonly' ,
                    'setlocal nowrap' , 
                    'setlocal nonumber' , 
                    'setlocal foldcolumn=0' , 
                    'setlocal bufhidden=hide' ,
                    'setlocal nobuflisted' ]
        elif type == PV_BUF_TYPE_NORMAL :
            self.buffered_command_list = ['setlocal buflisted']
        else:
            raise RuntimeError('pvBuffer , invalid type[%d]' % type )

        # create buffer, get the buffer id ( which is unique )
        buffer_id = int( vim.eval('bufnr( "%s" ,1 )' % self.name ) )

        # get the vim buffer object
        self._buffer = filter( lambda x : x.number == buffer_id , vim.buffers )[0]

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

    def setFocus( self ):
        show_win_id = int( vim.eval( 'bufwinnr(%d)' % self._buffer.number ) )
        if show_win_id == -1 :
            return False

        vim.command("%dwincmd w" % ( show_win_id , ) )
        return True

    def getID( self ):
        return self._buffer.number
        
    def getName( self ):
        return self._buffer.name

    def wipeout( self ):
        vim.command('bwipeout %d' % self._buffer.number )
        self._buffer = None
        
    def registerCommand( self , cmd ):
        self.buffered_command_list.append( cmd )

        # try to run the command
        # 1. save the current focus
        current_focus_win = pvWindow()
        # 2. if is shown , focus it and runcommand
        if not self.setFocus(): return 
        self.runCommand()

        # 3. recover the focus
        current_focus_win.setFocus()

    def runCommand( self ):
        while self.buffered_command_list : vim.command( self.buffered_command_list.pop(0) )

    def showBuffer( self , parentwin ):
        # the buffer does not exist
        if not self.isExist() : return

        # save focus
        current_focus_win = pvWindow()

        # can not focus the parent win , win is closed maybe
        if parentwin and ( not parentwin.setFocus() ):
            return 
            
        # open the buffer on the current window
        vim.command('buffer %d' % self._buffer.number )

        # run the buffer-specific command
        self.runCommand()

        # restore the focus
        if current_focus_win.getWindowID() != parentwin.getWindowID():
            current_focus_win.setFocus()


    def updateBuffer( self , **kwdict ):
        # save current focus win
        current_focus_win = pvWindow()

        # if not shown , do not update
        if not self.setFocus() : return


        # close readonly if need to
        if self.type == PV_BUF_TYPE_READONLY :
            vim.command('setlocal modifiable')
            vim.command('setlocal noreadonly')

        self.OnUpdate( ** kwdict )

        # open readonly after update buffer
        if self.type == PV_BUF_TYPE_READONLY :
            vim.command('setlocal nomodifiable')
            vim.command('setlocal readonly')

        # restore focus
        current_focus_win.setFocus()
            
    def OnUpdate(self , ** kwdict ):
        # give the change to user to update the context
        pass


class pvWindow(object):
    """
    pvWindow is the wrap to a vim-window-object(VWO)
    This class just attach to the VWO , not create it.
    To create the VWO ,use the pvWindowManager ,and pvWindowManager
    return the pvWindow Object.
    """
    def __init__( self , winObj = None ):
        self._window = winObj if winObj else vim.current.window
        #self._statusline= None

    def __eq__( self , other ):
        if isinstance( other , pvWindow ):
            self_id = self.getWindowID()
            other_id = other.getWindowID()
            return self_id != -1 and other_id != -1 and self_id == other_id

        return False

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



PV_SPLIT_TYPE_MOST_TOP     = 0x01
PV_SPLIT_TYPE_MOST_BOTTOM  = 0x02
PV_SPLIT_TYPE_MOST_RIGHT   = 0x04
PV_SPLIT_TYPE_MOST_LEFT    = 0x08
PV_SPLIT_TYPE_CUR_TOP      = 0x10
PV_SPLIT_TYPE_CUR_BOTTOM   = 0x20
PV_SPLIT_TYPE_CUR_LEFT     = 0x40
PV_SPLIT_TYPE_CUR_RIGHT    = 0x80

class pvWinSplitter(object):
    _split_map = {
            PV_SPLIT_TYPE_MOST_TOP   : 'topleft' ,
            PV_SPLIT_TYPE_MOST_RIGHT : 'vertical botright',
            PV_SPLIT_TYPE_MOST_LEFT  : 'vertical topleft',
            PV_SPLIT_TYPE_MOST_BOTTOM: 'botright' ,
            PV_SPLIT_TYPE_CUR_TOP    : 'aboveleft' ,
            PV_SPLIT_TYPE_CUR_BOTTOM : 'rightbelow' ,
            PV_SPLIT_TYPE_CUR_LEFT   : 'vertical aboveleft' ,
            PV_SPLIT_TYPE_CUR_RIGHT  : 'vertical rightbelow' }

    _split_command = 'split'
    _split_format = '%(type)s %(width)d%(cmd)s'

    def __init__( self , type , size , base_window = None):
        if type & 0xF0 and base_window == None :
            raise "pvWinSplitter : Must give base window when split with CUR"

        self.type = type
        self._basewin = base_window
        self.size = size

    def getSplitCmd( self ):
        return self._split_format % {
                'width' : 1 , 
                'type'  : self._split_map[self.type] , 
                'cmd'   : self._split_command }
        
    def doSplit(self):
        if self._basewin :
            self._basewin.setFocus()

        command = self.getSplitCmd()
        vim.command( command )

        if self.size[0] > 0 :
            command = "vertical resize %d" % self.size[0]
            vim.command( command )

        if self.size[1] > 0 :
            command = "resize %d" % self.size[1]
            vim.command( command )

        return pvWindow ( vim.current.window )


class pvWindowManager(object):
    def __init__( self ):
        self.windows = {}
        self.mainwin_position = (-1,-1)
        self.windows_info = []

    def analyzeDescription( self , description ):
        # analyze the description
        reEachWindow = re.compile("""
                \(\s*
                (?P<width>[\d-]+)
                \s*,\s*
                (?P<height>[\d-]+)
                \s*\)\s*
                (?P<name>[\w_-]+)
                """ , re.VERBOSE )
        for x in description.split('|') :
            self.windows_info.append([])
            for eachwin in reEachWindow.finditer( x ):
                self.windows_info[-1].append(
                        { 'name': eachwin.group('name') , 
                          'size' : ( 
                              -1 if eachwin.group('width') == '-' else int( eachwin.group('width') ),
                              -1 if eachwin.group('height') == '-' else int( eachwin.group('height') ) 
                                   )
                        } )

        # search 'main' window , get index ( x , y )
        try :
            for x in xrange( len(  self.windows_info ) ) :
                for y in xrange( len( self.windows_info[x] ) ):
                    if self.windows_info[x][y]['name'] == 'main':
                        self.mainwin_position = ( x , y )
                        raise
        except:
            pass

        if self.mainwin_position[0] == -1 :
            raise RuntimeError('must specify the "main" window info!')


    def makeColumnWindows( self , win_group_info , split_type ):
        info = win_group_info[0]
        self.windows[info['name']] = pvWinSplitter( split_type , info['size'] ).doSplit()

        prev_win = self.windows[info['name']]
        for index_win in xrange( 1 , len( win_group_info ) ) :
            info = win_group_info[index_win]
            self.windows[ info['name'] ] = pvWinSplitter(
                    PV_SPLIT_TYPE_CUR_BOTTOM ,
                    info['size'] , 
                    prev_win ).doSplit()
            prev_win = self.windows[ info['name'] ]
        

    def makeWindows( self , description ):
        self.analyzeDescription( description )

        # make current window to be the main window
        self.windows['main'] = pvWindow()
        # split the window left the main one
        if self.mainwin_position[0] != 0 : # if has left window
            for index_group in xrange( self.mainwin_position[0] - 1 , -1 , -1  ):
                self.makeColumnWindows( self.windows_info[index_group] , PV_SPLIT_TYPE_MOST_LEFT )

        if self.mainwin_position[1] != 0 :
            # split the window up the main one
            index_group = self.mainwin_position[0]

            prev_win = self.windows['main']
            for index_win in xrange( self.mainwin_position[1] - 1 , -1 , -1 ) :
                info = self.windows_info[index_group][index_win]
                self.windows[info['name']] = pvWinSplitter( 
                        PV_SPLIT_TYPE_CUR_TOP , 
                        info['size'] , 
                        prev_win )
                prev_win = self.windows[info['name']]

            # split the window down the main one
            prev_win = self.windows['main']
            for index_win in xrange( self.mainwin_position[1] + 1 , len( self.windows_info[index_group]) ) :
                info = self.windows_info[index_group][index_win]
                self.windows[info['name']] = pvWinSplitter( 
                        PV_SPLIT_TYPE_CUR_BOTTOM , 
                        info['size'] , 
                        prev_win )
                prev_win = self.windows[info['name']]


        # split the window right the main one
        for index_group in xrange( self.mainwin_position[0] + 1 , len( self.windows_info ) ):
            self.makeColumnWindows( self.windows_info[index_group] , PV_SPLIT_TYPE_MOST_RIGHT )

        for x in self.windows.keys():
            self.windows[x].setFocus()

        self.windows['main'].setFocus()

    def getWindow( self , name ):
        return self.windows[name]


