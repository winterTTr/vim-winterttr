from pyvim.pvUtil import pvString
from pyvim.pvWrap import pvBuffer , PV_BUF_TYPE_ATTACH
from pyvim.pvWrap import pvWindow
from pyvim.pvTree import pvTreeBuffer , pvTreeNode , pvTreeNodeFactory , pvTreeBufferObserver
from pyvim.pvTree import PV_TREE_NODE_TYPE_BRANCH , PV_TREE_NODE_TYPE_LEEF
from pyvim.pvTree import PV_TREE_UPDATE_TARGET , PV_TREE_UPDATE_SELECT
from pyvim.pvAutocmd import pvAutocmdEvent , pvAutocmdManager , pvAutocmdObserver 


import os 
import string
import vim

import logging
_logger = logging.getLogger('pve.FileExplorer')


# =============================================================
# implement the node for the directory and file
# =============================================================

class FENodeRoot( pvTreeNode ):
    def __init__( self ):
        super( FENodeRoot , self ).__init__( PV_TREE_NODE_TYPE_BRANCH )

    def __iter__( self ):
        for x in string.ascii_uppercase :
            driver_path = u'%s:\\' % x
            if os.path.isdir( driver_path ):
                yield FENodeDirectory( driver_path )

    def OnName( self ):
        return pvString()

class FENodeDirectory( pvTreeNode ):
    def __init__( self , path ):
        super( FENodeDirectory , self ).__init__( PV_TREE_NODE_TYPE_BRANCH )
        self.path = path

    def __iter__( self ):
        for x in os.listdir( self.path ):
            full_path = os.path.join( self.path , x )
            if not os.path.isdir( full_path ):
                yield FENodeFile( full_path )

        for x in os.listdir( self.path ):
            full_path = os.path.join( self.path , x )
            if os.path.isdir( full_path ):
                yield FENodeDirectory( full_path )


    def OnName( self ):
        name = os.path.basename( self.path )

        ret = pvString()
        ret.UnicodeString = self.path if name == u'' else name
        return ret

class FENodeFile( pvTreeNode ):
    def __init__( self , path ):
        super( FENodeFile , self ).__init__( PV_TREE_NODE_TYPE_LEEF )
        self.path = path

    def OnName( self ):
        name = pvString()
        name.UnicodeString = os.path.basename( self.path)
        return name


# =============================================================
# implement the node factory
# =============================================================

class FENodeFactory( pvTreeNodeFactory ):
    def generateNode( self , path ):
        if path == [] :
            return FENodeRoot()
        else:
            uni_path = [ x.UnicodeString for x in path ]
            full_path = os.path.join( *uni_path )
            if os.path.isdir( full_path ):
                return FENodeDirectory( full_path )
            elif os.path.isfile( full_path ):
                return FENodeFile( full_path )
            else :
                return None


# =============================================================
# file explorer
# =============================================================
class FileExplorer( pvTreeBufferObserver , pvAutocmdObserver ):
    def __init__( self , target_win ):
        self.__target_win = target_win

        self.__buffer = pvTreeBuffer( FENodeFactory() )
        self.__buffer.registerObserver( self )

        self.__evet_list = []
        self.__evet_list.append( pvAutocmdEvent( 'BufEnter' , '*' ) )
        for event in self.__evet_list:
            pvAutocmdManager.registerObserver( event , self )

    def destroy( self ):
        for event in self.__evet_list:
            pvAutocmdManager.removeObserver( event , self )
        self.__buffer.removeObserver( self )
        self.__buffer.wipeout()

    def showBuffer( self , show_win ):
        self.__buffer.showBuffer( show_win )
        self.syncWithMainWindow()
        self.__target_win.setFocus()

    # from |pvTreeBufferObserver|
    def OnBranchOpen( self , **kwdict ):
        if kwdict['node'] :
            os.chdir( kwdict['node'].path )

    def OnBranchClose( self , **kwdict ):
        if kwdict['node'] :
            os.chdir( kwdict['node'].path )

    def OnLeefSelect( self , **kwdict ):
        if not kwdict['node'] : return

        node = kwdict['node']
        _logger.debug('OnLeefSelect() path = %s' % node.path )
        dir , fname = os.path.split( node.path )
        os.chdir( dir )

        if kwdict['type'] == PV_TREE_UPDATE_SELECT:
            from pyvim.pvWrap import pvBuffer , PV_BUF_TYPE_NORMAL
            buf = pvBuffer( type = PV_BUF_TYPE_NORMAL , name = pvString( UnicodeString = node.path ).MultibyteString )
            buf.showBuffer( self.__target_win )
            buf.detach()


        self.__target_win.setFocus()


    # from |pvAutocmdObserver|
    def OnHandleAutocmdEvent( self , **kwdict ):
        if not self.__buffer.isShown(): return
        if kwdict['event'] == 'bufenter' and self.__target_win == pvWindow() :
            self.syncWithMainWindow()

    def syncWithMainWindow( self ):
        buf_no = self.__target_win.bufferid
        if buf_no == -1 :
            cwd = os.getcwdu() # unicode current work directory
        else:
            buf = pvBuffer( PV_BUF_TYPE_ATTACH )
            buf.attach( buf_no )
            cwd = pvString( MultibyteString = buf.name ).UnicodeString
            if cwd == u"" :
                cwd = os.getcwdu() # unicode current work directory

        cwd_list = []
        while True:
            cwd , tail = os.path.split( cwd )
            if tail == u'': 
                if cwd[-1] == '/': cwd = cwd[:-1] + '\\'
                cwd_list.insert( 0 , pvString( UnicodeString = cwd ) )
                break

            cwd_list.insert( 0 ,  pvString( UnicodeString = tail ) )

        self.__buffer.updateBuffer( type = PV_TREE_UPDATE_TARGET , target = cwd_list )

