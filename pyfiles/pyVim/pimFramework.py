import vim
from pimWrap import *

class pimFramework:
    def __init__( self , name ):
        self.name = name
        self._framelist = []
        self.tmpbuf = None

    def showFramework( self ):
        # create new tab for the framework
        tmpBufID = self.getTmpBufferID()
        vim.command('silent! tab sbuffer %d' % tmpBufID )

        # show buffer
        self.basewin = pimWindow( vim.current.window , None )
        self.tmpbuf.showBuffer( self.basewin )

        # set tabTabel ( make sense with PimDynamicTabLabel )
        vim.command('let t:pimTitle="%s"' % self.name )

        # call custom init
        self.initInstance()

    def getTmpBufferID( self ):
        return self.getTmpBuffer().getID()
    
    def getTmpBuffer( self ):
        # check if the tmp buffer is exist
        if ( not self.tmpbuf ) or ( not self.tmpbuf.isExist() ):
            self.tmpbuf = pimBuffer( PIM_BUF_TYPE_READONLY )

        return self.tmpbuf

    def addFrame( self , frame ):
        self._framelist.append( frame )

    def updateAllFrame( self ):
        # show all frame
        for frame in self._framelist :
            frame.showFrame()

        # check if the tmp win ( first win ) is need to be left
        winCount = int( vim.eval('winnr("$")') )
        if winCount > 1:
            self.basewin.closeWindow()

        # resize the frame
        for frame in self._framelist:
            frame.resize()
            

    def initInstance( self ):
        #self.initEnd()
        pass
