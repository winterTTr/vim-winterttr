import os
import string

from pyVim.pvListBuffer import pvListBuffer
from pyVim.pvTabPanel import pvTabPanelItem

from pyVim.pvTreeBuffer import pvTreeBuffer , pvTreeNode , pvTreeNodeFactory
from pyVim.pvTreeBuffer import PV_TREE_NODE_TYPE_BRANCH , PV_TREE_NODE_TYPE_LEEF


class exVimPanel_ContextComplete( pvTabPanelItem ):
    def __init__( self ):
        self.buffer = pvListBuffer()

    def getBuffer( self ):
        return self.buffer

    def __str__( self ):
        return 'Context Complete'


class exVimPanel_BufferExplorer( pvTabPanelItem ):
    def __init__( self ):
        self.buffer = pvListBuffer()

    def getBuffer( self ):
        return self.buffer

    def __str__( self ):
        return 'Buffer Explorer'


class FENodeRoot( pvTreeNode ):
    def __init__( self ):
        super( FENodeRoot , self ).__init__( PV_TREE_NODE_TYPE_BRANCH )

    def __iter__( self ):
        for x in string.ascii_uppercase :
            driver_path = u'%s:\\' % x
            if os.path.isdir( driver_path ):
                yield FENodeDirectory( driver_path )

    def __unicode__( self ):
        return u''

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

    def __unicode__( self ):
        name = os.path.basename( self.path )
        return self.path if name == u'' else name

class FENodeFile( pvTreeNode ):
    def __init__( self , path ):
        super( FENodeFile , self ).__init__( PV_TREE_NODE_TYPE_LEEF )
        self.path = path

    def __unicode__( self ):
        return os.path.basename( self.path)


class exVimFileExplorer_NodeFactory( pvTreeNodeFactory ):
    def generateNode( self , path ):
        if path == [] :
            return FENodeRoot()
        else:
            full_path = os.path.join( *path )
            import types
            assert type( full_path ) ==  types.UnicodeType
            if os.path.isdir( full_path ):
                return FENodeDirectory( full_path )
            elif os.path.isfile( full_path ):
                return FENodeFile( full_path )
            else :
                return None


class exVimPanel_FileExplorer( pvTabPanelItem ):
    def __init__( self ):
        self.buffer = pvTreeBuffer( exVimFileExplorer_NodeFactory() )

    def getBuffer( self ):
        return self.buffer

    def __str__( self ):
        return 'File Explorer'

