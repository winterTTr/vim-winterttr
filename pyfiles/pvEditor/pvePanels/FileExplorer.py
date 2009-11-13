from _PanelBase_ import PanelBase

from pyVim.pvUtil import pvString
from pyVim.pvTreeBuffer import pvTreeBuffer , pvTreeNode , pvTreeNodeFactory , pvTreeObserver
from pyVim.pvTreeBuffer import PV_TREE_NODE_TYPE_BRANCH , PV_TREE_NODE_TYPE_LEEF
from pyVim.pvTreeBuffer import PV_TREE_UPDATE_TARGET , PV_TREE_UPDATE_SELECT


import os 
import string
import vim


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
            if os.path.isdir( full_path ):
                yield FENodeDirectory( full_path )
            else:
                yield FENodeFile( full_path )

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
class _class_( PanelBase , pvTreeObserver ):
    def __init__( self , win_mgr ):
        self.__win_mgr = win_mgr

        self.__buffer = pvTreeBuffer( FENodeFactory() )
        self.__buffer.registerObserver( self )

        self.__name = u"File Explorer"


    # from |PanelBase|
    def OnName( self ):
        str = pvString()
        str.UnicodeString = self.__name
        return str

    def OnPanelSelected( self , item ):
        if item.UnicodeString != self.__name :
            return

        cwd = os.getcwdu() # unicode current work directory
        
        cwd_list = []
        while True:
            cwd , tail = os.path.split( cwd )
            if tail == u'': 
                cwd_u = pvString( UnicodeString = cwd )
                cwd_list.insert( 0 , cwd_u )
                break

            tail_u = pvString( UnicodeString = tail )
            cwd_list.insert( 0 , tail_u )
        
        self.__buffer.showBuffer( self.__win_mgr.getWindow('panel') )
        self.__buffer.updateBuffer( type = PV_TREE_UPDATE_TARGET , target = cwd_list )


    # from |pvTreeObserver|
    def OnBranchOpen( self , node ):
        os.chdir( node.path )

    def OnBranchClose( self , node ):
        os.chdir( node.path )

    def OnLeefSelect( self , node ):
        dir , fname = os.path.split( node.path )
        os.chdir( dir )

        from pyVim.pvWrap import pvBuffer , PV_BUF_TYPE_NORMAL
        buf = pvBuffer( type = PV_BUF_TYPE_NORMAL , name = node.path )
        buf.showBuffer( self.__win_mgr.getWindow('main') )
        buf.detach()

