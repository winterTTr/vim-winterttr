from pimWrap import *

class pimFrameException(Exception):
    pass


PIM_FRAME_TYPE_TOP      = PIM_SPLIT_TYPE_MOST_TOP
PIM_FRAME_TYPE_BOTTOM   = PIM_SPLIT_TYPE_MOST_BOTTOM
PIM_FRAME_TYPE_LEFT     = PIM_SPLIT_TYPE_MOST_LEFT
PIM_FRAME_TYPE_RIGHT    = PIM_SPLIT_TYPE_MOST_RIGHT
PIM_FRAME_TYPE_FIXSIZE  = 0x100

class pimFrame( pimWindow ):
    def __init__( self , type  , width , framework ):
        # a frame must be position independent 
        if type & 0xF0 :
            raise pimFrameException('Frame split with "PIM_SLIT_TYPE_CRU_*" is invalid')

        # make splitter
        splitter = pimWinSplitter( type & 0xFF , width , None )
        # init base pimWindow
        pimWindow.__init__( self , None , splitter )

        # set property 
        self._framework = framework
        self._framework.addFrame( self )
        self._childwinlist = []
        self._type = type

        self._tmpwin = None
        self._mainWin = None

    def showFrame( self ):
        # must has a child win , if want the frame to show
        if len( self._childwinlist ) == 0:
            raise pimFrameException('Frame must has a child win')
        # check main win
        if self._mainWin == None and len( self._childwinlist ) != 1 :
            raise pimFrameException('Frame must know which window is the  main win , use setMainWin() first ')

        # if there is only one child win , make it as main window
        if self._mainWin == None and len( self._childwinlist ) == 1:
            self._mainWin = self._childwinlist[0] 

        # check if the all childwin is shown which means the frame has
        # been shown , if not , close Frame and recreate child win
        for childwin in self._childwinlist:
            if not childwin.isShown():
                self.closeFrame()
                break

        # show the main window as the base of childwin if there is
        self.showWindow()
        self._tmpwin = pimWindow( vim.current.window , None )

        # show the child base on the Frame itself
        for child in self._childwinlist:
            child.showWindow()

        # set fix win if neccessary
        if self._type & PIM_FRAME_TYPE_FIXSIZE :
            self._mainWin.setFocus()
            vim.command('setlocal winfixwidth')
            self.resize()

        # close tmp win
        self._tmpwin.closeWindow()
        self._tmpwin = None

    def setMainWin( self , win ):
        self._mainWin = win

    def resize( self ):
        if not (  self._type & PIM_FRAME_TYPE_FIXSIZE ):
            return

        command = self.splitter.getResizeCmd()

        if self._mainWin :
            self._mainWin.setFocus()
            vim.command( command )

    def getFramework( self ):
        return self.framework

    def addChildWindow( self , childwin ):
        # must be a child win
        if not isinstance( childwin , pimChildWindow ):
            raise pimFrameException('addChildWindow: a child win should be a class from pimChildWindow')
        # add to win list
        self._childwinlist.append( childwin )

    def getTmpBufferID( self ):
        return self._framework.getTmpBufferID()

    def closeFrame( self ):
        for childwin in self._childwinlist:
            childwin.closeWindow()



class pimChildWindowException(Exception):
    pass

PIM_CHILDWIN_TYPE_TOP       = PIM_SPLIT_TYPE_CUR_TOP
PIM_CHILDWIN_TYPE_BOTTOM    = PIM_SPLIT_TYPE_CUR_BOTTOM
PIM_CHILDWIN_TYPE_LEFT      = PIM_SPLIT_TYPE_CUR_LEFT
PIM_CHILDWIN_TYPE_RIGHT     = PIM_SPLIT_TYPE_CUR_RIGHT

class pimChildWindow( pimWindow ):
    def __init__( self , type , width , parentFrm ):
        # must be a child win
        assert type & 0xF0

        # make splitter
        splitter = pimWinSplitter( 
                type , 
                width ,
                parentFrm )

        # init base pimWinSplitter
        pimWindow.__init__( self , None , splitter )
        
        # set property 
        self._parentFrm = parentFrm
        self._parentFrm.addChildWindow( self )

    def getFrame( self ):
        return self._parentFrm
