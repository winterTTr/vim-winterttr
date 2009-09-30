from pimFrameBase import *
from pimExBuffer import pimTabBuffer
from pimWrap import *

class pimTabFrame(pimFrame):
    def __init__( self , type , width , framework ):
        pimFrame.__init__( 
                self , 
                type ,  
                width  ,
                framework )

        # tab windows and buffer
        self._tabbuf = pimTabBuffer()
        self._tabwin = pimChildWindow(PIM_CHILDWIN_TYPE_TOP , 10 , self )
        self._tabwin.setStatusLine( "=" * 50 )
        
        
        # main windows and bufferlist
        mainWin =  pimChildWindow(PIM_CHILDWIN_TYPE_BOTTOM , 10 , self )
        self.setMainWin( mainWin )
        self._buflist = []
        
    def showFrame( self ):
        # if no buffer , can not show
        if len ( self._buflist ) == 0:
            return False
            
        # call base to show buffer and child win
        pimFrame.showFrame( self )
        
        # call to update tab win
        self.updateTabWin()
        
        # show buffer
        self._buflist[0].showBuffer( self._mainWin)
        
    def updateTabWin( self ):
        namelist = []
        for buf in self._buflist:
            namelist.append( buf.getName() )
            
        self._tabbuf.showBuffer( self._tabwin , namelist = namelist , selected = 0 )        
        

    def searchBuffer( self , bufid ):
        for index , buf in enumerate( self._buflist):
            if buf.getID() == bufid :
                return index , buf

        return -1 , None

    def addBuffer( self , buf ):
        self._buflist.append( buf )

    def removeBuffer( self , bufid ):
        index , buf = self.searchBuffer( bufid )
        if index != -1 :
            del self._buflist[index]
            return buf
        else:
            return None

    def showBuffer( self , bufid ):
        index , buf = self._searchBuffer( bufid )
        if index != -1 :
            buf.showBuffer( self )
            return True
        else:
            return False



    #def createBuffer(self , classType , name = None ):
    #    # check type
    #    import types
    #    if type( classType ) != types.ClassType or \
    #            not issubclass( classType , pimBuffer ):
    #        raise pimChildWindowException('Invalid buffer type')
    #        
    #    buf = classType( )

        

